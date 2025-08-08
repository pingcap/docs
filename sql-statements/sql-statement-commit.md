---
title: COMMIT | TiDB SQL Statement Reference
summary: TiDB データベースの COMMIT の使用法の概要。
---

# 専念 {#commit}

このステートメントは、TiDBサーバー内でトランザクションをコミットします。

`BEGIN`または`START TRANSACTION`ステートメントがない場合、TiDB のデフォルトの動作では、各ステートメントが独自のトランザクションとなり、自動コミットされます。この動作により、MySQL との互換性が確保されます。

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

## MySQLの互換性 {#mysql-compatibility}

-   現在、TiDBはメタデータロック（MDL）を使用して、DDL文によるトランザクションで使用されるテーブルの変更をデフォルトで防止しています。メタデータロックの動作はTiDBとMySQLで異なります。詳細については、 [メタデータロック](/metadata-lock.md)参照してください。
-   TiDB 3.0.8以降のバージョンでは、デフォルトで[悲観的ロック](/pessimistic-transaction.md)使用されます。 [楽観的ロック](/optimistic-transaction.md)使用する場合は、別のトランザクションによって行が変更されているために`COMMIT`ステートメントが失敗する可能性があることを考慮することが重要です。
-   楽観的ロックが有効な場合、制約`UNIQUE`と`PRIMARY KEY`チェックは文のコミットまで延期されます。これにより、制約`COMMIT`文が失敗する状況が増えます。この動作は`tidb_constraint_check_in_place=ON`設定することで変更できます。
-   TiDBは構文`ROLLBACK AND [NO] RELEASE`を解析しますが、無視します。この機能はMySQLでトランザクションのコミット直後にクライアントセッションを切断するために使用されます。TiDBでは、代わりにクライアントドライバの`mysql_close()`機能を使用することをお勧めします。
-   TiDBは構文`ROLLBACK AND [NO] CHAIN`を解析しますが、無視します。この機能はMySQLで使用され、現在のトランザクションがコミットされている間に、同じ分離レベルで新しいトランザクションを即座に開始します。TiDBでは、代わりに新しいトランザクションを開始することが推奨されます。

## 参照 {#see-also}

-   [取引を開始](/sql-statements/sql-statement-start-transaction.md)
-   [ロールバック](/sql-statements/sql-statement-rollback.md)
-   [始める](/sql-statements/sql-statement-begin.md)
-   [制約の遅延チェック](/transaction-overview.md#lazy-check-of-constraints)
