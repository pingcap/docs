---
title: DROP FILE FORMAT
summary: ファイル形式を削除します。
---

# DROP FILE FORMAT

ファイル形式を削除します。

## 構文 {#syntax}

```sql
DROP FILE FORMAT [ IF EXISTS ] <format_name>;
```

## 例 {#examples}

```sql
DROP FILE FORMAT IF EXISTS my_custom_csv;
```