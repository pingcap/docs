---
title: Constraints
summary: TiDBはMySQLと同様の制約をサポートします。NOT NULL制約はMySQLと同じです。CHECK制約はデフォルトでは無効ですが、有効にすることができます。CHECK制約を追加、削除、有効または無効にすることができます。一意制約は一意のインデックスと主キー列内の非null値が一意であることを意味します。主キー制約には一意制約が含まれます。外部キー制約は実験的機能としてサポートされています。制約の追加、削除、有効または無効にすることができます。
---

# 制約 {#constraints}

TiDB は、MySQL とほぼ同じ制約をサポートします。

## NULLではありません {#not-null}

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

-   `AUTO_INCREMENT`列に`NULL`割り当てることができるため、最初の`INSERT`ステートメントは成功します。 TiDB はシーケンス番号を自動的に生成します。
-   2 番目の`INSERT`ステートメントは、 `age`列が`NOT NULL`として定義されているため失敗します。
-   `INSERT`列が明示的に`NOT NULL`として定義されていないため、 `last_login`番目の 1 ステートメントは成功します。デフォルトでは NULL 値が許可されます。

## チェック {#check}

> **注記：**
>
> `CHECK`制約機能はデフォルトでは無効になっています。これを有効にするには、変数[`tidb_enable_check_constraint`](/system-variables.md#tidb_enable_check_constraint-new-in-v720)を`ON`に設定する必要があります。

`CHECK`制約は、指定した条件を満たすようにテーブル内の列の値を制限します。 `CHECK`制約がテーブルに追加されると、TiDB はテーブルへのデータの挿入または更新中に制約が満たされているかどうかをチェックします。制約が満たされない場合は、エラーが返されます。

TiDB の`CHECK`制約の構文は MySQL の構文と同じです。

```sql
[CONSTRAINT [symbol]] CHECK (expr) [[NOT] ENFORCED]
```

構文の説明:

-   `[]` : `[]`以内の内容は任意です。
-   `CONSTRAINT [symbol]` : `CHECK`制約の名前を指定します。
-   `CHECK (expr)` : 制約条件を指定します。2 `expr`ブール式である必要があります。テーブル内の各行について、この式の計算結果は`TRUE` 、 `FALSE` 、または`UNKNOWN` (値が`NULL`個の場合) のいずれかである必要があります。計算結果が行ごとに`FALSE`の場合、制約に違反していることを示します。
-   `[NOT] ENFORCED` : 制約チェックを実装するかどうかを指定します。これを使用して、 `CHECK`制約を有効または無効にすることができます。

### <code>CHECK</code>制約を追加する {#add-code-check-code-constraints}

TiDB では、 [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)または[`ALTER TABLE`](/sql-statements/sql-statement-modify-column.md)ステートメントを使用してテーブルに`CHECK`制約を追加できます。

-   `CREATE TABLE`ステートメントを使用して`CHECK`制約を追加する例:

    ```sql
    CREATE TABLE t(a INT CHECK(a > 10) NOT ENFORCED, b INT, c INT, CONSTRAINT c1 CHECK (b > c));
    ```

-   `ALTER TABLE`ステートメントを使用して`CHECK`制約を追加する例:

    ```sql
    ALTER TABLE t ADD CONSTRAINT CHECK (1 < c);
    ```

`CHECK`制約を追加または有効にすると、TiDB はテーブル内の既存のデータをチェックします。データが制約に違反している場合、 `CHECK`制約を追加する操作は失敗し、エラーが返されます。

`CHECK`制約を追加する場合、制約名を指定することも、名前を指定しないままにすることもできます。制約名が指定されていない場合、TiDB は`<tableName>_chk_<1, 2, 3...>`形式で制約名を自動的に生成します。

### <code>CHECK</code>制約のビュー {#view-code-check-code-constraints}

[`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md)ステートメントを使用すると、テーブル内の制約情報を表示できます。例えば：

```sql
SHOW CREATE TABLE t;
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                                                                                                                                                                                                     |
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| t     | CREATE TABLE `t` (
  `a` int(11) DEFAULT NULL,
  `b` int(11) DEFAULT NULL,
  `c` int(11) DEFAULT NULL,
CONSTRAINT `c1` CHECK ((`b` > `c`)),
CONSTRAINT `t_chk_1` CHECK ((`a` > 10)) /*!80016 NOT ENFORCED */,
CONSTRAINT `t_chk_2` CHECK ((1 < `c`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

### <code>CHECK</code>制約の削除 {#delete-code-check-code-constraints}

`CHECK`制約を削除する場合は、削除する制約の名前を指定する必要があります。例えば：

```sql
ALTER TABLE t DROP CONSTRAINT t_chk_1;
```

### <code>CHECK</code>制約を有効または無効にする {#enable-or-disable-code-check-code-constraints}

テーブルに[`CHECK`制約の追加](#add-check-constraints)を設定すると、TiDB がデータの挿入または更新中に制約チェックを実装する必要があるかどうかを指定できます。

-   `NOT ENFORCED`を指定した場合、TiDB はデータの挿入または更新時に制約条件をチェックしません。
-   `NOT ENFORCED`が指定されない場合、または`ENFORCED`が指定された場合、TiDB はデータの挿入または更新時に制約条件をチェックします。

制約を追加するときに`[NOT] ENFORCED`を指定するだけでなく、 `ALTER TABLE`ステートメントを使用して`CHECK`制約を有効または無効にすることもできます。例えば：

```sql
ALTER TABLE t ALTER CONSTRAINT c1 NOT ENFORCED;
```

### MySQLの互換性 {#mysql-compatibility}

-   列 (たとえば、 `ALTER TABLE t ADD COLUMN a CHECK(a > 0)` ) を追加するときに`CHECK`制約を追加することはサポートされていません。この場合、列のみが正常に追加され、TiDB はエラーを報告せずに`CHECK`制約を無視します。
-   `ALTER TABLE t CHANGE a b int CHECK(b > 0)`を使用して`CHECK`制約を追加することはサポートされていません。このステートメントが実行されると、TiDB はエラーを報告します。

## 固有のキー {#unique-key}

一意制約とは、一意のインデックスと主キー列内のすべての非 null 値が一意であることを意味します。

### 楽観的な取引 {#optimistic-transactions}

デフォルトでは、楽観的トランザクションの場合、TiDB は実行フェーズおよび厳密にコミット フェーズで一意の制約[怠惰に](/transaction-overview.md#lazy-check-of-constraints)をチェックします。これにより、ネットワーク オーバーヘッドが削減され、パフォーマンスが向上します。

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

楽観的ロックと`tidb_constraint_check_in_place=OFF`の場合:

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

前述の楽観的例では、トランザクションがコミットされるまで一意のチェックが延期されました。値`bill`がすでに存在していたため、重複キー エラーが発生しました。

[`tidb_constraint_check_in_place`](/system-variables.md#tidb_constraint_check_in_place) ～ `ON`を設定すると、この動作を無効にできます。 `tidb_constraint_check_in_place=ON`の場合、ステートメントの実行時に一意制約がチェックされます。この変数は楽観的トランザクションにのみ適用されることに注意してください。悲観的トランザクションの場合、変数[`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)を使用してこの動作を制御できます。

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

最初の`INSERT`ステートメントにより、重複キー エラーが発生しました。これにより、追加のネットワーク通信オーバーヘッドが発生し、挿入操作のスループットが低下する可能性があります。

### 悲観的な取引 {#pessimistic-transactions}

悲観的トランザクションでは、一意のインデックスの挿入または更新を必要とする SQL ステートメントが実行されるときに、TiDB はデフォルトで`UNIQUE`制約をチェックします。

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

悲観的トランザクションのパフォーマンスを向上させるには、変数[`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)を`OFF`に設定します。これにより、TiDB が一意のインデックスの一意制約チェックを (次回このインデックスがロックを必要とするとき、またはトランザクションがコミットされるときまで) 延期できるようになります。 ) 対応する悲観的ロックをスキップします。この変数を使用するときは、次の点に注意してください。

-   一意制約チェックが遅延されるため、悲観的トランザクションをコミットすると、TiDB が一意制約を満たさない結果を読み取り、 `Duplicate entry`エラーを返す可能性があります。このエラーが発生すると、TiDB は現在のトランザクションをロールバックします。

    次の例ではロックを`bill`にスキップするため、TiDB は一意性制約を満たさない結果を取得する可能性があります。

    ```sql
    SET tidb_constraint_check_in_place_pessimistic = OFF;
    BEGIN PESSIMISTIC;
    INSERT INTO users (username) VALUES ('jane'), ('chris'), ('bill'); -- Query OK, 3 rows affected
    SELECT * FROM users FOR UPDATE;
    ```

    次の出力例のように、TiDB のクエリ結果には 2 つの`bills`含まれており、一意性制約を満たしていません。

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

    この時点で、トランザクションがコミットされている場合、TiDB は一意の制約チェックを実行し、 `Duplicate entry`エラーを報告し、トランザクションをロールバックします。

    ```sql
    COMMIT;
    ```

        ERROR 1062 (23000): Duplicate entry 'bill' for key 'users.username'

-   この変数が無効になっている場合、データを書き込む必要がある悲観的トランザクションをコミットすると、 `Write conflict`エラーが返される可能性があります。このエラーが発生すると、TiDB は現在のトランザクションをロールバックします。

    次の例のように、2 つの同時トランザクションが同じテーブルにデータを挿入する必要がある場合、悲観的ロックをスキップすると、トランザクションをコミットするときに TiDB が`Write conflict`エラーを返します。そしてトランザクションはロールバックされます。

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

    同時に、別のセッションが同じテーブルに`bill`を挿入します。

    ```sql
    INSERT INTO users (username) VALUES ('bill'); -- Query OK, 1 row affected
    ```

    その後、最初のセッションでトランザクションをコミットすると、TiDB は`Write conflict`エラーを報告します。

    ```sql
    COMMIT;
    ```

        ERROR 9007 (HY000): Write conflict, txnStartTS=435688780611190794, conflictStartTS=435688783311536129, conflictCommitTS=435688783311536130, key={tableID=74, indexID=1, indexValues={bill, }} primary={tableID=74, indexID=1, indexValues={bill, }}, reason=LazyUniquenessCheck [try again later]

-   この変数が無効になっている場合、複数の悲観的トランザクション間で書き込み競合が発生すると、他の悲観的トランザクションがコミットされるときに悲観的ロックが強制的にロールバックされ、その結果`Pessimistic lock not found`エラーが発生する可能性があります。このエラーが発生した場合は、悲観的トランザクションの一意制約チェックの延期がアプリケーション シナリオに適していないことを意味します。この場合、アプリケーション ロジックを調整して競合を回避するか、エラー発生後にトランザクションを再試行することを検討してください。

-   この変数が無効になっている場合、悲観的トランザクションで DML ステートメントを実行すると、エラー`8147: LazyUniquenessCheckFailure`が返される可能性があります。

    > **注記：**
    >
    > `8147`エラーが発生すると、TiDB は現在のトランザクションをロールバックします。

    次の例のように、 `INSERT`ステートメントの実行時に、TiDB はロックをスキップします。次に、 `DELETE`ステートメントの実行時に、TiDB は一意のインデックスをロックし、一意の制約をチェックするため、 `DELETE`ステートメントでエラーが報告されることがわかります。

    ```sql
    SET tidb_constraint_check_in_place_pessimistic = OFF;
    BEGIN PESSIMISTIC;
    INSERT INTO users (username) VALUES ('jane'), ('chris'), ('bill'); -- Query OK, 3 rows affected
    DELETE FROM users where username = 'bill';
    ```

        ERROR 8147 (23000): transaction aborted because lazy uniqueness check is enabled and an error occurred: [kv:1062]Duplicate entry 'bill' for key 'users.username'

-   この変数が無効になっている場合、 `1062 Duplicate entry`エラーは現在の SQL ステートメントからのものではない可能性があります。したがって、トランザクションが同じ名前のインデックスを持つ複数のテーブルで動作する場合は、 `1062`エラー メッセージを確認して、実際にどのインデックスからエラーが発生しているのかを確認する必要があります。

## 主キー {#primary-key}

MySQL と同様、主キー制約には一意制約が含まれます。つまり、主キー制約の作成は一意制約を持つことと同じです。さらに、TiDB の他の主キー制約も MySQL の制約と似ています。

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

-   列`a`が主キーとして定義されており、NULL 値が許可されていないため、テーブル`t2`の作成に失敗しました。
-   テーブルには主キーが 1 つしか持てないため、テーブル`t3`の作成に失敗しました。
-   主キーは 1 つしか存在できませんが、TiDB は複合主キーとして複数の列の定義をサポートしているため、テーブル`t4`正常に作成されました。

上記のルールに加えて、TiDB は現在、 `NONCLUSTERED`種類の主キーの追加と削除のみをサポートしています。例えば：

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

`CLUSTERED`タイプの主キーの詳細については、 [クラスター化インデックス](/clustered-indexes.md)を参照してください。

## 外部キー {#foreign-key}

> **注記：**
>
> v6.6.0 以降、TiDB は実験的機能として[FOREIGN KEY 制約](/foreign-key.md)をサポートします。 v6.6.0 より前では、TiDB は外部キー制約の作成と削除をサポートしていましたが、その制約は実際には有効ではありませんでした。 TiDB を v6.6.0 にアップグレードした後、無効な外部キーを削除し、新しい外部キーを作成して、外部キー制約を有効にすることができます。

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

TiDB は、 `ALTER TABLE`コマンドを介して`DROP FOREIGN KEY`と`ADD FOREIGN KEY`の構文もサポートします。

```sql
ALTER TABLE orders DROP FOREIGN KEY fk_user_id;
ALTER TABLE orders ADD FOREIGN KEY fk_user_id (user_id) REFERENCES users(id);
```
