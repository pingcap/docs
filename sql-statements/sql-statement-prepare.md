---
title: PREPARE | TiDB SQL Statement Reference
summary: An overview of the usage of PREPARE for the TiDB database.
---

# 準備 {#prepare}

`PREPARE`ステートメントは、サーバー側のプリペアドステートメントへのSQLインターフェイスを提供します。

## あらすじ {#synopsis}

```ebnf+diagram
PreparedStmt ::=
    'PREPARE' Identifier 'FROM' PrepareSQL

PrepareSQL ::=
    stringLit
|   UserVariable
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

-   [実行する](/sql-statements/sql-statement-execute.md)
-   [割り当て解除](/sql-statements/sql-statement-deallocate.md)
