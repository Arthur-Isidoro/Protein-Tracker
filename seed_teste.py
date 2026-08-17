"""
Script pra criar 3 usuários de teste com histórico
"""
from datetime import date, timedelta
import database

database.init_db()


def pegar_ou_criar_usuario(nome, objetivo, meta_min, meta_max):
    usuario = next((u for u in database.listar_usuarios() if u["nome"] == nome), None)
    if usuario:
        print(f"Usuário '{nome}' já existia, usando id {usuario['id']}")
        return usuario["id"]
    novo_id = database.criar_usuario(nome, objetivo, meta_min, meta_max)
    print(f"Usuário '{nome}' criado com id {novo_id}")
    return novo_id


MEAL_PLAN = [
    ("Café da manhã", [("Ovos (2 unidades)", 0.12), ("Iogurte grego", 0.08)]),
    ("Almoço", [("Peito de frango", 0.30), ("Arroz e feijão", 0.08)]),
    ("Lanche", [("Whey protein", 0.15)]),
    ("Jantar", [("Salmão grelhado", 0.20), ("Batata doce", 0.07)]),
]


def limpar_itens_dia(usuario_id, data_str):
    for item in database.listar_itens_dia(usuario_id, data_str):
        database.remover_item(item["id"], usuario_id)


def lancar_refeicoes(usuario_id, data_str, total):
    limpar_itens_dia(usuario_id, data_str)
    soma_real = 0.0
    for refeicao, itens in MEAL_PLAN:
        for alimento, fracao in itens:
            gramas = round(total * fracao, 1)
            if gramas <= 0:
                continue
            database.adicionar_item(usuario_id, data_str, refeicao, alimento, gramas)
            soma_real += gramas
    return round(soma_real, 1)


usuario_teste = pegar_ou_criar_usuario("Teste", "ganho de massa", 140, 170)

hoje = date.today()
meta_teste = 140

consumos_teste = [
    130, 145, 150,
    160, 155, 158, 152,
    100,
    148, 151,
    120,
    142, 149, 156, 160, 145,
    110,
    150, 153,
    158,
]

for i, alvo in enumerate(reversed(consumos_teste)):
    dias_atras = i + 1
    data_str = (hoje - timedelta(days=dias_atras)).isoformat()
    total_real = lancar_refeicoes(usuario_teste, data_str, alvo)
    database.salvar_registro(usuario_teste, data_str, total_real, meta_teste)

data_hoje_str = hoje.isoformat()
total_hoje = lancar_refeicoes(usuario_teste, data_hoje_str, 165)

print(f"'Teste': {len(consumos_teste)} dias de histórico com refeições detalhadas + hoje ({total_hoje}g em refeições)")


usuario_streak = pegar_ou_criar_usuario("Testestreak", "manutenção", 130, 130)

meta_streak = 130
consumos_streak = [135, 132, 140, 138, 145, 133, 150, 142, 148, 155]

for i, alvo in enumerate(reversed(consumos_streak)):
    dias_atras = i + 1
    data_str = (hoje - timedelta(days=dias_atras)).isoformat()
    total_real = lancar_refeicoes(usuario_streak, data_str, alvo)
    database.salvar_registro(usuario_streak, data_str, total_real, meta_streak)

print(f"'Testestreak': {len(consumos_streak)} dias de histórico com refeições detalhadas, todos batendo a meta")


pegar_ou_criar_usuario("Testezerado", "perda de gordura", 150, 180)
print("'Testezerado': cadastrado sem histórico")


print("\nPronto! Rode o app e selecione 'Teste', 'Testestreak' ou 'Testezerado' na tela inicial.")