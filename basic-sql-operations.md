---
title: Explore SQL with TiDB
summary: TiDBデータベースの基本的なSQL文について学びましょう。
---

# TiDBでSQLを試す {#explore-sql-with-tidb}

TiDBはMySQLと互換性があり、ほとんどの場合、MySQLのステートメントを直接使用できます。サポートされていない機能については、 [MySQLとの互換性](/mysql-compatibility.md#unsupported-features)参照してください。

<CustomContent platform="tidb">

SQLを試したり、TiDBとMySQLクエリの互換性をテストしたりするには、 [TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&#x26;utm_medium=basic-sql-operations)を試すことができます。また、まずTiDBクラスターをデプロイしてから、その中でSQL文を実行することもできます。

</CustomContent>

このページでは、DDL、DML、CRUD操作などのTiDB SQL文について解説します。TiDB文の完全なリストについては、 [SQLステートメントの概要](/sql-statements/sql-statement-overview.md)を参照してください。

## カテゴリ {#category}

SQLは、その関数に応じて以下の4種類に分類されます。

-   DDL（データ定義言語）：データベース、テーブル、ビュー、インデックスなど、データベースオブジェクトを定義するために使用されます。

-   DML（データ操作言語）：アプリケーション関連のレコードを操作するために使用されます。

-   DQL（データクエリ言語）：条件付きフィルタリング後にレコードをクエリするために使用されます。

-   DCL（データ制御言語）：アクセス権限とセキュリティレベルを定義するために使用されます。

一般的な DDL 機能には、オブジェクト (テーブルやインデックスなど) の作成、変更、削除があります。対応するコマンドは`CREATE` 、 `ALTER` 、 `DROP`です。

## データベースの表示、作成、削除 {#show-create-and-drop-a-database}

TiDBにおけるデータベースは、テーブルやインデックスなどのオブジェクトの集合体と考えることができます。

データベースの一覧を表示するには、 `SHOW DATABASES`ステートメントを使用します。

```sql
SHOW DATABASES;
```

`mysql`という名前のデータベースを使用するには、次のステートメントを使用します。

```sql
USE mysql;
```

データベース内のすべてのテーブルを表示するには、 `SHOW TABLES`ステートメントを使用します。

```sql
SHOW TABLES FROM mysql;
```

データベースを作成するには、 `CREATE DATABASE`ステートメントを使用します。

```sql
CREATE DATABASE db_name [options];
```

`samp_db`という名前のデータベースを作成するには、次のステートメントを使用します。

```sql
CREATE DATABASE IF NOT EXISTS samp_db;
```

データベースが存在する場合にエラーが発生しないように、 `IF NOT EXISTS`を追加してください。

データベースを削除するには、 `DROP DATABASE`ステートメントを使用します。

```sql
DROP DATABASE samp_db;
```

## テーブルの作成、表示、削除 {#create-show-and-drop-a-table}

テーブルを作成するには、 `CREATE TABLE`ステートメントを使用します。

```sql
CREATE TABLE table_name column_name data_type constraint;
```

例えば、数値、名前、誕生日などのフィールドを含む`person`という名前のテーブルを作成するには、次のステートメントを使用します。

```sql
CREATE TABLE person (
    id INT,
    name VARCHAR(255),
    birthday DATE
    );
```

テーブルを作成するステートメント（DDL）を表示するには、 `SHOW CREATE TABLE`ステートメントを使用します。

```sql
SHOW CREATE TABLE person;
```

テーブルを削除するには、 `DROP TABLE`ステートメントを使用します。

```sql
DROP TABLE person;
```

## インデックスの作成、表示、削除 {#create-show-and-drop-an-index}

インデックスは、インデックス付き列に対するクエリの速度を向上させるために使用されます。値が一意でない列にインデックスを作成するには、 `CREATE INDEX`ステートメントを使用します。

```sql
CREATE INDEX person_id ON person (id);
```

または、 `ALTER TABLE`ステートメントを使用してください。

```sql
ALTER TABLE person ADD INDEX person_id (id);
```

値が一意である列に対して一意のインデックスを作成するには、 `CREATE UNIQUE INDEX`ステートメントを使用します。

```sql
CREATE UNIQUE INDEX person_unique_id ON person (id);
```

または、 `ALTER TABLE`ステートメントを使用してください。

```sql
ALTER TABLE person ADD UNIQUE person_unique_id (id);
```

テーブル内のすべてのインデックスを表示するには、 `SHOW INDEX`ステートメントを使用します。

```sql
SHOW INDEX FROM person;
```

インデックスを削除するには、 `DROP INDEX`または`ALTER TABLE`ステートメントを使用します。 `DROP INDEX` `ALTER TABLE`の中にネストできます。

```sql
DROP INDEX person_id ON person;
```

```sql
ALTER TABLE person DROP INDEX person_unique_id;
```

> **注記：**
>
> DDL操作はトランザクションではありません。DDL操作を実行する際に`COMMIT`ステートメントを実行する必要はありません。

## データの挿入、更新、削除 {#insert-update-and-delete-data}

一般的な DML 機能には、テーブル レコードの追加、変更、削除があります。対応するコマンドは`INSERT` 、 `UPDATE` 、 `DELETE` 。

テーブルにデータを挿入するには、 `INSERT`ステートメントを使用します。

```sql
INSERT INTO person VALUES(1,'tom','20170912');
```

いくつかのフィールドのデータを含むレコードをテーブルに挿入するには、 `INSERT`ステートメントを使用します。

```sql
INSERT INTO person(id,name) VALUES('2','bob');
```

テーブル内のレコードの一部のフィールドを更新するには、 `UPDATE`ステートメントを使用します。

```sql
UPDATE person SET birthday='20180808' WHERE id=2;
```

テーブル内のデータを削除するには、 `DELETE`ステートメントを使用します。

```sql
DELETE FROM person WHERE id=2;
```

> **注記：**
>
> `UPDATE`および`DELETE`ステートメントは、フィルターとして`WHERE`句を指定しない場合、テーブル全体に対して動作します。

## クエリデータ {#query-data}

DQLは、テーブルまたは複数のテーブルから目的のデータ行を取得するために使用されます。

データを表形式で表示するには、 `SELECT`ステートメントを使用します。

```sql
SELECT * FROM person;
```

特定の列をクエリするには、 `SELECT`キーワードの後に​​列名を追加します。

```sql
SELECT name FROM person;
```

```sql
+------+
| name |
+------+
| tom  |
+------+
1 rows in set (0.00 sec)
```

`WHERE`句を使用して、条件に一致するすべてのレコードをフィルタリングし、結果を返します。

```sql
SELECT * FROM person where id<5;
```

## ユーザーの作成、承認、削除 {#create-authorize-and-delete-a-user}

DCLは通常、ユーザーの作成や削除、およびユーザー権限の管理に使用されます。

ユーザーを作成するには、 `CREATE USER`ステートメントを使用します。次の例では`tiuser`という名前のユーザーを`123456`というパスワードで作成します。

```sql
CREATE USER 'tiuser'@'localhost' IDENTIFIED BY '123456';
```

`tiuser`に`samp_db`データベース内のテーブルを取得する権限を付与するには：

```sql
GRANT SELECT ON samp_db.* TO 'tiuser'@'localhost';
```

`tiuser`の権限を確認するには：

```sql
SHOW GRANTS for tiuser@localhost;
```

`tiuser`を削除するには：

```sql
DROP USER 'tiuser'@'localhost';
```
