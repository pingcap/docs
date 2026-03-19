---
title: EXECUTE IMMEDIATE
summary: Executes a SQL script. For how to write SQL scripts for Databend, see Stored Procedure & SQL Scripting.
---

# EXECUTE IMMEDIATE

> **Note:**
>
> Introduced or updated in v1.2.452.

Executes a SQL script. For how to write SQL scripts for Databend, see [Stored Procedure & SQL Scripting](/tidb-cloud-lake/sql/stored-procedure-scripting.md).

## Syntax

```sql
EXECUTE IMMEDIATE $$
BEGIN
    <procedure_body>
    RETURN <return_value>;             -- Use to return a single value
    -- OR
    RETURN TABLE(<select_query>);      -- Use to return a table
END;
$$;
```

## Examples

This example uses a loop to increment sum by iterating from -1 to 2, and the result is the sum (2):

```sql
EXECUTE IMMEDIATE $$
BEGIN
    LET x := -1;
    LET sum := 0;
    FOR x IN x TO x + 3 DO
        sum := sum + x;
    END FOR;
    RETURN sum;
END;
$$;

┌────────┐
│ Result │
│ String │
├────────┤
│ 2      │
└────────┘
```

The following example returns a table with a column `1 + 1` and the value 2:

```sql
EXECUTE IMMEDIATE $$
BEGIN
    LET x := 1;
    RETURN TABLE(SELECT :x + 1);
END;
$$;

┌───────────┐
│   Result  │
│   String  │
├───────────┤
│ ┌───────┐ │
│ │ 1 + 1 │ │
│ │ UInt8 │ │
│ ├───────┤ │
│ │     2 │ │
│ └───────┘ │
└───────────┘
```
