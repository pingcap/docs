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
> -   TiDB Binlogが有効な状態で`SAVEPOINT`を使用することはできません。
> -   [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)が無効になっている場合、悲観的トランザクションで`SAVEPOINT`を使用することはできません。

-   `SAVEPOINT`は、現在のトランザクションで指定された名前のセーブポイントを設定するために使用されます。同名のセーブポイントが既に存在する場合は、そのセーブポイントを削除し、同名のセーブポイントを新たに設定します。

-   `ROLLBACK TO SAVEPOINT` 、指定された名前のセーブポイントまでトランザクションをロールバックし、トランザクションを終了しません。セーブポイント以降にテーブル データに加えられたデータ変更はロールバックで元に戻され、セーブポイント以降のすべてのセーブポイントが削除されます。悲観的トランザクションでは、トランザクションが保持するロックはロールバックされません。代わりに、トランザクションが終了するとロックが解放されます。

    `ROLLBACK TO SAVEPOINT`ステートメントで指定されたセーブポイントが存在しない場合、ステートメントは次のエラーを返します。

    ```
    ERROR 1305 (42000): SAVEPOINT identifier does not exist
    ```

-   `RELEASE SAVEPOINT`ステートメントは、現在のトランザクションをコミットまたはロールバックせずに、指定されたセーブポイントとこのセーブポイントより後の**すべてのセーブポイントを**現在のトランザクションから削除します。指定した名前のセーブポイントが存在しない場合、次のエラーが返されます。

    ```
    ERROR 1305 (42000): SAVEPOINT identifier does not exist
    ```

    トランザクションがコミットまたはロールバックされると、トランザクション内のすべてのセーブポイントが削除されます。

## 例 {#examples}

テーブルを作成します`t1` :

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

トランザクションをコミットし、テーブルをクエリします。 `sp1`の前に挿入されたデータのみが返されます。

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

## MySQL の互換性 {#mysql-compatibility}

トランザクションを指定されたセーブポイントにロールバックするために`ROLLBACK TO SAVEPOINT`が使用される場合、MySQL は指定されたセーブポイントの後にのみ保持されたロックを解放しますが、TiDB悲観的トランザクションでは、TiDB は指定されたセーブポイントの後に保持されたロックをすぐには解放しません。代わりに、トランザクションがコミットまたはロールバックされると、TiDB はすべてのロックを解放します。

## こちらもご覧ください {#see-also}

-   [専念](/sql-statements/sql-statement-commit.md)
-   [ロールバック](/sql-statements/sql-statement-rollback.md)
-   [取引開始](/sql-statements/sql-statement-start-transaction.md)
-   [TiDB オプティミスティックトランザクションモード](/optimistic-transaction.md)
-   [TiDB ペシミスティックトランザクションモード](/pessimistic-transaction.md)
