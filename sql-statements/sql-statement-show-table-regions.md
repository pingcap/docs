---
title: SHOW TABLE REGIONS
summary: Learn how to use SHOW TABLE REGIONS in TiDB.
---

# テーブル領域を表示 {#show-table-regions}

`SHOW TABLE REGIONS`ステートメントは、TiDB 内のテーブルのリージョン情報を表示するために使用されます。

## 構文 {#syntax}

```sql
SHOW TABLE [table_name] REGIONS [WhereClauseOptional];
SHOW TABLE [table_name] INDEX [index_name] REGIONS [WhereClauseOptional];
```

## あらすじ {#synopsis}

**ShowTableRegionStmt:**

![ShowTableRegionStmt](/media/sqlgram/ShowTableRegionStmt.png)

**テーブル名:**

![TableName](/media/sqlgram/TableName.png)

**PartitionNameListOpt:**

![PartitionNameListOpt](/media/sqlgram/PartitionNameListOpt.png)

**Where句オプション:**

![WhereClauseOptional](/media/sqlgram/WhereClauseOptional.png)

**Where句:**

![WhereClause](/media/sqlgram/WhereClause.png)

`SHOW TABLE REGIONS`を実行すると、次の列が返されます。

-   `REGION_ID` :リージョンID。
-   `START_KEY` :リージョンの開始キー。
-   `END_KEY` :リージョンの終了キー。
-   `LEADER_ID` :リージョンのLeaderID。
-   `LEADER_STORE_ID` :リージョンリーダーが配置されているストア (TiKV) の ID。
-   `PEERS` : すべてのリージョンレプリカの ID。
-   `SCATTERING` :リージョンがスケジュールされているかどうか。 `1`真を意味します。
-   `WRITTEN_BYTES` : 1ハートビートサイクル内でリージョンに書き込まれる推定データ量。単位はバイトです。
-   `READ_BYTES` : 1ハートビートサイクル内にリージョンから読み取られた推定データ量。単位はバイトです。
-   `APPROXIMATE_SIZE(MB)` : リージョン内の推定データ量。単位はメガバイト (MB) です。
-   `APPROXIMATE_KEYS` :リージョン内のキーの推定数。

<CustomContent platform="tidb">

-   `SCHEDULING_CONSTRAINTS` :リージョンが属するテーブルまたはパーティションに関連付けられた[配置ポリシー設定](/placement-rules-in-sql.md) 。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   `SCHEDULING_CONSTRAINTS` :リージョンが属するテーブルまたはパーティションに関連付けられた配置ポリシー設定。

</CustomContent>

-   `SCHEDULING_STATE` : 配置ポリシーを持つリージョンのスケジュール状態。

> **ノート：**
>
> `WRITTEN_BYTES` 、 `READ_BYTES` 、 `APPROXIMATE_SIZE(MB)` 、 `APPROXIMATE_KEYS`の値は正確なデータではありません。これらは、 PD がリージョンから受信したハートビート情報に基づいて PD から推定されたデータです。

## 例 {#examples}

いくつかのリージョンを埋めるのに十分なデータを含むサンプル テーブルを作成します。

{{< copyable "" >}}

```sql
CREATE TABLE t1 (
 id INT NOT NULL PRIMARY KEY auto_increment,
 b INT NOT NULL,
 pad1 VARBINARY(1024),
 pad2 VARBINARY(1024),
 pad3 VARBINARY(1024)
);
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM dual;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
SELECT SLEEP(5);
SHOW TABLE t1 REGIONS;
```

出力は、テーブルがリージョンに分割されていることを示しているはずです。 `REGION_ID` 、 `START_KEY` 、および`END_KEY`正確に一致しない場合があります。

```sql
...
mysql> SHOW TABLE t1 REGIONS;
+-----------+--------------+--------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
| REGION_ID | START_KEY    | END_KEY      | LEADER_ID | LEADER_STORE_ID | PEERS | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS | SCHEDULING_CONSTRAINTS | SCHEDULING_STATE |
+-----------+--------------+--------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
|        94 | t_75_        | t_75_r_31717 |        95 |               1 | 95    |          0 |             0 |          0 |                  112 |           207465 |                        |                  |
|        96 | t_75_r_31717 | t_75_r_63434 |        97 |               1 | 97    |          0 |             0 |          0 |                   97 |                0 |                        |                  |
|         2 | t_75_r_63434 |              |         3 |               1 | 3     |          0 |     269323514 |   66346110 |                  245 |           162020 |                        |                  |
+-----------+--------------+--------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
3 rows in set (0.00 sec)
```

上記の出力では、 `t_75_r_31717`の`START_KEY`と`t_75_r_63434`の`END_KEY` PRIMARY KEY が`31717` ～ `63434`のデータがこのリージョンに格納されていることを示しています。プレフィックス`t_75_`これが内部テーブル ID `75`を持つテーブル ( `t` ) のリージョンであることを示します。 `START_KEY`または`END_KEY`空のキー値は、それぞれ負の無限大または正の無限大を示します。

TiDB は、必要に応じてリージョンを自動的に再調整します。手動でリバランスするには、次の`SPLIT TABLE REGION`ステートメントを使用します。

```sql
mysql> SPLIT TABLE t1 BETWEEN (31717) AND (63434) REGIONS 2;
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
|                  1 |                    1 |
+--------------------+----------------------+
1 row in set (42.34 sec)

mysql> SHOW TABLE t1 REGIONS;
+-----------+--------------+--------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
| REGION_ID | START_KEY    | END_KEY      | LEADER_ID | LEADER_STORE_ID | PEERS | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS | SCHEDULING_CONSTRAINTS | SCHEDULING_STATE |
+-----------+--------------+--------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
|        94 | t_75_        | t_75_r_31717 |        95 |               1 | 95    |          0 |             0 |          0 |                  112 |           207465 |                        |                  |
|        98 | t_75_r_31717 | t_75_r_47575 |        99 |               1 | 99    |          0 |          1325 |          0 |                   53 |            12052 |                        |                  |
|        96 | t_75_r_47575 | t_75_r_63434 |        97 |               1 | 97    |          0 |          1526 |          0 |                   48 |                0 |                        |                  |
|         2 | t_75_r_63434 |              |         3 |               1 | 3     |          0 |             0 |   55752049 |                   60 |                0 |                        |                  |
+-----------+--------------+--------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
4 rows in set (0.00 sec)
```

上記の出力は、リージョン96 が分割され、新しいリージョン98 が作成されたことを示しています。テーブル内の残りのリージョンは、分割操作の影響を受けませんでした。これは、出力統計によって確認されます。

-   `TOTAL_SPLIT_REGION`新しく分割されたリージョンの数を示します。この例では、番号は 1 です。
-   `SCATTER_FINISH_RATIO`新しく分割されたリージョンが正常に分散される割合を示します。 `1.0` 、すべてのリージョンが分散していることを意味します。

より詳細な例:

```sql
mysql> show table t regions;
+-----------+--------------+--------------+-----------+-----------------+---------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
| REGION_ID | START_KEY    | END_KEY      | LEADER_ID | LEADER_STORE_ID | PEERS         | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS | SCHEDULING_CONSTRAINTS | SCHEDULING_STATE |
+-----------+--------------+--------------+-----------+-----------------+---------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
| 102       | t_43_r       | t_43_r_20000 | 118       | 7               | 105, 118, 119 | 0          | 0             | 0          | 1                    | 0                |                        |                  |
| 106       | t_43_r_20000 | t_43_r_40000 | 120       | 7               | 107, 108, 120 | 0          | 23            | 0          | 1                    | 0                |                        |                  |
| 110       | t_43_r_40000 | t_43_r_60000 | 112       | 9               | 112, 113, 121 | 0          | 0             | 0          | 1                    | 0                |                        |                  |
| 114       | t_43_r_60000 | t_43_r_80000 | 122       | 7               | 115, 122, 123 | 0          | 35            | 0          | 1                    | 0                |                        |                  |
| 3         | t_43_r_80000 |              | 93        | 8               | 5, 73, 93     | 0          | 0             | 0          | 1                    | 0                |                        |                  |
| 98        | t_43_        | t_43_r       | 99        | 1               | 99, 100, 101  | 0          | 0             | 0          | 1                    | 0                |                        |                  |
+-----------+--------------+--------------+-----------+-----------------+---------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
6 rows in set
```

上記の例では:

-   表 t は 6 つの地域に対応しています。これらのリージョンでは、 `102` 、 `106` 、 `110` 、 `114` 、および`3`に行データが格納され、 `98`インデックス データが格納されます。
-   リージョン `102`の`START_KEY`と`END_KEY`の場合、 `t_43`テーブルのプレフィックスと ID を示します。 `_r`は、テーブル t のレコード データのプレフィックスです。 `_i`はインデックス データのプレフィックスです。
-   リージョン `102`は`[-inf, 20000)`の範囲`START_KEY`レコードデータが格納されて`END_KEY`ことを意味します。同様に、リージョン ( `106` 、 `110` 、 `114` 、 `3` ) のデータstorageの範囲も計算できます。
-   リージョン`98`にはインデックス データが格納されます。テーブル t のインデックス データの開始キーは`t_43_i`で、リージョン`98`の範囲にあります。

ストア 1 のテーブル t に対応するリージョンを確認するには、 `WHERE`句を使用します。

```sql
test> show table t regions where leader_store_id =1;
+-----------+-----------+---------+-----------+-----------------+--------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
| REGION_ID | START_KEY | END_KEY | LEADER_ID | LEADER_STORE_ID | PEERS        | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS | SCHEDULING_CONSTRAINTS | SCHEDULING_STATE |
+-----------+-----------+---------+-----------+-----------------+--------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
| 98        | t_43_     | t_43_r  | 99        | 1               | 99, 100, 101 | 0          | 0             | 0          | 1                    | 0                |                        |                  |
+-----------+-----------+---------+-----------+-----------------+--------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
```

インデックス データをリージョンに分割するには、 `SPLIT TABLE REGION`を使用します。次の例では、テーブル t のインデックス データ`name` `[a,z]`の範囲で 2 つの Region に分割されます。

```sql
test> split table t index name between ("a") and ("z") regions 2;
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
| 2                  | 1.0                  |
+--------------------+----------------------+
1 row in set
```

ここで、テーブル t は 7 つの地域に対応します。そのうちの 5 つ ( `102` ) は`3` t のレコード データ`114`格納し、残りの 2 つ`110` `135` ) `106`インデックス データ`name`を格納します`98`

```sql
test> show table t regions;
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
| REGION_ID | START_KEY                   | END_KEY                     | LEADER_ID | LEADER_STORE_ID | PEERS         | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS | SCHEDULING_CONSTRAINTS | SCHEDULING_STATE |
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
| 102       | t_43_r                      | t_43_r_20000                | 118       | 7               | 105, 118, 119 | 0          | 0             | 0          | 1                    | 0                |                        |                  |
| 106       | t_43_r_20000                | t_43_r_40000                | 120       | 7               | 108, 120, 126 | 0          | 0             | 0          | 1                    | 0                |                        |                  |
| 110       | t_43_r_40000                | t_43_r_60000                | 112       | 9               | 112, 113, 121 | 0          | 0             | 0          | 1                    | 0                |                        |                  |
| 114       | t_43_r_60000                | t_43_r_80000                | 122       | 7               | 115, 122, 123 | 0          | 35            | 0          | 1                    | 0                |                        |                  |
| 3         | t_43_r_80000                |                             | 93        | 8               | 73, 93, 128   | 0          | 0             | 0          | 1                    | 0                |                        |                  |
| 135       | t_43_i_1_                   | t_43_i_1_016d80000000000000 | 139       | 2               | 138, 139, 140 | 0          | 35            | 0          | 1                    | 0                |                        |                  |
| 98        | t_43_i_1_016d80000000000000 | t_43_r                      | 99        | 1               | 99, 100, 101  | 0          | 0             | 0          | 1                    | 0                |                        |                  |
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
7 rows in set
```

## MySQL の互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## こちらもご覧ください {#see-also}

-   [スプリットリージョン](/sql-statements/sql-statement-split-region.md)
-   [テーブルを作成](/sql-statements/sql-statement-create-table.md)
