---
title: CHANGE DRAINER
summary: An overview of the usage of CHANGE DRAINER for the TiDB database.
---

# チェンジドレイナー {#change-drainer}

`CHANGE DRAINER`ステートメントは、クラスタのDrainerのステータス情報を変更します。

> **ヒント：**
>
> ドレイナーの状態は、実行中にPDに自動的に報告されます。 Drainerが異常な状況にあり、その状態がPDに格納されている状態情報と矛盾している場合にのみ、 `CHANGE DRAINER`ステートメントを使用してPDに格納されている状態情報を変更できます。

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

ドレイナー1の状態は1日以上更新されておらず、Drainerは異常な状態ですが、 `State`は`Online`のままであることがわかります。 `CHANGE DRAINER`を使用した後、Drainerの`State`は「一時停止」に変更されます。

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

このステートメントは、MySQL構文のTiDB拡張です。

## も参照してください {#see-also}

-   [ポンプステータスを表示](/sql-statements/sql-statement-show-pump-status.md)
-   [ドレイナーステータスを表示](/sql-statements/sql-statement-show-drainer-status.md)
-   [ポンプステータスの変更](/sql-statements/sql-statement-change-pump.md)
