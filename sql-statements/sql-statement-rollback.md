---
title: ROLLBACK | TiDB SQL Statement Reference
summary: An overview of the usage of ROLLBACK for the TiDB database.
---

# ロールバック {#rollback}

このステートメントは、TIDB 内の現在のトランザクションのすべての変更を元に戻します。 `COMMIT`ステートメントの反対です。

## あらすじ {#synopsis}

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

## MySQL の互換性 {#mysql-compatibility}

-   TiDB は構文を解析しますが、構文`ROLLBACK AND [NO] RELEASE`を無視します。この機能は MySQL で使用され、トランザクションをロールバックした直後にクライアント セッションを切断します。 TiDB では、代わりにクライアント ドライバーの`mysql_close()`機能を使用することをお勧めします。
-   TiDB は構文を解析しますが、構文`ROLLBACK AND [NO] CHAIN`を無視します。この機能は MySQL で使用され、現在のトランザクションがロールバックされている間に、同じ分離レベルで新しいトランザクションをすぐに開始します。 TiDB では、代わりに新しいトランザクションを開始することをお勧めします。

## こちらもご覧ください {#see-also}

-   [セーブポイント](/sql-statements/sql-statement-savepoint.md)
-   [専念](/sql-statements/sql-statement-commit.md)
-   [始める](/sql-statements/sql-statement-begin.md)
-   [取引開始](/sql-statements/sql-statement-start-transaction.md)
