"""
Funções para coleta de dados utilizando a YouTube Data API v3.

Este módulo reúne funções responsáveis por criar o cliente da API,
buscar vídeos, coletar estatísticas e extrair comentários públicos.
"""

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def criar_cliente_youtube(api_key):
    """
    Cria o cliente de conexão com a YouTube Data API v3.

    Parâmetros:
        api_key (str): Chave de acesso à API do YouTube.

    Retorno:
        Resource: Objeto cliente utilizado para realizar requisições à API.
    """
    if not api_key:
        raise ValueError("A chave da API não foi encontrada. Verifique o arquivo .env.")

    return build("youtube", "v3", developerKey=api_key)


def buscar_videos(
    youtube,
    query,
    max_results=50,
    region_code="BR",
    relevance_language="pt"
):
    """
    Busca vídeos no YouTube a partir de uma palavra-chave.

    Parâmetros:
        youtube: Cliente de conexão com a YouTube Data API v3.
        query (str): Palavra-chave utilizada na busca.
        max_results (int): Número máximo de vídeos retornados.
        region_code (str): Código da região usado para priorizar os resultados.
        relevance_language (str): Idioma de relevância dos resultados.

    Retorno:
        list: Lista de dicionários com informações básicas dos vídeos encontrados.
    """
    videos = []

    try:
        request = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            maxResults=max_results,
            regionCode=region_code,
            relevanceLanguage=relevance_language,
            order="relevance"
        )

        response = request.execute()

        for item in response.get("items", []):
            video_id = item.get("id", {}).get("videoId")
            snippet = item.get("snippet", {})

            if not video_id:
                continue

            videos.append({
                "video_id": video_id,
                "titulo": snippet.get("title"),
                "descricao": snippet.get("description"),
                "canal": snippet.get("channelTitle"),
                "canal_id": snippet.get("channelId"),
                "data_publicacao": snippet.get("publishedAt"),
                "palavra_chave": query,
                "link_video": f"https://www.youtube.com/watch?v={video_id}"
            })

    except HttpError as erro:
        print(f"Erro na coleta de vídeos para '{query}'. Detalhes: {erro}")

    return videos


def coletar_videos_por_palavras_chave(
    youtube,
    palavras_chave,
    max_videos_por_termo=20,
    region_code="BR",
    relevance_language="pt"
):
    """
    Coleta vídeos para uma lista de palavras-chave.

    Para cada termo de busca, a função consulta a YouTube Data API
    e armazena os vídeos encontrados em uma única lista.

    Parâmetros:
        youtube: Cliente de conexão com a YouTube Data API v3.
        palavras_chave (list): Lista de termos utilizados na busca.
        max_videos_por_termo (int): Quantidade máxima de vídeos por palavra-chave.
        region_code (str): Código da região usado para priorizar os resultados.
        relevance_language (str): Idioma de relevância dos resultados.

    Retorno:
        list: Lista com todos os vídeos coletados.
    """
    todos_videos = []

    for palavra_chave in palavras_chave:
        videos = buscar_videos(
            youtube=youtube,
            query=palavra_chave,
            max_results=max_videos_por_termo,
            region_code=region_code,
            relevance_language=relevance_language
        )

        todos_videos.extend(videos)

    return todos_videos


def buscar_estatisticas_videos(youtube, video_ids):
    """
    Busca estatísticas dos vídeos coletados.

    A função recebe uma lista de IDs de vídeos e retorna métricas como
    visualizações, curtidas e quantidade de comentários.

    Parâmetros:
        youtube: Cliente de conexão com a YouTube Data API v3.
        video_ids (list): Lista com os IDs dos vídeos.

    Retorno:
        dict: Dicionário em que cada chave é um ID de vídeo e o valor contém
        suas estatísticas.
    """
    estatisticas = {}

    # Remove IDs duplicados sem alterar a ordem original da lista.
    video_ids_unicos = list(dict.fromkeys(video_ids))

    try:
        # A API permite consultar até 50 vídeos por requisição.
        for i in range(0, len(video_ids_unicos), 50):
            lote_ids = video_ids_unicos[i:i + 50]

            request = youtube.videos().list(
                part="statistics",
                id=",".join(lote_ids)
            )

            response = request.execute()

            for item in response.get("items", []):
                video_id = item.get("id")
                stats = item.get("statistics", {})

                estatisticas[video_id] = {
                    "visualizacoes": int(stats.get("viewCount", 0)),
                    "likes": int(stats.get("likeCount", 0)),
                    "quantidade_comentarios": int(stats.get("commentCount", 0))
                }

    except HttpError as erro:
        print(f"Erro ao buscar estatísticas dos vídeos. Detalhes: {erro}")

    return estatisticas


def adicionar_estatisticas_aos_videos(videos, estatisticas):
    """
    Adiciona métricas de engajamento aos vídeos coletados.

    As estatísticas incluem visualizações, curtidas e quantidade de comentários.

    Parâmetros:
        videos (list): Lista de vídeos coletados.
        estatisticas (dict): Dicionário com estatísticas por ID de vídeo.

    Retorno:
        list: Lista de vídeos com as métricas de engajamento adicionadas.
    """
    videos_com_estatisticas = []

    for video in videos:
        video_id = video.get("video_id")
        stats = estatisticas.get(video_id, {})

        video_atualizado = {
            **video,
            "visualizacoes": stats.get("visualizacoes", 0),
            "likes": stats.get("likes", 0),
            "quantidade_comentarios": stats.get("quantidade_comentarios", 0)
        }

        videos_com_estatisticas.append(video_atualizado)

    return videos_com_estatisticas


def buscar_comentarios_video(youtube, video_id, max_comentarios=100):
    """
    Coleta comentários públicos de um vídeo específico.

    Nesta versão, são coletados apenas comentários principais,
    sem incluir respostas aos comentários.

    Parâmetros:
        youtube: Cliente de conexão com a YouTube Data API v3.
        video_id (str): ID do vídeo do YouTube.
        max_comentarios (int): Número máximo de comentários a serem coletados.

    Retorno:
        list: Lista de dicionários contendo os comentários coletados.
    """
    comentarios = []
    next_page_token = None

    try:
        while len(comentarios) < max_comentarios:
            quantidade_restante = max_comentarios - len(comentarios)

            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=min(100, quantidade_restante),
                pageToken=next_page_token,
                textFormat="plainText",
                order="relevance"
            )

            response = request.execute()

            for item in response.get("items", []):
                comentario = item.get("snippet", {}).get("topLevelComment", {})
                snippet = comentario.get("snippet", {})

                comentarios.append({
                    "video_id": video_id,
                    "comentario_id": comentario.get("id"),
                    "texto_comentario": snippet.get("textOriginal"),
                    "data_comentario": snippet.get("publishedAt"),
                    "likes_comentario": snippet.get("likeCount", 0)
                })

                if len(comentarios) >= max_comentarios:
                    break

            next_page_token = response.get("nextPageToken")

            # Interrompe a coleta quando não há mais páginas de comentários.
            if not next_page_token:
                break

    except HttpError as erro:
        print(f"Não foi possível coletar comentários do vídeo {video_id}. Detalhes: {erro}")

    return comentarios


def coletar_comentarios_dos_videos(
    youtube,
    video_ids,
    max_comentarios_por_video=100
):
    """
    Coleta comentários públicos dos vídeos informados.

    Para cada vídeo, são coletados comentários principais, sem incluir
    respostas aos comentários. Alguns vídeos podem não permitir a coleta
    devido a comentários desativados, privacidade ou indisponibilidade.
    """
    todos_comentarios = []

    for video_id in video_ids:
        comentarios_video = buscar_comentarios_video(
            youtube=youtube,
            video_id=video_id,
            max_comentarios=max_comentarios_por_video
        )

        todos_comentarios.extend(comentarios_video)

    return todos_comentarios
