---
title: SHOW MASTER STATUS
summary: TiDB データベースの SHOW MASTER STATUS の使用法の概要。
---

# マスターステータスを表示 {#show-master-status}

`SHOW MASTER STATUS`ステートメントは、クラスター内の最新の TSO を表示します。

## 例 {#examples}

```sql
SHOW MASTER STATUS;
```

```sql
+-------------+--------------------+--------------+------------------+-------------------+
| File        | Position           | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+-------------+--------------------+--------------+------------------+-------------------+
| tidb-binlog | 416916363252072450 |              |                  |                   |
+-------------+--------------------+--------------+------------------+-------------------+
1 row in set (0.00 sec)
```

## MySQL 互換性 {#mysql-compatibility}

`SHOW MASTER STATUS`の出力はMySQLと一致するように設計されていますが、MySQLの結果はbinlogの位置情報であり、TiDBの結果は最新のTSO情報である点で実行結果が異なります。

`SHOW BINARY LOG STATUS`ステートメントは、MySQL 8.2.0 以降のバージョンでは非推奨となっている`SHOW MASTER STATUS`のエイリアスとして TiDB に追加されました。

## 参照 {#see-also}

<CustomContent platform="tidb">

-   [ポンプの状態を表示](/sql-statements/sql-statement-show-pump-status.md)
-   [ドレイナーステータスを表示](/sql-statements/sql-statement-show-drainer-status.md)
-   [ポンプステータスの変更](/sql-statements/sql-statement-change-pump.md)
-   [ドレイナーステータスの変更](/sql-statements/sql-statement-change-drainer.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [`SHOW TABLE STATUS`](/sql-statements/sql-statement-show-table-status.md)

</CustomContent>
