from typing import List, Dict, Any
import argparse
import asyncio
import os
import random
import json

from tqdm.asyncio import tqdm_asyncio

import utils
import model_utils

# --- FUNÇÃO ATUALIZADA ---
# Implementa a metodologia de "solicitação explícita de erros" com um prompt refinado.
async def generate_responses(examples: List[Dict[str, Any]], model: str, n_responses: int = 5, concurrency_limit: int = 1) -> List[Dict[str, Any]]:
    semaphore = asyncio.Semaphore(concurrency_limit)
    answer_api = model_utils.get_chat_api_from_model(model)
    
    async def generate_response(example: Dict[str, Any]):
        async with semaphore:
            
            # --- PROMPT REFINADO ---
            # Este prompt inclui uma instrução explícita para o modelo não se "auto-corrigir".
            prompt_novo = f"""
            Sua tarefa é gerar um conjunto de {n_responses} respostas para a questão de múltipla escolha a seguir.

            REGRAS:
            1.  **Exatamente UMA** dessas {n_responses} respostas deve ser a correta, com um raciocínio claro e preciso.
            2.  As outras **{n_responses - 1} respostas** devem ser SUTILMENTE INCORRETAS.
            3.  Uma resposta sutilmente incorreta é aquela que apresenta um raciocínio que parece plausível, mas que contém um erro lógico, de cálculo ou de interpretação.
            4.  **IMPORTANTE:** Ao escrever o raciocínio para uma resposta incorreta, você deve atuar como alguém que acredita genuinamente que aquele raciocínio está correto. Apresente o argumento com confiança. **NÃO INCLUA frases que revelem que a resposta está errada, que é uma suposição, ou que o cálculo correto seria outro.**
            5.  Para cada resposta, forneça um raciocínio passo a passo e, ao final, declare a alternativa escolhida no formato 'XXXXX' (ex: 'AAAAA').
            
            Formato da Saída: Sua resposta DEVE ser um objeto JSON válido contendo uma única chave "respostas". O valor deve ser uma lista de {n_responses} objetos, onde cada objeto tem duas chaves: "raciocinio" e "resposta_final".

            Exemplo do formato de saída:
            {{
              "respostas": [
                {{
                  "raciocinio": "Raciocínio correto...",
                  "resposta_final": "AAAAA"
                }},
                {{
                  "raciocinio": "Raciocínio confiante, mas com um erro sutil...",
                  "resposta_final": "BBBBB"
                }}
              ]
            }}

            Aqui está a questão:
            ---
            {example["question"]}
            """

            generated_responses = []
            try:
                response_json_str = await answer_api.chat(
                    messages=[{"role": "user", "content": prompt_novo}],
                    temperature=0.8,
                    response_format={"type": "json_object"},
                )
                
                response_data = json.loads(response_json_str)
                respostas_do_modelo = response_data.get("respostas", [])

                for resp in respostas_do_modelo:
                    full_response_text = f"{resp.get('raciocinio', '')}\n\n{resp.get('resposta_final', '')}"
                    generated_responses.append({
                        "model": model,
                        "response": full_response_text.strip(),
                        "is_correct": None,
                    })

            except Exception as e:
                print(f"Falha ao gerar o conjunto de respostas para a questão {example['question_id']} devido ao seguinte erro: {e}.")
                for _ in range(n_responses):
                    generated_responses.append({"model": model, "response": None, "is_correct": None})

            example["generated_responses"] = generated_responses

    tasks = [asyncio.create_task(generate_response(example)) for example in examples]

    for future in tqdm_asyncio.as_completed(tasks):
        await future
        
    return examples


async def check_responses(examples: List[Dict[str, Any]], dataset_name: str, concurrency_limit: int = 1) -> List[Dict[str, Any]]:
    semaphore = asyncio.Semaphore(concurrency_limit)
    solution_checkers = utils.get_solution_check_from_dataset_name(dataset_name)
    
    async def check_response(example: Dict[str, Any]):
        async with semaphore:
            
            question = example["question"]
            ground_truth = example["ground_truth"]
            generated_responses = example["generated_responses"]
            
            for generated_response in generated_responses:
                
                is_correct = []
                for solution_checker in solution_checkers:
                    try:
                        is_correct.append(await solution_checker.check(question, generated_response["response"], ground_truth))
                    except Exception as e:
                        is_correct.append(None)
                        print(f"Failed to check correctness of a response for question {example['question_id']} due to the following error: {e}.")
                
                if all(v is True for v in is_correct):
                    generated_response["is_correct"] = True
                elif all(v is False for v in is_correct):
                    generated_response["is_correct"] = False
                else:
                    generated_response["is_correct"] = None
                
            example["generated_responses"] = generated_responses

    tasks = [asyncio.create_task(check_response(example)) for example in examples]

    for future in tqdm_asyncio.as_completed(tasks):
        await future
        
    return examples
    
            
def main(args: argparse.Namespace) -> None:
    
    # 0. random stuff
    random.seed(args.seed)
    
    output_dir = ','.join(f'{k}={v}' for k, v in vars(args).items() if k in ["dataset_name", "response_model", "n_responses", "max_pairs_per_question"])
    output_dir = output_dir.replace("/", "_") # for local models
    output_dir = os.path.join("outputs", output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    if not args.questions_with_responses:
        # 1. load/sample dataset
        print("Loading dataset ...")
        examples = utils.load_examples_from_dataset_name(args.dataset_name)
        utils.write_to_jsonl(os.path.join(output_dir, "stage1.jsonl"), examples)
        
        # 2. generate n_responses responses for each question
        print("Generating responses ...")
        examples = asyncio.run(generate_responses(examples, args.response_model, n_responses=args.n_responses, concurrency_limit=args.concurrency_limit))
        utils.write_to_jsonl(os.path.join(output_dir, "stage2.jsonl"), examples)
        
    else:
        examples = utils.read_jsonl(args.questions_with_responses)
        
    # 3. check correctness of each repsonses for each question
    print("Checking correctness ...")
    examples = asyncio.run(check_responses(examples, args.dataset_name, concurrency_limit=args.concurrency_limit))
    utils.write_to_jsonl(os.path.join(output_dir, "stage3.jsonl"), examples)
    
    # 4. compute intermediate metrics
    print("Computing intermediate metrics ...")
    utils.compute_intermediate_metrics(examples)

    # 5. sample pairs for judging
    print("Sampling correct/incorrect pairs ...")
    pairs = utils.sample_pairs(examples, args.max_pairs_per_question)
    utils.write_to_jsonl(os.path.join(output_dir, "stage5.jsonl"), pairs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset_name', type=str, required=True)
    parser.add_argument('--response_model', type=str, required=True)
    parser.add_argument('--n_responses', type=int, default=5)
    parser.add_argument('--max_pairs_per_question', type=int, default=1)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--concurrency_limit', type=int, default=1)
    parser.add_argument('--questions_with_responses', type=str, default=None)
    args = parser.parse_args()
    main(args)