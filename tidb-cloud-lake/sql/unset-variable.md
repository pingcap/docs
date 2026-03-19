---
title: UNSET VARIABLE
summary: Removes one or more variables from the current session.
---

# UNSET VARIABLE

> **Note:**
>
> Introduced or updated in v1.2.609.

Removes one or more variables from the current session.

## Syntax

```sql
-- Remove one variable
UNSET VARIABLE <variable_name>

-- Remove more than one variable
UNSET VARIABLE (<variable1>, <variable2>, ...)
```

## Examples

The following example unsets a single variable:

```sql
-- Remove the variable a from the session
UNSET VARIABLE a;
```

The following example unsets multiple variables:

```sql
-- Remove variables x and y from the session
UNSET VARIABLE (x, y);
```
