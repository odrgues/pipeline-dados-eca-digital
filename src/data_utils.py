"""
Funções auxiliares para manipulação de diretórios e arquivos.

Este módulo centraliza operações reutilizáveis do projeto, como criação
de diretórios, salvamento e carregamento de arquivos CSV.
"""


import pandas as pd

def criar_diretorios(diretorios):
    """
    Cria os diretórios necessários para o projeto, caso ainda não existam.
    Parâmetros:
    - diretorios: lista de objetos Path representando os diretórios a serem criados.
    """
    for diretorio in diretorios:
        diretorio.mkdir(parents=True, exist_ok=True)
        
def salvar_csv(df, caminho):
    """
    Salva um DataFrame em formato CSV.

    Parâmetros:
        df (DataFrame): Conjunto de dados que será salvo.
        caminho (Path ou str): Caminho onde o arquivo CSV será armazenado.
    """
    caminho.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(caminho, index=False, encoding="utf-8-sig")
    
    
def remover_duplicados(df, subset):
    """
    Remove registros duplicados de um DataFrame com base em uma ou mais colunas.

    Parâmetros:
        df (DataFrame): Conjunto de dados a ser tratado.
        subset (str ou list): Coluna ou lista de colunas usadas para identificar duplicidades.

    Retorno:
        DataFrame: DataFrame sem registros duplicados.
    """
    return df.drop_duplicates(subset=subset).reset_index(drop=True)
    
def carregar_csv(caminho):
    """
    Carrega um arquivo CSV e retorna os dados em formato de DataFrame.

    Parâmetros:
    caminho (Path ou str): Caminho do arquivo CSV que será carregado.

    Retorno:
    DataFrame: Dados carregados a partir do arquivo CSV.
    """
    return pd.read_csv(caminho)