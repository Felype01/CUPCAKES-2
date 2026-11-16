# Escopo revisado (ciclo de melhoria contínua)

## Resumo do PIT I
- **Situação-problema:** digitalizar a jornada de compra do cliente de uma loja de cupcakes gourmet, mitigando falhas de comunicação entre stakeholders e desenvolvedores.
- **Objetivo:** documentação de requisitos, modelagem UML e prototipagem de interface que atendam usabilidade, regras de negócio e eficiência técnica.
- **Metodologia:** Scrum, com feedback constante do usuário e modelos visuais para evitar ambiguidades.
- **Ferramentas:** Trello (backlog), Draw.io/Lucidchart (UML), Balsamiq (wireframes), Word exportado para PDF.

## O que mudou no PIT II
| Item | PIT I | PIT II (revisão) | Motivo |
|---|---|---|---|
| Plataforma | App mobile | Web responsivo instalável (PWA) | Um único código roda em qualquer celular e é fácil de hospedar e de testar com colegas |
| Entrega | Delivery | Delivery com endereço informado no pedido | Torna o fluxo completo e testável |
| Pagamento | Não detalhado | **Fora do escopo desta versão** (pagamento na entrega) | Reduz risco; fica no backlog |
| Perfis | Cliente e loja | Cliente e administrador | Mesmo conceito, nome técnico |
| Status do pedido | Não detalhado | Recebido, Em preparo, Pronto, Entregue, Cancelado | Define o ciclo de vida do pedido |

## Dentro do escopo
Cadastro e login, cardápio, carrinho, pedido com endereço, acompanhamento de status, painel da loja (sabores e pedidos).

## Fora do escopo (backlog)
Pagamento online, cupons, notificações push, avaliação de sabores, cálculo de frete por região.

## Sprints do PIT II
| Sprint | Situação | Entregas |
|---|---|---|
| 1 | Situação 1 | Esta pasta: documentação revisada, banco físico, dicionário |
| 2 | Situação 2 | Código MVC, testes, manual, vídeo narrado |
| 3 | Situação 3 | Testes com 5 pessoas, correções, laudo, vídeo final |
