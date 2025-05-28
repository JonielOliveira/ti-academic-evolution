import requests
from bs4 import BeautifulSoup
import re
import copy
from utils_io import carregar_json, salvar_json

def extrair_dados_iniciais(arquivo_entrada_json, arquivo_saida_json):
    """
    Extrai dados iniciais a partir dos links em um arquivo JSON e salva os resultados em outro arquivo JSON.

    Parâmetros:
    - arquivo_entrada_json (str): nome do arquivo de entrada com as fontes.
    - arquivo_saida_json (str): nome do arquivo de saída para salvar os dados extraídos.
    """
    dados = []

    # Carrega os dados de fontes a partir do arquivo JSON
    fontes = carregar_json(arquivo_entrada_json)

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
        match = re.search(r'\(página (\d+) de (\d+)\)', resultado_info)
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

            if (pagina) % 20 == 0:
                salvar_json(dados, arquivo_saida_json)
                print(f"Progresso salvo até a página: {pagina}")

    # Salva os dados no arquivo JSON
    salvar_json(dados, arquivo_saida_json)


def verificar_completude_json(dados, template):
    """
    Verifica se todos os campos do template estão presentes em cada elemento de uma lista de dicionários.
    
    Parâmetros:
    - dados (list): lista de dicionários com os dados a verificar.
    - template (dict): dicionário modelo com as chaves esperadas.
    
    Retorna:
    - None. Apenas imprime o resultado.
    """

    total_elementos = len(dados)
    completos = 0
    incompletos = 0

    print(f"\nTotal de elementos: {total_elementos}")

    for idx, elemento in enumerate(dados, start=1):
        faltantes = []
        for chave in template.keys():
            if chave not in elemento:
                faltantes.append(chave)

        if not faltantes:
            completos += 1
            print(f"Elemento {idx}: COMPLETO")
        else:
            incompletos += 1
            print(f"Elemento {idx}: INCOMPLETO - Faltando {len(faltantes)} campos: {faltantes}")

    print("\nResumo:")
    print(f"Completos: {completos}")
    print(f"Incompletos: {incompletos}")
    print(f"Total verificado: {total_elementos}")


def extrair_email(tag):
    try:
        # Encontre o link <a> dentro da div
        link = tag.find('a')

        # Pegue o valor do atributo 'onclick'
        onclick_value = link['onclick']

        # Use uma expressão regular para extrair o nome do usuário e o domínio
        match = re.search(r"showEmail\('([^']+)','([^']+)'", onclick_value)

        if match:
            # Combine o nome do usuário e domínio para formar o e-mail
            email = match.group(1) + '@' + match.group(2)
            return email
        else:
            return ''
    except:
        return ''


def extrair_informacoes_arquivo(div):
    # Encontre o link <a> dentro da div
    link = div.find('a')
    
    # Se o link não for encontrado, retorna dados vazios
    if not link:
        return '', '', ''
    
    # Extrai o link do arquivo (atributo href)
    dominio = 'https://www.teses.usp.br'
    link_arquivo = dominio + link['href']
    
    # Extrai o nome do arquivo (texto dentro da tag <a>)
    nome_arquivo = link.text.strip()
    
    # Extrai a descrição do tamanho do arquivo
    tamanho_arquivo = div.text.strip()
    
    # Usando regex para pegar o tamanho do arquivo, que está após o nome
    match = re.search(r'\((.*?)\)', tamanho_arquivo)
    
    if match:
        descricao_tamanho = match.group(1)
    else:
        descricao_tamanho = ''
    
    return link_arquivo, nome_arquivo, descricao_tamanho


def extrair_texto_com_quebras_de_linha(div):
    # Substituindo as tags <br> por quebras de linha '\n'
    for br in div.find_all('br'):
        br.insert_before('\n')  # Insere uma nova linha antes de cada <br>
        br.extract()  # Remove o <br> da árvore

    # Extrai o texto da div com as quebras de linha
    texto_com_quebras = div.get_text()

    # Substitui múltiplas quebras de linha por uma única
    texto_com_quebras = re.sub(r'\n+', '\n', texto_com_quebras)

    # Substitui as quebras de linha por '---'
    texto_com_quebras = re.sub(r'\n', '---', texto_com_quebras)

    # Divide o texto nas ocorrências de '---', removendo elementos vazios
    textos = [t.strip() for t in texto_com_quebras.split('---') if t.strip()]

    return textos


def extrair_dados_lote(template, arquivo_entrada_json, arquivo_saida_json):
    
    dados = []

    # Carrega fontes
    fontes = carregar_json(arquivo_entrada_json)

    for i, fonte in enumerate(fontes):

        print(f"\nIniciando processo do documento: {i+1} de {len(fontes)}")

        cabecario = copy.deepcopy(template)
        cabecario["Link de Acesso"] = fonte['Link']

        try:
            response = requests.get(fonte['Link'])
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar: {e}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        for linha in soup.find_all('div', id='CorpoTexto'):

            titulos = linha.find_all('div', class_='DocumentoTituloTexto')
            descricoes = linha.find_all('div', class_='DocumentoTexto')

            for titulo, descricao in zip(titulos, descricoes):
                info_titulo = titulo.get_text(strip=True) if titulo else ''
                info_descricao = descricao.get_text(strip=True) if descricao else ''

                if info_titulo == 'E-mail':
                    info_descricao = extrair_email(descricao)

                if info_titulo in ('Banca examinadora','Palavras-chave em português','Palavras-chave em inglês'):
                    info_descricao = extrair_texto_com_quebras_de_linha(descricao)

                if info_titulo in ('Autor','Orientador'):
                    info_descricao = info_descricao.removesuffix('(Catálogo USP)')

                if info_titulo in cabecario and info_descricao:
                    cabecario[info_titulo] = info_descricao

            titulos2 = linha.find_all('div', class_='DocumentoTituloTexto2')
            descricoes2 = linha.find_all('div', class_='DocumentoTextoResumo')

            for titulo, descricao in zip(titulos2, descricoes2):
                info_titulo = titulo.get_text(strip=True) if titulo else ''
                info_descricao = descricao.get_text(strip=True) if descricao else ''

                if info_titulo in cabecario and info_descricao:
                    cabecario[info_titulo] = info_descricao

            if titulos2:
                info_arquivo = titulos2[-1].get_text(strip=True) if titulo else ''
                if info_arquivo:
                    cabecario["Arquivo Link"], cabecario["Arquivo Nome"], cabecario["Arquivo Tamanho"] = extrair_informacoes_arquivo(titulos2[-1])

        dados.append(copy.deepcopy(cabecario))

        print(f"Finalizando processo do documento: {i+1} de {len(fontes)}")

        if (i + 1) % 100 == 0:
            salvar_json(dados, arquivo_saida_json)
            print(f"Progresso salvo até o documento: {i+1}")

    # Salva em JSON
    salvar_json(dados, arquivo_saida_json)

if __name__ == "__main__":

    extrair_dados_iniciais('config/sources.json', 'data/dados_iniciais.json')
    template = carregar_json('config/template.json')
    extrair_dados_lote(template, 'data/dados_iniciais.json','data/dados_completos.json')
    dados = carregar_json('data/dados_completos.json')
    verificar_completude_json(dados, template)

    dados = carregar_json('data/dados_completos.json')
