---
title: CHANGE DRAINER
summary: TiDB データベースの CHANGE DRAINER の使用法の概要。
---

# ドレイナーの変更 {#change-drainer}

`CHANGE DRAINER`ステートメントは、クラスター内のDrainerのステータス情報を変更します。

> **注記：**
>
> この機能は TiDB Self-Managed にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では使用できません。

> **ヒント：**
>
> Drainerの状態は実行中に自動的に PD に報告されます。Drainer が異常な状況にあり、その状態が PD に保存されている状態情報と一致しない場合にのみ、 `CHANGE DRAINER`ステートメントを使用して PD に保存されている状態情報を変更できます。

## 例 {#examples}

```sql
SHOW DRAINER STATUS;
```

```sql
+----------|----------------|--------|--------------------|---------------------|
|  NodeID  |     Address    | State  |   Max_Commit_Ts    |    Update_Time      |
+----------|----------------|--------|--------------------|---------------------|
| drainer1 | 127.0.0.3:8249 | Online | 408553768673342532 | 2019-04-30 00:00:03 |
+----------|----------------|--------|--------------------|---------------------|
| drainer2 | 127.0.0.4:8249 | Online | 408553768673345531 | 2019-05-01 00:00:04 |
+----------|----------------|--------|--------------------|---------------------|
2 rows in set (0.00 sec)
```

ドレイナー 1 の状態は 1 日以上更新されていないことがわかります。Drainerは異常な状態ですが、 `State` `Online`ままです。 `CHANGE DRAINER`使用した後、ドレイナーの`State` 「一時停止」に変更されます。

```sql
CHANGE DRAINER TO NODE_STATE ='paused' FOR NODE_ID 'drainer1';
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

```sql
SHOW DRAINER STATUS;
```

```sql
+----------|----------------|--------|--------------------|---------------------|
|  NodeID  |     Address    | State  |   Max_Commit_Ts    |    Update_Time      |
+----------|----------------|--------|--------------------|---------------------|
| drainer1 | 127.0.0.3:8249 | Paused | 408553768673342532 | 2019-04-30 00:00:03 |
+----------|----------------|--------|--------------------|---------------------|
| drainer2 | 127.0.0.4:8249 | Online | 408553768673345531 | 2019-05-01 00:00:04 |
+----------|----------------|--------|--------------------|---------------------|
2 rows in set (0.00 sec)
```

## MySQL 互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [ポンプの状態を表示](/sql-statements/sql-statement-show-pump-status.md)
-   [ドレイナーステータスを表示](/sql-statements/sql-statement-show-drainer-status.md)
-   [ポンプステータスの変更](/sql-statements/sql-statement-change-pump.md)
