---
title: Explore SQL with TiDB
summary: TiDB データベースの基本的な SQL ステートメントについて学習します。
---

# TiDB で SQL を探索する {#explore-sql-with-tidb}

TiDB は MySQL と互換性があり、ほとんどの場合 MySQL ステートメントを直接使用できます。サポートされていない機能については、 [MySQLとの互換性](/mysql-compatibility.md#unsupported-features)参照してください。

<CustomContent platform="tidb">

SQL を試して、MySQL クエリと TiDB の互換性をテストするには、 [TiDB プレイグラウンド](https://play.tidbcloud.com/?utm_source=docs&#x26;utm_medium=basic-sql-operations)試すことができます。また、最初に TiDB クラスターをデプロイし、その中で SQL ステートメントを実行することもできます。

</CustomContent>

このページでは、DDL、DML、CRUD 操作などの基本的なTiDB SQLステートメントについて説明します。TiDB ステートメントの完全なリストについては、 [TiDB SQL構文図](https://pingcap.github.io/sqlgram/)参照してください。

## カテゴリー {#category}

SQL は関数に応じて次の 4 つのタイプに分けられます。

-   DDL (データ定義言語): データベース、テーブル、ビュー、インデックスなどのデータベース オブジェクトを定義するために使用されます。

-   DML (データ操作言語): アプリケーション関連のレコードを操作するために使用されます。

-   DQL (データ クエリ言語): 条件付きフィルタリング後にレコードをクエリするために使用されます。

-   DCL (データ制御言語): アクセス権限とセキュリティ レベルを定義するために使用されます。

一般的な DDL 機能は、オブジェクト (テーブルやインデックスなど) の作成、変更、削除です。対応するコマンドは`CREATE` 、 `ALTER` 、 `DROP`です。

## データベースの表示、作成、削除 {#show-create-and-drop-a-database}

TiDB のデータベースは、テーブルやインデックスなどのオブジェクトのコレクションと考えることができます。

データベースのリストを表示するには、次`SHOW DATABASES`ステートメントを使用します。

```sql
SHOW DATABASES;
```

`mysql`という名前のデータベースを使用するには、次のステートメントを使用します。

```sql
USE mysql;
```

データベース内のすべてのテーブルを表示するには、次`SHOW TABLES`ステートメントを使用します。

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

データベースが存在する場合にエラーを防ぐために`IF NOT EXISTS`追加します。

データベースを削除するには、次`DROP DATABASE`ステートメントを使用します。

```sql
DROP DATABASE samp_db;
```

## テーブルを作成、表示、削除する {#create-show-and-drop-a-table}

テーブルを作成するには、 `CREATE TABLE`ステートメントを使用します。

```sql
CREATE TABLE table_name column_name data_type constraint;
```

たとえば、番号、名前、誕生日などのフィールドを含む`person`名前のテーブルを作成するには、次のステートメントを使用します。

```sql
CREATE TABLE person (
    id INT(11),
    name VARCHAR(255),
    birthday DATE
    );
```

テーブルを作成するステートメント (DDL) を表示するには、次`SHOW CREATE`ステートメントを使用します。

```sql
SHOW CREATE table person;
```

テーブルを削除するには、 `DROP TABLE`ステートメントを使用します。

```sql
DROP TABLE person;
```

## インデックスの作成、表示、削除 {#create-show-and-drop-an-index}

インデックスは、インデックス付き列のクエリを高速化するために使用されます。値が一意でない列のインデックスを作成するには、次`CREATE INDEX`ステートメントを使用します。

```sql
CREATE INDEX person_id ON person (id);
```

または、次`ALTER TABLE`ステートメントを使用します。

```sql
ALTER TABLE person ADD INDEX person_id (id);
```

値が一意の列に一意のインデックスを作成するには、次`CREATE UNIQUE INDEX`ステートメントを使用します。

```sql
CREATE UNIQUE INDEX person_unique_id ON person (id);
```

または、次`ALTER TABLE`ステートメントを使用します。

```sql
ALTER TABLE person ADD UNIQUE person_unique_id (id);
```

テーブル内のすべてのインデックスを表示するには、 `SHOW INDEX`ステートメントを使用します。

```sql
SHOW INDEX FROM person;
```

インデックスを削除するには、 `DROP INDEX`または`ALTER TABLE`ステートメントを使用します。 `DROP INDEX` `ALTER TABLE`にネストできます。

```sql
DROP INDEX person_id ON person;
```

```sql
ALTER TABLE person DROP INDEX person_unique_id;
```

> **注記：**
>
> DDL 操作はトランザクションではありません。DDL 操作を実行するときに`COMMIT`ステートメントを実行する必要はありません。

## データの挿入、更新、削除 {#insert-update-and-delete-data}

一般的な DML 機能は、テーブル レコードの追加、変更、および削除です。対応するコマンドは`INSERT` 、 `UPDATE` 、および`DELETE`です。

テーブルにデータを挿入するには、 `INSERT`ステートメントを使用します。

```sql
INSERT INTO person VALUES(1,'tom','20170912');
```

いくつかのフィールドのデータを含むレコードをテーブルに挿入するには、次`INSERT`ステートメントを使用します。

```sql
INSERT INTO person(id,name) VALUES('2','bob');
```

テーブル内のレコードの一部のフィールドを更新するには、次`UPDATE`ステートメントを使用します。

```sql
UPDATE person SET birthday='20180808' WHERE id=2;
```

テーブル内のデータを削除するには、次`DELETE`ステートメントを使用します。

```sql
DELETE FROM person WHERE id=2;
```

> **注記：**
>
> フィルターとして`WHERE`節を使用しない`UPDATE`および`DELETE`ステートメントは、テーブル全体に対して動作します。

## クエリデータ {#query-data}

DQL は、1 つまたは複数のテーブルから必要なデータ行を取得するために使用されます。

テーブル内のデータを表示するには、 `SELECT`ステートメントを使用します。

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

DCL は通常、ユーザーの作成や削除、ユーザー権限の管理に使用されます。

ユーザーを作成するには、 `CREATE USER`ステートメントを使用します。次の例では、 `tiuser`という名前のユーザーとパスワード`123456`を作成します。

```sql
CREATE USER 'tiuser'@'localhost' IDENTIFIED BY '123456';
```

`tiuser` `samp_db`データベース内のテーブルを取得する権限を付与するには:

```sql
GRANT SELECT ON samp_db.* TO 'tiuser'@'localhost';
```

`tiuser`の権限を確認するには:

```sql
SHOW GRANTS for tiuser@localhost;
```

`tiuser`削除するには:

```sql
DROP USER 'tiuser'@'localhost';
```
