---
title: CHANGE PUMP
summary: An overview of the usage of CHANGE PUMP for the TiDB database.
---

# ポンプの交換 {#change-pump}

`CHANGE PUMP`ステートメントは、クラスタのPumpのステータス情報を変更します。

> **ヒント：**
>
> ポンプの状態は、実行中にPDに自動的に報告されます。 Pumpが異常な状況にあり、その状態がPDに格納されている状態情報と矛盾している場合にのみ、 `CHANGE PUMP`ステートメントを使用してPDに格納されている状態情報を変更できます。

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

pump1の状態が1日以上更新されておらず、 Pumpが異常な状態になっていることがわかりますが、 `State`は`Online`のままです。 `CHANGE PUMP`を使用した後、ポンプの`State`は「一時停止」に変更されます。

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

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文のTiDB拡張です。

## も参照してください {#see-also}

-   [ポンプステータスを表示](/sql-statements/sql-statement-show-pump-status.md)
-   [ドレイナーステータスを表示](/sql-statements/sql-statement-show-drainer-status.md)
-   [ドレイナーステータスの変更](/sql-statements/sql-statement-change-drainer.md)
