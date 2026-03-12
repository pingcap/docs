---
title: Information_Schema Tables
---

## Information Schema

| Table                                        | Description                                    |
|----------------------------------------------|------------------------------------------------|
| [tables](information-schema-tables.md)       | ANSI SQL standard metadata view for tables.    |
| [schemata](information-schema-schemata.md) | ANSI SQL standard metadata view for databases. |
| [views](information-schema-views.md)         | ANSI SQL standard metadata view for views.     |
| [keywords](information-schema-keywords.md)   | ANSI SQL standard metadata view for keywords.  |
| [columns](information-schema-columns.md)     | ANSI SQL standard metadata view for columns.   |


```sql
SHOW VIEWS FROM INFORMATION_SCHEMA;
╭─────────────────────────────╮
│ Views_in_information_schema │
│            String           │
├─────────────────────────────┤
│ columns                     │
│ key_column_usage            │
│ keywords                    │
│ schemata                    │
│ statistics                  │
│ tables                      │
│ views                       │
╰─────────────────────────────╯

```