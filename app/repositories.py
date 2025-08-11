import sqlite3
from .schemas import MediaCreate, MediaUpdate

def get_all(db: sqlite3.Connection):
    return db.execute('SELECT * FROM medias').fetchall()

def get_by_id(db: sqlite3.Connection, media_id: int):
    return db.execute('SELECT * FROM medias WHERE id = ?', (media_id,)).fetchone()

def get_totals(db: sqlite3.Connection):
    return db.execute('SELECT SUM(likes) as total_likes, SUM(dislikes) as total_dislikes FROM medias').fetchone()

def create(db: sqlite3.Connection, media: MediaCreate):
    cursor = db.execute(
        'INSERT INTO medias (title, genre, description, image) VALUES (?, ?, ?, ?)', 
        (media.title, media.genre, media.description, str(media.image))
    )
    db.commit()
    return cursor.lastrowid

def update(db: sqlite3.Connection, media_id: int, media: MediaUpdate):
    """Atualiza os dados de uma mídia existente no banco de dados."""
    cursor = db.execute(
        """
        UPDATE medias 
        SET title = ?, genre = ?, description = ?, image = ?
        WHERE id = ?
        """,
        (media.title, media.genre, media.description, str(media.image), media_id)
    )
    db.commit()
    # Retorna o número de linhas afetadas. Se for 1, a atualização foi bem-sucedida.
    return cursor.rowcount

def delete(db: sqlite3.Connection, media_id: int):
    """Apaga uma mídia do banco de dados com base no seu ID"""
    cursor = db.execute(
        'DELETE FROM medias WHERE id = ?',
        (media_id,)
    )
    db.commit()

    return cursor.rowcount

def update_vote(db: sqlite3.Connection, media_id: int, column_to_update: str):
    query = f'UPDATE medias SET {column_to_update} = {column_to_update} + 1 WHERE id = ?'
    db.execute(query, (media_id,))
    db.commit()