---
title: CREATE PROCEDURE
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.816"/>

Defines a stored procedure that executes SQL operations and returns a result.

## Syntax

```sql
CREATE PROCEDURE <procedure_name>(<parameter_name> <data_type>, ...)
RETURNS <return_data_type> [NOT NULL]
LANGUAGE <language>
[ COMMENT '<comment>' ]
AS $$
BEGIN
    <procedure_body>
    RETURN <return_value>;             -- Use to return a single value
    -- OR
    RETURN TABLE(<select_query>);      -- Use to return a table
END;
$$;
```

| Parameter                               | Description                                                                                                               |
|-----------------------------------------|---------------------------------------------------------------------------------------------------------------------------|
| `<procedure_name>`                      | Name of the procedure.                                                                                                    |
| `<parameter_name> <data_type>`          | Input parameters (optional), each with a specified data type. Multiple parameters can be defined and separated by commas. |
| `RETURNS <return_data_type> [NOT NULL]` | Specifies the data type of the return value. `NOT NULL` ensures the returned value cannot be NULL.                        |
| `LANGUAGE`                              | Specifies the language in which the procedure body is written. Currently, only `SQL` is supported.                       |
| `COMMENT`                               | Optional text describing the procedure.                                                                                   |
| `AS ...`                                | Encloses the procedure body, which contains SQL statements, variable declarations, loops, and a  RETURN statement.        |

## Access control requirements

| Privilege        | Object Type | Description          |
|:-----------------|:------------|:---------------------|
| CREATE PROCEDURE | Global      | Creates a procedure. |


To create a procedure, the user performing the operation or the [current_role](/guides/security/access-control/roles) must have the CREATE PROCEDURE [privilege](/guides/security/access-control/privileges).


## Examples

This example defines a stored procedure that converts weight from kilograms (kg) to pounds (lb):

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
```

You can also define a stored procedure that works with loops, conditions, and dynamic variables.

```sql

CREATE OR REPLACE PROCEDURE loop_test()
RETURNS INT
LANGUAGE SQL
COMMENT = 'loop test'
AS $$
BEGIN
    LET x RESULTSET := select number n from numbers(10);
    LET sum := 0;
    FOR x IN x DO
        FOR batch in 0 TO x.n DO
            IF batch % 2 = 0 THEN
                sum := sum + batch;
            ELSE
                sum := sum - batch;
            END IF;
        END FOR;
    END FOR;
    RETURN sum;
END;
$$;

-- Grant ACCESS PROCEDURE Privilege TO role test
GRANT ACCESS PROCEDURE ON PROCEDURE loop_test() to role test;

```

```sql
CALL PROCEDURE loop_test();

┌─Result─┐
│   -5   │
└────────┘
```