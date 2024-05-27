---
title: BATCH
summary: TiDB データベースでの BATCH の使用法の概要。
---

# バッチ {#batch}

`BATCH`構文は、DML ステートメントを TiDB 内の複数のステートメントに分割して実行します。つまり、トランザクションの原子性と分離性**は保証されません**。したがって、これは「非トランザクション」ステートメントです。

現在、 `BATCH`では`INSERT` 、 `REPLACE` 、 `UPDATE` 、 `DELETE`がサポートされています。

`BATCH`構文は、列に基づいて、DML ステートメントを複数の実行範囲に分割します。各範囲で、1 つの SQL ステートメントが実行されます。

使用方法や制限事項の詳細については[非トランザクションDMLステートメント](/non-transactional-dml.md)を参照してください。

`BATCH`のステートメントで複数テーブルの結合を使用する場合は、あいまいさを避けるために列の完全なパスを指定する必要があります。

```sql
BATCH ON test.t2.id LIMIT 1 INSERT INTO t SELECT t2.id, t2.v, t3.v FROM t2 JOIN t3 ON t2.k = t3.k;
```

上記のステートメントでは、分割する列を`test.t2.id`として指定しており、これは明確です。次のように`id`を使用すると、エラーが報告されます。

```sql
BATCH ON id LIMIT 1 INSERT INTO t SELECT t2.id, t2.v, t3.v FROM t2 JOIN t3 ON t2.k = t3.k;

Non-transactional DML, shard column must be fully specified
```

## 概要 {#synopsis}

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

## MySQL 互換性 {#mysql-compatibility}

`BATCH`構文は TiDB 固有であり、MySQL とは互換性がありません。

## 参照 {#see-also}

-   [非トランザクションDMLステートメント](/non-transactional-dml.md)
