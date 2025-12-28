"""
Radar Games ML v4.3 - Session Editor Widget
Main interface for loading, playing, and editing saved recording sessions.

Features:
- Load saved sessions from disk
- Audio playback with visual waveform
- Add/edit/delete labels
- Save modifications back to disk
- Non-destructive editing workflow
"""

from __future__ import annotations

from typing import Optional
from pathlib import Path

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QTableWidget,
    QPushButton, QLabel, QHeaderView, QTableWidgetItem, QMessageBox,
    QFileDialog, QInputDialog
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor

import numpy as np

from app.core.logger import log
from app.audio import AudioPlaybackEngine, PlaybackState
from app.ml.training import SessionManager, LabeledSession, AudioLabel
from app.widgets.waveform_timeline import WaveformTimelineWidget
from app.widgets.playback_controls import PlaybackControlsWidget

try:
    from app.core.translations import tr
except ImportError:
    def tr(x): return x


class SessionEditorWidget(QWidget):
    """
    Main session editing interface.

    Coordinates audio playback, waveform visualization, and label editing
    for saved recording sessions.

    Signals:
        session_loaded: Emitted when a session is successfully loaded
        session_saved: Emitted when session modifications are saved
        label_modified: Emitted when labels are added/edited/deleted
    """

    # Signals
    session_loaded = pyqtSignal(str)  # session_id
    session_saved = pyqtSignal(str)  # session_id
    label_modified = pyqtSignal()

    def __init__(self, session_manager: Optional[SessionManager] = None, parent: Optional[QWidget] = None):
        super().__init__(parent)

        # Components
        self.session_manager = session_manager or SessionManager()
        self.playback_engine = AudioPlaybackEngine()
        self.waveform = WaveformTimelineWidget()
        self.controls = PlaybackControlsWidget()

        # State
        self.current_session: Optional[LabeledSession] = None
        self.current_audio: Optional[np.ndarray] = None
        self.is_modified = False

        self._build_ui()
        self._connect_signals()
        self._refresh_sessions_table()

        log("SessionEditorWidget initialized", "INFO")

    def _build_ui(self):
        """Build the session editor UI."""
        main_layout = QVBoxLayout()

        # Session selector group
        sessions_group = self._build_sessions_selector_group()
        main_layout.addWidget(sessions_group)

        # Session info label
        self.session_info_label = QLabel("No session loaded")
        self.session_info_label.setStyleSheet("""
            font-size: 10pt;
            color: #AAAAAA;
            padding: 5px 10px;
            background: #2a2a2a;
            border-radius: 3px;
        """)
        main_layout.addWidget(self.session_info_label)

        # Playback controls
        controls_group = QGroupBox("🎵 Playback Controls")
        controls_layout = QVBoxLayout()
        controls_layout.addWidget(self.controls)
        controls_group.setLayout(controls_layout)
        main_layout.addWidget(controls_group)

        # Waveform display (v4.3.1-k0024: Increased height for better visibility)
        waveform_group = QGroupBox("📈 Audio Waveform & Timeline")
        waveform_layout = QVBoxLayout()
        self.waveform.setMinimumHeight(250)  # v4.3.1-k0024: Better visibility
        waveform_layout.addWidget(self.waveform)
        waveform_group.setLayout(waveform_layout)
        main_layout.addWidget(waveform_group)

        # Label editor panel (placeholder for now - will integrate in Phase 4)
        labels_group = QGroupBox("🏷️ Session Labels")
        labels_layout = QVBoxLayout()

        # Simple labels table (v4.3.1-k0024: Increased height for better readability)
        self.labels_table = QTableWidget()
        self.labels_table.setColumnCount(4)
        self.labels_table.setHorizontalHeaderLabels(["Time", "Class", "Description", "Duration"])
        self.labels_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.labels_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.labels_table.setMinimumHeight(300)  # v4.3.1-k0024: Increased from 200 for better visibility
        self.labels_table.setStyleSheet("""
            QTableWidget {
                background: #1a1a1a;
                color: #DDDDDD;
                gridline-color: #333333;
            }
            QTableWidget::item:selected {
                background: #004466;
            }
        """)
        labels_layout.addWidget(self.labels_table)

        # Label action buttons
        label_buttons = QHBoxLayout()
        label_buttons.addStretch()

        self.add_label_btn = QPushButton("➕ Add Label at Position")
        self.add_label_btn.setEnabled(False)
        self.add_label_btn.setStyleSheet("""
            QPushButton {
                background: #005500;
                color: #AAFFAA;
                padding: 6px 12px;
                border-radius: 3px;
            }
            QPushButton:hover { background: #007700; }
            QPushButton:disabled { background: #333333; color: #666666; }
        """)
        self.add_label_btn.clicked.connect(self._add_label_at_playback_position)
        self.add_label_btn.setToolTip("Add label at current playback position")
        label_buttons.addWidget(self.add_label_btn)

        self.delete_label_btn = QPushButton("🗑️ Delete Selected")
        self.delete_label_btn.setEnabled(False)
        self.delete_label_btn.setStyleSheet("""
            QPushButton {
                background: #552222;
                color: #FFAAAA;
                padding: 6px 12px;
                border-radius: 3px;
            }
            QPushButton:hover { background: #663333; }
            QPushButton:disabled { background: #333333; color: #666666; }
        """)
        self.delete_label_btn.clicked.connect(self._delete_selected_label)
        self.delete_label_btn.setToolTip("Delete selected label")
        label_buttons.addWidget(self.delete_label_btn)

        labels_layout.addLayout(label_buttons)

        labels_group.setLayout(labels_layout)
        main_layout.addWidget(labels_group)

        # Save button
        save_row = QHBoxLayout()
        save_row.addStretch()

        self.save_btn = QPushButton("💾 Save Session Changes")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background: #0066AA;
                color: white;
                font-weight: bold;
                padding: 10px 24px;
                border-radius: 5px;
                font-size: 11pt;
            }
            QPushButton:hover { background: #0088CC; }
            QPushButton:disabled { background: #444444; color: #777777; }
        """)
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self._save_session)
        self.save_btn.setToolTip("Save all label modifications to disk")
        save_row.addWidget(self.save_btn)

        main_layout.addLayout(save_row)

        self.setLayout(main_layout)

    def _build_sessions_selector_group(self) -> QGroupBox:
        """Build the saved sessions selector group."""
        group = QGroupBox("📁 Saved Sessions")
        layout = QVBoxLayout()

        # Sessions table (v4.3.1-k0024: Increased height for better readability)
        self.sessions_table = QTableWidget()
        self.sessions_table.setColumnCount(4)
        self.sessions_table.setHorizontalHeaderLabels(["Session ID", "Duration", "Labels", "Audio"])
        self.sessions_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.sessions_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.sessions_table.setSelectionMode(QTableWidget.SingleSelection)
        self.sessions_table.setMinimumHeight(250)  # v4.3.1-k0024: Increased from 150 for better visibility
        self.sessions_table.setStyleSheet("""
            QTableWidget {
                background: #1a1a1a;
                color: #DDDDDD;
                gridline-color: #333333;
            }
            QTableWidget::item:selected {
                background: #00AA66;
            }
            QHeaderView::section {
                background: #2a2a2a;
                color: #DDDDDD;
                padding: 5px;
                border: none;
            }
        """)
        self.sessions_table.doubleClicked.connect(self._on_session_double_clicked)
        layout.addWidget(self.sessions_table)

        # Buttons row
        buttons_row = QHBoxLayout()

        self.load_btn = QPushButton("📂 Load Selected Session")
        self.load_btn.setStyleSheet("""
            QPushButton {
                background: #00AA66;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover { background: #00CC88; }
            QPushButton:disabled { background: #444444; color: #777777; }
        """)
        self.load_btn.clicked.connect(self._load_selected_session)
        self.load_btn.setToolTip("Load selected session for editing (or double-click)")
        buttons_row.addWidget(self.load_btn)

        self.refresh_btn = QPushButton("🔄 Refresh List")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background: #555555;
                color: #DDDDDD;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover { background: #666666; }
        """)
        self.refresh_btn.clicked.connect(self._refresh_sessions_table)
        self.refresh_btn.setToolTip("Refresh sessions list from disk")
        buttons_row.addWidget(self.refresh_btn)

        # v4.3.1-k0024: Button to open audio archive folder
        self.open_archive_btn = QPushButton("🎵 Open Audio Archive")
        self.open_archive_btn.setStyleSheet("""
            QPushButton {
                background: #0066AA;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover { background: #0088CC; }
        """)
        self.open_archive_btn.clicked.connect(self._open_audio_archive_folder)
        self.open_archive_btn.setToolTip("Open AudioArchive folder with WAV files")
        buttons_row.addWidget(self.open_archive_btn)

        buttons_row.addStretch()
        layout.addLayout(buttons_row)

        group.setLayout(layout)
        return group

    def _connect_signals(self):
        """Connect all signals and slots."""
        # Playback engine signals
        self.playback_engine.position_changed.connect(self._on_playback_position_changed)
        self.playback_engine.state_changed.connect(self._on_playback_state_changed)
        self.playback_engine.playback_finished.connect(self._on_playback_finished)
        self.playback_engine.error_occurred.connect(self._on_playback_error)

        # Playback controls signals
        self.controls.play_clicked.connect(self._on_play_clicked)
        self.controls.pause_clicked.connect(self._on_pause_clicked)
        self.controls.stop_clicked.connect(self._on_stop_clicked)
        self.controls.seek_requested.connect(self._on_seek_requested)
        self.controls.loop_toggled.connect(self._on_loop_toggled)

        # Waveform signals
        self.waveform.timestamp_clicked.connect(self._on_waveform_clicked)
        self.waveform.segment_selected.connect(self._on_segment_selected)

        # Labels table signals
        self.labels_table.itemSelectionChanged.connect(self._on_label_selection_changed)

    # ========================================================================
    # SESSION LOADING
    # ========================================================================

    def _refresh_sessions_table(self):
        """Refresh the saved sessions table."""
        self.sessions_table.setRowCount(0)

        try:
            sessions = self.session_manager.list_sessions()

            for session_info in sessions:
                row = self.sessions_table.rowCount()
                self.sessions_table.insertRow(row)

                # Session ID
                self.sessions_table.setItem(row, 0, QTableWidgetItem(session_info["session_id"]))

                # Duration
                duration_sec = session_info.get("duration_sec", 0.0)
                duration_str = f"{int(duration_sec // 60)}:{int(duration_sec % 60):02d}"
                self.sessions_table.setItem(row, 1, QTableWidgetItem(duration_str))

                # Labels count
                label_count = session_info.get("label_count", 0)
                self.sessions_table.setItem(row, 2, QTableWidgetItem(str(label_count)))

                # Has audio
                has_audio = "✓ Yes" if session_info.get("has_audio", False) else "✗ No"
                audio_item = QTableWidgetItem(has_audio)
                if session_info.get("has_audio", False):
                    audio_item.setForeground(QColor(0, 200, 100))
                else:
                    audio_item.setForeground(QColor(200, 100, 100))
                self.sessions_table.setItem(row, 3, audio_item)

            log(f"Loaded {len(sessions)} sessions into table", "INFO")

        except Exception as e:
            log(f"Failed to refresh sessions table: {e}", "ERROR")
            QMessageBox.warning(self, "Error", f"Failed to load sessions list:\n{e}")

    def _on_session_double_clicked(self, index):
        """Handle double-click on session row."""
        self._load_selected_session()

    def _load_selected_session(self):
        """Load the selected session for editing."""
        selected_rows = self.sessions_table.selectedIndexes()
        if not selected_rows:
            QMessageBox.information(self, "No Selection", "Please select a session to load")
            return

        row = selected_rows[0].row()
        session_id = self.sessions_table.item(row, 0).text()

        self._load_session(session_id)

    def _load_session(self, session_id: str):
        """
        Load a session for editing.

        Args:
            session_id: ID of session to load
        """
        # Check for unsaved changes
        if self.is_modified:
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "Current session has unsaved changes. Discard them?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return

        try:
            # Stop any ongoing playback
            self.playback_engine.stop()

            # Load session metadata and labels
            session = self.session_manager.load_session(session_id)
            if not session:
                QMessageBox.warning(self, "Error", f"Failed to load session: {session_id}")
                return

            # Load audio data
            audio_data = self.session_manager.load_audio(session_id)
            if audio_data is None:
                QMessageBox.warning(
                    self, "No Audio",
                    f"Session {session_id} has no audio data.\nCannot play or edit."
                )
                return

            # Update state
            self.current_session = session
            self.current_audio = audio_data
            self.is_modified = False

            # Initialize playback engine
            sample_rate = getattr(session, 'sample_rate', 48000)
            self.playback_engine.load_audio(audio_data, sample_rate)

            # Update waveform
            self.waveform.set_audio_data(audio_data, sample_rate)

            # Load label markers
            markers = [(label.timestamp_sec, label.label_class) for label in session.labels]
            self.waveform.set_markers(markers)

            # Load labels into table
            self._refresh_labels_table()

            # Update UI
            duration_str = f"{int(session.duration_sec // 60)}:{int(session.duration_sec % 60):02d}"
            self.session_info_label.setText(
                f"📂 Session: {session_id} | ⏱️ Duration: {duration_str} | "
                f"🏷️ Labels: {len(session.labels)} | 🎵 Sample Rate: {sample_rate}Hz"
            )
            self.session_info_label.setStyleSheet("""
                font-size: 10pt;
                color: #00DDFF;
                font-weight: bold;
                padding: 5px 10px;
                background: #1a3a3a;
                border-radius: 3px;
            """)

            # Enable controls
            self.controls.set_audio_loaded(True)
            self.controls.update_position(0.0, session.duration_sec)
            self.add_label_btn.setEnabled(True)
            self.delete_label_btn.setEnabled(False)
            self.save_btn.setEnabled(False)  # No modifications yet

            # Emit signal
            self.session_loaded.emit(session_id)

            log(f"Session loaded: {session_id}", "INFO")

        except Exception as e:
            log(f"Failed to load session {session_id}: {e}", "ERROR")
            QMessageBox.critical(self, "Load Error", f"Failed to load session:\n{e}")

    def _refresh_labels_table(self):
        """Refresh the labels table from current session."""
        self.labels_table.setRowCount(0)

        if not self.current_session:
            return

        for label in self.current_session.labels:
            row = self.labels_table.rowCount()
            self.labels_table.insertRow(row)

            # Time
            time_str = f"{label.timestamp_sec:.2f}s"
            self.labels_table.setItem(row, 0, QTableWidgetItem(time_str))

            # Class
            self.labels_table.setItem(row, 1, QTableWidgetItem(label.label_class))

            # Description
            self.labels_table.setItem(row, 2, QTableWidgetItem(label.description))

            # Duration (if interval label)
            if label.is_interval and label.end_time_sec is not None:
                duration = label.end_time_sec - label.timestamp_sec
                duration_str = f"{duration:.2f}s"
            else:
                duration_str = "instant"
            self.labels_table.setItem(row, 3, QTableWidgetItem(duration_str))

    # ========================================================================
    # PLAYBACK CONTROL
    # ========================================================================

    def _on_play_clicked(self):
        """Handle play button click."""
        self.playback_engine.play()

    def _on_pause_clicked(self):
        """Handle pause button click."""
        self.playback_engine.pause()

    def _on_stop_clicked(self):
        """Handle stop button click."""
        self.playback_engine.stop()

    def _on_seek_requested(self, position_sec: float):
        """Handle seek request from progress slider."""
        self.playback_engine.seek(position_sec)

    def _on_loop_toggled(self, enabled: bool):
        """Handle loop checkbox toggle."""
        # Loop region already set by segment selection
        # This just enables/disables the loop
        pass  # Loop handled by playback engine when segment is selected

    def _on_playback_position_changed(self, position_sec: float):
        """Sync waveform and controls with playback position."""
        self.waveform.set_playhead(position_sec)

        if self.current_session:
            self.controls.update_position(position_sec, self.current_session.duration_sec)

    def _on_playback_state_changed(self, state: PlaybackState):
        """Update UI based on playback state."""
        is_playing = (state == PlaybackState.PLAYING)
        is_paused = (state == PlaybackState.PAUSED)

        self.controls.set_playback_state(is_playing, is_paused)

    def _on_playback_finished(self):
        """Handle playback reaching end."""
        self.controls.set_playback_state(False, False)
        log("Playback finished", "INFO")

    def _on_playback_error(self, error_msg: str):
        """Handle playback error."""
        QMessageBox.warning(self, "Playback Error", f"Audio playback error:\n{error_msg}")
        log(f"Playback error: {error_msg}", "ERROR")

    def _on_waveform_clicked(self, timestamp_sec: float):
        """Seek playback when waveform is clicked."""
        self.playback_engine.seek(timestamp_sec)

    def _on_segment_selected(self, start_sec: float, end_sec: float):
        """Handle segment selection from waveform."""
        # Enable loop checkbox
        self.controls.loop_checkbox.setEnabled(True)

        # If loop is enabled, set loop region
        if self.controls.loop_checkbox.isChecked():
            self.playback_engine.set_loop_region(start_sec, end_sec, enabled=True)
            log(f"Loop region set: {start_sec:.2f}s - {end_sec:.2f}s", "INFO")

    # ========================================================================
    # LABEL EDITING
    # ========================================================================

    def _add_label_at_playback_position(self):
        """Add label at current playback position (v4.3.1-k0023: With class selector)."""
        if not self.current_session:
            return

        current_pos = self.playback_engine.position

        # Show dialog to choose label class
        label_class, ok = QInputDialog.getItem(
            self,
            "Add Label",
            f"Select label class for position {current_pos:.2f}s:",
            SessionManager.DEFAULT_LABEL_CLASSES,
            0,  # Default to first item
            False  # Not editable
        )

        if not ok:
            return  # User cancelled

        # Create new label
        label = AudioLabel(
            id=len(self.current_session.labels),
            timestamp_sec=current_pos,
            label_class=label_class,
            description=f"Added at {current_pos:.2f}s"
        )

        self.current_session.labels.append(label)
        self._mark_modified()
        self._refresh_labels_table()

        # Update waveform markers
        markers = [(lbl.timestamp_sec, lbl.label_class) for lbl in self.current_session.labels]
        self.waveform.set_markers(markers)

        log(f"Label '{label_class}' added at {current_pos:.2f}s", "INFO")

    def _delete_selected_label(self):
        """Delete selected label from session."""
        if not self.current_session:
            return

        selected_rows = self.labels_table.selectedIndexes()
        if not selected_rows:
            return

        row = selected_rows[0].row()

        # Remove label (by index since labels are in order)
        if 0 <= row < len(self.current_session.labels):
            label = self.current_session.labels.pop(row)
            self._mark_modified()
            self._refresh_labels_table()

            # Update waveform markers
            markers = [(lbl.timestamp_sec, lbl.label_class) for lbl in self.current_session.labels]
            self.waveform.set_markers(markers)

            log(f"Label deleted from {label.timestamp_sec:.2f}s", "INFO")

    def _on_label_selection_changed(self):
        """Handle label selection change."""
        has_selection = len(self.labels_table.selectedIndexes()) > 0
        self.delete_label_btn.setEnabled(has_selection and self.current_session is not None)

    def _mark_modified(self):
        """Mark session as modified."""
        if not self.is_modified:
            self.is_modified = True
            self.save_btn.setEnabled(True)
            self.session_info_label.setText(
                self.session_info_label.text() + " [Modified ⚠️]"
            )
            self.label_modified.emit()

    # ========================================================================
    # SAVE WORKFLOW
    # ========================================================================

    def _save_session(self):
        """Save modified session to disk."""
        if not self.current_session:
            return

        if not self.is_modified:
            QMessageBox.information(self, "No Changes", "No modifications to save")
            return

        # Confirm save
        reply = QMessageBox.question(
            self, "Save Session",
            f"Save label modifications to session:\n{self.current_session.session_id}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.No:
            return

        try:
            # Save session (audio data not modified, only labels)
            success = self.session_manager.save_session(
                self.current_session,
                audio_data=None  # Don't re-save audio
            )

            if success:
                self.is_modified = False
                self.save_btn.setEnabled(False)

                # Update session info label (remove "Modified" marker)
                info_text = self.session_info_label.text().replace(" [Modified ⚠️]", "")
                self.session_info_label.setText(info_text)

                QMessageBox.information(self, "Success", "Session saved successfully!")
                self.session_saved.emit(self.current_session.session_id)
                log(f"Session saved: {self.current_session.session_id}", "INFO")
            else:
                QMessageBox.warning(self, "Save Failed", "Failed to save session")
                log(f"Failed to save session: {self.current_session.session_id}", "ERROR")

        except Exception as e:
            log(f"Save session error: {e}", "ERROR")
            QMessageBox.critical(self, "Save Error", f"Failed to save session:\n{e}")

    def _open_audio_archive_folder(self):
        """Open the AudioArchive folder in file manager (v4.3.1-k0024)."""
        import subprocess
        import platform
        from pathlib import Path

        try:
            # Get archive path from session manager
            archive_path = self.session_manager.audio_archive_path

            # Create if doesn't exist
            archive_path.mkdir(parents=True, exist_ok=True)

            # Open folder based on OS
            system = platform.system()
            if system == "Windows":
                subprocess.Popen(f'explorer "{archive_path}"')
            elif system == "Darwin":  # macOS
                subprocess.Popen(['open', str(archive_path)])
            else:  # Linux
                subprocess.Popen(['xdg-open', str(archive_path)])

            log(f"Opened audio archive folder: {archive_path}", "INFO")

        except Exception as e:
            log(f"Failed to open audio archive folder: {e}", "ERROR")
            QMessageBox.warning(
                self,
                "Open Folder Error",
                f"Could not open AudioArchive folder:\n{e}"
            )

    def cleanup(self):
        """Cleanup resources before closing."""
        self.playback_engine.cleanup()
        log("SessionEditorWidget cleaned up", "INFO")
