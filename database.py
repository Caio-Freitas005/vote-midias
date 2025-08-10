import sqlite3

DB_NAME = 'media.db'

def get_db():
    """Cria e fornece uma conexão com o banco, garantindo que ela seja fechada no final."""
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row # Transforma o resultado em objeto Row, que funciona como dicionário
    try:
        yield conn
    finally:
        conn.close()