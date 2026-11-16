"""Decoradores de acesso, proteção CSRF e formatação."""
import functools
import secrets

from flask import abort, current_app, flash, g, redirect, request, session, url_for


def login_required(view):
    @functools.wraps(view)
    def envolvido(*args, **kwargs):
        if g.user is None:
            flash("Entre na sua conta para continuar.", "erro")
            return redirect(url_for("auth.login", proximo=request.path))
        return view(*args, **kwargs)
    return envolvido


def admin_required(view):
    @functools.wraps(view)
    @login_required
    def envolvido(*args, **kwargs):
        if not g.user["is_admin"]:
            abort(403)
        return view(*args, **kwargs)
    return envolvido


def csrf_token():
    if "csrf" not in session:
        session["csrf"] = secrets.token_hex(16)
    return session["csrf"]


def verificar_csrf():
    if request.method == "POST" and current_app.config.get("CSRF_ATIVO", True):
        enviado = request.form.get("csrf_token", "").encode()
        esperado = session.get("csrf", "").encode()
        if not esperado or not secrets.compare_digest(enviado, esperado):
            abort(400)


def formatar_brl(centavos):
    reais, cents = divmod(int(centavos), 100)
    return f"R$ {reais:,}".replace(",", ".") + f",{cents:02d}"


def destino_seguro(caminho):
    """Evita open redirect: só aceita caminhos internos."""
    if caminho and caminho.startswith("/") and not caminho.startswith("//"):
        return caminho
    return url_for("loja.index")
