import argparse
import logging
from pathlib import Path
import json

# Imports from our pipeline modules
from problem_loader import load_problem_from_directory
from pair_generator import create_code_pairs

def append_to_jsonl(file_path: Path, new_data: list):
    """
    Appends a list of dictionaries to the end of a .jsonl file.
    Opens the file in 'a' (append) mode to ensure persistence.
    """
    with open(file_path, 'a', encoding='utf-8') as f:
        for item in new_data:
            json_line = json.dumps(item, ensure_ascii=False)
            f.write(json_line + '\n')

def load_processed_ids(file_path: Path) -> set:
    """
    Reads an existing .jsonl file and returns a set of problem IDs
    that have already been processed to avoid duplicate work.
    """
    processed_ids = set()
    if not file_path.exists():
        return processed_ids
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                if "problem_id" in data:
                    processed_ids.add(data["problem_id"])
            except json.JSONDecodeError:
                logging.warning(f"Malformed line found and ignored in {file_path}: {line.strip()}")
    return processed_ids

def process_problem_directory(
    data_path: Path, 
    output_path: Path,
    num_mutants: int,
    max_pairs: int
):
    """
    Processes a directory containing problem folders, saving progress
    incrementally and skipping already processed problems.
    """
    logging.info("--- STARTING PAIR GENERATION PIPELINE ---")
    
    # Load IDs of problems that are already in the output file
    processed_ids = load_processed_ids(output_path)
    if processed_ids:
        logging.info(f"Found {len(processed_ids)} problems already processed in the output file. They will be skipped.")

    problem_directories = [d for d in data_path.iterdir() if d.is_dir()]
    if not problem_directories:
        logging.warning(f"No problem directory found in '{data_path}'.")
        return

    total_problems = len(problem_directories)
    new_pairs_generated = 0
    
    for i, problem_dir in enumerate(problem_directories):
        problem_id = problem_dir.name
        logging.info(f"\n--- Checking Problem {i+1}/{total_problems}: {problem_id} ---")

        if problem_id in processed_ids:
            logging.info(f"Problem '{problem_id}' has already been processed. Skipping.")
            continue
        
        try:
            problem = load_problem_from_directory(problem_dir)
            pairs = create_code_pairs(problem, num_mutants, max_pairs)
            if pairs:
                append_to_jsonl(output_path, pairs)
                logging.info(f"✅ Success! {len(pairs)} pairs for '{problem_id}' were saved to '{output_path}'.")
                new_pairs_generated += len(pairs)
        except Exception as e:
            logging.error(f"Failed to process problem '{problem_id}': {e}", exc_info=True)

    logging.info("\n--- PIPELINE FINISHED ---")
    if new_pairs_generated > 0:
        logging.info(f"✅ {new_pairs_generated} new pairs were added to the output file.")
    else:
        logging.warning("No new pairs were generated in this run.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser(
        description="Pipeline to generate preference pairs for code problems with persistence.",
    )
    
    parser.add_argument(
        "--data_dir",
        type=str,
        default="questions",
        help="Path to the directory containing problem folders. Default: 'questions'"
    )
    parser.add_argument(
        "--output_file",
        type=str,
        default="outputs/pairs.jsonl",
        help="Path to the output .jsonl file. Default: 'outputs/pairs.jsonl'"
    )
    parser.add_argument(
        "--num_mutants",
        type=int,
        default=5,
        help="Number of mutants to request from the LLM per problem. Default: 5"
    )
    parser.add_argument(
        "--max_pairs",
        type=int,
        default=1,
        help="Maximum number of pairs to save per problem. Default: 1"
    )

    args = parser.parse_args()
    
    Path(args.output_file).parent.mkdir(parents=True, exist_ok=True)
    
    process_problem_directory(
        data_path=Path(args.data_dir),
        output_path=Path(args.output_file),
        num_mutants=args.num_mutants,
        max_pairs=args.max_pairs
    )
