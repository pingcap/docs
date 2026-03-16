---
title: DROP PROCEDURE
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.637"/>

Deletes an existing stored procedure.

## Syntax

```sql
DROP PROCEDURE <procedure_name>([<parameter_type1>, <parameter_type2>, ...])
```

- If a procedure has no parameters, use empty parentheses: `DROP PROCEDURE <procedure_name>()`;
- For procedures with parameters, specify the exact types to avoid errors.

## Examples

This example creates and then drops a stored procedure:

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

DROP PROCEDURE convert_kg_to_lb(Decimal(4, 2));
```