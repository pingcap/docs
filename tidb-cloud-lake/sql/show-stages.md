---
title: SHOW STAGES
summary: Returns a list of the created stages. The output list does not include the user stage.
---
Returns a list of the created stages. The output list does not include the user stage.

## Syntax

```sql
SHOW STAGES;
```

## Examples

```sql
SHOW STAGES;

---
name|stage_type|number_of_files|creator   |comment|
----+----------+---------------+----------+-------+
eric|Internal  |              0|'root'@'%'|       |
```