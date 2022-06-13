---
title: SHUTDOWN
summary: An overview of the usage of SHUTDOWN for the TiDB database.
---

# シャットダウン {#shutdown}

`SHUTDOWN`ステートメントは、TiDBでシャットダウン操作を実行するために使用されます。 `SHUTDOWN`ステートメントを実行するには、ユーザーが`SHUTDOWN privilege`を持っている必要があります。

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
> TiDBは分散データベースであるため、TiDBでのシャットダウン操作は、TiDBクラスタ全体ではなく、クライアントに接続されたTiDBインスタンスを停止します。

`SHUTDOWN`ステートメントはMySQLと部分的に互換性があります。互換性の問題が発生した場合は、問題を報告できます[GitHubで](https://github.com/pingcap/tidb/issues/new/choose) 。
