---
title: Information_Schema Tables
summary: 本页介绍 TiDB Cloud Lake 中的 Information_Schema 表。
---

# Information_Schema Tables

## Information Schema {#information-schema}

| 表 | 描述 |
|----------------------------------------------|------------------------------------------------|
| [tables](/tidb-cloud-lake/sql/information-schema-tables-sql.md)       | 用于表的 ANSI SQL 标准元信息视图。    |
| [schemata](/tidb-cloud-lake/sql/information-schema-schemata-sql.md) | 用于数据库的 ANSI SQL 标准元信息视图。 |
| [views](/tidb-cloud-lake/sql/information-schema-views-sql.md)         | 用于视图的 ANSI SQL 标准元信息视图。     |
| [keywords](/tidb-cloud-lake/sql/information-schema-keywords-sql.md)   | 用于关键字的 ANSI SQL 标准元信息视图。  |
| [columns](/tidb-cloud-lake/sql/information-schema-columns-sql.md)     | 用于列的 ANSI SQL 标准元信息视图。   |

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