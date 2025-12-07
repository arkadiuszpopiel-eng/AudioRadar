import pytest

pytest.importorskip("numpy", reason="numpy required for self-test runner checks")

from diagnostics.selftest import SelfTestRunner


def test_selftest_runner_quick(tmp_path, monkeypatch):
    runner = SelfTestRunner(include_gui_checks=False)

    # Point session manager writes to temp directory via monkeypatching default path
    monkeypatch.chdir(tmp_path)
    results, report = runner.run_quick()

    assert results
    assert report.exists()
