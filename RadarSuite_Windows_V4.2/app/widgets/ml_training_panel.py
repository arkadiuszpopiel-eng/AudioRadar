"""
RadarSuite v4.2.0 - ML Training Panel
User-friendly UI for recording, labeling, and training custom audio models

Features:
- One-click recording start/stop
- Real-time labeling with hotkeys (1-8)
- Label list with edit/delete
- Training progress display
- No terminal required
"""

import numpy as np
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QTableWidget, QTableWidgetItem, QTextEdit,
    QComboBox, QLineEdit, QProgressBar, QHeaderView,
    QMessageBox, QDialog, QFormLayout, QDialogButtonBox,
    QSplitter, QFrame
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QColor, QKeyEvent

try:
    from core import log, tr
    from ml.training import (
        SessionManager, LabeledSession, AudioLabel,
        LabeledRecorder, ModelTrainer, TrainingConfig, TrainingStatus
    )
except ImportError:
    from ..core.logger import log
    def tr(x): return x
    from ..ml.training import (
        SessionManager, LabeledSession, AudioLabel,
        LabeledRecorder, ModelTrainer, TrainingConfig, TrainingStatus
    )


class AddLabelDialog(QDialog):
    """Dialog for adding/editing labels."""

    def __init__(self, parent=None, label: AudioLabel = None, timestamp: float = 0.0):
        super().__init__(parent)
        self.setWindowTitle("Add Label" if label is None else "Edit Label")
        self.setMinimumWidth(350)

        layout = QFormLayout()

        # Label class dropdown
        self.class_combo = QComboBox()
        self.class_combo.addItems(SessionManager.DEFAULT_LABEL_CLASSES)
        self.class_combo.setEditable(True)
        if label:
            self.class_combo.setCurrentText(label.label_class)
        layout.addRow("Class:", self.class_combo)

        # Timestamp (read-only)
        self.timestamp_label = QLabel(f"{timestamp:.2f}s")
        layout.addRow("Timestamp:", self.timestamp_label)

        # Description
        self.description_edit = QLineEdit()
        self.description_edit.setPlaceholderText("Optional description...")
        if label:
            self.description_edit.setText(label.description)
        layout.addRow("Description:", self.description_edit)

        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

        self.setLayout(layout)

    def get_values(self):
        return {
            "label_class": self.class_combo.currentText(),
            "description": self.description_edit.text(),
        }


class MLTrainingPanel(QWidget):
    """
    ML Training Panel - main widget for recording and training.

    Provides:
    - Recording controls (Start/Stop)
    - Real-time labeling (buttons + hotkeys 1-8)
    - Label list with timestamps
    - Training controls and progress
    - Session management
    """

    # Signal emitted when panel needs audio data
    audio_data_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        log("MLTrainingPanel.__init__", "INFO")

        # Initialize managers
        self.session_manager = SessionManager()
        self.recorder = LabeledRecorder(self.session_manager)
        self.trainer = ModelTrainer(self.session_manager)

        # Set callbacks
        self.recorder.set_callbacks(
            on_state_change=self._on_recording_state_change,
            on_label_added=self._on_label_added
        )
        self.trainer.set_callbacks(
            on_progress=self._on_training_progress,
            on_complete=self._on_training_complete,
            on_log=self._on_training_log
        )

        # Timer for updating elapsed time
        self._timer = QTimer()
        self._timer.timeout.connect(self._update_timer)

        # Audio buffer for current frame
        self._current_audio_block = None

        self._build_ui()
        self._update_sessions_table()

    def _build_ui(self):
        """Build the complete UI."""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Title
        title = QLabel("🧠 ML Training Studio")
        title.setStyleSheet("font-size: 16pt; font-weight: bold; color: #00DDFF; margin-bottom: 10px;")
        main_layout.addWidget(title)

        # Create splitter for two columns
        splitter = QSplitter(Qt.Horizontal)

        # Left column: Recording
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 5, 0)

        left_layout.addWidget(self._build_recording_group())
        left_layout.addWidget(self._build_labeling_group())
        left_layout.addWidget(self._build_labels_table_group())

        splitter.addWidget(left_widget)

        # Right column: Training
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(5, 0, 0, 0)

        right_layout.addWidget(self._build_sessions_group())
        right_layout.addWidget(self._build_training_group())
        right_layout.addWidget(self._build_log_group())

        splitter.addWidget(right_widget)

        # Set splitter sizes
        splitter.setSizes([400, 400])

        main_layout.addWidget(splitter)

        # Hotkey hint
        hotkey_hint = QLabel("💡 Tip: Press 1-8 during recording to quickly add labels")
        hotkey_hint.setStyleSheet("font-size: 9pt; color: #888888; margin-top: 5px;")
        main_layout.addWidget(hotkey_hint)

        self.setLayout(main_layout)

    def _build_recording_group(self) -> QGroupBox:
        """Build recording controls group."""
        group = QGroupBox("🎙️ Recording")
        layout = QVBoxLayout()

        # Status row
        status_row = QHBoxLayout()

        self.status_label = QLabel("⚪ Ready")
        self.status_label.setStyleSheet("font-size: 12pt; font-weight: bold;")
        status_row.addWidget(self.status_label)

        self.elapsed_label = QLabel("0:00")
        self.elapsed_label.setStyleSheet("font-size: 12pt; font-family: monospace;")
        status_row.addWidget(self.elapsed_label)

        status_row.addStretch()
        layout.addLayout(status_row)

        # Control buttons row
        btn_row = QHBoxLayout()

        self.start_btn = QPushButton("▶ Start Recording")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background: #00AA00;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 11pt;
            }
            QPushButton:hover { background: #00CC00; }
            QPushButton:disabled { background: #555555; color: #888888; }
        """)
        self.start_btn.clicked.connect(self._on_start_recording)
        btn_row.addWidget(self.start_btn)

        self.stop_btn = QPushButton("⏹ Stop Recording")
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background: #AA0000;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 11pt;
            }
            QPushButton:hover { background: #CC0000; }
            QPushButton:disabled { background: #555555; color: #888888; }
        """)
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self._on_stop_recording)
        btn_row.addWidget(self.stop_btn)

        layout.addLayout(btn_row)

        group.setLayout(layout)
        return group

    def _build_labeling_group(self) -> QGroupBox:
        """Build labeling controls group."""
        group = QGroupBox("🏷️ Add Labels (Hotkeys 1-8)")
        layout = QVBoxLayout()

        # Label class buttons grid (2 rows x 4 columns)
        for row_idx in range(2):
            row = QHBoxLayout()
            for col_idx in range(4):
                idx = row_idx * 4 + col_idx
                if idx < len(SessionManager.DEFAULT_LABEL_CLASSES):
                    label_class = SessionManager.DEFAULT_LABEL_CLASSES[idx]
                    btn = QPushButton(f"{idx+1}: {label_class[:10]}")
                    btn.setToolTip(f"Add '{label_class}' label (Hotkey: {idx+1})")
                    btn.setStyleSheet("""
                        QPushButton {
                            background: #2a2a2a;
                            color: #00DDFF;
                            padding: 8px;
                            border: 1px solid #444;
                            border-radius: 4px;
                        }
                        QPushButton:hover { background: #3a3a3a; border-color: #00DDFF; }
                        QPushButton:disabled { color: #666666; }
                    """)
                    btn.clicked.connect(lambda checked, i=idx: self._add_label_by_index(i))
                    row.addWidget(btn)
            layout.addLayout(row)

        # Custom label button
        self.custom_label_btn = QPushButton("➕ Add Custom Label...")
        self.custom_label_btn.setStyleSheet("""
            QPushButton {
                background: #1a1a1a;
                color: #AAAAAA;
                padding: 8px;
                border: 1px dashed #444;
                border-radius: 4px;
            }
            QPushButton:hover { border-color: #888; color: #DDDDDD; }
        """)
        self.custom_label_btn.clicked.connect(self._add_custom_label)
        layout.addWidget(self.custom_label_btn)

        group.setLayout(layout)
        return group

    def _build_labels_table_group(self) -> QGroupBox:
        """Build labels table group."""
        group = QGroupBox("📋 Current Session Labels")
        layout = QVBoxLayout()

        self.labels_table = QTableWidget()
        self.labels_table.setColumnCount(4)
        self.labels_table.setHorizontalHeaderLabels(["ID", "Time", "Class", "Description"])
        self.labels_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.labels_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.labels_table.setAlternatingRowColors(True)
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
        layout.addWidget(self.labels_table)

        # Delete button
        delete_row = QHBoxLayout()
        delete_row.addStretch()

        self.delete_label_btn = QPushButton("🗑️ Delete Selected")
        self.delete_label_btn.setStyleSheet("""
            QPushButton {
                background: #552222;
                color: #FFAAAA;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover { background: #663333; }
        """)
        self.delete_label_btn.clicked.connect(self._delete_selected_label)
        delete_row.addWidget(self.delete_label_btn)

        layout.addLayout(delete_row)

        group.setLayout(layout)
        return group

    def _build_sessions_group(self) -> QGroupBox:
        """Build saved sessions group."""
        group = QGroupBox("📁 Saved Sessions")
        layout = QVBoxLayout()

        self.sessions_table = QTableWidget()
        self.sessions_table.setColumnCount(4)
        self.sessions_table.setHorizontalHeaderLabels(["Session", "Duration", "Labels", "Audio"])
        self.sessions_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.sessions_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.sessions_table.setMaximumHeight(150)
        self.sessions_table.setStyleSheet("""
            QTableWidget {
                background: #1a1a1a;
                color: #DDDDDD;
                gridline-color: #333333;
            }
            QTableWidget::item:selected {
                background: #004466;
            }
        """)
        layout.addWidget(self.sessions_table)

        # Stats
        self.stats_label = QLabel("Total: 0 sessions, 0 labels, 0:00 audio")
        self.stats_label.setStyleSheet("font-size: 9pt; color: #888888;")
        layout.addWidget(self.stats_label)

        group.setLayout(layout)
        return group

    def _build_training_group(self) -> QGroupBox:
        """Build training controls group."""
        group = QGroupBox("🎓 Train Model")
        layout = QVBoxLayout()

        # Train button
        self.train_btn = QPushButton("🚀 Train Model From All Sessions")
        self.train_btn.setStyleSheet("""
            QPushButton {
                background: #0066AA;
                color: white;
                font-weight: bold;
                padding: 12px 20px;
                border-radius: 5px;
                font-size: 11pt;
            }
            QPushButton:hover { background: #0088CC; }
            QPushButton:disabled { background: #555555; color: #888888; }
        """)
        self.train_btn.clicked.connect(self._on_start_training)
        layout.addWidget(self.train_btn)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p% - Idle")
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background: #2a2a2a;
                border: 1px solid #444;
                border-radius: 4px;
                text-align: center;
                color: #DDDDDD;
            }
            QProgressBar::chunk {
                background: #0088CC;
                border-radius: 3px;
            }
        """)
        layout.addWidget(self.progress_bar)

        # Status
        self.training_status_label = QLabel("Ready to train")
        self.training_status_label.setStyleSheet("font-size: 9pt; color: #888888;")
        layout.addWidget(self.training_status_label)

        # Cancel button (hidden by default)
        self.cancel_train_btn = QPushButton("❌ Cancel Training")
        self.cancel_train_btn.setStyleSheet("""
            QPushButton {
                background: #AA4400;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover { background: #CC5500; }
        """)
        self.cancel_train_btn.clicked.connect(self._on_cancel_training)
        self.cancel_train_btn.hide()
        layout.addWidget(self.cancel_train_btn)

        group.setLayout(layout)
        return group

    def _build_log_group(self) -> QGroupBox:
        """Build training log group."""
        group = QGroupBox("📜 Training Log")
        layout = QVBoxLayout()

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background: #0a0a0a;
                color: #00DD00;
                font-family: monospace;
                font-size: 9pt;
                border: 1px solid #333;
            }
        """)
        layout.addWidget(self.log_text)

        group.setLayout(layout)
        return group

    # ========================================================================
    # RECORDING HANDLERS
    # ========================================================================

    def _on_start_recording(self):
        """Handle start recording button."""
        if self.recorder.start_recording():
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self._timer.start(100)  # Update every 100ms
            self._clear_labels_table()

    def _on_stop_recording(self):
        """Handle stop recording button."""
        session = self.recorder.stop_recording()
        if session:
            self._timer.stop()
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self._update_sessions_table()

            QMessageBox.information(
                self,
                "Recording Saved",
                f"Session saved: {session.session_id}\n"
                f"Duration: {session.duration_sec:.1f}s\n"
                f"Labels: {len(session.labels)}"
            )

    def _on_recording_state_change(self, state):
        """Handle recording state changes."""
        if state.is_recording:
            self.status_label.setText("🔴 Recording")
            self.status_label.setStyleSheet("font-size: 12pt; font-weight: bold; color: #FF4444;")
        else:
            self.status_label.setText("⚪ Ready")
            self.status_label.setStyleSheet("font-size: 12pt; font-weight: bold; color: #888888;")

    def _update_timer(self):
        """Update elapsed time display."""
        elapsed = self.recorder.elapsed_seconds
        mins = int(elapsed // 60)
        secs = int(elapsed % 60)
        self.elapsed_label.setText(f"{mins}:{secs:02d}")

    # ========================================================================
    # LABELING HANDLERS
    # ========================================================================

    def _add_label_by_index(self, index: int):
        """Add label by class index."""
        if not self.recorder.is_recording:
            QMessageBox.warning(self, "Not Recording", "Start recording first to add labels.")
            return

        label = self.recorder.add_label_with_hotkey(index + 1)
        if label:
            self._add_label_to_table(label)

    def _add_custom_label(self):
        """Add custom label via dialog."""
        if not self.recorder.is_recording:
            QMessageBox.warning(self, "Not Recording", "Start recording first to add labels.")
            return

        dialog = AddLabelDialog(self, timestamp=self.recorder.elapsed_seconds)
        if dialog.exec_() == QDialog.Accepted:
            values = dialog.get_values()
            label = self.recorder.add_label(
                label_class=values["label_class"],
                description=values["description"]
            )
            if label:
                self._add_label_to_table(label)

    def _on_label_added(self, label: AudioLabel):
        """Handle label added callback."""
        # Already handled in _add_label_by_index
        pass

    def _add_label_to_table(self, label: AudioLabel):
        """Add a label to the labels table."""
        row = self.labels_table.rowCount()
        self.labels_table.insertRow(row)

        self.labels_table.setItem(row, 0, QTableWidgetItem(str(label.id)))
        self.labels_table.setItem(row, 1, QTableWidgetItem(f"{label.timestamp_sec:.2f}s"))
        self.labels_table.setItem(row, 2, QTableWidgetItem(label.label_class))
        self.labels_table.setItem(row, 3, QTableWidgetItem(label.description))

    def _clear_labels_table(self):
        """Clear the labels table."""
        self.labels_table.setRowCount(0)

    def _delete_selected_label(self):
        """Delete selected label."""
        selected = self.labels_table.selectedItems()
        if not selected:
            return

        row = selected[0].row()
        label_id = int(self.labels_table.item(row, 0).text())

        if self.recorder.current_session:
            self.recorder.current_session.remove_label(label_id)
            self.labels_table.removeRow(row)

    # ========================================================================
    # TRAINING HANDLERS
    # ========================================================================

    def _on_start_training(self):
        """Handle start training button."""
        sessions = self.session_manager.list_sessions()
        sessions_with_audio = [s for s in sessions if s["has_audio"]]

        if not sessions_with_audio:
            QMessageBox.warning(
                self,
                "No Data",
                "No sessions with audio found.\n"
                "Record some sessions with labels first."
            )
            return

        total_labels = sum(s["label_count"] for s in sessions_with_audio)
        if total_labels < 10:
            QMessageBox.warning(
                self,
                "Insufficient Data",
                f"Only {total_labels} labels found.\n"
                "Please add at least 10 labels across sessions."
            )
            return

        self.log_text.clear()
        self._log_message("Starting training...")
        self._log_message(f"Sessions: {len(sessions_with_audio)}, Labels: {total_labels}")

        self.train_btn.setEnabled(False)
        self.cancel_train_btn.show()

        self.trainer.start_training()

    def _on_cancel_training(self):
        """Handle cancel training button."""
        self.trainer.cancel_training()
        self._log_message("Cancellation requested...")

    def _on_training_progress(self, progress):
        """Handle training progress update."""
        self.progress_bar.setValue(int(progress.progress_percent))
        self.progress_bar.setFormat(f"%p% - {progress.current_step}")
        self.training_status_label.setText(progress.current_step)

        if progress.accuracy > 0:
            self._log_message(f"Accuracy: {progress.accuracy:.1%}")

    def _on_training_complete(self, result):
        """Handle training completion."""
        self.train_btn.setEnabled(True)
        self.cancel_train_btn.hide()

        if result.success:
            self.progress_bar.setFormat("100% - Complete!")
            self._log_message(f"✅ Training completed!")
            self._log_message(f"   Accuracy: {result.accuracy:.1%}")
            self._log_message(f"   Model: {result.model_path}")
            self._log_message(f"   Time: {result.training_time_sec:.1f}s")

            QMessageBox.information(
                self,
                "Training Complete",
                f"Model trained successfully!\n\n"
                f"Accuracy: {result.accuracy:.1%}\n"
                f"Samples: {result.samples_used}\n"
                f"Saved to: {result.model_path}"
            )
        else:
            self.progress_bar.setFormat("0% - Failed")
            self._log_message(f"❌ Training failed: {result.error_message}")

            QMessageBox.warning(
                self,
                "Training Failed",
                f"Training failed:\n{result.error_message}"
            )

    def _on_training_log(self, message: str):
        """Handle training log message."""
        self._log_message(message)

    def _log_message(self, message: str):
        """Add message to log."""
        self.log_text.append(message)
        # Scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    # ========================================================================
    # SESSIONS
    # ========================================================================

    def _update_sessions_table(self):
        """Update the saved sessions table."""
        sessions = self.session_manager.list_sessions()

        self.sessions_table.setRowCount(len(sessions))

        total_duration = 0
        total_labels = 0

        for row, session_info in enumerate(sessions):
            self.sessions_table.setItem(row, 0, QTableWidgetItem(session_info["session_id"]))

            duration = session_info["duration_sec"]
            total_duration += duration
            mins = int(duration // 60)
            secs = int(duration % 60)
            self.sessions_table.setItem(row, 1, QTableWidgetItem(f"{mins}:{secs:02d}"))

            labels = session_info["label_count"]
            total_labels += labels
            self.sessions_table.setItem(row, 2, QTableWidgetItem(str(labels)))

            has_audio = "✅" if session_info["has_audio"] else "❌"
            self.sessions_table.setItem(row, 3, QTableWidgetItem(has_audio))

        # Update stats
        mins = int(total_duration // 60)
        secs = int(total_duration % 60)
        self.stats_label.setText(
            f"Total: {len(sessions)} sessions, {total_labels} labels, {mins}:{secs:02d} audio"
        )

    # ========================================================================
    # AUDIO INTERFACE
    # ========================================================================

    def feed_audio(self, block: np.ndarray):
        """
        Feed audio data to the recorder.

        Called by MainWindow during audio processing.

        Args:
            block: Audio data block
        """
        if self.recorder.is_recording:
            self.recorder.add_audio_block(block)

    # ========================================================================
    # KEYBOARD SHORTCUTS
    # ========================================================================

    def keyPressEvent(self, event: QKeyEvent):
        """Handle keyboard shortcuts for quick labeling."""
        if not self.recorder.is_recording:
            super().keyPressEvent(event)
            return

        key = event.key()

        # Number keys 1-8 for quick labeling
        if Qt.Key_1 <= key <= Qt.Key_8:
            index = key - Qt.Key_1
            self._add_label_by_index(index)
            return

        # Backspace to remove last label
        if key == Qt.Key_Backspace:
            if self.recorder.remove_last_label():
                if self.labels_table.rowCount() > 0:
                    self.labels_table.removeRow(self.labels_table.rowCount() - 1)
            return

        super().keyPressEvent(event)
