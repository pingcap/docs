---
title: SHOW DRAINER STATUS
summary: An overview of the usage of SHOW DRAINER STATUS for the TiDB database.
---

# ドレイナーステータスを表示 {#show-drainer-status}

`SHOW DRAINER STATUS`ステートメントは、クラスタのすべてのDrainerノードのステータス情報を表示します。

## 例 {#examples}

{{< copyable "" >}}

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

このステートメントは、MySQL構文のTiDB拡張です。

## も参照してください {#see-also}

-   [ポンプステータスを表示](/sql-statements/sql-statement-show-pump-status.md)
-   [ポンプステータスの変更](/sql-statements/sql-statement-change-pump.md)
-   [ドレイナーステータスの変更](/sql-statements/sql-statement-change-drainer.md)
