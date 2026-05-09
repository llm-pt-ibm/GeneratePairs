import json
import argparse
from pathlib import Path


def jsonl_to_json(input_path: str, output_path: str) -> None:
    input_file = Path(input_path)
    output_file = Path(output_path)

    data = []
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"{len(data)} pairs converted: {input_file} -> {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a .jsonl file to .json")
    parser.add_argument("--input",  type=str, default="outputs/pairs.jsonl")
    parser.add_argument("--output", type=str, default="outputs/pairs.json")
    args = parser.parse_args()

    jsonl_to_json(args.input, args.output)
