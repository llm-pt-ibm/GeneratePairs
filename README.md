# GeneratePairs

Pipeline for generating **preference pairs** (correct vs. subtly incorrect responses) used to evaluate **LLM-as-a-Judge** systems on Brazilian benchmarks.

The core challenge for a Judge model is to correctly identify which of two responses is better when both sound plausible — the incorrect response is deliberately designed to contain a subtle flaw in reasoning rather than an obvious error.

![Pipeline Overview](image/pipeline.png)

## How It Works

For each question, the pipeline:

1. **Loads questions** from a supported dataset.
2. **Generates k responses** using an LLM, instructed to produce exactly 1 correct and k−1 subtly incorrect answers.
3. **Validates each response** using a combination of an LLM checker (GPT-4o-mini) and a regex-based checker, keeping only responses with high confidence.
4. **Computes metrics** on the proportion of all-correct / all-incorrect / mixed questions.
5. **Samples preference pairs** — one correct response vs. one incorrect response per question, with positions (A/B) randomized to avoid position bias.

Intermediate outputs are saved at each stage (`stage1.jsonl` through `stage5.jsonl`) so the pipeline can be resumed from any checkpoint.

## Datasets

All datasets are Brazilian Portuguese benchmarks:

| Area | Sources | Questions in final dataset |
|------|---------|---------------------------|
| `knowledge` | BLUEX (100), HEALTHQA (100), ENEM (100) → filtered to ~30% each | 87 pairs |
| `mathematics` | BLUEX (100), ENEM (85), POSCOMP (100) → filtered to ~30% each | 72 pairs |
| `reasoning` | POSCOMP — Lógica Matemática (62 questions) | 50 pairs |
| `code` | Programming problems (Java) | 53 pairs |
| **Total** | | **262 pairs** |

## Directory Structure

```
GeneratePairs/
├── judgebench-pipeline/       # Main pipeline for multiple-choice questions
│   ├── generate_pairs.py      # Orchestrates all pipeline stages
│   ├── utils.py               # Dataset loaders, checkers, pair sampling
│   ├── model_utils.py         # API clients (OpenAI, Anthropic, Gemini, etc.)
│   ├── add_area.py            # Utility to tag pairs with an area label
│   └── outputs/               # Per-run intermediate outputs (stage1–stage5)
├── code_pairs/                # Preference pairs from code/programming domain
├── knowledge/                 # Raw knowledge question files
├── mathematics/               # Raw math question files
├── reasoning/                 # Raw reasoning question files
├── pairs_all_tasks/           # Final merged dataset (all 262 pairs)
│   ├── data.jsonl             # The complete preference pair dataset
│   └── info.txt               # Dataset composition notes
└── image/                     # Pipeline diagram
```

## Installation

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install openai anthropic backoff datasets tqdm
```

## Configuration

Set the API keys for whichever providers you plan to use:

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENROUTER_API_KEY="sk-or-..."   # for OpenRouter models
# For Google Gemini via Vertex AI, run: gcloud auth application-default login
```

## Usage

Run the pipeline from the `judgebench-pipeline/` directory:

```bash
cd judgebench-pipeline

python generate_pairs.py \
  --dataset_name knowledge \
  --response_model openai/gpt-4o-mini \
  --n_responses 5 \
  --max_pairs_per_question 1
```

### Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--dataset_name` | Dataset to use: `knowledge`, `math`, `reasoning` | required |
| `--response_model` | Model to generate responses (see below) | required |
| `--n_responses` | Total responses per question (1 correct + n−1 incorrect) | `5` |
| `--max_pairs_per_question` | Max preference pairs sampled per question | `1` |
| `--concurrency_limit` | Number of concurrent API requests | `1` |
| `--seed` | Random seed for reproducibility | `42` |
| `--questions_with_responses` | Skip generation and start from a `stage2.jsonl` file | `None` |

### Supported Models

The `--response_model` argument accepts any of the following formats:

| Format | Example | Provider |
|--------|---------|----------|
| `gpt-*` / `o*` | `gpt-4o`, `o1` | OpenAI |
| `claude-*` | `claude-3-5-sonnet-20241022` | Anthropic |
| `gemini-*` | `gemini-1.5-pro-001` | Google (Vertex AI) |
| `provider/model` | `openai/gpt-4o-mini`, `google/gemini-2.0-flash-001` | OpenRouter |
| any other string | `meta-llama/Llama-3.1-70B-Instruct` | Local (vLLM on `localhost:8000`) |

### Resuming from a checkpoint

If response generation already ran, skip it and go straight to validation:

```bash
python generate_pairs.py \
  --dataset_name knowledge \
  --response_model openai/gpt-4o-mini \
  --questions_with_responses outputs/dataset_name=knowledge,.../stage2.jsonl
```

### Tagging pairs with an area label

After generating pairs (`stage5.jsonl`), add an `area` field:

```bash
python add_area.py \
  --input outputs/.../stage5.jsonl \
  --area knowledge
```

This produces `stage5_area.jsonl` alongside the input file.

## Output Format

Each line in the final `data.jsonl` is a JSON object:

```json
{
  "pair_id": "<uuid>",
  "question_id": "<uuid>",
  "original_id": "...",
  "source": "bluex-knowledge-42",
  "question": "Which of the following ...\n(A) ...\n(B) ...",
  "ground_truth": "(A) ...",
  "response_model": "openai/gpt-4o-mini",
  "response_A": "Step-by-step reasoning... AAAAA",
  "response_B": "Plausible but subtly wrong reasoning... BBBBB",
  "label": "A>B",
  "area": "knowledge"
}
```

`label` is either `"A>B"` (response A is correct) or `"B>A"` (response B is correct). Positions are randomized at pair-sampling time.
