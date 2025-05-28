import json
import requests
import os

def get_file_path(filename):
    """Retorna o caminho absoluto de um arquivo localizado na mesma pasta do script .py."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, filename)


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


def chamar_api_para_keywords(title, abstract, api_url='http://localhost:5000/llm/extract-keywords'):
    """
    Faz a chamada para a API e retorna a lista de palavras-chave.
    """
    payload = {
        "title": title,
        "abstract": abstract
    }
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("keywords", ["indisponível"])
    except Exception as e:
        print(f"Erro ao chamar API: {e}")
        return ["indisponível"]

def processar_lista_para_keywords(lista_objetos, arquivo_saida_json):
    """
    Processa a lista, adiciona Palavras-chave LLM, e salva no arquivo JSON.
    """
    resultado = []

    for i, item in enumerate(lista_objetos):
        palavras_chave = ["indisponível"]

        # Prepara dados
        titulo_pt = item.get("Título em português", "").lower()
        resumo_pt = item.get("Resumo em português", "").lower()
        titulo_en = item.get("Título em inglês", "").lower()
        resumo_en = item.get("Resumo em inglês", "").lower()

        # Define função auxiliar
        def valido(texto):
            return texto and texto not in ["indisponível", "não consta", "not available"]

        # Escolhe título e resumo válidos
        if valido(titulo_pt) and valido(resumo_pt):
            title = item["Título em português"]
            abstract = item["Resumo em português"]
        elif valido(titulo_en) and valido(resumo_en):
            title = item["Título em inglês"]
            abstract = item["Resumo em inglês"]
        else:
            title = None
            abstract = None

        # Se tiver dados válidos, chama API
        if title and abstract:
            palavras_chave = chamar_api_para_keywords(title, abstract)

        resultado.append({
            "Link de Acesso": item.get("Link de Acesso", "indisponível"),
            "Palavras-chave LLM": palavras_chave
        })
        
        if (i + 1) % 10 == 0:
            salvar_json(resultado, arquivo_saida_json)
            print(f"Progresso salvo até o documento: {i+1}")

    # Salva o resultado
    salvar_json(resultado, arquivo_saida_json)

dados = carregar_json('data/dados_amostra.json')
processar_lista_para_keywords(dados, 'data/keywords.json')
