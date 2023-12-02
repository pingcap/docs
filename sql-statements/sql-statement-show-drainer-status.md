---
title: SHOW DRAINER STATUS
summary: An overview of the usage of SHOW DRAINER STATUS for the TiDB database.
---

# ドレイナーのステータスを表示 {#show-drainer-status}

`SHOW DRAINER STATUS`ステートメントは、クラスター内のすべてのDrainerノードのステータス情報を表示します。

> **注記：**
>
> この機能は TiDB セルフホスト型にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では利用できません。

## 例 {#examples}

```sql
SHOW DRAINER STATUS;
```

```sql
+----------|----------------|--------|--------------------|---------------------|
|  NodeID  |     Address    | State  |   Max_Commit_Ts    |    Update_Time      |
+----------|----------------|--------|--------------------|---------------------|
| drainer1 | 127.0.0.3:8249 | Online | 408553768673342532 | 2019-05-01 00:00:03 |
+----------|----------------|--------|--------------------|---------------------|
| drainer2 | 127.0.0.4:8249 | Online | 408553768673345531 | 2019-05-01 00:00:04 |
+----------|----------------|--------|--------------------|---------------------|
2 rows in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [ポンプのステータスを表示](/sql-statements/sql-statement-show-pump-status.md)
-   [ポンプステータスの変更](/sql-statements/sql-statement-change-pump.md)
-   [ドレイナーステータスの変更](/sql-statements/sql-statement-change-drainer.md)
