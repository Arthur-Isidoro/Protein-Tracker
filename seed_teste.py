"""
Script pra criar um usuário de teste com histórico
"""
import database

database.init_db()

try:
    usuario_id = database.criar_usuario(
        nome="Teste",
        objetivo="ganho de massa",
        meta_min=140,
        meta_max=170
    )
    print(f"Usuário 'Teste' criado com id {usuario_id}")
except Exception:
    usuario = next((u for u in database.listar_usuarios() if u["nome"] == "Teste"), None)
    usuario_id = usuario["id"]
    print(f"Usuário 'Teste' já existia, usando id {usuario_id}")

registros = [
    ("2026-08-05", 155),
    ("2026-08-06", 160),
    ("2026-08-07", 100),
    ("2026-08-08", 145),
    ("2026-08-09", 150),
    ("2026-08-10", 165),
    ("2026-08-11", 148),
    ("2026-08-12", 120),
    ("2026-08-13", 152),
    ("2026-08-14", 158),
]

meta = 140 

for data, consumo in registros:
    database.salvar_registro(usuario_id, data, consumo, meta)

print(f"{len(registros)} dias de histórico criados para o usuário 'Teste'.")
print(f"Streak atual esperado: 2 (dias 13 e 14)")
print(f"Maior streak esperado: 4 (dias 08, 09, 10 e 11)")