---
title: Constraints
summary: Learn how SQL Constraints apply to TiDB.
---

# 制約 {#constraints}

TiDB は、MySQL とほぼ同じ制約をサポートしています。

## ヌルではない {#not-null}

TiDB でサポートされている NOT NULL 制約は、MySQL でサポートされているものと同じです。

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

-   `AUTO_INCREMENT`列に`NULL`を代入できるため、最初の`INSERT`ステートメントは成功します。 TiDB はシーケンス番号を自動的に生成します。
-   `age`列が`NOT NULL`として定義されているため、2 番目の`INSERT`ステートメントは失敗します。
-   `last_login`列が`NOT NULL`として明示的に定義されていないため、3 番目の`INSERT`ステートメントは成功します。デフォルトでは NULL 値が許可されています。

## 小切手 {#check}

TiDB は解析しますが、 `CHECK`の制約を無視します。これはMySQL 5.7互換の動作です。

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

トランザクション モードと`tidb_constraint_check_in_place`の値に応じて、TiDB は`UNIQUE`の制約[怠惰に](/transaction-overview.md#lazy-check-of-constraints)をチェックする場合があります。これにより、ネットワーク アクセスをバッチ処理してパフォーマンスを向上させることができます。

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

悲観的ロックのデフォルトでは:

{{< copyable "" >}}

```sql
BEGIN;
INSERT INTO users (username) VALUES ('jane'), ('chris'), ('bill');
```

```
ERROR 1062 (23000): Duplicate entry 'bill' for key 'username'
```

楽観的ロックと`tidb_constraint_check_in_place=0`の場合:

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

楽観的な例では、トランザクションがコミットされるまで一意のチェックが遅れました。値`bill`が既に存在していたため、重複キー エラーが発生しました。

`tidb_constraint_check_in_place`から`1`を設定すると、この動作を無効にできます。ペシミスティック トランザクション モードではステートメントの実行時に制約が常にチェックされるため、この変数設定はペシミスティック トランザクションには影響しません。 `tidb_constraint_check_in_place=1`の場合、ステートメントの実行時に一意制約がチェックされます。

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

最初の`INSERT`ステートメントで重複キー エラーが発生しました。これにより、追加のネットワーク通信オーバーヘッドが発生し、挿入操作のスループットが低下する可能性があります。

## 主キー {#primary-key}

MySQL と同様に、主キー制約には一意の制約が含まれます。つまり、主キー制約を作成することは、一意の制約を持つことと同じです。さらに、TiDB のその他の主キー制約も、MySQL のものと似ています。

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

-   列`a`が主キーとして定義されており、NULL 値が許可されていないため、表`t2`を作成できませんでした。
-   テーブルには 1 つの主キーしか持てないため、テーブル`t3`を作成できませんでした。
-   主キーは 1 つしか存在できませんが、TiDB は複数の列を複合主キーとして定義することをサポートしているため、表`t4`は正常に作成されました。

上記のルールに加えて、TiDB は現在、 `NONCLUSTERED`種類の主キーの追加と削除のみをサポートしています。例えば：

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

`CLUSTERED`型の主キーの詳細については、 [クラスター化インデックス](/clustered-indexes.md)を参照してください。

## 外部キー {#foreign-key}

> **ノート：**
>
> TiDB では、外部キー制約のサポートが制限されています。

TiDB は、DDL コマンドでの`FOREIGN KEY`制約の作成をサポートしています。

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

TiDB は、 `ALTER TABLE`コマンドを介して`DROP FOREIGN KEY`および`ADD FOREIGN KEY`への構文もサポートします。

{{< copyable "" >}}

```sql
ALTER TABLE orders DROP FOREIGN KEY fk_user_id;
ALTER TABLE orders ADD FOREIGN KEY fk_user_id (user_id) REFERENCES users(id);
```

### ノート {#notes}

-   TiDB は、他のデータベースから TiDB にデータを移行するときにこの構文によって引き起こされるエラーを回避するために、外部キーをサポートしています。

    ただし、TiDB は DML ステートメントの外部キーに対して制約チェックを実行しません。たとえば、users テーブルに id=123 のレコードがなくても、次のトランザクションは正常に送信できます。

    ```sql
    START TRANSACTION;
    INSERT INTO orders (user_id, doc) VALUES (123, NULL);
    COMMIT;
    ```
