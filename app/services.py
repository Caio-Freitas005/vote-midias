import sqlite3
from fastapi import HTTPException
from . import repositories
from .schemas import MediaCreate, MediaUpdate

def get_all_medias(db: sqlite3.Connection):
    return repositories.get_all(db)

def get_media_by_id(db: sqlite3.Connection, media_id: int):
    media = repositories.get_by_id(db, media_id)
    if not media:
        raise HTTPException(status_code=404, detail='Mídia não encontrada')
    return media

def create_media(media: MediaCreate, db: sqlite3.Connection):
    new_id = repositories.create(db, media)

    if new_id is None:
        raise HTTPException(status_code=500, detail='Falha ao criar a mídia no banco de dados.')
   
    return repositories.get_by_id(db, new_id)

def update_media(media_id: int, media_data: MediaUpdate, db: sqlite3.Connection):
    """Atualiza os dados de uma mídia existente."""
    # Verifica se a mídia existe
    existing_media = repositories.get_by_id(db, media_id)
    if not existing_media:
        raise HTTPException(status_code=404, detail='Mídia não encontrada')

    # Se existe, chama o repositório para fazer a atualização
    repositories.update(db, media_id, media_data)
    
    # Retorna a mídia com os dados atualizados
    return repositories.get_by_id(db, media_id)

def delete_media(media_id: int, db: sqlite3.Connection):
    """Apaga uma mídia existente."""
    existing_media = repositories.get_by_id(db, media_id)
    if not existing_media:
        raise HTTPException(status_code=404, detail='Mídia não encontrada')

    # Se existe, chama o repositório para apagar
    repositories.delete(db, media_id)
    
    # Retorna uma mensagem de sucesso.
    return {'detail': 'Mídia apagada com sucesso'}

def get_all_totals(db: sqlite3.Connection):
    return repositories.get_totals(db)

def update_vote(media_id: int, vote_type: str, db: sqlite3.Connection):
    media = repositories.get_by_id(db, media_id)
    if not media:
        raise HTTPException(status_code=404, detail='Mídia não encontrada')

    if vote_type == 'like':
        column = 'likes'
    elif vote_type == 'dislike':
        column = 'dislikes'
    else:
        raise HTTPException(status_code=500, detail='Tipo de voto inválido.')
    
    repositories.update_vote(db, media_id, column)
    return repositories.get_by_id(db, media_id)