---
title: COMMIT | TiDB SQL Statement Reference
summary: TiDB データベースの COMMIT の使用法の概要。
---

# 専念 {#commit}

このステートメントは、TIDBサーバー内でトランザクションをコミットします。

`BEGIN`または`START TRANSACTION`ステートメントがない場合、TiDB のデフォルトの動作では、すべてのステートメントが独自のトランザクションと自動コミットになります。この動作により、MySQL との互換性が確保されます。

## 概要 {#synopsis}

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

## MySQL 互換性 {#mysql-compatibility}

-   現在、TiDB はメタデータ ロック (MDL) を使用して、デフォルトでトランザクションで使用されるテーブルが DDL ステートメントによって変更されるのを防ぎます。メタデータ ロックの動作は、TiDB と MySQL で異なります。詳細については、 [メタデータロック](/metadata-lock.md)参照してください。
-   デフォルトでは、 TiDB 3.0.8 以降のバージョンでは[悲観的ロック](/pessimistic-transaction.md)使用されます。 [楽観的ロック](/optimistic-transaction.md)を使用する場合は、別のトランザクションによって行が変更されているために`COMMIT`ステートメントが失敗する可能性があることを考慮することが重要です。
-   オプティミスティック ロックが有効になっている場合、 `UNIQUE`および`PRIMARY KEY`制約チェックはステートメントがコミットされるまで延期されます。これにより、 `COMMIT`ステートメントが失敗する可能性がある状況が追加されます。この動作は`tidb_constraint_check_in_place=ON`を設定することで変更できます。
-   TiDB は構文`ROLLBACK AND [NO] RELEASE`を解析しますが無視します。この機能は、MySQL でトランザクションをコミットした直後にクライアント セッションを切断するために使用されます。TiDB では、代わりにクライアント ドライバーの`mysql_close()`機能を使用することをお勧めします。
-   TiDB は構文`ROLLBACK AND [NO] CHAIN`を解析しますが無視します。この機能は、現在のトランザクションがコミットされている間に、同じ分離レベルで新しいトランザクションをすぐに開始するために MySQL で使用されます。TiDB では、代わりに新しいトランザクションを開始することをお勧めします。

## 参照 {#see-also}

-   [取引を開始](/sql-statements/sql-statement-start-transaction.md)
-   [ロールバック](/sql-statements/sql-statement-rollback.md)
-   [始める](/sql-statements/sql-statement-begin.md)
-   [制約の遅延チェック](/transaction-overview.md#lazy-check-of-constraints)
