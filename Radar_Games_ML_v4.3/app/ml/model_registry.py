"""
Radar Games ML v4.3.0-k0001 - Model Registry
Manages trained ML models: loading, caching, auto-selection

Features:
- Model discovery and metadata parsing
- Automatic best model selection (by accuracy)
- Model caching for fast inference
- Model validation and integrity checks
"""

import json
import joblib
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime

from app.core.logger import log
from app.core.constants import VERSION


@dataclass
class ModelInfo:
    """Metadata for a trained model."""
    name: str
    path: Path
    created_at: str
    accuracy: float
    class_names: List[str]
    samples_used: int
    app_version: str
    config: Dict[str, Any]

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": str(self.path),
            "created_at": self.created_at,
            "accuracy": self.accuracy,
            "class_names": self.class_names,
            "samples_used": self.samples_used,
            "app_version": self.app_version,
            "config": self.config
        }


class ModelRegistry:
    """
    Registry for managing trained ML models.

    Provides:
    - Model discovery and listing
    - Best model auto-selection
    - Model loading with caching
    - Metadata parsing and validation
    """

    def __init__(self, models_dir: Path = None):
        """
        Initialize model registry.

        Args:
            models_dir: Directory containing trained models (default: ml_sessions/models)
        """
        if models_dir is None:
            from app.core.constants import ML_SESSIONS_DIR
            models_dir = Path(ML_SESSIONS_DIR) / "models"

        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)

        # Model cache: {model_name: (model, class_names)}
        self._model_cache: Dict[str, Tuple[Any, List[str]]] = {}

        log(f"ModelRegistry initialized: {self.models_dir}", "INFO")

    def list_models(self) -> List[ModelInfo]:
        """
        List all available trained models.

        Returns:
            List of ModelInfo objects sorted by accuracy (descending)
        """
        models = []

        for model_dir in self.models_dir.iterdir():
            if not model_dir.is_dir():
                continue

            # Check for required files
            metadata_path = model_dir / "metadata.json"
            model_path = model_dir / "model.joblib"

            if not metadata_path.exists() or not model_path.exists():
                log(f"Skipping incomplete model: {model_dir.name}", "WARNING")
                continue

            try:
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)

                model_info = ModelInfo(
                    name=model_dir.name,
                    path=model_dir,
                    created_at=metadata.get("created_at", "Unknown"),
                    accuracy=metadata.get("accuracy", 0.0),
                    class_names=metadata.get("class_names", []),
                    samples_used=metadata.get("samples_used", 0),
                    app_version=metadata.get("app_version", "Unknown"),
                    config=metadata.get("config", {})
                )
                models.append(model_info)

            except Exception as e:
                log(f"Error reading model {model_dir.name}: {e}", "WARNING")

        # Sort by accuracy (descending)
        models.sort(key=lambda x: x.accuracy, reverse=True)

        return models

    def get_best_model(self) -> Optional[ModelInfo]:
        """
        Get the best available model (highest accuracy).

        Returns:
            ModelInfo of best model, or None if no models found
        """
        models = self.list_models()
        if not models:
            log("No trained models found", "WARNING")
            return None

        best_model = models[0]
        log(f"Best model: {best_model.name} (accuracy: {best_model.accuracy:.1%})", "INFO")
        return best_model

    def load_model(self, model_name: str, use_cache: bool = True) -> Optional[Tuple[Any, List[str]]]:
        """
        Load a trained model by name.

        Args:
            model_name: Name of model directory (e.g., "radarsuite_custom_20250101_120000")
            use_cache: If True, use cached model if available

        Returns:
            Tuple of (model, class_names) or None if load fails
        """
        # Check cache first
        if use_cache and model_name in self._model_cache:
            log(f"Model loaded from cache: {model_name}", "DEBUG")
            return self._model_cache[model_name]

        model_dir = self.models_dir / model_name
        if not model_dir.exists():
            log(f"Model directory not found: {model_name}", "ERROR")
            return None

        try:
            # Load model
            model_path = model_dir / "model.joblib"
            if not model_path.exists():
                log(f"Model file not found: {model_path}", "ERROR")
                return None

            model = joblib.load(model_path)

            # Load metadata for class names
            metadata_path = model_dir / "metadata.json"
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)

            class_names = metadata.get("class_names", [])

            if not class_names:
                log(f"No class names found in metadata for {model_name}", "WARNING")

            # Cache the model
            self._model_cache[model_name] = (model, class_names)

            log(f"Model loaded: {model_name} ({len(class_names)} classes)", "INFO")
            return (model, class_names)

        except Exception as e:
            log(f"Error loading model {model_name}: {e}", "ERROR")
            return None

    def load_best_model(self) -> Optional[Tuple[Any, List[str], ModelInfo]]:
        """
        Load the best available model (highest accuracy).

        Returns:
            Tuple of (model, class_names, model_info) or None if no models available
        """
        best_info = self.get_best_model()
        if not best_info:
            return None

        result = self.load_model(best_info.name)
        if not result:
            return None

        model, class_names = result
        return (model, class_names, best_info)

    def get_model_info(self, model_name: str) -> Optional[ModelInfo]:
        """
        Get metadata for a specific model.

        Args:
            model_name: Name of model directory

        Returns:
            ModelInfo object or None if not found
        """
        models = self.list_models()
        for model_info in models:
            if model_info.name == model_name:
                return model_info
        return None

    def delete_model(self, model_name: str) -> bool:
        """
        Delete a trained model.

        Args:
            model_name: Name of model directory to delete

        Returns:
            True if deletion successful
        """
        model_dir = self.models_dir / model_name
        if not model_dir.exists():
            log(f"Model not found for deletion: {model_name}", "WARNING")
            return False

        try:
            import shutil
            shutil.rmtree(model_dir)

            # Remove from cache
            if model_name in self._model_cache:
                del self._model_cache[model_name]

            log(f"Model deleted: {model_name}", "INFO")
            return True

        except Exception as e:
            log(f"Error deleting model {model_name}: {e}", "ERROR")
            return False

    def clear_cache(self) -> None:
        """Clear the model cache."""
        self._model_cache.clear()
        log("Model cache cleared", "DEBUG")

    def get_stats(self) -> dict:
        """
        Get registry statistics.

        Returns:
            Dictionary with stats (total models, best accuracy, cache size, etc.)
        """
        models = self.list_models()
        best = self.get_best_model()

        return {
            "total_models": len(models),
            "cached_models": len(self._model_cache),
            "best_accuracy": best.accuracy if best else 0.0,
            "best_model_name": best.name if best else None,
            "models_dir": str(self.models_dir),
        }


# Singleton instance
_registry_instance: Optional[ModelRegistry] = None


def get_model_registry() -> ModelRegistry:
    """Get the global ModelRegistry instance."""
    global _registry_instance
    if _registry_instance is None:
        _registry_instance = ModelRegistry()
    return _registry_instance


def reset_model_registry() -> None:
    """Reset the global ModelRegistry instance."""
    global _registry_instance
    _registry_instance = None
