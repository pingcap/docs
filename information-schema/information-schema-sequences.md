---
title: SEQUENCES
summary: SEQUENCES INFORMATION_SCHEMA テーブルについて学習します。
---

# シーケンス {#sequences}

`SEQUENCES`テーブルはシーケンスに関する情報を提供します。3 [シーケンス機能](/sql-statements/sql-statement-create-sequence.md) MariaDB の同様の機能に基づいてモデル化されています。

```sql
USE INFORMATION_SCHEMA;
DESC SEQUENCES;
```

出力は次のようになります。

```sql
+-----------------+--------------+------+------+---------+-------+
| Field           | Type         | Null | Key  | Default | Extra |
+-----------------+--------------+------+------+---------+-------+
| TABLE_CATALOG   | varchar(512) | NO   |      | NULL    |       |
| SEQUENCE_SCHEMA | varchar(64)  | NO   |      | NULL    |       |
| SEQUENCE_NAME   | varchar(64)  | NO   |      | NULL    |       |
| CACHE           | tinyint(0)   | NO   |      | NULL    |       |
| CACHE_VALUE     | bigint(21)   | YES  |      | NULL    |       |
| CYCLE           | tinyint(0)   | NO   |      | NULL    |       |
| INCREMENT       | bigint(21)   | NO   |      | NULL    |       |
| MAX_VALUE       | bigint(21)   | YES  |      | NULL    |       |
| MIN_VALUE       | bigint(21)   | YES  |      | NULL    |       |
| START           | bigint(21)   | YES  |      | NULL    |       |
| COMMENT         | varchar(64)  | YES  |      | NULL    |       |
+-----------------+--------------+------+------+---------+-------+
11 rows in set (0.00 sec)
```

シーケンス`test.seq`を作成し、シーケンスの次の値を照会します。

```sql
CREATE SEQUENCE test.seq;
SELECT NEXTVAL(test.seq);
SELECT * FROM sequences\G
```

出力は次のようになります。

```sql
+-------------------+
| NEXTVAL(test.seq) |
+-------------------+
|                 1 |
+-------------------+
1 row in set (0.01 sec)
```

すべてのシーケンスをビュー:

```sql
SELECT * FROM SEQUENCES\G
```

出力は次のようになります。

```sql
*************************** 1. row ***************************
  TABLE_CATALOG: def
SEQUENCE_SCHEMA: test
  SEQUENCE_NAME: seq
          CACHE: 1
    CACHE_VALUE: 1000
          CYCLE: 0
      INCREMENT: 1
      MAX_VALUE: 9223372036854775806
      MIN_VALUE: 1
          START: 1
        COMMENT:
1 row in set (0.00 sec)
```

## 参照 {#see-also}

-   [`CREATE SEQUENCE`](/sql-statements/sql-statement-create-sequence.md)
-   [`SHOW CREATE SEQUENCE`](/sql-statements/sql-statement-show-create-sequence.md)
-   [`ALTER SEQUENCE`](/sql-statements/sql-statement-alter-sequence.md)
-   [`DROP SEQUENCE`](/sql-statements/sql-statement-drop-sequence.md)
-   [シーケンス関数](/functions-and-operators/sequence-functions.md)
