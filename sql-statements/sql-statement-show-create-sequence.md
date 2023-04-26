---
title: SHOW CREATE SEQUENCE
summary: An overview of the usage of SHOW CREATE SEQUENCE for the TiDB database.
---

# 作成シーケンスを表示 {#show-create-sequence}

`SHOW CREATE SEQUENCE` `SHOW CREATE TABLE`と同様にシーケンスの詳細情報を示します。

## あらすじ {#synopsis}

**ShowCreateSequenceStmt:**

![ShowCreateSequenceStmt](/media/sqlgram/ShowCreateSequenceStmt.png)

**テーブル名:**

![TableName](/media/sqlgram/TableName.png)

## 例 {#examples}

{{< copyable "" >}}

```sql
CREATE SEQUENCE seq;
```

```
Query OK, 0 rows affected (0.03 sec)
```

{{< copyable "" >}}

```sql
SHOW CREATE SEQUENCE seq;
```

```
+-------+----------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                               |
+-------+----------------------------------------------------------------------------------------------------------------------------+
| seq   | CREATE SEQUENCE `seq` start with 1 minvalue 1 maxvalue 9223372036854775806 increment by 1 cache 1000 nocycle ENGINE=InnoDB |
+-------+----------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## MySQL の互換性 {#mysql-compatibility}

このステートメントは TiDB 拡張機能です。実装は、MariaDB で利用可能なシーケンスをモデルにしています。

## こちらもご覧ください {#see-also}

-   [シーケンスを作成](/sql-statements/sql-statement-create-sequence.md)
-   [ドロップシーケンス](/sql-statements/sql-statement-drop-sequence.md)
