---
title: GROUP BY Modifiers
summary: TiDB GROUP BY 修飾子の使用方法を学習します。
---

# GROUP BY 修飾子 {#group-by-modifiers}

v7.4.0 以降、TiDB の`GROUP BY`句は`WITH ROLLUP`修飾子をサポートします。

`GROUP BY`節では、1 つ以上の列をグループリストとして指定し、リストの後に`WITH ROLLUP`修飾子を付加できます。すると、TiDB はグループリスト内の列に基づいて多次元降順グループ化を実行し、各グループの要約結果を出力します。

-   グループ化方法:

    -   最初のグループ化ディメンションには、グループ リスト内のすべての列が含まれます。
    -   後続のグループ化ディメンションは、グループ化リストの右端から始まり、一度に 1 列ずつ除外して新しいグループを形成します。

-   集計サマリー：クエリは各ディメンションに対して集計演算を実行し、そのディメンションの結果を以前のすべてのディメンションの結果と集計します。つまり、詳細ディメンションから全体ディメンションまで、さまざまなディメンションで集計データを取得できます。

このグループ化方法では、グループ リストに`N`列がある場合、TiDB はクエリ結果を`N+1`グループに集計します。

例えば：

```sql
SELECT count(1) FROM t GROUP BY a,b,c WITH ROLLUP;
```

この例では、TiDB は`count(1)`の計算結果を 4 つのグループ (つまり`{a, b, c}` 、 `{a, b}` 、 `{a}` 、 `{}` ) に集計し、各グループの概要結果を出力します。

> **注記：**
>
> 現在、TiDB は Cube 構文をサポートしていません。

## ユースケース {#use-cases}

複数`WITH ROLLUP`列からのデータの集計と要約は、OLAP（オンライン分析処理）シナリオでよく使用されます。1 修飾子を使用すると、集計結果に他の高レベルディメンションからのスーパーサマリー情報を表示する行を追加できます。これにより、スーパーサマリー情報を高度なデータ分析やレポート作成に活用できます。

## 前提条件 {#prerequisites}

<CustomContent platform="tidb">

v8.3.0より前のTiDBでは、 [TiFlash MPPモード](/tiflash/use-tiflash-mpp-mode.md)の`WITH ROLLUP`構文に対してのみ有効な実行プランの生成がサポートされています。そのため、TiDBクラスターにはTiFlashノードが含まれており、ターゲットテーブルには正しいTiFlashレプリカが設定されている必要があります。詳細については、 [TiFlashクラスターのスケールアウト](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

v8.3.0より前のTiDBでは、 [TiFlash MPPモード](/tiflash/use-tiflash-mpp-mode.md)の`WITH ROLLUP`構文に対してのみ有効な実行プランの生成がサポートされています。そのため、TiDBクラスターにはTiFlashノードが含まれており、ターゲットテーブルには正しいTiFlashレプリカが設定されている必要があります。詳細については、 [ノード番号を変更する](/tidb-cloud/scale-tidb-cluster.md#change-node-number)参照してください。

</CustomContent>

v8.3.0以降では、上記の制限は解除されました。TiDBクラスターにTiFlashノードが含まれているかどうかに関係なく、TiDBは`WITH ROLLUP`構文の有効な実行プランの生成をサポートします。

TiDBとTiFlashのどちらが演算子`Expand`実行するかを確認するには、実行プランで演算子`Expand`の属性`task`確認します。詳細については、 [ROLLUP実行プランの解釈方法](#how-to-interpret-the-rollup-execution-plan)参照してください。

## 例 {#examples}

`year` 、 `month` 、 `day` 、 `profit`列を持つ`bank`という名前の利益テーブルがあるとします。

```sql
CREATE TABLE bank
(
    year    INT,
    month   VARCHAR(32),
    day     INT,
    profit  DECIMAL(13, 7)
);

ALTER TABLE bank SET TIFLASH REPLICA 1; -- Add a TiFlash replica for the table in TiFlash MPP mode.

INSERT INTO bank VALUES(2000, "Jan", 1, 10.3),(2001, "Feb", 2, 22.4),(2000,"Mar", 3, 31.6)
```

銀行の年間利益を取得するには、次のように単純な`GROUP BY`節を使用できます。

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

銀行レポートでは通常、年間利益に加えて、全年度の利益全体、または詳細な利益分析のために月ごとの利益を分割して記載する必要があります。v7.4.0より前は、複数のクエリで異なる`GROUP BY`句を使用し、結果をUNIONで結合して集計結果を取得する必要がありました。v7.4.0以降では、 `GROUP BY`句に`WITH ROLLUP`修飾子を追加するだけで、単一のクエリで目的の結果を簡単に得ることができます。

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

上記の結果には、年と月の両方、年ごと、全体という異なるディメンションで集計されたデータが含まれています。結果において、 `NULL`値が存在しない行は、その行の`profit`年と月の両方をグループ化して計算されていることを示します。7 列の値が`NULL`で`month`行は、その行の`profit` 1 年間のすべての月を集計して計算されていることを示し、 `year`列の値が`NULL`である行は、その行の`profit`すべての年を集計して計算されていることを示します。

具体的には：

-   最初の行の`profit`値は 2 次元グループ`{year, month}`からのもので、細粒度`{2000, "Jan"}`グループに対する集計結果を表しています。
-   2 行目の値`profit`は 1 次元グループ`{year}`からのもので、中間レベルのグループ`{2001}`の集計結果を表しています。
-   最後の行の`profit`値は 0 次元のグループ化`{}`から取得され、全体的な集計結果を表します。

`WITH ROLLUP`結果のうち`NULL`値は、Aggregate 演算子が適用される直前に生成されます。したがって、 `SELECT` 、 `HAVING` 、 `ORDER BY`句で`NULL`値を使用して、集計結果をさらに絞り込むことができます。

たとえば、 `HAVING`句の`NULL`使用して、2 次元グループの集計結果のみをフィルタリングして表示できます。

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

`GROUP BY`の列にネイティブ`NULL`値が含まれている場合、 `WITH ROLLUP`の集計結果がクエリ結果を誤解させる可能性があることに注意してください。この問題に対処するには、 `GROUPING()`関数を使用して、ネイティブ`NULL`値と`WITH ROLLUP`によって生成された`NULL`値を区別できます。この関数はグループ化式をパラメータとして受け取り、現在の結果でグループ化式が集計されているかどうかを示す`0`または`1`返します。19 `1`集計されていることを表し、 `0`集計されていないことを表します。

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

この出力では、 `grp_year`と`grp_month`結果から行の集計ディメンションを直接把握することができ、 `year`と`month`グループ化式におけるネイティブの`NULL`値からの干渉を防ぐことができます。

`GROUPING()`関数は、最大 64 個のグループ化式をパラメータとして受け入れることができます。複数のパラメータが出力された場合、各パラメータは`0`または`1`という結果を生成し、これらのパラメータは合計で 64 ビットの`UNSIGNED LONGLONG`を形成し、各ビットは`0`または`1`となります。各パラメータのビット位置を取得するには、次の式を使用します。

```go
GROUPING(day, month, year):
  result for GROUPING(year)
+ result for GROUPING(month) << 1
+ result for GROUPING(day) << 2
```

`GROUPING()`関数で複数のパラメータを使用することで、任意の高次元で集計結果を効率的にフィルタリングできます。例えば、 `GROUPING(year, month)`使用すると、各年と全年の集計結果を素早くフィルタリングできます。

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

## ROLLUP実行プランの解釈方法 {#how-to-interpret-the-rollup-execution-plan}

多次元データ集約では、 `Expand`の演算子を用いてデータをコピーすることで、多次元グループ化のニーズに対応します。各データコピーは、特定の次元のグループ化に対応します。MPPモードでは、 `Expand`番目の演算子はデータシャッフルを容易にし、複数のノード間で大量のデータを迅速に再編成・計算することで、各ノードの計算能力を最大限に活用します。TiFlashノードのないTiFlashクラスターでは、 `Expand`演算子は単一のTiDBノードでのみ実行されるため、次元グループ化の数（ `grouping set` ）が増えるにつれてデータの冗長性が向上します。

`Expand`演算子の実装は`Projection`演算子と似ています。違いは、 `Expand`多階層の`Projection`であり、複数階層の射影演算式を含むことです。生データの各行に対して、 `Projection`演算子は結果に 1 行のみを生成しますが、 `Expand`演算子は結果に複数行を生成します（行数は射影演算式のレベル数に等しくなります）。

次の例は、 TiFlashノードのない TiDB クラスターの実行プランを示しています。3 `Expand`演算子のうちの`task` `root`であり、 `Expand`演算子が TiDB で実行されることを示しています。

```sql
EXPLAIN SELECT year, month, grouping(year), grouping(month), SUM(profit) AS profit FROM bank GROUP BY year, month WITH ROLLUP;
+--------------------------------+---------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                             | estRows | task      | access object | operator info                                                                                                                                                                                                                        |
+--------------------------------+---------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Projection_7                   | 2.40    | root      |               | Column#6->Column#12, Column#7->Column#13, grouping(gid)->Column#14, grouping(gid)->Column#15, Column#9->Column#16                                                                                                                    |
| └─HashAgg_8                    | 2.40    | root      |               | group by:Column#6, Column#7, gid, funcs:sum(test.bank.profit)->Column#9, funcs:firstrow(Column#6)->Column#6, funcs:firstrow(Column#7)->Column#7, funcs:firstrow(gid)->gid                                                            |
|   └─Expand_12                  | 3.00    | root      |               | level-projection:[test.bank.profit, <nil>->Column#6, <nil>->Column#7, 0->gid],[test.bank.profit, Column#6, <nil>->Column#7, 1->gid],[test.bank.profit, Column#6, Column#7, 3->gid]; schema: [test.bank.profit,Column#6,Column#7,gid] |
|     └─Projection_14            | 3.00    | root      |               | test.bank.profit, test.bank.year->Column#6, test.bank.month->Column#7                                                                                                                                                                |
|       └─TableReader_16         | 3.00    | root      |               | data:TableFullScan_15                                                                                                                                                                                                                |
|         └─TableFullScan_15     | 3.00    | cop[tikv] | table:bank    | keep order:false, stats:pseudo                                                                                                                                                                                                       |
+--------------------------------+---------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
6 rows in set (0.00 sec)
```

次の例は、 TiFlash MPP モードでの実行プランを示しています。3 `Expand`演算子のうち`task` `mpp[tiflash]`であり、これは`Expand`演算子がTiFlashで実行されることを示しています。

```sql
EXPLAIN SELECT year, month, grouping(year), grouping(month), SUM(profit) AS profit FROM bank GROUP BY year, month WITH ROLLUP;
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

この実行プランの例では、 `Expand_20`行目の`operator info`列目に`Expand`演算子の複数レベルの式が表示されています。これは2次元の式で構成されており、行末の`schema: [test.bank.profit, Column#6, Column#7, gid]`に`Expand`演算子のスキーマ情報が表示されています。

`Expand`演算子のスキーマ情報では、 `GID`追加列として生成されます。その値は、 `Expand`演算子によって異なる次元のグループ化ロジックに基づいて計算され、現在のデータレプリカと`grouping set`関係を反映します。ほとんどの場合、 `Expand`演算子はBit-And演算を使用し、ROLLUPのグループ化項目の組み合わせを63通り表現でき、64次元のグループ化に対応します。このモードでは、TiDBは現在のデータレプリカを複製する際に、必要な次元の`grouping set`グループ化式が含まれているかどうかに応じて`GID`値を生成し、グループ化する列の順序で64ビットのUINT64値を埋めます。

上の例では、グループ化リスト内の列の順序は`[year, month]`で、 ROLLUP 構文によって生成されるディメンショングループは`{year, month}` 、 `{year}` 、 `{}`です。ディメンショングループ`{year, month}`では、 `year`と`month`両方が必須列であるため、TiDBはそれらのビット位置にそれぞれ 1 と 1 を設定します。これにより、UINT64 の`11...0`形成され、これは10進数では 3 です。したがって、射影式は`[test.bank.profit, Column#6, Column#7, 3->gid]`となります（ `column#6` `year`に、 `column#7` `month`に対応します）。

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

クエリ内の`SELECT`節は`GROUPING`関数を使用していることに注意してください。 `GROUPING`関数が`SELECT` 、 `HAVING` 、または`ORDER BY`節で使用されている場合、TiDB は論理最適化フェーズでそれを書き換え、 `GROUPING`関数と`GROUP BY`項目の関係をディメンショングループ（ `grouping set`とも呼ばれます）のロジックに関連する`GID`に変換し、この`GID`新しい`GROUPING`関数にメタデータとして入力します。
