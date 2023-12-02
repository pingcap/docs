---
title: SET TRANSACTION | TiDB SQL Statement Reference
summary: An overview of the usage of SET TRANSACTION for the TiDB database.
---

# トランザクションの設定 {#set-transaction}

`SET TRANSACTION`ステートメントを使用すると、現在の分離レベルを`GLOBAL`または`SESSION`に基づいて変更できます。この構文は`SET transaction_isolation='new-value'`の代替であり、MySQL と SQL 標準の両方との互換性のために組み込まれています。

## あらすじ {#synopsis}

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

## 例 {#examples}

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

## MySQLの互換性 {#mysql-compatibility}

-   TiDB は、構文のみでトランザクションを読み取り専用として設定する機能をサポートしています。
-   分離レベル`READ-UNCOMMITTED`と`SERIALIZABLE`はサポートされていません。
-   分離レベル`REPEATABLE-READ` 、MySQL と部分的に互換性のあるスナップショット分離テクノロジーを使用することで実現されます。
-   悲観的トランザクションでは、TiDB は MySQL と互換性のある 2 つの分離レベル ( `REPEATABLE-READ`と`READ-COMMITTED`をサポートします。詳細な説明については、 [分離レベル](/transaction-isolation-levels.md)を参照してください。

## こちらも参照 {#see-also}

-   [`SET [GLOBAL|SESSION] &#x3C;variable>`](/sql-statements/sql-statement-set-variable.md)
-   [分離レベル](/transaction-isolation-levels.md)
