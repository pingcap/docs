---
title: SHOW TABLE REGIONS
summary: Learn how to use SHOW TABLE REGIONS in TiDB.
---

# テーブルの地域を表示する {#show-table-regions}

`SHOW TABLE REGIONS`ステートメントは、TiDBのテーブルのリージョン情報を表示するために使用されます。

## 構文 {#syntax}

```sql
SHOW TABLE [table_name] REGIONS [WhereClauseOptional];
SHOW TABLE [table_name] INDEX [index_name] REGIONS [WhereClauseOptional];
```

## あらすじ {#synopsis}

**ShowTableRegionStmt：**

![ShowTableRegionStmt](/media/sqlgram/ShowTableRegionStmt.png)

**TableName：**

![TableName](/media/sqlgram/TableName.png)

**PartitionNameListOpt：**

![PartitionNameListOpt](/media/sqlgram/PartitionNameListOpt.png)

**WhereClauseOptional：**

![WhereClauseOptional](/media/sqlgram/WhereClauseOptional.png)

**WhereClause：**

![WhereClause](/media/sqlgram/WhereClause.png)

`SHOW TABLE REGIONS`を実行すると、次の列が返されます。

-   `REGION_ID` ：リージョンID。
-   `START_KEY` ：リージョンの開始キー。
-   `END_KEY` ：リージョンのエンドキー。
-   `LEADER_ID` ：リージョンのリーダーID。
-   `LEADER_STORE_ID` ：リージョンリーダーが配置されているストア（TiKV）のID。
-   `PEERS` ：すべてのリージョンレプリカのID。
-   `SCATTERING` ：リージョンがスケジュールされているかどうか。 `1`は真を意味します。
-   `WRITTEN_BYTES` ：1心拍サイクル内にリージョンに書き込まれるデータの推定量。単位はバイトです。
-   `READ_BYTES` ：1心拍サイクル内にリージョンから読み取られたデータの推定量。単位はバイトです。
-   `APPROXIMATE_SIZE(MB)` ：リージョン内の推定データ量。単位はメガバイト（MB）です。
-   `APPROXIMATE_KEYS` ：リージョン内のキーの推定数。

> **ノート：**
>
> `WRITTEN_BYTES`の`READ_BYTES`は`APPROXIMATE_KEYS`なデータではありませ`APPROXIMATE_SIZE(MB)` 。これらは、PDが地域から受信する心拍情報に基づいてPDから推定されたデータです。

## 例 {#examples}

いくつかのリージョンを満たすのに十分なデータを含むサンプルテーブルを作成します。

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

出力には、テーブルがリージョンに分割されていることが示されます。 `REGION_ID` 、および`START_KEY`は正確に一致しない場合があり`END_KEY` 。

```sql
...
mysql> SHOW TABLE t1 REGIONS;
+-----------+--------------+--------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+
| REGION_ID | START_KEY    | END_KEY      | LEADER_ID | LEADER_STORE_ID | PEERS | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS |
+-----------+--------------+--------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+
|        94 | t_75_        | t_75_r_31717 |        95 |               1 | 95    |          0 |             0 |          0 |                  112 |           207465 |
|        96 | t_75_r_31717 | t_75_r_63434 |        97 |               1 | 97    |          0 |             0 |          0 |                   97 |                0 |
|         2 | t_75_r_63434 |              |         3 |               1 | 3     |          0 |     269323514 |   66346110 |                  245 |           162020 |
+-----------+--------------+--------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+
3 rows in set (0.00 sec)
```

上記の`START_KEY`では、 `t_75_r_31717`および`END_KEY`は、 `63434` KEYが`31717`のデータがこのリージョンに保管されていることを示してい`t_75_r_63434` 。プレフィックス`t_75_`は、これが内部テーブルIDが`75`のテーブル（ `t` ）のリージョンであることを示します。 `START_KEY`または`END_KEY`の空のキー値は、それぞれ負の無限大または正の無限大を示します。

TiDBは、必要に応じてリージョンを自動的にリバランスします。手動でリバランスするには、次の`SPLIT TABLE REGION`のステートメントを使用します。

```sql
mysql> SPLIT TABLE t1 BETWEEN (31717) AND (63434) REGIONS 2;
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
|                  1 |                    1 |
+--------------------+----------------------+
1 row in set (42.34 sec)

mysql> SHOW TABLE t1 REGIONS;
+-----------+--------------+--------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+
| REGION_ID | START_KEY    | END_KEY      | LEADER_ID | LEADER_STORE_ID | PEERS | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS |
+-----------+--------------+--------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+
|        94 | t_75_        | t_75_r_31717 |        95 |               1 | 95    |          0 |             0 |          0 |                  112 |           207465 |
|        98 | t_75_r_31717 | t_75_r_47575 |        99 |               1 | 99    |          0 |          1325 |          0 |                   53 |            12052 |
|        96 | t_75_r_47575 | t_75_r_63434 |        97 |               1 | 97    |          0 |          1526 |          0 |                   48 |                0 |
|         2 | t_75_r_63434 |              |         3 |               1 | 3     |          0 |             0 |   55752049 |                   60 |                0 |
+-----------+--------------+--------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+
4 rows in set (0.00 sec)
```

上記の出力は、リージョン96が分割され、新しいリージョン98が作成されたことを示しています。テーブル内の残りのリージョンは、分割操作の影響を受けませんでした。これは、出力統計によって確認されます。

-   `TOTAL_SPLIT_REGION`は、新しく分割されたリージョンの数を示します。この例では、番号は1です。
-   `SCATTER_FINISH_RATIO`は、新しく分割されたリージョンが正常に分散される割合を示します。 `1.0`は、すべてのリージョンが分散していることを意味します。

より詳細な例については：

```sql
mysql> show table t regions;
+-----------+--------------+--------------+-----------+-----------------+---------------+------------+---------------+------------+----------------------+------------------+
| REGION_ID | START_KEY    | END_KEY      | LEADER_ID | LEADER_STORE_ID | PEERS         | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS |
+-----------+--------------+--------------+-----------+-----------------+---------------+------------+---------------+------------+----------------------+------------------+
| 102       | t_43_r       | t_43_r_20000 | 118       | 7               | 105, 118, 119 | 0          | 0             | 0          | 1                    | 0                |
| 106       | t_43_r_20000 | t_43_r_40000 | 120       | 7               | 107, 108, 120 | 0          | 23            | 0          | 1                    | 0                |
| 110       | t_43_r_40000 | t_43_r_60000 | 112       | 9               | 112, 113, 121 | 0          | 0             | 0          | 1                    | 0                |
| 114       | t_43_r_60000 | t_43_r_80000 | 122       | 7               | 115, 122, 123 | 0          | 35            | 0          | 1                    | 0                |
| 3         | t_43_r_80000 |              | 93        | 8               | 5, 73, 93     | 0          | 0             | 0          | 1                    | 0                |
| 98        | t_43_        | t_43_r       | 99        | 1               | 99, 100, 101  | 0          | 0             | 0          | 1                    | 0                |
+-----------+--------------+--------------+-----------+-----------------+---------------+------------+---------------+------------+----------------------+------------------+
6 rows in set
```

上記の例では：

-   表tは6つの地域に対応しています。これらのリージョンでは、 `102` 、および`106`が行データを`3`し、 `114`が`98`データを格納し`110` 。
-   リージョン`102`の`START_KEY`と`END_KEY`の場合、 `t_43`はテーブルプレフィックスとIDを示します。 `_r`は、テーブルtのレコードデータのプレフィックスです。 `_i`はインデックスデータのプレフィックスです。
-   リージョン`102` 、および`START_KEY`は、 `[-inf, 20000)`の範囲のレコード・データが保管されることを意味し`END_KEY` 。同様に、 `110` （ `106` ）の`3` `114`の範囲も計算できます。
-   リージョン`98`はインデックスデータを格納します。テーブルtのインデックスデータの開始キーは`t_43_i`であり、これはリージョン`98`の範囲内にあります。

ストア1のテーブルtに対応するリージョンを確認するには、 `WHERE`節を使用します。

```sql
test> show table t regions where leader_store_id =1;
+-----------+-----------+---------+-----------+-----------------+--------------+------------+---------------+------------+----------------------+------------------+
| REGION_ID | START_KEY | END_KEY | LEADER_ID | LEADER_STORE_ID | PEERS        | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS |
+-----------+-----------+---------+-----------+-----------------+--------------+------------+---------------+------------+----------------------+------------------+
| 98        | t_43_     | t_43_r  | 99        | 1               | 99, 100, 101 | 0          | 0             | 0          | 1                    | 0                |
+-----------+-----------+---------+-----------+-----------------+--------------+------------+---------------+------------+----------------------+------------------+
```

`SPLIT TABLE REGION`を使用して、インデックスデータをリージョンに分割します。次の例では、テーブルtのインデックスデータ`name`が`[a,z]`の範囲の2つのリージョンに分割されています。

```sql
test> split table t index name between ("a") and ("z") regions 2;
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
| 2                  | 1.0                  |
+--------------------+----------------------+
1 row in set
```

これで、テーブルtは7つのリージョンに対応します。それらのうちの`106` `110` （ `102` ）はテーブルtのレコードデータを格納し、別の`135`つ（ `114` ）は`98`データ`3`を`name`します。

```sql
test> show table t regions;
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------+------------+---------------+------------+----------------------+------------------+
| REGION_ID | START_KEY                   | END_KEY                     | LEADER_ID | LEADER_STORE_ID | PEERS         | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS |
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------+------------+---------------+------------+----------------------+------------------+
| 102       | t_43_r                      | t_43_r_20000                | 118       | 7               | 105, 118, 119 | 0          | 0             | 0          | 1                    | 0                |
| 106       | t_43_r_20000                | t_43_r_40000                | 120       | 7               | 108, 120, 126 | 0          | 0             | 0          | 1                    | 0                |
| 110       | t_43_r_40000                | t_43_r_60000                | 112       | 9               | 112, 113, 121 | 0          | 0             | 0          | 1                    | 0                |
| 114       | t_43_r_60000                | t_43_r_80000                | 122       | 7               | 115, 122, 123 | 0          | 35            | 0          | 1                    | 0                |
| 3         | t_43_r_80000                |                             | 93        | 8               | 73, 93, 128   | 0          | 0             | 0          | 1                    | 0                |
| 135       | t_43_i_1_                   | t_43_i_1_016d80000000000000 | 139       | 2               | 138, 139, 140 | 0          | 35            | 0          | 1                    | 0                |
| 98        | t_43_i_1_016d80000000000000 | t_43_r                      | 99        | 1               | 99, 100, 101  | 0          | 0             | 0          | 1                    | 0                |
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------+------------+---------------+------------+----------------------+------------------+
7 rows in set
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文のTiDB拡張です。

## も参照してください {#see-also}

-   [スプリットリージョン](/sql-statements/sql-statement-split-region.md)
-   [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
