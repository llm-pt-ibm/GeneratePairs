import json
import uuid
import argparse
from pathlib import Path


def format_code_pairs(input_path: str, output_path: str, response_model: str) -> None:
    input_file = Path(input_path)
    output_file = Path(output_path)

    data = []
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)

            formatted = {
                "pair_id": str(uuid.uuid4()),
                "source": item["problem_id"],
                "question": item["prompt"],
                "response_model": response_model,
                "response_A": item["response_A"],
                "response_B": item["response_B"],
                "label": item["label"],
                "area": "code",
            }
            data.append(formatted)

    with open(output_file, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"{len(data)} pairs formatted: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Format code pairs to the standard pipeline format.")
    parser.add_argument("--input",          type=str, default="outputs/pairs.jsonl")
    parser.add_argument("--output",         type=str, default="outputs/pairs_formatted.jsonl")
    parser.add_argument("--response_model", type=str, required=True, help="Model used to generate the mutants (ex: openai/gpt-4o)")
    args = parser.parse_args()

    format_code_pairs(args.input, args.output, args.response_model)
