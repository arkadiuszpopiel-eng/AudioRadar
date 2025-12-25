"""
Radar Games ML v4.3.0-k0001 - ML Footstep Detector
Real-time inference using trained ML models for footstep detection

Features:
- Integration with ModelRegistry for auto-loading best model
- Real-time feature extraction and classification
- Fallback to rule-based detection if no model loaded
- Confidence scoring and class prediction
"""

import numpy as np
from typing import Optional, Dict, Any, Tuple, List
from pathlib import Path

from app.core.logger import log
from app.ml.feature_extractor import FeatureExtractor
from app.ml.model_registry import ModelRegistry, ModelInfo, get_model_registry


class MLFootstepDetector:
    """
    ML-powered footstep detector for real-time inference.

    Uses trained models from ModelRegistry to classify audio segments.
    Falls back to rule-based detection if no model is available.
    """

    def __init__(self, sample_rate: int = 48000, auto_load_best: bool = True):
        """
        Initialize ML footstep detector.

        Args:
            sample_rate: Audio sample rate (Hz)
            auto_load_best: If True, automatically load best model on init
        """
        self.sample_rate = sample_rate
        self.feature_extractor = FeatureExtractor(source_sample_rate=sample_rate)
        self.registry = get_model_registry()

        # Model state
        self._model: Optional[Any] = None
        self._class_names: List[str] = []
        self._model_info: Optional[ModelInfo] = None
        self._is_loaded = False

        # Inference state
        self._last_prediction: Optional[str] = None
        self._last_confidence: float = 0.0

        log(f"MLFootstepDetector initialized (sample_rate={sample_rate})", "INFO")

        if auto_load_best:
            self.load_best_model()

    @property
    def is_model_loaded(self) -> bool:
        """Check if a model is currently loaded."""
        return self._is_loaded and self._model is not None

    @property
    def model_info(self) -> Optional[ModelInfo]:
        """Get info about the currently loaded model."""
        return self._model_info

    def load_best_model(self) -> bool:
        """
        Load the best available model from registry.

        Returns:
            True if model loaded successfully
        """
        result = self.registry.load_best_model()
        if not result:
            log("No trained models available for auto-load", "WARNING")
            self._is_loaded = False
            return False

        model, class_names, model_info = result
        self._model = model
        self._class_names = class_names
        self._model_info = model_info
        self._is_loaded = True

        log(f"Best model loaded: {model_info.name} (accuracy: {model_info.accuracy:.1%})", "INFO")
        return True

    def load_model(self, model_name: str) -> bool:
        """
        Load a specific model by name.

        Args:
            model_name: Name of model to load

        Returns:
            True if model loaded successfully
        """
        result = self.registry.load_model(model_name)
        if not result:
            log(f"Failed to load model: {model_name}", "ERROR")
            self._is_loaded = False
            return False

        model, class_names = result
        self._model = model
        self._class_names = class_names
        self._model_info = self.registry.get_model_info(model_name)
        self._is_loaded = True

        log(f"Model loaded: {model_name}", "INFO")
        return True

    def unload_model(self) -> None:
        """Unload the current model."""
        self._model = None
        self._class_names = []
        self._model_info = None
        self._is_loaded = False
        log("Model unloaded", "DEBUG")

    def predict(self, audio_segment: np.ndarray) -> Optional[Dict[str, Any]]:
        """
        Predict footstep class for audio segment.

        Args:
            audio_segment: Audio data (1D numpy array)

        Returns:
            Dictionary with prediction results:
            {
                'class': str,           # Predicted class name
                'confidence': float,    # Confidence score (0-1)
                'probabilities': dict,  # Class probabilities
                'model_name': str       # Name of model used
            }
            Returns None if no model loaded or prediction fails
        """
        if not self.is_model_loaded:
            log("No model loaded for prediction", "WARNING")
            return None

        try:
            # Extract features (mel-spectrogram)
            features = self.feature_extractor.extract_mel_spectrogram(
                audio_segment,
                n_mels=self._model_info.config.get('n_mels', 64),
                n_fft=self._model_info.config.get('n_fft', 512),
                hop_length=self._model_info.config.get('hop_length', 160)
            )

            # Flatten features for sklearn model
            features_flat = features.flatten().reshape(1, -1)

            # Predict
            predicted_class_idx = self._model.predict(features_flat)[0]
            predicted_class = self._class_names[predicted_class_idx]

            # Get probabilities if available
            probabilities = {}
            if hasattr(self._model, 'predict_proba'):
                proba = self._model.predict_proba(features_flat)[0]
                probabilities = {
                    class_name: float(prob)
                    for class_name, prob in zip(self._class_names, proba)
                }
                confidence = float(proba[predicted_class_idx])
            else:
                confidence = 1.0  # No probability info available

            # Store for history
            self._last_prediction = predicted_class
            self._last_confidence = confidence

            result = {
                'class': predicted_class,
                'confidence': confidence,
                'probabilities': probabilities,
                'model_name': self._model_info.name,
                'model_accuracy': self._model_info.accuracy
            }

            log(f"Prediction: {predicted_class} (confidence: {confidence:.2f})", "DEBUG")
            return result

        except Exception as e:
            log(f"Prediction error: {e}", "ERROR")
            return None

    def predict_with_fallback(
        self,
        audio_segment: np.ndarray,
        fallback_detector=None
    ) -> Dict[str, Any]:
        """
        Predict with fallback to rule-based detector.

        Args:
            audio_segment: Audio data
            fallback_detector: Fallback detector to use if ML fails

        Returns:
            Prediction dict with 'source' field indicating 'ml' or 'fallback'
        """
        result = self.predict(audio_segment)

        if result is not None:
            result['source'] = 'ml'
            return result

        # Fallback to rule-based
        if fallback_detector and hasattr(fallback_detector, 'analyze_footstep'):
            fallback_result = fallback_detector.analyze_footstep(
                audio_segment,
                self.sample_rate
            )
            return {
                'class': 'footstep' if fallback_result.get('is_human_step') else 'unknown',
                'confidence': fallback_result.get('confidence', 0.0) / 100.0,
                'probabilities': {},
                'model_name': 'fallback_rule_based',
                'model_accuracy': 0.0,
                'source': 'fallback',
                'fallback_data': fallback_result
            }

        # No prediction available
        return {
            'class': 'unknown',
            'confidence': 0.0,
            'probabilities': {},
            'model_name': 'none',
            'model_accuracy': 0.0,
            'source': 'none'
        }

    def get_stats(self) -> dict:
        """
        Get detector statistics.

        Returns:
            Dictionary with detector stats
        """
        return {
            'model_loaded': self.is_model_loaded,
            'model_name': self._model_info.name if self._model_info else None,
            'model_accuracy': self._model_info.accuracy if self._model_info else 0.0,
            'num_classes': len(self._class_names),
            'class_names': self._class_names,
            'last_prediction': self._last_prediction,
            'last_confidence': self._last_confidence,
            'sample_rate': self.sample_rate
        }
