-- Projeto físico do banco de dados (SQLite 3). Modelo lógico em ../../situacao-1-planejamento/modelo-dados.md
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS usuario (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    nome       TEXT    NOT NULL CHECK (length(nome) >= 2),
    email      TEXT    NOT NULL UNIQUE,
    senha_hash TEXT    NOT NULL,
    telefone   TEXT,
    is_admin   INTEGER NOT NULL DEFAULT 0 CHECK (is_admin IN (0, 1)),
    criado_em  TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS produto (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    nome           TEXT    NOT NULL CHECK (length(nome) >= 2),
    descricao      TEXT,
    preco_centavos INTEGER NOT NULL CHECK (preco_centavos > 0),
    cor_glace      TEXT    NOT NULL DEFAULT '#A3214F',
    ativo          INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1)),
    criado_em      TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS pedido (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id       INTEGER NOT NULL REFERENCES usuario (id) ON DELETE RESTRICT,
    status           TEXT    NOT NULL DEFAULT 'Recebido'
                     CHECK (status IN ('Recebido', 'Em preparo', 'Pronto', 'Entregue', 'Cancelado')),
    total_centavos   INTEGER NOT NULL CHECK (total_centavos >= 0),
    endereco_entrega TEXT    NOT NULL,
    criado_em        TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS item_pedido (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id               INTEGER NOT NULL REFERENCES pedido (id)  ON DELETE CASCADE,
    produto_id              INTEGER NOT NULL REFERENCES produto (id) ON DELETE RESTRICT,
    quantidade              INTEGER NOT NULL CHECK (quantidade > 0),
    preco_unitario_centavos INTEGER NOT NULL CHECK (preco_unitario_centavos > 0),
    UNIQUE (pedido_id, produto_id)
);

CREATE INDEX IF NOT EXISTS idx_pedido_usuario ON pedido (usuario_id);
CREATE INDEX IF NOT EXISTS idx_pedido_status  ON pedido (status);
CREATE INDEX IF NOT EXISTS idx_item_pedido    ON item_pedido (pedido_id);
