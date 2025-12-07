import copy

from core.config import ConfigManager


def test_multiple_loads_are_consistent(tmp_path):
    cm = ConfigManager()
    cm.config_dir = tmp_path
    cm.config_file = tmp_path / "config.json"

    cm.save(copy.deepcopy(cm.default_config))
    first = cm.load()
    second = cm.load()
    assert first["ml_overlay"]["opacity"] == second["ml_overlay"]["opacity"]


def test_overlay_roundtrip(tmp_path):
    cm = ConfigManager()
    cm.config_dir = tmp_path
    cm.config_file = tmp_path / "config.json"
    config = copy.deepcopy(cm.default_config)
    config["ml_overlay"].update({"opacity": 0.5, "frameless": False, "size_preset": "large"})
    cm.save(config)

    loaded = cm.load()
    assert loaded["ml_overlay"]["opacity"] == 0.5
    assert loaded["ml_overlay"]["frameless"] is False
    assert loaded["ml_overlay"]["size_preset"] == "large"
