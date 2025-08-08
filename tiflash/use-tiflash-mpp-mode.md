---
title: Use TiFlash MPP Mode
summary: TiFlashの MPP モードとその使用方法を学びます。
---

# TiFlash MPPモードを使用する {#use-tiflash-mpp-mode}

<CustomContent platform="tidb">

このドキュメントでは、 TiFlashの[超並列処理（MPP）](/glossary.md#massively-parallel-processing-mpp)モードとその使用方法を紹介します。

</CustomContent>

<CustomContent platform="tidb-cloud">

このドキュメントでは、 TiFlashの[超並列処理（MPP）](/tidb-cloud/tidb-cloud-glossary.md#mpp)モードとその使用方法を紹介します。

</CustomContent>

TiFlashは、クエリ実行にMPPモードをサポートしています。このモードでは、ノード間のデータ交換（データシャッフルプロセス）が計算に導入されます。TiDBは、オプティマイザのコスト推定に基づいて、MPPモードを選択するかどうかを自動的に決定します。1と[`tidb_allow_mpp`](/system-variables.md#tidb_allow_mpp-new-in-v50) [`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51)値を変更することで、選択戦略を変更できます。

次の図は、MPP モードの動作を示しています。

![mpp-mode](/media/tiflash/tiflash-mpp.png)

## MPPモードを選択するかどうかを制御します {#control-whether-to-select-the-mpp-mode}

変数`tidb_allow_mpp` 、TiDBがクエリ実行時にMPPモードを選択できるかどうかを制御します。変数`tidb_enforce_mpp` 、オプティマイザのコスト見積もりを無視し、クエリ実行時にTiFlashのMPPモードを強制的に使用するかどうかを制御します。

これら 2 つの変数のすべての値に対応する結果は次のとおりです。

|                             | tidb_allow_mpp=オフ | tidb_allow_mpp=on (デフォルト)                 |
| --------------------------- | ----------------- | ----------------------------------------- |
| tidb_enforce_mpp=off（デフォルト） | MPP モードは使用されません。  | オプティマイザーはコスト推定に基づいて MPP モードを選択します。(デフォルト) |
| tidb_enforce_mpp=オン         | MPP モードは使用されません。  | TiDB はコスト見積りを無視し、MPP モードを選択します。           |

たとえば、MPP モードを使用しない場合は、次のステートメントを実行できます。

```sql
set @@session.tidb_allow_mpp=0;
```

TiDB のコストベース オプティマイザーで MPP モード (デフォルト) を使用するかどうかを自動的に決定する場合は、次のステートメントを実行します。

```sql
set @@session.tidb_allow_mpp=1;
set @@session.tidb_enforce_mpp=0;
```

TiDB でオプティマイザのコスト見積りを無視し、強制的に MPP モードを選択する場合は、次のステートメントを実行できます。

```sql
set @@session.tidb_allow_mpp=1;
set @@session.tidb_enforce_mpp=1;
```

<CustomContent platform="tidb">

セッション変数`tidb_enforce_mpp`の初期値は、この tidb-server インスタンスの[`enforce-mpp`](/tidb-configuration-file.md#enforce-mpp)設定値（デフォルトは`false` ）と同じです。TiDB クラスター内の複数の tidb-server インスタンスが分析クエリのみを実行し、これらのインスタンスで MPP モードが確実に使用されるようにしたい場合は、それらの[`enforce-mpp`](/tidb-configuration-file.md#enforce-mpp)設定値を`true`に変更できます。

</CustomContent>

> **注記：**
>
> `tidb_enforce_mpp=1`有効になると、TiDB オプティマイザはコスト見積もりを無視して MPP モードを選択します。ただし、他の要因によって MPP モードがブロックされる場合、TiDB は MPP モードを選択しません。これらの要因には、 TiFlashレプリカが存在しない、 TiFlashレプリカのレプリケーションが未完了である、MPP モードでサポートされていない演算子または関数を含むステートメントなどがあります。
>
> TiDBオプティマイザがコスト見積もり以外の理由でMPPモードを選択できない場合、 `EXPLAIN`ステートメントを使用して実行プランを確認すると、その理由を説明する警告が返されます。例:
>
> ```sql
> set @@session.tidb_enforce_mpp=1;
> create table t(a int);
> explain select count(*) from t;
> show warnings;
> ```
>
>     +---------+------+-----------------------------------------------------------------------------+
>     | Level   | Code | Message                                                                     |
>     +---------+------+-----------------------------------------------------------------------------+
>     | Warning | 1105 | MPP mode may be blocked because there aren't tiflash replicas of table `t`. |
>     +---------+------+-----------------------------------------------------------------------------+

## MPPモードのアルゴリズムサポート {#algorithm-support-for-the-mpp-mode}

MPPモードは、ブロードキャストハッシュ結合、シャッフルハッシュ結合、シャッフルハッシュ集計、Union All、TopN、およびLimitという物理アルゴリズムをサポートしています。オプティマイザーは、クエリで使用するアルゴリズムを自動的に決定します。具体的なクエリ実行プランを確認するには、 `EXPLAIN`のステートメントを実行してください。3 `EXPLAIN`のステートメントの結果にExchangeSender演算子とExchangeReceiver演算子が表示された場合、MPPモードが有効になっていることを示します。

次のステートメントは、TPC-H テスト セット内のテーブル構造を例として示しています。

```sql
explain select count(*) from customer c join nation n on c.c_nationkey=n.n_nationkey;
+------------------------------------------+------------+--------------+---------------+----------------------------------------------------------------------------+
| id                                       | estRows    | task         | access object | operator info                                                              |
+------------------------------------------+------------+--------------+---------------+----------------------------------------------------------------------------+
| HashAgg_23                               | 1.00       | root         |               | funcs:count(Column#16)->Column#15                                          |
| └─TableReader_25                         | 1.00       | root         |               | data:ExchangeSender_24                                                     |
|   └─ExchangeSender_24                    | 1.00       | mpp[tiflash] |               | ExchangeType: PassThrough                                                  |
|     └─HashAgg_12                         | 1.00       | mpp[tiflash] |               | funcs:count(1)->Column#16                                                  |
|       └─HashJoin_17                      | 3000000.00 | mpp[tiflash] |               | inner join, equal:[eq(tpch.nation.n_nationkey, tpch.customer.c_nationkey)] |
|         ├─ExchangeReceiver_21(Build)     | 25.00      | mpp[tiflash] |               |                                                                            |
|         │ └─ExchangeSender_20            | 25.00      | mpp[tiflash] |               | ExchangeType: Broadcast                                                    |
|         │   └─TableFullScan_18           | 25.00      | mpp[tiflash] | table:n       | keep order:false                                                           |
|         └─TableFullScan_22(Probe)        | 3000000.00 | mpp[tiflash] | table:c       | keep order:false                                                           |
+------------------------------------------+------------+--------------+---------------+----------------------------------------------------------------------------+
9 rows in set (0.00 sec)
```

この実行プランの例には、演算子`ExchangeReceiver`と演算子`ExchangeSender`含まれています。この実行プランは、演算子`ExchangeSender`テーブル`nation`読み取った後、各ノードにテーブルをブロードキャストし、演算子`HashJoin`と演算子`HashAgg`テーブル`nation`とテーブル`customer`に対して実行され、結果がTiDBに返されることを示しています。

TiFlash は、ブロードキャスト ハッシュ結合を使用するかどうかを制御する次の 3 つのグローバル/セッション変数を提供します。

-   [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-new-in-v50) : 値の単位はバイトです。テーブルサイズ（バイト単位）が変数の値より小さい場合は、ブロードキャストハッシュ結合アルゴリズムが使用されます。それ以外の場合は、シャッフルハッシュ結合アルゴリズムが使用されます。
-   [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50) : 値の単位は行です。結合操作のオブジェクトがサブクエリに属する場合、オプティマイザはサブクエリの結果セットのサイズを推定できないため、結果セットの行数によってサイズが決定されます。サブクエリの推定行数がこの変数の値より少ない場合は、ブロードキャストハッシュ結合アルゴリズムが使用されます。それ以外の場合は、シャッフルハッシュ結合アルゴリズムが使用されます。
-   [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-new-in-v710) : ネットワーク転送のオーバーヘッドが最小となるアルゴリズムを使用するかどうかを制御します。この変数を有効にすると、TiDBはネットワークで交換されるデータのサイズをそれぞれ`Broadcast Hash Join`と`Shuffled Hash Join`で推定し、サイズが小さい方を選択します。この変数を有効にすると、 [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50)と[`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-new-in-v50)無効になります。

## MPP モードでパーティション テーブルにアクセスする {#access-partitioned-tables-in-the-mpp-mode}

MPP モードでパーティション テーブルにアクセスするには、まず[動的剪定モード](https://docs.pingcap.com/tidb/stable/partitioned-table#dynamic-pruning-mode)有効にする必要があります。

例：

```sql
mysql> DROP TABLE if exists test.employees;
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> CREATE TABLE test.employees
(id int NOT NULL,
 fname varchar(30) DEFAULT NULL,
 lname varchar(30) DEFAULT NULL,
 hired date NOT NULL DEFAULT '1970-01-01',
 separated date DEFAULT '9999-12-31',
 job_code int DEFAULT NULL,
 store_id int NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
PARTITION BY RANGE (store_id)
(PARTITION p0 VALUES LESS THAN (6),
 PARTITION p1 VALUES LESS THAN (11),
 PARTITION p2 VALUES LESS THAN (16),
 PARTITION p3 VALUES LESS THAN (MAXVALUE));
Query OK, 0 rows affected (0.10 sec)

mysql> ALTER table test.employees SET tiflash replica 1;
Query OK, 0 rows affected (0.09 sec)

mysql> SET tidb_partition_prune_mode=static;
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> explain SELECT count(*) FROM test.employees;
+----------------------------------+----------+-------------------+-------------------------------+-----------------------------------+
| id                               | estRows  | task              | access object                 | operator info                     |
+----------------------------------+----------+-------------------+-------------------------------+-----------------------------------+
| HashAgg_18                       | 1.00     | root              |                               | funcs:count(Column#10)->Column#9  |
| └─PartitionUnion_20              | 4.00     | root              |                               |                                   |
|   ├─StreamAgg_35                 | 1.00     | root              |                               | funcs:count(Column#12)->Column#10 |
|   │ └─TableReader_36             | 1.00     | root              |                               | data:StreamAgg_26                 |
|   │   └─StreamAgg_26             | 1.00     | batchCop[tiflash] |                               | funcs:count(1)->Column#12         |
|   │     └─TableFullScan_34       | 10000.00 | batchCop[tiflash] | table:employees, partition:p0 | keep order:false, stats:pseudo    |
|   ├─StreamAgg_52                 | 1.00     | root              |                               | funcs:count(Column#14)->Column#10 |
|   │ └─TableReader_53             | 1.00     | root              |                               | data:StreamAgg_43                 |
|   │   └─StreamAgg_43             | 1.00     | batchCop[tiflash] |                               | funcs:count(1)->Column#14         |
|   │     └─TableFullScan_51       | 10000.00 | batchCop[tiflash] | table:employees, partition:p1 | keep order:false, stats:pseudo    |
|   ├─StreamAgg_69                 | 1.00     | root              |                               | funcs:count(Column#16)->Column#10 |
|   │ └─TableReader_70             | 1.00     | root              |                               | data:StreamAgg_60                 |
|   │   └─StreamAgg_60             | 1.00     | batchCop[tiflash] |                               | funcs:count(1)->Column#16         |
|   │     └─TableFullScan_68       | 10000.00 | batchCop[tiflash] | table:employees, partition:p2 | keep order:false, stats:pseudo    |
|   └─StreamAgg_86                 | 1.00     | root              |                               | funcs:count(Column#18)->Column#10 |
|     └─TableReader_87             | 1.00     | root              |                               | data:StreamAgg_77                 |
|       └─StreamAgg_77             | 1.00     | batchCop[tiflash] |                               | funcs:count(1)->Column#18         |
|         └─TableFullScan_85       | 10000.00 | batchCop[tiflash] | table:employees, partition:p3 | keep order:false, stats:pseudo    |
+----------------------------------+----------+-------------------+-------------------------------+-----------------------------------+
18 rows in set (0,00 sec)

mysql> SET tidb_partition_prune_mode=dynamic;
Query OK, 0 rows affected (0.00 sec)

mysql> explain SELECT count(*) FROM test.employees;
+------------------------------+----------+--------------+-----------------+---------------------------------------------------------+
| id                           | estRows  | task         | access object   | operator info                                           |
+------------------------------+----------+--------------+-----------------+---------------------------------------------------------+
| HashAgg_17                   | 1.00     | root         |                 | funcs:count(Column#11)->Column#9                        |
| └─TableReader_19             | 1.00     | root         | partition:all   | data:ExchangeSender_18                                  |
|   └─ExchangeSender_18        | 1.00     | mpp[tiflash] |                 | ExchangeType: PassThrough                               |
|     └─HashAgg_8              | 1.00     | mpp[tiflash] |                 | funcs:count(1)->Column#11                               |
|       └─TableFullScan_16     | 10000.00 | mpp[tiflash] | table:employees | keep order:false, stats:pseudo, PartitionTableScan:true |
+------------------------------+----------+--------------+-----------------+---------------------------------------------------------+
5 rows in set (0,00 sec)
```
