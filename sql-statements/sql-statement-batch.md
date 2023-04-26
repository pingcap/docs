---
title: BATCH
summary: An overview of the usage of BATCH for the TiDB database.
---

# バッチ {#batch}

`BATCH`構文は、実行のために DML ステートメントを TiDB の複数のステートメントに分割します。これは、トランザクションの原子性と分離**が保証されないこと**を意味します。したがって、これは「非トランザクション」ステートメントです。

現在、 `INSERT` 、 `REPLACE` 、 `UPDATE` 、および`DELETE` `BATCH`でサポートされています。

`BATCH`構文は、列に基づいて、DML ステートメントを複数の実行範囲に分割します。各範囲で、単一の SQL ステートメントが実行されます。

使用方法と制限事項については、 [非トランザクション DML ステートメント](/non-transactional-dml.md)を参照してください。

`BATCH`ステートメントで複数テーブルの結合を使用する場合、あいまいさを避けるために、列のフル パスを指定する必要があります。

```sql
BATCH ON test.t2.id LIMIT 1 INSERT INTO t SELECT t2.id, t2.v, t3.v FROM t2 JOIN t3 ON t2.k = t3.k;
```

前のステートメントでは、分割する列を`test.t2.id`として指定していますが、これは明確です。 `id`次のように使用すると、エラーが報告されます。

```sql
BATCH ON id LIMIT 1 INSERT INTO t SELECT t2.id, t2.v, t3.v FROM t2 JOIN t3 ON t2.k = t3.k;

Non-transactional DML, shard column must be fully specified
```

## あらすじ {#synopsis}

```ebnf+diagram
NonTransactionalDMLStmt ::=
    'BATCH' ( 'ON' ColumnName )? 'LIMIT' NUM DryRunOptions? ShardableStmt

DryRunOptions ::=
    'DRY' 'RUN' 'QUERY'?

ShardableStmt ::=
    DeleteFromStmt
|   UpdateStmt
|   InsertIntoStmt
|   ReplaceIntoStmt
```

## MySQL の互換性 {#mysql-compatibility}

`BATCH`構文は TiDB 固有であり、MySQL と互換性がありません。

## こちらもご覧ください {#see-also}

-   [非トランザクション DML ステートメント](/non-transactional-dml.md)
