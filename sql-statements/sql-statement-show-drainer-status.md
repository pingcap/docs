---
title: SHOW DRAINER STATUS
summary: TiDB データベースの SHOW DRAINER STATUS の使用法の概要。
---

# ドレイナーステータスを表示 {#show-drainer-status}

`SHOW DRAINER STATUS`ステートメントは、クラスター内のすべてのDrainerノードのステータス情報を表示します。

> **注記：**
>
> この機能は TiDB Self-Managed にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では使用できません。

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

## MySQL 互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [ポンプの状態を表示](/sql-statements/sql-statement-show-pump-status.md)
-   [ポンプステータスの変更](/sql-statements/sql-statement-change-pump.md)
-   [ドレイナーステータスの変更](/sql-statements/sql-statement-change-drainer.md)
