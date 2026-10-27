---
title: TiDB Cloud で PostgreSQL 互換 SQL を試す
summary: PostgreSQL 互換の TiDB Cloud Starter でサポートされる基本的な SQL 文について説明します。
---

# TiDB Cloud で PostgreSQL 互換 SQL を試す

PostgreSQL 互換の {{{ .starter }}} は、PostgreSQL ワイヤプロトコルと一般的な PostgreSQL 構文をサポートしています。ほとんどの PostgreSQL クライアント、ドライバ、ORM を使用してインスタンスを操作できます。

このページでは、DDL、DML、DQL、DCL、およびトランザクション制御を含む基本的な SQL 操作について説明します。

サポートされていない PostgreSQL 機能や動作が異なる機能については、[PostgreSQLとの互換性](/tidb-cloud/starter/postgresql-compatibility.md) を参照してください。

## カテゴリ {#categories}

SQL 文は、その機能に応じて次のカテゴリに分類できます。

- **DDL (Data Definition Language)**: データベース、スキーマ、テーブル、ビュー、インデックス、シーケンス、型などのデータベースオブジェクトを定義および管理します。
- **DML (Data Manipulation Language)**: テーブルデータを挿入、更新、削除します。
- **DQL (Data Query Language)**: `SELECT`、フィルタリング、テーブル結合、集計、サブクエリ、共通テーブル式（CTE）などのクエリ機能を使用してデータを問い合わせます。
- **DCL (Data Control Language)**: 権限とロールメンバーシップを管理します。
- **トランザクション制御**: `BEGIN`、`COMMIT`、`ROLLBACK`、`SAVEPOINT` などの文を使用してトランザクションを管理します。

一般的な DDL 操作には、オブジェクトの作成、変更、削除があります。対応するコマンドは `CREATE`、`ALTER`、`DROP` です。

## データベースの一覧表示、作成、削除 {#list-create-and-drop-databases}

データベースを一覧表示するには、`pg_database` システムカタログを問い合わせます。

```sql
SELECT datname
FROM pg_database
ORDER BY datname;
```

`samp_db` という名前のデータベースを作成するには、`CREATE DATABASE` 文を使用します。

```sql
CREATE DATABASE samp_db;
```

`psql` を使用してデータベースに接続するには、`\connect` コマンドを使用します。

```text
\connect samp_db
```

> **Note:**
>
> `\connect` は SQL 文ではなく、`psql` クライアントコマンドです。

データベースを削除するには、まず別のデータベースに接続します。

```text
\connect postgres
```

次に、`DROP DATABASE` 文を使用します。

```sql
DROP DATABASE samp_db;
```

## テーブルの作成、一覧表示、削除 {#create-list-and-drop-tables}

テーブルを作成するには、`CREATE TABLE` 文を使用します。

たとえば、`person` という名前のテーブルを作成します。

```sql
CREATE TABLE person (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birthday DATE
);
```

`public` スキーマ内のテーブルを一覧表示するには、次を実行します。

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_type = 'BASE TABLE'
ORDER BY table_name;
```

`person` テーブルのカラムを表示するには、次を実行します。

```sql
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'person'
ORDER BY ordinal_position;
```

テーブルを削除するには、`DROP TABLE` 文を使用します。

```sql
DROP TABLE person;
```

## インデックスの作成、一覧表示、削除 {#create-list-and-drop-indexes}

インデックスは、インデックス付きカラムに対するクエリ性能を向上させることができます。

`name` カラムにインデックスを作成するには、次を実行します。

```sql
CREATE INDEX person_name_idx ON person (name);
```

一意インデックスを作成するには、次を実行します。

```sql
CREATE UNIQUE INDEX person_name_unique_idx ON person (name);
```

`person` テーブルのインデックスを一覧表示するには、次を実行します。

```sql
SELECT
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename = 'person'
ORDER BY indexname;
```

インデックスを削除するには、`DROP INDEX` 文を使用します。

```sql
DROP INDEX person_name_idx;
```

サポートされる PostgreSQL のインデックスメソッドと互換性の違いについては、[PostgreSQLとの互換性](/tidb-cloud/starter/postgresql-compatibility.md) を参照してください。

## データの挿入、更新、削除 {#insert-update-and-delete-data}

一般的な DML 操作では、`INSERT`、`UPDATE`、`DELETE` 文を使用します。

`person` テーブルに 1 行挿入するには、次を実行します。

```sql
INSERT INTO person (name, birthday)
VALUES ('Tom', DATE '1990-09-12');
```

複数行を挿入するには、次を実行します。

```sql
INSERT INTO person (name, birthday)
VALUES
    ('Alice', DATE '1992-05-01'),
    ('Bob', DATE '1993-08-08');
```

PostgreSQL 互換の {{{ .starter }}} は `RETURNING` をサポートしています。たとえば、1 行挿入した後に生成された ID を返すには、次を実行します。

```sql
INSERT INTO person (name, birthday)
VALUES ('Carol', DATE '1994-03-15')
RETURNING id, name;
```

行を更新するには、次を実行します。

```sql
UPDATE person
SET birthday = DATE '1990-10-12'
WHERE name = 'Tom';
```

行を削除するには、次を実行します。

```sql
DELETE FROM person
WHERE name = 'Bob';
```

> **Note:**
>
> `WHERE` 句のない `UPDATE` 文および `DELETE` 文は、テーブル内のすべての行に対して実行されます。

### データをアップサートする {#upsert-data}

`INSERT ... ON CONFLICT` を使用して、行を挿入するか、一意性の競合を処理します。

例えば、次のとおりです。

```sql
CREATE TABLE account (
    id BIGSERIAL PRIMARY KEY,
    email TEXT UNIQUE,
    name TEXT
);

INSERT INTO account (email, name)
VALUES ('alice@example.com', 'Alice')
ON CONFLICT (email)
DO UPDATE SET name = excluded.name;
```

## データをクエリする {#query-data}

データをクエリするには、`SELECT` 文を使用します。

すべてのカラムをクエリするには、次のようにします。

```sql
SELECT *
FROM person;
```

特定のカラムをクエリするには、次のようにします。

```sql
SELECT id, name
FROM person;
```

行をフィルタリングするには、`WHERE` 句を使用します。

```sql
SELECT id, name, birthday
FROM person
WHERE birthday >= DATE '1992-01-01'
ORDER BY birthday;
```

PostgreSQL 互換の {{{ .starter }}} は、テーブル結合、サブクエリ、CTE、再帰 CTE、ウィンドウ関数、集合演算など、一般的な PostgreSQL のクエリ機能もサポートしています。

例えば、CTE を使用してデータをフィルタリングできます。

```sql
WITH recent_people AS (
    SELECT id, name, birthday
    FROM person
    WHERE birthday >= DATE '1992-01-01'
)
SELECT *
FROM recent_people
ORDER BY birthday;
```

## トランザクションを管理する {#manage-transactions}

`BEGIN` と `COMMIT` を使用して、1 つのトランザクション内で複数の文を実行します。

```sql
BEGIN;

UPDATE account
SET name = 'Alice Chen'
WHERE email = 'alice@example.com';

COMMIT;
```

現在のトランザクションでの変更を破棄するには、`ROLLBACK` を使用します。

```sql
BEGIN;

DELETE FROM account
WHERE email = 'alice@example.com';

ROLLBACK;
```

セーブポイントもサポートされています。

```sql
BEGIN;

UPDATE account
SET name = 'Alice'
WHERE email = 'alice@example.com';

SAVEPOINT before_second_update;

UPDATE account
SET name = 'Alice Updated'
WHERE email = 'alice@example.com';

ROLLBACK TO SAVEPOINT before_second_update;

COMMIT;
```

サポートされているトランザクション分離レベルと PostgreSQL 互換性の違いについては、[PostgreSQLとの互換性](/tidb-cloud/starter/postgresql-compatibility.md) を参照してください。

## ロールを作成し、権限を付与し、削除する {#create-grant-privileges-to-and-drop-a-role}

DCL 文は、権限とロールメンバーシップを管理するために使用されます。

ログイン可能なロールを作成するには、次のようにします。

```sql
CREATE ROLE app_user
LOGIN
PASSWORD 'SecurePass1';
```

`public` スキーマへのアクセス権と、`person` テーブルをクエリする権限をロールに付与します。

```sql
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT ON person TO app_user;
```

ロールに付与されたテーブル権限を確認するには、次のようにします。

```sql
SELECT
    grantee,
    table_schema,
    table_name,
    privilege_type
FROM information_schema.table_privileges
WHERE grantee = 'app_user'
ORDER BY table_schema, table_name, privilege_type;
```

権限を取り消すには、次のようにします。

```sql
REVOKE SELECT ON person FROM app_user;
REVOKE USAGE ON SCHEMA public FROM app_user;
```

ロールを削除するには、次のようにします。

```sql
DROP ROLE app_user;
```