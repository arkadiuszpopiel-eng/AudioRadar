"""
RadarSuite v3.5.0 - Detection_Panel Widgets
"""

import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QSlider, QCheckBox, QSpinBox, QGroupBox, QFormLayout
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QPalette

from core import log, tr, TOAST_DURATION_MS, TOAST_MAX_COUNT
from detection import HumanFootstepDetector
from audio import HumanVoiceDetector


class DetectionPanel(QWidget):
    """Sound detection configuration and status"""

    def __init__(self):
        super().__init__()
        log("DetectionPanel.__init__", "INFO")

        # Initialize advanced detectors (v3.0)
        self.footstep_detector = HumanFootstepDetector()
        self.voice_detector = HumanVoiceDetector()

        layout = QVBoxLayout()

        # Profile selection
        self.profile_group = QGroupBox(tr('detection_profile'))
        profile_layout = QVBoxLayout()

        self.profile_combo = QComboBox()
        self.profile_combo.addItems([
            'Universal',
            'ARC Raiders (PC)',
            'ARC Raiders + SB Z SE + Cloud II'
        ])
        self.profile_combo.setCurrentText('ARC Raiders + SB Z SE + Cloud II')
        profile_layout.addWidget(self.profile_combo)

        self.profile_group.setLayout(profile_layout)
        layout.addWidget(self.profile_group)

        # Detection enables
        self.enable_group = QGroupBox(tr('enable_detection'))
        enable_layout = QVBoxLayout()

        self.walk_enable = QCheckBox(tr('detect_walk'))
        self.walk_enable.setChecked(True)
        enable_layout.addWidget(self.walk_enable)

        self.run_enable = QCheckBox(tr('detect_run'))
        self.run_enable.setChecked(True)
        enable_layout.addWidget(self.run_enable)

        self.shot_enable = QCheckBox(tr('detect_shot'))
        self.shot_enable.setChecked(True)
        enable_layout.addWidget(self.shot_enable)

        self.enable_group.setLayout(enable_layout)
        layout.addWidget(self.enable_group)

        # Sensitivity sliders
        self.sens_group = QGroupBox(tr('sensitivity'))
        sens_layout = QVBoxLayout()

        # Walk
        walk_layout = QHBoxLayout()
        self.walk_label_sens = QLabel(tr('walk'))
        walk_layout.addWidget(self.walk_label_sens)
        self.walk_sens = QSlider(Qt.Horizontal)
        self.walk_sens.setRange(1, 100)
        self.walk_sens.setValue(50)  # FIXED v3.5.3: More sensitive (was 35)
        walk_layout.addWidget(self.walk_sens)
        self.walk_sens_label = QLabel("50")
        self.walk_sens.valueChanged.connect(lambda v: self.walk_sens_label.setText(str(v)))
        walk_layout.addWidget(self.walk_sens_label)
        sens_layout.addLayout(walk_layout)

        # Run
        run_layout = QHBoxLayout()
        self.run_label_sens = QLabel(tr('run'))
        run_layout.addWidget(self.run_label_sens)
        self.run_sens = QSlider(Qt.Horizontal)
        self.run_sens.setRange(1, 100)
        self.run_sens.setValue(50)  # FIXED v3.5.3: More sensitive (was 35)
        run_layout.addWidget(self.run_sens)
        self.run_sens_label = QLabel("50")
        self.run_sens.valueChanged.connect(lambda v: self.run_sens_label.setText(str(v)))
        run_layout.addWidget(self.run_sens_label)
        sens_layout.addLayout(run_layout)

        # Shot
        shot_layout = QHBoxLayout()
        self.shot_label_sens = QLabel(tr('shot'))
        shot_layout.addWidget(self.shot_label_sens)
        self.shot_sens = QSlider(Qt.Horizontal)
        self.shot_sens.setRange(1, 100)
        self.shot_sens.setValue(60)  # FIXED v3.5.3: More sensitive (was 45)
        shot_layout.addWidget(self.shot_sens)
        self.shot_sens_label = QLabel("60")
        self.shot_sens.valueChanged.connect(lambda v: self.shot_sens_label.setText(str(v)))
        shot_layout.addWidget(self.shot_sens_label)
        sens_layout.addLayout(shot_layout)

        self.sens_group.setLayout(sens_layout)
        layout.addWidget(self.sens_group)

        # Human Footstep Analysis (v3.0)
        self.footstep_group = QGroupBox("Human Footstep Analysis (v3.0)")
        footstep_layout = QVBoxLayout()

        self.human_confidence_label = QLabel("Confidence: —")
        self.human_confidence_label.setStyleSheet("font-size: 10pt; color: #888888;")
        footstep_layout.addWidget(self.human_confidence_label)

        self.cadence_label = QLabel("Cadence: —")
        self.cadence_label.setStyleSheet("font-size: 10pt; color: #888888;")
        footstep_layout.addWidget(self.cadence_label)

        self.foot_label = QLabel("Foot: —")
        self.foot_label.setStyleSheet("font-size: 10pt; color: #888888;")
        footstep_layout.addWidget(self.foot_label)

        self.surface_label = QLabel("Surface: —")
        self.surface_label.setStyleSheet("font-size: 10pt; color: #888888;")
        footstep_layout.addWidget(self.surface_label)

        self.distance_label = QLabel("Distance: —")
        self.distance_label.setStyleSheet("font-size: 10pt; color: #888888;")
        footstep_layout.addWidget(self.distance_label)

        self.gait_label = QLabel("Gait: —")
        self.gait_label.setStyleSheet("font-size: 10pt; color: #888888;")
        footstep_layout.addWidget(self.gait_label)

        self.footstep_group.setLayout(footstep_layout)
        layout.addWidget(self.footstep_group)

        # Human Voice Analysis (v3.0)
        self.voice_group = QGroupBox("Human Voice Analysis (v3.0)")
        voice_layout = QVBoxLayout()

        self.voice_confidence_label = QLabel("Confidence: —")
        self.voice_confidence_label.setStyleSheet("font-size: 10pt; color: #888888;")
        voice_layout.addWidget(self.voice_confidence_label)

        self.voice_type_label = QLabel("Voice Type: —")
        self.voice_type_label.setStyleSheet("font-size: 10pt; color: #888888;")
        voice_layout.addWidget(self.voice_type_label)

        self.pitch_label = QLabel("Pitch: — Hz")
        self.pitch_label.setStyleSheet("font-size: 10pt; color: #888888;")
        voice_layout.addWidget(self.pitch_label)

        self.intensity_label = QLabel("Intensity: —")
        self.intensity_label.setStyleSheet("font-size: 10pt; color: #888888;")
        voice_layout.addWidget(self.intensity_label)

        self.communication_label = QLabel("Communication: —")
        self.communication_label.setStyleSheet("font-size: 10pt; color: #888888;")
        voice_layout.addWidget(self.communication_label)

        self.breathing_label = QLabel("Breathing: —")
        self.breathing_label.setStyleSheet("font-size: 10pt; color: #888888;")
        voice_layout.addWidget(self.breathing_label)

        self.voice_group.setLayout(voice_layout)
        layout.addWidget(self.voice_group)

        # Detection status
        self.status_group = QGroupBox(tr('detection_status'))
        status_layout = QVBoxLayout()

        self.walk_label = QLabel(tr('walk_none'))
        self.walk_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        status_layout.addWidget(self.walk_label)

        self.run_label = QLabel(tr('run_none'))
        self.run_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        status_layout.addWidget(self.run_label)

        self.shot_label = QLabel(tr('shot_none'))
        self.shot_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        status_layout.addWidget(self.shot_label)

        self.status_group.setLayout(status_layout)
        layout.addWidget(self.status_group)

        layout.addStretch()
        self.setLayout(layout)

        self.walk_hold = 0
        self.run_hold = 0
        self.shot_hold = 0

    def analyze(self, block, sample_rate, fft_cache=None):
        """Analyze audio block for walk/run/shot detection (Module 12: optimized with FFT caching)"""
        try:
            # Use cached FFT if available (Module 12 - Performance Optimization)
            if fft_cache is not None:
                fft_data = fft_cache['fft_data']
                freqs = fft_cache['freqs']
                power = fft_cache['power']
            else:
                # Fallback: compute FFT (legacy mode)
                if block.ndim == 2:
                    mono = np.mean(block, axis=1)
                else:
                    mono = block.ravel()

                window = np.hanning(len(mono))
                windowed = mono * window

                fft_data = np.fft.rfft(windowed)
                freqs = np.fft.rfftfreq(len(mono), d=1.0/sample_rate)
                power = np.abs(fft_data)

            low_mask = (freqs >= 20) & (freqs < 200)
            mid_mask = (freqs >= 200) & (freqs < 1500)
            high_mask = (freqs >= 1500) & (freqs < 6000)

            low_power = power[low_mask]
            mid_power = power[mid_mask]
            high_power = power[high_mask]

            total_power = np.mean(power) + 1e-9

            # FIXED v3.5.3: Use max() instead of mean() for better peak detection
            low_r = np.max(low_power) / total_power if len(low_power) > 0 else 0.0
            mid_r = np.max(mid_power) / total_power if len(mid_power) > 0 else 0.0
            high_r = np.max(high_power) / total_power if len(high_power) > 0 else 0.0

            # FIXED v3.5.3: Lower base thresholds for more sensitive detection
            walk_i = self.band_intensity(low_r, 0.04, self.walk_sens.value() / 100.0)
            run_i = self.band_intensity(mid_r, 0.03, self.run_sens.value() / 100.0)
            shot_i = self.band_intensity(high_r, 0.06, self.shot_sens.value() / 100.0)

            walk_det = walk_i > 0.0 and self.walk_enable.isChecked()
            run_det = run_i > 0.0 and self.run_enable.isChecked()
            shot_det = shot_i > 0.0 and self.shot_enable.isChecked()

            # FIXED v3.5.3: Reduced hold time for faster UI response
            if walk_det:
                self.walk_hold = 3
            if run_det:
                self.run_hold = 3
            if shot_det:
                self.shot_hold = 3

            if self.walk_hold > 0:
                self.walk_hold -= 1
                self.walk_label.setText(tr('walk_detected'))
                self.walk_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #00FF00;")
            else:
                self.walk_label.setText(tr('walk_none'))
                self.walk_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #666666;")

            if self.run_hold > 0:
                self.run_hold -= 1
                self.run_label.setText(tr('run_detected'))
                self.run_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #FFA500;")
            else:
                self.run_label.setText(tr('run_none'))
                self.run_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #666666;")

            if self.shot_hold > 0:
                self.shot_hold -= 1
                self.shot_label.setText(tr('shot_detected'))
                self.shot_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #FF0000;")
            else:
                self.shot_label.setText(tr('shot_none'))
                self.shot_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #666666;")

            events = {
                'walk': walk_det,
                'run': run_det,
                'shot': shot_det,
                'walk_int': walk_i,
                'run_int': run_i,
                'shot_int': shot_i
            }

            bands = {
                'low_r': low_r,
                'mid_r': mid_r,
                'high_r': high_r
            }

            # Advanced human footstep analysis (v3.0)
            footstep_result = self.footstep_detector.analyze_footstep(block, sample_rate, stereo=(block.ndim == 2))

            # Update UI with footstep analysis
            if footstep_result['is_human_step']:
                conf = footstep_result['confidence']
                color = "#00FF00" if conf > 75 else "#FFA500" if conf > 50 else "#FFFF00"

                self.human_confidence_label.setText(f"Confidence: {conf:.1f}%")
                self.human_confidence_label.setStyleSheet(f"font-size: 10pt; font-weight: bold; color: {color};")

                self.cadence_label.setText(f"Cadence: {footstep_result['cadence']:.2f} steps/s")
                self.cadence_label.setStyleSheet(f"font-size: 10pt; color: {color};")

                foot_icon = "👣L" if footstep_result['foot'] == 'left' else "👣R" if footstep_result['foot'] == 'right' else "👣"
                self.foot_label.setText(f"Foot: {foot_icon} {footstep_result['foot'].upper()}")
                self.foot_label.setStyleSheet(f"font-size: 10pt; color: {color};")

                self.surface_label.setText(f"Surface: {footstep_result['surface'].upper()}")
                self.surface_label.setStyleSheet(f"font-size: 10pt; color: {color};")

                self.distance_label.setText(f"Distance: ~{footstep_result['distance_m']:.1f}m")
                self.distance_label.setStyleSheet(f"font-size: 10pt; color: {color};")

                gait_icon = "🚶" if footstep_result['gait_type'] == 'walk' else "🏃" if footstep_result['gait_type'] == 'run' else "❓"
                self.gait_label.setText(f"Gait: {gait_icon} {footstep_result['gait_type'].upper()}")
                self.gait_label.setStyleSheet(f"font-size: 10pt; font-weight: bold; color: {color};")

                # Add footstep info to events
                events['footstep_detected'] = True
                events['footstep_confidence'] = conf
                events['footstep_distance'] = footstep_result['distance_m']
            else:
                # Reset to inactive state
                gray = "#666666"
                self.human_confidence_label.setText("Confidence: —")
                self.human_confidence_label.setStyleSheet(f"font-size: 10pt; color: {gray};")

                self.cadence_label.setText("Cadence: —")
                self.cadence_label.setStyleSheet(f"font-size: 10pt; color: {gray};")

                self.foot_label.setText("Foot: —")
                self.foot_label.setStyleSheet(f"font-size: 10pt; color: {gray};")

                self.surface_label.setText("Surface: —")
                self.surface_label.setStyleSheet(f"font-size: 10pt; color: {gray};")

                self.distance_label.setText("Distance: —")
                self.distance_label.setStyleSheet(f"font-size: 10pt; color: {gray};")

                self.gait_label.setText("Gait: —")
                self.gait_label.setStyleSheet(f"font-size: 10pt; color: {gray};")

                events['footstep_detected'] = False
                events['footstep_confidence'] = 0.0
                events['footstep_distance'] = 0.0

            # Advanced human voice analysis (v3.0)
            voice_result = self.voice_detector.analyze_voice(block, sample_rate, stereo=(block.ndim == 2))

            # Update UI with voice analysis
            if voice_result['is_human_voice']:
                v_conf = voice_result['confidence']
                v_color = "#00FF00" if v_conf > 75 else "#FFA500" if v_conf > 50 else "#FFFF00"

                self.voice_confidence_label.setText(f"Confidence: {v_conf:.1f}%")
                self.voice_confidence_label.setStyleSheet(f"font-size: 10pt; font-weight: bold; color: {v_color};")

                # Voice type with icons
                vtype_icon = "🗣️♂️" if voice_result['voice_type'] == 'male' else "🗣️♀️" if voice_result['voice_type'] == 'female' else "🗣️👶" if voice_result['voice_type'] == 'child' else "🗣️"
                self.voice_type_label.setText(f"Voice: {vtype_icon} {voice_result['voice_type'].upper()}")
                self.voice_type_label.setStyleSheet(f"font-size: 10pt; color: {v_color};")

                self.pitch_label.setText(f"Pitch: {voice_result['pitch_hz']:.1f} Hz")
                self.pitch_label.setStyleSheet(f"font-size: 10pt; color: {v_color};")

                # Intensity with icons
                intensity_icon = "📢" if voice_result['intensity'] == 'shout' else "🤫" if voice_result['intensity'] == 'whisper' else "🔊"
                self.intensity_label.setText(f"Intensity: {intensity_icon} {voice_result['intensity'].upper()}")
                self.intensity_label.setStyleSheet(f"font-size: 10pt; color: {v_color};")

                # Communication
                comm_status = "💬 TALKING" if voice_result['is_communication'] else "— No sustained speech"
                comm_color = "#FF5500" if voice_result['is_communication'] else v_color
                self.communication_label.setText(f"Communication: {comm_status}")
                self.communication_label.setStyleSheet(f"font-size: 10pt; font-weight: bold; color: {comm_color};")

                # Breathing
                if voice_result['is_breathing']:
                    self.breathing_label.setText("Breathing: 💨 DETECTED")
                    self.breathing_label.setStyleSheet(f"font-size: 10pt; color: #00DDFF;")
                else:
                    self.breathing_label.setText("Breathing: —")
                    self.breathing_label.setStyleSheet(f"font-size: 10pt; color: {v_color};")

                # Add voice info to events
                events['voice_detected'] = True
                events['voice_confidence'] = v_conf
                events['voice_type'] = voice_result['voice_type']
                events['is_communication'] = voice_result['is_communication']
            elif voice_result['is_breathing']:
                # Only breathing, no voice
                gray = "#666666"
                self.voice_confidence_label.setText("Confidence: —")
                self.voice_confidence_label.setStyleSheet(f"font-size: 10pt; color: {gray};")

                self.voice_type_label.setText("Voice: —")
                self.voice_type_label.setStyleSheet(f"font-size: 10pt; color: {gray};")

                self.pitch_label.setText("Pitch: — Hz")
                self.pitch_label.setStyleSheet(f"font-size: 10pt; color: {gray};")

                self.intensity_label.setText("Intensity: —")
                self.intensity_label.setStyleSheet(f"font-size: 10pt; color: {gray};")

                self.communication_label.setText("Communication: —")
                self.communication_label.setStyleSheet(f"font-size: 10pt; color: {gray};")

                self.breathing_label.setText("Breathing: 💨 DETECTED (Heavy breathing)")
                self.breathing_label.setStyleSheet("font-size: 10pt; font-weight: bold; color: #00DDFF;")

                events['voice_detected'] = False
                events['voice_confidence'] = 0.0
                events['is_communication'] = False
                events['breathing_detected'] = True
            else:
                # No voice, no breathing
                gray = "#666666"
                self.voice_confidence_label.setText("Confidence: —")
                self.voice_confidence_label.setStyleSheet(f"font-size: 10pt; color: {gray};")

                self.voice_type_label.setText("Voice: —")
                self.voice_type_label.setStyleSheet(f"font-size: 10pt; color: {gray};")

                self.pitch_label.setText("Pitch: — Hz")
                self.pitch_label.setStyleSheet(f"font-size: 10pt; color: {gray};")

                self.intensity_label.setText("Intensity: —")
                self.intensity_label.setStyleSheet(f"font-size: 10pt; color: {gray};")

                self.communication_label.setText("Communication: —")
                self.communication_label.setStyleSheet(f"font-size: 10pt; color: {gray};")

                self.breathing_label.setText("Breathing: —")
                self.breathing_label.setStyleSheet(f"font-size: 10pt; color: {gray};")

                events['voice_detected'] = False
                events['voice_confidence'] = 0.0
                events['is_communication'] = False
                events['breathing_detected'] = False

            return events, bands

        except Exception as e:
            log(f"Error in analyze: {e}", "ERROR")
            return {'walk': False, 'run': False, 'shot': False}, {}

    def band_intensity(self, ratio, base, sens):
        """Calculate band intensity with sensitivity threshold"""
        thr = base * (1.4 - sens)
        thr = max(0.02, min(0.6, thr))

        if ratio <= thr:
            return 0.0

        return min(1.0, (ratio - thr) / (1.0 - thr))

    def reset_detection(self):
        """Reset all detection states - call when audio stops (FIXED v3.5.3)"""
        # Reset hold counters
        self.walk_hold = 0
        self.run_hold = 0
        self.shot_hold = 0

        # Reset labels to "none" state
        self.walk_label.setText(tr('walk_none'))
        self.walk_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #666666;")

        self.run_label.setText(tr('run_none'))
        self.run_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #666666;")

        self.shot_label.setText(tr('shot_none'))
        self.shot_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #666666;")

        # Reset human detection labels if they exist
        if hasattr(self, 'human_confidence_label'):
            self.human_confidence_label.setText("Confidence: ---%")
            self.human_confidence_label.setStyleSheet("font-size: 10pt; font-weight: bold; color: #666666;")

        log("Detection state reset", "INFO")

    def update_translations(self):
        """Update UI translations"""
        # Update group boxes
        self.profile_group.setTitle(tr('detection_profile'))
        self.enable_group.setTitle(tr('enable_detection'))
        self.sens_group.setTitle(tr('sensitivity'))
        self.status_group.setTitle(tr('detection_status'))

        # Update checkboxes
        self.walk_enable.setText(tr('detect_walk'))
        self.run_enable.setText(tr('detect_run'))
        self.shot_enable.setText(tr('detect_shot'))

        # Update sensitivity labels
        self.walk_label_sens.setText(tr('walk'))
        self.run_label_sens.setText(tr('run'))
        self.shot_label_sens.setText(tr('shot'))

        # Update detection status labels (preserve current state)
        # We need to check current text to determine state
        if 'DETECTED' in self.walk_label.text() or 'WYKRYTO' in self.walk_label.text():
            self.walk_label.setText(tr('walk_detected'))
        else:
            self.walk_label.setText(tr('walk_none'))

        if 'DETECTED' in self.run_label.text() or 'WYKRYTO' in self.run_label.text():
            self.run_label.setText(tr('run_detected'))
        else:
            self.run_label.setText(tr('run_none'))

        if 'DETECTED' in self.shot_label.text() or 'WYKRYTO' in self.shot_label.text():
            self.shot_label.setText(tr('shot_detected'))
        else:
            self.shot_label.setText(tr('shot_none'))


# ============================================================================
# LED OVERLAY WIDGET
# ============================================================================


