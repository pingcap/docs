---
title: information_schema.schemata
summary: 提供系统中所有数据库的元信息。
---

# information_schema.schemata

提供系统中所有数据库的元信息。

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