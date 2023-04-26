---
title: COMMIT | TiDB SQL Statement Reference
summary: An overview of the usage of COMMIT for the TiDB database.
---

# 専念 {#commit}

このステートメントは、TIDBサーバー内でトランザクションをコミットします。

`BEGIN`または`START TRANSACTION`ステートメントがない場合、TiDB のデフォルトの動作では、すべてのステートメントが独自のトランザクションになり、自動コミットされます。この動作により、MySQL の互換性が確保されます。

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

## MySQL の互換性 {#mysql-compatibility}

-   現在、TiDB は Metadata Locking (MDL) を使用して、DDL ステートメントがデフォルトでトランザクションによって使用されるテーブルを変更するのを防ぎます。メタデータ ロックの動作は、TiDB と MySQL で異なります。詳細については、 [メタデータ ロック](/metadata-lock.md)を参照してください。
-   デフォルトでは、TiDB 3.0.8 以降のバージョンは[悲観的ロック](/pessimistic-transaction.md)を使用します。 [楽観的ロック](/optimistic-transaction.md)を使用する場合、行が別のトランザクションによって変更されたために`COMMIT`ステートメントが失敗する可能性があることを考慮することが重要です。
-   楽観的ロックが有効な場合、ステートメントがコミットされるまで、 `UNIQUE`つと`PRIMARY KEY`制約チェックが延期されます。これにより、aa `COMMIT`ステートメントが失敗する可能性がある追加の状況が発生します。この動作は`tidb_constraint_check_in_place=ON`を設定することで変更できます。
-   TiDB は構文を解析しますが、構文`ROLLBACK AND [NO] RELEASE`を無視します。この機能は MySQL で使用され、トランザクションをコミットした直後にクライアント セッションを切断します。 TiDB では、代わりにクライアント ドライバーの`mysql_close()`機能を使用することをお勧めします。
-   TiDB は構文を解析しますが、構文`ROLLBACK AND [NO] CHAIN`を無視します。この機能は MySQL で使用され、現在のトランザクションがコミットされている間に、同じ分離レベルで新しいトランザクションをすぐに開始します。 TiDB では、代わりに新しいトランザクションを開始することをお勧めします。

## こちらもご覧ください {#see-also}

-   [取引開始](/sql-statements/sql-statement-start-transaction.md)
-   [ロールバック](/sql-statements/sql-statement-rollback.md)
-   [始める](/sql-statements/sql-statement-begin.md)
-   [制約の遅延チェック](/transaction-overview.md#lazy-check-of-constraints)
