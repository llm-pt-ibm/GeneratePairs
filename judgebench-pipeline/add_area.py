import json
import argparse
from pathlib import Path


def add_area(input_path: str, output_path: str, area: str) -> None:
    input_file = Path(input_path)
    output_file = Path(output_path)

    data = []
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            item["area"] = area
            data.append(item)

    with open(output_file, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"{len(data)} pairs updated with area='{area}': {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add area field to stage5.jsonl")
    parser.add_argument("--input",  type=str, required=True, help="Path to stage5.jsonl")
    parser.add_argument("--output", type=str, default=None,  help="Output path (default: stage5_area.jsonl alongside input)")
    parser.add_argument("--area",   type=str, required=True, help="Area value to add (ex: mathematics, knowledge, reasoning, code)")
    args = parser.parse_args()

    output = args.output or str(Path(args.input).parent / "stage5_area.jsonl")
    add_area(args.input, output, args.area)
