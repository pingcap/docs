---
title: DESC PROCEDURE
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.690"/>

Displays detailed information about a specific stored procedure.

## Syntax

```sql
DESC | DESCRIBE PROCEDURE <procedure_name>([<parameter_type1>, <parameter_type2>, ...])
```

- If a procedure has no parameters, use empty parentheses: `DESC PROCEDURE <procedure_name>()`;
- For procedures with parameters, specify the exact types to avoid errors.

## Examples

This example creates and then displays a stored procedure named `sum_even_numbers`.

```sql
CREATE PROCEDURE sum_even_numbers(start_val UInt8, end_val UInt8) 
RETURNS UInt8 NOT NULL 
LANGUAGE SQL 
COMMENT='Calculate the sum of all even numbers' 
AS $$
BEGIN
    LET sum := 0;
    FOR i IN start_val TO end_val DO
        IF i % 2 = 0 THEN
            sum := sum + i;
        END IF;
    END FOR;
    
    RETURN sum;
END;
$$;

DESC PROCEDURE sum_even_numbers(Uint8, Uint8);

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  Property │                                                                                        Value                                                                                       │
├───────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ signature │ (start_val,end_val)                                                                                                                                                                │
│ returns   │ (UInt8)                                                                                                                                                                            │
│ language  │ SQL                                                                                                                                                                                │
│ body      │ BEGIN\n    LET sum := 0;\n    FOR i IN start_val TO end_val DO\n        IF i % 2 = 0 THEN\n            sum := sum + i;\n        END IF;\n    END FOR;\n    \n    RETURN sum;\nEND; │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```