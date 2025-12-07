import copy

import pytest

pytest.importorskip("numpy", reason="numpy required for overlay logic tests")

from ml.training import RecordingController
from ml.training.session_manager import SessionManager


class _FakeConfigManager:
    def __init__(self, base_config):
        self.default_config = copy.deepcopy(base_config)
        self._config = copy.deepcopy(base_config)
        self.load_calls = 0
        self.save_calls = 0

    def load(self):
        self.load_calls += 1
        return copy.deepcopy(self._config)

    def save(self, cfg):
        self.save_calls += 1
        self._config = copy.deepcopy(cfg)


def test_overlay_uses_cached_config(tmp_path):
    pytest.importorskip("PyQt5", reason="PyQt5 not installed")
    from PyQt5.QtWidgets import QApplication
    from widgets.ml_quick_overlay import MLQuickRecordOverlay

    app = QApplication.instance() or QApplication([])
    base_manager = SessionManager(base_path=tmp_path)
    controller = RecordingController(session_manager=base_manager)

    from core.config import ConfigManager

    fake_cfg = _FakeConfigManager(ConfigManager().default_config)
    overlay = MLQuickRecordOverlay(controller=controller, config_manager=fake_cfg)
    assert fake_cfg.load_calls == 1

    overlay._apply_size_preset()  # noqa: SLF001
    overlay._on_opacity_changed(70)
    overlay.close()

    assert fake_cfg.load_calls == 1
    assert fake_cfg.save_calls >= 1

    if not QApplication.instance().closingDown():
        app.quit()
