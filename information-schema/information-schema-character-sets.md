---
title: CHARACTER_SETS
summary: Learn the `CHARACTER_SETS` information_schema table.
---

# CHARACTER_SETS {#character-sets}

`CHARACTER_SETS`の表は、 [文字セット](/character-set-and-collation.md)に関する情報を提供します。現在、TiDBは一部の文字セットのみをサポートしています。

{{< copyable "" >}}

```sql
USE information_schema;
DESC character_sets;
```

```
+----------------------+-------------+------+------+---------+-------+
| Field                | Type        | Null | Key  | Default | Extra |
+----------------------+-------------+------+------+---------+-------+
| CHARACTER_SET_NAME   | varchar(32) | YES  |      | NULL    |       |
| DEFAULT_COLLATE_NAME | varchar(32) | YES  |      | NULL    |       |
| DESCRIPTION          | varchar(60) | YES  |      | NULL    |       |
| MAXLEN               | bigint(3)   | YES  |      | NULL    |       |
+----------------------+-------------+------+------+---------+-------+
4 rows in set (0.00 sec)
```

{{< copyable "" >}}

```sql
SELECT * FROM `character_sets`;
```

```
+--------------------+----------------------+---------------+--------+
| CHARACTER_SET_NAME | DEFAULT_COLLATE_NAME | DESCRIPTION   | MAXLEN |
+--------------------+----------------------+---------------+--------+
| utf8               | utf8_bin             | UTF-8 Unicode |      3 |
| utf8mb4            | utf8mb4_bin          | UTF-8 Unicode |      4 |
| ascii              | ascii_bin            | US ASCII      |      1 |
| latin1             | latin1_bin           | Latin1        |      1 |
| binary             | binary               | binary        |      1 |
+--------------------+----------------------+---------------+--------+
5 rows in set (0.00 sec)
```

`CHARACTER_SETS`テーブルの列の説明は次のとおりです。

-   `CHARACTER_SET_NAME` ：文字セットの名前。
-   `DEFAULT_COLLATE_NAME`文字セットのデフォルトの照合順序名。
-   `DESCRIPTION`文字セットの説明。
-   `MAXLEN`この文字セットに文字を格納するために必要な最大長。
