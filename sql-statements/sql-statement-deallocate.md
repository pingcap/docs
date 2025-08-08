---
title: DEALLOCATE | TiDB SQL Statement Reference
summary: TiDB データベースの DEALLOCATE の使用法の概要。
---

# 割り当て解除 {#deallocate}

`DEALLOCATE`ステートメントは、サーバー側の準備済みステートメントへの SQL インターフェイスを提供します。

## 概要 {#synopsis}

```ebnf+diagram
DeallocateStmt ::=
    DeallocateSym 'PREPARE' Identifier

DeallocateSym ::=
    'DEALLOCATE'
|   'DROP'

Identifier ::=
    identifier
|   UnReservedKeyword
|   NotKeywordToken
|   TiDBKeyword
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

## MySQLの互換性 {#mysql-compatibility}

TiDBの`DEALLOCATE`文はMySQLと完全に互換性があります。互換性に違いがある場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support)参照してください。

## 参照 {#see-also}

-   [準備する](/sql-statements/sql-statement-prepare.md)
-   [実行する](/sql-statements/sql-statement-execute.md)
