"""Fábrica da aplicação Flask (padrão MVC)."""
import os

from flask import Flask, render_template

from . import db, utils


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-troque-em-producao"),
        DATABASE=os.path.join(app.instance_path, "cupcakes.sqlite"),
        CSRF_ATIVO=True,
    )
    if config:
        app.config.update(config)
    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    app.before_request(utils.verificar_csrf)
    app.context_processor(lambda: {"csrf_token": utils.csrf_token})
    app.template_filter("brl")(utils.formatar_brl)

    from .controllers import admin, auth, loja

    for modulo in (auth, loja, admin):
        app.register_blueprint(modulo.bp)

    @app.errorhandler(403)
    def proibido(_e):
        return render_template("erro.html", codigo=403,
                               mensagem="Esta área é exclusiva da equipe da loja."), 403

    @app.errorhandler(404)
    def nao_encontrado(_e):
        return render_template("erro.html", codigo=404,
                               mensagem="Não encontramos essa página."), 404

    @app.errorhandler(400)
    def requisicao_invalida(_e):
        return render_template("erro.html", codigo=400,
                               mensagem="A sessão expirou. Volte e envie o formulário de novo."), 400

    return app
