---
title: information_schema.keywords
summary: information_schema.keywords 系统表是一个视图，提供 {{{ .lake }}} 中的所有关键字。
---

# information_schema.keywords

`information_schema.keywords` 系统表是一个视图，提供 {{{ .lake }}} 中的所有关键字。

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