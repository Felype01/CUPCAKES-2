"""Model: produto (sabor de cupcake)."""
import re

from ..db import get_db

COR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")


def validar(nome, preco_centavos, cor):
    erros = []
    if len((nome or "").strip()) < 2:
        erros.append("Informe o nome do sabor.")
    if not isinstance(preco_centavos, int) or preco_centavos <= 0:
        erros.append("Informe um preço maior que zero, como 12,50.")
    if not COR_RE.match(cor or ""):
        erros.append("Escolha uma cor de glacê válida.")
    return erros


def converter_preco(texto):
    """'12,50' -> 1250. Retorna None se inválido."""
    try:
        return round(float((texto or "").replace(",", ".")) * 100)
    except ValueError:
        return None


def listar(apenas_ativos=True):
    sql = "SELECT * FROM produto" + (" WHERE ativo = 1" if apenas_ativos else "") + " ORDER BY nome"
    return get_db().execute(sql).fetchall()


def buscar(produto_id):
    return get_db().execute("SELECT * FROM produto WHERE id = ?", (produto_id,)).fetchone()


def criar(nome, descricao, preco_centavos, cor_glace):
    db = get_db()
    cur = db.execute(
        "INSERT INTO produto (nome, descricao, preco_centavos, cor_glace) VALUES (?, ?, ?, ?)",
        (nome.strip(), descricao, preco_centavos, cor_glace),
    )
    db.commit()
    return cur.lastrowid


def atualizar(produto_id, nome, descricao, preco_centavos, cor_glace):
    db = get_db()
    db.execute(
        "UPDATE produto SET nome = ?, descricao = ?, preco_centavos = ?, cor_glace = ? WHERE id = ?",
        (nome.strip(), descricao, preco_centavos, cor_glace, produto_id),
    )
    db.commit()


def alternar_ativo(produto_id):
    db = get_db()
    db.execute("UPDATE produto SET ativo = 1 - ativo WHERE id = ?", (produto_id,))
    db.commit()
