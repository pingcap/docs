---
title: BEGIN | TiDB SQL Statement Reference
summary: An overview of the usage of BEGIN for the TiDB database.
---

# 始める {#begin}

このステートメントは、TiDB内で新しいトランザクションを開始します。これは、ステートメント`START TRANSACTION`および`SET autocommit=0`に似ています。

`BEGIN`のステートメントがない場合、すべてのステートメントはデフォルトで独自のトランザクションで自動コミットされます。この動作により、MySQLの互換性が保証されます。

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

TiDBは、 `BEGIN PESSIMISTIC`または`BEGIN OPTIMISTIC`の構文拡張をサポートしています。これにより、トランザクションのデフォルトのトランザクションモデルを上書きできます。

## も参照してください {#see-also}

-   [専念](/sql-statements/sql-statement-commit.md)
-   [ロールバック](/sql-statements/sql-statement-rollback.md)
-   [トランザクションを開始します](/sql-statements/sql-statement-start-transaction.md)
-   [TiDB楽観的トランザクションモデル](/optimistic-transaction.md)
-   [TiDB悲観的トランザクションモード](/pessimistic-transaction.md)
