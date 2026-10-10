---
title: DROP VIEW
summary: ビューを削除します。
---

# DROP VIEW

ビューを削除します。

## 構文 {#syntax}

```sql
DROP VIEW [ IF EXISTS ] [ <database_name>. ]view_name
```

## 例 {#examples}

```sql
DROP VIEW IF EXISTS tmp_view;

SELECT * FROM tmp_view;
ERROR 1105 (HY000): Code: 1025, Text = Unknown table 'tmp_view'.
```