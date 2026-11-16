"""Acesso ao banco de dados (SQLite) e comandos de CLI."""
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_erro=None):
    conexao = g.pop("db", None)
    if conexao is not None:
        conexao.close()


def init_db():
    with current_app.open_resource("schema.sql") as arquivo:
        get_db().executescript(arquivo.read().decode("utf-8"))


SABORES = [
    ("Red velvet", "Massa aveludada com cream cheese e raspas de chocolate branco.", 1200, "#B3213B"),
    ("Brigadeiro belga", "Chocolate belga 54% com cobertura de brigadeiro cremoso.", 1100, "#4A2C2A"),
    ("Limão siciliano", "Massa cítrica, recheio de curd e glacê de limão.", 1000, "#E9D758"),
    ("Pistache", "Pasta de pistache e cobertura de buttercream com nibs.", 1400, "#9CC48A"),
    ("Morango com creme", "Recheio de geleia de morango e chantilly fresco.", 1050, "#F29CB1"),
    ("Doce de leite com flor de sal", "Massa de baunilha e doce de leite artesanal.", 1100, "#C98A4B"),
]


def seed_db():
    """Cria o administrador e alguns sabores de exemplo (idempotente)."""
    from .models import produto, usuario

    if usuario.buscar_por_email("admin@cupcakeria.com") is None:
        usuario.criar("Administrador", "admin@cupcakeria.com", "admin123", is_admin=True)
    if not produto.listar(apenas_ativos=False):
        for nome, descricao, preco, cor in SABORES:
            produto.criar(nome, descricao, preco, cor)


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Cria as tabelas do banco."""
    init_db()
    click.echo("Banco criado.")


@click.command("seed")
@with_appcontext
def seed_command():
    """Insere administrador e sabores de exemplo."""
    seed_db()
    click.echo("Dados de exemplo inseridos. Admin: admin@cupcakeria.com / admin123")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_command)
