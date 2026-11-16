from app.models import pedido, produto, usuario
from tests.base import BaseTestCase


class UsuarioTests(BaseTestCase):
    def test_criar_e_autenticar(self):
        with self.app.app_context():
            self.assertIsNotNone(usuario.criar("Ana Lima", "Ana@Exemplo.com", "segredo1"))
            self.assertIsNotNone(usuario.autenticar("ana@exemplo.com", "segredo1"))
            self.assertIsNone(usuario.autenticar("ana@exemplo.com", "errada"))

    def test_email_duplicado_retorna_none(self):
        with self.app.app_context():
            usuario.criar("Ana Lima", "ana@exemplo.com", "segredo1")
            self.assertIsNone(usuario.criar("Outra Ana", "ana@exemplo.com", "segredo2"))

    def test_senha_nao_e_guardada_em_texto_puro(self):
        with self.app.app_context():
            usuario.criar("Ana Lima", "ana@exemplo.com", "segredo1")
            self.assertNotIn("segredo1", usuario.buscar_por_email("ana@exemplo.com")["senha_hash"])

    def test_validacao_de_cadastro(self):
        self.assertEqual(len(usuario.validar_cadastro("", "invalido", "123")), 3)
        self.assertEqual(usuario.validar_cadastro("Ana", "a@b.com", "123456"), [])


class ProdutoTests(BaseTestCase):
    def test_converter_preco(self):
        self.assertEqual(produto.converter_preco("12,50"), 1250)
        self.assertEqual(produto.converter_preco("9"), 900)
        self.assertIsNone(produto.converter_preco("abc"))

    def test_validar_rejeita_preco_zero_e_cor_invalida(self):
        self.assertEqual(len(produto.validar("Ok", 0, "vermelho")), 2)
        self.assertEqual(produto.validar("Ok", 100, "#A3214F"), [])

    def test_alternar_ativo_tira_do_cardapio(self):
        with self.app.app_context():
            pid = produto.listar()[0]["id"]
            total = len(produto.listar())
            produto.alternar_ativo(pid)
            self.assertEqual(len(produto.listar()), total - 1)
            produto.alternar_ativo(pid)
            self.assertEqual(len(produto.listar()), total)


class PedidoTests(BaseTestCase):
    def test_criar_pedido_calcula_total_e_status_inicial(self):
        with self.app.app_context():
            uid = usuario.criar("Ana Lima", "ana@exemplo.com", "segredo1")
            p1, p2 = produto.listar()[:2]
            pid = pedido.criar(uid, "Rua A, 10, Centro", [(p1, 2), (p2, 1)])
            ped = pedido.listar_por_usuario(uid)[0]
            self.assertEqual(ped["id"], pid)
            self.assertEqual(ped["status"], "Recebido")
            self.assertEqual(ped["total_centavos"], 2 * p1["preco_centavos"] + p2["preco_centavos"])
            self.assertEqual(len(ped["itens"]), 2)

    def test_status_invalido_e_recusado(self):
        with self.app.app_context():
            uid = usuario.criar("Ana Lima", "ana@exemplo.com", "segredo1")
            pid = pedido.criar(uid, "Rua A, 10, Centro", [(produto.listar()[0], 1)])
            self.assertFalse(pedido.atualizar_status(pid, "Voou"))
            self.assertTrue(pedido.atualizar_status(pid, "Em preparo"))
