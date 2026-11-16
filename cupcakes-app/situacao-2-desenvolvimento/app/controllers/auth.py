"""Controller: cadastro, login e logout."""
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from ..models import usuario
from ..utils import destino_seguro

bp = Blueprint("auth", __name__)


@bp.before_app_request
def carregar_usuario():
    uid = session.get("usuario_id")
    g.user = usuario.buscar_por_id(uid) if uid else None


@bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome, email = request.form.get("nome", ""), request.form.get("email", "")
        senha, telefone = request.form.get("senha", ""), request.form.get("telefone", "")
        erros = usuario.validar_cadastro(nome, email, senha)
        if not erros:
            novo_id = usuario.criar(nome, email, senha, telefone or None)
            if novo_id is None:
                erros.append("Este e-mail já tem cadastro. Entre na sua conta.")
            else:
                session.clear()
                session["usuario_id"] = novo_id
                flash("Cadastro feito. Bem-vindo!", "ok")
                return redirect(url_for("loja.index"))
        for erro in erros:
            flash(erro, "erro")
    return render_template("cadastro.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = usuario.autenticar(request.form.get("email"), request.form.get("senha"))
        if u:
            session.clear()
            session["usuario_id"] = u["id"]
            return redirect(destino_seguro(request.args.get("proximo")))
        flash("E-mail ou senha incorretos. Confira e tente de novo.", "erro")
    return render_template("login.html")


@bp.route("/sair", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("loja.index"))
