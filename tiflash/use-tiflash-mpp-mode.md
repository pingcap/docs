---
title: Use TiFlash MPP Mode
summary: Learn the MPP mode of TiFlash and how to use it.
---

# TiFlashMPPモードを使用する {#use-tiflash-mpp-mode}

このドキュメントでは、TiFlashのMPPモードとその使用方法を紹介します。

TiFlashは、MPPモードを使用したクエリの実行をサポートします。これにより、ノード間のデータ交換（データシャッフルプロセス）が計算に導入されます。 TiDBは、オプティマイザのコスト見積もりを使用して、MPPモードを選択するかどうかを自動的に決定します。 [`tidb_allow_mpp`](/system-variables.md#tidb_allow_mpp-new-in-v50)と[`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51)の値を変更することにより、選択戦略を変更できます。

## MPPモードを選択するかどうかを制御します {#control-whether-to-select-the-mpp-mode}

`tidb_allow_mpp`変数は、TiDBがクエリを実行するためにMPPモードを選択できるかどうかを制御します。 `tidb_enforce_mpp`変数は、オプティマイザーのコスト見積もりを無視するかどうかを制御し、TiFlashのMPPモードを使用してクエリを強制的に実行します。

これら2つの変数のすべての値に対応する結果は次のとおりです。

|                               | tidb_allow_mpp = off | tidb_allow_mpp = on（デフォルト）                 |
| ----------------------------- | -------------------- | ------------------------------------------ |
| tidb_enforce_mpp = off（デフォルト） | MPPモードは使用されません。      | オプティマイザは、コスト見積もりに基づいてMPPモードを選択します。 （デフォルト） |
| tidb_enforce_mpp = on         | MPPモードは使用されません。      | TiDBはコスト見積もりを無視し、MPPモードを選択します。             |

たとえば、MPPモードを使用したくない場合は、次のステートメントを実行できます。

{{< copyable "" >}}

```sql
set @@session.tidb_allow_mpp=1;
set @@session.tidb_enforce_mpp=0;
```

TiDBのコストベースのオプティマイザでMPPモード（デフォルト）を使用するかどうかを自動的に決定する場合は、次のステートメントを実行できます。

{{< copyable "" >}}

```sql
set @@session.tidb_allow_mpp=1;
set @@session.tidb_enforce_mpp=0;
```

TiDBでオプティマイザのコスト見積もりを無視し、MPPモードを強制的に選択する場合は、次のステートメントを実行できます。

{{< copyable "" >}}

```sql
set @@session.tidb_allow_mpp=1;
set @@session.tidb_enforce_mpp=1;
```

`tidb_enforce_mpp`セッション変数の初期値は、このtidb-serverインスタンスの[`enforce-mpp`](/tidb-configuration-file.md#enforce-mpp)構成値（デフォルトでは`false` ）と同じです。 TiDBクラスタの複数のtidb-serverインスタンスが分析クエリのみを実行し、これらのインスタンスでMPPモードが使用されていることを確認する場合は、 [`enforce-mpp`](/tidb-configuration-file.md#enforce-mpp)の構成値を`true`に変更できます。

> **ノート：**
>
> `tidb_enforce_mpp=1`が有効になると、TiDBオプティマイザはコスト見積もりを無視してMPPモードを選択します。ただし、他の要因がMPPモードをブロックしている場合、TiDBはMPPモードを選択しません。これらの要因には、TiFlashレプリカの欠如、TiFlashレプリカの未完成の複製、およびMPPモードでサポートされていない演算子または関数を含むステートメントが含まれます。
>
> コスト見積もり以外の理由でTiDBオプティマイザがMPPモードを選択できない場合、 `EXPLAIN`ステートメントを使用して実行プランをチェックアウトすると、理由を説明する警告が返されます。例えば：
>
> {{< copyable "" >}}
>
> ```sql
> set @@session.tidb_enforce_mpp=1;
> create table t(a int);
> explain select count(*) from t;
> show warnings;
> ```
>
> ```
> +---------+------+-----------------------------------------------------------------------------+
> | Level   | Code | Message                                                                     |
> +---------+------+-----------------------------------------------------------------------------+
> | Warning | 1105 | MPP mode may be blocked because there aren't tiflash replicas of table `t`. |
> +---------+------+-----------------------------------------------------------------------------+
> ```

## MPPモードのアルゴリズムサポート {#algorithm-support-for-the-mpp-mode}

MPPモードは、ブロードキャストハッシュ結合、シャッフルハッシュ結合、シャッフルハッシュ集計、Union All、TopN、およびLimitの物理アルゴリズムをサポートします。オプティマイザは、クエリで使用するアルゴリズムを自動的に決定します。特定のクエリ実行プランを確認するには、 `EXPLAIN`ステートメントを実行します。 `EXPLAIN`ステートメントの結果にExchangeSenderおよびExchangeReceiver演算子が表示されている場合は、MPPモードが有効になっていることを示しています。

次のステートメントは、TPC-Hテストセットのテーブル構造を例として取り上げています。

```sql
explain select count(*) from customer c join nation n on c.c_nationkey=n.n_nationkey;
+------------------------------------------+------------+-------------------+---------------+----------------------------------------------------------------------------+
| id                                       | estRows    | task              | access object | operator info                                                              |
+------------------------------------------+------------+-------------------+---------------+----------------------------------------------------------------------------+
| HashAgg_23                               | 1.00       | root              |               | funcs:count(Column#16)->Column#15                                          |
| └─TableReader_25                         | 1.00       | root              |               | data:ExchangeSender_24                                                     |
|   └─ExchangeSender_24                    | 1.00       | batchCop[tiflash] |               | ExchangeType: PassThrough                                                  |
|     └─HashAgg_12                         | 1.00       | batchCop[tiflash] |               | funcs:count(1)->Column#16                                                  |
|       └─HashJoin_17                      | 3000000.00 | batchCop[tiflash] |               | inner join, equal:[eq(tpch.nation.n_nationkey, tpch.customer.c_nationkey)] |
|         ├─ExchangeReceiver_21(Build)     | 25.00      | batchCop[tiflash] |               |                                                                            |
|         │ └─ExchangeSender_20            | 25.00      | batchCop[tiflash] |               | ExchangeType: Broadcast                                                    |
|         │   └─TableFullScan_18           | 25.00      | batchCop[tiflash] | table:n       | keep order:false                                                           |
|         └─TableFullScan_22(Probe)        | 3000000.00 | batchCop[tiflash] | table:c       | keep order:false                                                           |
+------------------------------------------+------------+-------------------+---------------+----------------------------------------------------------------------------+
9 rows in set (0.00 sec)
```

実行プランの例には、 `ExchangeReceiver`と`ExchangeSender`の演算子が含まれています。実行プランは、 `nation`テーブルが読み取られた後、 `ExchangeSender`オペレーターがテーブルを各ノードにブロードキャストし、 `HashJoin`および`HashAgg`操作が`nation`テーブルと`customer`テーブルで実行され、結果がTiDBに返されることを示しています。

TiFlashは、ブロードキャストハッシュ結合を使用するかどうかを制御するために、次の2つのグローバル/セッション変数を提供します。

-   [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50) ：値の単位はバイトです。テーブルサイズ（バイト単位）が変数の値よりも小さい場合は、ブロードキャストハッシュ結合アルゴリズムが使用されます。それ以外の場合は、シャッフルハッシュ結合アルゴリズムが使用されます。
-   [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50) ：値の単位は行です。結合操作のオブジェクトがサブクエリに属している場合、オプティマイザはサブクエリ結果セットのサイズを推定できないため、サイズは結果セットの行数によって決定されます。サブクエリの推定行数がこの変数の値よりも少ない場合は、ブロードキャストハッシュ結合アルゴリズムが使用されます。それ以外の場合は、シャッフルハッシュ結合アルゴリズムが使用されます。

## MPPモードでパーティションテーブルにアクセスする {#access-partitioned-tables-in-the-mpp-mode}

MPPモードでパーティションテーブルにアクセスするには、最初に[動的剪定モード](https://docs.pingcap.com/tidb/stable/partitioned-table#dynamic-pruning-mode)を有効にする必要があります。

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
