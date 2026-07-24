---
title: TIDB_INDEX_USAGE
summary: TIDB_INDEX_USAGE` INFORMATION_SCHEMA テーブルについて学習してください。
---

# TIDB_INDEX_USAGE {#tidb_index_usage}

<CustomContent platform="tidb">

バージョン8.0.0以降、TiDBは`TIDB_INDEX_USAGE`テーブルを提供します。 `TIDB_INDEX_USAGE`を使用すると、現在のTiDBノード上のすべてのインデックスの使用統計情報を取得できます。デフォルトでは、TiDBはSQLステートメントの実行中にこれらのインデックス使用統計情報を収集します。この機能は、 [`instance.tidb_enable_collect_execution_info`](/tidb-configuration-file.md#tidb_enable_collect_execution_info)構成項目または[`tidb_enable_collect_execution_info`](/system-variables.md#tidb_enable_collect_execution_info)システム変数をオフにすることで無効にできます。

</CustomContent>

<CustomContent platform="tidb-cloud">

バージョン8.0.0以降、TiDBは`TIDB_INDEX_USAGE`テーブルを提供します。 `TIDB_INDEX_USAGE`を使用すると、現在のTiDBノード上のすべてのインデックスの使用統計情報を取得できます。デフォルトでは、TiDBはSQLステートメントの実行中にこれらのインデックス使用統計情報を収集します。この機能は、 [`instance.tidb_enable_collect_execution_info`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#tidb_enable_collect_execution_info)構成項目または[`tidb_enable_collect_execution_info`](/system-variables.md#tidb_enable_collect_execution_info)システム変数をオフにすることで無効にできます。

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

`TIDB_INDEX_USAGE`テーブルの列は以下のとおりです。

-   `TABLE_SCHEMA` : インデックスを含むテーブルが属するデータベースの名前。
-   `TABLE_NAME` : インデックスを含むテーブルの名前。
-   `INDEX_NAME` : インデックスの名前。
-   `QUERY_TOTAL` : インデックスにアクセスするステートメントの総数。
-   `KV_REQ_TOTAL` : インデックスにアクセスした際に生成された KV リクエストの総数。
-   `ROWS_ACCESS_TOTAL` : インデックスにアクセスする際にスキャンされた行の総数。
-   `PERCENTAGE_ACCESS_0` : 行アクセス率（テーブル内の全行数に対するアクセスされた行の割合）が 0 になる回数。
-   `PERCENTAGE_ACCESS_0_1` : 行アクセス率が 0% ～ 1% である回数。
-   `PERCENTAGE_ACCESS_1_10` : 行アクセス率が 1% ～ 10% である回数。
-   `PERCENTAGE_ACCESS_10_20` : 行アクセス率が 10% ～ 20% の間である回数。
-   `PERCENTAGE_ACCESS_20_50` : 行アクセス率が 20% ～ 50% の間である回数。
-   `PERCENTAGE_ACCESS_50_100` : 行アクセス率が 50% ～ 100% の間である回数。
-   `PERCENTAGE_ACCESS_100` : 行アクセス率が 100% になる回数。
-   `LAST_ACCESS_TIME` : インデックスへの最新のアクセス時刻。

## クラスターTIDBインデックス使用状況 {#cluster_tidb_index_usage}

`TIDB_INDEX_USAGE`テーブルは、単一の TiDB ノード上のすべてのインデックスの使用統計情報のみを提供します。クラスタ内のすべての TiDB ノードのインデックス使用統計情報を取得するには、 `CLUSTER_TIDB_INDEX_USAGE`テーブルをクエリする必要があります。

`TIDB_INDEX_USAGE`テーブルと比較して、 `CLUSTER_TIDB_INDEX_USAGE`テーブルのクエリ結果には`INSTANCE`フィールドが追加されています。このフィールドには、クラスタ内の各ノードの IP アドレスとポートが表示され、異なるノード間の統計情報を区別するのに役立ちます。

```sql
USE INFORMATION_SCHEMA;
DESC CLUSTER_TIDB_INDEX_USAGE;
```

出力は以下のとおりです。

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

-   `TIDB_INDEX_USAGE`テーブルのデータは、最大 5 分遅れる場合があります。
-   TiDBが再起動すると、 `TIDB_INDEX_USAGE`テーブルのデータがクリアされます。
-   TiDBは、テーブルに有効な統計情報がある場合にのみ、そのテーブルのインデックス使用状況を記録します。

## 続きを読む {#read-more}

-   [`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md)
