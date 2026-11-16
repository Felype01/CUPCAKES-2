# Laudo de qualidade

## 1. Verificação e validação (Modelo V)
| Nível | Teste | Evidência | Resultado |
|---|---|---|---|
| Unitário | `tests/test_models.py` (usuário, produto, pedido) | saída do `pytest` | Aprovado: 24 testes em conjunto com os de rotas |
| Integração / sistema | `tests/test_rotas.py` (compra completa, painel, CSRF, permissões) | saída do `pytest` | Aprovado |
| Aceitação | Relatórios dos 5 testadores | `relatorios-testadores.md` | Preencher |

Para gerar a evidência: `cd situacao-2-desenvolvimento && pytest -v` e salvar um print em `evidencias/`.

## 2. Erros encontrados e correções
Preencher com o que os testadores relataram. Uma linha por problema.

| # | Erro relatado | Quem relatou | Gravidade | Correção feita | Evidência (print) | Status |
|---|---|---|---|---|---|---|
| 1 | | | | | `evidencias/` | |

## 3. Sugestões aceitas e recusadas
| Sugestão | Decisão | Motivo |
|---|---|---|
| | | |

## 4. Funcionalidades não implementadas (backlog)
Pagamento online, cupons, notificações push, avaliação de sabores, frete por região.

## 5. Conclusão
Resumir o que melhorou após os testes e o que ficou para a próxima versão.
