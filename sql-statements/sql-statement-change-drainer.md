---
title: CHANGE DRAINER
summary: An overview of the usage of CHANGE DRAINER for the TiDB database.
---

# チェンジドレイナー {#change-drainer}

`CHANGE DRAINER`ステートメントは、クラスター内のDrainerのステータス情報を変更します。

> **ヒント：**
>
> 実行中、Drainer の状態が自動的に PD に報告されます。 Drainerが異常な状況にあり、その状態が PD に格納されている状態情報と一致しない場合にのみ、 `CHANGE DRAINER`ステートメントを使用して PD に格納されている状態情報を変更できます。

## 例 {#examples}

{{< copyable "" >}}

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

Drainer1 の状態が 1 日以上更新されていないことがわかります。Drainerは異常な状態にありますが、 `State` `Online`のままです。 `CHANGE DRAINER`使用した後、Drainer の`State` 「一時停止」に変更されます。

{{< copyable "" >}}

```sql
CHANGE DRAINER TO NODE_STATE ='paused' FOR NODE_ID 'drainer1';
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

{{< copyable "" >}}

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

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [<a href="/sql-statements/sql-statement-show-pump-status.md">ポンプのステータスを表示</a>](/sql-statements/sql-statement-show-pump-status.md)
-   [<a href="/sql-statements/sql-statement-show-drainer-status.md">ドレイナーステータスを表示</a>](/sql-statements/sql-statement-show-drainer-status.md)
-   [<a href="/sql-statements/sql-statement-change-pump.md">ポンプステータスの変更</a>](/sql-statements/sql-statement-change-pump.md)
