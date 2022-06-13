---
title: SELECT | TiDB SQL Statement Reference
summary: An overview of the usage of SELECT for the TiDB database.
---

# 選択する {#select}

`SELECT`ステートメントは、TiDBからデータを読み取るために使用されます。

## あらすじ {#synopsis}

**SelectStmt：**

![SelectStmt](/media/sqlgram/SelectStmt.png)

**FromDual：**

![FromDual](/media/sqlgram/FromDual.png)

**WhereClauseOptional：**

![WhereClauseOptional](/media/sqlgram/WhereClauseOptional.png)

**SelectStmtOpts：**

![SelectStmtOpts](/media/sqlgram/SelectStmtOpts.png)

**SelectStmtFieldList：**

![SelectStmtFieldList](/media/sqlgram/SelectStmtFieldList.png)

**TableRefsClause：**

```ebnf+diagram
TableRefsClause ::=
    TableRef AsOfClause? ( ',' TableRef AsOfClause? )*

AsOfClause ::=
    'AS' 'OF' 'TIMESTAMP' Expression
```

**WhereClauseOptional：**

![WhereClauseOptional](/media/sqlgram/WhereClauseOptional.png)

**SelectStmtGroup：**

![SelectStmtGroup](/media/sqlgram/SelectStmtGroup.png)

**HaveClause：**

![HavingClause](/media/sqlgram/HavingClause.png)

**OrderByOptional：**

![OrderByOptional](/media/sqlgram/OrderByOptional.png)

**SelectStmtLimit：**

![SelectStmtLimit](/media/sqlgram/SelectStmtLimit.png)

**FirstOrNext：**

![FirstOrNext](/media/sqlgram/FirstOrNext.png)

**FetchFirstOpt：**

![FetchFirstOpt](/media/sqlgram/FetchFirstOpt.png)

**RowOrRows：**

![RowOrRows](/media/sqlgram/RowOrRows.png)

**SelectLockOpt：**

```ebnf+diagram
SelectLockOpt ::=
    ( ( 'FOR' 'UPDATE' ( 'OF' TableList )? 'NOWAIT'? )
|   ( 'LOCK' 'IN' 'SHARE' 'MODE' ) )?

TableList ::=
    TableName ( ',' TableName )*
```

**WindowClauseOptional**

![WindowClauseOptional](/media/sqlgram/WindowClauseOptional.png)

## 構文要素の説明 {#description-of-the-syntax-elements}

| 構文要素                           | 説明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| :----------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TableOptimizerHints`          | これは、TiDBのオプティマイザの動作を制御するためのヒントです。詳細については、 [オプティマイザーのヒント](/optimizer-hints.md)を参照してください。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `ALL` `DISTINCT` `DISTINCTROW` | `ALL` `DISTINCTROW` `DISTINCT`は、重複する行を返すかどうかを指定します。 ALL（デフォルト）は、一致するすべての行を返す必要があることを指定します。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `HIGH_PRIORITY`                | `HIGH_PRIORITY`は、現在のステートメントに他のステートメントよりも高い優先順位を与えます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `SQL_CALC_FOUND_ROWS`          | TiDBはこの機能をサポートしておらず、 [`tidb_enable_noop_functions=1`](/system-variables.md#tidb_enable_noop_functions-new-in-v40)が設定されていない限りエラーを返します。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `SQL_CACHE` `SQL_NO_CACHE`     | `SQL_CACHE`と`SQL_NO_CACHE`は、リクエスト結果をTiKVの`BlockCache` （RocksDB）にキャッシュするかどうかを制御するために使用されます。 `count(*)`クエリなど、大量のデータに対する1回限りのクエリの場合、ホットユーザーデータが`BlockCache`でフラッシュされないように、 `SQL_NO_CACHE`を入力することをお勧めします。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `STRAIGHT_JOIN`                | `STRAIGHT_JOIN`は、オプティマイザに`FROM`節で使用されているテーブルの順序でユニオンクエリを実行するように強制します。オプティマイザが適切でない結合順序を選択した場合、この構文を使用してクエリの実行を高速化できます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `select_expr`                  | 各`select_expr`は、取得する列を示します。列名と式を含みます。 `\*`はすべての列を表します。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `FROM table_references`        | `FROM table_references`句は、行を取得するテーブル（ `select * from t;`など）、テーブル（ `select * from t1 join t2;`など）、または0テーブル（ `select 1+1;`に相当する`select 1+1 from dual;`など）を示します。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `WHERE where_condition`        | `WHERE`節は、指定されている場合、行が選択されるために満たす必要のある1つまたは複数の条件を示します。結果には、条件を満たすデータのみが含まれます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `GROUP BY`                     | `GROUP BY`ステートメントは、結果セットをグループ化するために使用されます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `HAVING where_condition`       | `HAVING`句と`WHERE`句はどちらも、結果をフィルタリングするために使用されます。 `HAVING`句は`GROUP BY`の結果をフィルタリングし、 `WHERE`句は集計前に結果をフィルタリングします。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `ORDER BY`                     | `ORDER BY`句は、 `select_expr`リストの列、式、または項目に基づいて、データを昇順または降順で並べ替えるために使用されます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `LIMIT`                        | `LIMIT`句を使用して、行数を制限できます。 `LIMIT`は1つまたは2つの数値引数を取ります。引数が1つの場合、引数は返される行の最大数を指定します。返される最初の行は、デフォルトではテーブルの最初の行です。 2つの引数を使用すると、最初の引数は返される最初の行のオフセットを指定し、2番目の引数は返される行の最大数を指定します。 TiDBは`FETCH FIRST/NEXT n ROW/ROWS ONLY`構文もサポートしており、 `LIMIT n`と同じ効果があります。この構文では`n`を省略でき、その効果は`LIMIT 1`と同じです。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `Window window_definition`     | これはウィンドウ関数の構文であり、通常、分析計算を行うために使用されます。詳細については、 [ウィンドウ関数](/functions-and-operators/window-functions.md)を参照してください。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `FOR UPDATE`                   | `SELECT FOR UPDATE`句は、結果セット内のすべてのデータをロックして、他のトランザクションからの同時更新を検出します。現在のトランザクションの開始後に他のトランザクションによって書き込まれた行データなど、クエリ条件に一致するが結果セットに存在しないデータは読み取りロックされません。 TiDBは[楽観的なトランザクションモデル](/optimistic-transaction.md)を使用します。トランザクションの競合は、ステートメント実行フェーズでは検出されません。したがって、現在のトランザクションは、 `SELECT FOR UPDATE` `UPDATE` `DELETE`することをブロックしません。コミットフェーズでは、 `SELECT FOR UPDATE`によって読み取られた行は、2つのフェーズでコミットされます。つまり、競合検出に参加することもできます。書き込みの競合が発生した場合、 `SELECT FOR UPDATE`句を含むすべてのトランザクションでコミットが失敗します。競合が検出されない場合、コミットは成功します。また、ロックされた行に対して新しいバージョンが生成されるため、他のコミットされていないトランザクションが後でコミットされたときに書き込みの競合を検出できます。悲観的トランザクションモードを使用する場合、動作は基本的に他のデータベースと同じです。詳細については、 [MySQLInnoDBとの違い](/pessimistic-transaction.md#difference-with-mysql-innodb)を参照してください。 TiDBは、 `FOR UPDATE`の`NOWAIT`修飾子をサポートします。詳細は[TiDB悲観的トランザクションモード](/pessimistic-transaction.md)を参照してください。 |
| `LOCK IN SHARE MODE`           | 互換性を保証するために、TiDBはこれらの3つの修飾子を解析しますが、それらを無視します。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |

## 例 {#examples}

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

## MySQLの互換性 {#mysql-compatibility}

-   構文`SELECT ... INTO @variable`はサポートされていません。
-   構文`SELECT ... GROUP BY ... WITH ROLLUP`はサポートされていません。
-   構文`SELECT .. GROUP BY expr`は、MySQL5.7のように`GROUP BY expr ORDER BY expr`を意味しません。代わりに、TiDBはMySQL 8.0の動作と一致し、デフォルトの順序を意味しません。

## も参照してください {#see-also}

-   [入れる](/sql-statements/sql-statement-insert.md)
-   [消去](/sql-statements/sql-statement-delete.md)
-   [アップデート](/sql-statements/sql-statement-update.md)
-   [交換](/sql-statements/sql-statement-replace.md)
