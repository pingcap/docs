---
title: SHOW ENGINES | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW ENGINES for the TiDB database.
---

# エンジンを表示 {#show-engines}

このステートメントは、サポートされているすべてのストレージエンジンを一覧表示するために使用されます。構文は、MySQLとの互換性のためにのみ含まれています。

## あらすじ {#synopsis}

**ShowEnginesStmt：**

![ShowEnginesStmt](/media/sqlgram/ShowEnginesStmt.png)

```sql
SHOW ENGINES
```

## 例 {#examples}

```sql
mysql> SHOW ENGINES;
+--------+---------+------------------------------------------------------------+--------------+------+------------+
| Engine | Support | Comment                                                    | Transactions | XA   | Savepoints |
+--------+---------+------------------------------------------------------------+--------------+------+------------+
| InnoDB | DEFAULT | Supports transactions, row-level locking, and foreign keys | YES          | YES  | YES        |
+--------+---------+------------------------------------------------------------+--------------+------+------------+
1 row in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

-   このステートメントは、サポートされているエンジンとして常にInnoDBのみを返します。内部的には、TiDBは通常TiKVをストレージエンジンとして使用します。
