---
title: LIKE
summary: SQL パターンを使用したパターンマッチング。1 (TRUE) または 0 (FALSE) を返します。expr または pat のいずれかが NULL の場合、結果は NULL です。
---

# LIKE

SQL パターンを使用したパターンマッチングです。1 (TRUE) または 0 (FALSE) を返します。expr または pat のいずれかが NULL の場合、結果は NULL です。

## 構文 {#syntax}

```sql
<expr> LIKE <pattern>
```

## 例 {#examples}

```sql
SELECT name, category FROM system.functions WHERE name like 'tou%' ORDER BY name;
+----------+------------+
| name     | category   |
+----------+------------+
| touint16 | conversion |
| touint32 | conversion |
| touint64 | conversion |
| touint8  | conversion |
+----------+------------+
```