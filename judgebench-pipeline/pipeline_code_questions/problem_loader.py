import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class ProblemData:
    """
    Structured representation of a coding problem.
    """
    problem_id: str
    statement: str
    reference_solution: str
    tests: List[Dict[str, Any]]


def load_problem_from_directory(directory_path: Path) -> ProblemData:
    """
    Load all information for a coding problem from a directory.

    The function expects:
    1. A .yaml file with the same name as the directory.
    2. Exactly one .java file containing the reference solution.

    Args:
        directory_path: Path object for the problem folder (e.g., .../teorema_mestre).

    Returns:
        A ProblemData object containing all problem data.

    Raises:
        FileNotFoundError: If the .yaml or .java files are not found.
        Exception: If more than one .java file exists in the directory.
    """
    problem_id = directory_path.name

    # The YAML file name must match the folder name.
    yaml_file = directory_path / f"{problem_id}.yaml"
    if not yaml_file.exists():
        raise FileNotFoundError(f"Required YAML file not found: {yaml_file}")

    # Search for any .java file in the directory.
    java_files = list(directory_path.glob("*.java"))
    if not java_files:
        raise FileNotFoundError(f"No .java solution file found in: {directory_path}")
    if len(java_files) > 1:
        raise Exception(f"Multiple .java files found in {directory_path}. Only one is allowed.")

    java_file = java_files[0]

    # Load YAML file content.
    with open(yaml_file, "r", encoding="utf-8") as f:
        problem_data_raw = yaml.safe_load(f)

    # Load reference solution code.
    with open(java_file, "r", encoding="utf-8") as f:
        solution_code = f.read()

    # Extract information into our data structure.
    statement = problem_data_raw.get("text", "")
    tests = problem_data_raw.get("tests", [])

    return ProblemData(
        problem_id=problem_id,
        statement=statement,
        reference_solution=solution_code,
        tests=tests,
    )






