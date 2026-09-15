---
title: NOT LIKE
summary: 使用 SQL 模式进行不匹配。返回 1 (TRUE) 或 0 (FALSE)。如果 expr 或 pat 任一为 NULL，结果为 NULL。
---

# NOT LIKE

使用 SQL 模式进行不匹配。返回 1 (TRUE) 或 0 (FALSE)。如果 expr 或 pat 任一为 NULL，结果为 NULL。

## 语法 {#syntax}

```sql
<expr> NOT LIKE <pattern>
```

## 示例 {#examples}

```sql
SELECT name, category FROM system.functions WHERE name like 'tou%' AND name not like '%64' ORDER BY name;
+----------+------------+
| name     | category   |
+----------+------------+
| touint16 | conversion |
| touint32 | conversion |
| touint8  | conversion |
+----------+------------+
```