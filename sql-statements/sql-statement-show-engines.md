---
title: SHOW ENGINES | TiDB SQL Statement Reference
summary: このステートメントは、サポートされているすべてのstorageエンジンを一覧表示するために使用されます。MySQLとの互換性を維持するためにのみ含まれています。このステートメントは常に、サポートされているエンジンとしてInnoDBのみを返します。内部的には、TiDBは通常、storageエンジンとしてTiKVを使用します。
---

# ショーエンジン {#show-engines}

このステートメントは、サポートされているすべてのstorageエンジンを一覧表示するために使用されます。この構文は、MySQL との互換性を維持するためにのみ含まれています。

## あらすじ {#synopsis}

**ShowEnginesStmt:**

![ShowEnginesStmt](/media/sqlgram/ShowEnginesStmt.png)

```sql
SHOW ENGINES;
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

-   このステートメントは常に、サポートされているエンジンとして InnoDB のみを返します。内部的には、TiDB は通常、storageエンジンとして TiKV を使用します。
