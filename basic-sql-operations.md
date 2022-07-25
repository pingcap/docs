---
title: Explore SQL with TiDB
summary: Learn about the basic SQL statements for the TiDB database.
---

# TiDBでSQLを探索する {#explore-sql-with-tidb}

TiDBはMySQLと互換性があり、ほとんどの場合、MySQLステートメントを直接使用できます。サポートされていない機能については、 [MySQLとの互換性](/mysql-compatibility.md#unsupported-features)を参照してください。

<CustomContent platform="tidb">

SQLを試し、MySQLクエリとのTiDBの互換性をテストするには、次のことができます[TiDBをインストールせずにWebブラウザで直接実行する](https://tour.tidb.io/) 。最初にTiDBクラスタをデプロイしてから、その中でSQLステートメントを実行することもできます。

</CustomContent>

このページでは、DDL、DML、CRUD操作などの基本的なTiDB SQLステートメントについて説明します。 TiDBステートメントの完全なリストについては、 [TiDB SQL構文図](https://pingcap.github.io/sqlgram/)を参照してください。

## カテゴリー {#category}

SQLは、その関数に応じて次の4つのタイプに分類されます。

-   DDL（データ定義言語）：データベース、テーブル、ビュー、インデックスなどのデータベースオブジェクトを定義するために使用されます。

-   DML（データ操作言語）：アプリケーション関連のレコードを操作するために使用されます。

-   DQL（データクエリ言語）：条件付きフィルタリング後にレコードをクエリするために使用されます。

-   DCL（データ制御言語）：アクセス特権とセキュリティレベルを定義するために使用されます。

一般的なDDL機能は、オブジェクト（テーブルやインデックスなど）の作成、変更、および削除です。対応するコマンドは、 `CREATE` 、および`ALTER` `DROP` 。

## データベースを表示、作成、および削除します {#show-create-and-drop-a-database}

TiDBのデータベースは、テーブルやインデックスなどのオブジェクトのコレクションと見なすことができます。

データベースのリストを表示するには、次の`SHOW DATABASES`のステートメントを使用します。

{{< copyable "" >}}

```sql
SHOW DATABASES;
```

`mysql`という名前のデータベースを使用するには、次のステートメントを使用します。

{{< copyable "" >}}

```sql
USE mysql;
```

データベース内のすべてのテーブルを表示するには、次の`SHOW TABLES`のステートメントを使用します。

{{< copyable "" >}}

```sql
SHOW TABLES FROM mysql;
```

データベースを作成するには、次の`CREATE DATABASE`のステートメントを使用します。

{{< copyable "" >}}

```sql
CREATE DATABASE db_name [options];
```

`samp_db`という名前のデータベースを作成するには、次のステートメントを使用します。

{{< copyable "" >}}

```sql
CREATE DATABASE IF NOT EXISTS samp_db;
```

データベースが存在する場合にエラーを防ぐには、 `IF NOT EXISTS`を追加します。

データベースを削除するには、次の`DROP DATABASE`のステートメントを使用します。

{{< copyable "" >}}

```sql
DROP DATABASE samp_db;
```

## テーブルを作成、表示、およびドロップします {#create-show-and-drop-a-table}

テーブルを作成するには、次の`CREATE TABLE`のステートメントを使用します。

{{< copyable "" >}}

```sql
CREATE TABLE table_name column_name data_type constraint;
```

たとえば、number、name、birthdayなどのフィールドを含む`person`という名前のテーブルを作成するには、次のステートメントを使用します。

{{< copyable "" >}}

```sql
CREATE TABLE person (
    id INT(11),
    name VARCHAR(255),
    birthday DATE
    );
```

テーブル（DDL）を作成するステートメントを表示するには、次の`SHOW CREATE`のステートメントを使用します。

{{< copyable "" >}}

```sql
SHOW CREATE table person;
```

テーブルを削除するには、次の`DROP TABLE`のステートメントを使用します。

{{< copyable "" >}}

```sql
DROP TABLE person;
```

## インデックスを作成、表示、削除する {#create-show-and-drop-an-index}

インデックスは、インデックス付きの列に対するクエリを高速化するために使用されます。値が一意でない列のインデックスを作成するには、 `CREATE INDEX`ステートメントを使用します。

{{< copyable "" >}}

```sql
CREATE INDEX person_id ON person (id);
```

または、 `ALTER TABLE`のステートメントを使用します。

{{< copyable "" >}}

```sql
ALTER TABLE person ADD INDEX person_id (id);
```

値が一意である列の一意のインデックスを作成するには、 `CREATE UNIQUE INDEX`ステートメントを使用します。

{{< copyable "" >}}

```sql
CREATE UNIQUE INDEX person_unique_id ON person (id);
```

または、 `ALTER TABLE`のステートメントを使用します。

{{< copyable "" >}}

```sql
ALTER TABLE person ADD UNIQUE person_unique_id (id);
```

テーブル内のすべてのインデックスを表示するには、 `SHOW INDEX`ステートメントを使用します。

{{< copyable "" >}}

```sql
SHOW INDEX FROM person;
```

インデックスを削除するには、 `DROP INDEX`または`ALTER TABLE`ステートメントを使用します。 `DROP INDEX`は`ALTER TABLE`にネストできます：

{{< copyable "" >}}

```sql
DROP INDEX person_id ON person;
```

{{< copyable "" >}}

```sql
ALTER TABLE person DROP INDEX person_unique_id;
```

> **ノート：**
>
> DDL操作はトランザクションではありません。 DDL操作を実行するときに`COMMIT`ステートメントを実行する必要はありません。

## データの挿入、更新、削除 {#insert-update-and-delete-data}

一般的なDML機能は、テーブルレコードの追加、変更、および削除です。対応するコマンドは、 `INSERT` 、および`UPDATE` `DELETE` 。

テーブルにデータを挿入するには、次の`INSERT`のステートメントを使用します。

{{< copyable "" >}}

```sql
INSERT INTO person VALUES(1,'tom','20170912');
```

一部のフィールドのデータを含むレコードをテーブルに挿入するには、 `INSERT`ステートメントを使用します。

{{< copyable "" >}}

```sql
INSERT INTO person(id,name) VALUES('2','bob');
```

テーブル内のレコードの一部のフィールドを更新するには、 `UPDATE`ステートメントを使用します。

{{< copyable "" >}}

```sql
UPDATE person SET birthday='20180808' WHERE id=2;
```

テーブル内のデータを削除するには、次の`DELETE`のステートメントを使用します。

{{< copyable "" >}}

```sql
DELETE FROM person WHERE id=2;
```

> **ノート：**
>
> フィルタとして`WHERE`句を含まない`UPDATE`および`DELETE`ステートメントは、テーブル全体で機能します。

## クエリデータ {#query-data}

DQLは、1つまたは複数のテーブルから目的のデータ行を取得するために使用されます。

テーブル内のデータを表示するには、次の`SELECT`のステートメントを使用します。

{{< copyable "" >}}

```sql
SELECT * FROM person;
```

特定の列を照会するには、 `SELECT`キーワードの後に列名を追加します。

{{< copyable "" >}}

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

{{< copyable "" >}}

```sql
SELECT * FROM person where id<5;
```

## ユーザーの作成、承認、および削除 {#create-authorize-and-delete-a-user}

DCLは通常、ユーザーの作成または削除、およびユーザー特権の管理に使用されます。

ユーザーを作成するには、 `CREATE USER`ステートメントを使用します。次の例では、パスワード`123456`で`tiuser`という名前のユーザーを作成します。

{{< copyable "" >}}

```sql
CREATE USER 'tiuser'@'localhost' IDENTIFIED BY '123456';
```

`samp_db`データベース内のテーブルを取得する特権を`tiuser`に付与するには、次のようにします。

{{< copyable "" >}}

```sql
GRANT SELECT ON samp_db.* TO 'tiuser'@'localhost';
```

`tiuser`の権限を確認するには：

{{< copyable "" >}}

```sql
SHOW GRANTS for tiuser@localhost;
```

`tiuser`を削除するには：

{{< copyable "" >}}

```sql
DROP USER 'tiuser'@'localhost';
```
