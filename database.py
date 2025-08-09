import sqlite3

DB_NAME = 'media.db'

def create_tbs(conn: sqlite3.Connection):
    """Cria a tabela de mídias usando uma conexão existente."""
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

def populate_tbs(conn: sqlite3.Connection):
    """Popula a tabela de mídias se ela estiver vazia, usando uma conexão existente."""
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM medias")
    count = cursor.fetchone()[0]

    if count == 0:
        print("Banco de dados vazio. Populando com dados iniciais...")
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
        print("Mídias inseridas com sucesso.")
    else:
        print("O banco de dados já contém dados. Nenhuma ação necessária.")

if __name__ == '__main__':
    print(f"Iniciando configuração do banco de dados '{DB_NAME}'...")
    conn = None # Inicializa a variável
    try:
        # Abre a conexão apenas uma vez
        conn = sqlite3.connect(DB_NAME)
        create_tbs(conn)
        populate_tbs(conn)
        conn.commit()
        
        print("\nConfiguração do banco de dados concluída com sucesso!")
        
    except sqlite3.Error as e:
        print(f"Ocorreu um erro ao configurar o banco de dados: {e}")
        
    finally:
        # Garante que a conexão seja fechada, não importa o que aconteça
        if conn:
            conn.close()
            print("Conexão com o banco de dados fechada.")