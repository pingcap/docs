---
title: Explore SQL with TiDB
summary: Learn about the basic SQL statements for the TiDB database.
---

# TiDB で SQL を調べる {#explore-sql-with-tidb}

TiDB は MySQL と互換性があり、ほとんどの場合、MySQL ステートメントを直接使用できます。サポートされていない機能については、 [MySQL との互換性](/mysql-compatibility.md#unsupported-features)を参照してください。

<CustomContent platform="tidb">

SQL を試して、TiDB と MySQL クエリとの互換性をテストするには、 [TiDB をインストールせずに Web ブラウザーで直接実行する](https://tour.tidb.io/)ことができます。最初に TiDB クラスターをデプロイしてから、そこで SQL ステートメントを実行することもできます。

</CustomContent>

SQL を実験し、MySQL クエリと TiDB の互換性をテストするには、[TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&utm_medium=basic-sql-operations) ことができます。最初に TiDB クラスターをデプロイしてから、その中で SQL ステートメントを実行することもできます。

## カテゴリー {#category}

SQL は、その関数によって次の 4 つのタイプに分けられます。

-   DDL (データ定義言語): データベース、テーブル、ビュー、インデックスなどのデータベース オブジェクトを定義するために使用されます。

-   DML (Data Manipulation Language): アプリケーション関連のレコードを操作するために使用されます。

-   DQL (Data Query Language): 条件付きフィルタリングの後にレコードを照会するために使用されます。

-   DCL (Data Control Language): アクセス権限とセキュリティ レベルを定義するために使用されます。

一般的な DDL 機能は、オブジェクト (テーブルやインデックスなど) の作成、変更、および削除です。対応するコマンドは`CREATE` 、 `ALTER` 、および`DROP`です。

## データベースの表示、作成、削除 {#show-create-and-drop-a-database}

TiDB のデータベースは、テーブルやインデックスなどのオブジェクトのコレクションと見なすことができます。

データベースのリストを表示するには、次`SHOW DATABASES`ステートメントを使用します。

{{< copyable "" >}}

```sql
SHOW DATABASES;
```

`mysql`という名前のデータベースを使用するには、次のステートメントを使用します。

{{< copyable "" >}}

```sql
USE mysql;
```

データベース内のすべてのテーブルを表示するには、 `SHOW TABLES`ステートメントを使用します。

{{< copyable "" >}}

```sql
SHOW TABLES FROM mysql;
```

データベースを作成するには、 `CREATE DATABASE`ステートメントを使用します。

{{< copyable "" >}}

```sql
CREATE DATABASE db_name [options];
```

`samp_db`という名前のデータベースを作成するには、次のステートメントを使用します。

{{< copyable "" >}}

```sql
CREATE DATABASE IF NOT EXISTS samp_db;
```

データベースが存在する場合、エラーを防ぐために`IF NOT EXISTS`を追加します。

データベースを削除するには、 `DROP DATABASE`ステートメントを使用します。

{{< copyable "" >}}

```sql
DROP DATABASE samp_db;
```

## テーブルの作成、表示、および削除 {#create-show-and-drop-a-table}

テーブルを作成するには、 `CREATE TABLE`ステートメントを使用します。

{{< copyable "" >}}

```sql
CREATE TABLE table_name column_name data_type constraint;
```

たとえば、番号、名前、誕生日などのフィールドを含む`person`という名前のテーブルを作成するには、次のステートメントを使用します。

{{< copyable "" >}}

```sql
CREATE TABLE person (
    id INT(11),
    name VARCHAR(255),
    birthday DATE
    );
```

テーブル (DDL) を作成するステートメントを表示するには、 `SHOW CREATE`ステートメントを使用します。

{{< copyable "" >}}

```sql
SHOW CREATE table person;
```

テーブルを削除するには、 `DROP TABLE`ステートメントを使用します。

{{< copyable "" >}}

```sql
DROP TABLE person;
```

## インデックスの作成、表示、削除 {#create-show-and-drop-an-index}

インデックスは、インデックス付きの列に対するクエリを高速化するために使用されます。値が一意でない列のインデックスを作成するには、 `CREATE INDEX`ステートメントを使用します。

{{< copyable "" >}}

```sql
CREATE INDEX person_id ON person (id);
```

または、 `ALTER TABLE`ステートメントを使用します。

{{< copyable "" >}}

```sql
ALTER TABLE person ADD INDEX person_id (id);
```

値が一意である列に一意のインデックスを作成するには、次の`CREATE UNIQUE INDEX`ステートメントを使用します。

{{< copyable "" >}}

```sql
CREATE UNIQUE INDEX person_unique_id ON person (id);
```

または、 `ALTER TABLE`ステートメントを使用します。

{{< copyable "" >}}

```sql
ALTER TABLE person ADD UNIQUE person_unique_id (id);
```

テーブル内のすべてのインデックスを表示するには、 `SHOW INDEX`ステートメントを使用します。

{{< copyable "" >}}

```sql
SHOW INDEX FROM person;
```

インデックスを削除するには、 `DROP INDEX`または`ALTER TABLE`ステートメントを使用します。 `DROP INDEX` `ALTER TABLE`にネストできます。

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
> DDL 操作はトランザクションではありません。 DDL 操作を実行するときに`COMMIT`ステートメントを実行する必要はありません。

## データの挿入、更新、および削除 {#insert-update-and-delete-data}

一般的な DML 機能は、テーブル レコードの追加、変更、および削除です。対応するコマンドは`INSERT` 、 `UPDATE` 、および`DELETE`です。

テーブルにデータを挿入するには、 `INSERT`ステートメントを使用します。

{{< copyable "" >}}

```sql
INSERT INTO person VALUES(1,'tom','20170912');
```

いくつかのフィールドのデータを含むレコードをテーブルに挿入するには、 `INSERT`ステートメントを使用します。

{{< copyable "" >}}

```sql
INSERT INTO person(id,name) VALUES('2','bob');
```

テーブル内のレコードの一部のフィールドを更新するには、 `UPDATE`ステートメントを使用します。

{{< copyable "" >}}

```sql
UPDATE person SET birthday='20180808' WHERE id=2;
```

テーブル内のデータを削除するには、 `DELETE`ステートメントを使用します。

{{< copyable "" >}}

```sql
DELETE FROM person WHERE id=2;
```

> **ノート：**
>
> フィルターとしての`WHERE`句のない`UPDATE`ステートメントと`DELETE`ステートメントは、テーブル全体に作用します。

## クエリデータ {#query-data}

DQL は、テーブルまたは複数のテーブルから目的のデータ行を取得するために使用されます。

テーブル内のデータを表示するには、 `SELECT`ステートメントを使用します。

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

DCL は通常、ユーザーの作成または削除、およびユーザー権限の管理に使用されます。

ユーザーを作成するには、 `CREATE USER`ステートメントを使用します。次の例では、パスワード`123456`を持つ`tiuser`という名前のユーザーを作成します。

{{< copyable "" >}}

```sql
CREATE USER 'tiuser'@'localhost' IDENTIFIED BY '123456';
```

`samp_db`データベース内のテーブルを取得する権限を`tiuser`付与するには、次のようにします。

{{< copyable "" >}}

```sql
GRANT SELECT ON samp_db.* TO 'tiuser'@'localhost';
```

`tiuser`の権限を確認するには:

{{< copyable "" >}}

```sql
SHOW GRANTS for tiuser@localhost;
```

`tiuser`を削除するには:

{{< copyable "" >}}

```sql
DROP USER 'tiuser'@'localhost';
```
