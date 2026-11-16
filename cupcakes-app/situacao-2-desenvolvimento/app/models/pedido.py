"""Model: pedido e itens do pedido."""
from ..db import get_db

STATUS = ("Recebido", "Em preparo", "Pronto", "Entregue", "Cancelado")


def criar(usuario_id, endereco, itens):
    """itens: lista de (produto_row, quantidade). Retorna o id do pedido."""
    db = get_db()
    total = sum(p["preco_centavos"] * q for p, q in itens)
    cur = db.execute(
        "INSERT INTO pedido (usuario_id, status, total_centavos, endereco_entrega) VALUES (?, 'Recebido', ?, ?)",
        (usuario_id, total, endereco),
    )
    pedido_id = cur.lastrowid
    db.executemany(
        "INSERT INTO item_pedido (pedido_id, produto_id, quantidade, preco_unitario_centavos) VALUES (?, ?, ?, ?)",
        [(pedido_id, p["id"], q, p["preco_centavos"]) for p, q in itens],
    )
    db.commit()
    return pedido_id


def _com_itens(linhas):
    db = get_db()
    pedidos = []
    for linha in linhas:
        p = dict(linha)
        p["itens"] = db.execute(
            "SELECT i.quantidade, i.preco_unitario_centavos, pr.nome FROM item_pedido i "
            "JOIN produto pr ON pr.id = i.produto_id WHERE i.pedido_id = ?", (p["id"],)
        ).fetchall()
        pedidos.append(p)
    return pedidos


def listar_por_usuario(usuario_id):
    linhas = get_db().execute(
        "SELECT * FROM pedido WHERE usuario_id = ? ORDER BY id DESC", (usuario_id,)).fetchall()
    return _com_itens(linhas)


def listar_todos():
    linhas = get_db().execute(
        "SELECT p.*, u.nome AS cliente FROM pedido p JOIN usuario u ON u.id = p.usuario_id "
        "ORDER BY p.id DESC").fetchall()
    return _com_itens(linhas)


def atualizar_status(pedido_id, status):
    """Retorna False se o status for inválido."""
    if status not in STATUS:
        return False
    db = get_db()
    db.execute("UPDATE pedido SET status = ? WHERE id = ?", (status, pedido_id))
    db.commit()
    return True
