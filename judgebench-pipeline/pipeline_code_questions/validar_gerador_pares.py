import argparse
import logging
from pathlib import Path
import sys
import os

# --- Adiciona o diretório raiz ao path para resolver importações ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# --- Fim ---

from carregador_problema import carregar_problema_do_diretorio
from gerar_pares import criar_pares_de_codigo

def validar_gerador_de_pares(caminho_do_problema: Path, num_mutantes: int, max_pares: int):
    """
    Função principal para testar o pipeline completo de criação de pares.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    print("\n--- Iniciando teste do 'gerador_pares.py' (Pipeline Completo) ---")

    try:
        # Etapa 1: Carregar o problema.
        logging.info(f"Carregando o problema de '{caminho_do_problema}'...")
        problema = carregar_problema_do_diretorio(caminho_do_problema)
        logging.info("Problema carregado com sucesso.")

        # Etapa 2: Chamar a função principal para criar os pares.
        # Esta função irá orquestrar a geração de mutantes e a verificação internamente.
        logging.info(f"Iniciando a criação de pares com num_mutantes={num_mutantes} e max_pares={max_pares}...")
        pares_gerados = criar_pares_de_codigo(problema, num_mutantes, max_pares)

        # Etapa 3: Validar a saída.
        print("\n--- Validação do Resultado ---")
        if not pares_gerados:
            print("⚠️ ATENÇÃO: Nenhum par foi gerado.")
            print("   Isso pode ser normal se nenhum mutante válido foi encontrado, ou pode indicar um problema.")
            print("   Verifique os logs acima para mais detalhes.")
            return

        print(f"✅ SUCESSO: Foram gerados {len(pares_gerados)} pares de preferência.")
        print("Abaixo está um exemplo do primeiro par gerado:")
        print("-" * 50)

        primeiro_par = pares_gerados[0]
        print(f"  ID do Problema: {primeiro_par.get('problem_id')}")
        print(f"  Rótulo (Label): {primeiro_par.get('label')}")
        print(f"  Início da Resposta A: {primeiro_par.get('response_A', '')}...")
        print(f"  Início da Resposta B: {primeiro_par.get('response_B', '')}...")
        
        print("-" * 50)
        print("✅ Validação concluída com sucesso!")

    except Exception as e:
        print(f"\n❌ ERRO: Ocorreu um erro inesperado durante o teste do gerador de pares.")
        logging.error(f"Detalhe do erro: {e}", exc_info=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script de validação para a função 'criar_pares_de_preferencia'.",
    )
    
    parser.add_argument(
        "caminho_problema",
        type=str,
        help="O caminho para o diretório do problema a ser usado. Ex: teorema_mestre"
    )
    parser.add_argument(
        "--num_mutantes",
        type=int,
        default=5,
        help="Número de mutantes a serem solicitados ao LLM. Padrão: 5"
    )
    parser.add_argument(
        "--max_pares",
        type=int,
        default=2,
        help="Número máximo de pares a serem retornados. Padrão: 2"
    )

    args = parser.parse_args()
    caminho = Path(args.caminho_problema)
    validar_gerador_de_pares(caminho, args.num_mutantes, args.max_pares)
