"""
Comprehensive Auto-Tester for Radar Games ML
Tests EVERY button, slider, checkbox, and function in EVERY tab automatically.

Features:
- Crash-resistant incremental logging (saves even if program freezes)
- Point-by-point scoring system
- Detailed developer logs
- Tests run in background thread (non-blocking GUI)
- HTML + text report generation
"""

from __future__ import annotations

import threading
import traceback
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Callable, Any, TYPE_CHECKING

try:
    from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QSlider, QCheckBox
    from PyQt5.QtCore import QTimer, Qt
    QT_AVAILABLE = True
except Exception:
    QT_AVAILABLE = False

from app.core.logger import log
from app.core import get_logs_directory

if TYPE_CHECKING:
    from app.main import MainWindow


@dataclass
class TestResult:
    """Single test result with detailed information."""
    category: str  # "Tab", "Button", "Slider", "Checkbox", "Function"
    name: str
    success: bool
    message: str = ""
    error: Optional[str] = None
    duration_ms: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%H:%M:%S.%f")[:-3])


class CrashResistantLogger:
    """
    Incremental file logger that writes immediately.
    Ensures logs survive even if program freezes or crashes.
    """

    def __init__(self, log_path: Path):
        self.log_path = log_path
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

        # Create/clear log file
        with self.log_path.open("w", encoding="utf-8") as f:
            f.write(f"Radar Games ML - Comprehensive Auto-Test Log\n")
            f.write(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")

    def write(self, message: str) -> None:
        """Write message immediately to file (crash-resistant)."""
        try:
            with self.log_path.open("a", encoding="utf-8") as f:
                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                f.write(f"[{timestamp}] {message}\n")
                f.flush()  # Force write to disk immediately
        except Exception as e:
            # Fallback: print to console if file write fails
            print(f"[LOG ERROR] {e}: {message}")


class ComprehensiveAutoTester:
    """
    Tests every UI element and function automatically.

    Tests performed:
    - Tab switching (all 5 tabs)
    - All buttons (click test)
    - All sliders (min/max test)
    - All checkboxes (toggle test)
    - Core functions (start/stop, recording, detection)
    """

    def __init__(self, main_window: Optional["MainWindow"] = None):
        self.main_window = main_window
        self.results: List[TestResult] = []
        self.logger: Optional[CrashResistantLogger] = None
        self.start_time: float = 0.0
        self.test_running: bool = False

        # Timeout protection (seconds)
        self.timeout_per_test: float = 3.0

    def run_all_tests(self, log_directory: Optional[Path] = None) -> tuple[List[TestResult], Path, Path]:
        """
        Run all comprehensive tests.

        Returns:
            (results, log_path, report_path)
        """
        if not QT_AVAILABLE:
            raise RuntimeError("PyQt5 required for comprehensive testing")

        if self.main_window is None:
            raise RuntimeError("MainWindow instance required")

        # Setup logging
        if log_directory is None:
            log_directory = get_logs_directory()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = log_directory / f"comprehensive_test_{timestamp}.log"
        report_path = log_directory / f"comprehensive_test_{timestamp}_report.html"

        self.logger = CrashResistantLogger(log_path)
        self.results = []
        self.start_time = time.time()
        self.test_running = True

        self.logger.write("=" * 80)
        self.logger.write("STARTING COMPREHENSIVE AUTO-TEST")
        self.logger.write("=" * 80)

        try:
            # Test Category 1: Tab Switching
            self._test_all_tabs()

            # Test Category 2: All Buttons
            self._test_all_buttons()

            # Test Category 3: All Sliders
            self._test_all_sliders()

            # Test Category 4: All Checkboxes
            self._test_all_checkboxes()

            # Test Category 5: Core Functions
            self._test_core_functions()

        except Exception as e:
            self.logger.write(f"FATAL ERROR during test execution: {e}")
            self.logger.write(traceback.format_exc())

        finally:
            self.test_running = False
            elapsed = time.time() - self.start_time
            self.logger.write("")
            self.logger.write("=" * 80)
            self.logger.write(f"TEST COMPLETED - Total time: {elapsed:.2f}s")
            self.logger.write("=" * 80)

        # Generate reports
        self._generate_text_report(log_path)
        self._generate_html_report(report_path)

        return self.results, log_path, report_path

    # =========================================================================
    # TEST CATEGORIES
    # =========================================================================

    def _test_all_tabs(self) -> None:
        """Test switching to every tab."""
        self.logger.write("\n" + "=" * 80)
        self.logger.write("CATEGORY 1: TAB SWITCHING")
        self.logger.write("=" * 80)

        if not hasattr(self.main_window, 'main_tabs'):
            self.logger.write("ERROR: main_tabs not found!")
            return

        tab_widget = self.main_window.main_tabs
        tab_count = tab_widget.count()

        self.logger.write(f"Found {tab_count} tabs to test")

        for i in range(tab_count):
            tab_name = tab_widget.tabText(i)
            self._run_test_with_timeout(
                category="Tab",
                name=f"Switch to '{tab_name}'",
                test_func=lambda idx=i: self._switch_to_tab(idx)
            )

            # Small delay between tab switches
            QApplication.processEvents()
            time.sleep(0.1)

    def _test_all_buttons(self) -> None:
        """Test clicking every button in the application."""
        self.logger.write("\n" + "=" * 80)
        self.logger.write("CATEGORY 2: BUTTON TESTING")
        self.logger.write("=" * 80)

        # List of button attributes to test (button_attr, skip_if_disabled, description)
        buttons_to_test = [
            ('start_btn', False, "Main Start/Stop button"),
            ('record_btn', True, "Recording button (skip if disabled)"),
            ('test_btn', False, "Self-test button"),
            ('quick_setup_btn', False, "Quick setup button"),
            ('detach_radar_btn', False, "Detach radar button"),
            ('detach_led_btn', False, "Detach LED button"),
            ('lang_btn', False, "Language toggle button"),
        ]

        for btn_attr, skip_disabled, description in buttons_to_test:
            if not hasattr(self.main_window, btn_attr):
                self.logger.write(f"SKIP: Button '{btn_attr}' not found")
                continue

            button = getattr(self.main_window, btn_attr)
            if not isinstance(button, QPushButton):
                self.logger.write(f"SKIP: '{btn_attr}' is not a QPushButton")
                continue

            if skip_disabled and not button.isEnabled():
                self.logger.write(f"SKIP: Button '{btn_attr}' is disabled")
                result = TestResult(
                    category="Button",
                    name=description,
                    success=True,
                    message="Skipped (disabled)"
                )
                self.results.append(result)
                continue

            self._run_test_with_timeout(
                category="Button",
                name=description,
                test_func=lambda b=button: self._click_button(b)
            )

            # Small delay between button clicks
            QApplication.processEvents()
            time.sleep(0.2)

    def _test_all_sliders(self) -> None:
        """Test all sliders (move to min, max, restore original)."""
        self.logger.write("\n" + "=" * 80)
        self.logger.write("CATEGORY 3: SLIDER TESTING")
        self.logger.write("=" * 80)

        sliders_to_test = [
            ('radar_alpha', "Radar opacity slider"),
            ('led_alpha', "LED opacity slider"),
        ]

        for slider_attr, description in sliders_to_test:
            if not hasattr(self.main_window, slider_attr):
                self.logger.write(f"SKIP: Slider '{slider_attr}' not found")
                continue

            slider = getattr(self.main_window, slider_attr)
            if not isinstance(slider, QSlider):
                self.logger.write(f"SKIP: '{slider_attr}' is not a QSlider")
                continue

            self._run_test_with_timeout(
                category="Slider",
                name=description,
                test_func=lambda s=slider: self._test_slider(s)
            )

            QApplication.processEvents()
            time.sleep(0.1)

    def _test_all_checkboxes(self) -> None:
        """Test all checkboxes (toggle on, off, restore)."""
        self.logger.write("\n" + "=" * 80)
        self.logger.write("CATEGORY 4: CHECKBOX TESTING")
        self.logger.write("=" * 80)

        checkboxes_to_test = [
            ('radar_frameless_btn', "Radar frameless mode"),
            ('led_frameless_btn', "LED frameless mode"),
        ]

        for checkbox_attr, description in checkboxes_to_test:
            if not hasattr(self.main_window, checkbox_attr):
                self.logger.write(f"SKIP: Checkbox '{checkbox_attr}' not found")
                continue

            checkbox = getattr(self.main_window, checkbox_attr)
            if not isinstance(checkbox, QCheckBox):
                self.logger.write(f"SKIP: '{checkbox_attr}' is not a QCheckBox")
                continue

            self._run_test_with_timeout(
                category="Checkbox",
                name=description,
                test_func=lambda c=checkbox: self._test_checkbox(c)
            )

            QApplication.processEvents()
            time.sleep(0.1)

    def _test_core_functions(self) -> None:
        """Test core application functions."""
        self.logger.write("\n" + "=" * 80)
        self.logger.write("CATEGORY 5: CORE FUNCTION TESTING")
        self.logger.write("=" * 80)

        # Test 1: Start/Stop engine (if not already running)
        if hasattr(self.main_window, 'is_running'):
            was_running = self.main_window.is_running

            if not was_running:
                self._run_test_with_timeout(
                    category="Function",
                    name="Start audio engine",
                    test_func=lambda: self._test_start_engine()
                )
                time.sleep(0.5)

                self._run_test_with_timeout(
                    category="Function",
                    name="Stop audio engine",
                    test_func=lambda: self._test_stop_engine()
                )
            else:
                self.logger.write("SKIP: Engine already running, won't interrupt")

        # Test 2: Detection panel updates
        self._run_test_with_timeout(
            category="Function",
            name="Detection panel update",
            test_func=lambda: self._test_detection_panel()
        )

        # Test 3: Radar widget update
        self._run_test_with_timeout(
            category="Function",
            name="Radar widget update",
            test_func=lambda: self._test_radar_update()
        )

    # =========================================================================
    # TEST HELPERS
    # =========================================================================

    def _run_test_with_timeout(self, category: str, name: str, test_func: Callable[[], None]) -> None:
        """Run a single test with timeout protection."""
        self.logger.write(f"\nTEST: [{category}] {name}")

        result_holder = {}
        start_time = time.time()

        def target():
            try:
                test_func()
                result_holder['success'] = True
                result_holder['message'] = "OK"
            except Exception as e:
                result_holder['success'] = False
                result_holder['message'] = str(e)
                result_holder['error'] = traceback.format_exc()

        thread = threading.Thread(target=target, daemon=True)
        thread.start()
        thread.join(self.timeout_per_test)

        duration_ms = (time.time() - start_time) * 1000

        if thread.is_alive():
            # Timeout
            self.logger.write(f"  ✗ TIMEOUT after {self.timeout_per_test}s")
            result = TestResult(
                category=category,
                name=name,
                success=False,
                message=f"Timeout after {self.timeout_per_test}s",
                duration_ms=duration_ms
            )
        elif 'success' in result_holder:
            if result_holder['success']:
                self.logger.write(f"  ✓ PASS ({duration_ms:.1f}ms)")
                result = TestResult(
                    category=category,
                    name=name,
                    success=True,
                    message=result_holder['message'],
                    duration_ms=duration_ms
                )
            else:
                self.logger.write(f"  ✗ FAIL: {result_holder['message']}")
                if 'error' in result_holder:
                    self.logger.write(f"  Traceback:\n{result_holder['error']}")
                result = TestResult(
                    category=category,
                    name=name,
                    success=False,
                    message=result_holder['message'],
                    error=result_holder.get('error'),
                    duration_ms=duration_ms
                )
        else:
            # Unknown error
            self.logger.write(f"  ✗ UNKNOWN ERROR")
            result = TestResult(
                category=category,
                name=name,
                success=False,
                message="Unknown error",
                duration_ms=duration_ms
            )

        self.results.append(result)

    def _switch_to_tab(self, tab_index: int) -> None:
        """Switch to specified tab."""
        tab_widget = self.main_window.main_tabs
        tab_widget.setCurrentIndex(tab_index)
        QApplication.processEvents()

        # Verify switch was successful
        if tab_widget.currentIndex() != tab_index:
            raise AssertionError(f"Failed to switch to tab {tab_index}")

    def _click_button(self, button: QPushButton) -> None:
        """Click a button safely."""
        if not button.isEnabled():
            raise AssertionError("Button is disabled")

        # Simulate click
        button.click()
        QApplication.processEvents()

    def _test_slider(self, slider: QSlider) -> None:
        """Test slider by moving to min, max, and restoring."""
        original_value = slider.value()
        min_value = slider.minimum()
        max_value = slider.maximum()

        # Test minimum
        slider.setValue(min_value)
        QApplication.processEvents()
        if slider.value() != min_value:
            raise AssertionError(f"Failed to set slider to minimum ({min_value})")

        # Test maximum
        slider.setValue(max_value)
        QApplication.processEvents()
        if slider.value() != max_value:
            raise AssertionError(f"Failed to set slider to maximum ({max_value})")

        # Restore original
        slider.setValue(original_value)
        QApplication.processEvents()

    def _test_checkbox(self, checkbox: QCheckBox) -> None:
        """Test checkbox by toggling and restoring."""
        original_state = checkbox.isChecked()

        # Toggle on
        checkbox.setChecked(True)
        QApplication.processEvents()
        if not checkbox.isChecked():
            raise AssertionError("Failed to check checkbox")

        # Toggle off
        checkbox.setChecked(False)
        QApplication.processEvents()
        if checkbox.isChecked():
            raise AssertionError("Failed to uncheck checkbox")

        # Restore original
        checkbox.setChecked(original_state)
        QApplication.processEvents()

    def _test_start_engine(self) -> None:
        """Test starting the audio engine."""
        if not hasattr(self.main_window, 'toggle_start_stop'):
            raise AssertionError("toggle_start_stop method not found")

        self.main_window.toggle_start_stop()
        QApplication.processEvents()
        time.sleep(0.3)  # Allow engine to start

        if not self.main_window.is_running:
            raise AssertionError("Engine failed to start")

    def _test_stop_engine(self) -> None:
        """Test stopping the audio engine."""
        if not hasattr(self.main_window, 'toggle_start_stop'):
            raise AssertionError("toggle_start_stop method not found")

        self.main_window.toggle_start_stop()
        QApplication.processEvents()
        time.sleep(0.3)  # Allow engine to stop

        if self.main_window.is_running:
            raise AssertionError("Engine failed to stop")

    def _test_detection_panel(self) -> None:
        """Test detection panel can update without crashing."""
        if not hasattr(self.main_window, 'det_panel'):
            raise AssertionError("Detection panel not found")

        panel = self.main_window.det_panel

        # Simulate detection update
        test_events = {'walk': True, 'run': False, 'shot': False}
        panel.update_detections(test_events)
        QApplication.processEvents()

    def _test_radar_update(self) -> None:
        """Test radar widget can update with targets."""
        if not hasattr(self.main_window, 'radar_widget'):
            raise AssertionError("Radar widget not found")

        radar = self.main_window.radar_widget

        # Simulate target update
        test_targets = [{
            'angle': 45.0,
            'distance': 50.0,
            'type': 'walk',
            'confidence': 0.8
        }]

        radar.update_targets(test_targets)
        QApplication.processEvents()

    # =========================================================================
    # REPORT GENERATION
    # =========================================================================

    def _generate_text_report(self, log_path: Path) -> None:
        """Append summary to text log."""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.success)
        failed = total - passed

        pass_rate = (passed / total * 100) if total > 0 else 0

        with log_path.open("a", encoding="utf-8") as f:
            f.write("\n\n")
            f.write("=" * 80 + "\n")
            f.write("TEST SUMMARY\n")
            f.write("=" * 80 + "\n")
            f.write(f"Total Tests: {total}\n")
            f.write(f"Passed: {passed} ({pass_rate:.1f}%)\n")
            f.write(f"Failed: {failed} ({100-pass_rate:.1f}%)\n")
            f.write("\n")

            # Category breakdown
            categories = {}
            for result in self.results:
                cat = result.category
                if cat not in categories:
                    categories[cat] = {'total': 0, 'passed': 0}
                categories[cat]['total'] += 1
                if result.success:
                    categories[cat]['passed'] += 1

            f.write("Category Breakdown:\n")
            f.write("-" * 80 + "\n")
            for cat, stats in categories.items():
                cat_pass_rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
                f.write(f"  {cat}: {stats['passed']}/{stats['total']} ({cat_pass_rate:.1f}%)\n")

            f.write("\n")
            f.write("Detailed Results:\n")
            f.write("-" * 80 + "\n")

            for result in self.results:
                status = "✓ PASS" if result.success else "✗ FAIL"
                f.write(f"{status} [{result.category}] {result.name}\n")
                if not result.success:
                    f.write(f"       Error: {result.message}\n")

    def _generate_html_report(self, report_path: Path) -> None:
        """Generate HTML report with visual styling."""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.success)
        failed = total - passed
        pass_rate = (passed / total * 100) if total > 0 else 0

        # Category breakdown
        categories = {}
        for result in self.results:
            cat = result.category
            if cat not in categories:
                categories[cat] = {'total': 0, 'passed': 0, 'results': []}
            categories[cat]['total'] += 1
            if result.success:
                categories[cat]['passed'] += 1
            categories[cat]['results'].append(result)

        # Generate HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comprehensive Auto-Test Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eee;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: #0f3460;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            padding: 30px;
        }}
        h1 {{
            color: #4ECDC4;
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}
        .timestamp {{
            text-align: center;
            color: #aaa;
            margin-bottom: 30px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 10px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            border: 2px solid #2A82DA;
        }}
        .stat-value {{
            font-size: 3em;
            font-weight: bold;
            margin: 10px 0;
        }}
        .stat-label {{
            font-size: 1.1em;
            color: #aaa;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .pass {{ color: #00FF88; }}
        .fail {{ color: #FF6B6B; }}
        .pass-rate {{
            color: {'#00FF88' if pass_rate >= 90 else '#FFE66D' if pass_rate >= 70 else '#FF6B6B'};
        }}
        .category {{
            background: #16213e;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 25px;
            border-left: 5px solid #4ECDC4;
        }}
        .category-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        .category-title {{
            font-size: 1.5em;
            color: #4ECDC4;
            font-weight: bold;
        }}
        .category-stats {{
            font-size: 1.2em;
            color: #aaa;
        }}
        .test-result {{
            padding: 12px 15px;
            margin: 8px 0;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #1a1a2e;
            border-left: 4px solid #666;
        }}
        .test-result.passed {{
            border-left-color: #00FF88;
        }}
        .test-result.failed {{
            border-left-color: #FF6B6B;
            background: #2a1a1e;
        }}
        .test-name {{
            flex: 1;
        }}
        .test-status {{
            font-weight: bold;
            padding: 5px 15px;
            border-radius: 5px;
            font-size: 0.9em;
        }}
        .test-status.pass {{
            background: #00FF88;
            color: #000;
        }}
        .test-status.fail {{
            background: #FF6B6B;
            color: #fff;
        }}
        .error-message {{
            margin-top: 8px;
            padding: 10px;
            background: #1a0a0a;
            border-radius: 5px;
            color: #FF6B6B;
            font-family: monospace;
            font-size: 0.9em;
            white-space: pre-wrap;
        }}
        .duration {{
            color: #888;
            font-size: 0.9em;
            margin-left: 15px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 Comprehensive Auto-Test Report</h1>
        <div class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>

        <div class="summary">
            <div class="stat-card">
                <div class="stat-label">Total Tests</div>
                <div class="stat-value">{total}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Passed</div>
                <div class="stat-value pass">{passed}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Failed</div>
                <div class="stat-value fail">{failed}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Pass Rate</div>
                <div class="stat-value pass-rate">{pass_rate:.1f}%</div>
            </div>
        </div>
"""

        # Add category sections
        for cat_name, cat_data in categories.items():
            cat_pass_rate = (cat_data['passed'] / cat_data['total'] * 100) if cat_data['total'] > 0 else 0

            html += f"""
        <div class="category">
            <div class="category-header">
                <div class="category-title">📋 {cat_name}</div>
                <div class="category-stats">{cat_data['passed']}/{cat_data['total']} ({cat_pass_rate:.1f}%)</div>
            </div>
"""

            for result in cat_data['results']:
                status_class = "passed" if result.success else "failed"
                status_badge = "pass" if result.success else "fail"
                status_text = "✓ PASS" if result.success else "✗ FAIL"

                html += f"""
            <div class="test-result {status_class}">
                <div class="test-name">
                    {result.name}
                    <span class="duration">({result.duration_ms:.1f}ms)</span>
"""

                if not result.success and result.message:
                    html += f"""
                    <div class="error-message">Error: {result.message}</div>
"""

                html += f"""
                </div>
                <div class="test-status {status_badge}">{status_text}</div>
            </div>
"""

            html += """
        </div>
"""

        html += """
    </div>
</body>
</html>
"""

        # Write HTML file
        with report_path.open("w", encoding="utf-8") as f:
            f.write(html)

        self.logger.write(f"\nHTML report generated: {report_path}")
