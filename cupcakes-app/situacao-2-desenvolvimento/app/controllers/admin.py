"""Controller: painel da loja (produtos e pedidos)."""
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from ..models import pedido, produto
from ..utils import admin_required

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/produtos")
@admin_required
def produtos():
    return render_template("admin/produtos.html", produtos=produto.listar(apenas_ativos=False))


def _ler_formulario():
    nome = request.form.get("nome", "")
    descricao = request.form.get("descricao", "").strip()
    preco = produto.converter_preco(request.form.get("preco"))
    cor = request.form.get("cor_glace", "")
    return nome, descricao, preco, cor, produto.validar(nome, preco, cor)


@bp.route("/produtos/novo", methods=["GET", "POST"])
@admin_required
def novo_produto():
    if request.method == "POST":
        nome, descricao, preco, cor, erros = _ler_formulario()
        if not erros:
            produto.criar(nome, descricao, preco, cor)
            flash("Sabor cadastrado.", "ok")
            return redirect(url_for("admin.produtos"))
        for e in erros:
            flash(e, "erro")
    return render_template("admin/produto_form.html", produto=None)


@bp.route("/produtos/<int:produto_id>/editar", methods=["GET", "POST"])
@admin_required
def editar_produto(produto_id):
    p = produto.buscar(produto_id)
    if p is None:
        abort(404)
    if request.method == "POST":
        nome, descricao, preco, cor, erros = _ler_formulario()
        if not erros:
            produto.atualizar(produto_id, nome, descricao, preco, cor)
            flash("Sabor atualizado.", "ok")
            return redirect(url_for("admin.produtos"))
        for e in erros:
            flash(e, "erro")
    return render_template("admin/produto_form.html", produto=p)


@bp.route("/produtos/<int:produto_id>/alternar", methods=["POST"])
@admin_required
def alternar_produto(produto_id):
    if produto.buscar(produto_id) is None:
        abort(404)
    produto.alternar_ativo(produto_id)
    return redirect(url_for("admin.produtos"))


@bp.route("/pedidos")
@admin_required
def pedidos():
    return render_template("admin/pedidos.html", pedidos=pedido.listar_todos(), status_lista=pedido.STATUS)


@bp.route("/pedidos/<int:pedido_id>/status", methods=["POST"])
@admin_required
def atualizar_status(pedido_id):
    if pedido.atualizar_status(pedido_id, request.form.get("status", "")):
        flash(f"Pedido #{pedido_id} atualizado.", "ok")
    else:
        flash("Status inválido.", "erro")
    return redirect(url_for("admin.pedidos"))
