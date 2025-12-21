# Code Question Preference Pair Generation Pipeline

A Python pipeline for generating preference pairs from code problems using LLM-generated mutants. This pipeline processes Java coding problems, generates mutated (buggy) versions using an LLM, validates them through test execution, and creates preference pairs for training and evaluation purposes.

## Overview

This pipeline automates the generation of preference pairs from coding problems by:

1. **Loading** coding problems from structured directories
2. **Validating** the reference solution against test cases
3. **Generating** mutated versions of the solution using an LLM
4. **Executing** tests to verify which mutants fail
5. **Creating** preference pairs (correct vs incorrect solutions)

The generated pairs can be used for training preference models, evaluating code generation systems, or creating datasets for research purposes.

## Requirements

### System Requirements

- **Python**: 3.7 or higher
- **Java Development Kit (JDK)**: Required for compiling and executing Java code
- **OpenAI API Key**: Required for generating mutants using GPT models

### Python Dependencies

Install the required packages:

```bash
pip install openai pyyaml
```

Or install from the parent directory's requirements:

```bash
pip install -r ../requirements.txt
```

## Setup

### 1. Configure API Key

Edit `config.py` and add your OpenAI API key:

```python
OPENAI_API_KEY = "your-api-key-here"
MUTATION_MODEL = "gpt-4o"  # or another model of your choice
```

### 2. Prepare Your Data Structure

Each coding problem should be in its own directory with the following structure:

```
questions/
├── problem_name/
│   ├── problem_name.yaml    # Problem metadata and test cases
│   └── Solution.java        # Reference solution (or any .java file)
```

#### YAML File Format

The YAML file must contain:
- `text`: The problem statement/description
- `tests`: A list of test cases, each with:
  - `input`: Input string for the program
  - `output`: Expected output string

Example YAML structure:
```yaml
name: busca_binaria
text: |
  # Problem Description
  Implement a binary search algorithm...
tests:
  - input: |
      3 5 8 10 12 18 20
      99
    output: |
      3
      5
      6
      -1
  - input: |
      3 5 8 10 12 18
      3
    output: |
      2
      0
```

#### Java Solution Format

The Java file must:
- Contain a class with a `public static void main(String[] args)` method
- Read input from `stdin`
- Write output to `stdout`
- Compile and run successfully with `javac` and `java`

## Usage

### Basic Usage

Run the pipeline with default settings:

```bash
python main.py
```

This will:
- Process all problems in the `questions/` directory
- Generate 5 mutants per problem
- Create up to 1 preference pair per problem
- Save results to `saidas/pares.jsonl`

### Command-Line Arguments

```bash
python main.py [OPTIONS]
```

**Options:**

- `--data_dir PATH`: Path to directory containing problem folders (default: `questions`)
- `--output_file PATH`: Path to output JSONL file (default: `saidas/pares.jsonl`)
- `--num_mutants N`: Number of mutants to generate per problem (default: `5`)
- `--max_pairs N`: Maximum pairs to save per problem (default: `1`)

### Example Commands

Process a specific directory with custom settings:

```bash
python main.py \
  --data_dir ../questions \
  --output_file outputs/pairs.jsonl \
  --num_mutants 10 \
  --max_pairs 3
```

Resume processing (skips already processed problems):

```bash
python main.py --output_file existing_output.jsonl
```

The pipeline automatically detects which problems have already been processed by checking the `problem_id` field in the output file, allowing you to resume interrupted runs.

## Output Format

The pipeline generates a JSONL file where each line is a JSON object representing a preference pair:

```json
{
  "problem_id": "busca_binaria",
  "prompt": "Implement a binary search algorithm...",
  "response_A": "public class Solution { ... }",
  "response_B": "public class Solution { ... }",
  "label": "A>B"
}
```

**Fields:**
- `problem_id`: Identifier of the problem (directory name)
- `prompt`: Problem statement/description
- `response_A`: First code solution
- `response_B`: Second code solution
- `label`: Preference label (`"A>B"` means A is preferred over B, `"B>A"` means B is preferred over A)

The order of correct vs incorrect solutions is randomized to avoid bias in training.

## Architecture

The pipeline consists of several modules:

### Core Modules

- **`main.py`**: Entry point and orchestration
- **`carregador_problema.py`**: Loads problem data from directories
- **`gerador_mutantes.py`**: Generates mutants using LLM API
- **`executor_codigo.py`**: Compiles and executes Java code with test cases
- **`gerar_pares.py`**: Orchestrates pair creation workflow
- **`config.py`**: Configuration settings (API keys, model selection)

### Workflow

```
1. Load Problem
   └─> Read YAML (problem statement + tests)
   └─> Read Java file (reference solution)

2. Validate Reference Solution
   └─> Compile Java code
   └─> Run all test cases
   └─> Verify all tests pass

3. Generate Mutants
   └─> Call LLM API with reference solution
   └─> Request N mutated versions with subtle bugs

4. Validate Mutants
   └─> For each mutant:
       ├─> Compile code
       ├─> Run test cases
       └─> Keep only mutants that fail tests

5. Create Preference Pairs
   └─> Pair correct solution with each failing mutant
   └─> Randomize order (A/B)
   └─> Limit to max_pairs per problem

6. Save Results
   └─> Append pairs to JSONL file
   └─> Track processed problem IDs
```

## License

See the LICENSE file in the repository root.

