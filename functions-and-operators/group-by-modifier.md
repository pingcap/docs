---
title: GROUP BY Modifiers
summary: Learn how to use TiDB GROUP BY modifiers.
---

# GROUP BY 修飾子 {#group-by-modifiers}

v7.4.0 以降、TiDB の`GROUP BY`句は`WITH ROLLUP`修飾子をサポートします。

`GROUP BY`句では、1 つ以上の列をグループ リストとして指定し、リストの後に`WITH ROLLUP`修飾子を追加できます。次に、TiDB は、グループ リストの列に基づいて多次元降順グループ化を実行し、出力で各グループの概要結果を提供します。

-   グループ化方法:

    -   最初のグループ化ディメンションには、グループ リスト内のすべての列が含まれます。
    -   後続のグループ化ディメンションはグループ化リストの右端から始まり、一度に 1 つ以上の列を除外して新しいグループを形成します。

-   集計概要: クエリはディメンションごとに集計操作を実行し、このディメンションの結果を以前のすべてのディメンションの結果と集計します。これは、詳細から全体まで、さまざまな次元で集計されたデータを取得できることを意味します。

このグループ化方法では、グループ リストに列が`N`ある場合、TiDB はクエリ結果を`N+1`のグループに集約します。

例えば：：

```sql
SELECT count(1) FROM t GROUP BY a,b,c WITH ROLLUP;
```

この例では、TiDB は`count(1)`の計算結果を 4 つのグループ (つまり、 `{a, b, c}` 、 `{a, b}` 、 `{a}` 、および`{}` ) に集計し、各グループの集計結果を出力します。

> **注記：**
>
> 現在、TiDB は Cube 構文をサポートしていません。

## ユースケース {#use-cases}

複数の列からのデータの集計と要約は、OLAP (オンライン分析処理) シナリオでよく使用されます。 `WITH ROLLUP`修飾子を使用すると、集計結果内の他の高レベルのディメンションからのスーパー サマリー情報を表示する追加の行を取得できます。その後、スーパー サマリー情報を使用して、高度なデータ分析とレポートの生成を行うことができます。

## 前提条件 {#prerequisites}

現在、TiDB は、 TiFlash MPP モードでのみ`WITH ROLLUP`構文の有効な実行プランの生成をサポートしています。したがって、TiDB クラスターがTiFlashノードを使用してデプロイされていること、およびターゲット ファクト テーブルがTiFlashレプリカを使用して適切に構成されていることを確認してください。

<CustomContent platform="tidb">

詳細については、 [TiFlashクラスターをスケールアウトする](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster)を参照してください。

</CustomContent>

## 例 {#examples}

`year` 、 `month` 、 `day` 、および`profit`列を含む`bank`という名前の利益テーブルがあるとします。

```sql
CREATE TABLE bank
(
    year    INT,
    month   VARCHAR(32),
    day     INT,
    profit  DECIMAL(13, 7)
);

ALTER TABLE bank SET TIFLASH REPLICA 1; -- Add a TiFlash replica for the table

INSERT INTO bank VALUES(2000, "Jan", 1, 10.3),(2001, "Feb", 2, 22.4),(2000,"Mar", 3, 31.6)
```

銀行の年間利益を取得するには、次のように単純な`GROUP BY`句を使用できます。

```sql
SELECT year, SUM(profit) AS profit FROM bank GROUP BY year;
+------+--------------------+
| year | profit             |
+------+--------------------+
| 2001 | 22.399999618530273 |
| 2000 |  41.90000057220459 |
+------+--------------------+
2 rows in set (0.15 sec)
```

銀行報告書には通常、年間利益に加えて、詳細な利益分析のために全年度の全体利益または月次分割利益も含める必要があります。 v7.4.0 より前では、複数のクエリで異なる`GROUP BY`句を使用し、UNION を使用して結果を結合して、集計された概要を取得する必要がありました。 v7.4.0 以降では、 `GROUP BY`句に`WITH ROLLUP`修飾子を追加するだけで、単一のクエリで目的の結果を簡単に得ることができます。

```sql
SELECT year, month, SUM(profit) AS profit from bank GROUP BY year, month WITH ROLLUP ORDER BY year desc, month desc;
+------+-------+--------------------+
| year | month | profit             |
+------+-------+--------------------+
| 2001 | Feb   | 22.399999618530273 |
| 2001 | NULL  | 22.399999618530273 |
| 2000 | Mar   | 31.600000381469727 |
| 2000 | Jan   | 10.300000190734863 |
| 2000 | NULL  |  41.90000057220459 |
| NULL | NULL  |  64.30000019073486 |
+------+-------+--------------------+
6 rows in set (0.025 sec)
```

前述の結果には、年と月の両方、年ごと、全体など、さまざまな次元で集計されたデータが含まれています。結果で、値`NULL`のない行は、その行の`profit`が年と月の両方をグループ化して計算されていることを示します。 `month`列の値が`NULL`行は、その行の`profit` 1 年のすべての月を集計して計算されていることを示し、 `year`列の値`NULL`の行は、その行の`profit`すべての年を集計して計算されていることを示します。

具体的には：

-   最初の行の`profit`値は 2 次元グループ`{year, month}`から取得され、きめの細かい`{2000, "Jan"}`グループの集計結果を表します。
-   2 行目の値`profit`は 1 次元グループ`{year}`から取得され、中間レベル`{2001}`グループの集計結果を表します。
-   最後の行の`profit`値は、0 次元のグループ`{}`から取得され、全体的な集計結果を表します。

`WITH ROLLUP`の結果の`NULL`値は、Aggregate 演算子が適用される直前に生成されます。したがって、 `SELECT` 、 `HAVING` 、および`ORDER BY`句で`NULL`値を使用して、集計結果をさらにフィルタリングできます。

たとえば、 `HAVING`句で`NULL`使用すると、2 次元グループのみの集計結果をフィルタリングして表示できます。

```sql
SELECT year, month, SUM(profit) AS profit FROM bank GROUP BY year, month WITH ROLLUP HAVING year IS NOT null AND month IS NOT null;
+------+-------+--------------------+
| year | month | profit             |
+------+-------+--------------------+
| 2000 | Mar   | 31.600000381469727 |
| 2000 | Jan   | 10.300000190734863 |
| 2001 | Feb   | 22.399999618530273 |
+------+-------+--------------------+
3 rows in set (0.02 sec)
```

`GROUP BY`リストの列にネイティブ`NULL`値が含まれている場合、 `WITH ROLLUP`という集計結果がクエリ結果を誤解させる可能性があることに注意してください。この問題に対処するには、 `GROUPING()`関数を使用して、ネイティブの`NULL`値と`WITH ROLLUP`によって生成された`NULL`値を区別します。この関数はグループ化式をパラメータとして受け取り、グループ化式が現在の結果に集約されているかどうかを示す`0`または`1`を返します。 `1`集約されていることを表し、 `0`集約されていないことを表します。

次の例は、 `GROUPING()`関数の使用方法を示しています。

```sql
SELECT year, month, SUM(profit) AS profit, grouping(year) as grp_year, grouping(month) as grp_month FROM bank GROUP BY year, month WITH ROLLUP ORDER BY year DESC, month DESC;
+------+-------+--------------------+----------+-----------+
| year | month | profit             | grp_year | grp_month |
+------+-------+--------------------+----------+-----------+
| 2001 | Feb   | 22.399999618530273 |        0 |         0 |
| 2001 | NULL  | 22.399999618530273 |        0 |         1 |
| 2000 | Mar   | 31.600000381469727 |        0 |         0 |
| 2000 | Jan   | 10.300000190734863 |        0 |         0 |
| 2000 | NULL  |  41.90000057220459 |        0 |         1 |
| NULL | NULL  |  64.30000019073486 |        1 |         1 |
+------+-------+--------------------+----------+-----------+
6 rows in set (0.028 sec)
```

この出力から、 `grp_year`と`grp_month`の結果から直接行の集計ディメンションを把握できます。これにより、 `year`と`month`のグループ化式のネイティブ`NULL`値による干渉が防止されます。

`GROUPING()`関数は、最大 64 個のグループ化式をパラメータとして受け入れることができます。複数のパラメーターの出力では、各パラメーターは`0`または`1`の結果を生成し、これらのパラメーターは集合的に、各ビットが`0`または`1`である 64 ビット`UNSIGNED LONGLONG`を形成します。次の式を使用して、次のように各パラメータのビット位置を取得できます。

```go
GROUPING(day, month, year):
  result for GROUPING(year)
+ result for GROUPING(month) << 1
+ result for GROUPING(day) << 2
```

`GROUPING()`関数で複数のパラメーターを使用すると、集計結果を任意の高次元で効率的にフィルターできます。たとえば、 `GROUPING(year, month)`を使用すると、各年およびすべての年の集計結果をすばやくフィルタリングできます。

```sql
SELECT year, month, SUM(profit) AS profit, grouping(year) as grp_year, grouping(month) as grp_month FROM bank GROUP BY year, month WITH ROLLUP HAVING GROUPING(year, month) <> 0 ORDER BY year DESC, month DESC;
+------+-------+--------------------+----------+-----------+
| year | month | profit             | grp_year | grp_month |
+------+-------+--------------------+----------+-----------+
| 2001 | NULL  | 22.399999618530273 |        0 |         1 |
| 2000 | NULL  |  41.90000057220459 |        0 |         1 |
| NULL | NULL  |  64.30000019073486 |        1 |         1 |
+------+-------+--------------------+----------+-----------+
3 rows in set (0.023 sec)
```

## ROLLUP 実行計画を解釈する方法 {#how-to-interpret-the-rollup-execution-plan}

多次元グループ化の要件を満たすために、多次元データ集計では`Expand`演算子を使用してデータを複製します。各レプリカは、特定の次元のグループに対応します。 MPP のデータ シャッフル機能により、オペレーターは複数のTiFlashノード間で大量のデータを迅速に再編成して計算し、各ノードの計算能力を最大限に`Expand`できます。

`Expand`演算子の実装は`Projection`演算子の実装と似ています。違いは、 `Expand`が複数レベルの射影演算式を含むマルチレベル`Projection`であることです。生データの各行について、 `Projection`演算子は結果に 1 行のみを生成しますが、 `Expand`演算子は結果に複数行を生成します (行数は射影演算式のレベル数と同じです)。

以下は実行計画の例です。

```sql
explain SELECT year, month, grouping(year), grouping(month), SUM(profit) AS profit FROM bank GROUP BY year, month WITH ROLLUP;
+----------------------------------------+---------+--------------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                                     | estRows | task         | access object | operator info                                                                                                                                                                                                                        |
+----------------------------------------+---------+--------------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| TableReader_44                         | 2.40    | root         |               | MppVersion: 2, data:ExchangeSender_43                                                                                                                                                                                                |
| └─ExchangeSender_43                    | 2.40    | mpp[tiflash] |               | ExchangeType: PassThrough                                                                                                                                                                                                            |
|   └─Projection_8                       | 2.40    | mpp[tiflash] |               | Column#6->Column#12, Column#7->Column#13, grouping(gid)->Column#14, grouping(gid)->Column#15, Column#9->Column#16                                                                                                                    |
|     └─Projection_38                    | 2.40    | mpp[tiflash] |               | Column#9, Column#6, Column#7, gid                                                                                                                                                                                                    |
|       └─HashAgg_36                     | 2.40    | mpp[tiflash] |               | group by:Column#6, Column#7, gid, funcs:sum(test.bank.profit)->Column#9, funcs:firstrow(Column#6)->Column#6, funcs:firstrow(Column#7)->Column#7, funcs:firstrow(gid)->gid, stream_count: 8                                           |
|         └─ExchangeReceiver_22          | 3.00    | mpp[tiflash] |               | stream_count: 8                                                                                                                                                                                                                      |
|           └─ExchangeSender_21          | 3.00    | mpp[tiflash] |               | ExchangeType: HashPartition, Compression: FAST, Hash Cols: [name: Column#6, collate: binary], [name: Column#7, collate: utf8mb4_bin], [name: gid, collate: binary], stream_count: 8                                                  |
|             └─Expand_20                | 3.00    | mpp[tiflash] |               | level-projection:[test.bank.profit, <nil>->Column#6, <nil>->Column#7, 0->gid],[test.bank.profit, Column#6, <nil>->Column#7, 1->gid],[test.bank.profit, Column#6, Column#7, 3->gid]; schema: [test.bank.profit,Column#6,Column#7,gid] |
|               └─Projection_16          | 3.00    | mpp[tiflash] |               | test.bank.profit, test.bank.year->Column#6, test.bank.month->Column#7                                                                                                                                                                |
|                 └─TableFullScan_17     | 3.00    | mpp[tiflash] | table:bank    | keep order:false, stats:pseudo                                                                                                                                                                                                       |
+----------------------------------------+---------+--------------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
10 rows in set (0.05 sec)
```

この実行プランの例では、 `Expand_20`行の`operator info`列にある`Expand`演算子の複数レベルの式を表示できます。これは 2 次元の式で構成されており、行の最後`schema: [test.bank.profit, Column#6, Column#7, gid]`にある`Expand`演算子のスキーマ情報を表示できます。

`Expand`演算子のスキーマ情報には、追加列として`GID`が生成されます。その値は、さまざまな次元のグループ化ロジックに基づいて`Expand`演算子によって計算され、その値は現在のデータ レプリカと`grouping set`の間の関係を反映します。ほとんどの場合、 `Expand`演算子はビット And 演算を使用します。これは、ROLLUP のグループ化項目の 63 の組み合わせを表すことができ、グループ化の 64 次元に対応します。このモードでは、TiDB は、現在のデータ レプリカがレプリケートされるときに、必要なディメンションの`grouping set`にグループ化式が含まれているかどうかに応じて`GID`値を生成し、グループ化される列の順序で 64 ビットの UINT64 値を埋めます。

前述の例では、グループ化リスト内の列の順序は`[year, month]`で、ROLLUP 構文によって生成されるディメンション グループは`{year, month}` 、 `{year}` 、および`{}`です。ディメンション グループ`{year, month}`の場合、 `year`と`month`両方とも必須の列であるため、TiDB はそれらのビット位置を対応して 1 と 1 で埋めます。これは`11...0`の UINT64 を形成します。これは 10 進数で 3 です。したがって、射影式は`[test.bank.profit, Column#6, Column#7, 3->gid]`になります ( `column#6` `year`に対応し、 `column#7` `month`に対応します)。

以下は生データの行の例です。

```sql
+------+-------+------+------------+
| year | month | day  | profit     |
+------+-------+------+------------+
| 2000 | Jan   |    1 | 10.3000000 |
+------+-------+------+------------+
```

`Expand`演算子を適用すると、次の 3 行の結果が得られます。

```sql
+------------+------+-------+-----+
| profit     | year | month | gid |
+------------+------+-------+-----+
| 10.3000000 | 2000 | Jan   |  3  |
+------------+------+-------+-----+
| 10.3000000 | 2000 | NULL  |  1  |
+------------+------+-------+-----+
| 10.3000000 | NULL | NULL  |  0  |
+------------+------+-------+-----+
```

クエリの`SELECT`句では`GROUPING`関数が使用されていることに注意してください。 `GROUPING`関数が`SELECT` 、 `HAVING` 、または`ORDER BY`句で使用されている場合、TiDB は論理最適化フェーズ中にそれを書き換え、 `GROUPING`関数と`GROUP BY`項目の間の関係を、ディメンション グループ (別名: ディメンション グループ) のロジックに関連する`GID`に変換します。 `grouping set` )、この`GID`メタデータとして新しい`GROUPING`関数に入力します。
