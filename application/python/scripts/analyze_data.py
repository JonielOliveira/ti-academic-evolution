from scripts.utils_io import carregar_json, salvar_json
import pandas as pd
from pandas import json_normalize
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def funcao_frequencia_de_palavras():

    # Explode as listas de palavras-chave em português
    palavras_explodidas = df.explode('Palavras-chave em português')

    # Conta a frequência de cada palavra-chave
    frequencia = palavras_explodidas['Palavras-chave em português'].value_counts()

    # Exibe o resultado
    print(frequencia)

def funcao_nuvem_de_palavras():

    # Explode as listas de palavras-chave em português
    palavras_explodidas = df.explode('Palavras-chave em português')

    # Remove valores nulos (caso existam)
    palavras_explodidas = palavras_explodidas.dropna(subset=['Palavras-chave em português'])

    # Junta todas as palavras numa única string
    texto = ' '.join(palavras_explodidas['Palavras-chave em português'])

    # Gera a nuvem de palavras
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(texto)

    # Exibe a nuvem de palavras
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def funcao_verificar_data_defesa():
    # Converte o campo para datetime, erros viram NaT (Not a Time)
    df['Data de Defesa Convertida'] = pd.to_datetime(df['Data de Defesa'], errors='coerce')

    # Verifica quantos são NaT (ou seja, inválidos)
    num_invalidos = df['Data de Defesa Convertida'].isna().sum()

    print(f"Número de datas inválidas: {num_invalidos}")

#  Carrega os dados do arquivo JSON
dados = carregar_json('data/dados_completos.json')

# Transforma em DataFrame
df = json_normalize(dados)

# Converte o campo para datetime, erros viram NaT
df['Data de Defesa Convertida'] = pd.to_datetime(df['Data de Defesa'], errors='coerce')

# Cria novo campo: Ano de Defesa
df['Ano de Defesa'] = df['Data de Defesa Convertida'].dt.year


# Acha a data mais antiga e mais recente
data_min = df['Data de Defesa Convertida'].min()
data_max = df['Data de Defesa Convertida'].max()

print(f"Ano mais antigo: {data_min}")
print(f"Ano mais recente: {data_max}")


# Calcula a década
df['Década'] = (df['Ano de Defesa'] // 10) * 10


# Mostra os 5 primeiros com o novo campo
print(df[['Data de Defesa', 'Data de Defesa Convertida', 'Ano de Defesa', 'Década']].head(30))


# Agrupa por década e conta quantos registros tem em cada
contagem_decadas = df.groupby('Década').size()

# Exibe o resultado
print(contagem_decadas)

# Agrupa por década e conta quantos registros tem em cada
contagem_anos = df.groupby('Ano de Defesa').size()

# Exibe o resultado
print(contagem_anos)



# Cria o gráfico de barras
plt.figure(figsize=(10, 6))
contagem_anos.plot(kind='bar')

# Ajusta o título e os rótulos
plt.title('Número de Defesas por Década')
plt.xlabel('Década')
plt.ylabel('Quantidade de Defesas')

# Mostra o gráfico
plt.show()


plt.figure(figsize=(12, 6))
contagem_anos.plot(kind='line', marker='o')

plt.title('Número de Defesas por Ano')
plt.xlabel('Ano de Defesa')
plt.ylabel('Quantidade de Defesas')

plt.grid(True)
plt.show()


# funcao_frequencia_de_palavras()
# funcao_nuvem_de_palavras()
# funcao_verificar_data_defesa()
