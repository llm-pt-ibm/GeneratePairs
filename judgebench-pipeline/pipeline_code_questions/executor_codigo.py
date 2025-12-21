import subprocess
import tempfile
import logging
import re  # Importa a biblioteca de Expressões Regulares
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Any

# A estrutura de dados para o resultado permanece a mesma
@dataclass
class ResultadoExecucao:
    passou: bool
    status: str
    detalhes: str

def _encontrar_classe_principal(codigo_fonte: str) -> str:
    """
    Usa Regex para encontrar o nome da classe que contém o método main.
    """
    # Procura por um padrão como: class NomeDaClasse { ... public static void main ... }
    # O re.DOTALL faz com que o '.' também corresponda a quebras de linha.
    padrao = re.compile(r"class\s+([A-Za-z0-9_]+)\s*\{.*public\s+static\s+void\s+main", re.DOTALL)
    match = padrao.search(codigo_fonte)
    if match:
        return match.group(1) # Retorna o primeiro grupo capturado (o nome da classe)
    return None

def verificar_solucao(codigo_fonte: str, testes: List[Dict[str, Any]], timeout_segundos: int = 5) -> ResultadoExecucao:
    """
    Verifica uma solução em Java, agora descobrindo dinamicamente a classe principal.
    """
    # --- MELHORIA: Descobrir o nome da classe principal ---
    nome_classe_principal = _encontrar_classe_principal(codigo_fonte)
    if not nome_classe_principal:
        return ResultadoExecucao(
            passou=False,
            status="Erro de Estrutura",
            detalhes="Não foi possível encontrar uma classe com o método 'public static void main'."
        )

    with tempfile.TemporaryDirectory() as tmpdir:
        dir_path = Path(tmpdir)
        # Salva o arquivo .java com o nome correto da classe encontrada
        arquivo_java = dir_path / f"{nome_classe_principal}.java"

        with open(arquivo_java, "w", encoding="utf-8") as f:
            f.write(codigo_fonte)

        # --- Etapa 1: Compilação ---
        try:
            resultado_compilacao = subprocess.run(
                ["javac", str(arquivo_java)],
                capture_output=True, text=True, timeout=timeout_segundos
            )
            if resultado_compilacao.returncode != 0:
                return ResultadoExecucao(
                    passou=False,
                    status="Erro de compilação",
                    detalhes=resultado_compilacao.stderr
                )
        except subprocess.TimeoutExpired:
            return ResultadoExecucao(
                passou=False, status="Timeout durante a compilação",
                detalhes=f"A compilação excedeu {timeout_segundos} segundos."
            )

        # --- Etapa 2: Execução dos Testes ---
        for i, teste in enumerate(testes):
            entrada_teste = teste.get("input", "")
            saida_esperada = teste.get("output", "")

            try:
                # Executa o .class usando o nome da classe que descobrimos
                resultado_execucao = subprocess.run(
                    ["java", nome_classe_principal],
                    capture_output=True, text=True, input=entrada_teste,
                    cwd=dir_path,
                    timeout=timeout_segundos
                )

                if resultado_execucao.returncode != 0:
                    return ResultadoExecucao(
                        passou=False, status=f"Erro de execução no teste {i+1}",
                        detalhes=resultado_execucao.stderr
                    )

                if resultado_execucao.stdout.strip() != saida_esperada.strip():
                    return ResultadoExecucao(
                        passou=False, status=f"Saída incorreta no teste {i+1}",
                        detalhes=f"Esperado: '{saida_esperada.strip()}'\nRecebido: '{resultado_execucao.stdout.strip()}'"
                    )

            except subprocess.TimeoutExpired:
                return ResultadoExecucao(
                    passou=False, status=f"Timeout no teste {i+1}",
                    detalhes=f"A execução excedeu {timeout_segundos} segundos."
                )

    return ResultadoExecucao(
        passou=True,
        status=f"Compilado e passou em {len(testes)} testes",
        detalhes=""
    )