---
title: EXPLAIN | TiDB SQL Statement Reference
summary: An overview of the usage of EXPLAIN for the TiDB database.
---

# <code>EXPLAIN</code> {#code-explain-code}

`EXPLAIN`ステートメントは、クエリを実行せずにクエリの実行プランを示します。クエリを実行する`EXPLAIN ANALYZE`によって補完されます。 `EXPLAIN`の出力が期待される結果と一致しない場合は、クエリ内の各テーブルで`ANALYZE TABLE`を実行することを検討してください。

ステートメント`DESC`と`DESCRIBE`は、このステートメントの別名です。 `EXPLAIN <tableName>`の代替使用法は[`SHOW [FULL] COLUMNS FROM`](/sql-statements/sql-statement-show-columns-from.md)の下に文書化されています。

TiDB は`EXPLAIN [options] FOR CONNECTION connection_id`ステートメントをサポートしています。ただし、このステートメントは MySQL の`EXPLAIN FOR`ステートメントとは異なります。詳細については、 [`EXPLAIN FOR CONNECTION`](#explain-for-connection)を参照してください。

## あらすじ {#synopsis}

```ebnf+diagram
ExplainSym ::=
    'EXPLAIN'
|   'DESCRIBE'
|   'DESC'

ExplainStmt ::=
    ExplainSym ( TableName ColumnName? | 'ANALYZE'? ExplainableStmt | 'FOR' 'CONNECTION' NUM | 'FORMAT' '=' ( stringLit | ExplainFormatType ) ( 'FOR' 'CONNECTION' NUM | ExplainableStmt ) )

ExplainableStmt ::=
    SelectStmt
|   DeleteFromStmt
|   UpdateStmt
|   InsertIntoStmt
|   ReplaceIntoStmt
|   UnionStmt
```

## <code>EXPLAIN</code>出力形式 {#code-explain-code-output-format}

> **ノート：**
>
> MySQL クライアントを使用して TiDB に接続する場合、出力結果を改行なしでより明確に読み取るには、 `pager less -S`コマンドを使用できます。次に、 `EXPLAIN`の結果が出力されたら、キーボードの右矢印<kbd>→</kbd>ボタンを押して、出力を水平方向にスクロールできます。

現在、TiDB の`EXPLAIN`は`id` 、 `estRows` 、 `task` 、 `access object` 、 `operator info`の 5 つの列を出力します。実行計画の各演算子はこれらの属性によって記述され、 `EXPLAIN`の出力の各行は演算子を記述します。各属性の説明は次のとおりです。

| 属性名         | 説明                                                                                                                                                                                                                                                                                                                         |
| :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ID          | オペレーター ID は、実行計画全体におけるオペレーターの固有 ID です。 TiDB 2.1 では、ID はオペレーターのツリー構造を表示するようにフォーマットされます。子ノードから親ノードにデータが流れます。オペレーターごとに 1 つだけの親ノード。                                                                                                                                                                                            |
| estRows     | オペレーターが出力すると予想される行数。この数は、統計とオペレーターのロジックに従って推定されます。 `estRows`は、以前のバージョンの TiDB 4.0 では`count`と呼ばれていました。                                                                                                                                                                                                                       |
| タスク         | オペレーターが属するタスクのタイプ。現在、実行計画は 2 つのタスクに分割されています。**ルート**タスクは tidb-server で実行され、 <strong>cop</strong>タスクは TiKV またはTiFlashで並行して実行されます。タスク レベルでの実行計画のトポロジは、ルート タスクの後に多数の警官タスクが続くというものです。 root タスクは、cop タスクの出力を入力として使用します。 cop タスクは、TiDB が TiKV またはTiFlashにプッシュするタスクを指します。各警官タスクは TiKV クラスターまたはTiFlashクラスターに分散され、複数のプロセスによって実行されます。 |
| アクセス オブジェクト | オペレーターがアクセスしたデータ項目情報。この情報には、 `table` 、 `partition` 、および`index` (存在する場合) が含まれます。データに直接アクセスするオペレーターだけがそのような情報を持っています。                                                                                                                                                                                                        |
| オペレーター情報    | オペレーターに関するその他の情報。各オペレーターの`operator info`は異なります。以下の例を参照できます。                                                                                                                                                                                                                                                                |

## 例 {#examples}

{{< copyable "" >}}

```sql
EXPLAIN SELECT 1;
```

```sql
+-------------------+---------+------+---------------+---------------+
| id                | estRows | task | access object | operator info |
+-------------------+---------+------+---------------+---------------+
| Projection_3      | 1.00    | root |               | 1->Column#1   |
| └─TableDual_4     | 1.00    | root |               | rows:1        |
+-------------------+---------+------+---------------+---------------+
2 rows in set (0.00 sec)
```

{{< copyable "" >}}

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
```

```sql
Query OK, 0 rows affected (0.10 sec)
```

{{< copyable "" >}}

```sql
INSERT INTO t1 (c1) VALUES (1), (2), (3);
```

```sql
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

{{< copyable "" >}}

```sql
EXPLAIN SELECT * FROM t1 WHERE id = 1;
```

```sql
+-------------+---------+------+---------------+---------------+
| id          | estRows | task | access object | operator info |
+-------------+---------+------+---------------+---------------+
| Point_Get_1 | 1.00    | root | table:t1      | handle:1      |
+-------------+---------+------+---------------+---------------+
1 row in set (0.00 sec)
```

{{< copyable "" >}}

```sql
DESC SELECT * FROM t1 WHERE id = 1;
```

```sql
+-------------+---------+------+---------------+---------------+
| id          | estRows | task | access object | operator info |
+-------------+---------+------+---------------+---------------+
| Point_Get_1 | 1.00    | root | table:t1      | handle:1      |
+-------------+---------+------+---------------+---------------+
1 row in set (0.00 sec)
```

{{< copyable "" >}}

```sql
DESCRIBE SELECT * FROM t1 WHERE id = 1;
```

```sql
+-------------+---------+------+---------------+---------------+
| id          | estRows | task | access object | operator info |
+-------------+---------+------+---------------+---------------+
| Point_Get_1 | 1.00    | root | table:t1      | handle:1      |
+-------------+---------+------+---------------+---------------+
1 row in set (0.00 sec)
```

{{< copyable "" >}}

```sql
EXPLAIN INSERT INTO t1 (c1) VALUES (4);
```

```sql
+----------+---------+------+---------------+---------------+
| id       | estRows | task | access object | operator info |
+----------+---------+------+---------------+---------------+
| Insert_1 | N/A     | root |               | N/A           |
+----------+---------+------+---------------+---------------+
1 row in set (0.00 sec)
```

{{< copyable "" >}}

```sql
EXPLAIN UPDATE t1 SET c1=5 WHERE c1=3;
```

```sql
+---------------------------+---------+-----------+---------------+--------------------------------+
| id                        | estRows | task      | access object | operator info                  |
+---------------------------+---------+-----------+---------------+--------------------------------+
| Update_4                  | N/A     | root      |               | N/A                            |
| └─TableReader_8           | 0.00    | root      |               | data:Selection_7               |
|   └─Selection_7           | 0.00    | cop[tikv] |               | eq(test.t1.c1, 3)              |
|     └─TableFullScan_6     | 3.00    | cop[tikv] | table:t1      | keep order:false, stats:pseudo |
+---------------------------+---------+-----------+---------------+--------------------------------+
4 rows in set (0.00 sec)
```

{{< copyable "" >}}

```sql
EXPLAIN DELETE FROM t1 WHERE c1=3;
```

```sql
+---------------------------+---------+-----------+---------------+--------------------------------+
| id                        | estRows | task      | access object | operator info                  |
+---------------------------+---------+-----------+---------------+--------------------------------+
| Delete_4                  | N/A     | root      |               | N/A                            |
| └─TableReader_8           | 0.00    | root      |               | data:Selection_7               |
|   └─Selection_7           | 0.00    | cop[tikv] |               | eq(test.t1.c1, 3)              |
|     └─TableFullScan_6     | 3.00    | cop[tikv] | table:t1      | keep order:false, stats:pseudo |
+---------------------------+---------+-----------+---------------+--------------------------------+
4 rows in set (0.01 sec)
```

出力の内容と形式を指定するには、 `EXPLAIN`ステートメントで`FORMAT = xxx`構文を使用できます。

`FORMAT` in `EXPLAIN`を指定しない場合、または`FORMAT = "row"`を指定する場合、 `EXPLAIN`ステートメントは結果を表形式で出力します。詳細については、 [クエリ実行計画を理解する](/explain-overview.md)参照してください。

`FORMAT = "brief"` in `EXPLAIN`を指定すると、出力のオペレーター ID は、 `FORMAT`指定しない場合に比べて単純化されます。

{{< copyable "" >}}

```sql
EXPLAIN FORMAT = "brief" DELETE FROM t1 WHERE c1 = 3;
```

```sql
+-------------------------+---------+-----------+---------------+--------------------------------+
| id                      | estRows | task      | access object | operator info                  |
+-------------------------+---------+-----------+---------------+--------------------------------+
| Delete                  | N/A     | root      |               | N/A                            |
| └─TableReader           | 0.00    | root      |               | data:Selection                 |
|   └─Selection           | 0.00    | cop[tikv] |               | eq(test.t1.c1, 3)              |
|     └─TableFullScan     | 3.00    | cop[tikv] | table:t1      | keep order:false, stats:pseudo |
+-------------------------+---------+-----------+---------------+--------------------------------+
4 rows in set (0.001 sec)
```

MySQL 標準の結果形式に加えて、TiDB は DotGraph もサポートしており、次の例のように`FORMAT = "dot"`を指定する必要があります。

{{< copyable "" >}}

```sql
create table t(a bigint, b bigint);
desc format = "dot" select A.a, B.b from t A join t B on A.a > B.b where A.a < 10;
```

```sql
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| dot contents                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|
digraph Projection_8 {
subgraph cluster8{
node [style=filled, color=lightgrey]
color=black
label = "root"
"Projection_8" -> "HashJoin_9"
"HashJoin_9" -> "TableReader_13"
"HashJoin_9" -> "Selection_14"
"Selection_14" -> "TableReader_17"
}
subgraph cluster12{
node [style=filled, color=lightgrey]
color=black
label = "cop"
"Selection_12" -> "TableFullScan_11"
}
subgraph cluster16{
node [style=filled, color=lightgrey]
color=black
label = "cop"
"Selection_16" -> "TableFullScan_15"
}
"TableReader_13" -> "Selection_12"
"TableReader_17" -> "Selection_16"
}
 |
+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

`dot`プログラム ( `graphviz`パッケージ内) がコンピューターにインストールされている場合、次の方法を使用して PNG ファイルを生成できます。

```bash
dot xx.dot -T png -O

The xx.dot is the result returned by the above statement.
```

`dot`プログラムがコンピューターにインストールされていない場合は、結果を[このウェブサイト](http://www.webgraphviz.com/)にコピーしてツリー図を取得します。

![Explain Dot](/media/explain_dot.png)

## MySQL の互換性 {#mysql-compatibility}

-   `EXPLAIN`の形式と TiDB での潜在的な実行計画の両方が、MySQL とはかなり異なります。
-   TiDB は`FORMAT=JSON`または`FORMAT=TREE`オプションをサポートしていません。

### <code>EXPLAIN FOR CONNECTION</code> {#code-explain-for-connection-code}

`EXPLAIN FOR CONNECTION` 、接続で現在実行されている SQL クエリまたは最後に実行された SQL クエリの実行計画を取得するために使用されます。出力形式は`EXPLAIN`と同じです。ただし、TiDB での`EXPLAIN FOR CONNECTION`の実装は、MySQL での実装とは異なります。それらの違い (出力形式を除く) は次のとおりです。

-   接続がスリープ状態の場合、MySQL は空の結果を返しますが、TiDB は最後に実行されたクエリ プランを返します。
-   現在のセッションの実行計画を取得しようとすると、MySQL はエラーを返しますが、TiDB は正常に結果を返します。
-   MySQL では、ログイン ユーザーがクエリ対象の接続と同じである必要があります。そうでない場合、ログイン ユーザーは**`PROCESS`**権限を持っています。一方、TiDB では、ログイン ユーザーがクエリ対象の接続と同じである必要があります。そうでない場合、ログイン ユーザーは<strong><code>SUPER</code></strong>権限を持っています。

## こちらもご覧ください {#see-also}

-   [クエリ実行プランについて](/explain-overview.md)
-   [EXPLAIN分析する](/sql-statements/sql-statement-explain-analyze.md)
-   [テーブルを分析](/sql-statements/sql-statement-analyze-table.md)
-   [痕跡](/sql-statements/sql-statement-trace.md)
