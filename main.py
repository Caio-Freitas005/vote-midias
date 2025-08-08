from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

DB_NAME = 'media.db'

app = FastAPI()

def connect_db():
    return sqlite3.connect(DB_NAME)

@app.get("/ping")
def ping():
    return {"status": "ok", "message": "pong"}

@app.get("/medias")
def get_medias():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medias")
    rows = cursor.fetchall()
    conn.close()
    return {"medias": rows}