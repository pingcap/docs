---
title: PREPARE | TiDB SQL Statement Reference
summary: TiDB データベースの PREPARE の使用法の概要。
---

# 準備する {#prepare}

`PREPARE`ステートメントは、サーバー側の準備済みステートメントへの SQL インターフェイスを提供します。

## 概要 {#synopsis}

```ebnf+diagram
PreparedStmt ::=
    'PREPARE' Identifier 'FROM' PrepareSQL

PrepareSQL ::=
    stringLit
|   UserVariable
```

> **注記：**
>
> `PREPARE`ステートメントごとに、プレースホルダーの最大数は 65535 です。

現在の TiDB インスタンス内の`PREPARE`ステートメントの数を制限するには、 [`max_prepared_stmt_count`](/system-variables.md#max_prepared_stmt_count)システム変数を使用できます。

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

## MySQL 互換性 {#mysql-compatibility}

TiDB の`PREPARE`ステートメントは MySQL と完全に互換性があります。互換性の違いが見つかった場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support) 。

## 参照 {#see-also}

-   [実行する](/sql-statements/sql-statement-execute.md)
-   [割り当て解除](/sql-statements/sql-statement-deallocate.md)
