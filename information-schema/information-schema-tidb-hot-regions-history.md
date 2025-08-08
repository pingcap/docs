---
title: TIDB_HOT_REGIONS_HISTORY
summary: TIDB_HOT_REGIONS_HISTORY` information_schema テーブルについて学習します。
---

# TIDB_ホットリージョン履歴 {#tidb-hot-regions-history}

`TIDB_HOT_REGIONS_HISTORY`テーブルは、PD によってローカルに定期的に記録される履歴ホット領域に関する情報を提供します。

> **注記：**
>
> このテーブルは[TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)クラスターでは使用できません。

<CustomContent platform="tidb">

[`hot-regions-write-interval`](/pd-configuration-file.md#hot-regions-write-interval-new-in-v540)設定することで、記録間隔を指定できます。デフォルト値は10分です。3 [`hot-regions-reserved-days`](/pd-configuration-file.md#hot-regions-reserved-days-new-in-v540)設定することで、ホットリージョンの履歴情報を保存する期間を指定できます。デフォルト値は7日間です。詳細は[PD設定ファイルの説明](/pd-configuration-file.md#hot-regions-write-interval-new-in-v540)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

デフォルトでは、記録間隔は 10 分、ホット リージョンの履歴情報を保存しておく期間は 7 日間です。

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

`TIDB_HOT_REGIONS_HISTORY`テーブル内のフィールドは次のように説明されます。

-   UPDATE_TIME: ホットリージョンの更新時刻。
-   DB_NAME: ホットリージョンが配置されているオブジェクトのデータベース名。
-   TABLE_ID: ホットリージョンが配置されているテーブルの ID。
-   TABLE_NAME: ホットリージョンが配置されているテーブルの名前。
-   INDEX_NAME: ホットリージョンが配置されているインデックスの名前。
-   INDEX_ID: ホットリージョンが配置されているインデックスの ID。
-   REGION_ID: ホットリージョンの ID。
-   STORE_ID: ホットリージョンが配置されているストアの ID。
-   PEER_ID: ホットリージョンに対応するピアの ID。
-   IS_LEARNER: PEER が LEARNER であるかどうか。
-   IS_LEADER: PEER が LEADER であるかどうか。
-   TYPE: ホットリージョンのタイプ。
-   HOT_DEGREE: ホットリージョンのホット度。
-   FLOW_BYTES:リージョン内で書き込まれたバイト数と読み取られたバイト数。
-   KEY_RATE:リージョン内で書き込まれ、読み取られたキーの数。
-   QUERY_RATE:リージョン内で書き込まれ、読み取られたクエリの数。

> **注記：**
>
> `UPDATE_TIME` 、 `REGION_ID` 、 `STORE_ID` 、 `PEER_ID` 、 `IS_LEARNER` 、 `IS_LEADER` 、 `TYPE`フィールドは、実行のためにPDサーバーにプッシュダウンされます。テーブル使用によるオーバーヘッドを削減するには、検索の期間を指定し、できるだけ多くの条件を指定する必要があります。例えば、 `select * from tidb_hot_regions_history where store_id = 11 and update_time > '2020-05-18 20:40:00' and update_time < '2020-05-18 21:40:00' and type='write'`です。

## 一般的なユーザーシナリオ {#common-user-scenarios}

-   特定の期間内でホットな地域をクエリします。1 `update_time`実際の時間に置き換えてください。

    ```sql
    SELECT * FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00';
    ```

    > **注記：**
    >
    > `UPDATE_TIME` Unix タイムスタンプもサポートします。たとえば、 `update_time >TIMESTAMP('2021-08-18 21:40:00')`や`update_time > FROM_UNIXTIME(1629294000.000)`です。

-   特定の期間におけるテーブル内の人気地域をクエリします。1と`update_time` `table_name`実際の値に置き換えてください。

    ```SQL
    SELECT * FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00' and TABLE_NAME = 'table_name';
    ```

-   特定の期間におけるホットな地域の分布を照会します。1と`update_time` `table_name`実際の値に置き換えてください。

    ```sql
    SELECT count(region_id) cnt, store_id FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00' and table_name = 'table_name' GROUP BY STORE_ID ORDER BY cnt DESC;
    ```

-   特定の期間における注目のLeader地域の分布を照会します。1と`update_time` `table_name`実際の値に置き換えてください。

    ```sql
    SELECT count(region_id) cnt, store_id FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00' and table_name = 'table_name' and is_leader=1 GROUP BY STORE_ID ORDER BY cnt DESC;
    ```

-   特定の期間におけるホットインデックスリージョンの分布をクエリします。1と`update_time` `table_name`実際の値に置き換えてください。

    ```sql
    SELECT count(region_id) cnt, index_name, store_id FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00' and table_name = 'table_name' group by index_name, store_id order by index_name,cnt desc;
    ```

-   特定の期間における注目のインデックスLeader地域の分布を照会します。1と`update_time` `table_name`実際の値に置き換えてください。

    ```sql
    SELECT count(region_id) cnt, index_name, store_id FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2022-09-19 00:00:00' and table_name = 'table_name' and is_leader=1 group by index_name, store_id order by index_name,cnt desc;
    ```
