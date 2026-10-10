---
title: RENAME TABLE
summary: テーブル名を変更します。
---

# RENAME TABLE

テーブル名を変更します。

## 構文 {#syntax}

```sql
ALTER TABLE [ IF EXISTS ] <name> RENAME TO <new_table_name>
```

## 例 {#examples}

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