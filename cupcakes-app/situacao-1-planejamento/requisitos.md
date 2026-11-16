# Requisitos

## Histórias de usuário
| ID | Como... | Quero... | Para... | Prioridade |
|---|---|---|---|---|
| HU01 | cliente | ver o cardápio com preços | escolher o que comprar | Alta |
| HU02 | cliente | adicionar e remover sabores do carrinho | montar meu pedido | Alta |
| HU03 | cliente | criar conta e entrar | finalizar e acompanhar pedidos | Alta |
| HU04 | cliente | informar o endereço e finalizar o pedido | receber em casa | Alta |
| HU05 | cliente | ver o status dos meus pedidos | saber quando chega | Média |
| HU06 | administrador | cadastrar, editar e ocultar sabores | manter o cardápio atual | Alta |
| HU07 | administrador | ver os pedidos e mudar o status | organizar a produção | Alta |

## Requisitos funcionais
| ID | Descrição | História |
|---|---|---|
| RF01 | Listar sabores ativos com nome, descrição e preço | HU01 |
| RF02 | Manter carrinho na sessão, com limite de 24 unidades por sabor | HU02 |
| RF03 | Cadastrar cliente com nome, e-mail único e senha (mín. 6 caracteres) | HU03 |
| RF04 | Autenticar por e-mail e senha | HU03 |
| RF05 | Criar pedido com itens, total e endereço (mín. 8 caracteres), status inicial "Recebido" | HU04 |
| RF06 | Exigir login para finalizar pedido | HU04 |
| RF07 | Listar pedidos do cliente logado | HU05 |
| RF08 | CRUD de sabores (ocultar em vez de excluir, para preservar histórico) | HU06 |
| RF09 | Listar todos os pedidos e alterar status para valores válidos | HU07 |

## Requisitos não funcionais
| ID | Descrição | Como foi tratado |
|---|---|---|
| RNF01 | Usabilidade em tela pequena | Layout mobile-first, botões de 44 px, rótulos em todos os campos |
| RNF02 | Segurança de senha | Hash com Werkzeug, nunca em texto puro |
| RNF03 | Segurança de formulários | Token CSRF em todo POST; redirecionamento restrito a caminhos internos |
| RNF04 | Controle de acesso | Rotas `/admin` só para administradores (403 para clientes) |
| RNF05 | Integridade dos dados | Chaves estrangeiras, CHECK e UNIQUE no banco |
| RNF06 | Manutenibilidade | Padrão MVC e testes automatizados |
| RNF07 | Acessibilidade | Link "pular para o conteúdo", foco visível, contraste, respeita `prefers-reduced-motion` |

## Regras de negócio
- RN01: o preço do item é copiado para o pedido no momento da compra (mudar o preço depois não altera pedidos antigos).
- RN02: sabor oculto não aparece no cardápio nem pode ser comprado.
- RN03: status válidos: Recebido, Em preparo, Pronto, Entregue, Cancelado.
- RN04: valores monetários são guardados em centavos (inteiro), evitando erro de arredondamento.
