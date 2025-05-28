from utils_io import carregar_json, salvar_json
from extract_data import extrair_dados_iniciais, extrair_dados_lote, verificar_completude_json
from transform_data import processar_dados_complementares


extrair_dados_iniciais('config/sample_sources.json', 'sample/dados_iniciais.json')

template = carregar_json('config/template.json')
extrair_dados_lote(template, 'sample/dados_iniciais.json','sample/dados_completos.json')

dados = carregar_json('sample/dados_completos.json')
verificar_completude_json(dados, template)

dados_enriquecidos = processar_dados_complementares(dados, 'sample/dados_ajustados.json')
