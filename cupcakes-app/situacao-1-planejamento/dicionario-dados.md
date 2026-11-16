# Dicionário de dados

## usuario
| Coluna | Tipo | Nulo | Restrições | Descrição |
|---|---|---|---|---|
| id | INTEGER | Não | PK, autoincremento | Identificador |
| nome | TEXT | Não | mín. 2 caracteres | Nome do usuário |
| email | TEXT | Não | UNIQUE | E-mail de acesso (minúsculas) |
| senha_hash | TEXT | Não | | Hash da senha |
| telefone | TEXT | Sim | | Contato |
| is_admin | INTEGER | Não | 0 ou 1; padrão 0 | 1 = equipe da loja |
| criado_em | TEXT | Não | padrão agora | Data do cadastro |

## produto
| Coluna | Tipo | Nulo | Restrições | Descrição |
|---|---|---|---|---|
| id | INTEGER | Não | PK | Identificador |
| nome | TEXT | Não | mín. 2 caracteres | Sabor |
| descricao | TEXT | Sim | | Descrição para o cardápio |
| preco_centavos | INTEGER | Não | > 0 | Preço em centavos (1200 = R$ 12,00) |
| cor_glace | TEXT | Não | padrão `#A3214F` | Cor hexadecimal do glacê na ilustração |
| ativo | INTEGER | Não | 0 ou 1; padrão 1 | 1 = aparece no cardápio |
| criado_em | TEXT | Não | padrão agora | Data de cadastro |

## pedido
| Coluna | Tipo | Nulo | Restrições | Descrição |
|---|---|---|---|---|
| id | INTEGER | Não | PK | Número do pedido |
| usuario_id | INTEGER | Não | FK → usuario.id, RESTRICT | Cliente |
| status | TEXT | Não | lista de 5 valores; padrão Recebido | Andamento |
| total_centavos | INTEGER | Não | >= 0 | Total em centavos |
| endereco_entrega | TEXT | Não | | Endereço informado |
| criado_em | TEXT | Não | padrão agora | Data do pedido |

## item_pedido
| Coluna | Tipo | Nulo | Restrições | Descrição |
|---|---|---|---|---|
| id | INTEGER | Não | PK | Identificador |
| pedido_id | INTEGER | Não | FK → pedido.id, CASCADE | Pedido |
| produto_id | INTEGER | Não | FK → produto.id, RESTRICT | Sabor |
| quantidade | INTEGER | Não | > 0 | Unidades |
| preco_unitario_centavos | INTEGER | Não | > 0 | Preço no momento da compra |
| | | | UNIQUE (pedido_id, produto_id) | Um sabor por linha |

## Índices
`idx_pedido_usuario` (pedido.usuario_id), `idx_pedido_status` (pedido.status), `idx_item_pedido` (item_pedido.pedido_id).
