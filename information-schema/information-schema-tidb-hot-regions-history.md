---
title: TIDB_HOT_REGIONS_HISTORY
summary: Learn the `TIDB_HOT_REGIONS_HISTORY` information_schema table.
---

# TIDB_HOT_REGIONS_HISTORY {#tidb-hot-regions-history}

`TIDB_HOT_REGIONS_HISTORY`の表は、PDによってローカルに定期的に記録される履歴ホットリージョンに関する情報を提供します。

<CustomContent platform="tidb">

[`hot-regions-write-interval`](/pd-configuration-file.md#hot-regions-write-interval-new-in-v540)を設定することにより、レコード間隔を指定できます。デフォルト値は10分です。 [`hot-regions-reserved-days`](/pd-configuration-file.md#hot-regions-reserved-days-new-in-v540)を設定することにより、ホットリージョンに関する履歴情報を予約する期間を指定できます。デフォルト値は7日です。詳細については、 [PD構成ファイルの説明](/pd-configuration-file.md#hot-regions-write-interval-new-in-v540)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

デフォルトでは、記録間隔は10分で、ホットリージョンに関する履歴情報を予約する期間は7日です。

</CustomContent>

{{< copyable "" >}}

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

`TIDB_HOT_REGIONS_HISTORY`表のフィールドは次のように説明されています。

-   UPDATE_TIME：ホットリージョンの更新時間。
-   DB_NAME：ホットリージョンが配置されているオブジェクトのデータベース名。
-   TABLE_ID：ホットリージョンが配置されているテーブルのID。
-   TABLE_NAME：ホットリージョンが配置されているテーブルの名前。
-   INDEX_NAME：ホットリージョンが配置されているインデックスの名前。
-   INDEX_ID：ホットリージョンが配置されているインデックスのID。
-   REGION_ID：ホットリージョンのID。
-   STORE_ID：ホットリージョンが配置されているストアのID。
-   PEER_ID：ホットリージョンに対応するピアのID。
-   IS_LEARNER：PEERがLEARNERであるかどうか。
-   IS_LEADER：PEERがLEADERであるかどうか。
-   TYPE：ホットリージョンのタイプ。
-   HOT_DEGREE：ホットリージョンのホット度。
-   FLOW_BYTES：リージョンで書き込まれ、読み取られたバイト数。
-   KEY_RATE：リージョンで書き込まれ、読み取られるキーの数。
-   QUERY_RATE：リージョンで書き込まれ、読み取られたクエリの数。

> **ノート：**
>
> `UPDATE_TIME` 、 `PEER_ID` `REGION_ID` `IS_LEARNER`は、 `TYPE`のために`IS_LEADER`サーバーにプッシュダウンされ`STORE_ID` 。テーブルを使用するオーバーヘッドを減らすには、検索の時間範囲を指定し、できるだけ多くの条件を指定する必要があります。たとえば、 `select * from tidb_hot_regions_history where store_id = 11 and update_time > '2020-05-18 20:40:00' and update_time < '2020-05-18 21:40:00' and type='write'` 。

## 一般的なユーザーシナリオ {#common-user-scenarios}

-   特定の期間内にホットリージョンをクエリします。 `update_time`を実際の時間に置き換えます。

    {{< copyable "" >}}

    ```sql
    SELECT * FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00';
    ```

    > **ノート：**
    >
    > `UPDATE_TIME`はUnixタイムスタンプもサポートします。たとえば、 `update_time >TIMESTAMP('2021-08-18 21:40:00')`または`update_time > FROM_UNIXTIME(1629294000.000)` 。

-   特定の期間内にテーブル内のホットリージョンをクエリします。 `update_time`と`table_name`を実際の値に置き換えます。

    {{< copyable "" >}}

    ```SQL
    SELECT * FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00' and TABLE_NAME = 'table_name';
    ```

-   特定の期間内のホットリージョンの分布を照会します。 `update_time`と`table_name`を実際の値に置き換えます。

    {{< copyable "" >}}

    ```sql
    SELECT count(region_id) cnt, store_id FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00' and table_name = 'table_name' GROUP BY STORE_ID ORDER BY cnt DESC;
    ```

-   特定の期間内のホットリーダーリージョンの分布を照会します。 `update_time`と`table_name`を実際の値に置き換えます。

    {{< copyable "" >}}

    ```sql
    SELECT count(region_id) cnt, store_id FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00' and table_name = 'table_name' and is_leader=1 GROUP BY STORE_ID ORDER BY cnt DESC;
    ```

-   特定の期間内のホットインデックス領域の分布を照会します。 `update_time`と`table_name`を実際の値に置き換えます。

    {{< copyable "" >}}

    ```sql
    SELECT count(region_id) cnt, index_name, store_id FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00' and table_name = 'table_name' group by index_name, store_id order by index_name,cnt desc;
    ```

-   特定の期間内のホットインデックスリーダーリージョンの分布をクエリします。 `update_time`と`table_name`を実際の値に置き換えます。

    {{< copyable "" >}}

    ```sql
    SELECT count(region_id) cnt, index_name, store_id FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2022-09-19 00:00:00' and table_name = 'table_name' and is_leader=1 group by index_name, store_id order by index_name,cnt desc;
    ```
