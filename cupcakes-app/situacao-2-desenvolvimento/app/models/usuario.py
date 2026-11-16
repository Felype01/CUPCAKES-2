"""Model: usuário (cliente ou administrador)."""
import re
import sqlite3

from werkzeug.security import check_password_hash, generate_password_hash

from ..db import get_db

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validar_cadastro(nome, email, senha):
    erros = []
    if len((nome or "").strip()) < 2:
        erros.append("Informe seu nome com pelo menos 2 letras.")
    if not EMAIL_RE.match(email or ""):
        erros.append("Informe um e-mail válido, como nome@exemplo.com.")
    if len(senha or "") < 6:
        erros.append("A senha precisa ter pelo menos 6 caracteres.")
    return erros


def criar(nome, email, senha, telefone=None, is_admin=False):
    """Retorna o id do novo usuário ou None se o e-mail já existir."""
    db = get_db()
    try:
        cur = db.execute(
            "INSERT INTO usuario (nome, email, senha_hash, telefone, is_admin) VALUES (?, ?, ?, ?, ?)",
            (nome.strip(), email.strip().lower(), generate_password_hash(senha), telefone, int(is_admin)),
        )
        db.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError:
        return None


def buscar_por_id(usuario_id):
    return get_db().execute("SELECT * FROM usuario WHERE id = ?", (usuario_id,)).fetchone()


def buscar_por_email(email):
    return get_db().execute("SELECT * FROM usuario WHERE email = ?", ((email or "").strip().lower(),)).fetchone()


def autenticar(email, senha):
    u = buscar_por_email(email)
    if u and check_password_hash(u["senha_hash"], senha or ""):
        return u
    return None
