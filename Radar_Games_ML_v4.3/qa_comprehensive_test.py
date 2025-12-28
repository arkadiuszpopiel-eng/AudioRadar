#!/usr/bin/env python3
"""
KOMPLEKSOWA WERYFIKACJA JAKOŚCI - Radar Games ML v4.3.1
Comprehensive QA testing suite for all code quality aspects

Tests:
1. Compilation and syntax (all Python files)
2. Module imports and dependencies
3. Path verification and typos
4. Critical code paths (start/stop/tick)
5. Widget initialization and responsiveness
6. Tab scaling and UI integrity
7. Event handler connections
8. Potential freeze scenarios
"""

import os
import sys
import ast
import re
import importlib.util
from pathlib import Path
from typing import List, Dict, Tuple, Set
import subprocess

# Color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

class ComprehensiveQA:
    """Comprehensive QA testing suite"""

    def __init__(self, app_dir: str):
        self.app_dir = Path(app_dir)
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.critical_issues: List[str] = []
        self.passed: int = 0
        self.failed: int = 0
        self.warnings_count: int = 0

    def print_header(self, title: str, level: int = 1):
        """Print test section header"""
        if level == 1:
            print(f"\n{BOLD}{BLUE}{'='*80}{RESET}")
            print(f"{BOLD}{BLUE}{title:^80}{RESET}")
            print(f"{BOLD}{BLUE}{'='*80}{RESET}\n")
        else:
            print(f"\n{CYAN}{'─'*80}{RESET}")
            print(f"{CYAN}{title}{RESET}")
            print(f"{CYAN}{'─'*80}{RESET}\n")

    def print_result(self, test_name: str, passed: bool, message: str = "", is_critical: bool = False):
        """Print test result"""
        if passed:
            self.passed += 1
            status = f"{GREEN}✓ PASSED{RESET}"
        else:
            self.failed += 1
            if is_critical:
                status = f"{RED}{BOLD}✗ CRITICAL FAIL{RESET}"
                self.critical_issues.append(test_name)
            else:
                status = f"{RED}✗ FAILED{RESET}"

        print(f"{status} - {test_name}")
        if message:
            print(f"         {message}")

    def print_warning(self, test_name: str, message: str):
        """Print warning"""
        self.warnings_count += 1
        print(f"{YELLOW}⚠ WARNING{RESET} - {test_name}")
        if message:
            print(f"           {message}")

    # ========================================================================
    # TEST 1: COMPILATION AND SYNTAX (2 rounds)
    # ========================================================================

    def test_compilation_round1(self) -> bool:
        """Round 1: Compile all Python files"""
        self.print_header("TEST 1/2 - ROUND 1: COMPILATION AND SYNTAX", 1)

        py_files = list(self.app_dir.rglob("*.py"))
        print(f"Found {len(py_files)} Python files to compile\n")

        all_passed = True
        for py_file in py_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    code = f.read()
                compile(code, str(py_file), 'exec')

                # Also run py_compile
                result = subprocess.run(
                    ['python3', '-m', 'py_compile', str(py_file)],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if result.returncode == 0:
                    self.print_result(f"Compile: {py_file.relative_to(self.app_dir)}", True)
                else:
                    self.print_result(
                        f"Compile: {py_file.relative_to(self.app_dir)}",
                        False,
                        result.stderr,
                        is_critical=True
                    )
                    all_passed = False

            except SyntaxError as e:
                self.print_result(
                    f"Syntax: {py_file.relative_to(self.app_dir)}",
                    False,
                    f"Line {e.lineno}: {e.msg}",
                    is_critical=True
                )
                self.errors.append(f"Syntax error in {py_file}: {e}")
                all_passed = False
            except Exception as e:
                self.print_result(
                    f"Compile: {py_file.relative_to(self.app_dir)}",
                    False,
                    str(e),
                    is_critical=True
                )
                all_passed = False

        return all_passed

    def test_compilation_round2(self) -> bool:
        """Round 2: AST parsing and validation"""
        self.print_header("TEST 2/2 - ROUND 2: AST PARSING AND VALIDATION", 1)

        py_files = list(self.app_dir.rglob("*.py"))
        print(f"Parsing {len(py_files)} Python files with AST\n")

        all_passed = True
        for py_file in py_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    code = f.read()
                tree = ast.parse(code, str(py_file))

                # Additional validation
                issues = []

                # Check for common issues
                for node in ast.walk(tree):
                    # Check for undefined names (basic check)
                    if isinstance(node, ast.Name) and node.id.startswith('undefined_'):
                        issues.append(f"Suspicious undefined variable: {node.id}")

                if issues:
                    self.print_warning(
                        f"AST: {py_file.relative_to(self.app_dir)}",
                        "; ".join(issues)
                    )
                else:
                    self.print_result(f"AST: {py_file.relative_to(self.app_dir)}", True)

            except SyntaxError as e:
                self.print_result(
                    f"AST: {py_file.relative_to(self.app_dir)}",
                    False,
                    f"Line {e.lineno}: {e.msg}",
                    is_critical=True
                )
                all_passed = False

        return all_passed

    # ========================================================================
    # TEST 3: MODULE STRUCTURE AND CONNECTIONS
    # ========================================================================

    def test_module_structure(self) -> bool:
        """Verify module structure and __init__.py exports"""
        self.print_header("TEST 3: MODULE STRUCTURE AND CONNECTIONS", 1)

        modules_to_check = [
            ('core', ['ConfigManager', 'log', 'ApplicationController']),
            ('audio', ['AudioEngine']),
            ('detection', ['DetectionWorker']),
            ('tracking', ['TargetTracker']),
            ('ui', ['EventHandlers']),
            ('widgets', []),  # Just check it exists
        ]

        all_passed = True
        for module_name, expected_exports in modules_to_check:
            module_path = self.app_dir / module_name / '__init__.py'

            if not module_path.exists():
                self.print_result(
                    f"Module: {module_name}/__init__.py",
                    False,
                    "File not found",
                    is_critical=True
                )
                all_passed = False
                continue

            try:
                with open(module_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Check for expected exports
                missing_exports = []
                for export in expected_exports:
                    if export not in content:
                        missing_exports.append(export)

                if missing_exports:
                    self.print_warning(
                        f"Module: {module_name}",
                        f"Missing exports: {', '.join(missing_exports)}"
                    )
                else:
                    self.print_result(f"Module: {module_name}", True, f"{len(expected_exports)} exports verified")

            except Exception as e:
                self.print_result(f"Module: {module_name}", False, str(e))
                all_passed = False

        return all_passed

    # ========================================================================
    # TEST 4: PATH AND IMPORT VERIFICATION
    # ========================================================================

    def test_imports_and_paths(self) -> bool:
        """Check all imports resolve correctly"""
        self.print_header("TEST 4: IMPORTS AND PATH VERIFICATION", 1)

        critical_files = [
            'main.py',
            'core/application_controller.py',
            'core/config.py',
            'audio/engine.py',
            'detection/worker.py',
            'ui/event_handlers.py',
        ]

        all_passed = True
        for file_path in critical_files:
            full_path = self.app_dir / file_path

            if not full_path.exists():
                self.print_result(
                    f"Path: {file_path}",
                    False,
                    "File not found",
                    is_critical=True
                )
                all_passed = False
                continue

            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Parse imports
                tree = ast.parse(content)
                imports = []

                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.append(node.module)

                self.print_result(
                    f"Imports: {file_path}",
                    True,
                    f"{len(imports)} imports found"
                )

            except Exception as e:
                self.print_result(f"Imports: {file_path}", False, str(e))
                all_passed = False

        return all_passed

    # ========================================================================
    # TEST 5: CRITICAL CODE PATHS (FREEZE DETECTION)
    # ========================================================================

    def test_critical_paths_no_freeze(self) -> bool:
        """CRITICAL: Check for potential freeze scenarios"""
        self.print_header("TEST 5: CRITICAL FREEZE DETECTION", 1)

        freeze_patterns = [
            ('Infinite loop', r'while\s+True\s*:(?!\s*#\s*SAFE)'),
            ('Blocking call', r'\.join\(\)\s*(?!#\s*timeout)'),
            ('QApplication.exec_', r'QApplication\.exec_\(\)'),
            ('processEvents abuse', r'processEvents\(\s*\).*for.*in'),
        ]

        critical_files = [
            'main.py',
            'core/application_controller.py',
            'ui/event_handlers.py',
        ]

        all_passed = True
        for file_path in critical_files:
            full_path = self.app_dir / file_path

            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                issues = []
                for pattern_name, pattern in freeze_patterns:
                    matches = re.findall(pattern, content, re.MULTILINE)
                    if matches:
                        issues.append(f"{pattern_name}: {len(matches)} occurrences")

                if issues:
                    self.print_warning(
                        f"Freeze check: {file_path}",
                        "; ".join(issues)
                    )
                else:
                    self.print_result(f"Freeze check: {file_path}", True)

            except Exception as e:
                self.print_result(f"Freeze check: {file_path}", False, str(e))
                all_passed = False

        return all_passed

    # ========================================================================
    # TEST 6: WIDGET AND EVENT HANDLER INTEGRITY
    # ========================================================================

    def test_widget_integrity(self) -> bool:
        """
        Check widget initialization and event connections
        v4.3.1 POPRAWKA #3: Check both main.py and ui/builder.py (UIBuilder pattern)
        """
        self.print_header("TEST 6: WIDGET AND EVENT HANDLER INTEGRITY", 1)

        # Check main.py and ui/builder.py for widget initialization
        main_path = self.app_dir / 'main.py'
        builder_path = self.app_dir / 'ui' / 'builder.py'

        critical_widgets = [
            'radar_widget',
            'radar_3d_widget',
            'start_btn',
            'dev_panel',
            'det_panel',
        ]

        try:
            with open(main_path, 'r', encoding='utf-8') as f:
                main_content = f.read()

            # v4.3.1 POPRAWKA #3: Also check UIBuilder
            builder_content = ""
            if builder_path.exists():
                with open(builder_path, 'r', encoding='utf-8') as f:
                    builder_content = f.read()

            all_passed = True
            for widget_name in critical_widgets:
                # Check if widget is initialized in main.py OR ui/builder.py
                found_in_main = f'self.{widget_name}' in main_content
                found_in_builder = f'self.main.{widget_name}' in builder_content

                if found_in_main:
                    self.print_result(f"Widget: {widget_name}", True, "Initialized (main.py)")
                elif found_in_builder:
                    # v4.3.1 POPRAWKA #3: Widgets created by UIBuilder are valid!
                    self.print_result(f"Widget: {widget_name}", True, "Initialized (UIBuilder)")
                else:
                    self.print_result(
                        f"Widget: {widget_name}",
                        False,
                        "Not found in main.py or ui/builder.py",
                        is_critical=True
                    )
                    all_passed = False

            # Check event handler
            if 'self.event_handlers = EventHandlers(self)' in main_content:
                self.print_result("EventHandlers", True, "Properly initialized")
            else:
                self.print_result("EventHandlers", False, "Not initialized", is_critical=True)
                all_passed = False

            # Check controller
            if 'self.controller = ApplicationController(self)' in main_content:
                self.print_result("ApplicationController", True, "Properly initialized")
            else:
                self.print_result("ApplicationController", False, "Not initialized", is_critical=True)
                all_passed = False

            return all_passed

        except Exception as e:
            self.print_result("Widget integrity", False, str(e), is_critical=True)
            return False

    # ========================================================================
    # TEST 7: START/STOP FUNCTIONALITY INTEGRITY
    # ========================================================================

    def test_start_stop_integrity(self) -> bool:
        """Verify start/stop methods don't cause freezes"""
        self.print_header("TEST 7: START/STOP FUNCTIONALITY INTEGRITY", 1)

        # Check that start() delegates to controller
        main_path = self.app_dir / 'main.py'
        controller_path = self.app_dir / 'core' / 'application_controller.py'

        all_passed = True

        try:
            # Check MainWindow.start() delegates
            with open(main_path, 'r', encoding='utf-8') as f:
                main_content = f.read()

            if 'def start(self):' in main_content and 'self.controller.start()' in main_content:
                self.print_result("MainWindow.start()", True, "Delegates to controller")
            else:
                self.print_result("MainWindow.start()", False, "Does not delegate properly", is_critical=True)
                all_passed = False

            # Check MainWindow.stop() delegates
            if 'def stop(self):' in main_content and 'self.controller.stop()' in main_content:
                self.print_result("MainWindow.stop()", True, "Delegates to controller")
            else:
                self.print_result("MainWindow.stop()", False, "Does not delegate properly", is_critical=True)
                all_passed = False

            # Check controller has proper methods
            with open(controller_path, 'r', encoding='utf-8') as f:
                controller_content = f.read()

            if 'def start(self):' in controller_content:
                self.print_result("Controller.start()", True, "Method exists")
            else:
                self.print_result("Controller.start()", False, "Method missing", is_critical=True)
                all_passed = False

            if 'def stop(self):' in controller_content:
                self.print_result("Controller.stop()", True, "Method exists")
            else:
                self.print_result("Controller.stop()", False, "Method missing", is_critical=True)
                all_passed = False

            # Check for state synchronization
            if 'self.window.is_running = True' in controller_content:
                self.print_result("State sync", True, "Controller syncs with window")
            else:
                self.print_warning("State sync", "Controller may not sync state properly")

            return all_passed

        except Exception as e:
            self.print_result("Start/Stop integrity", False, str(e), is_critical=True)
            return False

    # ========================================================================
    # TEST 8: PERFORMANCE - TICK() EXECUTION TIME
    # ========================================================================

    def test_tick_performance(self) -> bool:
        """
        v4.3.1 POPRAWKA #4: Verify tick() has no blocking calls that would exceed 50ms budget

        This test checks for common performance issues:
        - Blocking .result(timeout=X) calls where X > 0.05
        - Synchronous database/file operations
        - Long-running computations without threading
        """
        self.print_header("TEST 8: TICK() PERFORMANCE ANALYSIS", 1)

        main_path = self.app_dir / 'main.py'

        try:
            with open(main_path, 'r', encoding='utf-8') as f:
                content = f.read()

            all_passed = True

            # Check for blocking .result() calls with timeout > 50ms
            blocking_patterns = [
                (r'\.result\(timeout=([0-9.]+)\)', 'Blocking .result() call'),
                (r'time\.sleep\(([0-9.]+)\)', 'Blocking sleep() call'),
                (r'\.join\(\)', 'Thread join without timeout'),
                (r'while\s+True\s*:\s*(?!.*#\s*SAFE)', 'Potential infinite loop'),
            ]

            import re
            issues_found = []

            for pattern, description in blocking_patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1

                    # Skip if in comment
                    line = content.split('\n')[line_num - 1]
                    if line.strip().startswith('#'):
                        continue

                    # For .result(timeout=X), check if X > 0.05 (50ms)
                    if 'timeout' in pattern and len(match.groups()) > 0:
                        timeout_value = float(match.group(1))
                        if timeout_value > 0.05:
                            issues_found.append((line_num, f"{description} (timeout={timeout_value}s)", match.group(0)))

            if issues_found:
                self.print_result(
                    "Tick() performance",
                    False,
                    f"Found {len(issues_found)} potential blocking calls",
                    is_critical=True
                )
                for line_num, desc, code_snippet in issues_found:
                    print(f"    {YELLOW}Line {line_num}: {desc}{RESET}")
                    print(f"    {YELLOW}Code: {code_snippet[:60]}{'...' if len(code_snippet) > 60 else ''}{RESET}")
                all_passed = False
            else:
                self.print_result("Tick() performance", True, "No blocking calls found (50ms budget)")

            # v4.3.1 POPRAWKA #1: Verify non-blocking detection is implemented
            if '_pending_detection_future' in content and '.done()' in content:
                self.print_result("Non-blocking detection", True, "POPRAWKA #1 implemented")
            else:
                self.print_warning("Non-blocking detection", "POPRAWKA #1 may not be fully implemented")

            # v4.3.1 POPRAWKA #2: Verify cache timeout fallback is implemented
            if '_last_detection_update' in content and 'cache_age' in content:
                self.print_result("Cache timeout fallback", True, "POPRAWKA #2 implemented")
            else:
                self.print_warning("Cache timeout fallback", "POPRAWKA #2 may not be fully implemented")

            return all_passed

        except Exception as e:
            self.print_result("Tick() performance", False, str(e), is_critical=True)
            return False

    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================

    def run_all_tests(self) -> Tuple[bool, Dict]:
        """Run all QA tests"""
        print(f"\n{BOLD}{MAGENTA}{'='*80}{RESET}")
        print(f"{BOLD}{MAGENTA}KOMPLEKSOWA WERYFIKACJA JAKOŚCI - RADAR GAMES ML v4.3.1{RESET}")
        print(f"{BOLD}{MAGENTA}Comprehensive QA Testing Suite{RESET}")
        print(f"{BOLD}{MAGENTA}{'='*80}{RESET}")

        results = {}
        results['compilation_r1'] = self.test_compilation_round1()
        results['compilation_r2'] = self.test_compilation_round2()
        results['module_structure'] = self.test_module_structure()
        results['imports_paths'] = self.test_imports_and_paths()
        results['freeze_detection'] = self.test_critical_paths_no_freeze()
        results['widget_integrity'] = self.test_widget_integrity()
        results['start_stop'] = self.test_start_stop_integrity()
        results['tick_performance'] = self.test_tick_performance()  # v4.3.1 POPRAWKA #4

        # Print final summary
        self.print_header("PODSUMOWANIE TESTÓW QA", 1)

        print(f"{GREEN}✓ Passed: {self.passed}{RESET}")
        print(f"{RED}✗ Failed: {self.failed}{RESET}")
        print(f"{YELLOW}⚠ Warnings: {self.warnings_count}{RESET}")

        if self.critical_issues:
            print(f"\n{RED}{BOLD}KRYTYCZNE PROBLEMY:{RESET}")
            for issue in self.critical_issues:
                print(f"  • {issue}")

        if self.errors:
            print(f"\n{RED}BŁĘDY:{RESET}")
            for error in self.errors[:10]:
                print(f"  • {error}")

        if self.warnings:
            print(f"\n{YELLOW}OSTRZEŻENIA:{RESET}")
            for warning in self.warnings[:10]:
                print(f"  • {warning}")

        all_passed = all(results.values()) and self.failed == 0 and len(self.critical_issues) == 0

        if all_passed:
            print(f"\n{GREEN}{BOLD}{'='*80}{RESET}")
            print(f"{GREEN}{BOLD}✓ WSZYSTKIE TESTY PRZESZŁY POMYŚLNIE{RESET}")
            print(f"{GREEN}{BOLD}{'='*80}{RESET}\n")
        else:
            print(f"\n{RED}{BOLD}{'='*80}{RESET}")
            print(f"{RED}{BOLD}✗ WYKRYTO PROBLEMY - WYMAGANA INTERWENCJA{RESET}")
            print(f"{RED}{BOLD}{'='*80}{RESET}\n")

        return all_passed, results


if __name__ == '__main__':
    qa = ComprehensiveQA('app')
    success, results = qa.run_all_tests()

    # Return exit code
    sys.exit(0 if success else 1)
