import json
import random

INPUT_FILE = "questions_HEALTHQA.jsonl"   # seu arquivo original
OUTPUT_FILE = "SAMPLE_30_HEALTHQA.jsonl"  # nome do arquivo de saída

# Lê todas as linhas do arquivo
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    questoes = [json.loads(line) for line in f if line.strip()]

# Calcula 30% do total
num_amostra = int(0.3 * len(questoes))

# Seleciona aleatoriamente
amostra = random.sample(questoes, num_amostra)

# Salva a amostra em um novo arquivo
with open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:
    for questao in amostra:
        f_out.write(json.dumps(questao, ensure_ascii=False) + "\n")

print(f"{num_amostra} questões salvas em '{OUTPUT_FILE}'")
