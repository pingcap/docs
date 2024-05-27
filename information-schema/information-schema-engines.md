---
title: ENGINES
summary: ENGINES information_schema テーブルについて学習します。
---

# エンジン {#engines}

`ENGINES`テーブルはstorageエンジンに関する情報を提供します。互換性のため、TiDB は常に InnoDB のみをサポートするエンジンとして記述します。また、 `ENGINES`テーブルの他の列の値も固定値です。

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

`ENGINES`表の列の説明は次のとおりです。

-   `ENGINES` :storageエンジンの名前。
-   `SUPPORT` :サーバーがstorageエンジンに対して持つサポート レベル。TiDB では、値は常に`DEFAULT`です。
-   `COMMENT` :storageエンジンに関する簡単なコメント。
-   `TRANSACTIONS` :storageエンジンがトランザクションをサポートするかどうか。
-   `XA` :storageエンジンが XA トランザクションをサポートするかどうか。
-   `SAVEPOINTS` :storageエンジンが`savepoints`サポートするかどうか。

## 参照 {#see-also}

-   [`SHOW ENGINES`](/sql-statements/sql-statement-show-engines.md)
