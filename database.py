import sqlite3
from datetime import datetime, timedelta

DB_NAME = 'protein_tracker.db'

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        objetivo TEXT NOT NULL,
        meta_min REAL NOT NULL,
        meta_max REAL NOT NULL
        )
    ''')
    conn.execute('''
            CREATE TABLE IF NOT EXISTS registros_diarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            proteina_consumida REAL NOT NULL,
            meta_proteina REAL NOT NULL,
            bateu_meta INTEGER NOT NULL,
            UNIQUE(usuario_id, data),
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS itens_consumidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            refeicao TEXT NOT NULL,
            alimento TEXT NOT NULL,
            gramas REAL NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')

    conn.commit()
    conn.close()

def criar_usuario(nome, objetivo, meta_min, meta_max):
    conn = get_db()
    cursor = conn.execute('''
        INSERT INTO usuarios (nome, objetivo, meta_min, meta_max)
        VALUES (?, ?, ?, ?)
    ''', (nome, objetivo, meta_min, meta_max))
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()
    return novo_id

def listar_usuarios():
    conn = get_db()
    usuarios = conn.execute('SELECT * FROM usuarios ORDER BY nome').fetchall()
    conn.close()
    return usuarios

def buscar_usuario(usuario_id):
    conn = get_db()
    usuario = conn.execute('SELECT * FROM usuarios WHERE id = ?', (usuario_id,)).fetchone()
    conn.close()
    return usuario

def salvar_registro(usuario_id, data, proteina_consumida, meta_proteina):
    bateu = 1 if proteina_consumida >= meta_proteina else 0
    conn = get_db()
    conn.execute('''
        INSERT INTO registros_diarios (usuario_id, data, proteina_consumida, meta_proteina, bateu_meta)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(usuario_id, data) DO UPDATE SET
            proteina_consumida = excluded.proteina_consumida,
            meta_proteina = excluded.meta_proteina,
            bateu_meta = excluded.bateu_meta
    ''', (usuario_id, data, proteina_consumida, meta_proteina, bateu))
    conn.commit()
    conn.close()

def listar_registros(usuario_id,limite=30):
    conn = get_db()
    registros = conn.execute('''
        SELECT * FROM registros_diarios
        WHERE usuario_id = ?
        ORDER BY data DESC
        LIMIT ?
    ''', (usuario_id, limite,)).fetchall()
    conn.close()
    return registros

def buscar_registro_dia(usuario_id, data):
    conn = get_db()
    registro = conn.execute('''
        SELECT * FROM registros_diarios WHERE usuario_id = ? AND data = ?
    ''', (usuario_id, data)).fetchone()
    conn.close()
    return registro

def calcular_streak_atual(usuario_id):
    conn = get_db()
    registros = conn.execute('''
        SELECT data, bateu_meta FROM registros_diarios
        WHERE usuario_id = ?
        ORDER BY data DESC
    ''', (usuario_id,)).fetchall()
    conn.close()

    streak = 0
    data_esperada = None
    for r in registros:
        data_atual = datetime.strptime(r['data'], "%Y-%m-%d").date()

        if data_esperada is not None and data_atual != data_esperada:
            break

        if r['bateu_meta'] != 1:
            break

        streak += 1
        data_esperada = data_atual - timedelta(days=1)

    return streak


def calcular_maior_streak(usuario_id):
    conn = get_db()
    registros = conn.execute('''
        SELECT data, bateu_meta FROM registros_diarios
        WHERE usuario_id = ?
        ORDER BY data ASC
    ''', (usuario_id,)).fetchall()
    conn.close()

    maior = 0
    atual = 0
    data_anterior = None
    for r in registros:
        data_atual = datetime.strptime(r['data'], "%Y-%m-%d").date()

        if r['bateu_meta'] == 1:
            if data_anterior is not None and data_atual == data_anterior + timedelta(days=1):
                atual += 1
            else:
                atual = 1
            maior = max(maior, atual)
        else:
            atual = 0

        data_anterior = data_atual

    return maior

def calcular_media_geral(usuario_id):
    conn = get_db()
    registros = conn.execute('''
        SELECT proteina_consumida FROM registros_diarios WHERE usuario_id = ?
    ''', (usuario_id,)).fetchall()
    conn.close()
    if not registros:
        return 0
    total = sum(r['proteina_consumida'] for r in registros)
    return round(total / len(registros), 1)


def calcular_media_ultimos_dias(usuario_id, dias=7):
    conn = get_db()
    registros = conn.execute('''
        SELECT proteina_consumida FROM registros_diarios
        WHERE usuario_id = ?
        ORDER BY data DESC
        LIMIT ?
    ''', (usuario_id, dias)).fetchall()
    conn.close()
    if not registros:
        return 0
    total = sum(r['proteina_consumida'] for r in registros)
    return round(total / len(registros), 1)


def listar_registros_grafico(usuario_id, dias=30):
    conn = get_db()
    registros = conn.execute('''
        SELECT data, proteina_consumida, meta_proteina, bateu_meta FROM registros_diarios
        WHERE usuario_id = ?
        ORDER BY data DESC
        LIMIT ?
    ''', (usuario_id, dias)).fetchall()
    conn.close()
    return list(reversed(registros))

def adicionar_item(usuario_id, data, refeicao, alimento, gramas):
    conn = get_db()
    conn.execute('''
        INSERT INTO itens_consumidos (usuario_id, data, refeicao, alimento, gramas)
        VALUES (?, ?, ?, ?, ?)
    ''', (usuario_id, data, refeicao, alimento, gramas))
    conn.commit()
    conn.close()


def listar_itens_dia(usuario_id, data):
    conn = get_db()
    itens = conn.execute('''
        SELECT * FROM itens_consumidos
        WHERE usuario_id = ? AND data = ?
        ORDER BY id ASC
    ''', (usuario_id, data)).fetchall()
    conn.close()
    return itens


def remover_item(item_id, usuario_id):
    conn = get_db()
    conn.execute('DELETE FROM itens_consumidos WHERE id = ? AND usuario_id = ?', (item_id, usuario_id))
    conn.commit()
    conn.close()


def somar_consumo_dia(usuario_id, data):
    conn = get_db()
    resultado = conn.execute('''
        SELECT SUM(gramas) as total FROM itens_consumidos
        WHERE usuario_id = ? AND data = ?
    ''', (usuario_id, data)).fetchone()
    conn.close()
    return resultado['total'] if resultado['total'] else 0.0
 
if __name__ == '__main__':
    init_db()
    print(f'Banco de dados "{DB_NAME}" pronto.')
    