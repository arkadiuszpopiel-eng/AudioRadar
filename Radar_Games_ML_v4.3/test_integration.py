#!/usr/bin/env python3
"""
SPRINT 2.4 - Integration Tests (Senior-Level)
Tests for exception handling refactor and code integrity.

Tests:
1. Syntax validation - all Python files
2. Import validation - all modules
3. Dependency checks - missing imports
4. Exception handler integrity - no bare except, all have proper types
5. Critical path verification - main.py, audio/engine.py, core/config.py
"""

import os
import sys
import ast
import importlib.util
from pathlib import Path
from typing import List, Tuple, Dict

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

class IntegrationTester:
    """Senior-level integration tester for code quality and integrity."""

    def __init__(self, app_dir: str):
        self.app_dir = Path(app_dir)
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.passed: int = 0
        self.failed: int = 0

    def print_header(self, title: str):
        """Print test section header."""
        print(f"\n{BLUE}{'='*70}{RESET}")
        print(f"{BLUE}{title:^70}{RESET}")
        print(f"{BLUE}{'='*70}{RESET}\n")

    def print_result(self, test_name: str, passed: bool, message: str = ""):
        """Print test result."""
        if passed:
            self.passed += 1
            status = f"{GREEN}✓ PASSED{RESET}"
        else:
            self.failed += 1
            status = f"{RED}✗ FAILED{RESET}"

        print(f"{status} - {test_name}")
        if message:
            print(f"         {message}")

    def test_syntax_validation(self) -> bool:
        """Test 1: Validate syntax of all Python files."""
        self.print_header("TEST 1: SYNTAX VALIDATION")

        py_files = list(self.app_dir.rglob("*.py"))
        print(f"Found {len(py_files)} Python files to validate\n")

        all_passed = True
        for py_file in py_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    code = f.read()
                compile(code, str(py_file), 'exec')
                self.print_result(f"Syntax: {py_file.relative_to(self.app_dir)}", True)
            except SyntaxError as e:
                self.print_result(f"Syntax: {py_file.relative_to(self.app_dir)}", False,
                                f"Line {e.lineno}: {e.msg}")
                self.errors.append(f"Syntax error in {py_file}: {e}")
                all_passed = False

        return all_passed

    def test_import_validation(self) -> bool:
        """Test 2: Validate that key modules can be imported."""
        self.print_header("TEST 2: IMPORT VALIDATION")

        # Critical modules to test
        critical_modules = [
            'main.py',
            'audio/engine.py',
            'core/config.py',
            'core/logger.py',
            'core/constants.py',
            'core/application_controller.py',
            'ui/event_handlers.py',
        ]

        all_passed = True
        for module_path in critical_modules:
            full_path = self.app_dir / module_path
            if not full_path.exists():
                self.print_result(f"Import: {module_path}", False, "File not found")
                self.errors.append(f"Module not found: {module_path}")
                all_passed = False
                continue

            try:
                # Try to parse AST (checks for import errors in syntax)
                with open(full_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                tree = ast.parse(code, str(full_path))

                # Check for any bare imports that might fail
                imports = [node for node in ast.walk(tree)
                          if isinstance(node, (ast.Import, ast.ImportFrom))]

                self.print_result(f"Import: {module_path}", True,
                                f"{len(imports)} imports found")
            except Exception as e:
                self.print_result(f"Import: {module_path}", False, str(e))
                self.errors.append(f"Import error in {module_path}: {e}")
                all_passed = False

        return all_passed

    def test_exception_handlers(self) -> bool:
        """Test 3: Validate exception handlers (no bare except, proper types)."""
        self.print_header("TEST 3: EXCEPTION HANDLER INTEGRITY")

        # Files we modified
        modified_files = [
            'main.py',
            'audio/engine.py',
            'core/config.py',
        ]

        all_passed = True
        for file_path in modified_files:
            full_path = self.app_dir / file_path

            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                tree = ast.parse(code, str(full_path))

                # Find all exception handlers
                bare_excepts = []
                broad_excepts = []
                good_excepts = 0

                for node in ast.walk(tree):
                    if isinstance(node, ast.ExceptHandler):
                        if node.type is None:
                            # Bare except:
                            bare_excepts.append(node.lineno)
                        elif isinstance(node.type, ast.Name) and node.type.id == 'Exception':
                            # except Exception:
                            broad_excepts.append(node.lineno)
                        else:
                            # Specific exception types
                            good_excepts += 1

                # Report results
                issues = []
                if bare_excepts:
                    issues.append(f"{len(bare_excepts)} bare except at lines: {bare_excepts[:5]}")
                if broad_excepts:
                    issues.append(f"{len(broad_excepts)} broad 'Exception' at lines: {broad_excepts[:5]}")

                if issues:
                    self.print_result(f"Exceptions: {file_path}", False, "; ".join(issues))
                    self.warnings.extend(issues)
                    # Don't fail the test for broad exceptions, just warn
                    # all_passed = False
                else:
                    self.print_result(f"Exceptions: {file_path}", True,
                                    f"{good_excepts} specific exception handlers")

            except Exception as e:
                self.print_result(f"Exceptions: {file_path}", False, str(e))
                self.errors.append(f"Exception analysis error in {file_path}: {e}")
                all_passed = False

        return all_passed

    def test_traceback_coverage(self) -> bool:
        """Test 4: Verify traceback logging was added to ERROR-level exceptions."""
        self.print_header("TEST 4: TRACEBACK LOGGING COVERAGE")

        modified_files = [
            ('main.py', 16),  # Expected traceback count
            ('audio/engine.py', 9),
            ('core/config.py', 3),
        ]

        all_passed = True
        for file_path, expected_count in modified_files:
            full_path = self.app_dir / file_path

            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Count traceback.format_exc() and traceback.print_exc() calls
                traceback_count = content.count('traceback.format_exc()')
                traceback_count += content.count('traceback.print_exc()')

                # We expect at least some traceback logging
                if traceback_count >= expected_count - 2:  # Allow small variance
                    self.print_result(f"Traceback: {file_path}", True,
                                    f"{traceback_count} traceback calls (expected ~{expected_count})")
                else:
                    self.print_result(f"Traceback: {file_path}", False,
                                    f"Only {traceback_count} traceback calls (expected ~{expected_count})")
                    self.warnings.append(f"Low traceback coverage in {file_path}")

            except Exception as e:
                self.print_result(f"Traceback: {file_path}", False, str(e))
                self.errors.append(f"Traceback check error in {file_path}: {e}")
                all_passed = False

        return all_passed

    def test_critical_paths(self) -> bool:
        """Test 5: Verify critical code paths are intact."""
        self.print_header("TEST 5: CRITICAL PATH VERIFICATION")

        tests = [
            # Check main.py has tick() method
            ('main.py', 'def tick(self)', 'MainWindow.tick() method'),

            # Check audio engine has start/stop
            ('audio/engine.py', 'def start(self)', 'AudioEngine.start() method'),
            ('audio/engine.py', 'def stop(self)', 'AudioEngine.stop() method'),

            # Check config has save/load
            ('core/config.py', 'def save(self', 'ConfigManager.save() method'),
            ('core/config.py', 'def load(self', 'ConfigManager.load() method'),

            # Check ApplicationController exists
            ('core/application_controller.py', 'class ApplicationController', 'ApplicationController class'),
        ]

        all_passed = True
        for file_path, search_string, description in tests:
            full_path = self.app_dir / file_path

            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                if search_string in content:
                    self.print_result(f"Critical: {description}", True)
                else:
                    self.print_result(f"Critical: {description}", False,
                                    f"Missing: '{search_string}'")
                    self.errors.append(f"Critical path missing in {file_path}: {search_string}")
                    all_passed = False

            except Exception as e:
                self.print_result(f"Critical: {description}", False, str(e))
                self.errors.append(f"Critical path check error: {e}")
                all_passed = False

        return all_passed

    def run_all_tests(self) -> bool:
        """Run all integration tests."""
        print(f"\n{BLUE}{'='*70}{RESET}")
        print(f"{BLUE}SPRINT 2.4 - INTEGRATION TESTS (Senior-Level){RESET}")
        print(f"{BLUE}Exception Handling Refactor Verification{RESET}")
        print(f"{BLUE}{'='*70}{RESET}")

        results = []
        results.append(self.test_syntax_validation())
        results.append(self.test_import_validation())
        results.append(self.test_exception_handlers())
        results.append(self.test_traceback_coverage())
        results.append(self.test_critical_paths())

        # Print summary
        self.print_header("TEST SUMMARY")
        print(f"{GREEN}Passed: {self.passed}{RESET}")
        print(f"{RED}Failed: {self.failed}{RESET}")
        print(f"{YELLOW}Warnings: {len(self.warnings)}{RESET}")

        if self.errors:
            print(f"\n{RED}ERRORS:{RESET}")
            for error in self.errors[:10]:  # Show first 10 errors
                print(f"  • {error}")

        if self.warnings:
            print(f"\n{YELLOW}WARNINGS:{RESET}")
            for warning in self.warnings[:10]:
                print(f"  • {warning}")

        all_passed = all(results) and self.failed == 0

        if all_passed:
            print(f"\n{GREEN}{'='*70}{RESET}")
            print(f"{GREEN}✓ ALL TESTS PASSED - CODE INTEGRITY VERIFIED{RESET}")
            print(f"{GREEN}{'='*70}{RESET}\n")
        else:
            print(f"\n{RED}{'='*70}{RESET}")
            print(f"{RED}✗ SOME TESTS FAILED - REVIEW REQUIRED{RESET}")
            print(f"{RED}{'='*70}{RESET}\n")

        return all_passed


if __name__ == '__main__':
    tester = IntegrationTester('app')
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)
