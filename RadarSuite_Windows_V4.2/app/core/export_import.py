"""
RadarSuite v4.2.1 - Export/Import Module
ADDED v4.2.1: ZADANIE 5 - Configuration and model export/import

Features:
- Export/import full configuration (JSON)
- Export/import ML models (.rsmodel)
- Export/import training sessions (.rssession)
- Validation and versioning support
"""

import json
import shutil
import zipfile
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, Tuple, List
from dataclasses import dataclass, asdict

from .constants import VERSION
from .logger import log


@dataclass
class ExportResult:
    """Result of export operation."""
    success: bool
    file_path: Optional[str] = None
    error_message: Optional[str] = None
    items_exported: int = 0


@dataclass
class ImportResult:
    """Result of import operation."""
    success: bool
    error_message: Optional[str] = None
    items_imported: int = 0
    warnings: List[str] = None

    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []


class ExportImportManager:
    """
    Manages export/import operations for RadarSuite.

    Supports:
    - Configuration files (JSON)
    - ML models (ZIP with .rsmodel extension)
    - Training sessions (ZIP with .rssession extension)
    """

    # File extensions
    CONFIG_EXT = ".rscfg"
    MODEL_EXT = ".rsmodel"
    SESSION_EXT = ".rssession"

    # Magic header for validation
    MAGIC_HEADER = "RADARSUITE"

    def __init__(self, config_manager=None, session_manager=None):
        """
        Initialize export/import manager.

        Args:
            config_manager: ConfigManager instance for config operations
            session_manager: SessionManager instance for session operations
        """
        self.config_manager = config_manager
        self.session_manager = session_manager

    # ========================================================================
    # CONFIGURATION EXPORT/IMPORT
    # ========================================================================

    def export_config(self, config: Dict[str, Any], file_path: str) -> ExportResult:
        """
        Export configuration to file.

        Args:
            config: Configuration dictionary to export
            file_path: Output file path

        Returns:
            ExportResult with success status
        """
        try:
            # Add export metadata
            export_data = {
                "_radarsuite_export": {
                    "type": "configuration",
                    "version": VERSION,
                    "export_date": datetime.now().isoformat(),
                    "magic": self.MAGIC_HEADER
                },
                "config": config
            }

            # Ensure .rscfg extension
            if not file_path.endswith(self.CONFIG_EXT):
                file_path += self.CONFIG_EXT

            # Write JSON
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)

            log(f"Configuration exported to: {file_path}", "INFO")
            return ExportResult(
                success=True,
                file_path=file_path,
                items_exported=len(config)
            )

        except Exception as e:
            log(f"Configuration export failed: {e}", "ERROR")
            return ExportResult(
                success=False,
                error_message=str(e)
            )

    def import_config(self, file_path: str) -> Tuple[ImportResult, Optional[Dict[str, Any]]]:
        """
        Import configuration from file.

        Args:
            file_path: Input file path

        Returns:
            Tuple of (ImportResult, config_dict or None)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)

            # Validate header
            header = import_data.get("_radarsuite_export", {})
            if header.get("magic") != self.MAGIC_HEADER:
                return ImportResult(
                    success=False,
                    error_message="Invalid file format (not a RadarSuite export)"
                ), None

            if header.get("type") != "configuration":
                return ImportResult(
                    success=False,
                    error_message=f"Wrong file type: expected 'configuration', got '{header.get('type')}'"
                ), None

            config = import_data.get("config", {})

            # Check version compatibility
            warnings = []
            file_version = header.get("version", "unknown")
            if file_version != VERSION:
                warnings.append(f"Version mismatch: file is v{file_version}, current is v{VERSION}")

            log(f"Configuration imported from: {file_path}", "INFO")
            return ImportResult(
                success=True,
                items_imported=len(config),
                warnings=warnings
            ), config

        except json.JSONDecodeError as e:
            return ImportResult(
                success=False,
                error_message=f"Invalid JSON: {e}"
            ), None
        except Exception as e:
            log(f"Configuration import failed: {e}", "ERROR")
            return ImportResult(
                success=False,
                error_message=str(e)
            ), None

    # ========================================================================
    # ML MODEL EXPORT/IMPORT
    # ========================================================================

    def export_model(self, model_path: str, output_path: str,
                     metadata: Optional[Dict[str, Any]] = None) -> ExportResult:
        """
        Export ML model to portable format.

        Args:
            model_path: Path to trained model file
            output_path: Output file path
            metadata: Optional model metadata (accuracy, classes, etc.)

        Returns:
            ExportResult with success status
        """
        try:
            model_file = Path(model_path)
            if not model_file.exists():
                return ExportResult(
                    success=False,
                    error_message=f"Model file not found: {model_path}"
                )

            # Ensure .rsmodel extension
            if not output_path.endswith(self.MODEL_EXT):
                output_path += self.MODEL_EXT

            # Create ZIP archive with model and metadata
            with tempfile.TemporaryDirectory() as tmpdir:
                tmpdir_path = Path(tmpdir)

                # Copy model file
                model_dest = tmpdir_path / "model.pkl"
                shutil.copy(model_path, model_dest)

                # Create metadata file
                export_metadata = {
                    "_radarsuite_export": {
                        "type": "ml_model",
                        "version": VERSION,
                        "export_date": datetime.now().isoformat(),
                        "magic": self.MAGIC_HEADER
                    },
                    "model_info": metadata or {}
                }

                metadata_file = tmpdir_path / "metadata.json"
                with open(metadata_file, 'w', encoding='utf-8') as f:
                    json.dump(export_metadata, f, indent=2)

                # Create ZIP archive
                with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                    zf.write(model_dest, "model.pkl")
                    zf.write(metadata_file, "metadata.json")

            log(f"Model exported to: {output_path}", "INFO")
            return ExportResult(
                success=True,
                file_path=output_path,
                items_exported=1
            )

        except Exception as e:
            log(f"Model export failed: {e}", "ERROR")
            return ExportResult(
                success=False,
                error_message=str(e)
            )

    def import_model(self, file_path: str, output_dir: str) -> Tuple[ImportResult, Optional[str]]:
        """
        Import ML model from portable format.

        Args:
            file_path: Input .rsmodel file path
            output_dir: Directory to extract model to

        Returns:
            Tuple of (ImportResult, model_path or None)
        """
        try:
            if not zipfile.is_zipfile(file_path):
                return ImportResult(
                    success=False,
                    error_message="Invalid file format (not a ZIP archive)"
                ), None

            with zipfile.ZipFile(file_path, 'r') as zf:
                # Read metadata
                try:
                    with zf.open("metadata.json") as f:
                        metadata = json.load(f)
                except KeyError:
                    return ImportResult(
                        success=False,
                        error_message="Missing metadata.json in archive"
                    ), None

                # Validate header
                header = metadata.get("_radarsuite_export", {})
                if header.get("magic") != self.MAGIC_HEADER:
                    return ImportResult(
                        success=False,
                        error_message="Invalid file format (not a RadarSuite export)"
                    ), None

                if header.get("type") != "ml_model":
                    return ImportResult(
                        success=False,
                        error_message=f"Wrong file type: expected 'ml_model', got '{header.get('type')}'"
                    ), None

                # Extract model
                output_path = Path(output_dir)
                output_path.mkdir(parents=True, exist_ok=True)

                # Generate unique filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                model_filename = f"imported_model_{timestamp}.pkl"
                model_dest = output_path / model_filename

                with zf.open("model.pkl") as src:
                    with open(model_dest, 'wb') as dst:
                        dst.write(src.read())

                warnings = []
                file_version = header.get("version", "unknown")
                if file_version != VERSION:
                    warnings.append(f"Version mismatch: file is v{file_version}, current is v{VERSION}")

                log(f"Model imported to: {model_dest}", "INFO")
                return ImportResult(
                    success=True,
                    items_imported=1,
                    warnings=warnings
                ), str(model_dest)

        except Exception as e:
            log(f"Model import failed: {e}", "ERROR")
            return ImportResult(
                success=False,
                error_message=str(e)
            ), None

    # ========================================================================
    # SESSION EXPORT/IMPORT
    # ========================================================================

    def export_session(self, session_id: str, output_path: str) -> ExportResult:
        """
        Export training session to portable format.

        Args:
            session_id: Session ID to export
            output_path: Output file path

        Returns:
            ExportResult with success status
        """
        try:
            if self.session_manager is None:
                return ExportResult(
                    success=False,
                    error_message="Session manager not available"
                )

            # Get session data
            session = self.session_manager.load_session(session_id)
            if session is None:
                return ExportResult(
                    success=False,
                    error_message=f"Session not found: {session_id}"
                )

            # Ensure .rssession extension
            if not output_path.endswith(self.SESSION_EXT):
                output_path += self.SESSION_EXT

            # Create ZIP archive
            with tempfile.TemporaryDirectory() as tmpdir:
                tmpdir_path = Path(tmpdir)

                # Create session metadata
                export_metadata = {
                    "_radarsuite_export": {
                        "type": "session",
                        "version": VERSION,
                        "export_date": datetime.now().isoformat(),
                        "magic": self.MAGIC_HEADER
                    },
                    "session": {
                        "session_id": session.session_id,
                        "created_at": session.created_at.isoformat() if hasattr(session, 'created_at') else None,
                        "duration_sec": session.duration_sec,
                        "labels": [
                            {
                                "id": label.id,
                                "timestamp_sec": label.timestamp_sec,
                                "label_class": label.label_class,
                                "description": label.description
                            }
                            for label in session.labels
                        ]
                    }
                }

                metadata_file = tmpdir_path / "metadata.json"
                with open(metadata_file, 'w', encoding='utf-8') as f:
                    json.dump(export_metadata, f, indent=2)

                # Create ZIP
                with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                    zf.write(metadata_file, "metadata.json")

                    # Add audio file if exists
                    audio_path = self.session_manager.get_audio_path(session_id)
                    if audio_path and Path(audio_path).exists():
                        zf.write(audio_path, "audio.npy")

            log(f"Session exported to: {output_path}", "INFO")
            return ExportResult(
                success=True,
                file_path=output_path,
                items_exported=len(session.labels)
            )

        except Exception as e:
            log(f"Session export failed: {e}", "ERROR")
            return ExportResult(
                success=False,
                error_message=str(e)
            )

    def import_session(self, file_path: str) -> ImportResult:
        """
        Import training session from portable format.

        Args:
            file_path: Input .rssession file path

        Returns:
            ImportResult with success status
        """
        try:
            if self.session_manager is None:
                return ImportResult(
                    success=False,
                    error_message="Session manager not available"
                )

            if not zipfile.is_zipfile(file_path):
                return ImportResult(
                    success=False,
                    error_message="Invalid file format (not a ZIP archive)"
                )

            with zipfile.ZipFile(file_path, 'r') as zf:
                # Read metadata
                try:
                    with zf.open("metadata.json") as f:
                        metadata = json.load(f)
                except KeyError:
                    return ImportResult(
                        success=False,
                        error_message="Missing metadata.json in archive"
                    ), None

                # Validate header
                header = metadata.get("_radarsuite_export", {})
                if header.get("magic") != self.MAGIC_HEADER:
                    return ImportResult(
                        success=False,
                        error_message="Invalid file format (not a RadarSuite export)"
                    )

                if header.get("type") != "session":
                    return ImportResult(
                        success=False,
                        error_message=f"Wrong file type: expected 'session', got '{header.get('type')}'"
                    )

                # Import session via session manager
                session_data = metadata.get("session", {})

                # Generate new session ID to avoid conflicts
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_session_id = f"imported_{timestamp}"

                # Create session
                result = self.session_manager.create_imported_session(
                    session_id=new_session_id,
                    labels=session_data.get("labels", []),
                    duration_sec=session_data.get("duration_sec", 0.0)
                )

                if not result:
                    return ImportResult(
                        success=False,
                        error_message="Failed to create session in session manager"
                    )

                # Extract audio if present
                if "audio.npy" in zf.namelist():
                    audio_dest = self.session_manager.get_audio_path(new_session_id)
                    if audio_dest:
                        with zf.open("audio.npy") as src:
                            with open(audio_dest, 'wb') as dst:
                                dst.write(src.read())

                warnings = []
                file_version = header.get("version", "unknown")
                if file_version != VERSION:
                    warnings.append(f"Version mismatch: file is v{file_version}, current is v{VERSION}")

                log(f"Session imported: {new_session_id}", "INFO")
                return ImportResult(
                    success=True,
                    items_imported=len(session_data.get("labels", [])),
                    warnings=warnings
                )

        except Exception as e:
            log(f"Session import failed: {e}", "ERROR")
            return ImportResult(
                success=False,
                error_message=str(e)
            )

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    @staticmethod
    def get_file_filter(export_type: str) -> str:
        """
        Get file filter string for file dialogs.

        Args:
            export_type: 'config', 'model', or 'session'

        Returns:
            File filter string for QFileDialog
        """
        filters = {
            "config": "RadarSuite Configuration (*.rscfg);;All Files (*.*)",
            "model": "RadarSuite Model (*.rsmodel);;All Files (*.*)",
            "session": "RadarSuite Session (*.rssession);;All Files (*.*)",
        }
        return filters.get(export_type, "All Files (*.*)")

    @staticmethod
    def validate_file(file_path: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Validate a RadarSuite export file.

        Args:
            file_path: Path to file to validate

        Returns:
            Tuple of (is_valid, file_type, metadata_or_error)
        """
        try:
            # Try JSON first (config files)
            if file_path.endswith(ExportImportManager.CONFIG_EXT):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                header = data.get("_radarsuite_export", {})
                if header.get("magic") == ExportImportManager.MAGIC_HEADER:
                    return True, header.get("type", "unknown"), header
                return False, "invalid", {"error": "Invalid magic header"}

            # Try ZIP (model/session files)
            if zipfile.is_zipfile(file_path):
                with zipfile.ZipFile(file_path, 'r') as zf:
                    if "metadata.json" in zf.namelist():
                        with zf.open("metadata.json") as f:
                            metadata = json.load(f)

                        header = metadata.get("_radarsuite_export", {})
                        if header.get("magic") == ExportImportManager.MAGIC_HEADER:
                            return True, header.get("type", "unknown"), header

            return False, "unknown", {"error": "Unrecognized file format"}

        except Exception as e:
            return False, "error", {"error": str(e)}
