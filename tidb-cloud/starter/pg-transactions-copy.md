---
title: PostgreSQL のトランザクションと COPY
summary: PostgreSQL互換のTiDB Cloud Starterにおけるトランザクション制御とCOPYサポートについて説明します。
---

# PostgreSQL のトランザクションと COPY

PostgreSQL互換の{{{ .starter }}}は、PostgreSQLのトランザクション制御、セーブポイント、一般的なトランザクション分離レベル、および一括データ転送のためのPostgreSQL `COPY`プロトコルをサポートしています。

## サンプルデータをセットアップする {#set-up-sample-data}

このページの一部の例では、サンプルテーブルを使用します。これらの例を実行する前に、必要なテーブルを作成し、テストデータベースにサンプルデータを挿入してください。

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

これらのセットアップは、例を実行する前に一度だけ実行してください。`users`テーブルは、セーブポイントの例でサンプル行を挿入できるよう、初期状態では空です。

## トランザクション制御 {#transaction-control}

明示的なトランザクションを開始するには `BEGIN` を使用し、変更を永続化するには `COMMIT` を使用します。

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

現在のトランザクション内のすべての変更を破棄するには `ROLLBACK` を使用します。

```sql
BEGIN;

DELETE FROM orders
WHERE id = 100;

ROLLBACK;
```

## 自動コミット {#autocommit}

明示的な `BEGIN` ブロックの外で実行された文は、自動コミットモードで実行されます。

各文はそれぞれ独自のトランザクションで実行され、成功した場合は自動的にコミットされます。文が失敗した場合、そのトランザクションはロールバックされます。

## セーブポイント {#savepoints}

セーブポイントを使用すると、トランザクション全体を破棄せずに、トランザクションの一部だけをロールバックできます。

例:

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

この例では、`Bob` の挿入はロールバックされ、`Alice` の挿入はコミットされます。

セーブポイントの動作は PostgreSQL のセマンティクスに従います。

- 重複するセーブポイント名を使用できます。その名前で最後に作成されたセーブポイントが使用されます。
- `ROLLBACK TO SAVEPOINT` は、セーブポイント以降の変更をロールバックし、そのセーブポイントは再利用可能なまま保持されます。
- `RELEASE SAVEPOINT` は、指定したセーブポイントと、それ以降に作成されたセーブポイントを削除します。

## トランザクション分離 {#transaction-isolation}

デフォルトのトランザクション分離レベルは `READ COMMITTED` です。

要求できる分離レベルは次のとおりです。

| 分離レベル | 動作 |
| --- | --- |
| `READ COMMITTED` | デフォルト。各文は、その文の開始前にコミットされた行を参照します。 |
| `READ UNCOMMITTED` | `READ COMMITTED` として動作します。 |
| `REPEATABLE READ` | トランザクションの存続期間中、1つのスナップショットを使用します。 |
| `SERIALIZABLE` | PostgreSQL Serializable Snapshot Isolation は実装されていません。PostgreSQL ワイヤプロトコル経由では、このトランザクションは `REPEATABLE READ` にダウングレードされます。 |

特定の分離レベルでトランザクションを開始するには、次のようにします。

```sql
BEGIN ISOLATION LEVEL REPEATABLE READ;

SELECT *
FROM accounts;

COMMIT;
```

実効的な分離レベルは次のように確認できます。

```sql
SHOW transaction_isolation;
```

> **Note:**
>
> PostgreSQL ワイヤプロトコル経由で `SERIALIZABLE` が要求された場合、PostgreSQL互換の{{{ .starter }}}は代わりに `REPEATABLE READ` を使用します。PostgreSQL Serializable Snapshot Isolation を必要とするアプリケーションは、移行前に確認する必要があります。詳細は、[PostgreSQLとの互換性](/tidb-cloud/starter/postgresql-compatibility.md) を参照してください。

## 読み取り専用トランザクション {#read-only-transactions}

読み取り専用トランザクションを開始するには `BEGIN READ ONLY` を使用します。

```sql
BEGIN READ ONLY;

SELECT *
FROM users;

COMMIT;
```

`BEGIN` の後でトランザクションを読み取り専用に設定することもできます。

```sql
BEGIN;

SET TRANSACTION READ ONLY;

SELECT *
FROM users;

COMMIT;
```

読み取り専用トランザクションでは、DML および DDL の書き込みは拒否されます。

現在のセッションで新しいトランザクションのデフォルトモードを設定することもできます。

```sql
SET default_transaction_read_only = on;
```

## トランザクションにおけるシーケンスの動作 {#sequence-behavior-in-transactions}

`nextval()` などのシーケンス操作は、PostgreSQL の動作に合わせて非トランザクションです。

トランザクション内で `nextval()` を呼び出した後にロールバックしても、生成されたシーケンス値は再利用されません。

例:

```sql
BEGIN;

SELECT nextval('order_seq');

ROLLBACK;
```

ロールバック後もシーケンスは進んだままです。欠番のない連番が必要な用途にシーケンスを使用しないでください。

## トランザクションの失敗状態 {#failed-transaction-state}

明示的なトランザクション内で文が失敗すると、そのトランザクションは失敗状態になります。

例えば次のとおりです。

```sql
BEGIN;

INSERT INTO users (id, name)
VALUES (1, 'Alice');

-- If a statement fails here, the transaction enters a failed state.

ROLLBACK;
```

トランザクションが失敗状態になった後は、通常の SQL 操作を続行する前に、`ROLLBACK` を使用するか、以前のセーブポイントまでロールバックしてください。

## COPY {#copy}

PostgreSQL の `COPY` プロトコルは、PostgreSQL ワイヤプロトコルを介した効率的な一括データ転送を提供します。

PostgreSQL 互換の {{{ .starter }}} は、テキストデータおよび CSV データに対する `COPY` のテーブル形式をサポートしています。

### `COPY FROM STDIN` を使用してデータをインポートする {#import-data-with-copy-from-stdin}

`COPY ... FROM STDIN` を使用して、PostgreSQL クライアントからデータをストリーミングします。

```sql
COPY users (name, email)
FROM STDIN
WITH (FORMAT csv);
```

`psql` を使用する場合は、`\copy` クライアントコマンドを使ってローカルファイルを読み込み、PostgreSQL 接続を通じてデータを送信できます。

```text
\copy users (name, email) FROM 'users.csv' WITH (FORMAT csv, HEADER)
```

> **Note:**
>
> `\copy` は `psql` のクライアントコマンドであり、SQL 文ではありません。

### COPY を使用してデータをエクスポートする {#export-data-with-copy}

`COPY ... TO STDOUT` のテーブル形式を使用すると、テーブルデータをクライアントにストリーミングできます。

例えば次のとおりです。

```sql
COPY users (id, name, email)
TO STDOUT
WITH (FORMAT csv, HEADER);
```

`psql` を使用する場合は、`\copy` を使ってテーブルデータをローカルファイルに書き込めます。

```text
\copy users TO 'users.csv' WITH (FORMAT csv, HEADER)
```

### COPY の形式 {#copy-formats}

以下の一般的な形式がサポートされています。

| 形式 | サポート |
| --- | --- |
| テキスト | サポート |
| CSV | サポート |
| バイナリ | 非サポート |

Parquet のインポートは `parquet` 拡張機能を通じても利用できます。詳細は [Parquet データをインポートする](/tidb-cloud/starter/pg-parquet-import.md) を参照してください。

### COPY の制限事項 {#copy-limitations}

次の制限事項に注意してください。

- テーブル形式 `COPY table_name [(columns)] ...` を使用してください。
- バイナリ `COPY` はサポートされていません。
- `COPY (SELECT ...) TO STDOUT` はサポートされていません。
- ローカルファイルについては、ファイルがクライアントによって読み取られ、PostgreSQL 接続を介して転送されるように、`psql` の `\copy` コマンドを使用してください。