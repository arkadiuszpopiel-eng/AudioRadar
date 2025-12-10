"""
Radar Games ML v4.3.0 - Session Integrity Validator

Validates and repairs corrupted ML training sessions.
Ensures data integrity and prevents data loss.

FEATURES:
- Validates metadata.json, labels.json, audio.npy existence
- Cross-validates metadata vs actual audio duration
- Detects empty/corrupted files
- Auto-repair for recoverable corruptions
- Integrity checks on startup
"""

import json
import numpy as np
from pathlib import Path
from typing import Tuple, List, Optional, Dict
from dataclasses import dataclass

from app.core.logger import log


@dataclass
class ValidationResult:
    """Result of session validation."""
    session_id: str
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    can_repair: bool


class SessionValidator:
    """
    Validates session integrity and repairs corrupted sessions.

    v4.3.0-k0001: Prevents data loss from interrupted saves
    """

    def __init__(self):
        """Initialize session validator."""
        log("SessionValidator initialized", "INFO")

    def validate_session(self, session_dir: Path) -> ValidationResult:
        """
        Validate session completeness and integrity.

        Args:
            session_dir: Path to session directory

        Returns:
            ValidationResult with detailed status
        """
        session_id = session_dir.name
        errors = []
        warnings = []
        can_repair = False

        log(f"Validating session: {session_id}", "INFO")

        # Check if directory exists
        if not session_dir.exists():
            errors.append("Session directory does not exist")
            return ValidationResult(session_id, False, errors, warnings, False)

        # Check metadata.json
        metadata_path = session_dir / "metadata.json"
        if not metadata_path.exists():
            errors.append("Missing metadata.json")
        else:
            try:
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
            except Exception as e:
                errors.append(f"Corrupted metadata.json: {e}")
                metadata = None

        # Check labels.json
        labels_path = session_dir / "labels.json"
        if not labels_path.exists():
            errors.append("Missing labels.json")
        else:
            try:
                with open(labels_path, 'r', encoding='utf-8') as f:
                    labels_data = json.load(f)
            except Exception as e:
                errors.append(f"Corrupted labels.json: {e}")
                labels_data = None

        # Check audio.npy
        audio_path = session_dir / "audio.npy"
        audio_data = None
        if not audio_path.exists():
            warnings.append("Missing audio.npy (session may be in progress)")
        else:
            try:
                audio_data = np.load(audio_path)
                if audio_data.size == 0:
                    errors.append("Empty audio.npy (no audio recorded)")
            except Exception as e:
                errors.append(f"Corrupted audio.npy: {e}")
                audio_data = None

        # Cross-validate metadata vs audio
        if metadata and audio_data is not None and len(errors) == 0:
            duration = metadata.get("duration_sec", 0)
            sample_rate = metadata.get("sample_rate", 48000)
            channels = metadata.get("channels", 2)

            expected_samples = int(duration * sample_rate)
            actual_samples = len(audio_data)

            # Allow 1 second tolerance (one chunk)
            tolerance = sample_rate
            if abs(actual_samples - expected_samples) > tolerance:
                warnings.append(
                    f"Duration mismatch: metadata={duration:.1f}s, "
                    f"audio={actual_samples/sample_rate:.1f}s"
                )
                # This is repairable - we can update metadata
                can_repair = True

        # Determine if session can be repaired
        if not errors and warnings:
            can_repair = True
        elif len(errors) == 1 and "Missing audio.npy" in errors[0]:
            # Session without audio can be kept (just labels)
            can_repair = True

        is_valid = len(errors) == 0

        log(f"Validation result for {session_id}: valid={is_valid}, "
            f"errors={len(errors)}, warnings={len(warnings)}, can_repair={can_repair}",
            "INFO")

        return ValidationResult(session_id, is_valid, errors, warnings, can_repair)

    def auto_repair_session(self, session_dir: Path) -> bool:
        """
        Attempt to repair corrupted session.

        Args:
            session_dir: Path to session directory

        Returns:
            True if repair successful
        """
        session_id = session_dir.name
        log(f"Attempting to repair session: {session_id}", "INFO")

        try:
            metadata_path = session_dir / "metadata.json"
            audio_path = session_dir / "audio.npy"

            # Repair 1: Update duration from actual audio
            if metadata_path.exists() and audio_path.exists():
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)

                audio_data = np.load(audio_path)
                sample_rate = metadata.get("sample_rate", 48000)
                actual_duration = len(audio_data) / sample_rate

                if abs(metadata.get("duration_sec", 0) - actual_duration) > 1.0:
                    metadata["duration_sec"] = actual_duration

                    with open(metadata_path, 'w', encoding='utf-8') as f:
                        json.dump(metadata, f, indent=2)

                    log(f"Repaired duration mismatch: {actual_duration:.1f}s", "INFO")
                    return True

            # Repair 2: Create empty labels.json if missing
            labels_path = session_dir / "labels.json"
            if not labels_path.exists() and metadata_path.exists():
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)

                empty_labels = {
                    "session_id": metadata.get("session_id", session_id),
                    "labels": []
                }

                with open(labels_path, 'w', encoding='utf-8') as f:
                    json.dump(empty_labels, f, indent=2)

                log("Created empty labels.json", "INFO")
                return True

            return False

        except Exception as e:
            log(f"Repair failed for {session_id}: {e}", "ERROR")
            return False

    def validate_all_sessions(self, sessions_dir: Path) -> List[ValidationResult]:
        """
        Validate all sessions in directory.

        Args:
            sessions_dir: Path to LabeledSessions directory

        Returns:
            List of validation results
        """
        if not sessions_dir.exists():
            log(f"Sessions directory does not exist: {sessions_dir}", "WARNING")
            return []

        results = []
        session_dirs = [d for d in sessions_dir.iterdir() if d.is_dir() and d.name.startswith("session_")]

        log(f"Validating {len(session_dirs)} sessions...", "INFO")

        for session_dir in session_dirs:
            result = self.validate_session(session_dir)
            results.append(result)

        # Summary
        valid_count = sum(1 for r in results if r.is_valid)
        invalid_count = len(results) - valid_count
        repairable_count = sum(1 for r in results if not r.is_valid and r.can_repair)

        log(f"Validation complete: {valid_count} valid, {invalid_count} invalid "
            f"({repairable_count} repairable)", "INFO")

        return results

    def auto_repair_all_sessions(self, sessions_dir: Path) -> Dict[str, bool]:
        """
        Auto-repair all repairable sessions.

        Args:
            sessions_dir: Path to LabeledSessions directory

        Returns:
            Dict of session_id -> repair_success
        """
        validation_results = self.validate_all_sessions(sessions_dir)
        repair_results = {}

        for result in validation_results:
            if not result.is_valid and result.can_repair:
                session_dir = sessions_dir / result.session_id
                success = self.auto_repair_session(session_dir)
                repair_results[result.session_id] = success

        if repair_results:
            success_count = sum(1 for s in repair_results.values() if s)
            log(f"Auto-repair complete: {success_count}/{len(repair_results)} repaired successfully", "INFO")

        return repair_results
