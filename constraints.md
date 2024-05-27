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

-   最初の`INSERT`文は、 `AUTO_INCREMENT`列に`NULL`を割り当てることができるため成功します。TiDB はシーケンス番号を自動的に生成します。
-   2 番目の`INSERT`ステートメントは、 `age`列が`NOT NULL`として定義されているため失敗します。
-   3 番目の`INSERT`ステートメントは、 `last_login`列が`NOT NULL`として明示的に定義されていないため成功します。デフォルトでは NULL 値が許可されます。

## チェック {#check}

> **注記：**
>
> `CHECK`制約機能はデフォルトで無効になっています。有効にするには、 [`tidb_enable_check_constraint`](/system-variables.md#tidb_enable_check_constraint-new-in-v720)変数を`ON`に設定する必要があります。

`CHECK`制約は、テーブル内の列の値を、指定した条件を満たすように制限します。3 制約`CHECK`テーブルに追加されると、TiDB はテーブルへのデータの挿入または更新中に制約が満たされているかどうかを確認します。制約が満たされていない場合は、エラーが返されます。

TiDB の`CHECK`制約の構文は、MySQL の構文と同じです。

```sql
[CONSTRAINT [symbol]] CHECK (expr) [[NOT] ENFORCED]
```

構文の説明:

-   `[]` : `[]`内の内容はオプションです。
-   `CONSTRAINT [symbol]` : `CHECK`番目の制約の名前を指定します。
-   `CHECK (expr)` : 制約条件を指定します。2 `expr`ブール式である必要があります。テーブルの各行について、この式の計算結果は`TRUE` 、 `FALSE` 、または`UNKNOWN` ( `NULL`の値の場合) のいずれかである必要があります。行の計算結果が`FALSE`の場合、制約に違反していることを示します。
-   `[NOT] ENFORCED` : 制約チェックを実装するかどうかを指定します。これを使用して、制約`CHECK`を有効または無効にすることができます。

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

`CHECK`制約を追加または有効にすると、TiDB はテーブル内の既存のデータをチェックします。制約に違反するデータがある場合、 `CHECK`制約を追加する操作は失敗し、エラーが返されます。

`CHECK`制約を追加する場合、制約名を指定するか、名前を指定しないままにすることができます。制約名が指定されていない場合、TiDB は`<tableName>_chk_<1, 2, 3...>`形式で制約名を自動的に生成します。

### <code>CHECK</code>制約のビュー {#view-code-check-code-constraints}

[`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md)ステートメントを使用して、制約情報をテーブルで表示できます。例:

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

### <code>CHECK</code>制約を削除する {#delete-code-check-code-constraints}

`CHECK`制約を削除する場合は、削除する制約の名前を指定する必要があります。例:

```sql
ALTER TABLE t DROP CONSTRAINT t_chk_1;
```

### <code>CHECK</code>制約を有効または無効にする {#enable-or-disable-code-check-code-constraints}

テーブルに[`CHECK`制約を追加する](#add-check-constraints)設定すると、データの挿入または更新中に TiDB が制約チェックを実装する必要があるかどうかを指定できます。

-   `NOT ENFORCED`を指定すると、TiDB はデータの挿入または更新時に制約条件をチェックしません。
-   `NOT ENFORCED`が指定されていない場合、または`ENFORCED`指定されている場合、TiDB はデータの挿入または更新中に制約条件をチェックします。

制約を追加するときに`[NOT] ENFORCED`指定することに加えて、 `ALTER TABLE`ステートメントを使用して`CHECK`制約を有効または無効にすることもできます。例:

```sql
ALTER TABLE t ALTER CONSTRAINT c1 NOT ENFORCED;
```

### MySQL 互換性 {#mysql-compatibility}

-   列 (たとえば、 `ALTER TABLE t ADD COLUMN a CHECK(a > 0)` ) を追加するときに`CHECK`制約を追加することはサポートされていません。この場合、列のみが正常に追加され、TiDB はエラーを報告せずに`CHECK`制約を無視します。
-   `ALTER TABLE t CHANGE a b int CHECK(b > 0)`使用して`CHECK`制約を追加することはサポートされていません。このステートメントを実行すると、TiDB はエラーを報告します。

## ユニークキー {#unique-key}

一意制約とは、一意のインデックスと主キー列内のすべての NULL 以外の値が一意であることを意味します。

### 楽観的な取引 {#optimistic-transactions}

デフォルトでは、楽観的トランザクションの場合、TiDB は実行フェーズで一意制約[怠惰に](/transaction-overview.md#lazy-check-of-constraints)をチェックし、コミット フェーズで厳密にチェックします。これにより、ネットワーク オーバーヘッドが削減され、パフォーマンスが向上します。

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

楽観的ロックと`tidb_constraint_check_in_place=OFF`場合:

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

前述の楽観的例では、トランザクションがコミットされるまで一意のチェックが延期されました。値`bill`がすでに存在していたため、重複キー エラーが発生していました。

この動作を無効にするには、 [`tidb_constraint_check_in_place`](/system-variables.md#tidb_constraint_check_in_place)を`ON`に設定します。 `tidb_constraint_check_in_place=ON`の場合、ステートメントの実行時に一意制約がチェックされます。 この変数は楽観的トランザクションにのみ適用されることに注意してください。悲観的トランザクションの場合、 [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)変数を使用してこの動作を制御できます。

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

最初の`INSERT`ステートメントで重複キー エラーが発生しました。これにより、追加のネットワーク通信オーバーヘッドが発生し、挿入操作のスループットが低下する可能性があります。

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

悲観的トランザクションのパフォーマンスを向上させるには、 [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)変数を`OFF`に設定します。これにより、TiDB は一意のインデックスの一意制約チェックを延期し (このインデックスがロックを必要とする次の時点、またはトランザクションがコミットされる時点まで)、対応する悲観的ロックをスキップできます。この変数を使用する場合は、次の点に注意してください。

-   遅延された一意制約チェックにより、悲観的トランザクションをコミットすると、TiDB は一意制約を満たさない結果を読み取り、エラー`Duplicate entry`を返す場合があります。このエラーが発生すると、TiDB は現在のトランザクションをロールバックします。

    次の例では、ロックを`bill`にスキップするため、TiDB は一意性制約を満たさない結果を取得する可能性があります。

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

    このとき、トランザクションがコミットされると、TiDB は一意制約チェックを実行し、 `Duplicate entry`エラーを報告して、トランザクションをロールバックします。

    ```sql
    COMMIT;
    ```

        ERROR 1062 (23000): Duplicate entry 'bill' for key 'users.username'

-   この変数が無効になっている場合、データの書き込みが必要な悲観的トランザクションをコミットすると、 `Write conflict`エラーが返される可能性があります。このエラーが発生すると、TiDB は現在のトランザクションをロールバックします。

    次の例のように、2 つの同時トランザクションが同じテーブルにデータを挿入する必要がある場合、悲観的ロックをスキップすると、トランザクションをコミットしたときに TiDB は`Write conflict`エラーを返します。そして、トランザクションはロールバックされます。

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

-   この変数が無効になっている場合、複数の悲観的トランザクション間で書き込み競合が発生すると、他の悲観的トランザクションがコミットされたときに悲観的ロックが強制的にロールバックされ、 `Pessimistic lock not found`エラーが発生する可能性があります。このエラーが発生した場合は、悲観的トランザクションの一意制約チェックを延期することがアプリケーション シナリオに適していないことを意味します。この場合、競合を回避するためにアプリケーション ロジックを調整するか、エラー発生後にトランザクションを再試行することを検討してください。

-   この変数が無効になっている場合、悲観的トランザクションで DML ステートメントを実行するとエラー`8147: LazyUniquenessCheckFailure`が返される可能性があります。

    > **注記：**
    >
    > `8147`エラーが発生すると、TiDB は現在のトランザクションをロールバックします。

    次の例のように、 `INSERT`番目のステートメントの実行時に、TiDB はロックをスキップします。次に、 `DELETE`のステートメントの実行時に、TiDB は一意のインデックスをロックし、一意の制約をチェックするため、 `DELETE`のステートメントでエラーが報告されます。

    ```sql
    SET tidb_constraint_check_in_place_pessimistic = OFF;
    BEGIN PESSIMISTIC;
    INSERT INTO users (username) VALUES ('jane'), ('chris'), ('bill'); -- Query OK, 3 rows affected
    DELETE FROM users where username = 'bill';
    ```

        ERROR 8147 (23000): transaction aborted because lazy uniqueness check is enabled and an error occurred: [kv:1062]Duplicate entry 'bill' for key 'users.username'

-   この変数が無効になっている場合、 `1062 Duplicate entry`エラーは現在の SQL ステートメントからのものではない可能性があります。したがって、トランザクションが同じ名前のインデックスを持つ複数のテーブルで操作する場合、 `1062`エラー メッセージをチェックして、実際にエラーの原因となっているインデックスを見つける必要があります。

## 主キー {#primary-key}

MySQL と同様に、主キー制約には一意制約が含まれます。つまり、主キー制約を作成することは、一意制約を持つことと同じです。また、TiDB のその他の主キー制約も MySQL のものと似ています。

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

-   列`a`が主キーとして定義されており、NULL 値が許可されないため、テーブル`t2`を作成できませんでした。
-   テーブルには主キーを 1 つしか持てないため、テーブル`t3`を作成できませんでした。
-   主キーは 1 つしか存在できませんが、TiDB では複数の列を複合主キーとして定義することがサポートされているため、表`t4`正常に作成されました。

上記のルールに加えて、TiDB は現在、 `NONCLUSTERED`タイプの主キーの追加と削除のみをサポートしています。例:

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
> v6.6.0 以降、TiDB は[FOREIGN KEY制約](/foreign-key.md)を実験的機能としてサポートします。v6.6.0 より前の TiDB では、外部キー制約の作成と削除がサポートされていましたが、制約は実際には有効ではありませんでした。TiDB を v6.6.0 にアップグレードした後、無効な外部キーを削除して新しい外部キーを作成し、外部キー制約を有効にすることができます。

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

TiDB は、 `ALTER TABLE`コマンドを介して`DROP FOREIGN KEY`と`ADD FOREIGN KEY`の構文もサポートします。

```sql
ALTER TABLE orders DROP FOREIGN KEY fk_user_id;
ALTER TABLE orders ADD FOREIGN KEY fk_user_id (user_id) REFERENCES users(id);
```
