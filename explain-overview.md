---
title: TiDB Query Execution Plan Overview
summary: TiDB の EXPLAIN` ステートメントによって返される実行プラン情報について学習します。
---

# TiDB クエリ実行プランの概要 {#tidb-query-execution-plan-overview}

> **注記：**
>
> MySQL クライアントを使用して TiDB に接続する場合、出力結果を行の折り返しなしでより明確に読み取るには、 `pager less -S`コマンドを使用します。次に、 `EXPLAIN`結果が出力された後、キーボードの右矢印<kbd>→</kbd>ボタンを押して、出力を水平にスクロールします。

SQL は宣言型言語です。クエリの結果がどのようになるかを表すものであり、実際にその結果を取得する**方法を表すものではありません**。TiDB は、テーブルを結合する順序や、潜在的なインデックスを使用できるかどうかなど、クエリを実行する可能性のあるすべての方法を考慮します。*クエリ実行プランを検討する*プロセスは、SQL 最適化と呼ばれます。

`EXPLAIN`文は、特定の文に対して選択された実行プランを示します。つまり、クエリを実行するための何百、何千もの方法を検討した後、TiDB はこの*プランが*最も少ないリソースを消費し、最短時間で実行されると判断します。

```sql
CREATE TABLE t (id INT NOT NULL PRIMARY KEY auto_increment, a INT NOT NULL, pad1 VARCHAR(255), INDEX(a));
INSERT INTO t VALUES (1, 1, 'aaa'),(2,2, 'bbb');
EXPLAIN SELECT * FROM t WHERE a = 1;
```

```sql
Query OK, 0 rows affected (0.96 sec)

Query OK, 2 rows affected (0.02 sec)
Records: 2  Duplicates: 0  Warnings: 0

+-------------------------------+---------+-----------+---------------------+---------------------------------------------+
| id                            | estRows | task      | access object       | operator info                               |
+-------------------------------+---------+-----------+---------------------+---------------------------------------------+
| IndexLookUp_10                | 10.00   | root      |                     |                                             |
| ├─IndexRangeScan_8(Build)     | 10.00   | cop[tikv] | table:t, index:a(a) | range:[1,1], keep order:false, stats:pseudo |
| └─TableRowIDScan_9(Probe)     | 10.00   | cop[tikv] | table:t             | keep order:false, stats:pseudo              |
+-------------------------------+---------+-----------+---------------------+---------------------------------------------+
3 rows in set (0.00 sec)
```

`EXPLAIN`実際のクエリを実行しません。 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)クエリを実行し、 `EXPLAIN`情報を表示するために使用できます。これは、選択された実行プランが最適ではない場合の診断に役立ちます。 `EXPLAIN`使用例の詳細については、次のドキュメントを参照してください。

-   [インデックス](/explain-indexes.md)
-   [テーブル結合](/explain-joins.md)
-   [サブクエリ](/explain-subqueries.md)
-   [集計](/explain-aggregation.md)
-   [ビュー](/explain-views.md)
-   [パーティション](/explain-partitions.md)

## EXPLAIN出力を理解する {#understand-explain-output}

以下は、上記の`EXPLAIN`ステートメントの出力を説明しています。

-   `id` 、SQL ステートメントを実行するために必要な演算子またはサブタスクの名前を示します。詳細については[オペレーターの概要](#operator-overview)参照してください。
-   `estRows` TiDB が処理すると予想される行数の推定値を示します。この数値は、アクセス方法が主キーまたは一意のキーに基づいている場合などの辞書情報に基づく場合もあれば、CMSketch やヒストグラムなどの統計に基づく場合もあります。
-   `task`オペレーターが作業を行っている場所を示します。詳細については[タスクの概要](#task-overview)参照してください。
-   `access object`アクセスされているテーブル、パーティション、およびインデックスを示します。インデックスの列`a`が使用された上記のケースのように、インデックスの各部分も表示されます。これは、複合インデックスがある場合に役立ちます。
-   `operator info`アクセスに関する追加の詳細を表示します。詳細については[オペレーター情報の概要](#operator-info-overview)参照してください。

> **注記：**
>
> 返された実行プランでは、 `IndexJoin`および`Apply`演算子のすべてのプローブ側子ノードについて、v6.4.0 以降の`estRows`の意味は、v6.4.0 より前とは異なります。
>
> v6.4.0 より前では、 `estRows`ビルド側オペレータからの各行に対してプローブ側オペレータによって処理される推定行数を意味します。v6.4.0 以降では、 `estRows`プローブ側オペレータによって処理される推定行数の**合計**を意味します。結果`EXPLAIN ANALYZE`に表示される実際の行数 ( `actRows`列で示される) は合計行数を意味するため、v6.4.0 以降では、 `IndexJoin`および`Apply`オペレータのプローブ側子ノードの`estRows`および`actRows`の意味は一貫しています。
>
> 例えば：
>
> ```sql
> CREATE TABLE t1(a INT, b INT);
> CREATE TABLE t2(a INT, b INT, INDEX ia(a));
> EXPLAIN SELECT /*+ INL_JOIN(t2) */ * FROM t1 JOIN t2 ON t1.a = t2.a;
> EXPLAIN SELECT (SELECT a FROM t2 WHERE t2.a = t1.b LIMIT 1) FROM t1;
> ```
>
> ```sql
> -- Before v6.4.0:
> +---------------------------------+----------+-----------+-----------------------+-----------------------------------------------------------------------------------------------------------------+
> | id                              | estRows  | task      | access object         | operator info                                                                                                   |
> +---------------------------------+----------+-----------+-----------------------+-----------------------------------------------------------------------------------------------------------------+
> | IndexJoin_12                    | 12487.50 | root      |                       | inner join, inner:IndexLookUp_11, outer key:test.t1.a, inner key:test.t2.a, equal cond:eq(test.t1.a, test.t2.a) |
> | ├─TableReader_24(Build)         | 9990.00  | root      |                       | data:Selection_23                                                                                               |
> | │ └─Selection_23                | 9990.00  | cop[tikv] |                       | not(isnull(test.t1.a))                                                                                          |
> | │   └─TableFullScan_22          | 10000.00 | cop[tikv] | table:t1              | keep order:false, stats:pseudo                                                                                  |
> | └─IndexLookUp_11(Probe)         | 1.25     | root      |                       |                                                                                                                 |
> |   ├─Selection_10(Build)         | 1.25     | cop[tikv] |                       | not(isnull(test.t2.a))                                                                                          |
> |   │ └─IndexRangeScan_8          | 1.25     | cop[tikv] | table:t2, index:ia(a) | range: decided by [eq(test.t2.a, test.t1.a)], keep order:false, stats:pseudo                                    |
> |   └─TableRowIDScan_9(Probe)     | 1.25     | cop[tikv] | table:t2              | keep order:false, stats:pseudo                                                                                  |
> +---------------------------------+----------+-----------+-----------------------+-----------------------------------------------------------------------------------------------------------------+
> +---------------------------------+----------+-----------+-----------------------+------------------------------------------------------------------------------+
> | id                              | estRows  | task      | access object         | operator info                                                                |
> +---------------------------------+----------+-----------+-----------------------+------------------------------------------------------------------------------+
> | Projection_12                   | 10000.00 | root      |                       | test.t2.a                                                                    |
> | └─Apply_14                      | 10000.00 | root      |                       | CARTESIAN left outer join                                                    |
> |   ├─TableReader_16(Build)       | 10000.00 | root      |                       | data:TableFullScan_15                                                        |
> |   │ └─TableFullScan_15          | 10000.00 | cop[tikv] | table:t1              | keep order:false, stats:pseudo                                               |
> |   └─Limit_17(Probe)             | 1.00     | root      |                       | offset:0, count:1                                                            |
> |     └─IndexReader_21            | 1.00     | root      |                       | index:Limit_20                                                               |
> |       └─Limit_20                | 1.00     | cop[tikv] |                       | offset:0, count:1                                                            |
> |         └─IndexRangeScan_19     | 1.00     | cop[tikv] | table:t2, index:ia(a) | range: decided by [eq(test.t2.a, test.t1.b)], keep order:false, stats:pseudo |
> +---------------------------------+----------+-----------+-----------------------+------------------------------------------------------------------------------+
>
> -- Since v6.4.0:
>
> -- You can find that the `estRows` column values for `IndexLookUp_11`, `Selection_10`, `IndexRangeScan_8`, and `TableRowIDScan_9` since v6.4.0 are different from that before v6.4.0.
> +---------------------------------+----------+-----------+-----------------------+-----------------------------------------------------------------------------------------------------------------+
> | id                              | estRows  | task      | access object         | operator info                                                                                                   |
> +---------------------------------+----------+-----------+-----------------------+-----------------------------------------------------------------------------------------------------------------+
> | IndexJoin_12                    | 12487.50 | root      |                       | inner join, inner:IndexLookUp_11, outer key:test.t1.a, inner key:test.t2.a, equal cond:eq(test.t1.a, test.t2.a) |
> | ├─TableReader_24(Build)         | 9990.00  | root      |                       | data:Selection_23                                                                                               |
> | │ └─Selection_23                | 9990.00  | cop[tikv] |                       | not(isnull(test.t1.a))                                                                                          |
> | │   └─TableFullScan_22          | 10000.00 | cop[tikv] | table:t1              | keep order:false, stats:pseudo                                                                                  |
> | └─IndexLookUp_11(Probe)         | 12487.50 | root      |                       |                                                                                                                 |
> |   ├─Selection_10(Build)         | 12487.50 | cop[tikv] |                       | not(isnull(test.t2.a))                                                                                          |
> |   │ └─IndexRangeScan_8          | 12500.00 | cop[tikv] | table:t2, index:ia(a) | range: decided by [eq(test.t2.a, test.t1.a)], keep order:false, stats:pseudo                                    |
> |   └─TableRowIDScan_9(Probe)     | 12487.50 | cop[tikv] | table:t2              | keep order:false, stats:pseudo                                                                                  |
> +---------------------------------+----------+-----------+-----------------------+-----------------------------------------------------------------------------------------------------------------+
>
> -- You can find that the `estRows` column values for `Limit_17`, `IndexReader_21`, `Limit_20`, and `IndexRangeScan_19` since v6.4.0 are different from that before v6.4.0.
> +---------------------------------+----------+-----------+-----------------------+------------------------------------------------------------------------------+
> | id                              | estRows  | task      | access object         | operator info                                                                |
> +---------------------------------+----------+-----------+-----------------------+------------------------------------------------------------------------------+
> | Projection_12                   | 10000.00 | root      |                       | test.t2.a                                                                    |
> | └─Apply_14                      | 10000.00 | root      |                       | CARTESIAN left outer join                                                    |
> |   ├─TableReader_16(Build)       | 10000.00 | root      |                       | data:TableFullScan_15                                                        |
> |   │ └─TableFullScan_15          | 10000.00 | cop[tikv] | table:t1              | keep order:false, stats:pseudo                                               |
> |   └─Limit_17(Probe)             | 10000.00 | root      |                       | offset:0, count:1                                                            |
> |     └─IndexReader_21            | 10000.00 | root      |                       | index:Limit_20                                                               |
> |       └─Limit_20                | 10000.00 | cop[tikv] |                       | offset:0, count:1                                                            |
> |         └─IndexRangeScan_19     | 10000.00 | cop[tikv] | table:t2, index:ia(a) | range: decided by [eq(test.t2.a, test.t1.b)], keep order:false, stats:pseudo |
> +---------------------------------+----------+-----------+-----------------------+------------------------------------------------------------------------------+
> ```

### オペレーターの概要 {#operator-overview}

演算子は、クエリ結果を返す際に実行される特定のステップです。テーブル スキャン (ディスクまたは TiKV ブロック キャッシュ) を実行する演算子は次のとおりです。

-   **TableFullScan** : テーブル全体のスキャン
-   **TableRangeScan** : 指定された範囲でテーブルをスキャンします
-   **TableRowIDScan** : RowID に基づいてテーブル データをスキャンします。通常は、インデックス読み取り操作の後に、一致するデータ行を取得します。
-   **IndexFullScan** : テーブル データではなくインデックスがスキャンされる点を除いて、「フル テーブル スキャン」に似ています。
-   **IndexRangeScan** : 指定された範囲でインデックスをスキャンします。

TiDB は、 TiKV/ TiFlashからスキャンされたデータまたは計算結果を集約します。データ集約演算子は、次のカテゴリに分類できます。

-   **TableReader** : TiKV の`TableFullScan`や`TableRangeScan`などの基礎となる演算子によって取得されたデータを集計します。
-   **IndexReader** : TiKV の`IndexFullScan`や`IndexRangeScan`などの基礎となる演算子によって取得されたデータを集計します。
-   **IndexLookUp** : まず、 `Build`側でスキャンされた RowID (TiKV 内) を集計します。次に、 `Probe`側で、これらの RowID に基づいて TiKV からデータを正確に読み取ります。6 `Build`には、 `IndexFullScan`や`IndexRangeScan`などの演算子があり、 `Probe`側には、 `TableRowIDScan`演算子があります。
-   **IndexMerge** : `IndexLookUp`と似ています`IndexMerge` `IndexLookupReader`の拡張と見ることができます。8 `IndexMerge`複数のインデックスを同時に読み取ることをサポートしています。10 が`Build`あり、 `Probe` 1 つあります`IndexMerge`の実行プロセスは`IndexLookUp`と同じです。

構造はツリーとして表示されますが、クエリを実行する際に、子ノードが親ノードの前に完了する必要は厳密にはありません。TiDB はクエリ内並列処理をサポートしているため、実行をより正確に説明するには、子ノードが親ノード*に流れ込むとします*。親、子、兄弟演算子は、クエリの一部を並列で実行する可能性が*あります*。

前の例では、 `├─IndexRangeScan_8(Build)`演算子は`a(a)`インデックスに一致する行の内部`RowID`検索します。次に、 `└─TableRowIDScan_9(Probe)`演算子はテーブルからこれらの行を取得します。

#### 範囲クエリ {#range-query}

`WHERE` / `HAVING` / `ON`条件では、TiDB オプティマイザは主キー クエリまたはインデックス キー クエリによって返された結果を分析します。たとえば、これらの条件には、 `>` 、 `<` 、 `=` 、 `>=` 、 `<=`などの数値型と日付型の比較演算子や、 `LIKE`などの文字型の比較演算子が含まれる場合があります。

> **注記：**
>
> -   インデックスを使用するには、条件が*検索引数*可能でなければなりません。たとえば、条件`YEAR(date_column) < 1992`インデックスを使用できませんが、 `date_column < '1992-01-01`では使用できます。
> -   同じタイプのデータと[文字セットと照合順序](/character-set-and-collation.md)比較することをお勧めします。タイプを混在させると、追加の`cast`操作が必要になるか、インデックスが使用できなくなる可能性があります。
> -   `AND` (交差) と`OR` (結合) を使用して、1 つの列の範囲クエリ条件を組み合わせることもできます。多次元複合インデックスの場合は、複数の列で条件を使用できます。たとえば、複合インデックス`(a, b, c)`について:
>     -   `a`同等のクエリである場合は、 `b`のクエリ範囲を計算し続けます。 `b`も同等のクエリである場合は、 `c`のクエリ範囲を計算し続けます。
>     -   それ以外の場合、 `a`が同等でないクエリの場合は、 `a`の範囲しか把握できません。

### タスクの概要 {#task-overview}

現在、TiDB の計算タスクは、cop タスクとルート タスクの`cop[tikv]`つのカテゴリに分けられます。1 タスクは、演算子が TiKV コプロセッサ内で実行されることを示します。3 `root`は、TiDB 内で完了することを示します。

SQL 最適化の目標の 1 つは、計算を可能な限り TiKV に押し下げることです。TiKV のコプロセッサーは、組み込み SQL関数(集計関数とスカラー関数を含む)、SQL `LIMIT`操作、インデックス スキャン、およびテーブル スキャンのほとんどをサポートします。

### オペレーター情報の概要 {#operator-info-overview}

`operator info`は、どの条件をプッシュダウンできたかなどの有用な情報を表示できます。

-   `range: [1,1]`クエリ（ `a = 1` ）のwhere句の述語がTiKV（タスクは`cop[tikv]` ）にプッシュダウンされたことを示しています。
-   `keep order:false`このクエリのセマンティクスでは、TiKV が結果を順番に返す必要がないことを示しています。クエリが順序を要求するように変更された場合 ( `SELECT * FROM t WHERE a = 1 ORDER BY id`など)、この条件は`keep order:true`になります。
-   `stats:pseudo` 、 `estRows`に示されている推定値が正確ではない可能性があることを示しています。TiDB は、バックグラウンド操作の一環として定期的に統計を更新します。4 `ANALYZE TABLE t`実行して手動で更新することもできます。

`EXPLAIN`文が実行された後、異なる演算子は異なる情報を出力します。オプティマイザ ヒントを使用してオプティマイザの動作を制御し、それによって物理演算子の選択を制御できます。たとえば、 `/*+ HASH_JOIN(t1, t2) */`オプティマイザが`Hash Join`アルゴリズムを使用することを意味します。詳細については、 [オプティマイザーのヒント](/optimizer-hints.md)参照してください。
