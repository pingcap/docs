---
title: NOT LIKE
summary: SQL パターンを使用してパターンに一致しないことを判定します。1 (TRUE) または 0 (FALSE) を返します。expr または pat のいずれかが NULL の場合、結果は NULL です。
---

# NOT LIKE

SQL パターンを使用してパターンに一致しないことを判定します。1 (TRUE) または 0 (FALSE) を返します。expr または pat のいずれかが NULL の場合、結果は NULL です。

## 構文 {#syntax}

```sql
<expr> NOT LIKE <pattern>
```

## 例 {#examples}

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