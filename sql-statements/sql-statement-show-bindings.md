---
title: SHOW [GLOBAL|SESSION] BINDINGS
summary: `SHOW BINDINGS`ステートメントは、SQLバインディングに関する情報を表示するために使用されます。`BINDING`は`GLOBAL`または`SESSION`のいずれかをベースにすることができます。デフォルトは`SESSION`です。このステートメントは、実行計画バインディングをGLOBALまたはSESSIONレベルで出力します。現在、8列を出力します。MySQLの互換性に対するTiDBの拡張機能です。
---

# [グローバル|セッション] バインディングを表示 {#show-global-session-bindings}

`SHOW BINDINGS`ステートメントは、作成された SQL バインディングに関する情報を表示するために使用されます。 `BINDING`は`GLOBAL`または`SESSION`いずれかをベースにすることができます。デフォルトは`SESSION`です。

## あらすじ {#synopsis}

**表示手順:**

![ShowStmt](/media/sqlgram/ShowStmt.png)

**ShowTargetFilterable:**

![ShowTargetFilterable](/media/sqlgram/ShowTargetFilterable.png)

**グローバルスコープ:**

![GlobalScope](/media/sqlgram/GlobalScope.png)

**ShowLikeOrWhereOpt**

![ShowLikeOrWhereOpt](/media/sqlgram/ShowLikeOrWhereOpt.png)

## 構文の説明 {#syntax-description}

```sql
SHOW [GLOBAL | SESSION] BINDINGS [ShowLikeOrWhereOpt];
```

このステートメントは、実行計画バインディングを GLOBAL または SESSION レベルで出力します。デフォルトのスコープは SESSION です。現在、 `SHOW BINDINGS`以下に示すように 8 列を出力します。

| カラム名         | 説明                                                                                                                                      |
| :----------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| オリジナル_SQL    | パラメータ化後の元の SQL ステートメント                                                                                                                  |
| バインドSQL      | ヒントを含むバインドされた SQL ステートメント                                                                                                               |
| デフォルト_データベース | デフォルトのデータベース                                                                                                                            |
| 状態           | 「使用中」、「削除」、「無効」、「拒否」、「検証保留」などのステータス                                                                                                     |
| 作成時間         | 作成時間                                                                                                                                    |
| 更新時間         | 更新時間                                                                                                                                    |
| 文字コード        | キャラクターセット                                                                                                                               |
| 照合順序         | ソートルール                                                                                                                                  |
| ソース          | バインディングの作成方法`manual` ( `create [global] binding` SQL ステートメントによって作成)、 `capture` (TiDB によって自動的にキャプチャ)、 `evolve` (TiDB によって自動的に展開) が含まれます。 |

## 例 {#examples}

```sql
mysql> CREATE TABLE t1 (
          id INT NOT NULL PRIMARY KEY auto_increment,
          b INT NOT NULL,
          pad VARBINARY(255),
          INDEX(b)
         );
Query OK, 0 rows affected (0.07 sec)

mysql> INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM dual;
Query OK, 1 row affected (0.01 sec)
Records: 1  Duplicates: 0  Warnings: 0

mysql> INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
Query OK, 1 row affected (0.00 sec)
Records: 1  Duplicates: 0  Warnings: 0

mysql> INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
Query OK, 8 rows affected (0.00 sec)
Records: 8  Duplicates: 0  Warnings: 0

mysql> INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
Query OK, 1000 rows affected (0.04 sec)
Records: 1000  Duplicates: 0  Warnings: 0

mysql> INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
Query OK, 100000 rows affected (1.74 sec)
Records: 100000  Duplicates: 0  Warnings: 0

mysql> INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
Query OK, 100000 rows affected (2.15 sec)
Records: 100000  Duplicates: 0  Warnings: 0

mysql> INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
Query OK, 100000 rows affected (2.64 sec)
Records: 100000  Duplicates: 0  Warnings: 0

mysql> SELECT SLEEP(1);
+----------+
| SLEEP(1) |
+----------+
|        0 |
+----------+
1 row in set (1.00 sec)

mysql> ANALYZE TABLE t1;
Query OK, 0 rows affected (1.33 sec)

mysql> EXPLAIN ANALYZE SELECT * FROM t1 WHERE b = 123;
+-------------------------------+---------+---------+-----------+----------------------+---------------------------------------------------------------------------+-----------------------------------+----------------+------+
| id                            | estRows | actRows | task      | access object        | execution info                                                            | operator info                     | memory         | disk |
+-------------------------------+---------+---------+-----------+----------------------+---------------------------------------------------------------------------+-----------------------------------+----------------+------+
| IndexLookUp_10                | 583.00  | 297     | root      |                      | time:10.545072ms, loops:2, rpc num: 1, rpc time:398.359µs, proc keys:297  |                                   | 109.1484375 KB | N/A  |
| ├─IndexRangeScan_8(Build)     | 583.00  | 297     | cop[tikv] | table:t1, index:b(b) | time:0s, loops:4                                                          | range:[123,123], keep order:false | N/A            | N/A  |
| └─TableRowIDScan_9(Probe)     | 583.00  | 297     | cop[tikv] | table:t1             | time:12ms, loops:4                                                        | keep order:false                  | N/A            | N/A  |
+-------------------------------+---------+---------+-----------+----------------------+---------------------------------------------------------------------------+-----------------------------------+----------------+------+
3 rows in set (0.02 sec)

mysql> CREATE SESSION BINDING FOR
         SELECT * FROM t1 WHERE b = 123
        USING
         SELECT * FROM t1 IGNORE INDEX (b) WHERE b = 123;
Query OK, 0 rows affected (0.00 sec)

mysql> EXPLAIN ANALYZE SELECT * FROM t1 WHERE b = 123;
+-------------------------+-----------+---------+-----------+---------------+--------------------------------------------------------------------------------+--------------------+---------------+------+
| id                      | estRows   | actRows | task      | access object | execution info                                                                 | operator info      | memory        | disk |
+-------------------------+-----------+---------+-----------+---------------+--------------------------------------------------------------------------------+--------------------+---------------+------+
| TableReader_7           | 583.00    | 297     | root      |               | time:222.32506ms, loops:2, rpc num: 1, rpc time:222.078952ms, proc keys:301010 | data:Selection_6   | 88.6640625 KB | N/A  |
| └─Selection_6           | 583.00    | 297     | cop[tikv] |               | time:224ms, loops:298                                                          | eq(test.t1.b, 123) | N/A           | N/A  |
|   └─TableFullScan_5     | 301010.00 | 301010  | cop[tikv] | table:t1      | time:220ms, loops:298                                                          | keep order:false   | N/A           | N/A  |
+-------------------------+-----------+---------+-----------+---------------+--------------------------------------------------------------------------------+--------------------+---------------+------+
3 rows in set (0.22 sec)

mysql> SHOW SESSION BINDINGS\G
*************************** 1. row ***************************
Original_sql: select * from t1 where b = ?
    Bind_sql: SELECT * FROM t1 IGNORE INDEX (b) WHERE b = 123
  Default_db: test
      Status: using
 Create_time: 2020-05-22 14:38:03.456
 Update_time: 2020-05-22 14:38:03.456
     Charset: utf8mb4
   Collation: utf8mb4_0900_ai_ci
1 row in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [[グローバル|セッション] バインディングの作成](/sql-statements/sql-statement-create-binding.md)
-   [[グローバル|セッション] バインディングを削除します](/sql-statements/sql-statement-drop-binding.md)
-   [分析テーブル](/sql-statements/sql-statement-analyze-table.md)
-   [オプティマイザーのヒント](/optimizer-hints.md)
-   [SQL計画管理](/sql-plan-management.md)
