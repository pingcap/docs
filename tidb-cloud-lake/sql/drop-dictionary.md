---
title: DROP DICTIONARY
summary: Deletes a dictionary.
---

# DROP DICTIONARY

Deletes a dictionary.

## Syntax

```sql
DROP DICTIONARY [ IF EXISTS ] [ <catalog_name>. ][ <database_name>. ]<dictionary_name>
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `IF EXISTS` | Optional. Suppresses the error if the dictionary does not exist. |
| `<dictionary_name>` | The dictionary name. You can qualify it with catalog and database names. |

## Examples

```sql
DROP DICTIONARY user_info;
```

```sql
DROP DICTIONARY IF EXISTS default.user_info;
```
