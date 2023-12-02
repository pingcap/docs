---
title: SHOW CREATE SEQUENCE
summary: An overview of the usage of SHOW CREATE SEQUENCE for the TiDB database.
---

# シーケンスの作成を表示 {#show-create-sequence}

`SHOW CREATE SEQUENCE` `SHOW CREATE TABLE`と同様にシーケンスの詳細情報を示します。

## あらすじ {#synopsis}

**ShowCreateSequenceStmt:**

![ShowCreateSequenceStmt](/media/sqlgram/ShowCreateSequenceStmt.png)

**テーブル名:**

![TableName](/media/sqlgram/TableName.png)

## 例 {#examples}

```sql
CREATE SEQUENCE seq;
```

    Query OK, 0 rows affected (0.03 sec)

```sql
SHOW CREATE SEQUENCE seq;
```

    +-------+----------------------------------------------------------------------------------------------------------------------------+
    | Table | Create Table                                                                                                               |
    +-------+----------------------------------------------------------------------------------------------------------------------------+
    | seq   | CREATE SEQUENCE `seq` start with 1 minvalue 1 maxvalue 9223372036854775806 increment by 1 cache 1000 nocycle ENGINE=InnoDB |
    +-------+----------------------------------------------------------------------------------------------------------------------------+
    1 row in set (0.00 sec)

## MySQLの互換性 {#mysql-compatibility}

このステートメントは TiDB 拡張機能です。この実装は、MariaDB で利用可能なシーケンスに基づいてモデル化されています。

## こちらも参照 {#see-also}

-   [シーケンスの作成](/sql-statements/sql-statement-create-sequence.md)
-   [ドロップシーケンス](/sql-statements/sql-statement-drop-sequence.md)
