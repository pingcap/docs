---
title: TiDB Query Execution Plan Overview
summary: Learn about the execution plan information returned by the `EXPLAIN` statement in TiDB.
---

# TiDB クエリ実行計画の概要 {#tidb-query-execution-plan-overview}

> **注記：**
>
> MySQL クライアントを使用して TiDB に接続する場合、行の折り返しを行わずに出力結果をより明確に読み取るには、 `pager less -S`コマンドを使用できます。次に、 `EXPLAIN`結果が出力された後、キーボードの右矢印<kbd>→</kbd>ボタンを押して出力を水平方向にスクロールします。

SQL は宣言型言語です。ここでは、クエリの結果がどのように見えるべきかを説明します**が、実際に結果を取得する方法については説明しません**。 TiDB は、テーブルを結合する順序や潜在的なインデックスを使用できるかどうかなど、クエリを実行できるすべての方法を考慮します。*クエリ実行計画を検討する*プロセスは、SQL 最適化として知られています。

`EXPLAIN`ステートメントは、特定のステートメントに対して選択された実行プランを示します。つまり、クエリを実行する方法を何百、何千も検討した結果、TiDB は、この*プランが*リソースの消費を最小限に抑え、最短の時間で実行されると考えています。

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

`EXPLAIN`は実際のクエリを実行しません。 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)を使用してクエリを実行し、 `EXPLAIN`情報を表示できます。これは、選択した実行計画が最適ではないケースを診断する場合に役立ちます。 `EXPLAIN`その他の使用例については、次のドキュメントを参照してください。

-   [インデックス](/explain-indexes.md)
-   [テーブル結合](/explain-joins.md)
-   [サブクエリ](/explain-subqueries.md)
-   [集計](/explain-aggregation.md)
-   [ビュー](/explain-views.md)
-   [パーティション](/explain-partitions.md)

## EXPLAIN出力を理解する {#understand-explain-output}

以下に、上記の`EXPLAIN`ステートメントの出力について説明します。

-   `id` 、SQL ステートメントを実行するために必要な演算子またはサブタスクの名前を表します。詳細については[オペレーター概要](#operator-overview)参照してください。
-   `estRows` TiDB が処理すると予想される行数の推定値を示します。この数値は、アクセス方法が主キーまたは一意キーに基づいている場合など、辞書情報に基づいている場合や、CMSketch やヒストグラムなどの統計に基づいている場合があります。
-   `task`オペレーターが作業を行っている場所を示します。詳細については[タスクの概要](#task-overview)参照してください。
-   `access object`アクセスされているテーブル、パーティション、インデックスを示します。インデックスの列`a`が使用された上記の場合と同様に、インデックスの部分も表示されます。これは、複合インデックスがある場合に役立ちます。
-   `operator info`アクセスに関する追加の詳細を示します。詳細については[オペレーター情報の概要](#operator-info-overview)参照してください。

> **注記：**
>
> 返された実行プランでは、 `IndexJoin`および`Apply`演算子のすべてのプローブ側子ノードについて、v6.4.0 以降の`estRows`の意味は v6.4.0 以前とは異なります。
>
> v6.4.0 より前では、 `estRows` 、ビルド側のオペレーターからの行ごとにプローブ側のオペレーターによって処理される推定行数を意味します。 v6.4.0 以降、 `estRows`プローブ側のオペレーターによって処理される推定行の**合計数を**意味します。 `EXPLAIN ANALYZE`の結果に表示される実際の行数 ( `actRows`列で示される) は合計行数を意味するため、v6.4.0 以降、 `IndexJoin`および`Apply`演算子のプローブ側子ノードに対する`estRows`と`actRows`の意味は一貫しています。
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

### オペレーター概要 {#operator-overview}

演算子は、クエリ結果を返す一部として実行される特定のステップです。 (ディスクまたは TiKV ブロック キャッシュの) テーブル スキャンを実行するオペレーターは次のとおりです。

-   **TableFullScan** : フルテーブルスキャン
-   **TableRangeScan** : 指定された範囲でテーブルをスキャンします
-   **TableRowIDScan** : RowID に基づいてテーブル データをスキャンします。通常、インデックス読み取り操作の後に、一致するデータ行を取得します。
-   **IndexFullScan** : 「フル テーブル スキャン」と似ていますが、テーブル データではなくインデックスがスキャンされる点が異なります。
-   **IndexRangeScan** : 指定された範囲でインデックス スキャンを実行します。

TiDB は、TiKV/ TiFlashからスキャンしたデータまたは計算結果を集約します。データ集計演算子は次のカテゴリに分類できます。

-   **TableReader** : TiKV の`TableFullScan`や`TableRangeScan`の基礎となる演算子によって取得されたデータを集計します。
-   **IndexReader** : TiKV の`IndexFullScan`や`IndexRangeScan`の基礎となる演算子によって取得されたデータを集計します。
-   **IndexLookUp** : まず、 `Build`の側でスキャンされた RowID (TiKV 形式) を集計します。次に、 `Probe`側で、これらの RowID に基づいて TiKV からデータを正確に読み取ります。 `Build`の側には、 `IndexFullScan`や`IndexRangeScan`のような演算子があります。 `Probe`側には`TableRowIDScan`演算子があります。
-   **IndexMerge** : `IndexLookUp`に似ています。 `IndexMerge` `IndexLookupReader`の拡張として見ることができます。 `IndexMerge`複数のインデックスの同時読み取りがサポートされています。 `Build`がたくさんあり、 `Probe` 1 つあります。 `IndexMerge`の実行手順は`IndexLookUp`と同様である。

構造はツリーとして表示されますが、クエリの実行では、親ノードよりも前に子ノードが完了する必要は厳密にはありません。 TiDB はクエリ内並列処理をサポートしているため、実行をより正確に記述する方法は、子ノードが親ノード*に流れ込むこと*です。親、子、兄弟演算子は、クエリの一部を並行して実行する可能性*があります*。

前の例では、 `├─IndexRangeScan_8(Build)`演算子は`a(a)`インデックスに一致する行の内部`RowID`を検索します。次に、 `└─TableRowIDScan_9(Probe)`演算子はテーブルからこれらの行を取得します。

#### 範囲クエリ {#range-query}

`WHERE` / `HAVING` / `ON`条件では、TiDB オプティマイザーは主キー クエリまたはインデックス キー クエリによって返された結果を分析します。たとえば、これらの条件には`>` 、 `<` 、 `=` 、 `>=` 、 `<=`などの数値型と日付型の比較演算子や、 `LIKE`などの文字型の比較演算子が含まれる場合があります。

> **注記：**
>
> -   インデックスを使用するには、条件が*sargable*である必要があります。たとえば、条件`YEAR(date_column) < 1992`ではインデックスを使用できませんが、 `date_column < '1992-01-01`ではインデックスを使用できます。
> -   同じ種類のデータと[文字セットと照合順序](/character-set-and-collation.md)を比較することをお勧めします。型を混合すると、さらに`cast`操作が必要になったり、インデックスが使用できなくなる場合があります。
> -   `AND` (交差) と`OR` (和集合) を使用して、1 つの列の範囲クエリ条件を結合することもできます。多次元複合インデックスの場合、複数の列で条件を使用できます。たとえば、複合インデックス`(a, b, c)`に関しては次のようになります。
>     -   `a`が同等のクエリの場合、引き続き`b`のクエリ範囲を計算します。 `b`も同等のクエリである場合、引き続き`c`のクエリ範囲を計算します。
>     -   それ以外の場合、 `a`が等価でないクエリの場合は、 `a`の範囲しか把握できません。

### タスクの概要 {#task-overview}

現在、TiDB の計算タスクは、cop タスクと root タスクの 2 つのカテゴリに分類できます。 `cop[tikv]`タスクは、オペレーターが TiKV コプロセッサー内で実行されることを示します。 `root`タスクは、TiDB 内で完了することを示します。

SQL 最適化の目標の 1 つは、計算を可能な限り TiKV にプッシュすることです。 TiKV のコプロセッサーは、ほとんどの組み込み SQL関数(集計関数やスカラー関数を含む)、SQL `LIMIT`操作、インデックス スキャン、およびテーブル スキャンをサポートします。

### オペレーター情報の概要 {#operator-info-overview}

`operator info`どの条件をプッシュダウンできたかなどの有益な情報を表示できます。

-   `range: [1,1]`クエリ ( `a = 1` ) の where 句の述語が TiKV に直接プッシュされたことを示します (タスクは`cop[tikv]` )。
-   `keep order:false` 、このクエリのセマンティクスが TiKV が結果を順番に返す必要がないことを示します。順序 ( `SELECT * FROM t WHERE a = 1 ORDER BY id`など) を必要とするようにクエリが変更された場合、この条件は`keep order:true`になります。
-   `stats:pseudo` 、 `estRows`に示された推定値が正確ではない可能性があることを示します。 TiDB は、バックグラウンド操作の一部として統計を定期的に更新します。 `ANALYZE TABLE t`を実行して手動更新を実行することもできます。

演算子が異なれば、 `EXPLAIN`ステートメントの実行後に出力される情報も異なります。オプティマイザー ヒントを使用してオプティマイザーの動作を制御し、それによって物理演算子の選択を制御できます。たとえば、 `/*+ HASH_JOIN(t1, t2) */` 、オプティマイザが`Hash Join`アルゴリズムを使用することを意味します。詳細については、 [オプティマイザーのヒント](/optimizer-hints.md)を参照してください。
