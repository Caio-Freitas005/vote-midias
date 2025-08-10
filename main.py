import sqlite3
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from schemas import MediaCreate
from database import get_db
import services

DB_NAME = 'media.db'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'], 
    allow_credentials=True,
    allow_methods=['*'], 
    allow_headers=['*'], 
)

# Monta o diretório para servir os arquivos estáticos
app.mount('/static', StaticFiles(directory='static'), name='static')

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@app.get('/', response_class=FileResponse, include_in_schema=False)
async def read_root():
    return 'static/index.html'

@app.get('/medias')
def get_medias(db: sqlite3.Connection = Depends(get_db)):
    """Lista todas as mídias com os votos atuais."""
    return services.get_all_medias(db)

@app.post('/medias', status_code=201)
def create_media(media: MediaCreate, db: sqlite3.Connection = Depends(get_db)):
    """Cadastra uma nova mídia."""
    return services.create_media(media, db)

@app.post('/medias/{media_id}/like')
def like_media(media_id: int, db: sqlite3.Connection = Depends(get_db)):
    """Registra um voto positivo para uma mídia."""
    return services.update_vote(media_id, 'like', db)

@app.post('/medias/{media_id}/dislike')
def dislike_media(media_id: int, db: sqlite3.Connection = Depends(get_db)):
    """Registra um voto negativo para uma mídia."""
    return services.update_vote(media_id, 'dislike', db)

@app.get('/medias/totals')
def get_totals(db: sqlite3.Connection = Depends(get_db)):
    """Exibe os totais de votos positivos e negativos."""
    totals = services.get_all_totals(db)
    return {'total_likes': totals['total_likes'] or 0, 'total_dislikes': totals['total_dislikes'] or 0}