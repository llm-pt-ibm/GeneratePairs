import argparse
import logging
from pathlib import Path

# Importa as funções que vamos testar e suas dependências
from carregador_problema import carregar_problema_do_diretorio
from gerador_mutantes import gerar_mutantes_com_llm

def validar_gerador(caminho_do_problema: Path, num_mutantes: int):
    """
    Função principal para testar a geração de mutantes com IA.
    """
    # Configura o logging para vermos as mensagens de status do processo
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    print("\n--- Iniciando teste do 'gerador_mutantes.py' ---")

    try:
        # Etapa 1: Carregar os dados do problema.
        # Esta parte já foi validada e sabemos que funciona.
        print(f"\n[ETAPA 1/3] Carregando o problema de '{caminho_do_problema}'...")
        problema = carregar_problema_do_diretorio(caminho_do_problema)
        print("Problema carregado com sucesso.")

        # Etapa 2: Chamar a função para gerar os mutantes.
        # Esta é a função que estamos testando agora.
        print(f"\n[ETAPA 2/3] Solicitando {num_mutantes} mutantes ao LLM. Isso pode levar um momento...")
        mutantes_gerados = gerar_mutantes_com_llm(problema, num_mutantes)

        # Etapa 3: Validar e exibir os resultados.
        print("\n[ETAPA 3/3] Validando a saída do gerador de mutantes...")
        if not mutantes_gerados:
            print("\n❌ ERRO: A lista de mutantes retornou vazia.")
            print("   Verifique se a chave da API está correta em 'config.py' e se não houve erros de rede.")
            return

        print("-" * 50)
        print(f"✅ Geração concluída! Foram retornados {len(mutantes_gerados)} mutantes.")
        print("Abaixo estão os mutantes gerados para inspeção visual:")
        print("-" * 50)

        for i, mutante in enumerate(mutantes_gerados):
            print(f"\n--- Mutante {i + 1} ---")
            print(mutante)
            print("-" * 20)

        print("\n✅ Validação concluída. Verifique visualmente se os códigos acima são diferentes da solução original.")

    except Exception as e:
        print(f"\n❌ ERRO: Ocorreu um erro inesperado durante o teste do gerador.")
        print(f"   Detalhe: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script de validação para a função 'gerar_mutantes_com_llm'.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "caminho_problema",
        type=str,
        help="O caminho para o diretório do problema a ser usado como base para a mutação.\n"
             "Exemplo: teorema_mestre"
    )

    parser.add_argument(
        "--num_mutantes",
        type=int,
        default=3,
        help="O número de mutantes que você quer solicitar ao LLM.\n"
             "Padrão: 3"
    )

    args = parser.parse_args()
    
    caminho = Path(args.caminho_problema)
    validar_gerador(caminho, args.num_mutantes)