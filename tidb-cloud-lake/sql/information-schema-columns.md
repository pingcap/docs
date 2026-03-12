---
title: information_schema.columns
---

Contains information about columns of tables.

```sql
desc information_schema.columns

╭─────────────────────────────────────────────────────────────────────────╮
│           Field          │       Type       │  Null  │ Default │  Extra │
│          String          │      String      │ String │  String │ String │
├──────────────────────────┼──────────────────┼────────┼─────────┼────────┤
│ table_catalog            │ VARCHAR          │ NO     │ ''      │        │
│ table_schema             │ VARCHAR          │ NO     │ ''      │        │
│ table_name               │ VARCHAR          │ NO     │ ''      │        │
│ column_name              │ VARCHAR          │ NO     │ ''      │        │
│ ordinal_position         │ TINYINT UNSIGNED │ NO     │ 0       │        │
│ column_default           │ NULL             │ NO     │ NULL    │        │
│ column_comment           │ VARCHAR          │ NO     │ ''      │        │
│ column_key               │ NULL             │ NO     │ NULL    │        │
│ nullable                 │ TINYINT UNSIGNED │ YES    │ NULL    │        │
│ is_nullable              │ VARCHAR          │ NO     │ ''      │        │
│ data_type                │ VARCHAR          │ NO     │ ''      │        │
│ column_type              │ VARCHAR          │ NO     │ ''      │        │
│ character_maximum_length │ NULL             │ NO     │ NULL    │        │
│ character_octet_length   │ NULL             │ NO     │ NULL    │        │
│ numeric_precision        │ NULL             │ NO     │ NULL    │        │
│ numeric_precision_radix  │ NULL             │ NO     │ NULL    │        │
│ numeric_scale            │ NULL             │ NO     │ NULL    │        │
│ datetime_precision       │ NULL             │ NO     │ NULL    │        │
│ character_set_catalog    │ NULL             │ NO     │ NULL    │        │
│ character_set_schema     │ NULL             │ NO     │ NULL    │        │
│ character_set_name       │ NULL             │ NO     │ NULL    │        │
│ collation_catalog        │ NULL             │ NO     │ NULL    │        │
│ collation_schema         │ NULL             │ NO     │ NULL    │        │
│ collation_name           │ NULL             │ NO     │ NULL    │        │
│ domain_catalog           │ NULL             │ NO     │ NULL    │        │
│ domain_schema            │ NULL             │ NO     │ NULL    │        │
│ domain_name              │ NULL             │ NO     │ NULL    │        │
│ privileges               │ NULL             │ NO     │ NULL    │        │
│ default                  │ VARCHAR          │ NO     │ ''      │        │
│ extra                    │ NULL             │ NO     │ NULL    │        │
╰─────────────────────────────────────────────────────────────────────────╯

```
