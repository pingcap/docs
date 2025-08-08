---
title: SELECT | TiDB SQL Statement Reference
summary: TiDB データベースの SELECT の使用法の概要。
---

# 選択 {#select}

`SELECT`ステートメントは、TiDB からデータを読み取るために使用されます。

## 概要 {#synopsis}

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

| 構文要素                           | 説明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| :----------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TableOptimizerHints`          | これはTiDBのオプティマイザの動作を制御するためのヒントです。詳細については[オプティマイザヒント](/optimizer-hints.md)を参照してください。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `ALL` `DISTINCT` `DISTINCTROW` | `ALL`修飾子は`DISTINCTROW`重複する行を返すかどうかを指定します。ALL (デフォルト) は`DISTINCT`一致するすべての行を返すことを指定します。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `HIGH_PRIORITY`                | `HIGH_PRIORITY` 、現在のステートメントに他のステートメントよりも高い優先度を与えます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `SQL_CALC_FOUND_ROWS`          | TiDB はこの機能をサポートしていないため、 [`tidb_enable_noop_functions=1`](/system-variables.md#tidb_enable_noop_functions-new-in-v40)設定されていないとエラーが返されます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `SQL_CACHE` `SQL_NO_CACHE`     | `SQL_CACHE`と`SQL_NO_CACHE` 、リクエスト結果を TiKV (RocksDB) の`BlockCache`にキャッシュするかどうかを制御するために使用されます。6 クエリのような、大量のデータに対する`count(*)`回限りのクエリの場合は、 `BlockCache`のホットユーザーデータをフラッシュしないように、 `SQL_NO_CACHE`入力することをお勧めします。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `STRAIGHT_JOIN`                | `STRAIGHT_JOIN`指定すると、オプティマイザは`FROM`節で指定されたテーブルの順序で結合クエリを実行します。オプティマイザが不適切な結合順序を選択した場合、この構文を使用することでクエリの実行速度を向上させることができます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `select_expr`                  | `select_expr`はそれぞれ取得する列を示します。列名と式を含みます。3 `\*`すべての列を表します。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `FROM table_references`        | `FROM table_references`句は、行を取得するテーブル ( `select * from t;`など)、または複数のテーブル ( `select * from t1 join t2;`など)、あるいは 0 個のテーブル ( `select 1+1 from dual;`は`select 1+1;`に相当) を示します。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `WHERE where_condition`        | `WHERE`節が指定されている場合、行が選択するために満たさなければならない条件を示します。結果には、条件を満たすデータのみが含まれます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `GROUP BY`                     | `GROUP BY`ステートメントは結果セットをグループ化するために使用されます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `HAVING where_condition`       | `HAVING`節と`WHERE`節はどちらも結果をフィルタリングするために使用されます。5 節`HAVING` `GROUP BY`の結果をフィルタリングし、 `WHERE`節は集計前の結果をフィルタリングします。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `ORDER BY`                     | `ORDER BY`句は、 `select_expr`リスト内の列、式、または項目に基づいて、データを昇順または降順に並べ替えるために使用されます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `LIMIT`                        | `LIMIT`句は行数を制限できます。3 `LIMIT` 1つまたは2つの数値引数を取ります。引数が1つの場合、引数は返される行の最大数を指定します。返される最初の行はデフォルトでテーブルの最初の行になります。引数が2つの場合、最初の引数は返される最初の行のオフセットを指定し、2番目の引数は返される行の最大数を指定します。TiDBは、 `LIMIT n`と同じ効果を持つ`FETCH FIRST/NEXT n ROW/ROWS ONLY`構文もサポートしています。この構文では`n`省略でき、その効果は`LIMIT 1`と同じです。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `Window window_definition`     | これはウィンドウ関数の構文であり、通常は解析計算に使用されます。詳細については、 [ウィンドウ関数](/functions-and-operators/window-functions.md)を参照してください。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `FOR UPDATE`                   | `SELECT FOR UPDATE`節は、他のトランザクションからの同時更新を検出するために、結果セット内のすべてのデータをロックします。クエリ条件に一致しているが結果セットに存在しないデータは、現在のトランザクションの開始後に他のトランザクションによって書き込まれた行データなど、読み取りロックされません。 TiDB が[楽観的トランザクションモード](/optimistic-transaction.md)使用する場合、ステートメント実行フェーズではトランザクションの競合が検出されません。したがって、PostgreSQL などの他のデータベースのように、現在のトランザクションが他のトランザクションの実行を`UPDATE` 、 `DELETE` 、 `SELECT FOR UPDATE`からブロックすることはありません。コミットフェーズでは、 `SELECT FOR UPDATE`によって読み取られた行が 2 フェーズでコミットされるため、競合検出に参加することもできます。書き込み競合が発生した場合、 `SELECT FOR UPDATE`節を含むすべてのトランザクションのコミットは失敗します。競合が検出されない場合は、コミットは成功します。また、ロックされた行の新しいバージョンが生成されるため、後で他のコミットされていないトランザクションがコミットされるときに書き込み競合を検出できます。 TiDB が[悲観的トランザクションモード](/pessimistic-transaction.md)使用する場合、動作は基本的に他のデータベースと同じです。詳細については、 [MySQL InnoDBとの違い](/pessimistic-transaction.md#differences-from-mysql-innodb)を参照してください。 TiDBは`FOR UPDATE`の`NOWAIT`修飾子をサポートしています。詳細は[TiDB 悲観的トランザクションモード](/pessimistic-transaction.md#behaviors)参照してください。 |
| `LOCK IN SHARE MODE`           | 互換性を保証するために、TiDB はこれら 3 つの修飾子を解析しますが、無視します。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `TABLESAMPLE`                  | テーブルから行のサンプルを取得します。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |

> **注記：**
>
> TiDB v6.6.0以降、 [リソース管理](/tidb-resource-control-ru-groups.md)サポートします。この機能を使用すると、異なるリソースグループで異なる優先度のSQL文を実行できます。これらのリソースグループに適切なクォータと優先度を設定することで、優先度の異なるSQL文のスケジュールをより適切に制御できます。リソース制御を有効にすると、文の優先度（ `HIGH_PRIORITY` ）は無効になります。異なるSQL文のリソース使用量を管理するには、 [リソース管理](/tidb-resource-control-ru-groups.md)使用することをお勧めします。

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

上記の例では、 `tiup bench tpcc prepare`で生成されたデータを使用しています。最初のクエリは`TABLESAMPLE`の使用を示しています。

### 選択...出力ファイルへ {#select-into-outfile}

`SELECT ... INTO OUTFILE`ステートメントは、クエリの結果をファイルに書き込むために使用されます。

> **注記：**
>
> -   このステートメントは TiDB Self-Managed にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では使用できません。
> -   このステートメントは、Amazon S3 や GCS などへの[外部ストレージ](https://docs.pingcap.com/tidb/stable/backup-and-restore-storages)結果の書き込みをサポートしていません。

ステートメントでは、次の句を使用して出力ファイルの形式を指定できます。

-   `FIELDS TERMINATED BY` : ファイル内のフィールド区切り文字を指定します。例えば、カンマ区切り値 (CSV) を出力する場合は`','` 、タブ区切り値 (TSV) を出力する場合は`'\t'`指定します。
-   `FIELDS ENCLOSED BY` : ファイル内の各フィールドを囲む囲み文字を指定します。
-   `LINES TERMINATED BY` : 特定の文字で行を終了する場合に、ファイル内の行末文字を指定します。

次のような 3 つの列を持つテーブル`t`があるとします。

```sql
mysql> CREATE TABLE t (a INT, b VARCHAR(10), c DECIMAL(10,2));
Query OK, 0 rows affected (0.02 sec)

mysql> INSERT INTO t VALUES (1, 'a', 1.1), (2, 'b', 2.2), (3, 'c', 3.3);
Query OK, 3 rows affected (0.01 sec)
```

次の例は、 `SELECT ... INTO OUTFILE`ステートメントを使用してクエリ結果をファイルに書き込む方法を示しています。

**例1:**

```sql
mysql> SELECT * FROM t INTO OUTFILE '/tmp/tmp_file1';
Query OK, 3 rows affected (0.00 sec)
```

この例では、クエリ結果は次のように`/tmp/tmp_file1`で見つかります。

    1       a       1.10
    2       b       2.20
    3       c       3.30

**例2:**

```sql
mysql> SELECT * FROM t INTO OUTFILE '/tmp/tmp_file2' FIELDS TERMINATED BY ',' ENCLOSED BY '"';
Query OK, 3 rows affected (0.00 sec)
```

この例では、クエリ結果は次のように`/tmp/tmp_file2`で見つかります。

    "1","a","1.10"
    "2","b","2.20"
    "3","c","3.30"

**例3:**

```sql
mysql> SELECT * FROM t INTO OUTFILE '/tmp/tmp_file3'
    -> FIELDS TERMINATED BY ',' ENCLOSED BY '\'' LINES TERMINATED BY '<<<\n';
Query OK, 3 rows affected (0.00 sec)
```

この例では、クエリ結果は次のように`/tmp/tmp_file3`で見つかります。

    '1','a','1.10'<<<
    '2','b','2.20'<<<
    '3','c','3.30'<<<

## MySQLの互換性 {#mysql-compatibility}

-   構文`SELECT ... INTO @variable`サポートされていません。
-   構文`SELECT ... INTO DUMPFILE`サポートされていません。
-   構文`SELECT .. GROUP BY expr` 、MySQL 5.7のように`GROUP BY expr ORDER BY expr`意味するわけではありません。TiDB は MySQL 8.0 の動作と一致し、デフォルトの順序を意味しません。
-   構文`SELECT ... TABLESAMPLE ...` 、他のデータベース システムおよび[ISO/IEC 9075-2](https://standards.iso.org/iso-iec/9075/-2/ed-6/en/)標準との互換性のために設計された TiDB 拡張機能ですが、現在 MySQL ではサポートされていません。

## 参照 {#see-also}

-   [入れる](/sql-statements/sql-statement-insert.md)
-   [消去](/sql-statements/sql-statement-delete.md)
-   [アップデート](/sql-statements/sql-statement-update.md)
-   [交換する](/sql-statements/sql-statement-replace.md)
