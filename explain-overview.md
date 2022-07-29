---
title: TiDB Query Execution Plan Overview
summary: Learn about the execution plan information returned by the `EXPLAIN` statement in TiDB.
---

# TiDBクエリ実行プランの概要 {#tidb-query-execution-plan-overview}

> **ノート：**
>
> MySQLクライアントを使用してTiDBに接続する場合、行を折り返すことなく出力結果をより明確に読み取るには、 `pager less -S`コマンドを使用できます。次に、 `EXPLAIN`の結果が出力されたら、キーボードの右矢印<kbd>→</kbd>ボタンを押して、出力を水平方向にスクロールできます。

SQLは宣言型言語です。実際にそれらの結果を取得する**方法ではなく、**クエリの結果がどのように見えるかを説明します。 TiDBは、テーブルを結合する順序の使用や、潜在的なインデックスを使用できるかどうかなど、クエリを実行できるすべての可能な方法を検討します。*クエリ実行プランを検討する*プロセスは、SQL最適化として知られています。

`EXPLAIN`ステートメントは、特定のステートメントに対して選択された実行プランを示します。つまり、クエリを実行できる数百または数千の方法を検討した後、TiDBは、この*プラン*が最小のリソースを消費し、最短の時間で実行されると考えています。

{{< copyable "" >}}

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

`EXPLAIN`は実際のクエリを実行しません。 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)を使用してクエリを実行し、 `EXPLAIN`の情報を表示できます。これは、選択した実行プランが最適ではない場合の診断に役立ちます。 `EXPLAIN`の使用例については、次のドキュメントを参照してください。

-   [インデックス](/explain-indexes.md)
-   [テーブル結合](/explain-joins.md)
-   [サブクエリ](/explain-subqueries.md)
-   [集計](/explain-aggregation.md)
-   [ビュー](/explain-views.md)
-   [パーティション](/explain-partitions.md)

## EXPLAIN出力を理解する {#understand-explain-output}

以下に、上記の`EXPLAIN`ステートメントの出力について説明します。

-   `id`は、SQLステートメントの実行に必要なオペレーターまたはサブタスクの名前を示します。詳細については、 [オペレーターの概要](#operator-overview)を参照してください。
-   `estRows`は、TiDBが処理すると予想する行数の見積もりを示しています。この数は、アクセス方法が主キーまたは一意キーに基づいている場合などのディクショナリ情報に基づいている場合もあれば、CMSketchやヒストグラムなどの統計に基づいている場合もあります。
-   `task`は、オペレーターが作業を実行している場所を示します。詳細については、 [タスクの概要](#task-overview)を参照してください。
-   `access object`は、アクセスされているテーブル、パーティション、およびインデックスを示します。インデックスの列`a`が使用された上記の場合と同様に、インデックスの部分も表示されます。これは、複合インデックスがある場合に役立ちます。
-   `operator info`は、アクセスに関する追加の詳細を示します。詳細については、 [オペレーター情報の概要](#operator-info-overview)を参照してください。

### オペレーターの概要 {#operator-overview}

演算子は、クエリ結果を返す一部として実行される特定のステップです。 （ディスクまたはTiKVブロックキャッシュの）テーブルスキャンを実行するオペレーターは、次のとおりです。

-   **TableFullScan** ：全表スキャン
-   **TableRangeScan** ：指定された範囲でのテーブルスキャン
-   **TableRowIDScan** ：RowIDに基づいてテーブルデータをスキャンします。通常、インデックス読み取り操作の後に、一致するデータ行を取得します。
-   **IndexFullScan** ：「フルテーブルスキャン」に似ていますが、テーブルデータではなくインデックスがスキャンされる点が異なります。
-   **IndexRangeScan** ：指定された範囲でのインデックススキャン。

TiDBは、TiKV/TiFlashからスキャンされたデータまたは計算結果を集約します。データ集約演算子は、次のカテゴリに分類できます。

-   **TableReader** ：TiKVの`TableFullScan`や`TableRangeScan`などの基礎となる演算子によって取得されたデータを集約します。
-   **IndexReader** ：TiKVの`IndexFullScan`や`IndexRangeScan`などの基礎となる演算子によって取得されたデータを集約します。
-   **IndexLookUp** ：最初に、 `Build`側でスキャンされたRowID（TiKV単位）を集約します。次に、 `Probe`側で、これらのRowIDに基づいてTiKVからデータを正確に読み取ります。 `Build`側には、 `IndexFullScan`や`IndexRangeScan`のような演算子があります。 `Probe`側には、 `TableRowIDScan`人のオペレーターがいます。
-   **IndexMerge** ： `IndexLookUp`に似ています。 `IndexMerge`は`IndexLookupReader`の拡張として見ることができます。 `IndexMerge`は、複数のインデックスの同時読み取りをサポートします。多くの`Build`と1つの`Probe`があります。 `IndexMerge`の実行プロセスは`IndexLookUp`の実行プロセスと同じです。

構造はツリーとして表示されますが、クエリを実行するために、親ノードの前に子ノードを完了する必要はありません。 TiDBはクエリ内並列処理をサポートしているため、実行をより正確に説明する方法は、子ノードが親ノード*に流れ込むこと*です。親、子、および兄弟の演算子は、クエリの一部を並行して実行している<em>可能</em>性があります。

前の例では、 `├─IndexRangeScan_8(Build)`演算子は、 `a(a)`インデックスに一致する行の内部`RowID`を検索します。次に、 `└─TableRowIDScan_9(Probe)`演算子は、これらの行をテーブルから取得します。

#### 範囲クエリ {#range-query}

`WHERE`条件では、 `HAVING`オプティマイザーは主`ON`またはインデックスキークエリによって返された結果を分析します。たとえば、これらの条件には、 `>`などの`>=`型と`<` `<=` 、および`=`などの文字型の比較演算子が含まれる場合があり`LIKE` 。

> **ノート：**
>
> -   インデックスを使用するには、条件が*sargable*である必要があります。たとえば、条件`YEAR(date_column) < 1992`はインデックスを使用できませんが、 `date_column < '1992-01-01`は使用できます。
> -   同じタイプと[文字セットと照合順序](/character-set-and-collation.md)のデータを比較することをお勧めします。混合タイプでは、追加の`cast`の操作が必要になるか、インデックスが使用されない場合があります。
> -   `AND` （共通部分）と`OR` （結合）を使用して、1つの列の範囲クエリ条件を組み合わせることもできます。多次元複合インデックスの場合、複数の列で条件を使用できます。たとえば、複合インデックス`(a, b, c)`について：
>     -   `a`が同等のクエリである場合は、引き続き`b`のクエリ範囲を計算します。 `b`も同等のクエリである場合は、引き続き`c`のクエリ範囲を計算します。
>     -   それ以外の場合、 `a`が同等でないクエリである場合、 `a`の範囲しか把握できません。

### タスクの概要 {#task-overview}

現在、TiDBの計算タスクは、警官タスクとルートタスクの2つのカテゴリに分類できます。 `cop[tikv]`タスクは、オペレーターがTiKVコプロセッサー内で実行されることを示します。 `root`タスクは、TiDB内で完了することを示します。

SQL最適化の目標の1つは、計算を可能な限りTiKVにプッシュダウンすることです。 TiKVのコプロセッサーは、ほとんどの組み込みSQL関数（集計関数とスカラー関数を含む）、SQL `LIMIT`演算、インデックススキャン、およびテーブルスキャンをサポートします。ただし、 `Join`の操作はすべて、TiDBのルートタスクとしてのみ実行できます。

### オペレーター情報の概要 {#operator-info-overview}

`operator info`は、どの条件をプッシュダウンできたかなどの有用な情報を表示できます。

-   `range: [1,1]`は、クエリ（ `a = 1` ）のwhere句の述語がTiKVにプッシュされたことを示します（タスクは`cop[tikv]`です）。
-   `keep order:false`は、このクエリのセマンティクスが結果を順番に返すためにTiKVを必要としなかったことを示します。注文（ `SELECT * FROM t WHERE a = 1 ORDER BY id`など）を必要とするようにクエリを変更する場合、この条件は`keep order:true`になります。
-   `stats:pseudo`は、 `estRows`に示されている推定値が正確でない可能性があることを示します。 TiDBは、バックグラウンド操作の一部として統計を定期的に更新します。手動更新は、 `ANALYZE TABLE t`を実行して実行することもできます。

`EXPLAIN`ステートメントが実行された後、演算子が異なれば出力も異なります。オプティマイザーのヒントを使用してオプティマイザーの動作を制御し、それによって物理演算子の選択を制御できます。たとえば、 `/*+ HASH_JOIN(t1, t2) */`は、オプティマイザが`Hash Join`アルゴリズムを使用することを意味します。詳細については、 [オプティマイザーのヒント](/optimizer-hints.md)を参照してください。
