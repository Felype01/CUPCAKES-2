# Glacê & Cia: aplicativo para loja de cupcakes gourmet

Projeto Integrador Transdisciplinar em Engenharia de Software II (PIT II), continuação do PIT I
("Desenvolvimento de um aplicativo mobile para uma loja de cupcakes gourmet").

**Autor:** Felype Torres Silva e Sousa, RGM 34744002

O aplicativo digitaliza a jornada de compra do cliente: ver o cardápio, montar o carrinho, fazer o pedido
e acompanhar o andamento. A loja gerencia sabores e atualiza o status dos pedidos em um painel.

## Estrutura do repositório

| Pasta | Conteúdo | Desafio |
|---|---|---|
| `situacao-1-planejamento/` | Escopo revisado, requisitos, UML, IHC, modelo de dados, script SQL e dicionário de dados | Situação 1 |
| `situacao-2-desenvolvimento/` | Código (front-end e back-end em MVC), testes automatizados e manual de uso | Situação 2 |
| `situacao-3-testes/` | Formulário de teste, relatórios dos 5 testadores, laudo de qualidade e evidências | Situação 3 |

## Tecnologias

- **Back-end:** Python 3 + Flask, padrão MVC (`models/`, `controllers/`, `templates/`)
- **Banco de dados:** SQLite 3
- **Front-end:** HTML, CSS e JavaScript, responsivo e instalável no celular (PWA)
- **Testes:** pytest (a suíte usa `unittest`, que o pytest executa normalmente)
- **Modo de codificação:** tradicional

## Como rodar

```bash
cd situacao-2-desenvolvimento
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
flask --app run init-db
flask --app run seed
python run.py                                          # abre em http://127.0.0.1:5000
pytest                                                 # roda os testes
```

Conta da loja criada pelo `seed`: `admin@cupcakeria.com` / `admin123`. **Troque a senha antes de publicar.**

## Metodologia

Scrum com entregas em sprints, backlog no Trello, diagramas no Draw.io e wireframes no Balsamiq (PIT I).
No PIT II, as três situações foram tratadas como três sprints. Ver `situacao-1-planejamento/escopo-revisado.md`.
