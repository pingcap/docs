---
title: TiDB Query Execution Plan Overview
summary: TiDB の EXPLAIN` ステートメントによって返される実行プラン情報について学習します。
---

# TiDB クエリ実行プランの概要 {#tidb-query-execution-plan-overview}

> **注記：**
>
> MySQLクライアントを使用してTiDBに接続する場合、出力結果を行の折り返しなしでより明確に読み取るには、 `pager less -S`コマンドを使用します。3 `EXPLAIN`結果が出力された後、キーボードの右矢印<kbd>→</kbd>キーを押して出力を水平にスクロールします。

SQLは宣言型言語です。クエリの結果がどのようになるべきかを記述するものであり、実際に結果を取得する**方法論**を記述するものではありません。TiDBは、テーブルを結合する順序や、インデックスの使用可能性など、クエリの実行方法の可能性をすべて考慮します。*クエリ実行プランを検討する*プロセスは、SQL最適化と呼ばれます。

`EXPLAIN`文目は、特定の文に対して選択された実行プランを示します。つまり、TiDB は、クエリの実行方法を数百、数千通り検討した結果、この*プランが*最も少ないリソース消費量で、最短時間で実行されると判断します。

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

`EXPLAIN`実際のクエリを実行しません。2 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)クエリを実行し、 `EXPLAIN`情報を表示します。これは、選択された実行プランが最適ではないケースを診断するのに役立ちます。6 `EXPLAIN`使用例については、以下のドキュメントをご覧ください。

-   [インデックス](/explain-indexes.md)
-   [テーブル結合](/explain-joins.md)
-   [サブクエリ](/explain-subqueries.md)
-   [集計](/explain-aggregation.md)
-   [ビュー](/explain-views.md)
-   [パーティション](/explain-partitions.md)

## EXPLAIN出力を理解する {#understand-explain-output}

以下は、上記の`EXPLAIN`のステートメントの出力について説明しています。

-   `id` 、SQL文の実行に必要な演算子またはサブタスクの名前を表します。詳細については[オペレーターの概要](#operator-overview)参照してください。
-   `estRows` 、TiDB が処理すると予想される行数の推定値を示します。この数値は、アクセス方法が主キーまたは一意キーに基づいている場合など、辞書情報に基づく場合もあれば、CMSketch やヒストグラムなどの統計情報に基づく場合もあります。
-   `task`作業者が作業を行っている場所を示します。詳細は[タスクの概要](#task-overview)ご覧ください。
-   `access object` 、アクセスされているテーブル、パーティション、およびインデックスを示します。また、上記の例ではインデックスの列`a`が使用されているため、インデックスの各部分も表示されます。これは、複合インデックスがある場合に役立ちます。
-   `operator info`アクセスに関する追加情報を表示します。詳細については[オペレーター情報の概要](#operator-info-overview)ご覧ください。

> **注記：**
>
> 返された実行プランでは、演算子`IndexJoin`および`Apply`のすべてのプローブ側子ノードについて、v6.4.0 以降の`estRows`の意味は、v6.4.0 より前とは異なります。
>
> v6.4.0より前では、 `estRows`ビルド側オペレータからの各行に対してプローブ側オペレータが処理する推定行数を意味します。v6.4.0以降では、 `estRows`プローブ側オペレータが処理する推定行数の**合計**を意味します。結果`EXPLAIN ANALYZE`に表示される実際の行数（ `actRows`列で示される）は合計行数を意味します。そのため、v6.4.0以降、 `IndexJoin`および`Apply`オペレータのプローブ側子ノードにおける`estRows`および`actRows`の意味は一貫しています。
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

演算子とは、クエリ結果を返す際に実行される特定のステップです。テーブルスキャン（ディスクまたはTiKVブロックキャッシュ）を実行する演算子は以下のとおりです。

-   **TableFullScan** : テーブル全体のスキャン
-   **TableRangeScan** : 指定された範囲でテーブルをスキャンします
-   **TableRowIDScan** : RowIDに基づいてテーブルデータをスキャンします。通常、インデックス読み取り操作の後に、一致するデータ行を取得します。
-   **IndexFullScan** : テーブル データではなくインデックスがスキャンされる点を除いて、「フル テーブル スキャン」に似ています。
-   **IndexRangeScan** : 指定された範囲でインデックスをスキャンします。

TiDBは、TiKV/ TiFlashからスキャンされたデータまたは計算結果を集約します。データ集約演算子は以下のカテゴリに分類できます。

-   **TableReader** : TiKV の`TableFullScan`や`TableRangeScan`の基礎となる演算子によって取得されたデータを集計します。
-   **IndexReader** : TiKV の`IndexFullScan`や`IndexRangeScan`の基礎となる演算子によって取得されたデータを集計します。
-   **IndexLookUp** : まず、 `Build`側でスキャンされたRowID（TiKV内）を集計します。次に、 `Probe`側でこれらのRowIDに基づいてTiKVからデータを正確に読み取ります。6 `Build`には`IndexFullScan`や`IndexRangeScan`などの演算子があり、 `Probe`側には`TableRowIDScan`演算子があります。
-   **IndexMerge** : `IndexLookUp`と同様です。4 `IndexMerge` `IndexLookupReader`の拡張と見なすことができます。8 `IndexMerge`複数のインデックスの同時読み取りをサポートします。10 は`Build`あり、 `Probe`は1つです。14 の実行プロセスは`IndexMerge` `IndexLookUp`同じです。

構造はツリー構造のように見えますが、クエリの実行において子ノードが親ノードより先に完了している必要は必ずしもありません。TiDBはクエリ内並列処理をサポートしているため、より正確な表現は、子ノードが親ノード*に流れ込む*というものです。親ノード、子ノード、兄弟ノードの演算子によって、クエリの一部が並列実行される可能性*があります*。

前の例では、演算子`├─IndexRangeScan_8(Build)`はインデックス`a(a)`に一致する行の内部`RowID`検索します。次に、演算子`└─TableRowIDScan_9(Probe)`これらの行をテーブルから取得します。

#### 範囲クエリ {#range-query}

`WHERE` / `HAVING` / `ON`の条件では、TiDB オプティマイザは主キークエリまたはインデックスキークエリによって返された結果を分析します。例えば、これらの条件には、 `>` 、 `<` 、 `=` 、 `>=` 、 `<=`などの数値型と日付型の比較演算子や、 `LIKE`などの文字型の比較演算子が含まれる場合があります。

> **注記：**
>
> -   インデックスを使用するには、条件が*検索引数*可能でなければなりません。例えば、条件`YEAR(date_column) < 1992`インデックスを使用できませんが、 `date_column < '1992-01-01`では使用できます。
> -   同じタイプのデータと[文字セットと照合順序](/character-set-and-collation.md)比較することをお勧めします。タイプが混在すると、追加の`cast`操作が必要になるか、インデックスが使用できなくなる可能性があります。
> -   `AND` （積集合）と`OR` （和集合）を使用して、1つの列の範囲クエリ条件を組み合わせることもできます。多次元複合インデックスの場合は、複数の列で条件を使用できます。例えば、複合インデックス`(a, b, c)`場合：
>     -   `a`同等のクエリである場合は、 `b`のクエリ範囲を計算し続けます。 `b`同等のクエリである場合は、 `c`のクエリ範囲を計算し続けます。
>     -   それ以外の場合、 `a`同等でないクエリであれば、 `a`範囲しか把握できません。

### タスクの概要 {#task-overview}

現在、TiDBの計算タスクは、copタスクとルートタスクの2つのカテゴリに分類できます。タスク番号`cop[tikv]`場合、演算子はTiKVコプロセッサ内で実行されます。タスク番号が`root`場合、演算子はTiDB内で完了します。

SQL最適化の目標の一つは、計算を可能な限りTiKVに委ねることです。TiKVのコプロセッサーは、組み込みSQL関数（集計関数とスカラー関数を含む）、SQL `LIMIT`演算、インデックススキャン、テーブルスキャンのほとんどをサポートしています。

### オペレーター情報の概要 {#operator-info-overview}

`operator info` 、どの条件をプッシュダウンできたかなどの有用な情報を表示できます。

-   `range: [1,1]` 、クエリのwhere句の述語（ `a = 1` ）がTiKV（タスクは`cop[tikv]` ）にプッシュダウンされたことを示しています。
-   `keep order:false` 、このクエリのセマンティクスでは TiKV が結果を順番に返す必要がないことを示しています。クエリが順序付けを必要とするように変更された場合（例えば`SELECT * FROM t WHERE a = 1 ORDER BY id` ）、この条件は`keep order:true`になります。
-   `stats:pseudo` 、 `estRows`に示されている推定値が正確ではない可能性があることを示しています。TiDB はバックグラウンド処理の一環として定期的に統計を更新します。4 `ANALYZE TABLE t`実行して手動で更新することもできます。

`EXPLAIN`文の実行後、異なる演算子は異なる情報を出力します。オプティマイザヒントを使用してオプティマイザの動作を制御し、それによって物理演算子の選択を制御できます。例えば、 `/*+ HASH_JOIN(t1, t2) */`オプティマイザが`Hash Join`アルゴリズムを使用することを意味します。詳細については、 [オプティマイザヒント](/optimizer-hints.md)参照してください。
