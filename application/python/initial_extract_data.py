import json
import requests
from bs4 import BeautifulSoup
import csv
import re
import os

# Lista para armazenar os dados extraídos
dados = []

# Carrega os dados de fontes a partir de um arquivo JSON
with open('fontes.json', 'r', encoding='utf-8') as f:
    fontes = json.load(f)

fontes = fontes[5:]

# Nome do arquivo CSV
csv_filename = 'teses_dados_iniciais_usp1.csv'

# Verifica se o arquivo já existe para determinar se o cabeçalho deve ser adicionado
arquivo_existe = os.path.exists(csv_filename)

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
    response.raise_for_status()  # Verifica se houve erro na requisição
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extrai a linha de resultado
    resultado_info = soup.find('div', class_='dadosLinha').text.strip()

    # Usando expressão regular para extrair o número da página atual e o total de páginas
    match = re.search(r'Exibindo \d+ de \d+ na pagina (\d+) de (\d+)', resultado_info)
    pagina_atual = int(match.group(1)) if match else 1  # Página inicial
    pagina_final = int(match.group(2)) if match else 1  # Total de páginas

    # Loop para percorrer todas as páginas
    for pagina in range(pagina_atual, pagina_final + 1):
        print(f'Iniciando processo da página {pagina} de {pagina_final}')
        
        # URL da página específica
        url = url_base + "&pagina=" + str(pagina)
        
        # Faz a requisição HTTP
        try:
            response = requests.get(url)
            response.raise_for_status()  # Verifica se houve erro na requisição
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar a página {pagina}: {e}")
            continue  # Se houve erro, pula para a próxima página

        # Processa o HTML com BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontra todas as divs com as classes desejadas
        for linha in soup.find_all('div', class_=['dadosLinha dadosCor1', 'dadosLinha dadosCor2']):
            nome_div = linha.find('div', class_='dadosDocNome')
            titulo_div = linha.find('div', class_='dadosDocTitulo')
            area_div = linha.find('div', class_='dadosDocArea')
            tipo_div = linha.find('div', class_='dadosDocTipo')
            unidade_div = linha.find('div', class_='dadosDocUnidade')
            ano_div = linha.find('div', class_='dadosDocAno')
            
            link = nome_div.find('a')['href'] if nome_div.find('a') else ''
            nome = nome_div.get_text(strip=True) if nome_div else ''
            titulo = titulo_div.get_text(strip=True) if titulo_div else ''
            area = area_div.get_text(strip=True) if area_div else ''
            tipo = tipo_div.get_text(strip=True) if tipo_div else ''
            unidade = unidade_div.get_text(strip=True) if unidade_div else ''
            ano = ano_div.get_text(strip=True) if ano_div else ''
            
            dados.append([link, nome, titulo, area, tipo, unidade, ano])

        # Salva os dados no arquivo CSV após cada página
        with open(csv_filename, mode='a', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter='\t')  # Configura o separador como TAB
            
            # Se o arquivo não existir ainda, adiciona o cabeçalho
            if not arquivo_existe:
                writer.writerow(["Link", "Nome", "Título", "Área", "Tipo", "Unidade", "Ano"])
                arquivo_existe = True  # Marca o arquivo como existente após escrever o cabeçalho
            
            # Escreve os dados extraídos
            writer.writerows(dados)
        
        # Limpa os dados após cada página
        dados.clear()

        # Exibe informações da página
        print(f'Finalizando processo da página: {pagina} de {pagina_final}')

print(f'Dados extraídos e salvos em {csv_filename}')
