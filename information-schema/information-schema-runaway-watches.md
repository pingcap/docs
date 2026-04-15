---
title: RUNAWAY_WATCHES
summary: RUNAWAY_WATCHES` INFORMATION_SCHEMA テーブルについて学習してください。
---

# ランナウェイ・ウォッチズ {#runaway-watches}

`RUNAWAY_WATCHES`表には、想定よりも多くのリソースを消費する暴走クエリの監視リストが表示されます。詳細については、 [暴走クエリ](/tidb-resource-control-runaway-queries.md)参照してください。

> **注記：**
>
> このテーブルは、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスでは利用できません。

```sql
USE INFORMATION_SCHEMA;
DESC RUNAWAY_WATCHES;
```

```sql
+---------------------+--------------+------+------+---------+-------+
| Field               | Type         | Null | Key  | Default | Extra |
+---------------------+--------------+------+------+---------+-------+
| ID                  | bigint(64)   | NO   |      | NULL    |       |
| RESOURCE_GROUP_NAME | varchar(32)  | NO   |      | NULL    |       |
| START_TIME          | varchar(32)  | NO   |      | NULL    |       |
| END_TIME            | varchar(32)  | YES  |      | NULL    |       |
| WATCH               | varchar(12)  | NO   |      | NULL    |       |
| WATCH_TEXT          | text         | NO   |      | NULL    |       |
| SOURCE              | varchar(128) | NO   |      | NULL    |       |
| ACTION              | varchar(12)  | NO   |      | NULL    |       |
| RULE                | varchar(128) | NO   |      | NULL    |       |
+---------------------+--------------+------+------+---------+-------+
9 rows in set (0.00 sec)
```

## 例 {#examples}

暴走クエリの監視リストを照会する：

```sql
SELECT * FROM INFORMATION_SCHEMA.RUNAWAY_WATCHES ORDER BY id\G
```

出力は以下のとおりです。

```sql
*************************** 1. row ***************************
                 ID: 1
RESOURCE_GROUP_NAME: default
         START_TIME: 2024-09-11 07:20:48
           END_TIME: 2024-09-11 07:30:48
              WATCH: Exact
         WATCH_TEXT: select count(*) from `tpch1`.`supplier`
             SOURCE: 127.0.0.1:4000
             ACTION: Kill
               RULE: ProcessedKeys = 10000(100)
*************************** 2. row ***************************
                 ID: 2
RESOURCE_GROUP_NAME: default
         START_TIME: 2024-09-11 07:20:51
           END_TIME: 2024-09-11 07:30:51
              WATCH: Exact
         WATCH_TEXT: select count(*) from `tpch1`.`partsupp`
             SOURCE: 127.0.0.1:4000
             ACTION: Kill
               RULE: RequestUnit = RRU:143.369959, WRU:0.000000, WaitDuration:0s(10)
*************************** 3. row ***************************
                 ID: 3
RESOURCE_GROUP_NAME: default
         START_TIME: 2024-09-11 07:21:16
           END_TIME: 2024-09-11 07:31:16
              WATCH: Exact
         WATCH_TEXT: select sleep(2) from t
             SOURCE: 127.0.0.1:4000
             ACTION: Kill
               RULE: ElapsedTime = 2024-09-11T15:21:16+08:00(2024-09-11T15:21:16+08:00)
3 rows in set (0.00 sec)
```

リソースグループ`rg1`に監視アイテムをリストに追加します。

```sql
QUERY WATCH ADD RESOURCE GROUP rg1 SQL TEXT EXACT TO 'select * from sbtest.sbtest1';
```

暴走クエリの監視リストを再度照会します。

```sql
SELECT * FROM INFORMATION_SCHEMA.RUNAWAY_WATCHES\G
```

出力は以下のとおりです。

```sql
*************************** 1. row ***************************
                 ID: 1
RESOURCE_GROUP_NAME: default
         START_TIME: 2024-09-11 07:20:48
           END_TIME: 2024-09-11 07:30:48
              WATCH: Exact
         WATCH_TEXT: select count(*) from `tpch1`.`supplier`
             SOURCE: 127.0.0.1:4000
             ACTION: Kill
               RULE: ProcessedKeys = 10000(100)
*************************** 2. row ***************************
                 ID: 2
RESOURCE_GROUP_NAME: default
         START_TIME: 2024-09-11 07:20:51
           END_TIME: 2024-09-11 07:30:51
              WATCH: Exact
         WATCH_TEXT: select count(*) from `tpch1`.`partsupp`
             SOURCE: 127.0.0.1:4000
             ACTION: Kill
               RULE: RequestUnit = RRU:143.369959, WRU:0.000000, WaitDuration:0s(10)
*************************** 3. row ***************************
                 ID: 3
RESOURCE_GROUP_NAME: default
         START_TIME: 2024-09-11 07:21:16
           END_TIME: 2024-09-11 07:31:16
              WATCH: Exact
         WATCH_TEXT: select sleep(2) from t
             SOURCE: 127.0.0.1:4000
             ACTION: Kill
               RULE: ElapsedTime = 2024-09-11T15:21:16+08:00(2024-09-11T15:21:16+08:00)
*************************** 4. row ***************************
                 ID: 4
RESOURCE_GROUP_NAME: default
         START_TIME: 2024-09-11 07:23:10
           END_TIME: UNLIMITED
              WATCH: Exact
         WATCH_TEXT: select * from sbtest.sbtest1
             SOURCE: manual
             ACTION: Kill
               RULE: None
3 row in set (0.00 sec)
```

`RUNAWAY_WATCHES`テーブルの各列フィールドの意味は次のとおりです。

-   `ID` : ウォッチアイテムのID。
-   `RESOURCE_GROUP_NAME` : リソース グループの名前。
-   `START_TIME` : 開始時刻。
-   `END_TIME` ：終了時刻。 `UNLIMITED`は、ウォッチアイテムの有効期間が無制限であることを意味します。
-   `WATCH` : クイック識別のマッチタイプ。値は次のとおりです。
    -   `Plan`は、プランダイジェストが一致したことを示します。この場合、 `WATCH_TEXT`列にプランダイジェストが表示されます。
    -   `Similar`は、SQL ダイジェストが一致したことを示します。この場合、 `WATCH_TEXT`列に SQL ダイジェストが表示されます。
    -   `Exact`は、SQLテキストが一致したことを示します。この場合、 `WATCH_TEXT`列にSQLテキストが表示されます。
-   `SOURCE` ：監視対象アイテムの発生源。 `QUERY_LIMIT`ルールによって識別された場合は、識別されたTiDB IPアドレスが表示されます。手動で追加された場合は、 `manual`が表示されます。
-   `ACTION` : 識別後の対応する操作。
-   `RULE` : 識別ルール。現在の 3 つのルールは`ElapsedTime` 、 `ProcessedKeys` 、および`RequestUnit`です。形式は`ProcessedKeys = 666(10)`で、 `666`は実際の値、 `10`はしきい値です。
