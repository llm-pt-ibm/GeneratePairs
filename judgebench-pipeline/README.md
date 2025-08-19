### Generating Pairs
`generate_pairs.py` performs the following:
0. random stuff (e.g. random seeding, figuring out output dir)
1. load and optionally sample from the source dataset
2. generate n_responses responses for each question using the response_model
3. check correctness of each repsonses for each question
4. compute intermediate metrics (e.g., how accuracte was the response_model)
5. sample max_pairs_per_question pairs from each question which includes both correct/incorrect responses

> Intermediate files are saved after stages 1, 2, 3, and 5.

Example run command:
```
python generate_pairs.py --dataset_name mmlu_pro --response_model gpt-4o-mini-2024-07-18 --n_responses 5 --max_pairs_per_question 1  --seed 42 --concurrency_limit 10
```
`generate_pairs.py` has a secondary entry point at before stage 3, which can be useful if some error is not caught while checking correctness or generating the pairs. Pass the `stage2.jsonl` file as shown below:
```
python generate_pairs.py --dataset_name mmlu_pro --response_model gpt-4o-mini-2024-07-18 --n_responses 5 --max_pairs_per_question 1 --seed 42 --concurrency_limit 10 --questions_with_responses /path/to/stage2.jsonl
```