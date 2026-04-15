---
title: SELECT | TiDB SQL Statement Reference
summary: TiDBデータベースにおけるSELECT文の使用方法の概要。
---

# 選択 {#select}

`SELECT`ステートメントは、TiDB からデータを読み取るために使用されます。

## あらすじ {#synopsis}

```ebnf+diagram
SelectStmt ::=
    ( SelectStmtBasic | SelectStmtFromDualTable | SelectStmtFromTable )
    OrderBy? SelectStmtLimit? SelectLockOpt? SelectStmtIntoOption

SelectStmtBasic ::=
    "SELECT" SelectStmtOpts Field ("," Field)* ( "HAVING" Expression)?

SelectStmtFromDualTable ::=
    "SELECT" SelectStmtOpts Field ("," Field)* "FROM" "DUAL" WhereClause?

SelectStmtFromTable ::=
    "SELECT" SelectStmtOpts Field ("," Field)* "FROM" TableRefsClause
    WhereClause? GroupByClause? ( "HAVING" Expression)? WindowClause?

SelectStmtOpts ::=
    TableOptimizerHints DefaultFalseDistictOpt PriorityOpt SelectStmtSQLSmallResult
    SelectStmtSQLBigResult SelectStmtSQLBufferResult SelectStmtSQLCache SelectStmtCalcFoundRows
    SelectStmtStraightJoin

TableRefsClause ::=
    TableRef ( ',' TableRef )*

TableRef ::=
    TableFactor
|   JoinTable

TableFactor ::=
    TableName ( "PARTITION" "(" Identifier ("," Identifier)* ")" )? ("AS" TableAlias)? AsOfClause? TableSample?

JoinTable ::=
    TableRef
    (
        ("INNER" | "CROSS")? "JOIN" TableRef JoinClause?
        | "STRAIGHT_JOIN" TableRef "ON" Expression
        | ("LEFT" | "RIGHT") "OUTER"? "JOIN" TableRef JoinClause
        | "NATURAL" ("LEFT" | "RIGHT") "OUTER"? "JOIN" TableFactor
    )

JoinClause ::=
    ("ON" Expression
    | "USING" "(" ColumnNameList ")" )

AsOfClause ::=
    'AS' 'OF' 'TIMESTAMP' Expression

SelectStmtLimit ::=
    ("LIMIT" LimitOption ( ("," | "OFFSET") LimitOption )?
| "FETCH" ("FIRST" | "NEXT") LimitOption? ("ROW" | "ROWS") "ONLY" )

SelectLockOpt ::= 
    ( 'FOR' 'UPDATE' ( 'OF' TableList )? 'NOWAIT'?
|   'LOCK' 'IN' 'SHARE' 'MODE' )

TableList ::=
    TableName ( ',' TableName )*

WhereClause ::=
    "WHERE" Expression

GroupByClause ::=
    "GROUP" "BY" Expression

OrderBy ::=
    "ORDER" "BY" Expression

WindowClause ::=
    "WINDOW" WindowDefinition ("," WindowDefinition)*

TableSample ::=
    'TABLESAMPLE' 'REGIONS' '(' ')'
```

## 構文要素の説明 {#description-of-the-syntax-elements}

| 構文要素                               | 説明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| :--------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `TableOptimizerHints`              | これは、TiDB のオプティマイザーの動作を制御するためのヒントです。詳細については、[オプティマイザのヒント](/optimizer-hints.md)を参照してください。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `ALL` 、 `DISTINCT` 、 `DISTINCTROW` | `ALL` 、 `DISTINCT` / `DISTINCTROW`修飾子は、重複する行を返すかどうかを指定します。ALL（デフォルト）を指定すると、一致するすべての行が返されます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `HIGH_PRIORITY`                    | `HIGH_PRIORITY`は、現在のステートメントに他のステートメントよりも高い優先順位を与えます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `SQL_CALC_FOUND_ROWS`              | TiDBはこの機能をサポートしておらず、 [`tidb_enable_noop_functions=1`](/system-variables.md#tidb_enable_noop_functions-new-in-v40)が設定されていない限りエラーを返します。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `SQL_CACHE` 、 `SQL_NO_CACHE`       | `SQL_CACHE`と`SQL_NO_CACHE`は、リクエストの結果を TiKV (RocksDB) の`BlockCache`にキャッシュするかどうかを制御するために使用されます。 `count(*)`クエリのように、大量のデータに対して一度だけクエリを実行する場合は、 `SQL_NO_CACHE` `BlockCache`に値を入力することを推奨します。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `STRAIGHT_JOIN`                    | `STRAIGHT_JOIN` 、 `FROM`句で使用されているテーブルの順序で UNION クエリを実行するようにオプティマイザを強制します。オプティマイザが適切な結合順序を選択しない場合、この構文を使用してクエリの実行速度を向上させることができます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `select_expr`                      | `select_expr`は、取得する列を示します。列名と式が含まれます。 `\*`すべての列を表します。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `FROM table_references`            | `FROM table_references`句は、行を取得するテーブル ( `select * from t;`など)、複数のテーブル ( `select * from t1 join t2;`など)、または 0 個のテーブル ( `select 1+1 from dual;`など、 `select 1+1;`と同等) を指定します。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `WHERE where_condition`            | `WHERE`句が指定されている場合、行が選択される条件を示します。結果には、その条件を満たすデータのみが含まれます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `GROUP BY`                         | `GROUP BY`ステートメントは、結果セットをグループ化するために使用されます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `HAVING where_condition`           | `HAVING`句と`WHERE`句はどちらも結果をフィルタリングするために使用されます。 `HAVING`句は`GROUP BY`の結果をフィルタリングし、 `WHERE`句は集計前に結果をフィルタリングします。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `ORDER BY`                         | `ORDER BY`句は、 `select_expr`リスト内の列、式、または項目に基づいて、データを昇順または降順に並べ替えるために使用されます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `LIMIT`                            | `LIMIT`句を使用すると、行数を制限できます。 `LIMIT`は、1 つまたは 2 つの数値引数を取ります。引数が 1 つの場合、引数は返される行の最大数を指定します。返される最初の行は、デフォルトではテーブルの最初の行です。引数が 2 つの場合、最初の引数は返される最初の行のオフセットを指定し、2 番目の引数は返される行の最大数を指定します。TiDB は、 `FETCH FIRST/NEXT n ROW/ROWS ONLY`と同じ効果を持つ`LIMIT n`構文もサポートしています。この構文では`n`を省略でき、その効果は`LIMIT 1`と同じです。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `Window window_definition`         | これはウィンドウ関数の構文であり、通常は分析計算を行うために使用されます。詳細については、 [ウィンドウ機能](/functions-and-operators/window-functions.md)を参照してください。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `FOR UPDATE`                       | `SELECT FOR UPDATE`句は、結果セット内のすべてのデータをロックして、他のトランザクションからの同時更新を検出します。クエリ条件に一致するが結果セットに存在しないデータは、読み取りロックされません。たとえば、現在のトランザクションが開始された後に他のトランザクションによって書き込まれた行データなどです。TiDB が[楽観的トランザクションモード](/optimistic-transaction.md)モードを使用する場合、ステートメント実行フェーズではトランザクションの競合は検出されません。したがって、現在のトランザクションは、PostgreSQL などの他のデータベースのように、他のトランザクションが`UPDATE` 、 `DELETE` 、または`SELECT FOR UPDATE`を実行するのをブロックしません。コミットフェーズでは、 `SELECT FOR UPDATE`によって読み取られた行は 2 つのフェーズでコミットされるため、競合検出に参加することもできます。書き込み競合が発生した場合、 `SELECT FOR UPDATE`句を含むすべてのトランザクションのコミットは失敗します。競合が検出されなかった場合、コミットは成功します。また、ロックされた行に対して新しいバージョンが生成されるため、コミットされていない他のトランザクションが後でコミットされるときに書き込み競合を検出できます。 TiDB が[悲観的なトランザクションモード](/pessimistic-transaction.md)を使用する場合、動作は基本的に他のデータベースと同じです。詳細については、 [MySQL InnoDBとの違い](/pessimistic-transaction.md#differences-from-mysql-innodb)を参照してください。 TiDB は`NOWAIT`の`FOR UPDATE`修飾子をサポートしています。詳細については[TiDB悲観的トランザクションモード](/pessimistic-transaction.md#behaviors)を参照してください。 |
| `LOCK IN SHARE MODE`               | 互換性を保証するため、TiDBはこれら3つの修飾子を解析しますが、無視します。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `TABLESAMPLE`                      | テーブルから行のサンプルを取得する。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |

> **注記：**
>
> -   バージョン 8.5.6 以降、TiDB は`FOR UPDATE OF`句でテーブル エイリアスの使用をサポートしています。下位互換性を維持するために、エイリアスが定義されている場合でもベース テーブル名を参照できますが、明示的なエイリアスの使用を推奨する警告が表示されます。クエリが異なるデータベースにまたがる同じ名前の複数のテーブル (たとえば`FROM db1.t, db2.t FOR UPDATE OF t` ) に関係する場合、TiDB は現在のデータベース コンテキストではなく、 `FROM`句の順序に基づいて、対象テーブルを左から右に照合するようになりました。曖昧さを避けるため、 `FOR UPDATE OF`句でデータベース名を指定するか、エイリアスを使用することをお勧めします。
> -   v6.6.0以降、TiDBは[リソース制御](/tidb-resource-control-ru-groups.md)サポートしています。この機能を使用すると、異なるリソースグループで異なる優先度のSQLステートメントを実行できます。これらのリソースグループに適切なクォータと優先度を設定することで、異なる優先度のSQLステートメントのスケジューリングをより適切に制御できます。リソース制御が有効になっている場合、ステートメントの優先度（ `HIGH_PRIORITY` ）は適用されなくなります。 を使用して、異なるSQLステートメントの[リソース制御](/tidb-resource-control-ru-groups.md)使用量を管理することをお勧めします。

## 例 {#examples}

### 選択 {#select}

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM t1;
+----+----+
| id | c1 |
+----+----+
|  1 |  1 |
|  2 |  2 |
|  3 |  3 |
|  4 |  4 |
|  5 |  5 |
+----+----+
5 rows in set (0.00 sec)
```

```sql
mysql> SELECT AVG(s_quantity), COUNT(s_quantity) FROM stock TABLESAMPLE REGIONS();
+-----------------+-------------------+
| AVG(s_quantity) | COUNT(s_quantity) |
+-----------------+-------------------+
|         59.5000 |                 4 |
+-----------------+-------------------+
1 row in set (0.00 sec)

mysql> SELECT AVG(s_quantity), COUNT(s_quantity) FROM stock;
+-----------------+-------------------+
| AVG(s_quantity) | COUNT(s_quantity) |
+-----------------+-------------------+
|         54.9729 |           1000000 |
+-----------------+-------------------+
1 row in set (0.52 sec)
```

上記の例では`tiup bench tpcc prepare`で生成されたデータを使用しています。最初のクエリは`TABLESAMPLE`の使用例を示しています。

### SELECT ... INTO OUTFILE {#select-into-outfile}

`SELECT ... INTO OUTFILE`ステートメントは、クエリの結果をファイルに書き込むために使用されます。

> **注記：**
>
> -   この記述はTiDB Self-Managedにのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では利用できません。
> -   このステートメントは、Amazon S3 や GCS などの[外部ストレージ](https://docs.pingcap.com/tidb/stable/backup-and-restore-storages)へのクエリ結果の書き込みをサポートしていません。

ステートメントでは、以下の句を使用して出力ファイルの形式を指定できます。

-   `FIELDS TERMINATED BY` : ファイル内のフィールド区切り文字を指定します。たとえば、 `','`と指定するとカンマ区切り値 (CSV) が出力され、 `'\t'`と指定するとタブ区切り値 (TSV) が出力されます。
-   `FIELDS ENCLOSED BY` : ファイル内の各フィールドを囲む文字を指定します。
-   `LINES TERMINATED BY` : ファイル内の行末文字を指定します。特定の文字で行を終了したい場合に使用します。

`t`テーブルがあり、以下の3つの列があると仮定します。

```sql
mysql> CREATE TABLE t (a INT, b VARCHAR(10), c DECIMAL(10,2));
Query OK, 0 rows affected (0.02 sec)

mysql> INSERT INTO t VALUES (1, 'a', 1.1), (2, 'b', 2.2), (3, 'c', 3.3);
Query OK, 3 rows affected (0.01 sec)
```

以下の例は`SELECT ... INTO OUTFILE`ステートメントを使用してクエリ結果をファイルに書き込む方法を示しています。

**例１：**

```sql
mysql> SELECT * FROM t INTO OUTFILE '/tmp/tmp_file1';
Query OK, 3 rows affected (0.00 sec)
```

この例では、 `/tmp/tmp_file1`にクエリ結果が次のように表示されます。

    1       a       1.10
    2       b       2.20
    3       c       3.30

**例２：**

```sql
mysql> SELECT * FROM t INTO OUTFILE '/tmp/tmp_file2' FIELDS TERMINATED BY ',' ENCLOSED BY '"';
Query OK, 3 rows affected (0.00 sec)
```

この例では、 `/tmp/tmp_file2`にクエリ結果が次のように表示されます。

    "1","a","1.10"
    "2","b","2.20"
    "3","c","3.30"

**例３：**

```sql
mysql> SELECT * FROM t INTO OUTFILE '/tmp/tmp_file3'
    -> FIELDS TERMINATED BY ',' ENCLOSED BY '\'' LINES TERMINATED BY '<<<\n';
Query OK, 3 rows affected (0.00 sec)
```

この例では、 `/tmp/tmp_file3`にクエリ結果が次のように表示されます。

    '1','a','1.10'<<<
    '2','b','2.20'<<<
    '3','c','3.30'<<<

## MySQLとの互換性 {#mysql-compatibility}

-   構文`SELECT ... INTO @variable`はサポートされていません。
-   構文`SELECT ... INTO DUMPFILE`はサポートされていません。
-   構文`SELECT .. GROUP BY expr`は、 MySQL 5.7のように`GROUP BY expr ORDER BY expr`を暗示しません。TiDB は代わりに MySQL 8.0 の動作に一致し、デフォルトの順序を暗示しません。
-   `SELECT ... TABLESAMPLE ...`という構文は、他のデータベースシステムや[ISO/IEC 9075-2](https://standards.iso.org/iso-iec/9075/-2/ed-6/en/)規格との互換性のために設計された TiDB 拡張機能ですが、現在 MySQL ではサポートされていません。

## 関連項目 {#see-also}

-   [入れる](/sql-statements/sql-statement-insert.md)
-   [消去](/sql-statements/sql-statement-delete.md)
-   [アップデート](/sql-statements/sql-statement-update.md)
-   [交換する](/sql-statements/sql-statement-replace.md)
