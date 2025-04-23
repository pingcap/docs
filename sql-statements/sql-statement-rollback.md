---
title: ROLLBACK | TiDB SQL Statement Reference
summary: TiDB データベースの ROLLBACK の使用法の概要。
---

# ロールバック {#rollback}

このステートメントは、TiDB内の現在のトランザクション内のすべての変更を元に戻します。これは`COMMIT`ステートメントの逆の動作です。

## 概要 {#synopsis}

```ebnf+diagram
RollbackStmt ::=
    'ROLLBACK' CompletionTypeWithinTransaction?

CompletionTypeWithinTransaction ::=
    'AND' ( 'CHAIN' ( 'NO' 'RELEASE' )? | 'NO' 'CHAIN' ( 'NO'? 'RELEASE' )? )
|   'NO'? 'RELEASE'
```

## 例 {#examples}

```sql
mysql> CREATE TABLE t1 (a INT NOT NULL PRIMARY KEY);
Query OK, 0 rows affected (0.12 sec)

mysql> BEGIN;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t1 VALUES (1);
Query OK, 1 row affected (0.00 sec)

mysql> ROLLBACK;
Query OK, 0 rows affected (0.01 sec)

mysql> SELECT * FROM t1;
Empty set (0.01 sec)
```

## MySQLの互換性 {#mysql-compatibility}

-   TiDBは構文`ROLLBACK AND [NO] RELEASE`を解析しますが、無視します。この機能はMySQLでトランザクションのロールバック直後にクライアントセッションを切断するために使用されます。TiDBでは、代わりにクライアントドライバの`mysql_close()`機能を使用することをお勧めします。
-   TiDBは構文`ROLLBACK AND [NO] CHAIN`を解析しますが、無視します。この機能はMySQLで使用され、現在のトランザクションがロールバックされている間に、同じ分離レベルで新しいトランザクションを即座に開始します。TiDBでは、代わりに新しいトランザクションを開始することが推奨されます。

## 参照 {#see-also}

-   [セーブポイント](/sql-statements/sql-statement-savepoint.md)
-   [専念](/sql-statements/sql-statement-commit.md)
-   [始める](/sql-statements/sql-statement-begin.md)
-   [取引を開始](/sql-statements/sql-statement-start-transaction.md)
