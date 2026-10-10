---
title: USE DATABASE
summary: 現在のセッションのデータベースを選択します。このステートメントを使用すると、別のデータベースを指定して切り替えることができます。このコマンドで現在のデータベースを設定すると、変更しない限り、セッションの終了までそのまま維持されます。
---

# USE DATABASE

現在のセッションのデータベースを選択します。このステートメントを使用すると、別のデータベースを指定して切り替えることができます。このコマンドで現在のデータベースを設定すると、変更しない限り、セッションの終了までそのまま維持されます。

## 構文 {#syntax}

```sql
USE <database_name>
```

## 重要な注意事項 {#important-notes}

場合によっては、`USE <database>` の実行が遅くなることがあります。たとえば、ユーザーが一部のテーブルのみの所有権を持っている場合、{{{ .lake }}} はアクセス権を判断するためにメタデータをスキャンする必要があります。

`USE <database>` ステートメントのパフォーマンスを向上させるには、特にテーブル数が多いデータベースや権限が複雑なデータベースでは、データベースに対する `USAGE` 権限をロールに付与し、そのロールをユーザーに割り当てることができます。

```sql
-- Grant USAGE privilege on the database to a role
GRANT USAGE ON <database_name>.* TO ROLE <role_name>;

-- Assign the role to a user
GRANT ROLE <role_name> TO <user_name>;
```

`USAGE` 権限を使用すると、ユーザーはデータベースに入ることができますが、テーブルの表示やアクセスの権限は付与されません。ユーザーがテーブルを表示またはクエリするには、`SELECT` や `OWNERSHIP` などの適切なテーブルレベルの権限が引き続き必要です。

## 例 {#examples}

```sql
-- Create two databases
CREATE DATABASE database1;
CREATE DATABASE database2;

-- Select and use "database1" as the current database
USE database1;

-- Create a new table "table1" in "database1"
CREATE TABLE table1 (
  id INT,
  name VARCHAR(50)
);

-- Insert data into "table1"
INSERT INTO table1 (id, name) VALUES (1, 'John');
INSERT INTO table1 (id, name) VALUES (2, 'Alice');

-- Query all data from "table1"
SELECT * FROM table1;

-- Switch to "database2" as the current database
USE database2;

-- Create a new table "table2" in "database2"
CREATE TABLE table2 (
  id INT,
  city VARCHAR(50)
);

-- Insert data into "table2"
INSERT INTO table2 (id, city) VALUES (1, 'New York');
INSERT INTO table2 (id, city) VALUES (2, 'London');

-- Query all data from "table2"
SELECT * FROM table2;
```