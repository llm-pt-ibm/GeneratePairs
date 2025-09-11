import json

with open("questions_HEALTHQA.json", "r", encoding="utf-8") as f_in:
    lista = json.load(f_in)  # lista de objetos

with open("questions_HEALTHQA.jsonl", "w", encoding="utf-8") as f_out:
    for obj in lista:
        f_out.write(json.dumps(obj, ensure_ascii=False) + "\n")

print(f"{len(lista)} linhas escritas em JSONL.")
