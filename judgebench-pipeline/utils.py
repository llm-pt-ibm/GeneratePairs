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
# 0. Funções de Arquivo (sem alterações)


def read_jsonl(file_path: str) -> List[Any]:
    """
    Lê um arquivo .jsonl, agora ignorando linhas em branco para evitar erros.
    """
    res = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Remove espaços em branco do início e do fim da linha
            stripped_line = line.strip()
            # Apenas processa a linha se ela não estiver vazia
            if stripped_line:
                try:
                    json_obj = json.loads(stripped_line)
                    res.append(json_obj)
                except json.JSONDecodeError:
                    print(f"Aviso: Pulando linha com JSON mal formado: {stripped_line}")
    return res


def write_to_jsonl(file_path: str, data: List[Any]) -> None:
    with open(file_path, 'w') as f:
        for item in data:
            json_line = json.dumps(item, ensure_ascii=False)
            f.write(json_line + '\n')

##############################################################
# 1. Carregamento de Datasets

# --- NOVA ADIÇÃO: Função Auxiliar para Padronização ---
def _formatar_exemplo_multipla_escolha(
    id_original: str,
    fonte: str,
    enunciado: str,
    alternativas: List[str],
    gabarito_letra: str
) -> Dict[str, Any]:
    """
    Função auxiliar para padronizar qualquer questão de múltipla escolha
    para o formato que nosso pipeline espera.
    """
    prompt = enunciado
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    alternativas_formatadas = []
    for i, alt_texto in enumerate(alternativas):
        # Remove prefixos como "a) " ou "B) " para garantir um padrão único
        texto_limpo = re.sub(r'^[a-zA-Z]\)\s*', '', alt_texto).strip()
        alternativas_formatadas.append(f"({letras[i]}) {texto_limpo}")

    prompt += "\n" + "\n".join(alternativas_formatadas)
    
    # Adiciona as mesmas instruções do MMLU-pro para garantir a consistência
    prompt += "\n\nSe você não conseguir determinar a resposta correta de múltipla escolha, dê o seu melhor palpite. Depois de ter sua resposta, duplique essa letra cinco vezes em uma única string. Por exemplo, se a resposta for K, escreva KKKKK.\nVamos pensar passo a passo."

    # Encontra o índice da letra do gabarito para pegar o texto completo
    gabarito_letra_upper = gabarito_letra.upper()
    try:
        gabarito_index = letras.find(gabarito_letra_upper)
        if gabarito_index == -1: # Se a letra não for encontrada
            raise IndexError
        ground_truth = alternativas_formatadas[gabarito_index]
    except (IndexError, AttributeError):
        # Fallback caso o gabarito seja inválido ou não seja uma string
        ground_truth = gabarito_letra_upper

    example = {
        "original_id": id_original,
        "source": fonte,
        "question": prompt,
        "ground_truth": ground_truth,
    }

    unique_id = str(uuid.uuid5(
        uuid.NAMESPACE_DNS, json.dumps(example, sort_keys=True)))
    example_with_unique_id = {"question_id": unique_id}
    example_with_unique_id.update(example)
    return example_with_unique_id

# --- NOVA ADIÇÃO: Carregador para os datasets de Knowledge ---
def load_knowledge(file_path: str = "knowledge_data.jsonl") -> List[Dict[str, Any]]:
    """
    Nova função para carregar as questões do arquivo knowledge_data.jsonl,
    que contém uma mistura de formatos (BLUEX, ENEM, HEALTHQA).
    """
    dados_brutos = read_jsonl(file_path)
    exemplos_formatados = []

    for item in dados_brutos:
        # Tenta extrair os campos comuns. Continua se algum campo essencial faltar.
        enunciado = item.get("question")
        alternativas = item.get("alternatives")
        gabarito_letra = item.get("label")

        if not all([enunciado, alternativas, gabarito_letra]):
            continue

        # Identifica a fonte do dado e extrai as informações
        if "subject" in item: # Critério para BLUEX
            fonte = f"bluex-{item.get('id', 'unknown')}"
            id_original = item.get("id")
        elif "exam" in item: # Critério para ENEM
            fonte = f"enem-{item.get('exam', 'unknown')}-{item.get('id', 'unknown')}"
            id_original = item.get("id")
        elif "source" in item: # Critério para HEALTHQA
            fonte = f"healthqa-{item.get('source', 'unknown')}-{item.get('id', 'unknown')}"
            id_original = item.get("id")
        else:
            # Pula linhas que não correspondem a nenhum formato conhecido
            continue

        # Usa a função auxiliar para padronizar os dados extraídos
        exemplo_padronizado = _formatar_exemplo_multipla_escolha(
            id_original, fonte, enunciado, alternativas, gabarito_letra
        )
        exemplos_formatados.append(exemplo_padronizado)
        
    return exemplos_formatados

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

# --- NOVA ADIÇÃO: Atualização da função "Dispatcher" ---
def load_examples_from_dataset_name(dataset_name: str) -> Any:
    """
    Função "dispatcher" que chama o carregador correto com base no nome do dataset.
    """
    if dataset_name == "mmlu_pro":
        return load_mmlu_pro()
    elif dataset_name == "knowledge":
        # Adiciona o novo dataset aqui. Assume que o arquivo está na pasta raiz.
        return load_knowledge("/Users/ronalddmatias/GeneratePairs/knowledge/data.jsonl")
    else:
        raise NotImplementedError(
            f"O carregador para o dataset '{dataset_name}' ainda não foi implementado.")

##############################################################
# 2. Geração de Respostas (sem alterações)
##############################################################


##############################################################
# 3. Verificação de Correção

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

# --- NOVA ADIÇÃO: Atualização da função "Dispatcher" ---
def get_solution_check_from_dataset_name(dataset_name: str) -> Any:
    """
    Retorna a lista de verificadores corretos para um determinado dataset.
    """
    # Adicionamos nosso novo dataset à lista dos que usam os verificadores padrão.
    if dataset_name in ["mmlu_pro", "knowledge"]:
        return [MultipleChoiceSolutionChecker(), Regex5TimesMultipleChoiceSolutionChecker()]
    else:
        raise NotImplementedError(
            f"O verificador para o dataset '{dataset_name}' ainda não foi implementado.")

##############################################################
# 4. Métricas Intermediárias (sem alterações)
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
# 5. Amostragem de Pares (sem alterações)
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