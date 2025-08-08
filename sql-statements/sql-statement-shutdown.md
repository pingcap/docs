---
title: SHUTDOWN
summary: TiDB データベースの SHUTDOWN の使用法の概要。
---

# シャットダウン {#shutdown}

`SHUTDOWN`文はTiDBのシャットダウン操作を実行するために使用されます。3 `SHUTDOWN`を実行するには、ユーザーは`SHUTDOWN privilege`必要です。

> **注記：**
>
> この機能は TiDB Self-Managed にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では使用できません。

## 概要 {#synopsis}

```ebnf+diagram
ShutdownStmt ::=
    "SHUTDOWN"
```

## 例 {#examples}

```sql
SHUTDOWN;
```

    Query OK, 0 rows affected (0.00 sec)

## MySQLの互換性 {#mysql-compatibility}

> **注記：**
>
> TiDB は分散データベースであるため、TiDB のシャットダウン操作では、TiDB クラスター全体ではなく、クライアントに接続された TiDB インスタンスが停止されます。

`SHUTDOWN`文はMySQLと部分的に互換性があります。互換性の問題が発生した場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support)実行してください。
