from datetime import datetime
from utils_io import carregar_json, salvar_json

def extrair_ano_e_decada(data_str):
    try:
        ano = datetime.strptime(data_str, '%Y-%m-%d').year
        decada = ano // 10 * 10
        return ano, decada
    except:
        return None, None

def processar_dados_complementares(dados):
    novos_dados = []
    for item in dados:
        novo = item.copy()

        data_defesa = item.get("Data de Defesa", "")
        ano, decada = extrair_ano_e_decada(data_defesa)
        novo["Ano de Defesa"] = ano if ano else "indisponível"
        novo["Década"] = decada if decada else "indisponível"

        link_arquivo = item.get("Arquivo Link", "")
        novo["Arquivo Disponível"] = (bool(link_arquivo.strip()) and link_arquivo.strip() != "indisponível")

        novos_dados.append(novo)
    return novos_dados

# Execução principal
entrada = 'data/dados_completos.json'
saida = 'data/dados_ajustados.json'

dados = carregar_json(entrada)
dados_enriquecidos = processar_dados_complementares(dados)
salvar_json(dados_enriquecidos, saida)
