---
title: TIFLASH_REPLICA
summary: TIFLASH_REPLICA` INFORMATION_SCHEMA テーブルについて学習します。
---

# TIFLASH_レプリカ {#tiflash-replica}

`TIFLASH_REPLICA`表には、利用可能なTiFlashレプリカに関する情報が示されています。

```sql
USE INFORMATION_SCHEMA;
DESC TIFLASH_REPLICA;
```

出力は次のようになります。

```sql
+-----------------+-------------+------+------+---------+-------+
| Field           | Type        | Null | Key  | Default | Extra |
+-----------------+-------------+------+------+---------+-------+
| TABLE_SCHEMA    | varchar(64) | YES  |      | NULL    |       |
| TABLE_NAME      | varchar(64) | YES  |      | NULL    |       |
| TABLE_ID        | bigint(21)  | YES  |      | NULL    |       |
| REPLICA_COUNT   | bigint(64)  | YES  |      | NULL    |       |
| LOCATION_LABELS | varchar(64) | YES  |      | NULL    |       |
| AVAILABLE       | tinyint(1)  | YES  |      | NULL    |       |
| PROGRESS        | double      | YES  |      | NULL    |       |
+-----------------+-------------+------+------+---------+-------+
7 rows in set (0.01 sec)
```

`TIFLASH_REPLICA`テーブル内のフィールドは次のように説明されます。

-   `TABLE_SCHEMA` : テーブルが属するデータベースの名前。
-   `TABLE_NAME` : テーブルの名前。
-   `TABLE_ID` : テーブルの内部 ID。TiDB クラスター内で一意です。
-   `REPLICA_COUNT` : TiFlashレプリカの数。
-   `LOCATION_LABELS` : TiFlashレプリカが作成されるときに設定される LocationLabelList。
-   `AVAILABLE` : テーブルのTiFlashレプリカが利用可能かどうかを示します。値が`1` （利用可能）の場合、TiDB オプティマイザーはクエリコストに基づいて、クエリを TiKV またはTiFlashにプッシュダウンするかをインテリジェントに選択します。値が`0` （利用不可）の場合、TiDB はクエリをTiFlashにプッシュダウンしません。このフィールドの値が`1` （利用可能）になると、それ以上変化しなくなります。
-   `PROGRESS` : TiFlashレプリカのレプリケーションの進行状況。小数点以下2桁の精度で分単位です。このフィールドのスコープは`[0, 1]`です。4 `AVAILABLE`が`1`で`PROGRESS` 1未満の場合、 TiFlashレプリカはTiKVより大幅に遅れており、データレプリケーションの待機タイムアウトにより、 TiFlashにプッシュダウンされたクエリは失敗する可能性があります。
