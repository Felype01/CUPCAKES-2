from app.models import pedido
from tests.base import BaseTestCase


class FluxoClienteTests(BaseTestCase):
    def test_catalogo_lista_sabores(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertIn("Red velvet", r.get_data(as_text=True))

    def test_cadastro_com_dados_invalidos_mostra_erro(self):
        r = self.client.post("/cadastro", data={"nome": "A", "email": "x", "senha": "1"})
        self.assertIn("e-mail válido", r.get_data(as_text=True))

    def test_login_incorreto_mostra_mensagem(self):
        r = self.entrar("admin@cupcakeria.com", "errada")
        self.assertIn("incorretos", r.get_data(as_text=True))

    def test_finalizar_exige_login(self):
        r = self.client.post("/carrinho/finalizar", data={"endereco": "Rua A, 10, Centro"})
        self.assertEqual(r.status_code, 302)
        self.assertIn("/login", r.headers["Location"])

    def test_compra_completa(self):
        self.cadastrar_e_entrar()
        self.client.post("/carrinho/adicionar/1")
        self.client.post("/carrinho/adicionar/1")
        self.assertIn("2x", self.client.get("/carrinho").get_data(as_text=True))
        r = self.client.post("/carrinho/finalizar", data={"endereco": "Rua A, 10, Centro"}, follow_redirects=True)
        corpo = r.get_data(as_text=True)
        self.assertIn("Pedido #1", corpo)
        self.assertIn("Recebido", corpo)
        self.assertIn("Seu carrinho está vazio", self.client.get("/carrinho").get_data(as_text=True))

    def test_finalizar_com_carrinho_vazio(self):
        self.cadastrar_e_entrar()
        r = self.client.post("/carrinho/finalizar", data={"endereco": "Rua A, 10, Centro"}, follow_redirects=True)
        self.assertIn("carrinho está vazio", r.get_data(as_text=True))

    def test_endereco_curto_e_recusado(self):
        self.cadastrar_e_entrar()
        self.client.post("/carrinho/adicionar/1")
        r = self.client.post("/carrinho/finalizar", data={"endereco": "Rua"}, follow_redirects=True)
        self.assertIn("endereço de entrega completo", r.get_data(as_text=True))

    def test_produto_inexistente_nao_entra_no_carrinho(self):
        r = self.client.post("/carrinho/adicionar/999", follow_redirects=True)
        self.assertIn("não está disponível", r.get_data(as_text=True))

    def test_login_nao_redireciona_para_site_externo(self):
        r = self.client.post("/login?proximo=//malicioso.com", data={"email": "admin@cupcakeria.com", "senha": "admin123"})
        self.assertNotIn("malicioso", r.headers["Location"])


class AdminTests(BaseTestCase):
    def test_visitante_vai_para_login(self):
        self.assertEqual(self.client.get("/admin/pedidos").status_code, 302)

    def test_cliente_comum_recebe_403(self):
        self.cadastrar_e_entrar()
        self.assertEqual(self.client.get("/admin/pedidos").status_code, 403)

    def test_admin_cadastra_sabor_e_atualiza_status(self):
        self.entrar("admin@cupcakeria.com", "admin123")
        r = self.client.post("/admin/produtos/novo", data={"nome": "Coco", "descricao": "x", "preco": "13,00", "cor_glace": "#FFFFFF"},
                             follow_redirects=True)
        self.assertIn("Coco", r.get_data(as_text=True))
        self.client.post("/carrinho/adicionar/1")
        self.client.post("/carrinho/finalizar", data={"endereco": "Rua A, 10, Centro"})
        self.client.post("/admin/pedidos/1/status", data={"status": "Pronto"})
        with self.app.app_context():
            self.assertEqual(pedido.listar_todos()[0]["status"], "Pronto")

    def test_admin_nao_cadastra_preco_invalido(self):
        self.entrar("admin@cupcakeria.com", "admin123")
        r = self.client.post("/admin/produtos/novo", data={"nome": "Coco", "preco": "0", "cor_glace": "#FFFFFF"})
        self.assertIn("preço maior que zero", r.get_data(as_text=True))


class CsrfTests(BaseTestCase):
    csrf = True

    def test_post_sem_token_e_bloqueado(self):
        self.assertEqual(self.client.post("/login", data={"email": "a@b.com", "senha": "x"}).status_code, 400)

    def test_post_com_token_passa(self):
        self.client.get("/login")
        with self.client.session_transaction() as s:
            token = s["csrf"]
        r = self.client.post("/login", data={"email": "a@b.com", "senha": "x", "csrf_token": token})
        self.assertEqual(r.status_code, 200)
