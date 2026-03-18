---
title: Information_Schema Tables
summary: This page describes Information_Schema Tables in TiDB Cloud Lake.
---
## Information Schema

| Table                                        | Description                                    |
|----------------------------------------------|------------------------------------------------|
| [tables](/tidb-cloud-lake/sql/information-schema-tables-sql.md)       | ANSI SQL standard metadata view for tables.    |
| [schemata](/tidb-cloud-lake/sql/information-schema-schemata-sql.md) | ANSI SQL standard metadata view for databases. |
| [views](/tidb-cloud-lake/sql/information-schema-views-sql.md)         | ANSI SQL standard metadata view for views.     |
| [keywords](/tidb-cloud-lake/sql/information-schema-keywords-sql.md)   | ANSI SQL standard metadata view for keywords.  |
| [columns](/tidb-cloud-lake/sql/information-schema-columns-sql.md)     | ANSI SQL standard metadata view for columns.   |


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