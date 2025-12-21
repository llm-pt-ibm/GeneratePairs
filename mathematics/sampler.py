import json
import random
import argparse
from typing import List, Any

def sample_jsonl(input_path: str, output_path: str, n: int = 100, seed: int | None = None) -> None:
    if seed is not None:
        random.seed(seed)

    reservoir: List[Any] = []
    total = 0

    # Passa uma única vez pelo arquivo (streaming)
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                # pula linhas inválidas, se houver
                continue

            if total < n:
                reservoir.append(obj)
            else:
                j = random.randint(0, total)
                if j < n:
                    reservoir[j] = obj
            total += 1

    # Se o arquivo tiver menos de n linhas, ajusta
    k = min(n, total)

    with open(output_path, "w", encoding="utf-8") as out:
        for i in range(k):
            out.write(json.dumps(reservoir[i], ensure_ascii=False) + "\n")

    print(f"{k} instâncias salvas em '{output_path}' (de um total de {total} linhas lidas)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Amostragem aleatória de N instâncias de um JSONL (reservoir sampling).")
    parser.add_argument("--input", "-i", required=True, help="Caminho do JSONL de entrada")
    parser.add_argument("--output", "-o", default="SAMPLE_100.jsonl", help="Caminho do JSONL de saída")
    parser.add_argument("--n", "-n", type=int, default=100, help="Tamanho da amostra (padrão: 100)")
    parser.add_argument("--seed", type=int, default=None, help="Seed para reprodutibilidade (opcional)")
    args = parser.parse_args()

    sample_jsonl(args.input, args.output, args.n, args.seed)
