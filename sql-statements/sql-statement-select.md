---
title: SELECT | TiDB SQL Statement Reference
summary: An overview of the usage of SELECT for the TiDB database.
---

# 選択する {#select}

`SELECT`ステートメントは、TiDB からデータを読み取るために使用されます。

## あらすじ {#synopsis}

**SelectStmt:**

![SelectStmt](/media/sqlgram/SelectStmt.png)

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> `SELECT ... INTO OUTFILE`ステートメントはTiDB Cloudではサポートされていません。

</CustomContent>

**デュアルから:**

![FromDual](/media/sqlgram/FromDual.png)

**Where句オプション:**

![WhereClauseOptional](/media/sqlgram/WhereClauseOptional.png)

**SelectStmtOpts:**

![SelectStmtOpts](/media/sqlgram/SelectStmtOpts.png)

**SelectStmtFieldList:**

![SelectStmtFieldList](/media/sqlgram/SelectStmtFieldList.png)

**TableRefsClause:**

```ebnf+diagram
TableRefsClause ::=
    TableRef AsOfClause? ( ',' TableRef AsOfClause? )*

AsOfClause ::=
    'AS' 'OF' 'TIMESTAMP' Expression
```

**Where句オプション:**

![WhereClauseOptional](/media/sqlgram/WhereClauseOptional.png)

**SelectStmtGroup:**

![SelectStmtGroup](/media/sqlgram/SelectStmtGroup.png)

**有節:**

![HavingClause](/media/sqlgram/HavingClause.png)

**OrderByオプション:**

![OrderByOptional](/media/sqlgram/OrderByOptional.png)

**SelectStmtLimit:**

![SelectStmtLimit](/media/sqlgram/SelectStmtLimit.png)

**最初または次:**

![FirstOrNext](/media/sqlgram/FirstOrNext.png)

**FetchFirstOpt:**

![FetchFirstOpt](/media/sqlgram/FetchFirstOpt.png)

**行または行:**

![RowOrRows](/media/sqlgram/RowOrRows.png)

**SelectLockOpt:**

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

| 構文要素                               | 説明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| :--------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TableOptimizerHints`              | これは、TiDB のオプティマイザーの動作を制御するためのヒントです。詳細については、 [オプティマイザーのヒント](/optimizer-hints.md)を参照してください。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `ALL` 、 `DISTINCT` 、 `DISTINCTROW` | `ALL` 、 `DISTINCT` / `DISTINCTROW`修飾子は、重複する行を返すかどうかを指定します。 ALL (デフォルト) は、一致するすべての行を返すことを指定します。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `HIGH_PRIORITY`                    | `HIGH_PRIORITY`を指定すると、現在のステートメントが他のステートメントよりも優先されます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `SQL_CALC_FOUND_ROWS`              | TiDB はこの機能をサポートしていないため、 [`tidb_enable_noop_functions=1`](/system-variables.md#tidb_enable_noop_functions-new-in-v40)が設定されていないとエラーが返されます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `SQL_CACHE` 、 `SQL_NO_CACHE`       | `SQL_CACHE`と`SQL_NO_CACHE` 、リクエスト結果を TiKV (RocksDB) の`BlockCache`にキャッシュするかどうかを制御するために使用されます。 `count(*)`クエリなど、大量のデータに対する 1 回限りのクエリの場合は、ホット ユーザー データが`BlockCache`にフラッシュされないように`SQL_NO_CACHE`に入力することをお勧めします。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `STRAIGHT_JOIN`                    | `STRAIGHT_JOIN`指定すると、オプティマイザは`FROM`句で使用されるテーブルの順序でユニオン クエリを実行するようになります。オプティマイザーが不適切な結合順序を選択した場合、この構文を使用してクエリの実行を高速化できます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `select_expr`                      | それぞれの`select_expr`取得する列を示します。列名と式を含みます。 `\*`すべての列を表します。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `FROM table_references`            | `FROM table_references`句は、行を取得するテーブル ( `select * from t;`など)、テーブル ( `select * from t1 join t2;`など)、または 0 テーブル ( `select 1+1;`に相当する`select 1+1 from dual;`など) を示します。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `WHERE where_condition`            | `WHERE`節が指定されている場合、行が選択されるために満たさなければならない条件を示します。結果には、条件を満たすデータのみが含まれます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `GROUP BY`                         | `GROUP BY`ステートメントは、結果セットをグループ化するために使用されます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `HAVING where_condition`           | `HAVING`節と`WHERE`節は両方とも、結果をフィルター処理するために使用されます。 `HAVING`句は`GROUP BY`の結果をフィルター処理し、 `WHERE`句は集計前の結果をフィルター処理します。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `ORDER BY`                         | `ORDER BY`句は、 `select_expr`リストの列、式、または項目に基づいて、昇順または降順でデータを並べ替えるために使用されます。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `LIMIT`                            | `LIMIT`句を使用して、行数を制限できます。 `LIMIT` 1 つまたは 2 つの数値引数を取ります。引数を 1 つ指定すると、返される行の最大数が指定されます。返される最初の行は、デフォルトではテーブルの最初の行です。 2 つの引数がある場合、最初の引数は返す最初の行のオフセットを指定し、2 番目の引数は返す行の最大数を指定します。 TiDB は`FETCH FIRST/NEXT n ROW/ROWS ONLY`構文もサポートしており、これは`LIMIT n`と同じ効果があります。この構文では`n`を省略でき、その効果は`LIMIT 1`と同じです。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `Window window_definition`         | これはウィンドウ関数の構文で、通常は分析計算を行うために使用されます。詳細については、 [ウィンドウ関数](/functions-and-operators/window-functions.md)を参照してください。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `FOR UPDATE`                       | `SELECT FOR UPDATE`句は、結果セット内のすべてのデータをロックして、他のトランザクションからの同時更新を検出します。現在のトランザクションの開始後に他のトランザクションによって書き込まれた行データなど、クエリ条件に一致するが結果セットに存在しないデータは読み取りロックされません。 TiDB は[楽観的なトランザクションモデル](/optimistic-transaction.md)を使用します。ステートメント実行フェーズでは、トランザクションの競合は検出されません。したがって、現在のトランザクションは、PostgreSQL などの他のデータベースのように、他のトランザクションが`UPDATE` 、 `DELETE`または`SELECT FOR UPDATE`を実行することをブロックしません。コミット フェーズでは、 `SELECT FOR UPDATE`によって読み取られた行は 2 つのフェーズでコミットされます。つまり、競合検出にも参加できます。書き込みの競合が発生すると、 `SELECT FOR UPDATE`句を含むすべてのトランザクションでコミットが失敗します。競合が検出されない場合、コミットは成功します。また、ロックされた行に対して新しいバージョンが生成されるため、コミットされていない他のトランザクションが後でコミットされるときに、書き込みの競合を検出できます。悲観的トランザクション モードを使用する場合、動作は基本的に他のデータベースと同じです。詳細は[MySQL InnoDB との違い](/pessimistic-transaction.md#difference-with-mysql-innodb)をご覧ください。 TiDB は`FOR UPDATE`の`NOWAIT`修飾子をサポートしています。詳しくは[TiDB ペシミスティックトランザクションモード](/pessimistic-transaction.md)ご覧ください。 |
| `LOCK IN SHARE MODE`               | 互換性を保証するために、TiDB はこれら 3 つの修飾子を解析しますが、無視します。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |

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

## MySQL の互換性 {#mysql-compatibility}

-   構文`SELECT ... INTO @variable`はサポートされていません。
-   構文`SELECT ... GROUP BY ... WITH ROLLUP`はサポートされていません。
-   構文`SELECT .. GROUP BY expr`は、 MySQL 5.7のように`GROUP BY expr ORDER BY expr`を意味しません。代わりに、TiDB は MySQL 8.0 の動作と一致し、デフォルトの順序を意味しません。

## こちらもご覧ください {#see-also}

-   [入れる](/sql-statements/sql-statement-insert.md)
-   [消去](/sql-statements/sql-statement-delete.md)
-   [アップデート](/sql-statements/sql-statement-update.md)
-   [交換](/sql-statements/sql-statement-replace.md)
