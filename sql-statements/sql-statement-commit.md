---
title: COMMIT | TiDB SQL Statement Reference
summary: An overview of the usage of COMMIT for the TiDB database.
---

# 専念 {#commit}

このステートメントは、TIDBサーバー内でトランザクションをコミットします。

`BEGIN`または`START TRANSACTION`ステートメントがない場合、TiDB のデフォルトの動作では、すべてのステートメントが独自のトランザクションとなり自動コミットされます。この動作により、MySQL との互換性が保証されます。

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

-   現在、TiDB はメタデータ ロック (MDL) を使用して、デフォルトで DDL ステートメントがトランザクションで使用されるテーブルを変更するのを防ぎます。メタデータ ロックの動作は、TiDB と MySQL で異なります。詳細については、 [メタデータロック](/metadata-lock.md)を参照してください。
-   デフォルトでは、TiDB 3.0.8 以降のバージョンは[悲観的ロック](/pessimistic-transaction.md)を使用します。 [楽観的ロック](/optimistic-transaction.md)を使用する場合は、行が別のトランザクションによって変更されているため、 `COMMIT`ステートメントが失敗する可能性があることを考慮することが重要です。
-   オプティミスティック ロックが有効な場合、 `UNIQUE`と`PRIMARY KEY`の制約チェックはステートメントがコミットされるまで延期されます。これにより、aa `COMMIT`ステートメントが失敗する可能性がある追加の状況が発生します。この動作は`tidb_constraint_check_in_place=ON`を設定することで変更できます。
-   TiDB は構文を解析しますが無視します`ROLLBACK AND [NO] RELEASE` 。この機能は、トランザクションをコミットした直後にクライアント セッションを切断するために MySQL で使用されます。 TiDB では、代わりにクライアント ドライバーの`mysql_close()`機能を使用することをお勧めします。
-   TiDB は構文を解析しますが無視します`ROLLBACK AND [NO] CHAIN` 。この機能は MySQL で使用され、現在のトランザクションがコミットされている間に、同じ分離レベルで新しいトランザクションを即座に開始します。 TiDB では、代わりに新しいトランザクションを開始することをお勧めします。

## こちらも参照 {#see-also}

-   [取引を開始する](/sql-statements/sql-statement-start-transaction.md)
-   [ロールバック](/sql-statements/sql-statement-rollback.md)
-   [始める](/sql-statements/sql-statement-begin.md)
-   [制約の遅延チェック](/transaction-overview.md#lazy-check-of-constraints)
