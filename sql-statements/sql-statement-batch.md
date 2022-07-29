---
title: BATCH
summary: An overview of the usage of BATCH for the TiDB database.
---

# バッチ {#batch}

`BATCH`構文は、DMLステートメントをTiDB内の複数のステートメントに分割して実行します。これは、トランザクションの原子性と分離**の保証がないこと**を意味します。したがって、これは「非トランザクション」ステートメントです。

現在、 `BATCH`でサポートされているのは`DELETE`つだけです。

列に基づいて、 `BATCH`構文はDMLステートメントを実行のためにスコープの複数の範囲に分割します。各範囲で、単一のSQLステートメントが実行されます。

使用法と制限事項の詳細については、 [非トランザクションDMLステートメント](/non-transactional-dml.md)を参照してください。

## あらすじ {#synopsis}

```ebnf+diagram
NonTransactionalDeleteStmt ::=
    'BATCH' ( 'ON' ColumnName )? 'LIMIT' NUM DryRunOptions? DeleteFromStmt

DryRunOptions ::=
    'DRY' 'RUN' 'QUERY'?
```

## MySQLの互換性 {#mysql-compatibility}

`BATCH`構文はTiDB固有であり、MySQLと互換性がありません。

## も参照してください {#see-also}

-   [非トランザクションDMLステートメント](/non-transactional-dml.md)
