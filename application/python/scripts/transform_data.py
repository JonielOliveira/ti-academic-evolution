from datetime import datetime
from scripts.utils_io import carregar_json, salvar_json

def extrair_ano_e_decada(data_str):
    try:
        ano = datetime.strptime(data_str, '%Y-%m-%d').year
        decada = ano // 10 * 10
        return ano, decada
    except:
        return None, None

def processar_dados_complementares(dados, keywords, arquivo_saida_json):

    # Constrói um dicionário para acesso rápido às palavras-chave por link
    mapa_keywords = {
        k["Link de Acesso"]: k.get("Palavras-chave LLM", [])
        for k in keywords
    }

    novos_dados = []
    for item in dados:
        novo = item.copy()

        data_defesa = item.get("Data de Defesa", "")
        ano, decada = extrair_ano_e_decada(data_defesa)
        novo["Ano de Defesa"] = ano if ano else "indisponível"
        novo["Década"] = decada if decada else "indisponível"

        link_arquivo = item.get("Arquivo Link", "")
        novo["Arquivo Disponível"] = (bool(link_arquivo.strip()) and link_arquivo.strip() != "indisponível")

        # Adiciona Palavras-chave LLM se o link de acesso estiver mapeado
        link_acesso = item.get("Link de Acesso", "").strip()
        if link_acesso in mapa_keywords:
            novo["Palavras-chave LLM"] = mapa_keywords[link_acesso]
        else:
            novo["Palavras-chave LLM"] = ["indisponível"]
        
        novos_dados.append(novo)

    # Salva o resultado em arquivo
    salvar_json(novos_dados, arquivo_saida_json)


if __name__ == "__main__":
    
    # Execução principal
    entrada = 'data/dados_completos.json'
    saida = 'data/dados_ajustados.json'

    dados = carregar_json(entrada)
    dados_enriquecidos = processar_dados_complementares(dados, saida)
