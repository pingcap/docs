---
title: TopN and Limit Operator Push Down
summary: Learn the implementation of TopN and Limit operator pushdown.
---

# TopNおよびLimitOperatorプッシュダウン {#topn-and-limit-operator-push-down}

このドキュメントでは、TopNおよびLimit演算子のプッシュダウンの実装について説明します。

TiDB実行プランツリーでは、SQLの`LIMIT`句はLimit演算子ノードに対応し、 `ORDER BY`句はSort演算子ノードに対応します。隣接するLimit演算子とSort演算子は、TopN演算子ノードとして結合されます。これは、特定の並べ替え規則に従って、上位N個のレコードが返されることを意味します。つまり、Limit演算子は、nullの並べ替えルールを持つTopN演算子ノードと同等です。

述語のプッシュダウンと同様に、TopNとLimitは、実行プランツリー内でデータソースにできるだけ近い位置にプッシュダウンされるため、必要なデータが早期にフィルタリングされます。このように、プッシュダウンはデータ送信と計算のオーバーヘッドを大幅に削減します。

このルールを無効にするには、 [式プッシュダウンの最適化ルールとブロックリスト](/blocklist-control-plan.md)を参照してください。

## 例 {#examples}

このセクションでは、いくつかの例を通じてTopNプッシュダウンについて説明します。

### 例1：ストレージレイヤーのコプロセッサーにプッシュダウンする {#example-1-push-down-to-the-coprocessors-in-the-storage-layer}

{{< copyable "" >}}

```sql
create table t(id int primary key, a int not null);
explain select * from t order by a limit 10;
```

```
+----------------------------+----------+-----------+---------------+--------------------------------+
| id                         | estRows  | task      | access object | operator info                  |
+----------------------------+----------+-----------+---------------+--------------------------------+
| TopN_7                     | 10.00    | root      |               | test.t.a, offset:0, count:10   |
| └─TableReader_15           | 10.00    | root      |               | data:TopN_14                   |
|   └─TopN_14                | 10.00    | cop[tikv] |               | test.t.a, offset:0, count:10   |
|     └─TableFullScan_13     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo |
+----------------------------+----------+-----------+---------------+--------------------------------+
4 rows in set (0.00 sec)
```

このクエリでは、TopNオペレーターノードがデータフィルタリングのためにTiKVにプッシュダウンされ、各コプロセッサーは10レコードのみをTiDBに返します。 TiDBがデータを集約した後、最終的なフィルタリングが実行されます。

### 例2：TopNをJoinにプッシュダウンできます（並べ替えルールは外部テーブルの列にのみ依存します） {#example-2-topn-can-be-pushed-down-into-join-the-sorting-rule-only-depends-on-the-columns-in-the-outer-table}

{{< copyable "" >}}

```sql
create table t(id int primary key, a int not null);
create table s(id int primary key, a int not null);
explain select * from t left join s on t.a = s.a order by t.a limit 10;
```

```
+----------------------------------+----------+-----------+---------------+-------------------------------------------------+
| id                               | estRows  | task      | access object | operator info                                   |
+----------------------------------+----------+-----------+---------------+-------------------------------------------------+
| TopN_12                          | 10.00    | root      |               | test.t.a, offset:0, count:10                    |
| └─HashJoin_17                    | 12.50    | root      |               | left outer join, equal:[eq(test.t.a, test.s.a)] |
|   ├─TopN_18(Build)               | 10.00    | root      |               | test.t.a, offset:0, count:10                    |
|   │ └─TableReader_26             | 10.00    | root      |               | data:TopN_25                                    |
|   │   └─TopN_25                  | 10.00    | cop[tikv] |               | test.t.a, offset:0, count:10                    |
|   │     └─TableFullScan_24       | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                  |
|   └─TableReader_30(Probe)        | 10000.00 | root      |               | data:TableFullScan_29                           |
|     └─TableFullScan_29           | 10000.00 | cop[tikv] | table:s       | keep order:false, stats:pseudo                  |
+----------------------------------+----------+-----------+---------------+-------------------------------------------------+
8 rows in set (0.01 sec)
```

このクエリでは、TopN演算子の並べ替えルールは、外側のテーブル`t`の列にのみ依存するため、TopNをJoinにプッシュダウンする前に計算を実行して、Join操作の計算コストを削減できます。さらに、TiDBはTopNをストレージレイヤーにプッシュダウンします。

### 例3：参加する前にTopNをプッシュダウンすることはできません {#example-3-topn-cannot-be-pushed-down-before-join}

{{< copyable "" >}}

```sql
create table t(id int primary key, a int not null);
create table s(id int primary key, a int not null);
explain select * from t join s on t.a = s.a order by t.id limit 10;
```

```
+-------------------------------+----------+-----------+---------------+--------------------------------------------+
| id                            | estRows  | task      | access object | operator info                              |
+-------------------------------+----------+-----------+---------------+--------------------------------------------+
| TopN_12                       | 10.00    | root      |               | test.t.id, offset:0, count:10              |
| └─HashJoin_16                 | 12500.00 | root      |               | inner join, equal:[eq(test.t.a, test.s.a)] |
|   ├─TableReader_21(Build)     | 10000.00 | root      |               | data:TableFullScan_20                      |
|   │ └─TableFullScan_20        | 10000.00 | cop[tikv] | table:s       | keep order:false, stats:pseudo             |
|   └─TableReader_19(Probe)     | 10000.00 | root      |               | data:TableFullScan_18                      |
|     └─TableFullScan_18        | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo             |
+-------------------------------+----------+-----------+---------------+--------------------------------------------+
6 rows in set (0.00 sec)
```

TopNは`Inner Join`より前にプッシュダウンすることはできません。上記のクエリを例にとると、Join後に100レコードを取得した場合、TopNの後に10レコードを残すことができます。ただし、最初にTopNを実行して10レコードを取得すると、Join後に5レコードしか残りません。このような場合、プッシュダウンの結果は異なります。

同様に、TopNは、外部結合の内部テーブルにプッシュダウンすることも、ソート規則が`t.a+s.a`などの複数のテーブルの列に関連している場合にプッシュダウンすることもできません。 TopNの並べ替えルールが外部テーブルの列のみに依存している場合にのみ、TopNをプッシュダウンできます。

### 例4：TopNを制限に変換する {#example-4-convert-topn-to-limit}

{{< copyable "" >}}

```sql
create table t(id int primary key, a int not null);
create table s(id int primary key, a int not null);
explain select * from t left join s on t.a = s.a order by t.id limit 10;
```

```
+----------------------------------+----------+-----------+---------------+-------------------------------------------------+
| id                               | estRows  | task      | access object | operator info                                   |
+----------------------------------+----------+-----------+---------------+-------------------------------------------------+
| TopN_12                          | 10.00    | root      |               | test.t.id, offset:0, count:10                   |
| └─HashJoin_17                    | 12.50    | root      |               | left outer join, equal:[eq(test.t.a, test.s.a)] |
|   ├─Limit_21(Build)              | 10.00    | root      |               | offset:0, count:10                              |
|   │ └─TableReader_31             | 10.00    | root      |               | data:Limit_30                                   |
|   │   └─Limit_30                 | 10.00    | cop[tikv] |               | offset:0, count:10                              |
|   │     └─TableFullScan_29       | 10.00    | cop[tikv] | table:t       | keep order:true, stats:pseudo                   |
|   └─TableReader_35(Probe)        | 10000.00 | root      |               | data:TableFullScan_34                           |
|     └─TableFullScan_34           | 10000.00 | cop[tikv] | table:s       | keep order:false, stats:pseudo                  |
+----------------------------------+----------+-----------+---------------+-------------------------------------------------+
8 rows in set (0.00 sec)

```

上記のクエリでは、TopNは最初に外部テーブル`t`にプッシュされます。 TopNは、主キーである`t.id`で並べ替える必要があり、TopNで追加の並べ替えを行わなくても、順番に直接読み取ることができます（ `keep order: true` ）。したがって、TopNはLimitとして簡略化されます。
