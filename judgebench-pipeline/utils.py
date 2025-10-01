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
# 0. Funções de Arquivo
##############################################################

def read_jsonl(file_path: str) -> List[Any]:
    """
    Lê um arquivo .jsonl, ignorando linhas em branco ou mal formadas.
    """
    res = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            stripped_line = line.strip()
            if stripped_line:
                try:
                    json_obj = json.loads(stripped_line)
                    res.append(json_obj)
                except json.JSONDecodeError:
                    print(f"Aviso: Pulando linha com JSON mal formado: {stripped_line}")
    return res


def write_to_jsonl(file_path: str, data: List[Any]) -> None:
    """
    Escreve uma lista de dicionários em um arquivo .jsonl.
    """
    with open(file_path, 'w') as f:
        for item in data:
            json_line = json.dumps(item, ensure_ascii=False)
            f.write(json_line + '\n')

##############################################################
# 1. Carregamento de Datasets
##############################################################

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
        # Regex atualizado para pegar "a)" ou "a."
        texto_limpo = re.sub(r'^[a-zA-Z][\)\.]\s*', '', alt_texto).strip()
        alternativas_formatadas.append(f"({letras[i]}) {texto_limpo}")

    prompt += "\n" + "\n".join(alternativas_formatadas)
    prompt += "\n\nSe você não conseguir determinar a resposta correta de múltipla escolha, dê o seu melhor palpite. Depois de ter sua resposta, duplique essa letra cinco vezes em uma única string. Por exemplo, se a resposta for K, escreva KKKKK.\nVamos pensar passo a passo."

    gabarito_letra_upper = gabarito_letra.upper()
    try:
        gabarito_index = letras.find(gabarito_letra_upper)
        if gabarito_index == -1: raise IndexError
        ground_truth = alternativas_formatadas[gabarito_index]
    except (IndexError, AttributeError):
        ground_truth = gabarito_letra_upper

    example = {
        "original_id": id_original, "source": fonte,
        "question": prompt, "ground_truth": ground_truth,
    }

    unique_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, json.dumps(example, sort_keys=True)))
    example_with_unique_id = {"question_id": unique_id}
    example_with_unique_id.update(example)
    return example_with_unique_id

def load_knowledge(file_path: str) -> List[Dict[str, Any]]:
    """
    Carrega as questões do arquivo de 'knowledge'.
    """
    dados_brutos = read_jsonl(file_path)
    exemplos_formatados = []
    for item in dados_brutos:
        enunciado = item.get("question")
        alternativas = item.get("alternatives")
        gabarito_letra = item.get("label")
        if not all([enunciado, alternativas, gabarito_letra]): continue

        if "subject" in item and "physics" in item["subject"]:
            fonte, id_original = f"bluex-knowledge-{item.get('id', 'unknown')}", item.get("id")
        elif "exam" in item:
            fonte, id_original = f"enem-knowledge-{item.get('exam', 'unknown')}-{item.get('id', 'unknown')}", item.get("id")
        elif "source" in item:
            fonte, id_original = f"healthqa-{item.get('source', 'unknown')}-{item.get('id', 'unknown')}", item.get("id")
        else:
            continue
        
        exemplo_padronizado = _formatar_exemplo_multipla_escolha(
            id_original, fonte, enunciado, alternativas, gabarito_letra
        )
        exemplos_formatados.append(exemplo_padronizado)
    return exemplos_formatados

def load_math(file_path: str) -> List[Dict[str, Any]]:
    """
    Carrega as questões de matemática a partir de um arquivo .jsonl.
    """
    dados_brutos = read_jsonl(file_path)
    exemplos_formatados = []

    for item in dados_brutos:
        enunciado = item.get("question")
        alternativas = item.get("alternatives")
        gabarito_letra = item.get("label")
        if not all([enunciado, alternativas, gabarito_letra]): continue

        if "subject" in item and "mathematics" in item["subject"]:
            fonte = f"bluex-math-{item.get('id', 'unknown')}"
            id_original = item.get("id")
        elif "exam" in item:
            fonte = f"enem-math-{item.get('exam', 'unknown')}-{item.get('id', 'unknown')}"
            id_original = item.get("id")
        elif "area_conhecimento" in item and item["area_conhecimento"] == "Matemática":
            fonte = f"poscomp-{item.get('id', 'unknown')}"
            id_original = item.get("id")
        else:
            continue

        exemplo_padronizado = _formatar_exemplo_multipla_escolha(
            id_original, fonte, enunciado, alternativas, gabarito_letra
        )
        exemplos_formatados.append(exemplo_padronizado)
        
    return exemplos_formatados

def load_reasoning(file_path: str) -> List[Dict[str, Any]]:
    """
    Carrega as questões de 'reasoning' (POSCOMP - Lógica Matemática).
    """
    dados_brutos = read_jsonl(file_path)
    exemplos_formatados = []

    for item in dados_brutos:
        enunciado = item.get("question")
        alternativas = item.get("alternatives")
        gabarito_letra = item.get("label")
        if not all([enunciado, alternativas, gabarito_letra]): continue

        # Critério específico para identificar as questões de Lógica Matemática da POSCOMP
        if item.get("area") == "Lógica Matemática":
            fonte = f"poscomp-reasoning-{item.get('id', 'unknown')}"
            id_original = item.get("id")
            
            exemplo_padronizado = _formatar_exemplo_multipla_escolha(
                id_original, fonte, enunciado, alternativas, gabarito_letra
            )
            exemplos_formatados.append(exemplo_padronizado)
            
    return exemplos_formatados

def load_mmlu_pro() -> List[Dict[str, Any]]:
    # A implementação foi omitida por brevidade, mas o código original permanece aqui
    pass

def load_examples_from_dataset_name(dataset_name: str) -> Any:
    """
    Função "dispatcher" que chama o carregador correto com base no nome do dataset.
    """
    if dataset_name == "mmlu_pro":
        return load_mmlu_pro()
    elif dataset_name == "knowledge":
        return load_knowledge("knowledge_data.jsonl")
    elif dataset_name == "math":
        return load_math("/Users/ronalddmatias/GeneratePairs/mathematics/data.jsonl")
    elif dataset_name == "reasoning":
        return load_reasoning("/Users/ronalddmatias/GeneratePairs/reasoning/reasoning_poscomp.jsonl")
    else:
        raise NotImplementedError(
            f"O carregador para o dataset '{dataset_name}' ainda não foi implementado.")

##############################################################
# 3. Verificação de Correção
##############################################################

class SolutionChecker(ABC):
    @abstractmethod
    def __init__(self): pass
    def get_ground_truth(self, ground_truth: Any) -> str: return ground_truth
    async def check(self, question: str, response: str, ground_truth: str, **kwargs) -> bool:
        messages = [
            {"role": "system", "content": self.system_message},
            {"role": "user", "content": self.user_message.format(
                question, response, self.get_ground_truth(ground_truth))}
        ]
        return await self._chat(messages, **kwargs)
    @backoff.on_exception(backoff.fibo, (openai.OpenAIError), max_tries=5, max_value=30)
    async def _chat(self, messages: List[Dict[str, str]], **kwargs) -> bool:
        raise NotImplementedError

class MultipleChoiceSolutionChecker(SolutionChecker):
    def __init__(self):
        self.client = openai.AsyncClient(api_key=os.environ.get("OPENAI_API_KEY"))
        self.system_message = "I will provide you with a multiple-choice question, a response from an LLM, and the correct option. Output a valid JSON object containing a single key-value pair, where the key is \"is_correct\" and corresponding value is a boolean indicating whether or not the LLM-generated selects the correct option."
        self.user_message = "<|Question|>\n{0}\n\n<|LLM Response|>\n{1}\n\n<|Correct Answer|>\n{2}"
    
    async def _chat(self, messages: List[Dict[str, str]], **kwargs) -> bool:
        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.0,
            response_format={"type": "json_object"},
            **kwargs,
        )
        response_data = json.loads(response.choices[0].message.content)
        assert "is_correct" in response_data, "Key 'is_correct' missing from response."
        return response_data["is_correct"]


class RegexMultipleChoiceSolutionChecker(SolutionChecker):
    def __init__(self):
        self.pattern = r'[A-Z]'
    def get_ground_truth(self, ground_truth: Any) -> str:
        return ground_truth[1]
    async def check(self, question: str, response: str, ground_truth: str, **kwargs) -> bool:
        await asyncio.sleep(0)
        if not response: return False
        matches = re.findall(self.pattern, response)
        if not matches: return False
        pred = matches[-1]
        return pred == self.get_ground_truth(ground_truth)


class Regex5TimesMultipleChoiceSolutionChecker(RegexMultipleChoiceSolutionChecker):
    def __init__(self):
        self.pattern = r'\b([A-Z])\1{4}\b'


def get_solution_check_from_dataset_name(dataset_name: str) -> Any:
    """
    Retorna a lista de verificadores corretos para um determinado dataset.
    """
    if dataset_name in ["mmlu_pro", "knowledge", "math", "reasoning"]:
        return [MultipleChoiceSolutionChecker(), Regex5TimesMultipleChoiceSolutionChecker()]
    else:
        raise NotImplementedError(
            f"O verificador para o dataset '{dataset_name}' ainda não foi implementado.")

##############################################################
# 4. Métricas e 5. Amostragem de Pares
##############################################################
def compute_intermediate_metrics(examples: List[Dict[str, Any]]) -> None:
    n_examples = len(examples)
    if n_examples == 0:
        print("Nenhum exemplo para calcular métricas.")
        return
        
    n_all_correct = sum(
        all(g.get("is_correct") is True for g in ex.get("generated_responses", [])) for ex in examples
    )
    n_all_incorrect = sum(
        all(g.get("is_correct") is False for g in ex.get("generated_responses", [])) for ex in examples
    )
    n_some_correct = n_examples - n_all_correct - n_all_incorrect
    
    print(f"Total de exemplos: {n_examples}")
    print(f"{n_all_correct} de {n_examples} ({(100*n_all_correct/n_examples):.2f}%) das questões tiveram apenas respostas corretas.")
    print(f"{n_all_incorrect} de {n_examples} ({(100*n_all_incorrect/n_examples):.2f}%) das questões tiveram apenas respostas incorretas.")
    print(f"{n_some_correct} de {n_examples} ({(100*n_some_correct/n_examples):.2f}%) das questões tiveram respostas mistas.")

def sample_pairs(examples: List[Dict[str, Any]], max_pairs_per_question: int = 1) -> List[Dict[str, Any]]:
    pairs = []
    for example in examples:
        is_corrects = [answer.get("is_correct") for answer in example.get("generated_responses", [])]
        if not (True in is_corrects and False in is_corrects):
            continue

        correct = [answer for answer in example["generated_responses"] if answer["is_correct"] is True]
        incorrect = [answer for answer in example["generated_responses"] if answer["is_correct"] is False]

        new_pairs = []
        for correct_response in correct:
            for incorrect_response in incorrect:
                pair_base = {k: v for k, v in example.items() if k not in ["generated_responses", "question_id"]}
                
                model_name = correct_response.get("model") or (example["generated_responses"][0].get("model") if example["generated_responses"] else None)

                if random.random() < 0.5:
                    pair_base.update({
                        "response_model": model_name,
                        "response_A": correct_response["response"],
                        "response_B": incorrect_response["response"],
                        "label": "A>B",
                    })
                else:
                    pair_base.update({
                        "response_model": model_name,
                        "response_A": incorrect_response["response"],
                        "response_B": correct_response["response"],
                        "label": "B>A",
                    })
                
                unique_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, json.dumps(pair_base, sort_keys=True)))
                pair_with_id = {"pair_id": unique_id, "question_id": example["question_id"]}
                pair_with_id.update(pair_base)
                new_pairs.append(pair_with_id)

        random.shuffle(new_pairs)
        pairs.extend(new_pairs[:max_pairs_per_question])
    return pairs