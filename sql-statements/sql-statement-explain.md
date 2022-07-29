---
title: EXPLAIN | TiDB SQL Statement Reference
summary: An overview of the usage of EXPLAIN for the TiDB database.
---

# <code>EXPLAIN</code> {#code-explain-code}

`EXPLAIN`ステートメントは、クエリを実行せずに実行するための実行プランを示しています。クエリを実行する`EXPLAIN ANALYZE`によって補完されます。 `EXPLAIN`の出力が期待される結果と一致しない場合は、クエリの各テーブルで`ANALYZE TABLE`を実行することを検討してください。

ステートメント`DESC`と`DESCRIBE`は、このステートメントのエイリアスです。 `EXPLAIN <tableName>`の代替使用法は、 [`SHOW [FULL] COLUMNS FROM`](/sql-statements/sql-statement-show-columns-from.md)に記載されています。

TiDBは`EXPLAIN [options] FOR CONNECTION connection_id`ステートメントをサポートします。ただし、このステートメントはMySQLの`EXPLAIN FOR`ステートメントとは異なります。詳細については、 [`EXPLAIN FOR CONNECTION`](#explain-for-connection)を参照してください。

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

## <code>EXPLAIN</code>出力フォーマット {#code-explain-code-output-format}

> **ノート：**
>
> MySQLクライアントを使用してTiDBに接続する場合、行を折り返すことなく出力結果をより明確に読み取るには、 `pager less -S`コマンドを使用できます。次に、 `EXPLAIN`の結果が出力されたら、キーボードの右矢印<kbd>→</kbd>ボタンを押して、出力を水平方向にスクロールできます。

現在、 `task`の`EXPLAIN` `operator info`は`estRows`つの列を出力し`access object` ： `id` 。実行プランの各演算子はこれらの属性によって記述され、 `EXPLAIN`出力の各行は演算子を記述します。各属性の説明は次のとおりです。

| 属性名        | 説明                                                                                                                                                                                                                                                                                                         |
| :--------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| id         | オペレーターIDは、実行プラン全体におけるオペレーターの一意の識別子です。 TiDB 2.1では、IDは演算子のツリー構造を表示するようにフォーマットされています。データは子ノードから親ノードに流れます。オペレーターごとに1つだけの親ノード。                                                                                                                                                                                  |
| estRows    | オペレーターが出力すると予想される行数。この数は、統計とオペレーターのロジックに従って推定されます。 TiDB 4.0の以前のバージョンでは、 `estRows`は`count`と呼ばれていました。                                                                                                                                                                                                        |
| 仕事         | オペレーターが属するタスクのタイプ。現在、実行プランは、tidb-serverで実行される**ルート**タスクと、TiKVまたはTiFlashで並行して実行される<strong>cop</strong>タスクの2つのタスクに分割されています。タスクレベルでの実行プランのトポロジは、ルートタスクの後に多くの警官タスクが続くというものです。ルートタスクは、copタスクの出力を入力として使用します。警官タスクとは、TiDBがTiKVまたはTiFlashにプッシュダウンするタスクを指します。各警官タスクは、TiKVクラスタまたはTiFlashクラスタに分散され、複数のプロセスによって実行されます。 |
| アクセスオブジェクト | オペレーターがアクセスするデータ項目情報。情報には、 `table` 、および`partition` （存在する場合）が含まれ`index` 。データに直接アクセスするオペレーターだけがそのような情報を持っています。                                                                                                                                                                                               |
| オペレーター情報   | オペレーターに関するその他の情報。各演算子の`operator info`つは異なります。以下の例を参照してください。                                                                                                                                                                                                                                                |

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

`FORMAT`を指定しない場合、または`FORMAT = "row"`を指定する場合、 `EXPLAIN`ステートメントは結果を表形式で出力します。詳細については、 [クエリ実行プランを理解する](/explain-overview.md)を参照してください。

MySQLの標準結果形式に加えて、TiDBはDotGraphもサポートしているため、次の例のように`FORMAT = "dot"`を指定する必要があります。

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

`dot`のプログラム（ `graphviz`のパッケージに含まれる）がコンピューターにインストールされている場合は、次の方法を使用してPNGファイルを生成できます。

```bash
dot xx.dot -T png -O

The xx.dot is the result returned by the above statement.
```

`dot`のプログラムがコンピューターにインストールされていない場合は、結果を[このウェブサイト](http://www.webgraphviz.com/)にコピーして、ツリー図を取得します。

![Explain Dot](/media/explain_dot.png)

## MySQLの互換性 {#mysql-compatibility}

-   `EXPLAIN`の形式とTiDBの潜在的な実行プランはどちらも、MySQLとは実質的に異なります。
-   TiDBは`FORMAT=JSON`つまたは`FORMAT=TREE`のオプションをサポートしていません。

### <code>EXPLAIN FOR CONNECTION</code> {#code-explain-for-connection-code}

`EXPLAIN FOR CONNECTION`は、現在実行されているSQLクエリまたは接続で最後に実行されたSQLクエリの実行プランを取得するために使用されます。出力形式は`EXPLAIN`と同じです。ただし、TiDBでの`EXPLAIN FOR CONNECTION`の実装は、MySQLでの実装とは異なります。それらの違い（出力形式は別として）は次のとおりです。

-   MySQLは**実行中**のクエリプランを返し、TiDBは<strong>最後に実行された</strong>クエリプランを返します。
-   MySQLでは、ログインユーザーがクエリ対象の接続と同じである必要があります。そうでない場合、ログインユーザーは**`PROCESS`**権限を持っています。一方、TiDBでは、ログインユーザーがクエリ対象の接続と同じである必要があります。そうでない場合、ログインユーザーには<strong><code>SUPER</code></strong>権限があります。

## も参照してください {#see-also}

-   [クエリ実行プランを理解する](/explain-overview.md)
-   [EXPLAIN分析](/sql-statements/sql-statement-explain-analyze.md)
-   [テーブルの分析](/sql-statements/sql-statement-analyze-table.md)
-   [痕跡](/sql-statements/sql-statement-trace.md)
