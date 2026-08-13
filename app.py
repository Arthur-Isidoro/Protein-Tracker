from flask import Flask, render_template, request, redirect, url_for, session
from datetime import date
import database
import sqlite3

app = Flask(__name__)
app.secret_key = "chave-so-para-testes-locais"

database.init_db()

def entrar_como(usuario):
    session["usuario_id"] = usuario["id"]
    session["nome"] = usuario["nome"]
    session["objetivo"] = usuario["objetivo"]
    session["meta_min"] = usuario["meta_min"]
    session["meta_max"] = usuario["meta_max"]

    hoje = date.today().isoformat()
    registro_hoje = database.buscar_registro_dia(usuario["id"], hoje)
    session["consumo"] = registro_hoje["proteina_consumida"] if registro_hoje else 0.0

def calcular_meta(peso, objetivo):
    if objetivo in ["manutencao", "manutenção"]:
        return peso * 1.6, peso * 1.6
    elif objetivo == "ganho de massa":
        return peso * 1.8, peso * 2.2
    elif objetivo == "perda de gordura":
        return peso * 2.0, peso * 2.4
    else:
        return None, None


@app.route("/", methods=["GET", "POST"])
def cadastro():
    erro = None
    usuarios = database.listar_usuarios()

    if request.method == "POST":
        nome = request.form.get("nome", "").strip().capitalize()
        objetivo = request.form.get("objetivo", "").strip().lower()

        try:
            peso = float(request.form.get("peso", ""))
        except ValueError:
            erro = "Digite um peso válido (ex: 72.5)."
            return render_template("cadastro.html", erro=erro, usuarios=usuarios)

        meta_min, meta_max = calcular_meta(peso, objetivo)

        if meta_min is None:
            erro = 'Objetivo não reconhecido. Escolha "Manutenção", "Ganho de massa" ou "Perda de gordura".'
            return render_template("cadastro.html", erro=erro, usuarios=usuarios)

        try:
            novo_id = database.criar_usuario(nome, objetivo, meta_min, meta_max)
        except sqlite3.IntegrityError:
            erro = f'Já existe um usuário chamado "{nome}". Escolha outro nome ou selecione ele na lista.'
            return render_template("cadastro.html", erro=erro, usuarios=usuarios)

        usuario = database.buscar_usuario(novo_id)
        entrar_como(usuario)
        return redirect(url_for("tracker"))

    return render_template("cadastro.html", erro=erro, usuarios=usuarios)


@app.route("/selecionar/<int:usuario_id>")
def selecionar_usuario(usuario_id):
    usuario = database.buscar_usuario(usuario_id)
    if usuario is None:
        return redirect(url_for("cadastro"))
    entrar_como(usuario)
    return redirect(url_for("tracker"))


@app.route("/trocar-usuario")
def trocar_usuario():
    session.clear()
    return redirect(url_for("cadastro"))


@app.route("/tracker", methods=["GET", "POST"])
def tracker():
    if "usuario_id" not in session:
        return redirect(url_for("cadastro"))

    if request.method == "POST":
        try:
            consumida = float(request.form.get("consumida", ""))
            session["consumo"] += consumida
        except ValueError:
            pass

    meta_min = session["meta_min"]
    meta_max = session["meta_max"]
    consumo = session["consumo"]

    faixa_unica = meta_min == meta_max
    if faixa_unica:
        meta_batida = consumo >= meta_min
        restante = max(meta_min - consumo, 0)
        progresso = min(consumo / meta_min * 100, 100) if meta_min else 0
    else:
        meta_batida = consumo >= meta_min
        meta_max_batida = consumo >= meta_max
        restante = max(meta_min - consumo, 0)
        progresso = min(consumo / meta_max * 100, 100) if meta_max else 0

    streak_atual = database.calcular_streak_atual(session["usuario_id"])

    return render_template(
        "tracker.html",
        nome=session["nome"],
        objetivo=session["objetivo"],
        meta_min=meta_min,
        meta_max=meta_max,
        consumo=consumo,
        faixa_unica=faixa_unica,
        meta_batida=meta_batida,
        meta_max_batida=None if faixa_unica else meta_max_batida,
        restante=restante,
        progresso=progresso,
        streak_atual=streak_atual,
    )

@app.route('/registrar', methods=['POST'])
def registrar():
    if "usuario_id" not in session:
        return redirect(url_for("cadastro"))

    hoje = date.today().isoformat()
    meta = session["meta_max"] if session["meta_min"] != session["meta_max"] else session["meta_min"]

    database.salvar_registro(session["usuario_id"], hoje, session["consumo"], meta)

    return redirect(url_for('historico'))

@app.route('/historico')
def historico():
    if "usuario_id" not in session:
        return redirect(url_for("cadastro"))

    usuario_id = session["usuario_id"]
    registros = database.listar_registros(usuario_id, limite=30)
    streak_atual = database.calcular_streak_atual(usuario_id)
    maior_streak = database.calcular_maior_streak(usuario_id)

    total_dias = len(registros)
    dias_batidos = sum(1 for r in registros if r["bateu_meta"] == 1)
    percentual = round((dias_batidos / total_dias) * 100, 1) if total_dias else 0

    return render_template(
        'historico.html',
        nome=session["nome"],
        registros=registros,
        streak_atual=streak_atual,
        maior_streak=maior_streak,
        total_dias=total_dias,
        dias_batidos=dias_batidos,
        percentual=percentual,
    )

@app.route("/reiniciar")
def reiniciar():
    session["consumo"] = 0.0
    return redirect(url_for("tracker"))



if __name__ == "__main__":
    app.run(debug=True)
