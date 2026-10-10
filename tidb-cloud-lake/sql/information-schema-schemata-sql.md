---
title: information_schema.schemata
summary: システム内のすべてのデータベースに関するメタデータを提供します。
---

# information_schema.schemata

システム内のすべてのデータベースに関するメタデータを提供します。

```sql
desc information_schema.schemata

╭─────────────────────────────────────────────────────────────────────╮
│             Field             │   Type  │  Null  │ Default │  Extra │
│             String            │  String │ String │  String │ String │
├───────────────────────────────┼─────────┼────────┼─────────┼────────┤
│ catalog_name                  │ VARCHAR │ NO     │ ''      │        │
│ schema_name                   │ VARCHAR │ NO     │ ''      │        │
│ schema_owner                  │ VARCHAR │ NO     │ ''      │        │
│ default_character_set_catalog │ NULL    │ NO     │ NULL    │        │
│ default_character_set_schema  │ NULL    │ NO     │ NULL    │        │
│ default_character_set_name    │ NULL    │ NO     │ NULL    │        │
│ default_collation_name        │ NULL    │ NO     │ NULL    │        │
│ sql_path                      │ NULL    │ NO     │ NULL    │        │
╰─────────────────────────────────────────────────────────────────────╯
```