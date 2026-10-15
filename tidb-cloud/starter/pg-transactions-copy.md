---
title: PostgreSQL 事务和 COPY
summary: 了解 PostgreSQL 兼容的 TiDB Cloud Starter 中的事务控制和 COPY 支持。
---

# PostgreSQL 事务和 COPY

PostgreSQL 兼容的 {{{ .starter }}} 支持 PostgreSQL 事务控制、保存点、常见的事务隔离级别，以及用于批量数据传输的 PostgreSQL `COPY` 协议。

## 设置示例数据 {#set-up-sample-data}

本页中的一些示例会使用示例表。在运行这些示例之前，请先创建所需的表，并将示例数据插入到测试数据库中。

```sql
CREATE TABLE accounts (
    id BIGINT PRIMARY KEY,
    balance NUMERIC(12, 2) NOT NULL
);

CREATE TABLE orders (
    id BIGINT PRIMARY KEY
);

CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT
);

CREATE SEQUENCE order_seq START WITH 1000;

INSERT INTO accounts (id, balance) VALUES
    (1, 1000.00),
    (2, 500.00);

INSERT INTO orders (id) VALUES
    (100);
```

在执行示例之前，只需运行一次上述设置。`users` 表初始为空，以便保存点示例可以插入示例行。

## 事务控制 {#transaction-control}

使用 `BEGIN` 启动一个显式事务，并使用 `COMMIT` 持久化更改：

```sql
BEGIN;

UPDATE accounts
SET balance = balance - 100
WHERE id = 1;

UPDATE accounts
SET balance = balance + 100
WHERE id = 2;

COMMIT;
```

使用 `ROLLBACK` 丢弃当前事务中的所有更改：

```sql
BEGIN;

DELETE FROM orders
WHERE id = 100;

ROLLBACK;
```

## 自动提交 {#autocommit}

在显式 `BEGIN` 块之外执行的语句会以自动提交模式运行。

每条语句都在其自己的事务中运行，并在成功时自动提交。如果语句失败，则事务会回滚。

## 保存点 {#savepoints}

使用保存点可以回滚事务的一部分，而无需丢弃整个事务。

例如：

```sql
BEGIN;

INSERT INTO users (name)
VALUES ('Alice');

SAVEPOINT sp1;

INSERT INTO users (name)
VALUES ('Bob');

ROLLBACK TO SAVEPOINT sp1;

RELEASE SAVEPOINT sp1;

COMMIT;
```

在此示例中，插入 `Bob` 的操作会被回滚，而插入 `Alice` 的操作会被提交。

保存点行为遵循 PostgreSQL 语义：

- 允许重复的保存点名称。系统会使用最近创建的同名保存点。
- `ROLLBACK TO SAVEPOINT` 会回滚保存点之后的更改，并保留该保存点以供复用。
- `RELEASE SAVEPOINT` 会移除指定的保存点，以及在其之后创建的保存点。

## 事务隔离 {#transaction-isolation}

默认的事务隔离级别是 `READ COMMITTED`。

可以请求以下隔离级别：

| 隔离级别 | 行为 |
| --- | --- |
| `READ COMMITTED` | 默认值。每条语句都只能看到该语句开始前已提交的行。 |
| `READ UNCOMMITTED` | 行为与 `READ COMMITTED` 相同。 |
| `REPEATABLE READ` | 在整个事务生命周期内使用同一个快照。 |
| `SERIALIZABLE` | 未实现 PostgreSQL Serializable Snapshot Isolation。通过 PostgreSQL wire 协议时，该事务会降级为 `REPEATABLE READ`。 |

以特定隔离级别启动事务：

```sql
BEGIN ISOLATION LEVEL REPEATABLE READ;

SELECT *
FROM accounts;

COMMIT;
```

你可以检查实际生效的隔离级别：

```sql
SHOW transaction_isolation;
```

> **Note:**
>
> 如果通过 PostgreSQL wire 协议请求 `SERIALIZABLE`，PostgreSQL 兼容的 {{{ .starter }}} 会改用 `REPEATABLE READ`。对于需要 PostgreSQL Serializable Snapshot Isolation 的应用，在迁移前应进行评估。更多信息，参见[PostgreSQL 兼容性](/tidb-cloud/starter/postgresql-compatibility.md)。

## 只读事务 {#read-only-transactions}

使用 `BEGIN READ ONLY` 启动只读事务：

```sql
BEGIN READ ONLY;

SELECT *
FROM users;

COMMIT;
```

你也可以在 `BEGIN` 之后将事务设置为只读：

```sql
BEGIN;

SET TRANSACTION READ ONLY;

SELECT *
FROM users;

COMMIT;
```

在只读事务中，DML 和 DDL 写操作都会被拒绝。

你还可以为当前会话中的新事务设置默认模式：

```sql
SET default_transaction_read_only = on;
```

## 事务中的序列行为 {#sequence-behavior-in-transactions}

诸如 `nextval()` 之类的序列操作是非事务性的，这与 PostgreSQL 的行为一致。

如果某个事务调用了 `nextval()`，随后又发生回滚，则生成的序列值不会被复用。

例如：

```sql
BEGIN;

SELECT nextval('order_seq');

ROLLBACK;
```

回滚后，序列仍然会保持已推进的状态。不要依赖序列来实现无间隙编号。

## 失败事务状态 {#failed-transaction-state}

如果显式事务中的某条语句执行失败，该事务会进入失败状态。

例如：

```sql
BEGIN;

INSERT INTO users (id, name)
VALUES (1, 'Alice');

-- If a statement fails here, the transaction enters a failed state.

ROLLBACK;
```

事务进入失败状态后，需要先执行 `ROLLBACK`，或者回滚到之前的 savepoint，然后才能继续执行正常的 SQL 操作。

## COPY {#copy}

PostgreSQL 的 `COPY` 协议通过 PostgreSQL wire 协议提供高效的批量数据传输能力。

兼容 PostgreSQL 的 {{{ .starter }}} 支持 `COPY` 的表单形式，可用于文本和 CSV 数据。

### 使用 `COPY FROM STDIN` 导入数据 {#import-data-with-copy-from-stdin}

使用 `COPY ... FROM STDIN` 可以从 PostgreSQL 客户端流式传输数据：

```sql
COPY users (name, email)
FROM STDIN
WITH (FORMAT csv);
```

使用 `psql` 时，可以使用 `\copy` 客户端命令读取本地文件，并通过 PostgreSQL 连接发送数据：

```text
\copy users (name, email) FROM 'users.csv' WITH (FORMAT csv, HEADER)
```

> **Note:**
>
> `\copy` 是 `psql` 的客户端命令，不是 SQL 语句。

### 使用 COPY 导出数据 {#export-data-with-copy}

`COPY ... TO STDOUT` 的表单形式可用于将表数据流式传输到客户端。

例如：

```sql
COPY users (id, name, email)
TO STDOUT
WITH (FORMAT csv, HEADER);
```

使用 `psql` 时，可以使用 `\copy` 将表数据写入本地文件：

```text
\copy users TO 'users.csv' WITH (FORMAT csv, HEADER)
```

### COPY 格式 {#copy-formats}

支持以下常见格式：

| 格式 | 支持情况 |
| --- | --- |
| Text | 支持 |
| CSV | 支持 |
| Binary | 不支持 |

还可以通过 `parquet` 扩展导入 Parquet 数据。更多信息，参见[导入 Parquet 数据](/tidb-cloud/starter/pg-parquet-import.md)。

### COPY 限制 {#copy-limitations}

请注意以下限制：

- 使用表单形式 `COPY table_name [(columns)] ...`。
- 不支持 Binary `COPY`。
- 不支持 `COPY (SELECT ...) TO STDOUT`。
- 对于本地文件，请使用 `psql` 的 `\copy` 命令，这样文件会由客户端读取，并通过 PostgreSQL 连接传输。