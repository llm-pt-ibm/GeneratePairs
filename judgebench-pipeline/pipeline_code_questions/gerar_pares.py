import random
import logging
from typing import List, Dict, Any

# Importa as estruturas e funções dos outros módulos do nosso pipeline
from carregador_problema import ProblemaCodigo
from gerador_mutantes import gerar_mutantes_com_llm
from executor_codigo import verificar_solucao

def criar_pares_de_codigo(
    problema: ProblemaCodigo, 
    num_mutantes: int, 
    max_pares: int
) -> List[Dict[str, Any]]:
    """
    Orquestra todo o pipeline: gera mutantes, os verifica e monta os pares de preferência.

    Args:
        problema: O objeto ProblemaCodigo com os dados da questão.
        num_mutantes: O número de mutantes a serem gerados pela IA.
        max_pares: O número máximo de pares a serem salvos para esta questão.

    Returns:
        Uma lista de dicionários, onde cada dicionário é um par de preferência.
    """
    logging.info(f"Iniciando a criação de pares para o problema: '{problema.id_problema}'")

    # 1. Verifica a solução de referência para garantir que ela é a base correta.
    resultado_original = verificar_solucao(problema.solucao_referencia, problema.testes)
    if not resultado_original.passou:
        logging.warning(
            f"A solução de referência para '{problema.id_problema}' FALHOU nos testes. "
            "Nenhum par será gerado para este problema."
        )
        return []
    
    solucao_correta = problema.solucao_referencia
    logging.info("Solução de referência verificada com sucesso.")

    # 2. Gera os candidatos a respostas incorretas usando o LLM.
    mutantes_candidatos = gerar_mutantes_com_llm(problema, num_mutantes)
    if not mutantes_candidatos:
        logging.warning(f"Nenhum mutante foi gerado para '{problema.id_problema}'. Nenhum par será gerado.")
        return []

    # 3. Verifica cada mutante e coleta apenas os que falham nos testes.
    solucoes_incorretas = []
    for i, mutante in enumerate(mutantes_candidatos):
        logging.info(f"Verificando mutante {i+1}/{len(mutantes_candidatos)}...")
        resultado_mutante = verificar_solucao(mutante, problema.testes)
        if not resultado_mutante.passou:
            solucoes_incorretas.append(mutante)
        else:
            logging.warning(f"Mutante equivalente (passou nos testes) encontrado e descartado para '{problema.id_problema}'.")

    if not solucoes_incorretas:
        logging.warning(f"Nenhum dos mutantes gerados falhou nos testes. Nenhum par será gerado.")
        return []

    logging.info(f"Encontradas {len(solucoes_incorretas)} soluções incorretas válidas após verificação.")

    # 4. Monta os pares finais.
    pares_criados = []
    for solucao_incorreta in solucoes_incorretas:
        # Sorteia aleatoriamente a ordem (A/B) para evitar viés no treinamento futuro.
        if random.random() < 0.5:
            resposta_A = solucao_correta
            resposta_B = solucao_incorreta
            label = "A>B"
        else:
            resposta_A = solucao_incorreta
            resposta_B = solucao_correta
            label = "B>A"
        
        par = {
            "problem_id": problema.id_problema,
            "prompt": problema.enunciado,
            "response_A": resposta_A,
            "response_B": resposta_B,
            "label": label
        }
        pares_criados.append(par)

    # 5. Embaralha e limita o número de pares conforme solicitado.
    random.shuffle(pares_criados)
    pares_finais = pares_criados[:max_pares]
    
    logging.info(f"Criados e selecionados {len(pares_finais)} pares de preferência para '{problema.id_problema}'.")
    return pares_finais
