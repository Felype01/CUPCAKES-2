# Manual de uso

## Cliente
1. **Ver o cardápio:** a tela inicial mostra os sabores com preço. Toque em **Adicionar ao carrinho**.
2. **Revisar o carrinho:** toque em **Carrinho**. Para tirar um sabor, use **Remover**.
3. **Entrar:** para finalizar é preciso ter conta. Toque em **Entrar** e depois em **Crie sua conta**.
4. **Finalizar:** no carrinho, preencha o endereço (rua, número e bairro) e toque em **Finalizar pedido**.
5. **Acompanhar:** em **Meus pedidos** aparece o status: Recebido, Em preparo, Pronto ou Entregue.

## Loja (administrador)
1. Entre com a conta da loja. O menu mostra **Painel**.
2. **Pedidos:** escolha o novo status e toque em **Atualizar status**.
3. **Sabores:** cadastre, edite ou tire sabores do cardápio. Sabores tirados deixam de aparecer, mas o histórico de pedidos é mantido.

## Instalar no celular
Abra o endereço no navegador do celular e use **Adicionar à tela inicial** (iPhone: botão Compartilhar).

## Problemas comuns
| Mensagem | O que fazer |
|---|---|
| E-mail ou senha incorretos | Confira os dados ou crie uma conta |
| A sessão expirou | Volte, recarregue a página e envie de novo |
| Esta área é exclusiva da equipe | Use uma conta de administrador |

## Hospedagem (para o "link da solução em funcionamento")
Qualquer serviço que rode Python serve (por exemplo Render, Railway ou PythonAnywhere).
- Comando de início: `gunicorn wsgi:app` (adicione `gunicorn` ao `requirements.txt`)
- Variável de ambiente `SECRET_KEY` com um valor longo e aleatório
- Após o primeiro deploy, rode `flask --app run init-db` e `flask --app run seed` no console do serviço
- Atenção: o SQLite grava em arquivo. Em planos gratuitos sem disco persistente, os dados podem ser apagados a cada reinício. Para o vídeo e os testes isso basta; para uso real, migre para PostgreSQL.
