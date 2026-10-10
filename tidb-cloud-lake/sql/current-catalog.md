---
title: CURRENT_CATALOG
summary: セッションで現在使用中のカタログ名を返します。
---

# CURRENT_CATALOG

セッションで現在使用中のカタログ名を返します。

## 構文 {#syntax}

```sql
CURRENT_CATALOG()
```

## 例 {#examples}

```sql
SELECT CURRENT_CATALOG();

┌───────────────────┐
│ current_catalog() │
├───────────────────┤
│ default           │
└───────────────────┘
```