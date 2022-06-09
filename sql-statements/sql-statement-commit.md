---
title: COMMIT | TiDB SQL Statement Reference
summary: An overview of the usage of COMMIT for the TiDB database.
---

# 専念 {#commit}

このステートメントは、TIDBサーバー内でトランザクションをコミットします。

`BEGIN`つまたは`START TRANSACTION`のステートメントがない場合、TiDBのデフォルトの動作では、すべてのステートメントが独自のトランザクションおよび自動コミットになります。この動作により、MySQLの互換性が保証されます。

## あらすじ {#synopsis}

```ebnf+diagram
CommitStmt ::=
    'COMMIT' CompletionTypeWithinTransaction?

CompletionTypeWithinTransaction ::=
    'AND' ( 'CHAIN' ( 'NO' 'RELEASE' )? | 'NO' 'CHAIN' ( 'NO'? 'RELEASE' )? )
|   'NO'? 'RELEASE'
```

## 例 {#examples}

```sql
mysql> CREATE TABLE t1 (a int NOT NULL PRIMARY KEY);
Query OK, 0 rows affected (0.12 sec)

mysql> START TRANSACTION;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t1 VALUES (1);
Query OK, 1 row affected (0.00 sec)

mysql> COMMIT;
Query OK, 0 rows affected (0.01 sec)
```

## MySQLの互換性 {#mysql-compatibility}

-   現在、TiDBはメタデータロック（MDL）を使用して、DDLステートメントがトランザクションで使用されるテーブルを変更するのを防ぎません。テーブルの定義が変更された場合、トランザクションをコミットすると`Information schema is changed`エラーになります。この場合、トランザクションは自動的にロールバックされます。
-   デフォルトでは、TiDB3.0.8以降のバージョンは[悲観的なロック](/pessimistic-transaction.md)を使用します。 [楽観的ロック](/optimistic-transaction.md)を使用する場合、行が別のトランザクションによって変更されたために`COMMIT`ステートメントが失敗する可能性があることを考慮することが重要です。
-   Optimistic Lockingが有効になっている場合、ステートメントがコミットされるまで`UNIQUE`と`PRIMARY KEY`の制約チェックが延期されます。これにより、 `COMMIT`ステートメントが失敗する可能性がある追加の状況が発生します。この動作は、 `tidb_constraint_check_in_place=TRUE`を設定することで変更できます。
-   TiDBは構文解析しますが、構文`ROLLBACK AND [NO] RELEASE`を無視します。この機能は、トランザクションをコミットした直後にクライアントセッションを切断するためにMySQLで使用されます。 TiDBでは、代わりにクライアントドライバーの`mysql_close()`の機能を使用することをお勧めします。
-   TiDBは構文解析しますが、構文`ROLLBACK AND [NO] CHAIN`を無視します。この機能はMySQLで使用され、現在のトランザクションがコミットされている間、同じ分離レベルで新しいトランザクションをすぐに開始します。 TiDBでは、代わりに新しいトランザクションを開始することをお勧めします。

## も参照してください {#see-also}

-   [トランザクションを開始します](/sql-statements/sql-statement-start-transaction.md)
-   [ロールバック](/sql-statements/sql-statement-rollback.md)
-   [始める](/sql-statements/sql-statement-begin.md)
-   [制約のレイジーチェック](/transaction-overview.md#lazy-check-of-constraints)
