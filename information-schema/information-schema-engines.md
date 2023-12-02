---
title: ENGINES
summary: Learn the `ENGINES` information_schema table.
---

# エンジン {#engines}

表`ENGINES`は、storageエンジンに関する情報を示します。互換性のために、TiDB は常に InnoDB をサポートされる唯一のエンジンとして説明します。また、 `ENGINES`テーブルの他の列の値も固定値です。

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

```sql
SELECT * FROM engines;
```

    +--------+---------+------------------------------------------------------------+--------------+------+------------+
    | ENGINE | SUPPORT | COMMENT                                                    | TRANSACTIONS | XA   | SAVEPOINTS |
    +--------+---------+------------------------------------------------------------+--------------+------+------------+
    | InnoDB | DEFAULT | Supports transactions, row-level locking, and foreign keys | YES          | YES  | YES        |
    +--------+---------+------------------------------------------------------------+--------------+------+------------+
    1 row in set (0.01 sec)

`ENGINES`のテーブルの列の説明は次のとおりです。

-   `ENGINES` :storageエンジンの名前。
-   `SUPPORT` :サーバーがstorageエンジン上で持つサポートのレベル。 TiDB では、値は常に`DEFAULT`です。
-   `COMMENT` :storageエンジンに関する簡単なコメント。
-   `TRANSACTIONS` :storageエンジンがトランザクションをサポートするかどうか。
-   `XA` :storageエンジンが XA トランザクションをサポートするかどうか。
-   `SAVEPOINTS` :storageエンジンが`savepoints`をサポートするかどうか。
