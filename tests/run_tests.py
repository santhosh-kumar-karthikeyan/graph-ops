#!/usr/bin/env python3
"""
Comprehensive test runner for the graph-ops project.
Runs all tests and provides detailed reporting.
"""

import unittest
import sys
import time
import os
from io import StringIO


def discover_and_run_tests():
    """Discover and run all tests in the tests directory."""
    
    # Add the project root to the path
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)
    
    print("=" * 70)
    print("GRAPH-OPS PROJECT TEST SUITE")
    print("=" * 70)
    print(f"Python version: {sys.version}")
    print(f"Project root: {project_root}")
    print()
    
    # Discover tests
    test_dir = os.path.dirname(os.path.abspath(__file__))
    loader = unittest.TestLoader()
    suite = loader.discover(test_dir, pattern='test_*.py')
    
    # Count tests
    test_count = suite.countTestCases()
    print(f"Discovered {test_count} tests")
    print()
    
    # Create a custom test result to capture detailed information
    class DetailedTestResult(unittest.TextTestResult):
        def __init__(self, stream, descriptions, verbosity):
            super().__init__(stream, descriptions, verbosity)
            self.test_timings = {}
            self.start_time = None
        
        def startTest(self, test):
            super().startTest(test)
            self.start_time = time.time()
        
        def stopTest(self, test):
            super().stopTest(test)
            if self.start_time:
                duration = time.time() - self.start_time
                self.test_timings[str(test)] = duration
        
        def getDescription(self, test):
            return f"{test.__class__.__name__}.{test._testMethodName}"
    
    # Run tests with detailed output
    stream = StringIO()
    runner = unittest.TextTestRunner(
        stream=stream,
        verbosity=2,
        resultclass=DetailedTestResult
    )
    
    start_time = time.time()
    result = runner.run(suite)
    total_time = time.time() - start_time
    
    # Print results
    output = stream.getvalue()
    print(output)
    
    # Summary report
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    print(f"Total time: {total_time:.2f} seconds")
    print()
    
    if result.failures:
        print("FAILURES:")
        print("-" * 40)
        for test, traceback in result.failures:
            print(f"FAIL: {result.getDescription(test)}")
            print(traceback)
            print()
    
    if result.errors:
        print("ERRORS:")
        print("-" * 40)
        for test, traceback in result.errors:
            print(f"ERROR: {result.getDescription(test)}")
            print(traceback)
            print()
    
    # Performance report
    if hasattr(result, 'test_timings') and getattr(result, 'test_timings', None):
        print("PERFORMANCE REPORT:")
        print("-" * 40)
        timings = getattr(result, 'test_timings', {})
        sorted_timings = sorted(timings.items(), key=lambda x: x[1], reverse=True)
        for test_name, duration in sorted_timings[:10]:  # Top 10 slowest
            print(f"{duration:.3f}s - {test_name}")
        print()
    
    # Coverage report (if possible)
    try:
        import coverage  # type: ignore
        print("COVERAGE ANALYSIS:")
        print("-" * 40)
        print("Coverage package available but not configured.")
        print("To enable coverage: pip install coverage")
        print("Run: coverage run run_tests.py && coverage report")
        print()
    except ImportError:
        pass
    
    # Final status
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED!")
        return_code = 0
    else:
        print("❌ SOME TESTS FAILED!")
        return_code = 1
    
    print("=" * 70)
    return return_code


def run_specific_test_category(category):
    """Run tests from a specific category."""
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)
    
    test_files = {
        'graph': 'test_graph.py',
        'shell': 'test_shell.py',
        'ucs': 'test_ucs.py',
        'performance': 'test_performance.py'
    }
    
    if category not in test_files:
        print(f"Unknown category: {category}")
        print(f"Available categories: {', '.join(test_files.keys())}")
        return 1
    
    test_dir = os.path.dirname(os.path.abspath(__file__))
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(test_files[category].replace('.py', ''))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


def main():
    """Main entry point for the test runner."""
    if len(sys.argv) > 1:
        category = sys.argv[1]
        return run_specific_test_category(category)
    else:
        return discover_and_run_tests()


if __name__ == '__main__':
    sys.exit(main())
