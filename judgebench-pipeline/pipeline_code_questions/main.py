import argparse
import logging
from pathlib import Path
import json

# Importações dos nossos módulos do pipeline
from carregador_problema import carregar_problema_do_diretorio
from gerar_pares import criar_pares_de_codigo

def acrescentar_ao_jsonl(caminho_arquivo: Path, novos_dados: list):
    """
    Acrescenta uma lista de dicionários ao final de um arquivo .jsonl.
    Abre o arquivo no modo 'a' (append) para garantir a persistência.
    """
    with open(caminho_arquivo, 'a', encoding='utf-8') as f:
        for item in novos_dados:
            json_line = json.dumps(item, ensure_ascii=False)
            f.write(json_line + '\n')

def carregar_ids_processados(caminho_arquivo: Path) -> set:
    """
    Lê um arquivo .jsonl existente e retorna um conjunto com os IDs dos problemas
    que já foram processados para evitar trabalho duplicado.
    """
    ids_processados = set()
    if not caminho_arquivo.exists():
        return ids_processados
    
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                if "problem_id" in data:
                    ids_processados.add(data["problem_id"])
            except json.JSONDecodeError:
                logging.warning(f"Linha mal formada encontrada e ignorada em {caminho_arquivo}: {line.strip()}")
    return ids_processados

def processar_diretorio_de_problemas(
    caminho_dados: Path, 
    caminho_saida: Path,
    num_mutantes: int,
    max_pares: int
):
    """
    Processa um diretório contendo pastas de problemas, salvando o progresso
    incrementalmente e pulando problemas já processados.
    """
    logging.info("--- INICIANDO PIPELINE DE GERAÇÃO DE PARES ---")
    
    # Carrega os IDs dos problemas que já estão no arquivo de saída
    ids_processados = carregar_ids_processados(caminho_saida)
    if ids_processados:
        logging.info(f"Encontrados {len(ids_processados)} problemas já processados no arquivo de saída. Eles serão pulados.")

    diretorios_problemas = [d for d in caminho_dados.iterdir() if d.is_dir()]
    if not diretorios_problemas:
        logging.warning(f"Nenhum diretório de problema encontrado em '{caminho_dados}'.")
        return

    total_problemas = len(diretorios_problemas)
    novos_pares_gerados = 0
    
    for i, dir_problema in enumerate(diretorios_problemas):
        id_problema = dir_problema.name
        logging.info(f"\n--- Verificando Problema {i+1}/{total_problemas}: {id_problema} ---")

        if id_problema in ids_processados:
            logging.info(f"Problema '{id_problema}' já foi processado. Pulando.")
            continue
        
        try:
            problema = carregar_problema_do_diretorio(dir_problema)
            pares = criar_pares_de_codigo(problema, num_mutantes, max_pares)
            if pares:
                acrescentar_ao_jsonl(caminho_saida, pares)
                logging.info(f"✅ Sucesso! {len(pares)} pares para '{id_problema}' foram salvos em '{caminho_saida}'.")
                novos_pares_gerados += len(pares)
        except Exception as e:
            logging.error(f"Falha ao processar o problema '{id_problema}': {e}", exc_info=True)

    logging.info("\n--- PIPELINE FINALIZADO ---")
    if novos_pares_gerados > 0:
        logging.info(f"✅ {novos_pares_gerados} novos pares foram adicionados ao arquivo de saída.")
    else:
        logging.warning("Nenhum novo par foi gerado nesta execução.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser(
        description="Pipeline para gerar pares de preferência para problemas de código com persistência.",
    )
    
    parser.add_argument(
        "--data_dir",
        type=str,
        default="questions",
        help="O caminho para o diretório que contém as pastas dos problemas. Padrão: 'questions'"
    )
    parser.add_argument(
        "--output_file",
        type=str,
        default="saidas/pares.jsonl",
        help="O caminho para o arquivo de saída .jsonl. Padrão: 'saidas/pares.jsonl'"
    )
    parser.add_argument(
        "--num_mutants",
        type=int,
        default=5,
        help="Número de mutantes a serem solicitados ao LLM por problema. Padrão: 10"
    )
    parser.add_argument(
        "--max_pairs",
        type=int,
        default=1,
        help="Número máximo de pares a serem salvos por problema. Padrão: 5"
    )

    args = parser.parse_args()
    
    Path(args.output_file).parent.mkdir(parents=True, exist_ok=True)
    
    processar_diretorio_de_problemas(
        caminho_dados=Path(args.data_dir),
        caminho_saida=Path(args.output_file),
        num_mutantes=args.num_mutants,
        max_pares=args.max_pairs
    )

