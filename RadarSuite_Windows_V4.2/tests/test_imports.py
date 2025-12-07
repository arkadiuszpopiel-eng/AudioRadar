"""Smoke tests for critical imports."""

import importlib

import pytest


def test_ui_imports():
    pytest.importorskip("PyQt5", reason="PyQt5 not installed")
    assert importlib.import_module("main")
    assert importlib.import_module("ui.builder")
    assert importlib.import_module("widgets.ml_quick_overlay")


def test_core_imports():
    assert importlib.import_module("core.config")
    assert importlib.import_module("ml.training.recording_controller")
