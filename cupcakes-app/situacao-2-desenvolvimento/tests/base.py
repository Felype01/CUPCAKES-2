import os
import tempfile
import unittest

from app import create_app, db


class BaseTestCase(unittest.TestCase):
    """Cria um banco SQLite temporário e limpo para cada teste."""
    csrf = False

    def setUp(self):
        self.fd, self.caminho = tempfile.mkstemp(suffix=".sqlite")
        self.app = create_app({"TESTING": True, "DATABASE": self.caminho, "CSRF_ATIVO": self.csrf,
                               "SECRET_KEY": "teste"})
        with self.app.app_context():
            db.init_db()
            db.seed_db()
        self.client = self.app.test_client()

    def tearDown(self):
        os.close(self.fd)
        os.unlink(self.caminho)

    def entrar(self, email, senha):
        return self.client.post("/login", data={"email": email, "senha": senha})

    def cadastrar_e_entrar(self, email="ana@exemplo.com"):
        self.client.post("/cadastro", data={"nome": "Ana Lima", "email": email, "senha": "segredo1"})
