---
title: Constraints
summary: SQL 制約が TiDB にどのように適用されるかを学習します。
---

# 制約 {#constraints}

TiDB は MySQL とほぼ同じ制約をサポートします。

## NULLではない {#not-null}

TiDB でサポートされる NOT NULL 制約は、MySQL でサポートされる制約と同じです。

例えば：

```sql
CREATE TABLE users (
 id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 age INT NOT NULL,
 last_login TIMESTAMP
);
```

```sql
INSERT INTO users (id,age,last_login) VALUES (NULL,123,NOW());
```

    Query OK, 1 row affected (0.02 sec)

```sql
INSERT INTO users (id,age,last_login) VALUES (NULL,NULL,NOW());
```

    ERROR 1048 (23000): Column 'age' cannot be null

```sql
INSERT INTO users (id,age,last_login) VALUES (NULL,123,NULL);
```

    Query OK, 1 row affected (0.03 sec)

-   最初の`INSERT`文は、 `AUTO_INCREMENT`列目に`NULL`割り当てることができるため成功します。TiDBはシーケンス番号を自動的に生成します。
-   2 番目の`INSERT`ステートメントは、 `age`列目が`NOT NULL`として定義されているため失敗します。
-   3番目の`INSERT`文は、 `last_login`列目が明示的に`NOT NULL`として定義されていないため成功します。NULL値はデフォルトで許可されています。

## チェック {#check}

> **注記：**
>
> `CHECK`制約機能はデフォルトで無効になっています。有効にするには、 [`tidb_enable_check_constraint`](/system-variables.md#tidb_enable_check_constraint-new-in-v720)変数を`ON`に設定する必要があります。

制約`CHECK`は、テーブル内の列の値を、指定された条件を満たすように制限します。制約`CHECK`テーブルに追加されると、TiDBはテーブルへのデータの挿入または更新時に制約が満たされているかどうかを確認します。制約が満たされていない場合は、エラーが返されます。

TiDB の`CHECK`制約の構文は MySQL と同じです。

```sql
[CONSTRAINT [symbol]] CHECK (expr) [[NOT] ENFORCED]
```

構文の説明:

-   `[]` : `[]`内の内容はオプションです。
-   `CONSTRAINT [symbol]` : `CHECK`の制約の名前を指定します。
-   `CHECK (expr)` : 制約条件を指定します。ここで、 `expr`ブール式である必要があります。テーブルの各行について、この式の計算結果は`TRUE` 、 `FALSE` 、または`UNKNOWN` ( `NULL`値の場合) のいずれかである必要があります。ある行の計算結果が`FALSE`場合、制約に違反していることを示します。
-   `[NOT] ENFORCED` : 制約チェックを実装するかどうかを指定します。これを使用して、制約`CHECK`有効または無効にすることができます。

### <code>CHECK</code>制約を追加する {#add-code-check-code-constraints}

TiDB では、 [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)または[`ALTER TABLE`](/sql-statements/sql-statement-modify-column.md)ステートメントのいずれかを使用して、テーブルに`CHECK`制約を追加できます。

-   `CREATE TABLE`ステートメントを使用して`CHECK`制約を追加する例:

    ```sql
    CREATE TABLE t(a INT CHECK(a > 10) NOT ENFORCED, b INT, c INT, CONSTRAINT c1 CHECK (b > c));
    ```

-   `ALTER TABLE`ステートメントを使用して`CHECK`制約を追加する例:

    ```sql
    ALTER TABLE t ADD CONSTRAINT CHECK (1 < c);
    ```

制約`CHECK`追加または有効化する際、TiDBはテーブル内の既存データをチェックします。制約に違反するデータが存在する場合、制約`CHECK`追加する操作は失敗し、エラーが返されます。

`CHECK`制約を追加する場合、制約名を指定するか、未指定のままにすることができます。制約名を指定しない場合は、TiDB が`<tableName>_chk_<1, 2, 3...>`形式で自動的に制約名を生成します。

### <code>CHECK</code>制約のビュー {#view-code-check-code-constraints}

[`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md)ステートメントを使用すると、テーブル内の制約情報を表示できます。例:

```sql
SHOW CREATE TABLE t;
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                                                                                                                                                                                                     |
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| t     | CREATE TABLE `t` (
  `a` int DEFAULT NULL,
  `b` int DEFAULT NULL,
  `c` int DEFAULT NULL,
CONSTRAINT `c1` CHECK ((`b` > `c`)),
CONSTRAINT `t_chk_1` CHECK ((`a` > 10)) /*!80016 NOT ENFORCED */,
CONSTRAINT `t_chk_2` CHECK ((1 < `c`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

### <code>CHECK</code>制約を削除する {#delete-code-check-code-constraints}

`CHECK`制約を削除する場合は、削除する制約の名前を指定する必要があります。例：

```sql
ALTER TABLE t DROP CONSTRAINT t_chk_1;
```

### <code>CHECK</code>制約を有効または無効にする {#enable-or-disable-code-check-code-constraints}

テーブルに[`CHECK`制約を追加する](#add-check-constraints)設定すると、データの挿入または更新時に TiDB が制約チェックを実装する必要があるかどうかを指定できます。

-   `NOT ENFORCED`指定すると、TiDB はデータの挿入または更新時に制約条件をチェックしません。
-   `NOT ENFORCED`指定されていないか`ENFORCED`指定されている場合、TiDB はデータの挿入または更新中に制約条件をチェックします。

制約を追加するときに`[NOT] ENFORCED`指定するだけでなく、 `ALTER TABLE`ステートメントを使用して`CHECK`制約を有効または無効にすることもできます。例：

```sql
ALTER TABLE t ALTER CONSTRAINT c1 NOT ENFORCED;
```

### MySQLの互換性 {#mysql-compatibility}

-   列（例： `ALTER TABLE t ADD COLUMN a CHECK(a > 0)` ）の追加時に`CHECK`制約を追加することはサポートされていません。この場合、列のみが正常に追加され、TiDBは`CHECK`制約を無視し、エラーを報告しません。
-   `ALTER TABLE t CHANGE a b int CHECK(b > 0)`使用して`CHECK`制約を追加することはサポートされていません。この文を実行すると、TiDBはエラーを報告します。

## ユニークキー {#unique-key}

一意制約とは、一意のインデックスと主キー列内のすべての非 NULL 値が一意であることを意味します。

### 楽観的な取引 {#optimistic-transactions}

デフォルトでは、楽観的トランザクションの場合、TiDB は実行フェーズで一意制約[怠惰に](/transaction-overview.md#lazy-check-of-constraints)チェックし、コミット フェーズで厳密にチェックします。これにより、ネットワーク オーバーヘッドが削減され、パフォーマンスが向上します。

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

楽観的ロックと`tidb_constraint_check_in_place=OFF`場合：

```sql
BEGIN OPTIMISTIC;
INSERT INTO users (username) VALUES ('jane'), ('chris'), ('bill');
```

    Query OK, 3 rows affected (0.00 sec)
    Records: 3  Duplicates: 0  Warnings: 0

```sql
INSERT INTO users (username) VALUES ('steve'),('elizabeth');
```

    Query OK, 2 rows affected (0.00 sec)
    Records: 2  Duplicates: 0  Warnings: 0

```sql
COMMIT;
```

    ERROR 1062 (23000): Duplicate entry 'bill' for key 'users.username'

前述の楽観的例では、トランザクションがコミットされるまで一意性チェックが延期されました。その結果、値`bill`が既に存在していたため、重複キーエラーが発生しました。

この動作を無効にするには、 [`tidb_constraint_check_in_place`](/system-variables.md#tidb_constraint_check_in_place)を`ON`に設定します。 `tidb_constraint_check_in_place=ON`に設定すると、ステートメント実行時に一意制約がチェックされます。この変数は楽観的トランザクションにのみ適用されることに注意してください。悲観的トランザクションの場合は、 [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)変数を使用してこの動作を制御できます。

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

```sql
SET tidb_constraint_check_in_place = ON;
```

    Query OK, 0 rows affected (0.00 sec)

```sql
BEGIN OPTIMISTIC;
```

    Query OK, 0 rows affected (0.00 sec)

```sql
INSERT INTO users (username) VALUES ('jane'), ('chris'), ('bill');
```

    ERROR 1062 (23000): Duplicate entry 'bill' for key 'users.username'

最初の`INSERT`ステートメントで重複キーエラーが発生しました。これによりネットワーク通信のオーバーヘッドが増加し、挿入操作のスループットが低下する可能性があります。

### 悲観的な取引 {#pessimistic-transactions}

悲観的トランザクションでは、一意のインデックスの挿入または更新を必要とする SQL ステートメントが実行されると、TiDB はデフォルトで`UNIQUE`制約をチェックします。

```sql
DROP TABLE IF EXISTS users;
CREATE TABLE users (
 id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
 username VARCHAR(60) NOT NULL,
 UNIQUE KEY (username)
);
INSERT INTO users (username) VALUES ('dave'), ('sarah'), ('bill');

BEGIN PESSIMISTIC;
INSERT INTO users (username) VALUES ('jane'), ('chris'), ('bill');
```

    ERROR 1062 (23000): Duplicate entry 'bill' for key 'users.username'

悲観的トランザクションのパフォーマンスを向上させるには、変数[`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630) `OFF`に設定できます。これにより、TiDB は一意インデックスの一意制約チェックを（このインデックスが次にロックを必要とするとき、またはトランザクションがコミットされるときまで）延期し、対応する悲観的ロックをスキップします。この変数を使用する際は、以下の点に注意してください。

-   遅延された一意制約チェックのため、悲観的トランザクションをコミットすると、TiDB は一意制約を満たさない結果を読み取り、エラー`Duplicate entry`返す場合があります。このエラーが発生すると、TiDB は現在のトランザクションをロールバックします。

    次の例では、ロックを`bill`にスキップするため、TiDB は一意性制約を満たさない結果を取得する可能性があります。

    ```sql
    SET tidb_constraint_check_in_place_pessimistic = OFF;
    BEGIN PESSIMISTIC;
    INSERT INTO users (username) VALUES ('jane'), ('chris'), ('bill'); -- Query OK, 3 rows affected
    SELECT * FROM users FOR UPDATE;
    ```

    次の出力例のように、TiDB のクエリ結果には`bills`が 2 つ含まれており、一意性制約を満たしていません。

    ```sql
    +----+----------+
    | id | username |
    +----+----------+
    | 1  | dave     |
    | 2  | sarah    |
    | 3  | bill     |
    | 7  | jane     |
    | 8  | chris    |
    | 9  | bill     |
    +----+----------+
    ```

    このとき、トランザクションがコミットされると、TiDB は一意制約チェックを実行し、エラー`Duplicate entry`報告して、トランザクションをロールバックします。

    ```sql
    COMMIT;
    ```

        ERROR 1062 (23000): Duplicate entry 'bill' for key 'users.username'

-   この変数が無効になっている場合、データの書き込みを必要とする悲観的トランザクションをコミットすると、 `Write conflict`エラーが返される可能性があります。このエラーが発生すると、TiDBは現在のトランザクションをロールバックします。

    次の例のように、2つの同時トランザクションが同じテーブルにデータを挿入する必要がある場合、悲観的ロックをスキップすると、トランザクションをコミットしたときにTiDBはエラー`Write conflict`を返します。そして、トランザクションはロールバックされます。

    ```sql
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(60) NOT NULL,
    UNIQUE KEY (username)
    );

    SET tidb_constraint_check_in_place_pessimistic = OFF;
    BEGIN PESSIMISTIC;
    INSERT INTO users (username) VALUES ('jane'), ('chris'), ('bill'); -- Query OK, 3 rows affected
    ```

    同時に、別のセッションが同じテーブルに`bill`挿入します。

    ```sql
    INSERT INTO users (username) VALUES ('bill'); -- Query OK, 1 row affected
    ```

    その後、最初のセッションでトランザクションをコミットすると、TiDB は`Write conflict`エラーを報告します。

    ```sql
    COMMIT;
    ```

        ERROR 9007 (HY000): Write conflict, txnStartTS=435688780611190794, conflictStartTS=435688783311536129, conflictCommitTS=435688783311536130, key={tableID=74, indexID=1, indexValues={bill, }} primary={tableID=74, indexID=1, indexValues={bill, }}, reason=LazyUniquenessCheck [try again later]

-   この変数が無効になっている場合、複数の悲観的トランザクション間で書き込み競合が発生すると、他の悲観的トランザクションがコミットされた際に悲観的ロックが強制的にロールバックされ、エラー`Pessimistic lock not found`が発生する可能性があります。このエラーが発生した場合、悲観的トランザクションの一意制約チェックを延期することが、アプリケーションのシナリオに適していないことを意味します。この場合、競合を回避するようにアプリケーションロジックを調整するか、エラー発生後にトランザクションを再試行することを検討してください。

-   この変数が無効になっている場合、悲観的トランザクションで DML ステートメントを実行するとエラー`8147: LazyUniquenessCheckFailure`が返される可能性があります。

    > **注記：**
    >
    > `8147`エラーが発生すると、TiDB は現在のトランザクションをロールバックします。

    次の例のように、 `INSERT`のステートメントの実行時にTiDBはロックをスキップします。その後、 `DELETE`ステートメントの実行時にTiDBはユニークインデックスをロックし、ユニーク制約をチェックします。そのため、 `DELETE`ステートメントでエラーが報告されます。

    ```sql
    SET tidb_constraint_check_in_place_pessimistic = OFF;
    BEGIN PESSIMISTIC;
    INSERT INTO users (username) VALUES ('jane'), ('chris'), ('bill'); -- Query OK, 3 rows affected
    DELETE FROM users where username = 'bill';
    ```

        ERROR 8147 (23000): transaction aborted because lazy uniqueness check is enabled and an error occurred: [kv:1062]Duplicate entry 'bill' for key 'users.username'

-   この変数が無効になっている場合、 `1062 Duplicate entry`エラーは現在の SQL 文に起因しない可能性があります。そのため、トランザクションが同じ名前のインデックスを持つ複数のテーブルを操作する場合、 `1062`番目のエラーメッセージを確認して、実際にどのインデックスにエラーが発生しているかを特定する必要があります。

## 主キー {#primary-key}

MySQLと同様に、主キー制約には一意制約が含まれます。つまり、主キー制約を作成することは、一意制約を持つことと同じです。また、TiDBの他の主キー制約もMySQLと同様です。

例えば：

```sql
CREATE TABLE t1 (a INT NOT NULL PRIMARY KEY);
```

    Query OK, 0 rows affected (0.12 sec)

```sql
CREATE TABLE t2 (a INT NULL PRIMARY KEY);
```

    ERROR 1171 (42000): All parts of a PRIMARY KEY must be NOT NULL; if you need NULL in a key, use UNIQUE instead

```sql
CREATE TABLE t3 (a INT NOT NULL PRIMARY KEY, b INT NOT NULL PRIMARY KEY);
```

    ERROR 1068 (42000): Multiple primary key defined

```sql
CREATE TABLE t4 (a INT NOT NULL, b INT NOT NULL, PRIMARY KEY (a,b));
```

    Query OK, 0 rows affected (0.10 sec)

-   列`a`主キーとして定義されており、NULL 値が許可されないため、テーブル`t2`を作成できませんでした。
-   テーブルには主キーを 1 つしか持てないため、テーブル`t3`を作成できませんでした。
-   主キーは 1 つしか存在できませんが、TiDB では複数の列を複合主キーとして定義することがサポートされているため、テーブル`t4`正常に作成されました。

上記のルールに加えて、TiDBは現在、 `NONCLUSTERED`型の主キーの追加と削除のみをサポートしています。例えば：

```sql
CREATE TABLE t5 (a INT NOT NULL, b INT NOT NULL, PRIMARY KEY (a,b) CLUSTERED);
ALTER TABLE t5 DROP PRIMARY KEY;
```

    ERROR 8200 (HY000): Unsupported drop primary key when the table is using clustered index

```sql
CREATE TABLE t5 (a INT NOT NULL, b INT NOT NULL, PRIMARY KEY (a,b) NONCLUSTERED);
ALTER TABLE t5 DROP PRIMARY KEY;
```

    Query OK, 0 rows affected (0.10 sec)

`CLUSTERED`型の主キーの詳細については[クラスター化インデックス](/clustered-indexes.md)を参照してください。

## 外部キー {#foreign-key}

> **注記：**
>
> TiDBはv6.6.0以降、 [FOREIGN KEY制約](/foreign-key.md)サポートします。v6.6.0より前のバージョンでは、TiDBは外部キー制約の作成と削除をサポートしていますが、実際には制約は有効になっていません。TiDBをv6.6.0以降にアップグレードすると、無効な外部キーを削除し、新しい外部キーを作成することで、外部キー制約を有効にすることができます。この機能はv8.5.0で一般提供開始となります。

TiDB は、DDL コマンドで`FOREIGN KEY`制約の作成をサポートしています。

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

```sql
SELECT table_name, column_name, constraint_name, referenced_table_name, referenced_column_name
FROM information_schema.key_column_usage WHERE table_name IN ('users', 'orders');
```

    +------------+-------------+-----------------+-----------------------+------------------------+
    | table_name | column_name | constraint_name | referenced_table_name | referenced_column_name |
    +------------+-------------+-----------------+-----------------------+------------------------+
    | users      | id          | PRIMARY         | NULL                  | NULL                   |
    | orders     | id          | PRIMARY         | NULL                  | NULL                   |
    | orders     | user_id     | fk_user_id      | users                 | id                     |
    +------------+-------------+-----------------+-----------------------+------------------------+
    3 rows in set (0.00 sec)

TiDB は、 `ALTER TABLE`コマンドを介して`DROP FOREIGN KEY`と`ADD FOREIGN KEY`構文もサポートします。

```sql
ALTER TABLE orders DROP FOREIGN KEY fk_user_id;
ALTER TABLE orders ADD FOREIGN KEY fk_user_id (user_id) REFERENCES users(id);
```
