---
title: TIFLASH_REPLICA
summary: Learn the `TIFLASH_REPLICA` INFORMATION_SCHEMA table.
---

# TIFLASH_レプリカ {#tiflash-replica}

表`TIFLASH_REPLICA`は、利用可能なTiFlashレプリカに関する情報を示します。

```sql
USE INFORMATION_SCHEMA;
DESC TIFLASH_REPLICA;
```

出力は次のとおりです。

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

`TIFLASH_REPLICA`テーブルのフィールドは次のように説明されています。

-   `TABLE_SCHEMA` : テーブルが属するデータベースの名前。
-   `TABLE_NAME` : テーブルの名前。
-   `TABLE_ID` : テーブルの内部 ID。TiDB クラスター内で一意です。
-   `REPLICA_COUNT` : TiFlashレプリカの数。
-   `LOCATION_LABELS` : TiFlashレプリカの作成時に設定される LocationLabelList。
-   `AVAILABLE` : テーブルのTiFlashレプリカが使用可能かどうかを示します。値が`1` (使用可能) の場合、TiDB オプティマイザーはクエリ コストに基づいてクエリを TiKV またはTiFlashにプッシュダウンすることをインテリジェントに選択できます。値が`0` (使用不可) の場合、TiDB はクエリをTiFlashにプッシュダウンしません。このフィールドの値が`1` (使用可能) になると、それ以上変更されなくなります。
-   `PROGRESS` : TiFlashレプリカのレプリケーションの進行状況。小数点以下 2 桁までの精度で、分レベルで表示されます。このフィールドの範囲は`[0, 1]`です。 `AVAILABLE`フィールドが`1`で、 `PROGRESS`が 1 未満の場合、 TiFlashレプリカは TiKV よりもはるかに遅れており、 TiFlashにプッシュダウンされたクエリは、データ レプリケーションの待機のタイムアウトが原因で失敗する可能性があります。
