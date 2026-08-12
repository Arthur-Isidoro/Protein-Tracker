import sqlite3

DB_NAME = 'protein_tracker.db'

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
            CREATE TABLE IF NOT EXISTS registros_diarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL UNIQUE,
            proteina_consumida REAL NOT NULL,
            meta_proteina REAL NOT NULL,
            bateu_meta INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def salvar_registro(data, proteina_consumida, meta_proteina):
    bateu = 1 if proteina_consumida >= meta_proteina else 0
    conn = get_db()
    conn.execute('''
        INSERT INTO registros_diarios (data, proteina_consumida, meta_proteina, bateu_meta)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(data) DO UPDATE SET
            proteina_consumida = excluded.proteina_consumida,
            meta_proteina = excluded.meta_proteina,
            bateu_meta = excluded.bateu_meta
    ''', (data, proteina_consumida, meta_proteina, bateu))
    conn.commit()
    conn.close()

def listar_registros(limite=30):
    conn = get_db()
    registros = conn.execute('''
        SELECT * FROM registros_diarios
        ORDER BY data DESC
        LIMIT ?
    ''', (limite,)).fetchall()
    conn.close()
    return registros

def calcular_streak_atual():
    """Conta quantos dias seguidos (a partir do mais recente) bateram a meta."""
    conn = get_db()
    registros = conn.execute('''
        SELECT bateu_meta FROM registros_diarios
        ORDER BY data DESC
    ''').fetchall()
    conn.close()
 
    streak = 0
    for r in registros:
        if r['bateu_meta'] == 1:
            streak += 1
        else:
            break
    return streak
 
 
def calcular_maior_streak():
    """Percorre todo o histórico (em ordem cronológica) e acha a maior sequência já alcançada."""
    conn = get_db()
    registros = conn.execute('''
        SELECT bateu_meta FROM registros_diarios
        ORDER BY data ASC
    ''').fetchall()
    conn.close()
 
    maior = 0
    atual = 0
    for r in registros:
        if r['bateu_meta'] == 1:
            atual += 1
            maior = max(maior, atual)
        else:
            atual = 0
    return maior
 
 
if __name__ == '__main__':
    init_db()
    print(f'Banco de dados "{DB_NAME}" pronto.')
