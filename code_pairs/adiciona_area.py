import json

# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================
# 1. Coloque o nome do seu arquivo de entrada aqui
arquivo_entrada = 'data_code.jsonl'

# 2. Escolha o nome para o novo arquivo que será criado
arquivo_saida = 'code_area.jsonl'

# 3. Defina o valor padrão que será adicionado a todos os pares
valor_padrao_area = 'code'
# ==============================================================================


# --- O SCRIPT COMEÇA AQUI ---
def adicionar_area_padrao():
    """
    Função que lê o arquivo original e cria um novo
    adicionando o campo 'area' com um valor padrão em todas as linhas.
    Agora, ignora linhas vazias e comentários (iniciados com #).
    """
    print(f"Iniciando... Lendo de '{arquivo_entrada}'")
    
    contador_pares = 0
    contador_linhas_ignoradas = 0
    
    try:
        # Abre o arquivo de entrada para leitura e o de saída para escrita
        with open(arquivo_entrada, 'r', encoding='utf-8') as f_in, \
             open(arquivo_saida, 'w', encoding='utf-8') as f_out:
            
            # Usamos enumerate para saber o número da linha em caso de erro
            for num_linha, linha in enumerate(f_in, 1):
                
                # --- NOVA VERIFICAÇÃO ADICIONADA ---
                # Remove espaços em branco do início e fim da linha
                linha_limpa = linha.strip()
                
                # Se a linha estiver vazia ou for um comentário, pula para a próxima
                if not linha_limpa or linha_limpa.startswith('#'):
                    contador_linhas_ignoradas += 1
                    continue 
                # --- FIM DA VERIFICAÇÃO ---

                try:
                    # Tenta carregar a linha como um objeto JSON
                    par = json.loads(linha_limpa)
                    
                    # ADICIONA O CAMPO PADRÃO DIRETAMENTE
                    par['area'] = valor_padrao_area
                    
                    # Escreve o objeto modificado na nova linha do arquivo de saída
                    f_out.write(json.dumps(par, ensure_ascii=False) + '\n')
                    
                    contador_pares += 1

                except json.JSONDecodeError:
                    print(f"AVISO: Ignorando a linha {num_linha} por não ser um JSON válido.")
                    contador_linhas_ignoradas += 1


        print("-" * 50)
        print("Processamento concluído com sucesso!")
        print(f"Total de pares processados: {contador_pares}")
        print(f"Total de linhas ignoradas (vazias/comentários/inválidas): {contador_linhas_ignoradas}")
        print(f"Adicionado: '\"area\": \"{valor_padrao_area}\"' nas linhas válidas.")
        print(f"Novo arquivo salvo como: '{arquivo_saida}'")
        print("-" * 50)

    except FileNotFoundError:
        print(f"ERRO: O arquivo de entrada '{arquivo_entrada}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

# Executa a função principal
if __name__ == "__main__":
    adicionar_area_padrao()