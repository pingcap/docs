---
title: CALL PROCEDURE
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.637"/>

Executes a stored procedure by calling its name, optionally passing arguments if the procedure requires them.

## Syntax

```sql
CALL PROCEDURE <procedure_name>([<argument1>, <argument2>, ...])
```

## Examples

This example demonstrates how to create and call a stored procedure that converts a weight from kilograms (kg) to pounds (lb):

```sql
CREATE PROCEDURE convert_kg_to_lb(kg DECIMAL(4, 2)) 
RETURNS DECIMAL(10, 2) 
LANGUAGE SQL 
COMMENT = 'Converts kilograms to pounds'
AS $$
BEGIN
    RETURN kg * 2.20462;
END;
$$;

CALL PROCEDURE convert_kg_to_lb(10.00);

┌────────────┐
│   Result   │
├────────────┤
│ 22.0462000 │
└────────────┘
```