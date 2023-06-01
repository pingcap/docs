---
title: BATCH
summary: An overview of the usage of BATCH for the TiDB database.
---

# バッチ {#batch}

`BATCH`構文は、DML ステートメントを TiDB 内の複数のステートメントに分割して実行します。これは、トランザクションの原子性と分離性**が保証されていない**ことを意味します。したがって、これは「非トランザクション」ステートメントです。

現在、 `INSERT` 、 `REPLACE` 、 `UPDATE` 、および`DELETE` `BATCH`でサポートされています。

`BATCH`構文は、列に基づいて、DML ステートメントを実行範囲の複数の範囲に分割します。各範囲で、単一の SQL ステートメントが実行されます。

使用方法および制限事項の詳細については、 [非トランザクション DML ステートメント](/non-transactional-dml.md)を参照してください。

`BATCH`ステートメントで複数テーブル結合を使用する場合、あいまいさを避けるために列のフルパスを指定する必要があります。

```sql
BATCH ON test.t2.id LIMIT 1 INSERT INTO t SELECT t2.id, t2.v, t3.v FROM t2 JOIN t3 ON t2.k = t3.k;
```

前述のステートメントでは、分割する列を`test.t2.id`として指定していますが、これは明確です。次のように`id`使用すると、エラーが報告されます。

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

## MySQLの互換性 {#mysql-compatibility}

`BATCH`構文は TiDB 固有であり、MySQL とは互換性がありません。

## こちらも参照 {#see-also}

-   [非トランザクション DML ステートメント](/non-transactional-dml.md)
