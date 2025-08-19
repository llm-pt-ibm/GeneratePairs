from abc import ABC, abstractmethod
from typing import List, Dict, Any
import json
import uuid
import re
import os
import random
import asyncio

import backoff
import datasets
import openai

##############################################################
# 0. random stuff (e.g., file operations)


def read_jsonl(file_path: str) -> List[Any]:
    res = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            json_obj = json.loads(line.strip())
            res.append(json_obj)
    return res


def write_to_jsonl(file_path: str, data: List[Any]) -> None:
    with open(file_path, 'w') as f:
        for item in data:
            json_line = json.dumps(item, ensure_ascii=False)
            f.write(json_line + '\n')

##############################################################
# 1. load/sample dataset
#
# to add support for a new dataset, create a load frunction similar to those below
# the load function should return a list of dict objects, with the following keys:
#   id: unique uuid identifier for this question (see load_mmlu_pro for an example of how to construct them in a reproducable way)
#   original_id: original idenfier from origianl dataset (set to None if not applicable)
#   source: reference to original dataset/subset (if applicable)
#   question: the input passed to the model
#   ground truth: the correct responses (or anything that is necessary e.g., test cases).
#                  Additional processing of the ground truth can be done by subclassing SolutionChecker overriding get_ground_truth()
#
# also, add a corresponding if statement to load_examples_from_dataset_name, which maps the dataset name to the load function


def load_mmlu_pro() -> List[Dict[str, Any]]:
    dataset = datasets.load_dataset("TIGER-Lab/MMLU-Pro", split="test")

    examples = []
    for category in list(set(dataset["category"])):
        filtered_dataset = dataset.filter(
            lambda example: example["category"] == category)

        indicies = random.sample(range(0, len(filtered_dataset)), 5)
        filtered_dataset = filtered_dataset.select(list(indicies))

        for row in filtered_dataset:
            question = row["question"]
            letters = "ABCDEFGHIJ"
            for letter, option in zip(letters, row["options"]):
                question += f"\n({letter}) {option}"
            question += "\nIf you cannot determine the correct multiple-choice answer, take your best guess. Once you have your answer, please duplicate that letter five times in a single string. For example, if the answer is K, then write KKKKK.\nLet's think step by step."

            print(question)

            ground_truth = f"({letters[row['answer_index']]}) {row['options'][row['answer_index']]}"

            example = {
                "original_id": row["question_id"],
                "source": f"mmlu-pro-{category}",
                "question": question,
                "ground_truth": ground_truth,
            }

            unique_id = str(uuid.uuid5(
                uuid.NAMESPACE_DNS, json.dumps(example)))
            example_with_unique_id = {"question_id": unique_id}
            example_with_unique_id.update(example)

            examples.append(example_with_unique_id)

    return examples


def load_examples_from_dataset_name(dataset_name: str) -> Any:
    if dataset_name == "mmlu_pro":
        return load_mmlu_pro()
    else:
        raise NotImplementedError(
            f"Loader for {dataset_name} is not yet implemented.")

##############################################################
# 2. generate n_responses responses for each question


##############################################################
# 3. check correctness of each repsonses for each question
#
# The SolutionChecker is an abstract class, intended to be subclassed to exhibit specific behavior
# New solution checkers must override __init__() to define the client, system message, and user message template
# Feel free to also override get_ground_truth for more customization
#
# Internally, we route requests containing the question, response, ground truth to "gpt-4o-mini-2024-07-18",
# which returns a json object with the key "is_correct" indicating correctness. Be sure that the system message inlcudes such instructions
#
# Like many other parts of the pipeline, the check method must be async.
#
# One special case is evaluating code agianst test cases via the code interpreter, see dataset/check_answers/HumanEvalSolutionChecker


class SolutionChecker(ABC):

    @abstractmethod
    def __init__(self):
        pass

    def get_ground_truth(self, ground_truth: Any) -> str:
        return ground_truth

    async def check(self, question: str, response: str, ground_truth: str, **kwargs) -> bool:
        messages = [
            {"role": "system", "content": self.system_message},
            {"role": "user", "content": self.user_message.format(
                question, response, self.get_ground_truth(ground_truth))}
        ]
        return await self._chat(messages, **kwargs)

    @backoff.on_exception(backoff.fibo, (openai.OpenAIError), max_tries=5, max_value=30)
    async def _chat(self, messages: List[Dict[str, str]], **kwargs) -> bool:
        response = await self.client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=messages,
            temperature=0.0,
            response_format={"type": "json_object"},
            **kwargs,
        )
        response = json.loads(response.choices[0].message.content)
        assert "is_correct" in response, "Key is_correct missing from response."
        return response["is_correct"]


class MultipleChoiceSolutionChecker(SolutionChecker):
    def __init__(self):
        self.client = openai.AsyncClient(
            api_key=os.environ.get("OPENAI_API_KEY"))
        self.system_message = "I will provide you with a multiple-choice question, a response from an LLM, and the correct option. Output a valid JSON object containing a single key-value pair, where the key is \"is_correct\" and corresponding value is a boolean indicating whether or not the LLM-generated selects the correct option."
        self.user_message = "<|Question|>\n{0}\n\n<|LLM Response|>\n{1}\n\n<|Correct Answer|>\n{2}"


class RegexMultipleChoiceSolutionChecker(SolutionChecker):
    def __init__(self):
        self.pattern = r'[A-J]'

    def get_ground_truth(self, ground_truth: Any) -> str:
        # (A) blah so ground_truth[1] returns correct letter choice in mmlu-pro format
        return ground_truth[1]

    async def check(self, question: str, response: str, ground_truth: str, **kwargs) -> bool:

        await asyncio.sleep(0)  # hack to treat function as async

        matches = re.findall(self.pattern, response)
        if not matches:
            return False
        pred = matches[-1]
        if pred == self.get_ground_truth(ground_truth):
            return True
        else:
            return False


class Regex5TimesMultipleChoiceSolutionChecker(RegexMultipleChoiceSolutionChecker):
    def __init__(self):
        self.pattern = r'\b([A-J])\1{4}\b'


def get_solution_check_from_dataset_name(dataset_name: str) -> Any:
    if dataset_name in ["mmlu_pro"]:
        return [MultipleChoiceSolutionChecker(), Regex5TimesMultipleChoiceSolutionChecker()]
    else:
        raise NotImplementedError(
            f"Solution checker for {dataset_name} is not yet implemented.")

##############################################################
# 4. compute intermediate metrics
# Hopefully this is self-explanatory, basically just trying to understand how the response_model performs on the dataset


def compute_intermediate_metrics(examples: List[Dict[str, Any]]) -> None:
    n_examples = len(examples)
    n_all_correct = sum(
        all([generated_response["is_correct"]
            for generated_response in example["generated_responses"]])
        for example in examples
    )
    n_all_incorrect = sum(
        all([not generated_response["is_correct"]
            for generated_response in example["generated_responses"]])
        for example in examples
    )
    n_some_correct = n_examples - n_all_correct - n_all_incorrect
    print(f"Total number of examples: {n_examples}")
    print(f"{n_all_correct} of {n_examples} ({(100*n_all_correct/n_examples):.2f}%) questions contained only correct responses.")
    print(f"{n_all_incorrect} of {n_examples} ({(100*n_all_incorrect/n_examples):.2f}%) questions contained only incorrect responses.")
    print(f"{n_some_correct} of {n_examples} ({(100*n_some_correct/n_examples):.2f}%) questions contained both correct and incorrect responses.")

##############################################################
# 5. sample pairs for judging
# Here we sample pairs of correct/incorrect responses from each question
# default behavior is to sample just one pair from each questions, but can be configured via max_pairs_per_question
# pairs have a different json structure, see below


def sample_pairs(examples: List[Dict[str, Any]], max_pairs_per_question: int = 1) -> List[Dict[str, Any]]:

    pairs = []
    for example in examples:

        is_corrects = [answer["is_correct"]
                       for answer in example["generated_responses"]]

        if not (True in is_corrects and False in is_corrects):
            continue

        correct = [answer for answer in example["generated_responses"]
                   if answer["is_correct"] is True]
        incorrect = [answer for answer in example["generated_responses"]
                     if answer["is_correct"] is False]

        new_pairs = []
        for correct_response in correct:
            for incorrect_response in incorrect:

                pair = {k: v for k, v in example.items() if k !=
                        "generated_responses"}

                if random.random() < 0.5:
                    pair.update({
                        "response_model": example["generated_responses"][0]["model"],
                        "response_A": correct_response["response"],
                        "response_B": incorrect_response["response"],
                        "label": "A>B",
                    })
                else:
                    pair.update({
                        "response_model": example["generated_responses"][0]["model"],
                        "response_A": incorrect_response["response"],
                        "response_B": correct_response["response"],
                        "label": "B>A",
                    })

                unique_id = str(uuid.uuid5(
                    uuid.NAMESPACE_DNS, json.dumps(pair)))
                pair_with_unique_id = {"pair_id": unique_id}
                pair_with_unique_id.update(pair)
                new_pairs.append(pair_with_unique_id)

        random.shuffle(new_pairs)
        pairs.extend(new_pairs[:max_pairs_per_question])

    return pairs