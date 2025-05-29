import requests
import time
from scripts.utils_io import carregar_json, salvar_json
import os
from dotenv import load_dotenv
load_dotenv()

host = os.getenv("API_HOST", "http://localhost")
port = os.getenv("API_PORT", "5000")
route = "/llm/extract-keywords"
api_url = f"{host}:{port}{route}"

def chamar_api_para_keywords(title, abstract):
    """Faz a chamada para a API e retorna a lista de palavras-chave."""
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
    """Processa a lista, adiciona Palavras-chave LLM, e salva no arquivo JSON."""
    resultado = []

    tempo_inicio = time.time()  # Marca o tempo inicial

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
            tempo_decorrido = time.time() - tempo_inicio
            print(f"Progresso salvo até o documento: {i+1}")
            print(f"Tempo decorrido: {tempo_decorrido:.2f} segundos")

    # Salva o resultado final
    salvar_json(resultado, arquivo_saida_json)
    tempo_total = time.time() - tempo_inicio
    print(f"Processamento concluído. Tempo total: {tempo_total:.2f} segundos")

if __name__ == "__main__":

    # Execução
    dados = carregar_json('data/dados_completos.json')
    processar_lista_para_keywords(dados, 'data/keywords.json')
