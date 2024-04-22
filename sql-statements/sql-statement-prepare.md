---
title: PREPARE | TiDB SQL Statement Reference
summary: PREPAREステートメントは、サーバー側のプリペアド ステートメントへのSQLインターフェイスを提供します。MySQLの互換性があります。EXECUTEステートメントを使用してプリペアド ステートメントを実行し、DEALLOCATEステートメントを使用して解放します。
---

# 準備する {#prepare}

`PREPARE`ステートメントは、サーバー側のプリペアド ステートメントへの SQL インターフェイスを提供します。

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

TiDB の`PREPARE`ステートメントは MySQL と完全な互換性があります。互換性の違いが見つかった場合は、 [バグを報告](https://docs.pingcap.com/tidb/stable/support) .

## こちらも参照 {#see-also}

-   [実行する](/sql-statements/sql-statement-execute.md)
-   [割り当てを解除する](/sql-statements/sql-statement-deallocate.md)
