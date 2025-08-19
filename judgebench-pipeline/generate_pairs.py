from typing import List, Dict, Any
import argparse
import asyncio
import os
import random

from tqdm.asyncio import tqdm_asyncio

import utils
import model_utils

async def generate_responses(examples: List[Dict[str, Any]], model: str, n_responses: int = 5, concurrency_limit: int = 1) -> List[Dict[str, Any]]:
    semaphore = asyncio.Semaphore(concurrency_limit)
    answer_api = model_utils.get_chat_api_from_model(model)
    
    async def generate_response(example: Dict[str, Any]):
        async with semaphore:
            
            question = example["question"]
            ground_truth = example["ground_truth"]
            
            generated_responses = []
            for _ in range(n_responses):
                
                try:
                    response = await answer_api.chat(
                        messages = [{"role": "user", "content": question}],
                        temperature = 1.0,
                    )
                except Exception as e:
                    response = None
                    print(f"Failed to generate a response for question {example['question_id']} due to the following error: {e}.")
                
                generated_responses.append({
                    "model": model,
                    "response": response,
                    "is_correct": None,
                })
                
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
    parser.add_argument('--dataset_name', type=str, required=True) # dataset name, should correspond to an entry in utils/load_examples_from_dataset_name
    parser.add_argument('--response_model', type=str, required=True) # all openai/claude models are supported, other models are routed through VLLM client.
    parser.add_argument('--n_responses', type=int, default=5) # number of responses to generate for question
    parser.add_argument('--max_pairs_per_question', type=int, default=1) # maximum number of pairs to construct from each question
    parser.add_argument('--seed', type=int, default=42) # seed to use
    parser.add_argument('--concurrency_limit', type=int, default=1) # some stages use asyncio to speed things up, 10 is usally a good value here
    parser.add_argument('--questions_with_responses', type=str, default=None) # path to stage2.jsonl file that contains generated responses prior to their checking correctness
    args = parser.parse_args()
    main(args)
    
# some example run commands
#
# run the full pipeline to generate pairs
# python generate_pairs.py --dataset_name mmlu_pro --response_model gpt-4o-mini-2024-07-18 --n_responses 5 --max_pairs_per_question 1  --seed 42 --concurrency_limit 10
#
# secondary entry point between stages 2 and 3: given questions with responses, will check correctness and sample pairs for judging
# python generate_pairs.py --dataset_name mmlu_pro --response_model gpt-4o-mini-2024-07-18 --n_responses 5 --max_pairs_per_question 1 --seed 42 --concurrency_limit 10 --questions_with_responses /path/to/stage2.jsonl