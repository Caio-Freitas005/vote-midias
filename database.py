import sqlite3

DB_NAME = 'media.db'

def connect_db():
    return sqlite3.connect(DB_NAME)

def create_tbs():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            description TEXT NOT NULL,
            image TEXT NOT NULL,
            likes INTEGER DEFAULT 0,
            dislikes INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()

def populate_tbs():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM medias")
    count = cursor.fetchone()[0]

    if count == 0:
        medias = [
            ("A Origem", "Sci-Fi", "Um ladrão que invade sonhos.", "https://placehold.co/150/png"),
            ("Interestelar", "Sci-Fi", "Viagem no tempo e espaço para salvar a humanidade.", "https://placehold.co/150/png"),
            ("Batman: O Cavaleiro das Trevas", "Ação", "Batman enfrenta o Coringa.", "https://placehold.co/150/png"),
            ("Forrest Gump", "Drama", "A vida de um homem simples com um grande coração.", "https://placehold.co/150/png"),
            ("Matrix", "Ficção", "Descubra a verdade sobre a realidade.", "https://placehold.co/150/png")
        ]
        
        cursor.executemany("""
            INSERT INTO medias (title, genre, description, image) 
            VALUES (?, ?, ?, ?)
        """, medias)
        conn.commit()

    conn.close()

if __name__ == '__main__':
    create_tbs()
    populate_tbs()
    print("Banco criado e populado com sucesso.")