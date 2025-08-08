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

## MySQLの互換性 {#mysql-compatibility}

`SHOW MASTER STATUS`の出力はMySQLと一致するように設計されています。ただし、MySQLの結果はbinlogの位置情報であり、TiDBの結果は最新のTSO情報であるという点で実行結果が異なります。

`SHOW BINARY LOG STATUS`ステートメントは、MySQL 8.2.0 以降のバージョンでは非推奨となっている`SHOW MASTER STATUS`エイリアスとして TiDB に追加されました。
