---
title: BEGIN | TiDB SQL Statement Reference
summary: An overview of the usage of BEGIN for the TiDB database.
---

# 始める {#begin}

このステートメントは、TiDB 内で新しいトランザクションを開始します。これはステートメント`START TRANSACTION`とステートメント`SET autocommit=0`に似ています。

`BEGIN`ステートメントがない場合、デフォルトでは、すべてのステートメントが独自のトランザクションで自動コミットされます。この動作により、MySQL との互換性が保証されます。

## あらすじ {#synopsis}

```ebnf+diagram
BeginTransactionStmt ::=
    'BEGIN' ( 'PESSIMISTIC' | 'OPTIMISTIC' )?
|   'START' 'TRANSACTION' ( 'READ' ( 'WRITE' | 'ONLY' ( 'WITH' 'TIMESTAMP' 'BOUND' TimestampBound )? ) | 'WITH' 'CONSISTENT' 'SNAPSHOT' )?
```

## 例 {#examples}

```sql
mysql> CREATE TABLE t1 (a int NOT NULL PRIMARY KEY);
Query OK, 0 rows affected (0.12 sec)

mysql> BEGIN;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t1 VALUES (1);
Query OK, 1 row affected (0.00 sec)

mysql> COMMIT;
Query OK, 0 rows affected (0.01 sec)
```

## MySQLの互換性 {#mysql-compatibility}

TiDB は、 `BEGIN PESSIMISTIC`または`BEGIN OPTIMISTIC`の構文拡張をサポートします。これにより、トランザクションのデフォルトのトランザクション モデルをオーバーライドできます。

## こちらも参照 {#see-also}

-   [専念](/sql-statements/sql-statement-commit.md)
-   [ロールバック](/sql-statements/sql-statement-rollback.md)
-   [取引を開始する](/sql-statements/sql-statement-start-transaction.md)
-   [TiDB の楽観的トランザクション モデル](/optimistic-transaction.md)
-   [TiDB悲観的トランザクション モード](/pessimistic-transaction.md)
