---
title: SAVEPOINT | TiDB SQL Statement Reference
summary: An overview of the usage of SAVEPOINT for the TiDB database.
---

# セーブポイント {#savepoint}

`SAVEPOINT`は TiDB v6.2.0 で導入された機能です。構文は次のとおりです。

```sql
SAVEPOINT identifier
ROLLBACK TO [SAVEPOINT] identifier
RELEASE SAVEPOINT identifier
```

> **警告：**
>
> -   TiDB Binlogが有効な場合は`SAVEPOINT`を使用できません。
> -   [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)が無効になっている場合、悲観的トランザクションで`SAVEPOINT`を使用することはできません。

-   `SAVEPOINT`は、現在のトランザクションに指定された名前のセーブポイントを設定するために使用されます。同名のセーブポイントがすでに存在する場合は削除され、新たに同名のセーブポイントが設定されます。

-   `ROLLBACK TO SAVEPOINT` 、トランザクションを指定された名前のセーブポイントにロールバックしますが、トランザクションは終了しません。セーブポイントの後にテーブル データに加えられたデータ変更はロールバックで元に戻され、セーブポイント以降のセーブポイントはすべて削除されます。悲観的トランザクションでは、トランザクションによって保持されているロックはロールバックされません。代わりに、トランザクションが終了するとロックが解放されます。

    `ROLLBACK TO SAVEPOINT`ステートメントで指定されたセーブポイントが存在しない場合、ステートメントは次のエラーを返します。

        ERROR 1305 (42000): SAVEPOINT identifier does not exist

-   `RELEASE SAVEPOINT`ステートメントは、現在のトランザクションをコミットまたはロールバックせずに、指定されたセーブポイントとこのセーブポイント以降の**すべてのセーブポイントを**現在のトランザクションから削除します。指定された名前のセーブポイントが存在しない場合は、次のエラーが返されます。

        ERROR 1305 (42000): SAVEPOINT identifier does not exist

    トランザクションがコミットまたはロールバックされると、トランザクション内のすべてのセーブポイントが削除されます。

## 例 {#examples}

テーブル`t1`を作成します。

```sql
CREATE TABLE t1 (a INT NOT NULL PRIMARY KEY);
```

```sql
Query OK, 0 rows affected (0.12 sec)
```

現在のトランザクションを開始します。

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

テーブルにデータを再度挿入し、セーブポイント`sp2`を設定します。

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

セーブポイント`sp2`を解放します。

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

トランザクションをコミットし、テーブルをクエリします。 `sp1`より前に挿入されたデータのみが返されます。

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

トランザクションを指定されたセーブポイントにロールバックするために`ROLLBACK TO SAVEPOINT`が使用される場合、MySQL は指定されたセーブポイントの後にのみ保持されているロックを解放しますが、TiDB悲観的トランザクションでは、TiDB は指定されたセーブポイントの後に保持されているロックをすぐには解放しません。代わりに、TiDB はトランザクションがコミットまたはロールバックされるときにすべてのロックを解放します。

## こちらも参照 {#see-also}

-   [専念](/sql-statements/sql-statement-commit.md)
-   [ロールバック](/sql-statements/sql-statement-rollback.md)
-   [取引を開始する](/sql-statements/sql-statement-start-transaction.md)
-   [TiDB オプティミスティックトランザクションモード](/optimistic-transaction.md)
-   [TiDB ペシミスティックトランザクションモード](/pessimistic-transaction.md)
