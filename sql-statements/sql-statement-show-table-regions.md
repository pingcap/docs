---
title: SHOW TABLE REGIONS
summary: TiDBでSHOW TABLE REGIONSを使用する方法を学びましょう。
---

# テーブル領域を表示する {#show-table-regions}

`SHOW TABLE REGIONS`ステートメントは、TiDB のテーブルのリージョン情報を表示するために使用されます。

> **注記：**
>
> この機能は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

## 構文 {#syntax}

```sql
SHOW TABLE [table_name] REGIONS [WhereClauseOptional];
SHOW TABLE [table_name] INDEX [index_name] REGIONS [WhereClauseOptional];
```

## あらすじ {#synopsis}

```ebnf+diagram
ShowTableRegionStmt ::=
    "SHOW" "TABLE" TableName PartitionNameList? ("INDEX" IndexName)? "REGIONS" ("WHERE" Expression)?

TableName ::=
    (SchemaName ".")? Identifier
```

`SHOW TABLE REGIONS`を実行すると、次の列が返されます。

-   `REGION_ID` :リージョンID。
-   `START_KEY` :リージョンの開始キー。
-   `END_KEY` :リージョンの終了キー。
-   `LEADER_ID` :リージョンのLeaderID 。
-   `LEADER_STORE_ID` :リージョンリーダーが所在する店舗 (TiKV) の ID。
-   `PEERS` : すべてのリージョンレプリカのID。
-   `SCATTERING` :リージョンがスケジュールされているかどうか。 `1`は true を意味します。
-   `WRITTEN_BYTES` : 1回のハートビートサイクルでリージョンに書き込まれるデータの推定量。単位はバイトです。
-   `READ_BYTES` : 1回のハートビートサイクルでリージョンから読み取られたデータの推定量。単位はバイトです。
-   `APPROXIMATE_SIZE(MB)` :リージョン内の推定データ量。単位はメガバイト (MB) です。
-   `APPROXIMATE_KEYS` :リージョン内のキーの推定数。

<CustomContent platform="tidb">

-   `SCHEDULING_CONSTRAINTS` :リージョンが属するテーブルまたはパーティションに関連付けられた[配置ポリシー設定](/placement-rules-in-sql.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   `SCHEDULING_CONSTRAINTS` :リージョンが属するテーブルまたはパーティションに関連付けられた配置ポリシー設定。

</CustomContent>

-   `SCHEDULING_STATE` : 配置ポリシーを持つリージョンのスケジューリング状態。

> **注記：**
>
> `WRITTEN_BYTES` 、 `READ_BYTES` 、 `APPROXIMATE_SIZE(MB)` 、 `APPROXIMATE_KEYS`は正確なデータではありません。これらは、PD がリージョンから受信するハートビート情報に基づいて PD が推定したデータです。

## 例 {#examples}

いくつかのリージョンを埋めるのに十分なデータを含むサンプルテーブルを作成してください。

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

出力には、テーブルがリージョンに分割されていることが示されるはずです。 `REGION_ID` 、 `START_KEY` 、 `END_KEY`は完全に一致しない場合があります。

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

上記の出力では、 `START_KEY`の`t_75_r_31717`と`END_KEY`の`t_75_r_63434`は、 `31717`と`63434`の間の PRIMARY KEY を持つデータがこのリージョンに格納されていることを示しています。プレフィックス`t_75_`は、内部テーブル ID が`75` `t`のリージョンであることを示しています。 `START_KEY`または`END_KEY`のキー値が空の場合、それぞれ負の無限大または正の無限大を示します。

TiDB は必要に応じてリージョンを自動的に再バランスします。手動で再バランスする場合は、 `SPLIT TABLE REGION`ステートメントを使用してください。

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

上記の出力は、リージョン96が分割され、新しいリージョン98が作成されたことを示しています。表内の残りのリージョンは、分割操作の影響を受けませんでした。これは、出力統計によって確認できます。

-   `TOTAL_SPLIT_REGION`は、新しく分割されたリージョンの数を示します。この例では、その数は 1 です。
-   `SCATTER_FINISH_RATIO`新しく分割された領域が正常に分散される割合を示します。 `1.0` 、すべての領域が分散されたことを意味します。

より詳細な例については、以下を参照してください。

```sql
mysql> SHOW TABLE t REGIONS;
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

上記の例では：

-   テーブル t は 6 つの領域に対応しています。これらの領域では、 `102` 、 `106` 、 `110` 、 `114` 、および`3`に行データが格納され、 `98`にインデックスデータが格納されます。
-   リージョン`START_KEY`の`END_KEY`および`102`について、 `t_43`はテーブルのプレフィックスと ID を示します。 `_r`テーブル t のレコード データのプレフィックスです。 `_i`はインデックス データのプレフィックスです。
-   リージョン`102` 、 `START_KEY` 、および`END_KEY`では、 `[-inf, 20000)`の範囲内のstorageデータが格納されます。同様に、領域 ( `106` 、 `110` 、 `114` 、 `3` ) におけるデータ格納範囲も計算できます。
-   リージョン`98`にはインデックスデータが格納されます。テーブル t のインデックスデータの開始キーは`t_43_i`であり、これはリージョン`98`の範囲内にあります。

ストア1のテーブルtに対応するリージョンを確認するには、 `WHERE`句を使用します。

```sql
test> SHOW TABLE t REGIONS WHERE leader_store_id =1;
+-----------+-----------+---------+-----------+-----------------+--------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
| REGION_ID | START_KEY | END_KEY | LEADER_ID | LEADER_STORE_ID | PEERS        | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS | SCHEDULING_CONSTRAINTS | SCHEDULING_STATE |
+-----------+-----------+---------+-----------+-----------------+--------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
| 98        | t_43_     | t_43_r  | 99        | 1               | 99, 100, 101 | 0          | 0             | 0          | 1                    | 0                |                        |                  |
+-----------+-----------+---------+-----------+-----------------+--------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
```

`SPLIT TABLE REGION`を使用して、インデックス データを領域に分割します。次の例では、テーブル t のインデックス データ`name`が`[a,z]`の範囲内の 2 つの領域に分割されます。

```sql
test> SPLIT TABLE t INDEX name BETWEEN ("a") AND ("z") REGIONS 2;
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
| 2                  | 1.0                  |
+--------------------+----------------------+
1 row in set
```

テーブル t は 7 つの領域に対応しています。そのうち 5 つ ( `102` 、 `106` 、 `110` 、 `114` 、 `3` ) にはテーブル t のレコード データが格納され、残りの 2 つ ( `135` 、 `98` ) にはインデックス データ`name`格納されます。

```sql
test> SHOW TABLE t REGIONS;
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

## MySQLとの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文に対するTiDBの拡張機能です。

## 関連項目 {#see-also}

-   [分割領域](/sql-statements/sql-statement-split-region.md)
-   [テーブルを作成する](/sql-statements/sql-statement-create-table.md)
