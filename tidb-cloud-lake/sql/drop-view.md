---
title: DROP VIEW
summary: 删除视图。
---

# DROP VIEW

删除视图。

## 语法 {#syntax}

```sql
DROP VIEW [ IF EXISTS ] [ <database_name>. ]view_name
```

## 示例 {#examples}

```sql
DROP VIEW IF EXISTS tmp_view;

SELECT * FROM tmp_view;
ERROR 1105 (HY000): Code: 1025, Text = Unknown table 'tmp_view'.
```