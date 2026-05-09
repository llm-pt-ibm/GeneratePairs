import json
import logging
from typing import List

import openai

from problem_loader import ProblemData
from config import OPENAI_API_KEY, OPENROUTER_API_KEY, MUTATION_MODEL


def generate_mutants_with_llm(problem: ProblemData, num_mutants: int) -> List[str]:
    """
    Use a Large Language Model (LLM) to generate mutant (likely incorrect)
    versions of a correct reference solution.

    This approach aims to create semantically meaningful bugs that a human
    might introduce, providing a more challenging and realistic dataset
    for training and evaluation.

    Args:
        problem: ProblemData object containing the reference solution.
        num_mutants: Number of mutant versions to generate.

    Returns:
        A list of strings, where each string is a full mutant source code.
    """
    logging.info(
        f"Generating {num_mutants} mutants for problem '{problem.problem_id}' using {MUTATION_MODEL}..."
    )

    is_openrouter = "/" in MUTATION_MODEL
    if is_openrouter:
        if not OPENROUTER_API_KEY:
            logging.error("OPENROUTER_API_KEY is not set. Mutant generation will be skipped.")
            return []
        client = openai.OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
        )
    else:
        if not OPENAI_API_KEY:
            logging.error("OPENAI_API_KEY is not set. Mutant generation will be skipped.")
            return []
        client = openai.OpenAI(api_key=OPENAI_API_KEY)

    # Detailed prompt to guide the LLM to create useful mutations.
    prompt = f"""
    You are an expert in Software Mutation Testing. Your task is to act as a "mutation engine".
    I will provide a Java source code that correctly solves a problem.

    Your mission: Generate {num_mutants} alternative versions of this code. Each version must contain
    **one single subtle bug** that causes the program to fail on some test cases. The mutant code
    must, whenever possible, be syntactically correct and successfully compile.

    To introduce bugs, draw inspiration from the following mutation operator types:
    - Relational Operator Replacement: Replace >, <, >=, <=, ==, !=.
    - Off-By-One Error: Change loop bounds or array indexing.
    - Arithmetic Operator Replacement: Replace + with -, etc.
    - Constant Modification: Change a numeric literal value.

    **Important:** Do not add any comment or annotation in the mutant code explaining the change.
    The code must look natural, as if it were written by a human who did not notice the bug.

    Output format: Respond with a single JSON object. The object must have a single key, "mutants",
    which is a list of strings. Each string in the list must be the full source code of one mutant.

    Original and correct source code:
    ```java
    {problem.reference_solution}
    """

    try:
        response = client.chat.completions.create(
            model=MUTATION_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert in Software Mutation Testing and must respond in JSON format."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.5,  # Some creativity is useful for varied mutants
        )

        response_content = response.choices[0].message.content
        mutants_json = json.loads(response_content)

        mutants = mutants_json.get("mutants", [])
        if not isinstance(mutants, list) or not all(isinstance(m, str) for m in mutants):
            raise ValueError("LLM response for 'mutants' is not a list of strings.")

        logging.info(f"Successfully generated {len(mutants)} mutants.")
        return mutants

    except Exception as e:
        logging.error(
            f"Failed to generate mutants due to an API error or invalid response: {e}"
        )
        return []
