import subprocess
import tempfile
import logging
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class ExecutionResult:
    """
    Result of compiling and running a Java solution against a test suite.
    """
    passed: bool
    status: str
    details: str


def _find_main_class(source_code: str) -> str:
    """
    Use a regular expression to find the name of the class that contains
    the main method.
    """
    # Look for a pattern like: class ClassName { ... public static void main ... }
    # re.DOTALL makes '.' also match newlines.
    pattern = re.compile(
        r"class\s+([A-Za-z0-9_]+)\s*\{.*public\s+static\s+void\s+main", re.DOTALL
    )
    match = pattern.search(source_code)
    if match:
        # Return the first captured group (the class name)
        return match.group(1)
    return None


def evaluate_solution(
    source_code: str, tests: List[Dict[str, Any]], timeout_seconds: int = 5
) -> ExecutionResult:
    """
    Compile and run a Java solution, dynamically discovering the main class.
    """
    # Discover the name of the main class.
    main_class_name = _find_main_class(source_code)
    if not main_class_name:
        return ExecutionResult(
            passed=False,
            status="Structure Error",
            details="Could not find a class with method 'public static void main'.",
        )

    with tempfile.TemporaryDirectory() as tmpdir:
        dir_path = Path(tmpdir)
        # Save the .java file with the discovered class name.
        java_file = dir_path / f"{main_class_name}.java"

        with open(java_file, "w", encoding="utf-8") as f:
            f.write(source_code)

        # Step 1: Compilation
        try:
            compile_result = subprocess.run(
                ["javac", str(java_file)],
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
            )
            if compile_result.returncode != 0:
                return ExecutionResult(
                    passed=False,
                    status="Compilation Error",
                    details=compile_result.stderr,
                )
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                passed=False,
                status="Compilation Timeout",
                details=f"Compilation exceeded {timeout_seconds} seconds.",
            )

        # Step 2: Test Execution
        for i, test in enumerate(tests):
            test_input = test.get("input", "")
            expected_output = test.get("output", "")

            try:
                # Execute the .class using the discovered class name.
                run_result = subprocess.run(
                    ["java", main_class_name],
                    capture_output=True,
                    text=True,
                    input=test_input,
                    cwd=dir_path,
                    timeout=timeout_seconds,
                )

                if run_result.returncode != 0:
                    return ExecutionResult(
                        passed=False,
                        status=f"Runtime Error on test {i + 1}",
                        details=run_result.stderr,
                    )

                if run_result.stdout.strip() != expected_output.strip():
                    return ExecutionResult(
                        passed=False,
                        status=f"Wrong Answer on test {i + 1}",
                        details=(
                            f"Expected: '{expected_output.strip()}'\n"
                            f"Received: '{run_result.stdout.strip()}'"
                        ),
                    )

            except subprocess.TimeoutExpired:
                return ExecutionResult(
                    passed=False,
                    status=f"Timeout on test {i + 1}",
                    details=f"Execution exceeded {timeout_seconds} seconds.",
                )

    return ExecutionResult(
        passed=True,
        status=f"Compiled and passed {len(tests)} tests",
        details="",
    )




