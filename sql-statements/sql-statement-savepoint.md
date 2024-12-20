---
title: SAVEPOINT | TiDB SQL Statement Reference
summary: TiDB データベースの SAVEPOINT の使用法の概要。
---

# セーブポイント {#savepoint}

`SAVEPOINT` TiDB v6.2.0 で導入された機能です。構文は次のとおりです。

```sql
SAVEPOINT identifier
ROLLBACK TO [SAVEPOINT] identifier
RELEASE SAVEPOINT identifier
```

> **警告：**
>
> [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)が無効になっている場合、悲観的トランザクションでは`SAVEPOINT`使用できません。

-   `SAVEPOINT` 、現在のトランザクションで指定された名前のセーブポイントを設定するために使用されます。同じ名前のセーブポイントがすでに存在する場合は、削除され、同じ名前の新しいセーブポイントが設定されます。

-   `ROLLBACK TO SAVEPOINT`指定された名前のセーブポイントまでトランザクションをロールバックし、トランザクションを終了しません。セーブポイント後にテーブル データに加えられたデータ変更はロールバックで元に戻され、セーブポイント以降のすべてのセーブポイントは削除されます。悲観的トランザクションでは、トランザクションによって保持されたロックはロールバックされません。代わりに、トランザクションが終了するとロックが解放されます。

    `ROLLBACK TO SAVEPOINT`ステートメントで指定されたセーブポイントが存在しない場合、ステートメントは次のエラーを返します。

        ERROR 1305 (42000): SAVEPOINT identifier does not exist

-   `RELEASE SAVEPOINT`ステートメントは、現在のトランザクションをコミットまたはロールバックせずに、指定されたセーブポイントと、このセーブポイント以降の**すべてのセーブポイントを**現在のトランザクションから削除します。指定された名前のセーブポイントが存在しない場合は、次のエラーが返されます。

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

テーブルにデータを挿入し、セーブポイント`sp1`を設定します。

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

テーブルに再度データを挿入し、セーブポイント`sp2`を設定します。

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

セーブポイント`sp1`にロールバックします:

```sql
ROLLBACK TO SAVEPOINT sp1;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

トランザクションをコミットし、テーブルをクエリ`sp1`ます。1 より前に挿入されたデータのみが返されます。

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

## MySQL 互換性 {#mysql-compatibility}

`ROLLBACK TO SAVEPOINT`を使用してトランザクションを指定されたセーブポイントまでロールバックすると、MySQL は指定されたセーブポイント後にのみ保持されたロックを解放しますが、TiDB悲観的トランザクションでは、TiDB は指定されたセーブポイント後に保持されたロックをすぐには解放しません。代わりに、TiDB はトランザクションがコミットまたはロールバックされたときにすべてのロックを解放します。

TiDB は MySQL 構文`ROLLBACK WORK TO SAVEPOINT ...`をサポートしていません。

## 参照 {#see-also}

-   [専念](/sql-statements/sql-statement-commit.md)
-   [ロールバック](/sql-statements/sql-statement-rollback.md)
-   [取引を開始](/sql-statements/sql-statement-start-transaction.md)
-   [TiDB 楽観的トランザクションモード](/optimistic-transaction.md)
-   [TiDB 悲観的トランザクションモード](/pessimistic-transaction.md)
