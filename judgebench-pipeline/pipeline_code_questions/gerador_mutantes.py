import json
import logging
from typing import List

import openai

# Importa as estruturas e configurações que definimos
from carregador_problema import ProblemaCodigo
from config import OPENAI_API_KEY, MUTATION_MODEL

def gerar_mutantes_com_llm(problema: ProblemaCodigo, num_mutantes: int) -> List[str]:
    """
    Usa um Modelo de Linguagem Grande (LLM) para gerar versões mutantes e 
    provavelmente incorretas de uma solução de referência correta.

    Justificativa para o TCC: Esta abordagem é justificada por sua capacidade de
    criar bugs semanticamente relevantes que um humano poderia cometer, fornecendo
    um dataset mais desafiador e realista para treinamento e avaliação.

    Args:
        problema: O objeto ProblemaCodigo contendo a solução de referência.
        num_mutantes: O número de versões mutantes a serem geradas.

    Returns:
        Uma lista de strings, onde cada string é um código-fonte completo e mutante.
    """
    logging.info(f"Gerando {num_mutantes} mutantes para o problema '{problema.id_problema}' usando {MUTATION_MODEL}...")

    if not OPENAI_API_KEY or OPENAI_API_KEY == "SUA_CHAVE_API_AQUI":
        logging.error("A chave da API da OpenAI não está configurada em config.py. A geração de mutantes será pulada.")
        return []

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    # Um prompt detalhado para guiar o LLM a criar mutações úteis.
    # Esta é uma parte chave da metodologia para o seu TCC.
    prompt = f"""
    Você é um especialista em Teste de Mutação de Software. Sua tarefa é atuar como um 'motor de mutação'.
    Eu vou fornecer um código-fonte em Java que resolve um problema corretamente.

    Sua missão: Gerar {num_mutantes} versões alternativas deste código. Cada versão deve conter 
    **um único e sutil bug** que faça o programa falhar em alguns casos de teste. O código mutante 
    deve, sempre que possível, ser sintaticamente correto e compilar com sucesso.

    Para introduzir os bugs, inspire-se nos seguintes tipos de operadores de mutação:
    - Troca de Operador Relacional: Substitua >, <, >=, <=, ==, !=.
    - Erro Off-By-One: Altere os limites de um laço ou a indexação de um array.
    - Troca de Operador Aritmético: Substitua + por -.
    - Modificação de Constante: Altere um valor numérico literal.

    **Importante:** Não adicione nenhum comentário ou anotação no código mutante que explique a alteração que você fez. O código deve parecer natural, como se tivesse sido escrito por um humano sem perceber o erro.

    Formato da Saída: Responda com um único objeto JSON. O objeto deve ter uma única chave, "mutants",
    que é uma lista de strings. Cada string na lista deve ser o código-fonte completo de um mutante.

    Código-Fonte Original e Correto:
    ```java
    {problema.solucao_referencia}
    
    """

    try:
        response = client.chat.completions.create(
            model=MUTATION_MODEL,
            messages=[
                {"role": "system", "content": "Você é um especialista em Teste de Mutação de Software e responderá no formato JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.5, # Um pouco de criatividade é útil para mutantes variados
        )
        
        response_content = response.choices[0].message.content
        mutants_json = json.loads(response_content)
        
        mutants = mutants_json.get("mutants", [])
        if not isinstance(mutants, list) or not all(isinstance(m, str) for m in mutants):
            raise ValueError("A resposta do LLM para 'mutants' não é uma lista de strings.")
            
        logging.info(f"Gerados {len(mutants)} mutantes com sucesso.")
        return mutants

    except Exception as e:
        logging.error(f"Falha ao gerar mutantes devido a um erro na API ou resposta inválida: {e}")
        return []