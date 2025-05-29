from utils_io import carregar_json, salvar_json
from extract_data import extrair_dados_iniciais, extrair_dados_lote, verificar_completude_json
from keyword_inferencer import processar_lista_para_keywords
from transform_data import processar_dados_complementares
import os
from dotenv import load_dotenv
load_dotenv()

# Define qual ambiente usar (via variável do sistema: development | production)
ENV = os.getenv("ENV", "production")

# Carrega os dados iniciais a partir do arquivo de configuração
file_path = 'sample' if ENV == 'development' else 'data'

pipeline_filepath = 'config/pipeline.json'
pipeline = carregar_json(pipeline_filepath)
template_filepath = 'config/template.json'
sources_filepath = 'config/sample_sources.json' if ENV == 'development' else 'config/sources.json'
dados_iniciais_filepath = f'{file_path}/{"dados_iniciais.json"}'
dados_completos_filepath = f'{file_path}/{"dados_completos.json"}'
keywords_filepath = f'{file_path}/{"keywords.json"}'
dados_ajustados_filepath = f'{file_path}/{"dados_ajustados.json"}'


if pipeline.get("extrair_dados_iniciais"):
    extrair_dados_iniciais(sources_filepath, dados_iniciais_filepath)

if pipeline.get("extrair_dados_completos"):
    template = carregar_json(template_filepath)
    extrair_dados_lote(template, dados_iniciais_filepath, dados_completos_filepath)

if pipeline.get("verificar_completude"):
    template = carregar_json(template_filepath)
    dados = carregar_json(dados_completos_filepath)
    verificar_completude_json(dados, template)

if pipeline.get("inferir_keywords"):
    dados = carregar_json(dados_completos_filepath)
    processar_lista_para_keywords(dados, keywords_filepath)

if pipeline.get("processar_dados_complementares"):
    dados = carregar_json(dados_completos_filepath)
    keywords = carregar_json(keywords_filepath)
    processar_dados_complementares(dados, keywords, dados_ajustados_filepath)
