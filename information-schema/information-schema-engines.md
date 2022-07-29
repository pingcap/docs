---
title: ENGINES
summary: Learn the `ENGINES` information_schema table.
---

# エンジン {#engines}

`ENGINES`の表は、ストレージエンジンに関する情報を提供します。互換性のために、TiDBは常にInnoDBを唯一のサポートされているエンジンとして説明します。また、 `ENGINES`の表の他の列の値も固定値です。

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

-   `ENGINES` ：ストレージエンジンの名前。
-   `SUPPORT` ：サーバーがストレージエンジンに対して持っているサポートのレベル。 TiDBでは、値は常に`DEFAULT`です。
-   `COMMENT` ：ストレージエンジンに関する簡単なコメント。
-   `TRANSACTIONS` ：ストレージエンジンがトランザクションをサポートするかどうか。
-   `XA` ：ストレージエンジンがXAトランザクションをサポートするかどうか。
-   `SAVEPOINTS` ：ストレージエンジンが`savepoints`をサポートするかどうか。
