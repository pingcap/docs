---
title: ENGINES
summary: Learn the `ENGINES` information_schema table.
---

# エンジン {#engines}

`ENGINES`テーブルは、storageエンジンに関する情報を提供します。互換性のために、TiDB は常に InnoDB をサポートされている唯一のエンジンとして記述します。また、表`ENGINES`の他の列の値も固定値です。

{{< copyable "" >}}

```sql
USE information_schema;
DESC engines;
```

```sql
+--------------+-------------+------+------+---------+-------+
| Field        | Type        | Null | Key  | Default | Extra |
+--------------+-------------+------+------+---------+-------+
| ENGINE       | varchar(64) | YES  |      | NULL    |       |
| SUPPORT      | varchar(8)  | YES  |      | NULL    |       |
| COMMENT      | varchar(80) | YES  |      | NULL    |       |
| TRANSACTIONS | varchar(3)  | YES  |      | NULL    |       |
| XA           | varchar(3)  | YES  |      | NULL    |       |
| SAVEPOINTS   | varchar(3)  | YES  |      | NULL    |       |
+--------------+-------------+------+------+---------+-------+
6 rows in set (0.00 sec)
```

{{< copyable "" >}}

```sql
SELECT * FROM engines;
```

```
+--------+---------+------------------------------------------------------------+--------------+------+------------+
| ENGINE | SUPPORT | COMMENT                                                    | TRANSACTIONS | XA   | SAVEPOINTS |
+--------+---------+------------------------------------------------------------+--------------+------+------------+
| InnoDB | DEFAULT | Supports transactions, row-level locking, and foreign keys | YES          | YES  | YES        |
+--------+---------+------------------------------------------------------------+--------------+------+------------+
1 row in set (0.01 sec)
```

`ENGINES`テーブルの列の説明は次のとおりです。

-   `ENGINES` :storageエンジンの名前。
-   `SUPPORT` :storageエンジンに対するサーバーのサポート レベル。 TiDB では、値は常に`DEFAULT`です。
-   `COMMENT` :storageエンジンに関する簡単なコメント。
-   `TRANSACTIONS` :storageエンジンがトランザクションをサポートするかどうか。
-   `XA` :storageエンジンが XA トランザクションをサポートするかどうか。
-   `SAVEPOINTS` :storageエンジンが`savepoints`をサポートしているかどうか。
