import argparse
import logging
from pathlib import Path
import sys
import os


from carregador_problema import carregar_problema_do_diretorio
from gerador_mutantes import gerar_mutantes_com_llm
from executor_codigo import verificar_solucao

def validar_executor(caminho_do_problema: Path):
    """
    Função principal para testar a verificação funcional de códigos.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    print("\n--- Iniciando teste do 'executor_codigo.py' ---")

    try:
        # --- ETAPA 1: Carregar o Problema ---
        print(f"\n[ETAPA 1/4] Carregando o problema de '{caminho_do_problema}'...")
        problema = carregar_problema_do_diretorio(caminho_do_problema)
        print("Problema carregado.")

        # --- ETAPA 2: Testar a Solução Correta (Original) ---
        print("\n[ETAPA 2/4] Verificando a solução original e correta...")
        resultado_original = verificar_solucao(problema.solucao_referencia, problema.testes)

        print(f"Resultado: {resultado_original.status}")
        if resultado_original.passou:
            print("✅ SUCESSO: A solução original passou nos testes, como esperado.")
        else:
            print("❌ FALHA: A solução original falhou nos testes. Verifique a solução ou os testes.")
            print(f"   Detalhes: {resultado_original.detalhes}")
            return # Interrompe o teste se a base não estiver correta

        # --- ETAPA 3: Gerar Mutantes para Testar o Caso de Falha ---
        print("\n[ETAPA 3/4] Gerando 5 mutantes para testar o cenário de falha...")
        mutantes = gerar_mutantes_com_llm(problema, num_mutantes=5)
        if not mutantes:
            print("❌ FALHA: Nenhum mutante foi gerado. Verifique a API ou o 'gerador_mutantes.py'.")
            return
        print(f"{len(mutantes)} mutantes gerados.")

        # --- ETAPA 4: Testar as Soluções Incorretas (Mutantes) ---
        print("\n[ETAPA 4/4] Verificando as soluções mutantes (espera-se que falhem)...")
        todos_mutantes_falharam = True
        for i, mutante in enumerate(mutantes):
            print(f"\n--- Verificando Mutante {i + 1} ---")
            resultado_mutante = verificar_solucao(mutante, problema.testes)
            print(f"Resultado: {resultado_mutante.status}")
            
            if not resultado_mutante.passou:
                print(f"✅ SUCESSO: O mutante {i+1} falhou, como esperado.")
                # ACRESCENTADO: Exibe os detalhes da falha (Ex: Saída esperada vs. recebida)
                print(f"   Detalhes da falha: {resultado_mutante.detalhes}")
            else:
                print(f"❌ FALHA: O mutante {i+1} passou nos testes, o que não era esperado (mutante equivalente).")
                todos_mutantes_falharam = False

        print("-" * 50)
        if todos_mutantes_falharam:
            print("✅ Validação do executor concluída com sucesso!")
            print("   O sistema conseguiu diferenciar corretamente a solução original dos mutantes.")
        else:
            print("⚠️ Validação do executor concluída com problemas.")
            print("   Um ou mais mutantes passaram nos testes.")

    except Exception as e:
        print(f"\n❌ ERRO: Ocorreu um erro inesperado durante o teste do executor.")
        print(f"   Detalhe: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script de validação para a função 'verificar_solucao' do executor de código.",
    )
    
    parser.add_argument(
        "caminho_problema",
        type=str,
        help="O caminho para o diretório do problema a ser usado nos testes. Ex: teorema_mestre"
    )

    args = parser.parse_args()
    caminho = Path(args.caminho_problema)
    validar_executor(caminho)

