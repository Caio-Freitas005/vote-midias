from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

DB_NAME = 'media.db'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

# Monta o diretório para servir os arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    """Cria e fornece uma conexão com o banco, garantindo que ela seja fechada no final."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # Transforma o resultado em objeto Row, que funciona como dicionário
    try:
        yield conn
    finally:
        conn.close()

class MediaCreate(BaseModel):
    title: str
    genre: str
    description: str | None = None
    image: str 

def _update_vote(media_id: int, vote_type: str, conn: sqlite3.Connection):
    """Função interna para atualizar o voto (like ou dislike) de uma mídia."""
    cursor = conn.cursor()

    # Lógica repetida: verificar se a mídia existe
    cursor.execute("SELECT id FROM medias WHERE id = ?", (media_id,))
    media = cursor.fetchone()
    if not media:
        raise HTTPException(status_code=404, detail="Mídia não encontrada")

    # Torna dinâmica a escolha da coluna a ser atualizada
    if vote_type == "like":
        column_to_update = "likes"
    elif vote_type == "dislike":
        column_to_update = "dislikes"
    else:
        raise HTTPException(status_code=500, detail="Tipo de voto inválido.")

    # Lógica repetida: executar a atualização e retornar o resultado.
    query = f"UPDATE medias SET {column_to_update} = {column_to_update} + 1 WHERE id = ?"
    cursor.execute(query, (media_id,))
    conn.commit()

    updated_media = cursor.execute("SELECT * FROM medias WHERE id = ?", (media_id,)).fetchone()
    return updated_media

@app.get("/", response_class=FileResponse, include_in_schema=False)
async def read_root():
    return "static/index.html"

@app.get("/medias")
def get_medias(conn: sqlite3.Connection = Depends(get_db)):
    """Lista todas as mídias com os votos atuais."""
    medias = conn.execute("SELECT * FROM medias").fetchall()
    return medias

@app.post("/medias", status_code=201)
def create_media(media: MediaCreate, conn: sqlite3.Connection = Depends(get_db)):
    """Cadastra uma nova mídia."""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO medias (title, genre, description, image) VALUES (?, ?, ?, ?)", 
        (media.title, media.genre, media.description, media.image)
    )
    conn.commit()
    new_media_id = cursor.lastrowid

    new_media = conn.execute("SELECT * FROM medias WHERE id = ?", (new_media_id,)).fetchone()
    return new_media

@app.post("/medias/{media_id}/like")
def like_media(media_id: int, conn: sqlite3.Connection = Depends(get_db)):
    """Registra um voto positivo para uma mídia."""
    return _update_vote(media_id, "like", conn)

@app.post("/medias/{media_id}/dislike")
def dislike_media(media_id: int, conn: sqlite3.Connection = Depends(get_db)):
    """Registra um voto negativo para uma mídia."""
    return _update_vote(media_id, "dislike", conn)

@app.get("/medias/totals")
def get_totals(conn: sqlite3.Connection = Depends(get_db)):
    """Exibe os totais de votos positivos e negativos."""
    totals = conn.execute("SELECT SUM(likes) as total_likes, SUM(dislikes) as total_dislikes FROM medias").fetchone()
    return {"total_likes": totals["total_likes"] or 0, "total_dislikes": totals["total_dislikes"] or 0}