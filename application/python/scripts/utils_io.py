import json
import os

def get_file_path(filename):
    """Retorna o caminho absoluto de um arquivo, relativo à raiz da aplicação (onde está app.py)."""
    # Caminho absoluto do app.py
    app_root = os.path.dirname(os.path.abspath(__file__))  # /scripts
    root_dir = os.path.abspath(os.path.join(app_root, ".."))  # volta para a raiz da aplicação
    return os.path.join(root_dir, filename)


def carregar_json(arquivo_json):
    """
    Carrega e retorna o conteúdo de um arquivo JSON.

    Parâmetros:
    - arquivo_json (str): nome do arquivo JSON.

    Retorna:
    - O conteúdo carregado (normalmente um dict ou list).
    """
    try:
        with open(get_file_path(arquivo_json), 'r', encoding='utf-8') as f:
            conteudo = json.load(f)
        return conteudo
    except Exception as e:
        print(f"Erro ao ler o arquivo JSON '{arquivo_json}': {e}")
        return None


def salvar_json(conteudo, arquivo_json):
    """
    Salva o conteúdo fornecido em um arquivo JSON.

    Parâmetros:
    - conteudo: objeto Python (dict, list, etc.) a ser salvo.
    - arquivo_json (str): nome do arquivo JSON de destino.

    Retorna:
    - None.
    """
    try:
        with open(get_file_path(arquivo_json), 'w', encoding='utf-8') as f:
            json.dump(conteudo, f, ensure_ascii=False, indent=4)
        print(f"Arquivo JSON salvo com sucesso: {arquivo_json}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo JSON '{arquivo_json}': {e}")
