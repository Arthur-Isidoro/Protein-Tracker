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


usuario_teste = pegar_ou_criar_usuario("Teste", "ganho de massa", 140, 170)

meta_teste = 140
hoje = date.today()

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

for i, consumo in enumerate(reversed(consumos_teste)):
    dias_atras = i + 1
    data_str = (hoje - timedelta(days=dias_atras)).isoformat()
    database.salvar_registro(usuario_teste, data_str, consumo, meta_teste)

itens_hoje = [
    ("Café da manhã", "Ovos (2 unidades)", 12),
    ("Café da manhã", "Iogurte grego", 10),
    ("Almoço", "Peito de frango", 45),
    ("Almoço", "Arroz e feijão", 8),
    ("Lanche", "Whey protein", 25),
]
data_hoje_str = hoje.isoformat()
for refeicao, alimento, gramas in itens_hoje:
    database.adicionar_item(usuario_teste, data_hoje_str, refeicao, alimento, gramas)

print(f"'Teste': {len(consumos_teste)} dias de histórico + {len(itens_hoje)} itens lançados hoje")


usuario_streak = pegar_ou_criar_usuario("Testestreak", "manutenção", 130, 130)

meta_streak = 130
consumos_streak = [135, 132, 140, 138, 145, 133, 150, 142, 148, 155]

for i, consumo in enumerate(reversed(consumos_streak)):
    dias_atras = i + 1
    data_str = (hoje - timedelta(days=dias_atras)).isoformat()
    database.salvar_registro(usuario_streak, data_str, consumo, meta_streak)

print(f"'TesteStreak': {len(consumos_streak)} dias de histórico, todos batendo a meta (streak de {len(consumos_streak)})")


pegar_ou_criar_usuario("Testezerado", "perda de gordura", 150, 180)
print("'TesteZerado': cadastrado sem histórico (pra testar telas vazias)")


print("\nPronto! Rode o app e selecione 'Teste', 'Testestreak' ou 'Testezerado' na tela inicial.")