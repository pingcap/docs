---
title: Use TiFlash MPP Mode
summary: Learn the MPP mode of TiFlash and how to use it.
---

# TiFlash MPP モードを使用する {#use-tiflash-mpp-mode}

<CustomContent platform="tidb">

このドキュメントでは、 TiFlashの[超並列処理 (MPP)](/glossary.md#mpp)モードとその使用方法を紹介します。

</CustomContent>

<CustomContent platform="tidb-cloud">

このドキュメントでは、 TiFlashの[超並列処理 (MPP)](/tidb-cloud/tidb-cloud-glossary.md#mpp)モードとその使用方法を紹介します。

</CustomContent>

TiFlash は、計算にクロスノード データ交換 (データ シャッフル プロセス) を導入するクエリの実行に MPP モードの使用をサポートします。 TiDB は、オプティマイザーのコスト推定を使用して、MPP モードを選択するかどうかを自動的に決定します。 [`tidb_allow_mpp`](/system-variables.md#tidb_allow_mpp-new-in-v50)と[`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51)の値を変更することで、選択戦略を変更できます。

次の図は、MPP モードがどのように機能するかを示しています。

![mpp-mode](/media/tiflash/tiflash-mpp.png)

## MPP モードを選択するかどうかを制御します {#control-whether-to-select-the-mpp-mode}

`tidb_allow_mpp`変数は、TiDB がクエリを実行するために MPP モードを選択できるかどうかを制御します。 `tidb_enforce_mpp`変数は、オプティマイザのコスト推定を無視し、クエリの実行にTiFlashの MPP モードを強制的に使用するかどうかを制御します。

これら 2 つの変数のすべての値に対応する結果は次のとおりです。

|                              | tidb_allow_mpp=off | tidb_allow_mpp=on (デフォルト)                 |
| ---------------------------- | ------------------ | ----------------------------------------- |
| tidb_enforce_mpp=off (デフォルト) | MPPモードは使用しません。     | オプティマイザはコスト推定に基づいて MPP モードを選択します。 (デフォルト) |
| tidb_enforce_mpp=on          | MPPモードは使用しません。     | TiDB はコスト見積もりを無視し、MPP モードを選択します。          |

たとえば、MPP モードを使用したくない場合は、次のステートメントを実行できます。

```sql
set @@session.tidb_allow_mpp=0;
```

TiDB のコストベースのオプティマイザーに MPP モード (デフォルト) を使用するかどうかを自動的に決定させたい場合は、次のステートメントを実行できます。

```sql
set @@session.tidb_allow_mpp=1;
set @@session.tidb_enforce_mpp=0;
```

TiDB にオプティマイザーのコスト推定を無視させ、強制的に MPP モードを選択させるには、次のステートメントを実行できます。

```sql
set @@session.tidb_allow_mpp=1;
set @@session.tidb_enforce_mpp=1;
```

<CustomContent platform="tidb">

`tidb_enforce_mpp`セッション変数の初期値は、この tidb-server インスタンスの[`enforce-mpp`](/tidb-configuration-file.md#enforce-mpp)構成値 (デフォルトでは`false` ) と同じです。 TiDB クラスター内の複数の tidb-server インスタンスが分析クエリのみを実行し、これらのインスタンスで MPP モードが使用されていることを確認したい場合は、それらの[`enforce-mpp`](/tidb-configuration-file.md#enforce-mpp)構成値を`true`に変更できます。

</CustomContent>

> **注記：**
>
> `tidb_enforce_mpp=1`が有効になると、TiDB オプティマイザーはコスト見積もりを無視して MPP モードを選択します。ただし、他の要因が MPP モードをブロックする場合、TiDB は MPP モードを選択しません。これらの要因には、 TiFlashレプリカの欠如、 TiFlashレプリカの未完了のレプリケーション、MPP モードでサポートされていない演算子または関数を含むステートメントが含まれます。
>
> TiDB オプティマイザーがコスト見積もり以外の理由で MPP モードを選択できない場合、 `EXPLAIN`ステートメントを使用して実行プランをチェックアウトすると、理由を説明する警告が返されます。例えば：
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

## MPP モードのアルゴリズムのサポート {#algorithm-support-for-the-mpp-mode}

MPP モードは、ブロードキャスト ハッシュ結合、シャッフル ハッシュ結合、シャッフル ハッシュ集計、Union All、TopN、および Limit の物理アルゴリズムをサポートします。オプティマイザは、クエリでどのアルゴリズムを使用するかを自動的に決定します。特定のクエリ実行プランを確認するには、 `EXPLAIN`ステートメントを実行します。 `EXPLAIN`ステートメントの結果に ExchangeSender 演算子と ExchangeReceiver 演算子が表示される場合は、MPP モードが有効になっていることを示します。

次のステートメントでは、例として TPC-H テスト セットのテーブル構造を取り上げます。

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

実行プランの例には、 `ExchangeReceiver`と`ExchangeSender`演算子が含まれています。実行計画は、 `nation`テーブルが読み取られた後、 `ExchangeSender`オペレーターがテーブルを各ノードにブロードキャストし、 `HashJoin`と`HashAgg`操作が`nation`テーブルと`customer`テーブルに対して実行され、結果が TiDB に返されることを示しています。

TiFlash は、ブロードキャスト ハッシュ結合を使用するかどうかを制御するために、次の 3 つのグローバル/セッション変数を提供します。

-   [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-new-in-v50) : 値の単位はバイトです。テーブル サイズ (バイト単位) が変数の値より小さい場合は、ブロードキャスト ハッシュ結合アルゴリズムが使用されます。それ以外の場合は、シャッフル ハッシュ結合アルゴリズムが使用されます。
-   [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50) : 値の単位は行です。結合操作のオブジェクトがサブクエリに属している場合、オプティマイザはサブクエリの結果セットのサイズを推定できないため、サイズは結果セット内の行数によって決まります。サブクエリ内の推定行数がこの変数の値より小さい場合は、ブロードキャスト ハッシュ結合アルゴリズムが使用されます。それ以外の場合は、シャッフル ハッシュ結合アルゴリズムが使用されます。
-   [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-new-in-v710) : ネットワーク送信のオーバーヘッドを最小限に抑えたアルゴリズムを使用するかどうかを制御します。この変数が有効な場合、TiDB はネットワーク内で交換されるデータのサイズをそれぞれ`Broadcast Hash Join`と`Shuffled Hash Join`を使用して推定し、サイズの小さい方を選択します。この変数を有効にすると、 [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50)と[`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-new-in-v50)は無効になります。

## MPP モードでパーティション化されたテーブルにアクセスする {#access-partitioned-tables-in-the-mpp-mode}

MPP モードでパーティション化されたテーブルにアクセスするには、まず[動的プルーニングモード](https://docs.pingcap.com/tidb/stable/partitioned-table#dynamic-pruning-mode)有効にする必要があります。

例：

```sql
mysql> DROP TABLE if exists test.employees;
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> CREATE TABLE test.employees
(id int(11) NOT NULL,
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
Query OK, 0 rows affected (0.00 sec)

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
