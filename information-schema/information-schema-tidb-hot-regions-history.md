---
title: TIDB_HOT_REGIONS_HISTORY
summary: TIDB_HOT_REGIONS_HISTORY`情報スキーマテーブルについて学習してください。
---

# TIDB_ホットリージョン履歴 {#tidb-hot-regions-history}

`TIDB_HOT_REGIONS_HISTORY`テーブルは、PD によって定期的にローカルに記録される履歴ホット領域に関する情報を提供します。

> **注記：**
>
> このテーブルは、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスでは利用できません。

<CustomContent platform="tidb">

記録間隔は[`hot-regions-write-interval`](/pd-configuration-file.md#hot-regions-write-interval-new-in-v540)を設定することで指定できます。デフォルト値は 10 分です。ホット リージョンの履歴情報を保持する期間は[`hot-regions-reserved-days`](/pd-configuration-file.md#hot-regions-reserved-days-new-in-v540)を設定することで指定できます。デフォルト値は 7 日です。詳細は、 [PD設定ファイルの説明](/pd-configuration-file.md#hot-regions-write-interval-new-in-v540)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

デフォルトでは、記録間隔は10分で、ホットスポットに関する履歴情報を保持する期間は7日間です。

</CustomContent>

```sql
USE information_schema;
DESC tidb_hot_regions_history;
```

```sql
+-------------+--------------+------+------+---------+-------+
| Field       | Type         | Null | Key  | Default | Extra |
+-------------+--------------+------+------+---------+-------+
| UPDATE_TIME | timestamp(6) | YES  |      | NULL    |       |
| DB_NAME     | varchar(64)  | YES  |      | NULL    |       |
| TABLE_NAME  | varchar(64)  | YES  |      | NULL    |       |
| TABLE_ID    | bigint(21)   | YES  |      | NULL    |       |
| INDEX_NAME  | varchar(64)  | YES  |      | NULL    |       |
| INDEX_ID    | bigint(21)   | YES  |      | NULL    |       |
| REGION_ID   | bigint(21)   | YES  |      | NULL    |       |
| STORE_ID    | bigint(21)   | YES  |      | NULL    |       |
| PEER_ID     | bigint(21)   | YES  |      | NULL    |       |
| IS_LEARNER  | tinyint(1)   | NO   |      | 0       |       |
| IS_LEADER   | tinyint(1)   | NO   |      | 0       |       |
| TYPE        | varchar(64)  | YES  |      | NULL    |       |
| HOT_DEGREE  | bigint(21)   | YES  |      | NULL    |       |
| FLOW_BYTES  | double       | YES  |      | NULL    |       |
| KEY_RATE    | double       | YES  |      | NULL    |       |
| QUERY_RATE  | double       | YES  |      | NULL    |       |
+-------------+--------------+------+------+---------+-------+
16 rows in set (0.00 sec)
```

`TIDB_HOT_REGIONS_HISTORY`テーブルのフィールドは、次のように説明されます。

-   UPDATE_TIME: ホットリージョンの更新時間。
-   DB_NAME: ホットリージョンが存在するオブジェクトのデータベース名。
-   TABLE_ID: ホットリージョンが存在するテーブルのID。
-   TABLE_NAME: ホットリージョンが存在するテーブルの名前。
-   INDEX_NAME: ホットリージョンが存在するインデックスの名前。
-   INDEX_ID: ホットリージョンが存在するインデックスのID。
-   REGION_ID: ホットリージョンのID。
-   STORE_ID: ホットリージョンが存在する店舗のID。
-   PEER_ID: ホットリージョンに対応するピアのID。
-   IS_LEARNER: PEERが学習者であるかどうか。
-   IS_LEADER: PEERがLEADERであるかどうか。
-   タイプ: 高温リージョンのタイプ。
-   HOT_DEGREE: 高温リージョンの高温度。
-   FLOW_BYTES:リージョン内で書き込まれたバイト数と読み取られたバイト数。
-   KEY_RATE:リージョン内で書き込まれた鍵と読み取られた鍵の数。
-   QUERY_RATE:リージョン内で書き込まれたクエリと読み込まれたクエリの数。

> **注記：**
>
> `UPDATE_TIME` 、 `REGION_ID` 、 `STORE_ID` 、 `PEER_ID` 、 `IS_LEARNER` 、 `IS_LEADER`および`TYPE`フィールドは、実行のために PD サーバーにプッシュされます。テーブルの使用によるオーバーヘッドを減らすには、検索の時間範囲を指定し、可能な限り多くの条件を指定する必要があります。たとえば、 `select * from tidb_hot_regions_history where store_id = 11 and update_time > '2020-05-18 20:40:00' and update_time < '2020-05-18 21:40:00' and type='write'`のように指定します。

## 一般的なユーザーシナリオ {#common-user-scenarios}

-   特定の期間内のホットな地域を検索します。 `update_time`実際の時間に置き換えてください。

    ```sql
    SELECT * FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00';
    ```

    > **注記：**
    >
    > `UPDATE_TIME`は Unix タイムスタンプもサポートしています。たとえば、 `update_time >TIMESTAMP('2021-08-18 21:40:00')`や`update_time > FROM_UNIXTIME(1629294000.000)`などです。

-   特定の期間内のテーブル内のホットリージョンをクエリします。 `update_time`と`table_name`実際の値に置き換えてください。

    ```SQL
    SELECT * FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00' and TABLE_NAME = 'table_name';
    ```

-   特定の期間におけるホットリージョンの分布を照会します。 `update_time`と`table_name`実際の値に置き換えてください。

    ```sql
    SELECT count(region_id) cnt, store_id FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00' and table_name = 'table_name' GROUP BY STORE_ID ORDER BY cnt DESC;
    ```

-   特定の期間におけるホットLeader領域の分布を照会します。 `update_time`と`table_name`実際の値に置き換えてください。

    ```sql
    SELECT count(region_id) cnt, store_id FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00' and table_name = 'table_name' and is_leader=1 GROUP BY STORE_ID ORDER BY cnt DESC;
    ```

-   特定の期間におけるホットインデックス領域の分布を照会します。 `update_time`と`table_name`実際の値に置き換えてください。

    ```sql
    SELECT count(region_id) cnt, index_name, store_id FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00' and table_name = 'table_name' group by index_name, store_id order by index_name,cnt desc;
    ```

-   特定の期間におけるホットなインデックスLeader領域の分布を照会します。 `update_time`と`table_name`実際の値に置き換えてください。

    ```sql
    SELECT count(region_id) cnt, index_name, store_id FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2022-09-19 00:00:00' and table_name = 'table_name' and is_leader=1 group by index_name, store_id order by index_name,cnt desc;
    ```
