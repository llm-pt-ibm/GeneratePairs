import json
import argparse
from pathlib import Path
import uuid

def formatar_pares_de_codigo(
    arquivo_entrada: Path, 
    arquivo_saida: Path, 
    nome_modelo: str
):
    """
    Lê um arquivo .jsonl de pares de código, ajusta os campos conforme
    o formato desejado e salva em um novo arquivo.

    Ações:
    - Renomeia 'problem_id' para 'source'.
    - Adiciona 'response_model'.
    - Gera um novo 'pair_id'.
    """
    print(f"Processando '{arquivo_entrada}' para gerar '{arquivo_saida}'...")
    pares_formatados = []
    
    with open(arquivo_entrada, 'r', encoding='utf-8') as f:
        for linha in f:
            try:
                par_original = json.loads(linha)
                
                # Monta o novo par com a estrutura simplificada desejada
                par_formatado = {
                    "pair_id": str(uuid.uuid4()),
                    "source": par_original.get("problem_id"), # Renomeia o campo
                    "prompt": par_original.get("prompt"),
                    "response_model": nome_modelo,
                    "response_A": par_original.get("response_A"),
                    "response_B": par_original.get("response_B"),
                    "label": par_original.get("label"),
                }
                pares_formatados.append(par_formatado)
                
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Aviso: Pulando linha com erro ou formato inesperado: {linha.strip()}. Erro: {e}")

    # Salva todos os pares formatados no arquivo de saída
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        for par in pares_formatados:
            f.write(json.dumps(par, ensure_ascii=False) + '\n')
            
    print(f"🎉 Sucesso! {len(pares_formatados)} pares foram reformatados e salvos em '{arquivo_saida}'.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Formata um arquivo .jsonl de pares de código adicionando e renomeando campos.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "input_file",
        type=str,
        help="Caminho para o arquivo .jsonl de pares de código a ser processado."
    )
    parser.add_argument(
        "output_file",
        type=str,
        help="Caminho para o novo arquivo .jsonl de saída que será criado."
    )
    parser.add_argument(
        "--model_name",
        type=str,
        default="gpt-4o",
        help="Nome do modelo a ser adicionado no campo 'response_model'.\nPadrão: 'gpt-4o'"
    )
    
    args = parser.parse_args()
    
    # Cria o diretório de saída, se não existir
    Path(args.output_file).parent.mkdir(parents=True, exist_ok=True)
    
    formatar_pares_de_codigo(
        arquivo_entrada=Path(args.input_file),
        arquivo_saida=Path(args.output_file),
        nome_modelo=args.model_name
    )