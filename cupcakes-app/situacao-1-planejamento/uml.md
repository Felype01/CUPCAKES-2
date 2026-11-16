# Modelagem UML (revisada)

Os diagramas usam Mermaid, que o GitHub renderiza automaticamente. Os originais do PIT I (Draw.io/Lucidchart)
podem ser exportados e colocados na pasta `diagramas/` para comparação.

## Casos de uso
```mermaid
flowchart LR
  V([Visitante]) --> UC1(Ver cardápio)
  V --> UC2(Montar carrinho)
  V --> UC3(Criar conta)
  C([Cliente]) --> UC1
  C --> UC2
  C --> UC4(Finalizar pedido)
  C --> UC5(Acompanhar pedidos)
  A([Administrador]) --> UC6(Gerenciar sabores)
  A --> UC7(Atualizar status do pedido)
  UC4 -. inclui .-> UC8(Autenticar)
  UC5 -. inclui .-> UC8
```

## Diagrama de classes
```mermaid
classDiagram
  class Usuario {
    +int id
    +string nome
    +string email
    +string senhaHash
    +string telefone
    +bool isAdmin
    +autenticar(email, senha)
  }
  class Produto {
    +int id
    +string nome
    +string descricao
    +int precoCentavos
    +string corGlace
    +bool ativo
    +alternarAtivo()
  }
  class Pedido {
    +int id
    +string status
    +int totalCentavos
    +string enderecoEntrega
    +datetime criadoEm
    +atualizarStatus(status)
  }
  class ItemPedido {
    +int quantidade
    +int precoUnitarioCentavos
  }
  Usuario "1" --> "0..*" Pedido : faz
  Pedido "1" *-- "1..*" ItemPedido : composto por
  Produto "1" --> "0..*" ItemPedido : é vendido em
```

## Sequência: finalizar pedido
```mermaid
sequenceDiagram
  actor C as Cliente
  participant V as View (carrinho.html)
  participant K as Controller (loja.finalizar)
  participant M as Model (pedido)
  participant B as Banco
  C->>V: informa endereço e toca em "Finalizar pedido"
  V->>K: POST /carrinho/finalizar
  K->>K: valida login, carrinho e endereço
  alt dados inválidos
    K-->>V: mensagem de erro
  else dados válidos
    K->>M: criar(usuario, endereco, itens)
    M->>B: INSERT pedido + itens (uma transação)
    B-->>M: id do pedido
    K-->>C: redireciona para "Meus pedidos"
  end
```

## Atividades: ciclo do pedido
```mermaid
flowchart TD
  I((Início)) --> A[Escolher sabores]
  A --> B[Revisar carrinho]
  B --> C{Está logado?}
  C -- Não --> D[Entrar ou criar conta]
  D --> E
  C -- Sim --> E[Informar endereço]
  E --> F{Dados válidos?}
  F -- Não --> E
  F -- Sim --> G[Pedido Recebido]
  G --> H[Em preparo]
  H --> J[Pronto]
  J --> K[Entregue]
  K --> Z((Fim))
```

## Arquitetura MVC
```mermaid
flowchart LR
  U[Navegador] -->|HTTP| R[Rotas Flask]
  R --> K[Controllers: auth, loja, admin]
  K --> M[Models: usuario, produto, pedido]
  M --> B[(SQLite)]
  K --> T[Views: templates Jinja]
  T -->|HTML| U
```
