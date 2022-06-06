---
title: Constraints
summary: Learn how SQL Constraints apply to TiDB.
---

# 制約 {#constraints}

TiDBは、MySQLとほぼ同じ制約をサポートしています。

## NULLではありません {#not-null}

TiDBでサポートされているNOTNULL制約は、MySQLでサポートされているものと同じです。

例えば：

{{< copyable "" >}}

```sql
CREATE TABLE users (
 id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 age INT NOT NULL,
 last_login TIMESTAMP
);
```

{{< copyable "" >}}

```sql
INSERT INTO users (id,age,last_login) VALUES (NULL,123,NOW());
```

```
Query OK, 1 row affected (0.02 sec)
```

{{< copyable "" >}}

```sql
INSERT INTO users (id,age,last_login) VALUES (NULL,NULL,NOW());
```

```
ERROR 1048 (23000): Column 'age' cannot be null
```

{{< copyable "" >}}

```sql
INSERT INTO users (id,age,last_login) VALUES (NULL,123,NULL);
```

```
Query OK, 1 row affected (0.03 sec)
```

-   `AUTO_INCREMENT`列に`NULL`を割り当てることができるため、最初の`INSERT`ステートメントは成功します。 TiDBはシーケンス番号を自動的に生成します。
-   `age`列が`NOT NULL`として定義されているため、2番目の`INSERT`ステートメントは失敗します。
-   `last_login`列が`NOT NULL`として明示的に定義されていないため、3番目の`INSERT`ステートメントは成功します。デフォルトではNULL値が許可されています。

## 小切手 {#check}

TiDBは解析しますが、 `CHECK`の制約を無視します。これはMySQL5.7と互換性のある動作です。

例えば：

{{< copyable "" >}}

```sql
DROP TABLE IF EXISTS users;
CREATE TABLE users (
 id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 username VARCHAR(60) NOT NULL,
 UNIQUE KEY (username),
 CONSTRAINT min_username_length CHECK (CHARACTER_LENGTH(username) >=4)
);
INSERT INTO users (username) VALUES ('a');
SELECT * FROM users;
```

## ユニークキー {#unique-key}

トランザクションモードと`tidb_constraint_check_in_place`の値に応じて、TiDBは`UNIQUE`の制約をチェックする場合があります[怠惰に](/transaction-overview.md#lazy-check-of-constraints) 。これは、ネットワークアクセスをバッチ処理することでパフォーマンスを向上させるのに役立ちます。

例えば：

{{< copyable "" >}}

```sql
DROP TABLE IF EXISTS users;
CREATE TABLE users (
 id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 username VARCHAR(60) NOT NULL,
 UNIQUE KEY (username)
);
INSERT INTO users (username) VALUES ('dave'), ('sarah'), ('bill');
```

悲観的ロックのデフォルトでは：

{{< copyable "" >}}

```sql
BEGIN;
INSERT INTO users (username) VALUES ('jane'), ('chris'), ('bill');
```

```
ERROR 1062 (23000): Duplicate entry 'bill' for key 'username'
```

楽観的なロックと`tidb_constraint_check_in_place=0` ：

{{< copyable "" >}}

```sql
BEGIN OPTIMISTIC;
INSERT INTO users (username) VALUES ('jane'), ('chris'), ('bill');
```

```
Query OK, 0 rows affected (0.00 sec)

Query OK, 3 rows affected (0.00 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

{{< copyable "" >}}

```sql
INSERT INTO users (username) VALUES ('steve'),('elizabeth');
```

```
Query OK, 2 rows affected (0.00 sec)
Records: 2  Duplicates: 0  Warnings: 0
```

{{< copyable "" >}}

```sql
COMMIT;
```

```
ERROR 1062 (23000): Duplicate entry 'bill' for key 'username'
```

楽観的な例では、トランザクションがコミットされるまで一意のチェックが遅延されました。値`bill`がすでに存在していたため、これにより重複キーエラーが発生しました。

`tidb_constraint_check_in_place`を`1`に設定すると、この動作を無効にできます。悲観的トランザクションモードでは、ステートメントの実行時に制約が常にチェックされるため、この変数設定は悲観的トランザクションには影響しません。 `tidb_constraint_check_in_place=1`の場合、ステートメントの実行時に一意の制約がチェックされます。

例えば：

```sql
DROP TABLE IF EXISTS users;
CREATE TABLE users (
 id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 username VARCHAR(60) NOT NULL,
 UNIQUE KEY (username)
);
INSERT INTO users (username) VALUES ('dave'), ('sarah'), ('bill');
```

{{< copyable "" >}}

```sql
SET tidb_constraint_check_in_place = 1;
```

```
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "" >}}

```sql
BEGIN OPTIMISTIC;
```

```
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "" >}}

```sql
INSERT INTO users (username) VALUES ('jane'), ('chris'), ('bill');
```

```
ERROR 1062 (23000): Duplicate entry 'bill' for key 'username'
..
```

最初の`INSERT`のステートメントにより、重複キーエラーが発生しました。これにより、追加のネットワーク通信オーバーヘッドが発生し、挿入操作のスループットが低下する可能性があります。

## 主キー {#primary-key}

MySQLと同様に、主キー制約には一意の制約が含まれます。つまり、主キー制約を作成することは、一意の制約を持つことと同じです。さらに、TiDBの他の主キー制約もMySQLの制約と同様です。

例えば：

{{< copyable "" >}}

```sql
CREATE TABLE t1 (a INT NOT NULL PRIMARY KEY);
```

```
Query OK, 0 rows affected (0.12 sec)
```

{{< copyable "" >}}

```sql
CREATE TABLE t2 (a INT NULL PRIMARY KEY);
```

```
ERROR 1171 (42000): All parts of a PRIMARY KEY must be NOT NULL; if you need NULL in a key, use UNIQUE instead
```

{{< copyable "" >}}

```sql
CREATE TABLE t3 (a INT NOT NULL PRIMARY KEY, b INT NOT NULL PRIMARY KEY);
```

```
ERROR 1068 (42000): Multiple primary key defined
```

{{< copyable "" >}}

```sql
CREATE TABLE t4 (a INT NOT NULL, b INT NOT NULL, PRIMARY KEY (a,b));
```

```
Query OK, 0 rows affected (0.10 sec)
```

-   列`a`が主キーとして定義されており、NULL値を許可していないため、表`t2`を作成できませんでした。
-   テーブルには主キーが1つしかないため、テーブル`t3`を作成できませんでした。
-   表`t4`は正常に作成されました。これは、主キーが1つしかない場合でも、TiDBは複数の列を複合主キーとして定義することをサポートしているためです。

上記のルールに加えて、TiDBは現在、 `NONCLUSTERED`タイプの主キーの追加と削除のみをサポートしています。例えば：

{{< copyable "" >}}

```sql
CREATE TABLE t5 (a INT NOT NULL, b INT NOT NULL, PRIMARY KEY (a,b) CLUSTERED);
ALTER TABLE t5 DROP PRIMARY KEY;
```

```
ERROR 8200 (HY000): Unsupported drop primary key when the table is using clustered index
```

{{< copyable "" >}}

```sql
CREATE TABLE t5 (a INT NOT NULL, b INT NOT NULL, PRIMARY KEY (a,b) NONCLUSTERED);
ALTER TABLE t5 DROP PRIMARY KEY;
```

```
Query OK, 0 rows affected (0.10 sec)
```

`CLUSTERED`タイプの主キーの詳細については、 [クラスター化されたインデックス](/clustered-indexes.md)を参照してください。

## 外部キー {#foreign-key}

> **ノート：**
>
> TiDBは、外部キー制約のサポートが制限されています。

TiDBは、DDLコマンドでの`FOREIGN KEY`の制約の作成をサポートしています。

例えば：

```sql
CREATE TABLE users (
 id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 doc JSON
);
CREATE TABLE orders (
 id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 user_id INT NOT NULL,
 doc JSON,
 FOREIGN KEY fk_user_id (user_id) REFERENCES users(id)
);
```

{{< copyable "" >}}

```sql
SELECT table_name, column_name, constraint_name, referenced_table_name, referenced_column_name
FROM information_schema.key_column_usage WHERE table_name IN ('users', 'orders');
```

```
+------------+-------------+-----------------+-----------------------+------------------------+
| table_name | column_name | constraint_name | referenced_table_name | referenced_column_name |
+------------+-------------+-----------------+-----------------------+------------------------+
| users      | id          | PRIMARY         | NULL                  | NULL                   |
| orders     | id          | PRIMARY         | NULL                  | NULL                   |
| orders     | user_id     | fk_user_id      | users                 | id                     |
+------------+-------------+-----------------+-----------------------+------------------------+
3 rows in set (0.00 sec)
```

TiDBは、 `ALTER TABLE`コマンドを介した`DROP FOREIGN KEY`および`ADD FOREIGN KEY`の構文もサポートしています。

{{< copyable "" >}}

```sql
ALTER TABLE orders DROP FOREIGN KEY fk_user_id;
ALTER TABLE orders ADD FOREIGN KEY fk_user_id (user_id) REFERENCES users(id);
```

### ノート {#notes}

-   TiDBは外部キーをサポートして、他のデータベースからTiDBにデータを移行するときにこの構文によって引き起こされるエラーを回避します。

    ただし、TiDBはDMLステートメントの外部キーに対して制約チェックを実行しません。たとえば、usersテーブルにid = 123のレコードがない場合でも、次のトランザクションを正常に送信できます。

    ```sql
    START TRANSACTION;
    INSERT INTO orders (user_id, doc) VALUES (123, NULL);
    COMMIT;
    ```
