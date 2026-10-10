---
title: Information_Schema Tables
summary: このページでは、TiDB Cloud Lake の Information_Schema Tables について説明します。
---

# Information_Schema Tables

## Information Schema {#information-schema}

| Table                                        | 説明                                           |
|----------------------------------------------|------------------------------------------------|
| [tables](/tidb-cloud-lake/sql/information-schema-tables-sql.md)       | テーブル用の ANSI SQL 標準メタデータビューです。    |
| [schemata](/tidb-cloud-lake/sql/information-schema-schemata-sql.md) | データベース用の ANSI SQL 標準メタデータビューです。 |
| [views](/tidb-cloud-lake/sql/information-schema-views-sql.md)         | ビュー用の ANSI SQL 標準メタデータビューです。       |
| [keywords](/tidb-cloud-lake/sql/information-schema-keywords-sql.md)   | キーワード用の ANSI SQL 標準メタデータビューです。   |
| [columns](/tidb-cloud-lake/sql/information-schema-columns-sql.md)     | カラム用の ANSI SQL 標準メタデータビューです。       |

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