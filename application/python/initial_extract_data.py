import os
import json
import requests
from bs4 import BeautifulSoup
import re

def get_file_path(filename):
    """Retorna o caminho absoluto de um arquivo localizado na mesma pasta do script .py."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, filename)

def extrair_dados_iniciais(arquivo_entrada_json, arquivo_saida_json):
    """
    Extrai dados iniciais a partir dos links em um arquivo JSON e salva os resultados em outro arquivo JSON.

    Parâmetros:
    - arquivo_entrada_json (str): nome do arquivo de entrada com as fontes.
    - arquivo_saida_json (str): nome do arquivo de saída para salvar os dados extraídos.
    """
    dados = []

    # Carrega os dados de fontes a partir do arquivo JSON
    with open(get_file_path(arquivo_entrada_json), 'r', encoding='utf-8') as f:
        fontes = json.load(f)

    # Se quiser manter a filtragem a partir do 6º elemento
    # OBS.: Apenas para teste
    fontes = fontes[5:]

    # Loop pelas fontes
    for fonte in fontes:

        print(f"Iniciando processo da subárea: {fonte['area']}")

        # Página inicial
        pagina_inicial = 1

        # URL base
        url_base = fonte['url_base']

        # Primeira requisição para obter o número total de páginas
        url_primeira_pagina = url_base + "&pagina=" + str(pagina_inicial)
        response = requests.get(url_primeira_pagina)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extrai a linha de resultado
        resultado_info = soup.find('div', class_='dadosLinha').text.strip()

        # Extrai número da página atual e o total de páginas
        match = re.search(r'Exibindo \d+ de \d+ na pagina (\d+) de (\d+)', resultado_info)
        pagina_atual = int(match.group(1)) if match else 1
        pagina_final = int(match.group(2)) if match else 1

        # Loop para percorrer todas as páginas
        for pagina in range(pagina_atual, pagina_final + 1):
            print(f'Iniciando processo da página {pagina} de {pagina_final}')
            
            url = url_base + "&pagina=" + str(pagina)
            
            try:
                response = requests.get(url)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Erro ao acessar a página {pagina}: {e}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            
            for linha in soup.find_all('div', class_=['dadosLinha dadosCor1', 'dadosLinha dadosCor2']):
                nome_div = linha.find('div', class_='dadosDocNome')
                titulo_div = linha.find('div', class_='dadosDocTitulo')
                area_div = linha.find('div', class_='dadosDocArea')
                tipo_div = linha.find('div', class_='dadosDocTipo')
                unidade_div = linha.find('div', class_='dadosDocUnidade')
                ano_div = linha.find('div', class_='dadosDocAno')
                
                link = nome_div.find('a')['href'] if nome_div and nome_div.find('a') else ''
                nome = nome_div.get_text(strip=True) if nome_div else ''
                titulo = titulo_div.get_text(strip=True) if titulo_div else ''
                area = area_div.get_text(strip=True) if area_div else ''
                tipo = tipo_div.get_text(strip=True) if tipo_div else ''
                unidade = unidade_div.get_text(strip=True) if unidade_div else ''
                ano = ano_div.get_text(strip=True) if ano_div else ''
                
                dados.append({
                    "Link": link,
                    "Nome": nome,
                    "Título": titulo,
                    "Área": area,
                    "Tipo": tipo,
                    "Unidade": unidade,
                    "Ano": ano
                })

            print(f'Finalizando processo da página: {pagina} de {pagina_final}')

    # Salva os dados no arquivo JSON
    with open(get_file_path(arquivo_saida_json), 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

    print(f'Dados extraídos e salvos em {arquivo_saida_json}')

extrair_dados_iniciais('fontes.json', 'dados_iniciais.json')
