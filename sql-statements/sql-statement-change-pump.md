---
title: CHANGE PUMP
summary: An overview of the usage of CHANGE PUMP for the TiDB database.
---

# ポンプの交換 {#change-pump}

`CHANGE PUMP`ステートメントは、クラスター内のPumpのステータス情報を変更します。

> **ヒント：**
>
> ポンプの状態は、運転中に自動的に PD に報告されます。Pumpが異常な状態にあり、その状態が PD に格納されている状態情報と一致しない場合にのみ、 `CHANGE PUMP`ステートメントを使用して PD に格納されている状態情報を変更できます。

## 例 {#examples}

{{< copyable "" >}}

```sql
SHOW PUMP STATUS;
```

```sql
+--------|----------------|--------|--------------------|---------------------|
| NodeID |     Address    | State  |   Max_Commit_Ts    |    Update_Time      |
+--------|----------------|--------|--------------------|---------------------|
| pump1  | 127.0.0.1:8250 | Online | 408553768673342237 | 2019-04-30 00:00:01 |
+--------|----------------|--------|--------------------|---------------------|
| pump2  | 127.0.0.2:8250 | Online | 408553768673342335 | 2019-05-01 00:00:02 |
+--------|----------------|--------|--------------------|---------------------|
2 rows in set (0.00 sec)
```

pump1 の状態が 1 日以上更新されていないことがわかります。Pumpは異常な状態ですが、 `State` `Online`のままです。 `CHANGE PUMP`使用した後、ポンプの`State` &#39;paused&#39; に変更されます。

{{< copyable "" >}}

```sql
CHANGE PUMP TO NODE_STATE ='paused' FOR NODE_ID 'pump1';
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

{{< copyable "" >}}

```sql
SHOW PUMP STATUS;
```

```sql
+--------|----------------|--------|--------------------|---------------------|
| NodeID |     Address    | State  |   Max_Commit_Ts    |    Update_Time      |
+--------|----------------|--------|--------------------|---------------------|
| pump1  | 127.0.0.1:8250 | Paused | 408553768673342237 | 2019-04-30 00:00:01 |
+--------|----------------|--------|--------------------|---------------------|
| pump2  | 127.0.0.2:8250 | Online | 408553768673342335 | 2019-05-01 00:00:02 |
+--------|----------------|--------|--------------------|---------------------|
2 rows in set (0.00 sec)
```

## MySQL の互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## こちらもご覧ください {#see-also}

-   [ポンプの状態を表示](/sql-statements/sql-statement-show-pump-status.md)
-   [ドレイナーのステータスを表示](/sql-statements/sql-statement-show-drainer-status.md)
-   [ドレイナーステータスの変更](/sql-statements/sql-statement-change-drainer.md)
