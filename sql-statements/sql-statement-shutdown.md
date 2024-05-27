---
title: SHUTDOWN
summary: TiDB データベースの SHUTDOWN の使用法の概要。
---

# シャットダウン {#shutdown}

`SHUTDOWN`ステートメントは`SHUTDOWN` TiDB でシャットダウン操作を実行するために使用されます。3 ステートメントを実行するには、ユーザーが`SHUTDOWN privilege`を持っている必要があります。

> **注記：**
>
> この機能は TiDB Self-Hosted にのみ適用され、 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)では使用できません。

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

## MySQL 互換性 {#mysql-compatibility}

> **注記：**
>
> TiDB は分散データベースであるため、TiDB のシャットダウン操作では、TiDB クラスター全体ではなく、クライアントに接続された TiDB インスタンスが停止されます。

`SHUTDOWN`ステートメントは MySQL と部分的に互換性があります。互換性の問題が発生した場合は、 [バグを報告](https://docs.pingcap.com/tidb/stable/support)実行できます。
