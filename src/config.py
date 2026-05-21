"""
Configurações principais do projeto.

Este arquivo centraliza diretórios, parâmetros da coleta,
chave da API e palavras-chave utilizadas na busca de dados.
"""

from pathlib import Path
import os
from dotenv import load_dotenv


# Define o diretório raiz do projeto
ROOT_DIR = Path(__file__).resolve().parents[1]

# Carrega a variável de ambiente armazenada no arquivo .env
load_dotenv(ROOT_DIR / ".env")

# Recupera a chave da YouTube Data API v3
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


# Diretórios do projeto
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
FINAL_DATA_DIR = DATA_DIR / "final"

OUTPUTS_DIR = ROOT_DIR / "outputs"
FIGURES_DIR = OUTPUTS_DIR / "figures"
MODELS_DIR = OUTPUTS_DIR / "models"

DIRETORIOS_PROJETO = [
    DATA_DIR,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    FINAL_DATA_DIR,
    OUTPUTS_DIR,
    FIGURES_DIR,
    MODELS_DIR
]


# Parâmetros da coleta
REGION_CODE = "BR"
RELEVANCE_LANGUAGE = "pt"

MAX_VIDEOS_POR_TERMO = 20
MAX_COMENTARIOS_POR_VIDEO = 100


# Palavras-chave utilizadas na busca dos vídeos
PALAVRAS_CHAVE = [
    "Estatuto Digital da Criança e do Adolescente",
    "ECA Digital",
    "ECA Digital jogos",
    "ECA Digital jogos online",
    "ECA Digital games",
    "Lei do ECA Digital",
    "Lei Felca ECA Digital",
    "Lei 15211 ECA Digital",
    "proteção infantil na internet",
    "proteção infantil jogos online",
    "segurança infantil jogos online",
    "crianças e adolescentes jogos digitais",
    "regulação jogos digitais crianças",
    "regulação de jogos online para crianças",
    "adultização infantil internet jogos",
    "influenciadores infantis jogos",
    "crianças internet jogos online",
    "adolescentes jogos online segurança",
    "riscos dos jogos online para crianças",
    "exposição infantil jogos digitais",
    "plataformas digitais crianças adolescentes"
]