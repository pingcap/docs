---
title: RENAME TABLE
summary: 更改表的名称。
---

# RENAME TABLE

更改表的名称。

## 语法 {#syntax}

```sql
ALTER TABLE [ IF EXISTS ] <name> RENAME TO <new_table_name>
```

## 示例 {#examples}

```sql
CREATE TABLE test(a INT);
```

```sql
SHOW TABLES;
+------+
| name |
+------+
| test |
+------+
```

```sql
ALTER TABLE `test` RENAME TO `new_test`;
```

```sql
SHOW TABLES;
+----------+
| name     |
+----------+
| new_test |
+----------+
```