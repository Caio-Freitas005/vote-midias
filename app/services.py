import sqlite3
from fastapi import HTTPException
from . import repositories
from .schemas import MediaCreate

def get_all_medias(db: sqlite3.Connection):
    return repositories.get_all(db)

def create_media(media: MediaCreate, db: sqlite3.Connection):
    new_id = repositories.create(db, media)

    if new_id is None:
        raise HTTPException(status_code=500, detail='Falha ao criar a mídia no banco de dados.')
   
    return repositories.get_by_id(db, new_id)

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