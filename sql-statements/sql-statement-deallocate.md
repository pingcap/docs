---
title: DEALLOCATE | TiDB SQL Statement Reference
summary: An overview of the usage of DEALLOCATE for the TiDB database.
---

# 割り当て解除 {#deallocate}

`DEALLOCATE`ステートメントは、サーバー側のプリペアドステートメントへのSQLインターフェイスを提供します。

## あらすじ {#synopsis}

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

このステートメントは、MySQLと完全に互換性があると理解されています。互換性の違いは、GitHubでは[問題を介して報告された](https://github.com/pingcap/tidb/issues/new/choose)である必要があります。

## も参照してください {#see-also}

-   [準備](/sql-statements/sql-statement-prepare.md)
-   [実行する](/sql-statements/sql-statement-execute.md)
