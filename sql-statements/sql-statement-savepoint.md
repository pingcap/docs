---
title: SAVEPOINT | TiDB SQL Statement Reference
summary: TiDB データベースの SAVEPOINT の使用法の概要。
---

# SAVEPOINT {#savepoint}

`SAVEPOINT`はTiDB v6.2.0で導入された機能です。構文は次のとおりです。

```sql
SAVEPOINT identifier
ROLLBACK TO [SAVEPOINT] identifier
RELEASE SAVEPOINT identifier
```

> **Warning:**
>
> [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)無効になっている場合、悲観的トランザクションで`SAVEPOINT`を使用することはできません。

-   `SAVEPOINT` 、現在のトランザクションに指定された名前のセーブポイントを設定するために使用されます。同じ名前のセーブポイントが既に存在する場合、それは削除され、同じ名前の新しいセーブポイントが設定されます。

-   `ROLLBACK TO SAVEPOINT` 、指定された名前のセーブポイントまでトランザクションをロールバックしますが、トランザクション自体は終了しません。セーブポイント以降にテーブルデータに加えられたデータ変更はロールバック時に元に戻され、セーブポイント以降のすべてのセーブポイントは削除されます。悲観的トランザクションでは、トランザクションによって保持されているロックはロールバックされません。代わりに、トランザクション終了時にロックが解放されます。

    `ROLLBACK TO SAVEPOINT`のステートメントで指定されたセーブポイントが存在しない場合は、ステートメントは次のエラーを返します。

        ERROR 1305 (42000): SAVEPOINT identifier does not exist

-   `RELEASE SAVEPOINT`文は、現在のトランザクションをコミットまたはロールバックせずに、指定されたセーブポイントとそれ以降の**すべてのセーブポイントを**現在のトランザクションから削除します。指定された名前のセーブポイントが存在しない場合は、次のエラーが返されます。

        ERROR 1305 (42000): SAVEPOINT identifier does not exist

    トランザクションがコミットまたはロールバックされると、トランザクション内のすべてのセーブポイントが削除されます。

## 概要 {#synopsis}

```ebnf+diagram
SavepointStmt ::=
    "SAVEPOINT" Identifier

RollbackToStmt ::=
    "ROLLBACK" "TO" "SAVEPOINT"? Identifier

ReleaseSavepointStmt ::=
    "RELEASE" "SAVEPOINT" Identifier
```

## 例 {#examples}

テーブル`t1`を作成します。

```sql
CREATE TABLE t1 (a INT NOT NULL PRIMARY KEY);
```

```sql
Query OK, 0 rows affected (0.12 sec)
```

現在のトランザクションを開始します:

```sql
BEGIN;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

テーブルにデータを挿入し、セーブポイント`sp1`設定します。

```sql
INSERT INTO t1 VALUES (1);
```

```sql
Query OK, 1 row affected (0.00 sec)
```

```sql
SAVEPOINT sp1;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

テーブルに再度データを挿入し、セーブポイント`sp2`設定します。

```sql
INSERT INTO t1 VALUES (2);
```

```sql
Query OK, 1 row affected (0.00 sec)
```

```sql
SAVEPOINT sp2;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

セーブポイント`sp2`を解放します:

```sql
RELEASE SAVEPOINT sp2;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

セーブポイント`sp1`にロールバックします。

```sql
ROLLBACK TO SAVEPOINT sp1;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

トランザクションをコミットし、テーブルをクエリします。1 `sp1`前に挿入されたデータのみが返されます。

```sql
COMMIT;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

```sql
SELECT * FROM t1;
```

```sql
+---+
| a |
+---+
| 1 |
+---+
1 row in set
```

## MySQLの互換性 {#mysql-compatibility}

`ROLLBACK TO SAVEPOINT`を使用してトランザクションを指定されたセーブポイントまでロールバックすると、MySQL は指定されたセーブポイント以降に保持されているロックのみを解放します。一方、TiDB の悲観的トランザクションでは、TiDB は指定されたセーブポイント以降に保持されているロックをすぐには解放しません。代わりに、TiDB はトランザクションがコミットまたはロールバックされた時点ですべてのロックを解放します。

TiDB は MySQL 構文`ROLLBACK WORK TO SAVEPOINT ...`サポートしていません。

## 参照 {#see-also}

-   [COMMIT](/sql-statements/sql-statement-commit.md)
-   [ROLLBACK](/sql-statements/sql-statement-rollback.md)
-   [START TRANSACTION](/sql-statements/sql-statement-start-transaction.md)
-   [TiDB 楽観的トランザクションモード](/optimistic-transaction.md)
-   [TiDB 悲観的トランザクションモード](/pessimistic-transaction.md)
