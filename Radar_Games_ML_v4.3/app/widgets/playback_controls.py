"""
Radar Games ML v4.3 - Playback Controls Widget
Audio transport controls with play/pause/stop and progress tracking.

Features:
- Play/Pause/Stop buttons
- Seekable progress slider
- Time display (current/total)
- Playback speed control
- Loop region toggle
"""

from __future__ import annotations

from typing import Optional

from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QSlider, QLabel, QComboBox, QCheckBox
)
from PyQt5.QtCore import Qt, pyqtSignal

try:
    from app.core.translations import tr
except ImportError:
    def tr(x): return x


class PlaybackControlsWidget(QWidget):
    """
    Audio playback transport controls.

    Signals:
        play_clicked: Play button pressed
        pause_clicked: Pause button pressed
        stop_clicked: Stop button pressed
        seek_requested: User dragged progress slider (emits position_sec)
        speed_changed: Playback speed changed (emits multiplier)
        loop_toggled: Loop checkbox toggled (emits bool)
    """

    # Signals
    play_clicked = pyqtSignal()
    pause_clicked = pyqtSignal()
    stop_clicked = pyqtSignal()
    seek_requested = pyqtSignal(float)  # position_sec
    speed_changed = pyqtSignal(float)  # speed multiplier
    loop_toggled = pyqtSignal(bool)  # enabled

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self._duration_sec = 0.0
        self._is_seeking = False  # Prevent feedback loop during seek

        self._build_ui()

    def _build_ui(self):
        """Build the playback controls UI."""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Transport controls row
        transport_row = QHBoxLayout()

        # Play button
        self.play_btn = QPushButton("▶ Play")
        self.play_btn.setStyleSheet("""
            QPushButton {
                background: #00AA00;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 11pt;
            }
            QPushButton:hover { background: #00CC00; }
            QPushButton:disabled { background: #555555; color: #888888; }
        """)
        self.play_btn.clicked.connect(self.play_clicked.emit)
        self.play_btn.setToolTip("Play audio (Space)")
        transport_row.addWidget(self.play_btn)

        # Pause button
        self.pause_btn = QPushButton("⏸ Pause")
        self.pause_btn.setStyleSheet("""
            QPushButton {
                background: #DDAA00;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 11pt;
            }
            QPushButton:hover { background: #FFCC00; }
            QPushButton:disabled { background: #555555; color: #888888; }
        """)
        self.pause_btn.clicked.connect(self.pause_clicked.emit)
        self.pause_btn.setEnabled(False)
        self.pause_btn.setToolTip("Pause playback (Space)")
        transport_row.addWidget(self.pause_btn)

        # Stop button
        self.stop_btn = QPushButton("⏹ Stop")
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background: #AA0000;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 11pt;
            }
            QPushButton:hover { background: #CC0000; }
            QPushButton:disabled { background: #555555; color: #888888; }
        """)
        self.stop_btn.clicked.connect(self.stop_clicked.emit)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setToolTip("Stop playback and reset position")
        transport_row.addWidget(self.stop_btn)

        transport_row.addStretch()

        # Time display
        self.time_label = QLabel("00:00 / 00:00")
        self.time_label.setStyleSheet("""
            font-size: 11pt;
            font-family: monospace;
            font-weight: bold;
            color: #00DDFF;
            padding: 8px 12px;
        """)
        self.time_label.setToolTip("Current position / Total duration")
        transport_row.addWidget(self.time_label)

        main_layout.addLayout(transport_row)

        # Progress slider row
        progress_row = QHBoxLayout()

        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.setRange(0, 1000)  # 0-1000 for smooth seeking
        self.progress_slider.setValue(0)
        self.progress_slider.setEnabled(False)
        self.progress_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #2a2a2a;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #00DDFF;
                width: 16px;
                height: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }
            QSlider::handle:horizontal:hover {
                background: #00FFFF;
            }
            QSlider::sub-page:horizontal {
                background: #0088AA;
                border-radius: 4px;
            }
        """)
        self.progress_slider.sliderPressed.connect(self._on_slider_pressed)
        self.progress_slider.sliderReleased.connect(self._on_slider_released)
        self.progress_slider.setToolTip("Click to seek to position")
        progress_row.addWidget(self.progress_slider)

        main_layout.addLayout(progress_row)

        # Advanced controls row
        advanced_row = QHBoxLayout()

        # Playback speed
        speed_label = QLabel("Speed:")
        speed_label.setStyleSheet("font-size: 9pt; color: #AAAAAA;")
        advanced_row.addWidget(speed_label)

        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["0.5x", "0.75x", "1.0x", "1.25x", "1.5x", "2.0x"])
        self.speed_combo.setCurrentIndex(2)  # Default 1.0x
        self.speed_combo.setStyleSheet("""
            QComboBox {
                background: #2a2a2a;
                color: #DDDDDD;
                padding: 4px 8px;
                border: 1px solid #444;
                border-radius: 3px;
            }
            QComboBox:hover {
                border: 1px solid #00DDFF;
            }
        """)
        self.speed_combo.currentTextChanged.connect(self._on_speed_changed)
        self.speed_combo.setToolTip("Playback speed multiplier")
        advanced_row.addWidget(self.speed_combo)

        advanced_row.addSpacing(20)

        # Loop toggle
        self.loop_checkbox = QCheckBox("Loop Selection")
        self.loop_checkbox.setStyleSheet("""
            QCheckBox {
                color: #DDDDDD;
                font-size: 9pt;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:unchecked {
                background: #2a2a2a;
                border: 1px solid #444;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                background: #00AA00;
                border: 1px solid #00DD00;
                border-radius: 3px;
            }
        """)
        self.loop_checkbox.setEnabled(False)  # Enabled when segment selected
        self.loop_checkbox.toggled.connect(self.loop_toggled.emit)
        self.loop_checkbox.setToolTip("Loop selected segment continuously")
        advanced_row.addWidget(self.loop_checkbox)

        advanced_row.addStretch()

        main_layout.addLayout(advanced_row)

        self.setLayout(main_layout)

    def update_position(self, current_sec: float, total_sec: Optional[float] = None):
        """
        Update progress bar and time display.

        Args:
            current_sec: Current playback position
            total_sec: Total duration (updates if provided)
        """
        if total_sec is not None:
            self._duration_sec = total_sec

        # Update time label
        current_str = self._format_time(current_sec)
        total_str = self._format_time(self._duration_sec)
        self.time_label.setText(f"{current_str} / {total_str}")

        # Update progress slider (only if not seeking)
        if not self._is_seeking and self._duration_sec > 0:
            progress = int((current_sec / self._duration_sec) * 1000)
            self.progress_slider.setValue(progress)

    def set_playback_state(self, is_playing: bool, is_paused: bool):
        """
        Update button states based on playback state.

        Args:
            is_playing: True if currently playing
            is_paused: True if paused
        """
        if is_playing:
            self.play_btn.setEnabled(False)
            self.pause_btn.setEnabled(True)
            self.stop_btn.setEnabled(True)
        elif is_paused:
            self.play_btn.setEnabled(True)
            self.pause_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
        else:  # Stopped
            self.play_btn.setEnabled(True)
            self.pause_btn.setEnabled(False)
            self.stop_btn.setEnabled(False)

    def set_audio_loaded(self, loaded: bool):
        """
        Enable/disable controls based on whether audio is loaded.

        Args:
            loaded: True if audio data is loaded
        """
        self.progress_slider.setEnabled(loaded)
        self.speed_combo.setEnabled(loaded)

        if loaded:
            self.play_btn.setEnabled(True)
        else:
            self.play_btn.setEnabled(False)
            self.pause_btn.setEnabled(False)
            self.stop_btn.setEnabled(False)
            self.loop_checkbox.setEnabled(False)
            self.loop_checkbox.setChecked(False)

    def _on_slider_pressed(self):
        """User started dragging the slider."""
        self._is_seeking = True

    def _on_slider_released(self):
        """User released the slider - emit seek request."""
        self._is_seeking = False

        if self._duration_sec > 0:
            # Convert slider value (0-1000) to seconds
            position_sec = (self.progress_slider.value() / 1000.0) * self._duration_sec
            self.seek_requested.emit(position_sec)

    def _on_speed_changed(self, speed_text: str):
        """Playback speed changed."""
        # Extract multiplier from text (e.g., "1.5x" -> 1.5)
        try:
            multiplier = float(speed_text.replace('x', ''))
            self.speed_changed.emit(multiplier)
        except ValueError:
            pass

    @staticmethod
    def _format_time(seconds: float) -> str:
        """
        Format seconds as MM:SS.

        Args:
            seconds: Time in seconds

        Returns:
            Formatted string like "01:23"
        """
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
