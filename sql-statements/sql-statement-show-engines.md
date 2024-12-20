---
title: SHOW ENGINES | TiDB SQL Statement Reference
summary: TiDB データベースの SHOW ENGINES の使用法の概要。
---

# エンジンを表示 {#show-engines}

このステートメントは、サポートされているすべてのstorageエンジンを一覧表示するために使用されます。この構文は、MySQL との互換性のためだけに含まれています。

## 概要 {#synopsis}

```ebnf+diagram
ShowEnginesStmt ::=
    "SHOW" "ENGINES" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 例 {#examples}

```sql
mysql> SHOW ENGINES;
+--------+---------+------------------------------------------------------------+--------------+------+------------+
| Engine | Support | Comment                                                    | Transactions | XA   | Savepoints |
+--------+---------+------------------------------------------------------------+--------------+------+------------+
| InnoDB | DEFAULT | Supports transactions, row-level locking, and foreign keys | YES          | YES  | YES        |
+--------+---------+------------------------------------------------------------+--------------+------+------------+
1 row in set (0.00 sec)
```

## MySQL 互換性 {#mysql-compatibility}

-   このステートメントは、サポートされているエンジンとして常に InnoDB のみを返します。内部的には、TiDB は通常、storageエンジンとして[ティクヴ](/tikv-overview.md)使用します。
