---
title: TIDB_INDEX_USAGE
summary: TIDB_INDEX_USAGE` INFORMATION_SCHEMA テーブルについて学習します。
---

# TIDB_インデックス使用法 {#tidb-index-usage}

<CustomContent platform="tidb">

v8.0.0 以降、TiDB は`TIDB_INDEX_USAGE`テーブルを提供します`TIDB_INDEX_USAGE`使用して、現在の TiDB ノード上のすべてのインデックスの使用統計を取得できます。デフォルトでは、TiDB は SQL ステートメントの実行中にこれらのインデックス使用統計を[`tidb_enable_collect_execution_info`](/system-variables.md#tidb_enable_collect_execution_info) [`instance.tidb_enable_collect_execution_info`](/tidb-configuration-file.md#tidb_enable_collect_execution_info)変数をオフにすることで、この機能を無効にすることができます。

</CustomContent>

<CustomContent platform="tidb-cloud">

v8.0.0 以降、TiDB は`TIDB_INDEX_USAGE`テーブルを提供します`TIDB_INDEX_USAGE`使用して、現在の TiDB ノード上のすべてのインデックスの使用統計を取得できます。デフォルトでは、TiDB は SQL ステートメントの実行中にこれらのインデックス使用統計を[`tidb_enable_collect_execution_info`](/system-variables.md#tidb_enable_collect_execution_info) [`instance.tidb_enable_collect_execution_info`](https://docs.pingcap.com/tidb/v8.0/tidb-configuration-file#tidb_enable_collect_execution_info)変数をオフにすることで、この機能を無効にすることができます。

</CustomContent>

```sql
USE INFORMATION_SCHEMA;
DESC TIDB_INDEX_USAGE;
```

```sql
+--------------------------+-------------+------+------+---------+-------+
| Field                    | Type        | Null | Key  | Default | Extra |
+--------------------------+-------------+------+------+---------+-------+
| TABLE_SCHEMA             | varchar(64) | YES  |      | NULL    |       |
| TABLE_NAME               | varchar(64) | YES  |      | NULL    |       |
| INDEX_NAME               | varchar(64) | YES  |      | NULL    |       |
| QUERY_TOTAL              | bigint(21)  | YES  |      | NULL    |       |
| KV_REQ_TOTAL             | bigint(21)  | YES  |      | NULL    |       |
| ROWS_ACCESS_TOTAL        | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_0      | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_0_1    | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_1_10   | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_10_20  | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_20_50  | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_50_100 | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_100    | bigint(21)  | YES  |      | NULL    |       |
| LAST_ACCESS_TIME         | datetime    | YES  |      | NULL    |       |
+--------------------------+-------------+------+------+---------+-------+
14 rows in set (0.00 sec)
```

`TIDB_INDEX_USAGE`表の列は次のとおりです。

-   `TABLE_SCHEMA` : インデックスを含むテーブルが属するデータベースの名前。
-   `TABLE_NAME` : インデックスを含むテーブルの名前。
-   `INDEX_NAME` : インデックスの名前。
-   `QUERY_TOTAL` : インデックスにアクセスするステートメントの合計数。
-   `KV_REQ_TOTAL` : インデックスにアクセスするときに生成される KV リクエストの合計数。
-   `ROWS_ACCESS_TOTAL` : インデックスにアクセスするときにスキャンされる行の合計数。
-   `PERCENTAGE_ACCESS_0` : 行アクセス率 (テーブル内の行の総数に対するアクセスされた行の割合) が 0 である回数。
-   `PERCENTAGE_ACCESS_0_1` : 行アクセス率が 0% から 1% の間である回数。
-   `PERCENTAGE_ACCESS_1_10` : 行アクセス率が 1% から 10% の間である回数。
-   `PERCENTAGE_ACCESS_10_20` : 行アクセス率が 10% から 20% の間である回数。
-   `PERCENTAGE_ACCESS_20_50` : 行アクセス率が 20% から 50% の間である回数。
-   `PERCENTAGE_ACCESS_50_100` : 行アクセス率が 50% から 100% の間である回数。
-   `PERCENTAGE_ACCESS_100` : 行アクセス率が 100% となる回数。
-   `LAST_ACCESS_TIME` : インデックスへの最終アクセス時刻。

## クラスター_TIDB_インデックス_使用法 {#cluster-tidb-index-usage}

`TIDB_INDEX_USAGE`テーブルは、単一の TiDB ノード上のすべてのインデックスの使用状況統計のみを提供します。クラスター内のすべての TiDB ノードのインデックス使用状況統計を取得するには、 `CLUSTER_TIDB_INDEX_USAGE`テーブルをクエリする必要があります。

`TIDB_INDEX_USAGE`テーブルと比較すると、 `CLUSTER_TIDB_INDEX_USAGE`テーブルのクエリ結果には追加の`INSTANCE`フィールドが含まれます。このフィールドには、クラスター内の各ノードの IP アドレスとポートが表示されるため、異なるノード間の統計を区別するのに役立ちます。

```sql
USE INFORMATION_SCHEMA;
DESC CLUSTER_TIDB_INDEX_USAGE;
```

出力は次のようになります。

```sql
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
| Field                   | Type                                                            | Null | Key  | Default | Extra |
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
| INSTANCE                | varchar(64)                                                     | YES  |      | NULL    |       |
| ID                      | bigint(21) unsigned                                             | NO   | PRI  | NULL    |       |
| START_TIME              | timestamp(6)                                                    | YES  |      | NULL    |       |
| CURRENT_SQL_DIGEST      | varchar(64)                                                     | YES  |      | NULL    |       |
| CURRENT_SQL_DIGEST_TEXT | text                                                            | YES  |      | NULL    |       |
| STATE                   | enum('Idle','Running','LockWaiting','Committing','RollingBack') | YES  |      | NULL    |       |
| WAITING_START_TIME      | timestamp(6)                                                    | YES  |      | NULL    |       |
| MEM_BUFFER_KEYS         | bigint(64)                                                      | YES  |      | NULL    |       |
| MEM_BUFFER_BYTES        | bigint(64)                                                      | YES  |      | NULL    |       |
| SESSION_ID              | bigint(21) unsigned                                             | YES  |      | NULL    |       |
| USER                    | varchar(16)                                                     | YES  |      | NULL    |       |
| DB                      | varchar(64)                                                     | YES  |      | NULL    |       |
| ALL_SQL_DIGESTS         | text                                                            | YES  |      | NULL    |       |
| RELATED_TABLE_IDS       | text                                                            | YES  |      | NULL    |       |
| WAITING_TIME            | double                                                          | YES  |      | NULL    |       |
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
15 rows in set (0.00 sec)
```

## 制限事項 {#limitations}

-   `TIDB_INDEX_USAGE`のテーブルのデータは最大 5 分遅延される可能性があります。
-   TiDB が再起動すると、 `TIDB_INDEX_USAGE`テーブル内のデータがクリアされます。

## 続きを読む {#read-more}

-   [`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md)
