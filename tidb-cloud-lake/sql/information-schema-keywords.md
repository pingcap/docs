---
title: information_schema.keywords
---

The `information_schema.keywords` system table is a view that provides all keywords in Databend

```sql
DESCRIBE information_schema.keywords

╭─────────────────────────────────────────────────────────╮
│   Field  │       Type       │  Null  │ Default │  Extra │
│  String  │      String      │ String │  String │ String │
├──────────┼──────────────────┼────────┼─────────┼────────┤
│ keywords │ VARCHAR          │ NO     │ ''      │        │
│ reserved │ TINYINT UNSIGNED │ NO     │ 0       │        │
╰─────────────────────────────────────────────────────────╯
```