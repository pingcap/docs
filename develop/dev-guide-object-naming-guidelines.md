---
title: Object Naming Convention
summary: Introduces the object naming convention in TiDB.
---

# Object Naming Convention

This document introduces the rules for naming database objects, such as DATABASE, TABLE, INDEX, USER.

## Bedrock

- It is recommended to use meaningful English words separated by underscores.
- Name can only contain letters, numbers, and underscores.
- Avoid using TiDB reserved words, such as `group`, `order`, as a field name.
- It is recommended to use lowercase letters for all database objects.

## Database Naming Convention

It is recommended to differentiate names by business, product, or other metrics, generally no more than 20 characters. For example: temporary library (tmp_crm), test library (test_crm).

## Table Naming Convention

- Use the same prefix for tables of the same business or module and the name should express it's meaning of as much as possible.
- Multiple words are separated by underscores, and it is not recommended to exceed 32 characters.
- It is recommended to annotate the purpose of the table for understanding. For example:
    - Temporary table: `tmp_t_crm_relation_0425`
    - Backup table: `bak_t_crm_relation_20170425`
    - Temporary table of business operations: `tmp_st_{business code}_{creator abbreviation}_{date}`
    - Record table of accounts period: `t_crm_ec_record_YYYY{MM}{dd}`
- Create separate DATABASE for tables of different business modules and add annotations accordingly.
- Currently, TiDB only supports setting the value of `lower-case-table-names` to `2`. This means it is case-sensitive when you save a table name, but case-insensitive when you compare table names. The comparison is based on the lower case.

## Field Naming Convention

- The field naming is the actual meaning or abbreviation of the field.
- It is recommended to use the same name between tables with the same meaning field.
- It is recommended to add annotations to the field and specify named values for enumerated type, such as "0: offline, 1: online".
- It is recommended to name the boolean column as `is_{description}`. For example, the column of a `member` table which indicates whether the member is enabled, can be named as `is_enabled`.
- It is not recommended to name a field with more than 30 characters, and the number of fields should be less than 60.
- Avoid using TiDB reserved words, such as `order`, `from`, `desc`. For more information, refer to the TiDB reserved words.

## Index Naming Convention

- Primary key index: `pk_{table_name_abbreviation}_{field_name_abbreviation}`
- Unique index: `uk_{table_name_abbreviation}_{field_name_abbreviation}`
- Common index: `idx_{table_name_abbreviation}_{field_name_abbreviation}`
- Multi-word column name: use meaningful abbreviations