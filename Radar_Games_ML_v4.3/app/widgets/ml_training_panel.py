"""
Radar Games ML v4.3.1-k0023 - ML Training Panel
User-friendly UI for recording, labeling, and training custom audio models

ENHANCED v4.3.1-k0023: Extended to 13 label classes with full hotkey support
Features:
- One-click recording start/stop with pause/resume
- Real-time labeling with hotkeys (1-9, 0, -, =, [) for 13 classes
- Noise reduction for cleaner recordings
- Label list with edit/delete
- Training progress display
- Waveform timeline with zoom/scroll
- Segment selection and labeling
- No terminal required
"""

import numpy as np
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QTableWidget, QTableWidgetItem, QTextEdit,
    QComboBox, QLineEdit, QProgressBar, QHeaderView,
    QMessageBox, QDialog, QFormLayout, QDialogButtonBox,
    QSplitter, QFrame, QTabWidget, QStackedWidget
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QColor, QKeyEvent

from app.core.logger import log
from app.core.translations import tr
from app.ml.training import (
    SessionManager, LabeledSession, AudioLabel,
    LabeledRecorder, ModelTrainer, TrainingConfig, TrainingStatus,
    RecordingController, RecordingStateEnum,
)
from app.ml import ModelRegistry, MLFootstepDetector, get_model_registry
from app.widgets.waveform_timeline import WaveformTimelineWidget
from app.widgets.toast import ToastNotification
from app.widgets.session_editor import SessionEditorWidget


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
    - Recording controls (Start/Stop/Pause)
    - Real-time labeling (buttons + hotkeys 1-9, 0, -, =, [ for 13 classes)
    - Noise reduction for cleaner recordings
    - Label list with timestamps
    - Training controls and progress
    - Session management
    """

    # Signal emitted when panel needs audio data
    audio_data_requested = pyqtSignal()

    def __init__(self, parent=None, recording_controller: RecordingController = None, overlay_launcher=None, toast_notifier: ToastNotification = None):
        super().__init__(parent)
        log("MLTrainingPanel.__init__", "INFO")

        # Initialize managers shared with overlay
        self.recording_controller = recording_controller or RecordingController()
        self.session_manager = self.recording_controller.session_manager
        self.recorder = self.recording_controller.recorder
        self.trainer = ModelTrainer(self.session_manager)

        # v4.3.0-k0001: Toast notifications for live feedback
        self.toast = toast_notifier  # Optional: for showing status toasts

        # v4.3.0-k0001: Model management
        self.model_registry = get_model_registry()
        self.ml_detector = MLFootstepDetector(sample_rate=48000, auto_load_best=False)

        # Set callbacks
        self.recording_controller.add_state_listener(self._on_recording_state_change)
        self.recording_controller.add_label_listener(self._on_label_added)
        self.trainer.set_callbacks(
            on_progress=self._on_training_progress,
            on_complete=self._on_training_complete,
            on_log=self._on_training_log
        )

        self._overlay_launcher = overlay_launcher

        # Timer for updating elapsed time
        self._timer = QTimer()
        self._timer.timeout.connect(self._update_timer)

        # Audio buffer for current frame
        self._current_audio_block = None

        # v4.2.1: Waveform timeline state
        self._pending_waveform_update = False
        self._selected_segment = None

        self._build_ui()
        self._update_sessions_table()

    def _build_ui(self):
        """Build the complete UI with reorganized tabs (v4.3.1-k0023)."""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Title
        title = QLabel("🧠 ML Training Studio")
        title.setStyleSheet("font-size: 16pt; font-weight: bold; color: #00DDFF; margin-bottom: 10px;")
        main_layout.addWidget(title)

        # Create tab widget
        # v4.3.1-k0023: Reorganized - Tab A (Training), Tab B (Recording + Editing)
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #444;
                background: #1a1a1a;
                border-radius: 3px;
            }
            QTabBar::tab {
                background: #2a2a2a;
                color: #DDDDDD;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #00AA66;
                color: white;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background: #3a3a3a;
            }
        """)

        # Tab A: ML Training (training ONLY - no recording)
        training_tab = self._build_training_tab()
        self.tab_widget.addTab(training_tab, "🎓 ML Training")

        # Tab B: Recording & Editing (unified recording + editing)
        recording_editing_tab = self._build_recording_editing_tab()
        self.tab_widget.addTab(recording_editing_tab, "🎙️ Recording & Editing")

        main_layout.addWidget(self.tab_widget)

        self.setLayout(main_layout)

    def _build_training_tab(self) -> QWidget:
        """Build Tab A: ML Training (training ONLY - v4.3.1-k0023)."""
        tab_widget = QWidget()
        tab_layout = QVBoxLayout()
        tab_layout.setContentsMargins(5, 5, 5, 5)

        # Create splitter for two columns
        splitter = QSplitter(Qt.Horizontal)

        # Left column: Training data selection
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 5, 0)

        # Sessions selector (read-only for training selection)
        sessions_group = self._build_sessions_group()
        sessions_group.setTitle("📁 Training Data (Select Sessions)")
        left_layout.addWidget(sessions_group)

        # Future: Import audio files section
        import_label = QLabel("💡 Tip: Use Recording & Editing tab to create and edit training sessions")
        import_label.setStyleSheet("font-size: 9pt; color: #888888; padding: 10px;")
        import_label.setWordWrap(True)
        left_layout.addWidget(import_label)

        left_layout.addStretch()

        splitter.addWidget(left_widget)

        # Right column: Training controls, models, logs
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(5, 0, 0, 0)

        right_layout.addWidget(self._build_training_group())
        right_layout.addWidget(self._build_model_management_group())
        right_layout.addWidget(self._build_log_group())

        splitter.addWidget(right_widget)

        # Set splitter sizes
        splitter.setSizes([300, 500])

        tab_layout.addWidget(splitter)

        tab_widget.setLayout(tab_layout)
        return tab_widget

    def _build_recording_editing_tab(self) -> QWidget:
        """Build Tab B: Recording & Editing (unified - v4.3.1-k0023)."""
        tab_widget = QWidget()
        tab_layout = QVBoxLayout()
        tab_layout.setContentsMargins(5, 5, 5, 5)

        # Mode selector
        mode_row = QHBoxLayout()
        mode_label = QLabel("Mode:")
        mode_label.setStyleSheet("font-size: 11pt; font-weight: bold; color: #DDDDDD;")
        mode_row.addWidget(mode_label)

        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["🎙️ New Recording", "✏️ Edit Existing Session"])
        self.mode_selector.setStyleSheet("""
            QComboBox {
                background: #2a2a2a;
                color: #DDDDDD;
                padding: 8px 12px;
                border: 2px solid #00AA66;
                border-radius: 4px;
                font-size: 11pt;
                font-weight: bold;
            }
            QComboBox:hover {
                border: 2px solid #00DD88;
                background: #3a3a3a;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border: none;
            }
        """)
        mode_row.addWidget(self.mode_selector)
        mode_row.addStretch()

        tab_layout.addLayout(mode_row)

        # Stacked widget for mode switching
        self.mode_stack = QStackedWidget()

        # Mode 1: Recording
        recording_widget = self._build_recording_mode_widget()
        self.mode_stack.addWidget(recording_widget)

        # Mode 2: Editing (embed SessionEditorWidget)
        self.session_editor = SessionEditorWidget(self.session_manager, parent=self)
        self.mode_stack.addWidget(self.session_editor)

        # Connect mode selector
        self.mode_selector.currentIndexChanged.connect(self.mode_stack.setCurrentIndex)

        tab_layout.addWidget(self.mode_stack)

        tab_widget.setLayout(tab_layout)
        return tab_widget

    def _build_recording_mode_widget(self) -> QWidget:
        """Build recording mode widget for Tab B."""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Create splitter for two columns
        splitter = QSplitter(Qt.Horizontal)

        # Left column: Recording controls
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 5, 0)

        left_layout.addWidget(self._build_recording_group())
        left_layout.addWidget(self._build_labeling_group())
        left_layout.addWidget(self._build_waveform_timeline_group())

        splitter.addWidget(left_widget)

        # Right column: Current session labels
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(5, 0, 0, 0)

        right_layout.addWidget(self._build_labels_table_group())

        splitter.addWidget(right_widget)

        # Set splitter sizes
        splitter.setSizes([500, 300])

        layout.addWidget(splitter)

        # Hotkey hint
        hotkey_hint = QLabel("💡 Tip: Press 1-9, 0, -, =, [ during recording to quickly add labels")
        hotkey_hint.setStyleSheet("font-size: 9pt; color: #888888; margin-top: 5px;")
        layout.addWidget(hotkey_hint)

        widget.setLayout(layout)
        return widget

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

        # v4.3.0-k0001: FSM State Indicator
        fsm_row = QHBoxLayout()
        fsm_label = QLabel("State:")
        fsm_label.setStyleSheet("font-size: 9pt; color: #888888;")
        fsm_row.addWidget(fsm_label)

        self.fsm_indicator = QLabel("IDLE")
        self.fsm_indicator.setStyleSheet("""
            font-size: 10pt;
            font-weight: bold;
            font-family: monospace;
            padding: 3px 8px;
            border-radius: 3px;
            background: #555555;
            color: #AAAAAA;
        """)
        fsm_row.addWidget(self.fsm_indicator)
        fsm_row.addStretch()
        layout.addLayout(fsm_row)

        # Control buttons row
        btn_row = QHBoxLayout()

        self.start_btn = QPushButton(f"▶ {tr('start')}" if callable(tr) else "▶ Start Recording")
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

        # v4.3.1-k0023: Pause button
        self.pause_btn = QPushButton("⏸ Pause")
        self.pause_btn.setStyleSheet("""
            QPushButton {
                background: #DDAA00;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 11pt;
            }
            QPushButton:hover { background: #FFCC00; }
            QPushButton:disabled { background: #555555; color: #888888; }
        """)
        self.pause_btn.setEnabled(False)
        self.pause_btn.clicked.connect(self._on_pause_recording)
        btn_row.addWidget(self.pause_btn)

        self.stop_btn = QPushButton(f"⏹ {tr('stop')}" if callable(tr) else "⏹ Stop Recording")
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

        overlay_row = QHBoxLayout()
        self.overlay_btn = QPushButton(tr('ml_overlay_launch') if callable(tr) else "Open quick overlay")
        self.overlay_btn.clicked.connect(self._launch_overlay)
        overlay_row.addWidget(self.overlay_btn)
        overlay_row.addStretch()
        layout.addLayout(overlay_row)

        group.setLayout(layout)
        return group

    def _build_labeling_group(self) -> QGroupBox:
        """Build labeling controls group (v4.3.1-k0023: Extended to 13 classes)."""
        group = QGroupBox("🏷️ Add Labels (Hotkeys 1-9, 0, -, =, [)")
        layout = QVBoxLayout()

        # v4.3.1-k0023: Label class buttons grid (3 rows x 5 columns for 13 classes)
        # Layout: Row 1: 5 buttons, Row 2: 5 buttons, Row 3: 3 buttons + 2 spacers
        buttons_per_row = [5, 5, 3]  # 5 + 5 + 3 = 13
        button_idx = 0

        for row_idx, num_buttons in enumerate(buttons_per_row):
            row = QHBoxLayout()

            # Always create 5 columns for uniform button sizing
            for col_idx in range(5):
                if col_idx < num_buttons and button_idx < len(SessionManager.DEFAULT_LABEL_CLASSES):
                    # Create button
                    label_class = SessionManager.DEFAULT_LABEL_CLASSES[button_idx]

                    # v4.3.1-k0023: Hotkey mapping for 13 classes
                    hotkey_map = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', '[']
                    hotkey = hotkey_map[button_idx] if button_idx < len(hotkey_map) else '?'

                    btn = QPushButton(f"{hotkey}: {label_class[:10]}")
                    btn.setToolTip(f"Add '{label_class}' label (Hotkey: {hotkey})")
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
                    btn.clicked.connect(lambda checked, i=button_idx: self._add_label_by_index(i))
                    row.addWidget(btn, 1)  # Stretch factor = 1
                    button_idx += 1
                else:
                    # Empty slot - add spacer for uniform sizing
                    row.addStretch(1)  # Stretch factor = 1

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

    def _build_waveform_timeline_group(self) -> QGroupBox:
        """Build waveform timeline editor group (v4.2.1)."""
        group = QGroupBox("📈 " + (tr('waveform_timeline') if callable(tr) else "Waveform Timeline"))
        layout = QVBoxLayout()

        # Waveform timeline widget
        self.waveform_timeline = WaveformTimelineWidget()
        self.waveform_timeline.segment_selected.connect(self._on_segment_selected)
        self.waveform_timeline.timestamp_clicked.connect(self._on_timestamp_clicked)
        layout.addWidget(self.waveform_timeline)

        # Segment labeling controls
        segment_row = QHBoxLayout()

        self.segment_info_label = QLabel(tr('no_selection') if callable(tr) else "No selection")
        self.segment_info_label.setStyleSheet("color: #888888; font-family: monospace;")
        segment_row.addWidget(self.segment_info_label)

        segment_row.addStretch()

        self.add_segment_label_btn = QPushButton("🏷️ " + (tr('add_label_to_selection') if callable(tr) else "Label Selection"))
        self.add_segment_label_btn.setStyleSheet("""
            QPushButton {
                background: #2a4a2a;
                color: #88FF88;
                padding: 6px 12px;
                border: 1px solid #446644;
                border-radius: 4px;
            }
            QPushButton:hover { background: #3a5a3a; }
            QPushButton:disabled { background: #1a1a1a; color: #555; }
        """)
        self.add_segment_label_btn.setEnabled(False)
        self.add_segment_label_btn.clicked.connect(self._add_label_to_segment)
        segment_row.addWidget(self.add_segment_label_btn)

        self.clear_segment_btn = QPushButton("✕ " + (tr('clear_selection') if callable(tr) else "Clear"))
        self.clear_segment_btn.setStyleSheet("""
            QPushButton {
                background: #4a2a2a;
                color: #FF8888;
                padding: 6px 12px;
                border: 1px solid #664444;
                border-radius: 4px;
            }
            QPushButton:hover { background: #5a3a3a; }
        """)
        self.clear_segment_btn.clicked.connect(self._clear_segment_selection)
        segment_row.addWidget(self.clear_segment_btn)

        layout.addLayout(segment_row)

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
        """Build saved sessions group (v4.3.1-k0023: Enhanced clarity)."""
        group = QGroupBox("📁 Saved Sessions")
        layout = QVBoxLayout()

        self.sessions_table = QTableWidget()
        # v4.3.1-k0023: Added "Created" column for better clarity
        self.sessions_table.setColumnCount(5)
        self.sessions_table.setHorizontalHeaderLabels(["Session ID", "Created", "Duration", "Labels", "Audio"])

        # v4.3.1-k0023: Better column sizing - Session ID gets more space
        header = self.sessions_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Session ID
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Created
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Duration
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Labels
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Audio

        self.sessions_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.sessions_table.setMaximumHeight(200)  # v4.3.1-k0023: Increased from 150

        # v4.3.1-k0023: Enhanced styling for better readability
        self.sessions_table.setStyleSheet("""
            QTableWidget {
                background: #1a1a1a;
                color: #DDDDDD;
                gridline-color: #444444;
                font-size: 9pt;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background: #00558B;
                color: white;
            }
            QHeaderView::section {
                background: #2a2a2a;
                color: #00DDFF;
                font-weight: bold;
                padding: 6px;
                border: 1px solid #444;
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

    def _build_model_management_group(self) -> QGroupBox:
        """Build model management UI group (v4.3.0-k0001)."""
        group = QGroupBox("🤖 Trained Models")
        layout = QVBoxLayout()

        # Current model status
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("Loaded:"))
        self.model_status_label = QLabel("No model loaded")
        self.model_status_label.setStyleSheet("font-weight: bold; color: #888888;")
        status_layout.addWidget(self.model_status_label)
        status_layout.addStretch()
        layout.addLayout(status_layout)

        # Model list
        self.models_table = QTableWidget()
        self.models_table.setColumnCount(3)
        self.models_table.setHorizontalHeaderLabels(["Model", "Accuracy", "Samples"])
        self.models_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.models_table.setMaximumHeight(120)
        self.models_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.models_table)

        # Action buttons
        btn_row = QHBoxLayout()

        self.load_model_btn = QPushButton("📥 Load Selected")
        self.load_model_btn.clicked.connect(self._on_load_model)
        btn_row.addWidget(self.load_model_btn)

        self.refresh_models_btn = QPushButton("🔄 Refresh")
        self.refresh_models_btn.clicked.connect(self._on_refresh_models)
        btn_row.addWidget(self.refresh_models_btn)

        layout.addLayout(btn_row)

        group.setLayout(layout)

        # Initial populate
        self._update_models_table()

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
        """Handle start recording button (v4.3.1-k0023: Enable pause button)."""
        if self.recording_controller.start_recording():
            self.start_btn.setEnabled(False)
            self.pause_btn.setEnabled(True)  # v4.3.1-k0023: Enable pause
            self.stop_btn.setEnabled(True)
            self._timer.start(100)  # Update every 100ms
            self._clear_labels_table()

    def _on_stop_recording(self):
        """Handle stop recording button."""
        session = self.recording_controller.stop_recording()
        if session:
            self._timer.stop()
            self.start_btn.setEnabled(True)
            self.pause_btn.setEnabled(False)
            self.stop_btn.setEnabled(False)
            self._update_sessions_table()

            QMessageBox.information(
                self,
                "Recording Saved",
                f"Session saved: {session.session_id}\n"
                f"Duration: {session.duration_sec:.1f}s\n"
                f"Labels: {len(session.labels)}"
            )

    def _on_pause_recording(self):
        """Handle pause/resume recording button (v4.3.1-k0023)."""
        state = self.recording_controller.state

        if state.fsm_state == RecordingStateEnum.RECORDING:
            # Pause the recording
            if self.recording_controller.pause_recording():
                self.pause_btn.setText("▶ Resume")
                self.pause_btn.setStyleSheet("""
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
        elif state.fsm_state == RecordingStateEnum.PAUSED:
            # Resume the recording
            if self.recording_controller.resume_recording():
                self.pause_btn.setText("⏸ Pause")
                self.pause_btn.setStyleSheet("""
                    QPushButton {
                        background: #DDAA00;
                        color: white;
                        font-weight: bold;
                        padding: 10px 20px;
                        border-radius: 5px;
                        font-size: 11pt;
                    }
                    QPushButton:hover { background: #FFCC00; }
                    QPushButton:disabled { background: #555555; color: #888888; }
                """)

    def _launch_overlay(self):
        """Open the quick recording overlay if available."""
        if callable(self._overlay_launcher):
            self._overlay_launcher()
        else:
            log("Overlay launcher not configured", "WARNING")

    def _on_recording_state_change(self, state):
        """Handle recording state changes (v4.3.1-k0023: Added PAUSED state)."""
        # Update legacy status label
        if state.fsm_state == RecordingStateEnum.PAUSED:
            self.status_label.setText("⏸ Paused")
            self.status_label.setStyleSheet("font-size: 12pt; font-weight: bold; color: #DDAA00;")
        elif state.is_recording:
            self.status_label.setText("🔴 Recording")
            self.status_label.setStyleSheet("font-size: 12pt; font-weight: bold; color: #FF4444;")
        else:
            self.status_label.setText("⚪ Ready")
            self.status_label.setStyleSheet("font-size: 12pt; font-weight: bold; color: #888888;")

        # v4.3.1-k0023: Update FSM indicator with color-coded states (added PAUSED)
        fsm_state = state.fsm_state
        fsm_styles = {
            RecordingStateEnum.IDLE: ("IDLE", "#555555", "#AAAAAA"),
            RecordingStateEnum.STARTING: ("STARTING", "#F39C12", "#2C2C2C"),  # Orange
            RecordingStateEnum.RECORDING: ("RECORDING", "#E74C3C", "#FFFFFF"),  # Red
            RecordingStateEnum.PAUSED: ("PAUSED", "#DDAA00", "#FFFFFF"),  # Yellow (v4.3.1-k0023)
            RecordingStateEnum.STOPPING: ("STOPPING", "#E67E22", "#FFFFFF"),  # Dark orange
            RecordingStateEnum.ERROR: ("ERROR", "#C0392B", "#FFFFFF"),  # Dark red
        }

        if fsm_state in fsm_styles:
            text, bg_color, fg_color = fsm_styles[fsm_state]
            self.fsm_indicator.setText(text)
            self.fsm_indicator.setStyleSheet(f"""
                font-size: 10pt;
                font-weight: bold;
                font-family: monospace;
                padding: 3px 8px;
                border-radius: 3px;
                background: {bg_color};
                color: {fg_color};
            """)

        # v4.3.0-k0001: Toast notifications for state changes
        if self.toast:
            if fsm_state == RecordingStateEnum.RECORDING:
                self.toast.show_toast("Recording started", "success", duration=2000)
            elif fsm_state == RecordingStateEnum.IDLE and not state.is_recording:
                # Only show on actual stop (not initial IDLE)
                if hasattr(self, '_was_recording'):
                    self.toast.show_toast("Recording stopped", "info", duration=2000)
            elif fsm_state == RecordingStateEnum.ERROR:
                self.toast.show_toast("Recording error occurred", "error", duration=4000)

        # Track previous state
        self._was_recording = state.is_recording

    def _update_timer(self):
        """Update elapsed time display."""
        elapsed = self.recording_controller.state.elapsed_sec
        mins = int(elapsed // 60)
        secs = int(elapsed % 60)
        self.elapsed_label.setText(f"{mins}:{secs:02d}")

        # v4.2.1: Update waveform display periodically during recording
        if hasattr(self, '_pending_waveform_update') and self._pending_waveform_update:
            self._update_waveform_data()
            self._pending_waveform_update = False

    # ========================================================================
    # LABELING HANDLERS
    # ========================================================================

    def _add_label_by_index(self, index: int):
        """Add label by class index."""
        if not self.recording_controller.state.is_recording:
            QMessageBox.warning(self, "Not Recording", "Start recording first to add labels.")
            return

        label = self.recording_controller.add_label_hotkey(index + 1)
        if label:
            self._add_label_to_table(label)

    def _add_custom_label(self):
        """Add custom label via dialog."""
        if not self.recording_controller.state.is_recording:
            QMessageBox.warning(self, "Not Recording", "Start recording first to add labels.")
            return

        dialog = AddLabelDialog(self, timestamp=self.recording_controller.state.elapsed_sec)
        if dialog.exec_() == QDialog.Accepted:
            values = dialog.get_values()
            label = self.recording_controller.add_label(
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
            # Remove label from session
            if self.recorder.current_session.remove_label(label_id):
                # CRITICAL: Save session to disk to persist the deletion
                self.session_manager.save_session(self.recorder.current_session)
                # Update UI
                self.labels_table.removeRow(row)
                log(f"Label {label_id} deleted and saved for session {self.recorder.current_session.session_id}", "INFO")
            else:
                log(f"Failed to remove label {label_id} - not found in session", "WARNING")

    # ========================================================================
    # WAVEFORM TIMELINE HANDLERS (v4.2.1)
    # ========================================================================

    def _on_segment_selected(self, start_sec: float, end_sec: float):
        """Handle segment selection from waveform timeline."""
        duration = end_sec - start_sec
        self.segment_info_label.setText(
            f"Selection: {start_sec:.2f}s - {end_sec:.2f}s ({duration:.2f}s)"
        )
        self.add_segment_label_btn.setEnabled(True)
        self._selected_segment = (start_sec, end_sec)

    def _on_timestamp_clicked(self, timestamp_sec: float):
        """Handle timestamp click from waveform timeline."""
        # If recording, add instant label at this position
        if self.recorder.is_recording:
            # Just update position, labeling done via buttons
            pass
        self.segment_info_label.setText(f"Position: {timestamp_sec:.2f}s")
        self.add_segment_label_btn.setEnabled(False)
        self._selected_segment = None

    def _add_label_to_segment(self):
        """Add label to selected segment."""
        if not hasattr(self, '_selected_segment') or self._selected_segment is None:
            return

        start_sec, end_sec = self._selected_segment

        # Show dialog to choose label class
        dialog = AddLabelDialog(self, timestamp=start_sec)
        if dialog.exec_() == QDialog.Accepted:
            values = dialog.get_values()

            if self.recorder.current_session:
                # Add label with segment duration info in description
                desc = values["description"]
                if desc:
                    desc += f" (segment: {end_sec - start_sec:.2f}s)"
                else:
                    desc = f"segment: {start_sec:.2f}s - {end_sec:.2f}s"

                label = AudioLabel(
                    id=len(self.recorder.current_session.labels),
                    timestamp_sec=start_sec,
                    label_class=values["label_class"],
                    description=desc
                )
                self.recorder.current_session.labels.append(label)
                self._add_label_to_table(label)
                self._update_waveform_markers()

    def _clear_segment_selection(self):
        """Clear segment selection."""
        self.waveform_timeline.clear_selection()
        self.segment_info_label.setText(tr('no_selection') if callable(tr) else "No selection")
        self.add_segment_label_btn.setEnabled(False)
        self._selected_segment = None

    def _update_waveform_markers(self):
        """Update waveform timeline with current session markers."""
        if self.recorder.current_session:
            markers = [
                (label.timestamp_sec, label.label_class)
                for label in self.recorder.current_session.labels
            ]
            self.waveform_timeline.set_markers(markers)

    def _update_waveform_data(self):
        """Update waveform display with current audio data."""
        if self.recorder.current_session and hasattr(self.recorder, '_audio_buffer'):
            audio_data = self.recorder._audio_buffer
            if audio_data is not None and len(audio_data) > 0:
                sample_rate = getattr(self.recorder, '_sample_rate', 48000)
                self.waveform_timeline.set_audio_data(audio_data, sample_rate)

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

        # v4.3.0-k0001: Toast notification
        if self.toast:
            self.toast.show_toast(f"Training started with {total_labels} labels", "info", duration=3000)

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
        """Handle training completion (v4.3.0-k0001: Toast)."""
        self.train_btn.setEnabled(True)
        self.cancel_train_btn.hide()

        if result.success:
            self.progress_bar.setFormat("100% - Complete!")
            self._log_message(f"✅ Training completed!")
            self._log_message(f"   Accuracy: {result.accuracy:.1%}")
            self._log_message(f"   Model: {result.model_path}")
            self._log_message(f"   Time: {result.training_time_sec:.1f}s")

            # v4.3.0-k0001: Success toast
            if self.toast:
                self.toast.show_toast(
                    f"Model trained! Accuracy: {result.accuracy:.1%}",
                    "success",
                    duration=5000
                )

            # v4.3.0-k0001: Refresh models table
            self._update_models_table()

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

            # v4.3.0-k0001: Error toast
            if self.toast:
                self.toast.show_toast("Training failed", "error", duration=4000)

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
        """Update the saved sessions table (v4.3.1-k0023: Enhanced with creation time)."""
        sessions = self.session_manager.list_sessions()

        self.sessions_table.setRowCount(len(sessions))

        total_duration = 0
        total_labels = 0

        for row, session_info in enumerate(sessions):
            # Column 0: Session ID
            session_id_item = QTableWidgetItem(session_info["session_id"])
            session_id_item.setToolTip(f"Session: {session_info['session_id']}")
            self.sessions_table.setItem(row, 0, session_id_item)

            # Column 1: Created time (v4.3.1-k0023: NEW)
            # Extract timestamp from session_id (format: session_YYYYMMDD_HHMMSS)
            session_id = session_info["session_id"]
            if session_id.startswith("session_"):
                try:
                    date_part = session_id[8:16]  # YYYYMMDD
                    time_part = session_id[17:23]  # HHMMSS
                    created_str = f"{date_part[6:8]}/{date_part[4:6]} {time_part[0:2]}:{time_part[2:4]}"
                except:
                    created_str = "N/A"
            else:
                created_str = "N/A"

            created_item = QTableWidgetItem(created_str)
            created_item.setToolTip(f"Created: {created_str}")
            self.sessions_table.setItem(row, 1, created_item)

            # Column 2: Duration
            duration = session_info["duration_sec"]
            total_duration += duration
            mins = int(duration // 60)
            secs = int(duration % 60)
            duration_item = QTableWidgetItem(f"{mins}:{secs:02d}")
            duration_item.setToolTip(f"Duration: {mins}m {secs}s")
            self.sessions_table.setItem(row, 2, duration_item)

            # Column 3: Labels
            labels = session_info["label_count"]
            total_labels += labels
            labels_item = QTableWidgetItem(str(labels))
            labels_item.setToolTip(f"{labels} labels")
            # v4.3.1-k0023: Color-code based on label count
            if labels == 0:
                labels_item.setForeground(QColor("#FF4444"))  # Red if no labels
            elif labels < 5:
                labels_item.setForeground(QColor("#FFAA00"))  # Orange if few labels
            else:
                labels_item.setForeground(QColor("#00DD00"))  # Green if good labels
            self.sessions_table.setItem(row, 3, labels_item)

            # Column 4: Audio status
            has_audio = "✅" if session_info["has_audio"] else "❌"
            audio_item = QTableWidgetItem(has_audio)
            audio_item.setToolTip("Audio file present" if session_info["has_audio"] else "No audio file")
            self.sessions_table.setItem(row, 4, audio_item)

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
        self.recording_controller.feed_audio(block)
        if self.recording_controller.state.is_recording:
            # v4.2.1: Update waveform timeline periodically
            # (actual update happens via timer to avoid too frequent redraws)
            self._pending_waveform_update = True

    # ========================================================================
    # MODEL MANAGEMENT (v4.3.0-k0001)
    # ========================================================================

    def _update_models_table(self):
        """Update the trained models table."""
        models = self.model_registry.list_models()

        self.models_table.setRowCount(len(models))

        for row, model_info in enumerate(models):
            # Model name
            self.models_table.setItem(row, 0, QTableWidgetItem(model_info.name))

            # Accuracy
            acc_item = QTableWidgetItem(f"{model_info.accuracy:.1%}")
            self.models_table.setItem(row, 1, acc_item)

            # Samples
            self.models_table.setItem(row, 2, QTableWidgetItem(str(model_info.samples_used)))

        # Update loaded model status
        if self.ml_detector.is_model_loaded:
            model_info = self.ml_detector.model_info
            self.model_status_label.setText(
                f"{model_info.name} ({model_info.accuracy:.1%})"
            )
            self.model_status_label.setStyleSheet("font-weight: bold; color: #00DD00;")
        else:
            self.model_status_label.setText("No model loaded")
            self.model_status_label.setStyleSheet("font-weight: bold; color: #888888;")

    def _on_load_model(self):
        """Handle load model button click."""
        selected_rows = self.models_table.selectedIndexes()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a model to load.")
            return

        row = selected_rows[0].row()
        model_name = self.models_table.item(row, 0).text()

        if self.ml_detector.load_model(model_name):
            self._update_models_table()
            if self.toast:
                self.toast.show_toast(f"Model loaded: {model_name}", "success", duration=3000)
        else:
            if self.toast:
                self.toast.show_toast("Failed to load model", "error", duration=3000)

    def _on_refresh_models(self):
        """Handle refresh models button click."""
        self._update_models_table()
        if self.toast:
            models_count = self.models_table.rowCount()
            self.toast.show_toast(f"Refreshed: {models_count} models found", "info", duration=2000)

    # ========================================================================
    # KEYBOARD SHORTCUTS
    # ========================================================================

    def keyPressEvent(self, event: QKeyEvent):
        """Handle keyboard shortcuts for quick labeling (v4.3.1-k0023: Extended to 13 classes)."""
        if not self.recording_controller.state.is_recording:
            super().keyPressEvent(event)
            return

        key = event.key()

        # v4.3.1-k0023: Extended hotkeys for 13 classes: 1-9, 0, -, =, [
        # Mapping: 1→0, 2→1, 3→2, 4→3, 5→4, 6→5, 7→6, 8→7, 9→8, 0→9, -→10, =→11, [→12
        key_to_index = {
            Qt.Key_1: 0,   # Walk
            Qt.Key_2: 1,   # Run
            Qt.Key_3: 2,   # Shot
            Qt.Key_4: 3,   # Crouch
            Qt.Key_5: 4,   # Explosion
            Qt.Key_6: 5,   # NPC
            Qt.Key_7: 6,   # NPC_Arc
            Qt.Key_8: 7,   # Jump
            Qt.Key_9: 8,   # Doors
            Qt.Key_0: 9,   # Vehicle
            Qt.Key_Minus: 10,      # Voice
            Qt.Key_Equal: 11,      # Ambient
            Qt.Key_BracketLeft: 12 # Other
        }

        if key in key_to_index:
            index = key_to_index[key]
            if index < len(SessionManager.DEFAULT_LABEL_CLASSES):
                self._add_label_by_index(index)
                return

        # Backspace to remove last label
        if key == Qt.Key_Backspace:
            if self.recording_controller.remove_last_label():
                if self.labels_table.rowCount() > 0:
                    self.labels_table.removeRow(self.labels_table.rowCount() - 1)
            return

        super().keyPressEvent(event)
