---
title: information_schema.keywords
summary: information_schema.keywords システムテーブルは、{{{ .lake }}} のすべてのキーワードを提供するビューです。
---

# information_schema.keywords

`information_schema.keywords` システムテーブルは、{{{ .lake }}} のすべてのキーワードを提供するビューです。

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