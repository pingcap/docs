---
title: CHARACTER_SETS
summary: Learn the `CHARACTER_SETS` INFORMATION_SCHEMA table.
---

# CHARACTER_SETS {#character-sets}

`CHARACTER_SETS`表は[文字セット](/character-set-and-collation.md)に関する情報を提供します。現在、TiDB は一部の文字セットのみをサポートしています。

```sql
USE INFORMATION_SCHEMA;
DESC CHARACTER_SETS;
```

出力は次のとおりです。

    +----------------------+-------------+------+------+---------+-------+
    | Field                | Type        | Null | Key  | Default | Extra |
    +----------------------+-------------+------+------+---------+-------+
    | CHARACTER_SET_NAME   | varchar(32) | YES  |      | NULL    |       |
    | DEFAULT_COLLATE_NAME | varchar(32) | YES  |      | NULL    |       |
    | DESCRIPTION          | varchar(60) | YES  |      | NULL    |       |
    | MAXLEN               | bigint(3)   | YES  |      | NULL    |       |
    +----------------------+-------------+------+------+---------+-------+
    4 rows in set (0.00 sec)

`CHARACTER_SETS`テーブルをビュー。

```sql
SELECT * FROM `CHARACTER_SETS`;
```

出力は次のとおりです。

```sql
+--------------------+----------------------+-------------------------------------+--------+
| CHARACTER_SET_NAME | DEFAULT_COLLATE_NAME | DESCRIPTION                         | MAXLEN |
+--------------------+----------------------+-------------------------------------+--------+
| ascii              | ascii_bin            | US ASCII                            |      1 |
| binary             | binary               | binary                              |      1 |
| gbk                | gbk_chinese_ci       | Chinese Internal Code Specification |      2 |
| latin1             | latin1_bin           | Latin1                              |      1 |
| utf8               | utf8_bin             | UTF-8 Unicode                       |      3 |
| utf8mb4            | utf8mb4_bin          | UTF-8 Unicode                       |      4 |
+--------------------+----------------------+-------------------------------------+--------+
6 rows in set (0.00 sec)
```

`CHARACTER_SETS`のテーブルの列の説明は次のとおりです。

-   `CHARACTER_SET_NAME` : 文字セットの名前。
-   `DEFAULT_COLLATE_NAME`文字セットのデフォルトの照合順序名。
-   `DESCRIPTION`文字セットの説明。
-   `MAXLEN`この文字セットに文字を格納するために必要な最大長。
