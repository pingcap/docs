---
title: Object Naming Convention
summary: Introduces the object naming convention in TiDB.
---

# Object Naming Convention

Used to standardize the naming conventions for database objects such as DATABASE, TABLE, INDEX, USER, etc.

## Bedrock

- It is recommended to use meaningful words with underscores separating the words.
- Only letters, numbers, and underscores should be used for naming.
- Avoid using TiDB reserved words such as `group`, `order`, etc. as field names.
- It is recommended to use lowercase letters for all database objects.

## Database Naming Convention

It is recommended to differentiate by business, product, or other metrics, usually no more than `20` characters. For example: temporary library (tmp_crm), test library (test_crm).

## Table Naming Convention

- Use the same prefix for tables of the same business or module whenever possible, and express the meaning of the table name whenever possible.
- Multiple words are separated by underscores, and it is not recommended to exceed `32` characters.
- It is recommended to annotate the purpose of the table to facilitate uniform understanding. For example:
    - Temporary table (tmp_t_crm_relation_0425)
    - Backup table (bak_t_crm_relation_20170425)
    - Business operations temporary statistics table (`tmp_st_{business code}_{creator abbreviation}_{date}`)
    - Account period archive table (`t_crm_ec_record_YYYY{MM}{dd}`)
    - Create separate `DATABASE` for tables of different business modules and add comments accordingly.
- Currently TiDB only supports setting the `lower-case-table-names` value to `2`, which means that the table names are saved according to case and compared according to lower case (case-insensitive).

## Field Naming Convention

- Field naming needs to indicate the actual meaning of the English word or abbreviation.
- It is recommended that fields with the same meaning between tables should have the same name.
- Fields should also be annotated as much as possible, and enumerated types should indicate the meaning of the main value, e.g. "0 - offline, 1 - online".
- The boolean column is named `is_{description}`. For example, the column for a member that is enabled on the member table is named is_enabled.
- Field names are not recommended to be longer than `30` characters, and the number of fields is not recommended to be larger than `60`.
- Try to avoid using reserved words, such as `order`, `from`, `desc`, etc. Please refer to the Appendix section for official reserved words.

## Index Naming Convention

- Primary key index: `pk_{table_name_abbreviation}_{field_name_abbreviation}`
- Unique index: `uk_{table_name_abbreviation}_{field_name_abbreviation}`
- Common index: `idx_{table_name_abbreviation}_{field_name_abbreviation}`
- Multi-word column_name, taking abbreviations that are as representative as possible.