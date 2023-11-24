---
title: SHOW MASTER STATUS
summary: An overview of the usage of SHOW MASTER STATUS for the TiDB database.
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

## MySQLの互換性 {#mysql-compatibility}

`SHOW MASTER STATUS`の出力は MySQL と一致するように設計されています。ただし、実行結果は、MySQL の結果がbinlogの場所情報であり、TiDB の結果が最新の TSO 情報であるという点で異なります。

## こちらも参照 {#see-also}

<CustomContent platform="tidb">

-   [ポンプのステータスを表示](/sql-statements/sql-statement-show-pump-status.md)
-   [ドレイナーのステータスを表示](/sql-statements/sql-statement-show-drainer-status.md)
-   [ポンプステータスの変更](/sql-statements/sql-statement-change-pump.md)
-   [ドレイナーステータスの変更](/sql-statements/sql-statement-change-drainer.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [`SHOW TABLE STATUS`](/sql-statements/sql-statement-show-table-status.md)

</CustomContent>
