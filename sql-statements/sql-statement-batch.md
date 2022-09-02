---
title: BATCH
summary: An overview of the usage of BATCH for the TiDB database.
---

# バッチ {#batch}

`BATCH`構文は、実行のために DML ステートメントを TiDB の複数のステートメントに分割します。これは、トランザクションの原子性と分離が**保証されないこと**を意味します。したがって、これは「非トランザクション」ステートメントです。

現在、 `BATCH`では`DELETE`のみがサポートされています。

`BATCH`構文は、列に基づいて、DML ステートメントを複数の実行範囲に分割します。各範囲で、単一の SQL ステートメントが実行されます。

使用方法と制限事項については、 [非トランザクション DML ステートメント](/non-transactional-dml.md)を参照してください。

## あらすじ {#synopsis}

```ebnf+diagram
NonTransactionalDeleteStmt ::=
    'BATCH' ( 'ON' ColumnName )? 'LIMIT' NUM DryRunOptions? DeleteFromStmt

DryRunOptions ::=
    'DRY' 'RUN' 'QUERY'?
```

## MySQL の互換性 {#mysql-compatibility}

`BATCH`構文は TiDB 固有であり、MySQL と互換性がありません。

## こちらもご覧ください {#see-also}

-   [非トランザクション DML ステートメント](/non-transactional-dml.md)
