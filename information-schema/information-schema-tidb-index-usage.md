---
title: TIDB_INDEX_USAGE
summary: TIDB_INDEX_USAGE` INFORMATION_SCHEMA テーブルについて学習します。
---

# TIDB_インデックス_使用法 {#tidb-index-usage}

<CustomContent platform="tidb">

TiDB v8.0.0以降、 `TIDB_INDEX_USAGE`テーブルが提供されます`TIDB_INDEX_USAGE`使用すると、現在のTiDBノード上のすべてのインデックスの使用状況統計を取得できます。デフォルトでは、TiDBはSQL文の実行中にこれらのインデックス使用状況統計を収集します。この機能を無効にするには、 [`instance.tidb_enable_collect_execution_info`](/tidb-configuration-file.md#tidb_enable_collect_execution_info)設定項目または[`tidb_enable_collect_execution_info`](/system-variables.md#tidb_enable_collect_execution_info)システム変数をオフにします。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB v8.0.0以降、 `TIDB_INDEX_USAGE`テーブルが提供されます`TIDB_INDEX_USAGE`使用すると、現在のTiDBノード上のすべてのインデックスの使用状況統計を取得できます。デフォルトでは、TiDBはSQL文の実行中にこれらのインデックス使用状況統計を収集します。この機能を無効にするには、 [`instance.tidb_enable_collect_execution_info`](https://docs.pingcap.com/tidb/v8.0/tidb-configuration-file#tidb_enable_collect_execution_info)設定項目または[`tidb_enable_collect_execution_info`](/system-variables.md#tidb_enable_collect_execution_info)システム変数をオフにします。

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

`TIDB_INDEX_USAGE`テーブルの列は次のとおりです。

-   `TABLE_SCHEMA` : インデックスを含むテーブルが属するデータベースの名前。
-   `TABLE_NAME` : インデックスを含むテーブルの名前。
-   `INDEX_NAME` : インデックスの名前。
-   `QUERY_TOTAL` : インデックスにアクセスするステートメントの合計数。
-   `KV_REQ_TOTAL` : インデックスにアクセスするときに生成される KV リクエストの合計数。
-   `ROWS_ACCESS_TOTAL` : インデックスにアクセスするときにスキャンされる行の合計数。
-   `PERCENTAGE_ACCESS_0` : 行アクセス率 (テーブル内の行の総数に対するアクセスされた行の割合) が 0 である回数。
-   `PERCENTAGE_ACCESS_0_1` : 行アクセス率が 0% から 1% の間となる回数。
-   `PERCENTAGE_ACCESS_1_10` : 行アクセス率が 1% ～ 10% となる回数。
-   `PERCENTAGE_ACCESS_10_20` : 行アクセス率が 10% ～ 20% となる回数。
-   `PERCENTAGE_ACCESS_20_50` : 行アクセス率が 20% ～ 50% の間となる回数。
-   `PERCENTAGE_ACCESS_50_100` : 行アクセス率が 50% ～ 100% の間となる回数。
-   `PERCENTAGE_ACCESS_100` : 行アクセス率が 100% となる回数。
-   `LAST_ACCESS_TIME` : インデックスへの最終アクセス時刻。

## クラスター_TIDB_インデックス_使用法 {#cluster-tidb-index-usage}

`TIDB_INDEX_USAGE`テーブルは、単一の TiDB ノード上のすべてのインデックスの使用状況統計のみを提供します。クラスター内のすべての TiDB ノードのインデックス使用状況統計を取得するには、 `CLUSTER_TIDB_INDEX_USAGE`テーブルをクエリする必要があります。

`TIDB_INDEX_USAGE`番目のテーブルと比較すると、 `CLUSTER_TIDB_INDEX_USAGE`番目のテーブルのクエリ結果には`INSTANCE`のフィールドが追加されています。このフィールドには、クラスター内の各ノードの IP アドレスとポート番号が表示されるため、異なるノード間の統計情報を区別するのに役立ちます。

```sql
USE INFORMATION_SCHEMA;
DESC CLUSTER_TIDB_INDEX_USAGE;
```

出力は次のようになります。

```sql
+--------------------------+-------------+------+------+---------+-------+
| Field                    | Type        | Null | Key  | Default | Extra |
+--------------------------+-------------+------+------+---------+-------+
| INSTANCE                 | varchar(64) | YES  |      | NULL    |       |
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
15 rows in set (0.00 sec)
```

## 制限事項 {#limitations}

-   `TIDB_INDEX_USAGE`テーブルのデータは最大 5 分遅延される可能性があります。
-   TiDB が再起動すると、 `TIDB_INDEX_USAGE`テーブルのデータがクリアされます。
-   TiDB は、テーブルに有効な統計がある場合にのみ、テーブルのインデックスの使用状況を記録します。

## 続きを読む {#read-more}

-   [`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md)
