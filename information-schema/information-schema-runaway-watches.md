---
title: RUNAWAY_WATCHES
summary: RUNAWAY_WATCHES INFORMATION_SCHEMA テーブルについて学習します。
---

# ランナウェイウォッチ {#runaway-watches}

`RUNAWAY_WATCHES`表には、予想よりも多くのリソースを消費するランナウェイ クエリの監視リストが表示されます。詳細については、 [ランナウェイクエリ](/tidb-resource-control.md#manage-queries-that-consume-more-resources-than-expected-runaway-queries)を参照してください。

> **注記：**
>
> このテーブルは[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

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
+---------------------+--------------+------+------+---------+-------+
8 rows in set (0.00 sec)
```

## 例 {#examples}

ランナウェイクエリのウォッチリストをクエリします。

```sql
SELECT * FROM INFORMATION_SCHEMA.RUNAWAY_WATCHES\G
```

出力は次のようになります。

```sql
*************************** 1. row ***************************
                 ID: 20003
RESOURCE_GROUP_NAME: rg2
         START_TIME: 2023-07-28 13:06:08
           END_TIME: UNLIMITED
              WATCH: Similar
         WATCH_TEXT: 5b7fd445c5756a16f910192ad449c02348656a5e9d2aa61615e6049afbc4a82e
             SOURCE: 127.0.0.1:4000
             ACTION: Kill
*************************** 2. row ***************************
                 ID: 16004
RESOURCE_GROUP_NAME: rg2
         START_TIME: 2023-07-28 01:45:30
           END_TIME: UNLIMITED
              WATCH: Similar
         WATCH_TEXT: 3d48fca401d8cbb31a9f29adc9c0f9d4be967ca80a34f59c15f73af94e000c84
             SOURCE: 127.0.0.1:4000
             ACTION: Kill
2 rows in set (0.00 sec)
```

リソース グループ`rg1`のリストに監視項目を追加します。

```sql
QUERY WATCH ADD RESOURCE GROUP rg1 SQL TEXT EXACT TO 'select * from sbtest.sbtest1';
```

ランナウェイ クエリの監視リストを再度クエリします。

```sql
SELECT * FROM INFORMATION_SCHEMA.RUNAWAY_WATCHES\G
```

出力は次のようになります。

```sql
*************************** 1. row ***************************
                 ID: 20003
RESOURCE_GROUP_NAME: rg2
         START_TIME: 2023-07-28 13:06:08
           END_TIME: UNLIMITED
              WATCH: Similar
         WATCH_TEXT: 5b7fd445c5756a16f910192ad449c02348656a5e9d2aa61615e6049afbc4a82e
             SOURCE: 127.0.0.1:4000
             ACTION: Kill
*************************** 2. row ***************************
                 ID: 16004
RESOURCE_GROUP_NAME: rg2
         START_TIME: 2023-07-28 01:45:30
           END_TIME: UNLIMITED
              WATCH: Similar
         WATCH_TEXT: 3d48fca401d8cbb31a9f29adc9c0f9d4be967ca80a34f59c15f73af94e000c84
             SOURCE: 127.0.0.1:4000
             ACTION: Kill
*************************** 3. row ***************************
                 ID: 20004
RESOURCE_GROUP_NAME: rg1
         START_TIME: 2023-07-28 14:23:04
           END_TIME: UNLIMITED
              WATCH: Exact
         WATCH_TEXT: select * from sbtest.sbtest1
             SOURCE: manual
             ACTION: NoneAction
3 row in set (0.00 sec)
```

`RUNAWAY_WATCHES`表の各列フィールドの意味は次のとおりです。

-   `ID` : 監視項目の ID。
-   `RESOURCE_GROUP_NAME` : リソース グループの名前。
-   `START_TIME` : 開始時刻。
-   `END_TIME` : 終了時刻。2 `UNLIMITED` 、監視項目の有効期間が無制限であることを意味します。
-   `WATCH` : クイック識別の一致タイプ。値は次のとおりです。
    -   `Plan` 、プラン ダイジェストが一致していることを示します。この場合、 `WATCH_TEXT`列目にプラン ダイジェストが表示されます。
    -   `Similar` 、SQL ダイジェストが一致したことを示します。この場合、 `WATCH_TEXT`列目に SQL ダイジェストが表示されます。
    -   `Exact` SQL テキストが一致したことを示します。この場合、 `WATCH_TEXT`列目に SQL テキストが表示されます。
-   `SOURCE` : `QUERY_LIMIT`項目のソース。2 ルールで識別された場合は、識別された TiDB IP アドレスが表示されます。手動で追加された場合は、 `manual`が表示されます。
-   `ACTION` : 識別後の対応する操作。
