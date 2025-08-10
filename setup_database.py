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
    cursor.execute('SELECT COUNT(*) FROM medias')
    count = cursor.fetchone()[0]

    if count == 0:
        print('Banco de dados vazio. Populando com dados iniciais...')
        medias = [
            ('A Origem', 'Sci-Fi', 'Um ladrão que invade sonhos.', 'https://m.media-amazon.com/images/S/pv-target-images/3f122417c55feda5c465f701320892661bfea27c1dfcff81e7fb0641ba29171c.jpg'),
            ('Interestelar', 'Sci-Fi', 'Viagem no tempo e espaço para salvar a humanidade.', 'https://beam-images.warnermediacdn.com/BEAM_LWM_DELIVERABLES/aa5b9295-8f9c-44f5-809b-3f2b84badfbf/74a67d78-7c7e-47e8-9603-20fe2a00eae4?host=wbd-images.prod-vod.h264.io&partner=beamcom'),
            ('Batman: O Cavaleiro das Trevas', 'Ação', 'Batman enfrenta o Coringa.', 'https://m.media-amazon.com/images/S/pv-target-images/49eeda38b5fe2ef033861ef6b07ea914eeef437cdb1dd35e282d9acce008779e._SX1080_FMjpg_.jpg'),
            ('Forrest Gump', 'Drama', 'A vida de um homem simples com um grande coração.', 'https://wp-content.amenteemaravilhosa.com.br/2015/05/forrestgump.jpg'),
            ('Matrix', 'Ficção', 'Descubra a verdade sobre a realidade.', 'https://occ-0-8407-2219.1.nflxso.net/dnm/api/v6/Z-WHgqd_TeJxSuha8aZ5WpyLcX8/AAAABZzDupwylH-h0zoEyASxaxb-eXBvlskslcNE-zYTrF4-vtehLHmkb13FL95R8M9mjji5whxBux6iS-fKTRiHju_wAuMgRi7Dwybo.jpg?r=608')
        ]
        
        cursor.executemany("""
            INSERT INTO medias (title, genre, description, image) 
            VALUES (?, ?, ?, ?)
        """, medias)
        print('Mídias inseridas com sucesso.')
    else:
        print('O banco de dados já contém dados. Nenhuma ação necessária.')

if __name__ == '__main__':
    print(f"Iniciando configuração do banco de dados '{DB_NAME}'...")
    conn = None # Inicializa a variável
    try:
        # Abre a conexão apenas uma vez
        conn = sqlite3.connect(DB_NAME)
        create_tbs(conn)
        populate_tbs(conn)
        conn.commit()
        
        print('\nConfiguração do banco de dados concluída com sucesso!')
        
    except sqlite3.Error as e:
        print(f'Ocorreu um erro ao configurar o banco de dados: {e}')
        
    finally:
        # Garante que a conexão seja fechada, não importa o que aconteça
        if conn:
            conn.close()
            print('Conexão com o banco de dados fechada.')