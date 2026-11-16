"""Controller: catálogo, carrinho e pedidos do cliente."""
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from ..models import pedido, produto
from ..utils import login_required

bp = Blueprint("loja", __name__)
LIMITE_POR_ITEM = 24


@bp.app_context_processor
def contador_carrinho():
    return {"qtd_carrinho": sum(session.get("carrinho", {}).values())}


def _carrinho_detalhado():
    itens, total = [], 0
    for pid, qtd in session.get("carrinho", {}).items():
        p = produto.buscar(int(pid))
        if p and p["ativo"]:
            itens.append({"produto": p, "quantidade": qtd, "subtotal": p["preco_centavos"] * qtd})
            total += p["preco_centavos"] * qtd
    return itens, total


@bp.route("/")
def index():
    return render_template("index.html", produtos=produto.listar())


@bp.route("/carrinho")
def carrinho():
    itens, total = _carrinho_detalhado()
    return render_template("carrinho.html", itens=itens, total=total)


@bp.route("/carrinho/adicionar/<int:produto_id>", methods=["POST"])
def adicionar(produto_id):
    p = produto.buscar(produto_id)
    if not p or not p["ativo"]:
        flash("Este sabor não está disponível.", "erro")
        return redirect(url_for("loja.index"))
    cart = session.get("carrinho", {})
    cart[str(produto_id)] = min(cart.get(str(produto_id), 0) + 1, LIMITE_POR_ITEM)
    session["carrinho"] = cart
    flash(f"{p['nome']} foi para o carrinho.", "ok")
    return redirect(request.referrer or url_for("loja.index"))


@bp.route("/carrinho/remover/<int:produto_id>", methods=["POST"])
def remover(produto_id):
    cart = session.get("carrinho", {})
    cart.pop(str(produto_id), None)
    session["carrinho"] = cart
    return redirect(url_for("loja.carrinho"))


@bp.route("/carrinho/finalizar", methods=["POST"])
@login_required
def finalizar():
    itens, _ = _carrinho_detalhado()
    endereco = request.form.get("endereco", "").strip()
    if not itens:
        flash("Seu carrinho está vazio. Escolha um sabor para começar.", "erro")
        return redirect(url_for("loja.index"))
    if len(endereco) < 8:
        flash("Informe o endereço de entrega completo (rua, número e bairro).", "erro")
        return redirect(url_for("loja.carrinho"))
    pedido.criar(g.user["id"], endereco, [(i["produto"], i["quantidade"]) for i in itens])
    session.pop("carrinho", None)
    flash("Pedido recebido! Acompanhe o andamento nesta página.", "ok")
    return redirect(url_for("loja.meus_pedidos"))


@bp.route("/pedidos")
@login_required
def meus_pedidos():
    return render_template("pedidos.html", pedidos=pedido.listar_por_usuario(g.user["id"]))
