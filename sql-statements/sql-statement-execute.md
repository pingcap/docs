---
title: EXECUTE | TiDB SQL Statement Reference
summary: An overview of the usage of EXECUTE for the TiDB database.
---

# 実行する {#execute}

`EXECUTE`ステートメントは、サーバー側の準備済みステートメントへの SQL インターフェイスを提供します。

## あらすじ {#synopsis}

```ebnf+diagram
ExecuteStmt ::=
    'EXECUTE' Identifier ( 'USING' UserVariable ( ',' UserVariable )* )?
```

## 例 {#examples}

```sql
mysql> PREPARE mystmt FROM 'SELECT ? as num FROM DUAL';
Query OK, 0 rows affected (0.00 sec)

mysql> SET @number = 5;
Query OK, 0 rows affected (0.00 sec)

mysql> EXECUTE mystmt USING @number;
+------+
| num  |
+------+
| 5    |
+------+
1 row in set (0.00 sec)

mysql> DEALLOCATE PREPARE mystmt;
Query OK, 0 rows affected (0.00 sec)
```

## MySQL の互換性 {#mysql-compatibility}

このステートメントは、MySQL と完全に互換性があると理解されています。互換性の違いは、GitHub で[問題を介して報告された](https://github.com/pingcap/tidb/issues/new/choose)にする必要があります。

## こちらもご覧ください {#see-also}

-   [準備](/sql-statements/sql-statement-prepare.md)
-   [割り当て解除](/sql-statements/sql-statement-deallocate.md)
