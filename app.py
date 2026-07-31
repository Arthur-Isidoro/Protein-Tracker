from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "chave-so-para-testes-locais"


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

    if request.method == "POST":
        nome = request.form.get("nome", "").strip().capitalize()
        objetivo = request.form.get("objetivo", "").strip().lower()

        try:
            peso = float(request.form.get("peso", ""))
        except ValueError:
            erro = "Digite um peso válido (ex: 72.5)."
            return render_template("cadastro.html", erro=erro)

        meta_min, meta_max = calcular_meta(peso, objetivo)

        if meta_min is None:
            erro = 'Objetivo não reconhecido. Escolha "Manutenção", "Ganho de massa" ou "Perda de gordura".'
            return render_template("cadastro.html", erro=erro)

        # guarda tudo na sessão, assim a pessoa navega entre páginas sem perder o progresso
        session["nome"] = nome
        session["objetivo"] = objetivo
        session["meta_min"] = meta_min
        session["meta_max"] = meta_max
        session["consumo"] = 0.0

        return redirect(url_for("tracker"))

    return render_template("cadastro.html", erro=erro)


@app.route("/tracker", methods=["GET", "POST"])
def tracker():
    if "meta_min" not in session:
        return redirect(url_for("cadastro"))

    if request.method == "POST":
        try:
            consumida = float(request.form.get("consumida", ""))
            session["consumo"] += consumida
        except ValueError:
            pass  # ignora entradas inválidas, mantém o consumo como estava

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
    )


@app.route("/reiniciar")
def reiniciar():
    session.clear()
    return redirect(url_for("cadastro"))


if __name__ == "__main__":
    app.run(debug=True)
