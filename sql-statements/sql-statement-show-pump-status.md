---
title: SHOW PUMP STATUS
summary: An overview of the usage of SHOW PUMP STATUS for the TiDB database.
---

# ポンプのステータスを表示 {#show-pump-status}

`SHOW PUMP STATUS`ステートメントは、クラスター内のすべてのPumpノードのステータス情報を表示します。

## 例 {#examples}

{{< copyable "" >}}

```sql
SHOW PUMP STATUS;
```

```sql
+--------|----------------|--------|--------------------|---------------------|
| NodeID |     Address    | State  |   Max_Commit_Ts    |    Update_Time      |
+--------|----------------|--------|--------------------|---------------------|
| pump1  | 127.0.0.1:8250 | Online | 408553768673342237 | 2019-05-01 00:00:01 |
+--------|----------------|--------|--------------------|---------------------|
| pump2  | 127.0.0.2:8250 | Online | 408553768673342335 | 2019-05-01 00:00:02 |
+--------|----------------|--------|--------------------|---------------------|
2 rows in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [<a href="/sql-statements/sql-statement-show-drainer-status.md">ドレイナーステータスを表示</a>](/sql-statements/sql-statement-show-drainer-status.md)
-   [<a href="/sql-statements/sql-statement-change-pump.md">ポンプステータスの変更</a>](/sql-statements/sql-statement-change-pump.md)
-   [<a href="/sql-statements/sql-statement-change-drainer.md">ドレイナーステータスの変更</a>](/sql-statements/sql-statement-change-drainer.md)
