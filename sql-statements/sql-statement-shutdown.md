---
title: SHUTDOWN
summary: An overview of the usage of SHUTDOWN for the TiDB database.
---

# シャットダウン {#shutdown}

`SHUTDOWN`ステートメントは、TiDB でシャットダウン操作を実行するために使用されます。 `SHUTDOWN`ステートメントを実行するには、ユーザーが`SHUTDOWN privilege`を持っている必要があります。

## あらすじ {#synopsis}

**声明：**

![Statement](/media/sqlgram/ShutdownStmt.png)

## 例 {#examples}

{{< copyable "" >}}

```sql
SHUTDOWN;
```

```
Query OK, 0 rows affected (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

> **ノート：**
>
> TiDB は分散データベースであるため、TiDB でのシャットダウン操作は、TiDB クラスター全体ではなく、クライアントに接続された TiDB インスタンスを停止します。

`SHUTDOWN`ステートメントは部分的に MySQL と互換性があります。互換性の問題が発生した場合は、問題を報告できます[<a href="https://github.com/pingcap/tidb/issues/new/choose">GitHub 上で</a>](https://github.com/pingcap/tidb/issues/new/choose) 。
