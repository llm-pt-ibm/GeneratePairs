import argparse
from pathlib import Path

# Supondo que este script de teste está na mesma pasta (ou em uma pasta irmã)
# que o 'carregador_problema.py' e que o Python pode encontrá-lo.
from carregador_problema import carregar_problema_do_diretorio, ProblemaCodigo

def validar_carregador(caminho_do_problema: Path):
    """
    Função principal que executa a validação do carregador para um dado caminho.
    """
    print("\n--- Iniciando teste da função 'carregar_problema_do_diretorio' ---")
    
    # Verifica se o caminho fornecido existe e é um diretório
    if not caminho_do_problema.is_dir():
        print(f"❌ ERRO: O caminho fornecido não existe ou não é um diretório: '{caminho_do_problema}'")
        return

    print(f"Tentando carregar o problema de: {caminho_do_problema}")

    try:
        # 1. Chama a função que queremos testar com o caminho fornecido
        problema_carregado = carregar_problema_do_diretorio(caminho_do_problema)
        
        # 2. Verifica e imprime os resultados para validação visual
        print("\n✅ Problema carregado com sucesso! Verificando o conteúdo:")
        print("-" * 50)

        print(f"ID do Problema: {problema_carregado.id_problema}")
        print("-" * 50)
        print(f"Enunciado (início): {problema_carregado.enunciado.strip()}...")
        print("-" * 50)
        print(f"Solução de Referência (início): {problema_carregado.solucao_referencia.strip()}...")
        print("-" * 50)
        print(f"Número de Testes Encontrados: {len(problema_carregado.testes)}")
        print("-" * 50)

        for i in range(len(problema_carregado.testes)):
            print(f"Caso de Teste {i}: {problema_carregado.testes[i]}\n")

        # if problema_carregado.testes:
        #     print("\nExemplo do primeiro caso de teste carregado:")
        #     print(problema_carregado.testes[0])
        
        print("-" * 50)
        print("✅ Validação concluída com sucesso. A função parece estar funcionando corretamente!")

    except FileNotFoundError as e:
        print(f"\n❌ ERRO: Arquivo essencial não encontrado dentro do diretório.")
        print(f"   Verifique se o .yaml e o .java existem em '{caminho_do_problema}'.")
        print(f"   Detalhe do erro: {e}")
    except Exception as e:
        print(f"\n❌ ERRO: Ocorreu um erro inesperado durante o teste.")
        print(f"   Detalhe do erro: {e}")

if __name__ == "__main__":
    # Configura o parser para aceitar argumentos da linha de comando
    parser = argparse.ArgumentParser(
        description="Script de validação para a função 'carregar_problema_do_diretorio'.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    # Adiciona o argumento obrigatório para o caminho do problema
    parser.add_argument(
        "caminho_problema",
        type=str,
        help="O caminho para o diretório do problema que você deseja testar.\n"
             "Exemplo de uso:\n"
             "  python validar_carregador.py caminho/para/teorema_mestre"
    )

    args = parser.parse_args()
    
    # Converte a string do argumento para um objeto Path e chama a função de validação
    caminho_para_validar = Path(args.caminho_problema)
    validar_carregador(caminho_para_validar)
