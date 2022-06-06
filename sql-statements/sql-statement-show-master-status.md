---
title: SHOW MASTER STATUS
summary: An overview of the usage of SHOW MASTER STATUS for the TiDB database.
---

# マスターステータスを表示 {#show-master-status}

`SHOW MASTER STATUS`ステートメントは、クラスタの最新のTSOを表示します。

## 例 {#examples}

{{< copyable "" >}}

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

## MySQLの互換性 {#mysql-compatibility}

`SHOW MASTER STATUS`の出力は、MySQLと一致するように設計されています。ただし、実行結果は、MySQLの結果がbinlogの場所情報であり、TiDBの結果が最新のTSO情報であるという点で異なります。

## も参照してください {#see-also}

-   [ポンプステータスを表示](/sql-statements/sql-statement-show-pump-status.md)
-   [ドレイナーステータスを表示](/sql-statements/sql-statement-show-drainer-status.md)
-   [ポンプステータスの変更](/sql-statements/sql-statement-change-pump.md)
-   [ドレイナーステータスの変更](/sql-statements/sql-statement-change-drainer.md)
