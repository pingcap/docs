---
title: SET TRANSACTION | TiDB SQL 语句参考
summary: 关于在 TiDB 数据库中使用 SET TRANSACTION 的概述。
---

# SET TRANSACTION

`SET TRANSACTION` 语句可用于在 `GLOBAL` 或 `SESSION` 级别更改当前的隔离级别。此语法是 `SET transaction_isolation='new-value'` 的替代方案，旨在兼容 MySQL 和 SQL 标准。

## 概要

```ebnf+diagram
SetStmt ::=
    'SET' ( VariableAssignmentList |
    'PASSWORD' ('FOR' Username)? '=' PasswordOpt |
    ( 'GLOBAL'| 'SESSION' )? 'TRANSACTION' TransactionChars |
    'CONFIG' ( Identifier | stringLit) ConfigItemName EqOrAssignmentEq SetExpr )

TransactionChars ::=
    ( 'ISOLATION' 'LEVEL' IsolationLevel | 'READ' 'WRITE' | 'READ' 'ONLY' AsOfClause? )

IsolationLevel ::=
    ( 'REPEATABLE' 'READ' | 'READ' ( 'COMMITTED' | 'UNCOMMITTED' ) | 'SERIALIZABLE' )

AsOfClause ::=
    ( 'AS' 'OF' 'TIMESTAMP' Expression)
```

## 示例

```sql
mysql> SHOW SESSION VARIABLES LIKE 'transaction_isolation';
+-----------------------+-----------------+
| Variable_name         | Value           |
+-----------------------+-----------------+
| transaction_isolation | REPEATABLE-READ |
+-----------------------+-----------------+
1 row in set (0.00 sec)

mysql> SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
Query OK, 0 rows affected (0.00 sec)

mysql> SHOW SESSION VARIABLES LIKE 'transaction_isolation';
+-----------------------+----------------+
| Variable_name         | Value          |
+-----------------------+----------------+
| transaction_isolation | READ-COMMITTED |
+-----------------------+----------------+
1 row in set (0.01 sec)

mysql> SET SESSION transaction_isolation = 'REPEATABLE-READ';
Query OK, 0 rows affected (0.00 sec)

mysql> SHOW SESSION VARIABLES LIKE 'transaction_isolation';
+-----------------------+-----------------+
| Variable_name         | Value           |
+-----------------------+-----------------+
| transaction_isolation | REPEATABLE-READ |
+-----------------------+-----------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

* TiDB 仅支持语法上设置事务为只读的能力。
* 不支持 `READ-UNCOMMITTED` 和 `SERIALIZABLE` 这两个隔离级别。
* `REPEATABLE-READ` 隔离级别通过使用快照隔离技术实现，部分兼容 MySQL。
* 在悲观事务中，TiDB 支持两个与 MySQL 兼容的隔离级别：`REPEATABLE-READ` 和 `READ-COMMITTED`。详细描述请参见 [Isolation Levels](/transaction-isolation-levels.md)。

## 相关链接

* [`SET [GLOBAL|SESSION] <variable>`](/sql-statements/sql-statement-set-variable.md)
* [Isolation Levels](/transaction-isolation-levels.md)
