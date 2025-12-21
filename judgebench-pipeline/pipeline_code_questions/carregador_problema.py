import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Any

# Define uma estrutura de dados para carregar as informações do problema.
# Isso torna o código mais limpo e seguro do que usar dicionários.
@dataclass
class ProblemaCodigo:
    id_problema: str
    enunciado: str
    solucao_referencia: str
    testes: List[Dict[str, Any]]

def carregar_problema_do_diretorio(caminho_do_diretorio: Path) -> ProblemaCodigo:
    """
    Carrega todas as informações de um problema de código a partir de um diretório.

    A função agora é genérica e espera encontrar:
    1. Um arquivo .yaml com o mesmo nome do diretório.
    2. Exatamente um arquivo .java com a solução de referência.

    Args:
        caminho_do_diretorio: O objeto Path para a pasta do problema (ex: .../teorema_mestre).

    Returns:
        Um objeto ProblemaCodigo contendo todos os dados do problema.

    Raises:
        FileNotFoundError: Se os arquivos .yaml ou .java não forem encontrados.
        Exception: Se houver mais de um arquivo .java no diretório.
    """
    id_problema = caminho_do_diretorio.name

    # --- MELHORIA 1: Nome do arquivo YAML dinâmico ---
    # O nome do arquivo .yaml deve ser o mesmo nome da pasta.
    arquivo_yaml = caminho_do_diretorio / f"{id_problema}.yaml"
    if not arquivo_yaml.exists():
        raise FileNotFoundError(f"Arquivo YAML necessário não encontrado: {arquivo_yaml}")

    # --- MELHORIA 2: Busca pelo arquivo Java de forma flexível ---
    # Procura por qualquer arquivo que termine com .java no diretório.
    arquivos_java = list(caminho_do_diretorio.glob("*.java"))
    if not arquivos_java:
        raise FileNotFoundError(f"Nenhum arquivo .java de solução encontrado em: {caminho_do_diretorio}")
    if len(arquivos_java) > 1:
        raise Exception(f"Múltiplos arquivos .java encontrados em {caminho_do_diretorio}. Apenas um é permitido.")
    
    arquivo_java = arquivos_java[0]

    # Carrega o conteúdo do arquivo YAML
    with open(arquivo_yaml, 'r', encoding='utf-8') as f:
        dados_problema = yaml.safe_load(f)
    
    # Carrega o código da solução de referência
    with open(arquivo_java, 'r', encoding='utf-8') as f:
        codigo_solucao = f.read()

    # Extrai as informações e as coloca na nossa estrutura de dados
    enunciado = dados_problema.get("text", "")
    testes = dados_problema.get("tests", [])

    return ProblemaCodigo(
        id_problema=id_problema,
        enunciado=enunciado,
        solucao_referencia=codigo_solucao,
        testes=testes
    )


