"""Internal self-test runner for RadarSuite."""

from __future__ import annotations

import traceback
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable, List, Optional, Tuple

import numpy as np

try:  # pragma: no cover - optional in headless tests
    from PyQt5.QtWidgets import QApplication
    QT_AVAILABLE = True
except Exception:  # pragma: no cover - no Qt in environment
    QT_AVAILABLE = False

try:
    from ..core.logger import log
    from ..core.config import ConfigManager
except ImportError:  # pragma: no cover - fallback for script mode
    from core.logger import log  # type: ignore
    from core.config import ConfigManager  # type: ignore


@dataclass
class SelfTestResult:
    name: str
    success: bool
    message: str = ""
    error: Optional[str] = None


class SelfTestRunner:
    """Executes quick or full self-tests inside the app."""

    def __init__(self, config_manager: Optional[ConfigManager] = None, include_gui_checks: bool = True):
        self.config_manager = config_manager or ConfigManager()
        self.include_gui_checks = include_gui_checks and QT_AVAILABLE
        self._log_lines: List[str] = []
        self._report_path: Optional[Path] = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def run_quick(self) -> Tuple[List[SelfTestResult], Path]:
        steps: List[Tuple[str, Callable[[], None]]] = [
            ("Config load", self._step_config_load),
            ("ML imports", self._step_ml_imports),
            ("Recording FSM", self._step_recording_flow),
        ]

        if self.include_gui_checks:
            steps.append(("Overlay logic", self._step_overlay_logic))

        results = self._execute_steps(steps)
        return results, self._report_path or Path("logs/selftest_latest.log")

    # ------------------------------------------------------------------
    # Steps
    # ------------------------------------------------------------------
    def _step_config_load(self) -> None:
        cfg = self.config_manager.load()
        _ = cfg.get("ml_overlay", {})
        if "audio" not in cfg:
            raise AssertionError("Audio section missing")

    def _step_ml_imports(self) -> None:
        from ..widgets.ml_training_panel import MLTrainingPanel  # noqa: F401
        from ..widgets.ml_quick_overlay import MLQuickRecordOverlay  # noqa: F401
        from ..ml.training import RecordingController  # noqa: F401

    def _step_recording_flow(self) -> None:
        from ..ml.training import RecordingController
        from ..ml.training.session_manager import SessionManager

        manager = SessionManager(base_path=Path("./Data/TestSessions"))
        controller = RecordingController(session_manager=manager)
        assert controller.start_recording()
        block = np.zeros((1024,))
        controller.feed_audio(block)
        controller.add_label("test")
        session = controller.stop_recording()
        assert session is not None

    def _step_overlay_logic(self) -> None:
        if not QT_AVAILABLE:
            return
        from ..ml.training import RecordingController
        from ..widgets.ml_quick_overlay import MLQuickRecordOverlay
        from ..ml.training.session_manager import SessionManager

        owned_app = None
        app = QApplication.instance()
        if app is None:
            owned_app = QApplication([])
        controller = RecordingController(session_manager=SessionManager(base_path=Path("./Data/TestSessions")))
        overlay = MLQuickRecordOverlay(controller=controller, config_manager=self.config_manager)
        overlay.hide()
        overlay._apply_size_preset()  # noqa: SLF001
        overlay._toggle_frameless(1)
        overlay.close()
        if owned_app:
            owned_app.quit()

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    def _execute_steps(self, steps: List[Tuple[str, Callable[[], None]]]) -> List[SelfTestResult]:
        results: List[SelfTestResult] = []
        for name, func in steps:
            try:
                func()
                result = SelfTestResult(name=name, success=True, message="OK")
                self._log_lines.append(f"✓ {name}")
            except Exception as exc:  # pragma: no cover - defensive
                tb = traceback.format_exc()
                result = SelfTestResult(name=name, success=False, message=str(exc), error=tb)
                self._log_lines.append(f"✗ {name}: {exc}")
            results.append(result)

        self._report_path = self._write_report(results)
        return results

    def _write_report(self, results: List[SelfTestResult]) -> Path:
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = logs_dir / f"selftest_{timestamp}.log"
        with path.open("w", encoding="utf-8") as fh:
            fh.write("RadarSuite Self-Test Report\n")
            for line in self._log_lines:
                fh.write(line + "\n")
            for result in results:
                if not result.success and result.error:
                    fh.write(result.error + "\n")
        return path
