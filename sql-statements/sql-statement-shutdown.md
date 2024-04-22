---
title: SHUTDOWN
summary: TiDBの`SHUTDOWN`ステートメントは、データベースのシャットダウン操作を実行するために使用されます。ユーザーは`SHUTDOWN privilege`を持っている必要があります。この機能はTiDBセルフホスト型にのみ適用され、TiDB Cloudでは利用できません。`SHUTDOWN`ステートメントは部分的にMySQLと互換性があります。TiDBでのシャットダウン操作は、クライアントに接続されたTiDBインスタンスを停止します。
---

# シャットダウン {#shutdown}

`SHUTDOWN`ステートメントは、TiDB でシャットダウン操作を実行するために使用されます。 `SHUTDOWN`ステートメントを実行するには、ユーザーが`SHUTDOWN privilege`を持っている必要があります。

> **注記：**
>
> この機能は TiDB セルフホスト型にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では利用できません。

## あらすじ {#synopsis}

**声明：**

![Statement](/media/sqlgram/ShutdownStmt.png)

## 例 {#examples}

```sql
SHUTDOWN;
```

    Query OK, 0 rows affected (0.00 sec)

## MySQLの互換性 {#mysql-compatibility}

> **注記：**
>
> TiDB は分散データベースであるため、TiDB でのシャットダウン操作は、TiDB クラスター全体ではなく、クライアントに接続された TiDB インスタンスを停止します。

`SHUTDOWN`ステートメントは部分的に MySQL と互換性があります。互換性の問題が発生した場合は、次のことを行うことができます。 [バグを報告](https://docs.pingcap.com/tidb/stable/support) .
