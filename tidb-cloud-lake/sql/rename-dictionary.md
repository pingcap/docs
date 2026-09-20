---
title: RENAME DICTIONARY
summary: Renames a dictionary.
---

# RENAME DICTIONARY

Renames a dictionary.

## Syntax

```sql
RENAME DICTIONARY [ IF EXISTS ]
    [ <catalog_name>. ][ <database_name>. ]<dictionary_name>
    TO [ <new_catalog_name>. ][ <new_database_name>. ]<new_dictionary_name>
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `IF EXISTS` | Optional. Suppresses the error if the source dictionary does not exist. |
| `<dictionary_name>` | The current dictionary name. |
| `<new_dictionary_name>` | The new dictionary name. |

## Examples

```sql
RENAME DICTIONARY user_info TO user_profile;
```

```sql
RENAME DICTIONARY IF EXISTS default.user_info TO analytics.user_profile;
```
