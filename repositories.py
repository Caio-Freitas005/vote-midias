import sqlite3
from schemas import MediaCreate

def get_all(db: sqlite3.Connection):
    return db.execute('SELECT * FROM medias').fetchall()

def get_by_id(db: sqlite3.Connection, media_id: int):
    return db.execute('SELECT * FROM medias WHERE id = ?', (media_id,)).fetchone()

def get_totals(db: sqlite3.Connection):
    return db.execute('SELECT SUM(likes) as total_likes, SUM(dislikes) as total_dislikes FROM medias').fetchone()

def create(db: sqlite3.Connection, media: MediaCreate):
    cursor = db.execute(
        'INSERT INTO medias (title, genre, description, image) VALUES (?, ?, ?, ?)', 
        (media.title, media.genre, media.description, media.image)
    )
    db.commit()
    return cursor.lastrowid

def update_vote(db: sqlite3.Connection, media_id: int, column_to_update: str):
    query = f'UPDATE medias SET {column_to_update} = {column_to_update} + 1 WHERE id = ?'
    db.execute(query, (media_id,))
    db.commit()