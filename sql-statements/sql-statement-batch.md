---
title: BATCH
summary: TiDB データベースにおける BATCH の使用法の概要。
---

# バッチ {#batch}

`BATCH`構文は、TiDB 内で DML 文を複数の文に分割して実行します。つまり、トランザクションの原子性と独立性は**保証されません**。したがって、これは「非トランザクション」文です。

現在、 `BATCH`では`INSERT` 、 `REPLACE` 、 `UPDATE` 、 `DELETE`サポートされています。

`BATCH`構文は、列に基づいてDML文を複数の実行範囲に分割します。各範囲では、1つのSQL文が実行されます。

使用方法および制限事項の詳細については、 [非トランザクションDMLステートメント](/non-transactional-dml.md)参照してください。

`BATCH`ステートメントで複数テーブルの結合を使用する場合は、あいまいさを避けるために列の完全なパスを指定する必要があります。

```sql
BATCH ON test.t2.id LIMIT 1 INSERT INTO t SELECT t2.id, t2.v, t3.v FROM t2 JOIN t3 ON t2.k = t3.k;
```

上記の文では、分割する列を`test.t2.id`と指定しており、これは明確な値です。次のように`id`使用すると、エラーが発生します。

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

## MySQLの互換性 {#mysql-compatibility}

`BATCH`構文は TiDB 固有であり、MySQL とは互換性がありません。

## 参照 {#see-also}

-   [非トランザクションDMLステートメント](/non-transactional-dml.md)
