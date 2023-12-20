---
title: KEYWORDS
summary: Learn the `KEYWORDS` INFORMATION_SCHEMA table.
---

# KEYWORDS

The `KEYWORDS` table provides information about [keywords](/keywords.md).

```sql
USE INFORMATION_SCHEMA;
DESC keywords;
```

The output is as follows:

```
+----------+--------------+------+------+---------+-------+
| Field    | Type         | Null | Key  | Default | Extra |
+----------+--------------+------+------+---------+-------+
| WORD     | varchar(128) | YES  |      | NULL    |       |
| RESERVED | int(11)      | YES  |      | NULL    |       |
+----------+--------------+------+------+---------+-------+
2 rows in set (0.00 sec)
```

The following statement queries the information about `ADD` and `USER` keywords:

```sql
SELECT * FROM keywords
WHERE WORD IN ('ADD','USER')
```

```
+------+----------+
| WORD | RESERVED |
+------+----------+
| ADD  |        1 |
| USER |        0 |
+------+----------+
2 rows in set (0.00 sec)
```

Here you can see that `ADD` is a reserved keyword and `USER` is a non-reserved keyword.
