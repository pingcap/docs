---
title: Stored Procedure & SQL Scripting
slug: /stored-procedure-scripting/
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.833"/>

Stored procedures in Databend let you package SQL logic that runs on the server with access to control flow, variables, cursors, and dynamic statements. This page explains how to create procedures and write the inline scripting that powers them.

## Defining a Procedure

```sql
CREATE [OR REPLACE] PROCEDURE <name>(<param_name> <data_type>, ...)
RETURNS <return_type> [NOT NULL]
LANGUAGE SQL
[COMMENT = '<text>']
AS $$
BEGIN
    -- Declarations and statements
    RETURN <scalar_value>;
    -- Or return a query result
    -- RETURN TABLE(<select_query>);
END;
$$;
```

| Component | Description |
|-----------|-------------|
| `<name>` | Identifier for the procedure. Schema qualification is optional. |
| `<param_name> <data_type>` | Input parameters typed with Databend scalar types. Parameters are passed by value. |
| `RETURNS <return_type> [NOT NULL]` | Declares the logical return type. `NOT NULL` enforces a non-nullable response. |
| `LANGUAGE SQL` | Databend currently accepts `SQL` only. |
| `RETURN` / `RETURN TABLE` | Ends execution and provides either a scalar or tabular result. |

Use [`CREATE PROCEDURE`](/sql/sql-commands/ddl/procedure/create-procedure) to persist the definition, [`CALL`](/sql/sql-commands/ddl/procedure/call-procedure) to run it, and [`DROP PROCEDURE`](/sql/sql-commands/ddl/procedure/drop-procedure) to remove it.

### Minimal Example

```sql
CREATE OR REPLACE PROCEDURE convert_kg_to_lb(kg DOUBLE)
RETURNS DOUBLE
LANGUAGE SQL
COMMENT = 'Converts kilograms to pounds'
AS $$
BEGIN
    RETURN kg * 2.20462;
END;
$$;

CALL PROCEDURE convert_kg_to_lb(10);
```

## Language Basics Inside Procedures

### Declare Section

Stored procedures can start with an optional `DECLARE` block to initialize variables before the executable section. Each entry in the block follows the same syntax as `LET`: `name [<data_type>] [:= <expr> | DEFAULT <expr>]`. When you omit the initializer, the variable must be assigned before it is read; referencing it too early raises error 3129.

```sql
CREATE OR REPLACE PROCEDURE sp_with_declare()
RETURNS INT
LANGUAGE SQL
AS $$
DECLARE
    counter INT DEFAULT 0;
BEGIN
    counter := counter + 5;
    RETURN counter;
END;
$$;

CALL PROCEDURE sp_with_declare();
```

The `DECLARE` section accepts the same definitions as `LET`, including optional data types, `RESULTSET`, and `CURSOR` declarations. Use a semicolon after each item.

### Variables and Assignment

Use `LET` to declare variables or constants. You can optionally provide a type annotation and an initializer with either `:=` or the `DEFAULT` keyword. Without an initializer, the variable must be assigned before it is read; referencing it beforehand raises error 3129. Reassign by omitting `LET`.

```sql
CREATE OR REPLACE PROCEDURE sp_demo_variables()
RETURNS FLOAT
LANGUAGE SQL
AS $$
BEGIN
    LET total DECIMAL(10, 2) DEFAULT 100;
    LET rate FLOAT := 0.07;
    LET surcharge FLOAT := NULL; -- Explicitly initialize before use
    LET tax FLOAT DEFAULT rate;  -- DEFAULT can reference initialized variables

    total := total * rate; -- Multiply by the rate
    total := total + COALESCE(surcharge, 5); -- Reassign without LET
    total := total + tax;

    RETURN total;
END;
$$;

CALL PROCEDURE sp_demo_variables();
```

Referencing an uninitialized variable anywhere in a procedure raises error 3129.

### Variable Scope

Variables are scoped to the enclosing block. Inner blocks can shadow outer bindings, and the outer value is restored when the block exits.

```sql
CREATE OR REPLACE PROCEDURE sp_demo_scope()
RETURNS STRING
LANGUAGE SQL
AS $$
BEGIN
    LET threshold := 10;
    LET summary := 'outer=' || threshold;

    IF threshold > 0 THEN
        LET threshold := 5; -- Shadows the outer value
        summary := summary || ', inner=' || threshold;
    END IF;

    summary := summary || ', after=' || threshold;
    RETURN summary;
END;
$$;

CALL PROCEDURE sp_demo_scope();
```

### Comments

Procedures support single-line (`-- text`) and multi-line (`/* text */`) comments.

```sql
CREATE OR REPLACE PROCEDURE sp_demo_comments()
RETURNS FLOAT
LANGUAGE SQL
AS $$
BEGIN
    -- Calculate price with tax
    LET price := 15;
    LET tax_rate := 0.08;

    /*
        Multi-line comments are useful for documenting complex logic.
        The following line returns the tax-inclusive price.
    */
    RETURN price * (1 + tax_rate);
END;
$$;

CALL PROCEDURE sp_demo_comments();
```

### Lambda Expressions

Lambda expressions define inline logic that can be passed to array functions or invoked within queries. They follow the `<parameter> -> <expression>` form (wrap parameters in parentheses when more than one is provided). The expression can include casts, conditional logic, and even references to procedure variables.

- Use `:variable_name` to reference procedure variables inside the lambda when it runs within a SQL statement.
- Functions such as `ARRAY_TRANSFORM` and `ARRAY_FILTER` evaluate the lambda for each element in the input array.

```sql
CREATE OR REPLACE PROCEDURE sp_demo_lambda_array()
RETURNS STRING
LANGUAGE SQL
AS $$
BEGIN
    RETURN TABLE(
        SELECT ARRAY_TRANSFORM([1, 2, 3, 4], item -> (item::Int + 1)) AS incremented
    );
END;
$$;

CALL PROCEDURE sp_demo_lambda_array();
```

Lambdas can also appear inside queries executed by the procedure.

```sql
CREATE OR REPLACE PROCEDURE sp_demo_lambda_query()
RETURNS STRING
LANGUAGE SQL
AS $$
BEGIN
    RETURN TABLE(
        SELECT
            number,
            ARRAY_TRANSFORM([number, number + 1], val -> (val::Int + 1)) AS next_values
        FROM numbers(3)
    );
END;
$$;

CALL PROCEDURE sp_demo_lambda_query();
```

Capture procedure variables inside the lambda by prefixing them with `:` when the lambda runs in a SQL statement context.

```sql
CREATE OR REPLACE PROCEDURE sp_lambda_filter()
RETURNS STRING
LANGUAGE SQL
AS $$
BEGIN
    LET threshold := 2;
    RETURN TABLE(
        SELECT ARRAY_FILTER([1, 2, 3, 4], element -> (element::Int > :threshold)) AS filtered
    );
END;
$$;

CALL PROCEDURE sp_lambda_filter();
```

You can also place complex expressions, such as `CASE` logic, inside the lambda body.

```sql
CREATE OR REPLACE PROCEDURE sp_lambda_case()
RETURNS STRING
LANGUAGE SQL
AS $$
BEGIN
    RETURN TABLE(
        SELECT
            number,
            ARRAY_TRANSFORM(
                [number - 1, number, number + 1],
                val -> (CASE WHEN val % 2 = 0 THEN 'even' ELSE 'odd' END)
            ) AS parity_window
        FROM numbers(3)
    );
END;
$$;

CALL PROCEDURE sp_lambda_case();
```

## Control Flow

### IF Statements

Use `IF ... ELSEIF ... ELSE ... END IF;` to branch inside a procedure.

```sql
CREATE OR REPLACE PROCEDURE sp_evaluate_score(score INT)
RETURNS STRING
LANGUAGE SQL
AS $$
BEGIN
    IF score >= 90 THEN
        RETURN 'Excellent';
    ELSEIF score >= 70 THEN
        RETURN 'Good';
    ELSE
        RETURN 'Review';
    END IF;
END;
$$;

CALL PROCEDURE sp_evaluate_score(82);
```

### CASE Expressions

`CASE` expressions provide an alternative to nested `IF` statements.

```sql
CREATE OR REPLACE PROCEDURE sp_membership_discount(level STRING)
RETURNS FLOAT
LANGUAGE SQL
AS $$
BEGIN
    RETURN CASE
        WHEN level = 'gold' THEN 0.2
        WHEN level = 'silver' THEN 0.1
        ELSE 0
    END;
END;
$$;

CALL PROCEDURE sp_membership_discount('silver');
```

### Range `FOR`

Range-based loops iterate from a lower bound to an upper bound (inclusive). Use the optional `REVERSE` keyword to walk the range backwards.

```sql
CREATE OR REPLACE PROCEDURE sp_sum_range(start_val INT, end_val INT)
RETURNS INT
LANGUAGE SQL
AS $$
BEGIN
    LET total := 0;
    FOR i IN start_val TO end_val DO
        total := total + i;
    END FOR;
    RETURN total;
END;
$$;

CALL PROCEDURE sp_sum_range(1, 5);
```

Range loops require the lower bound to be less than or equal to the upper bound when stepping forward.

```sql
CREATE OR REPLACE PROCEDURE sp_reverse_count(start_val INT, end_val INT)
RETURNS STRING
LANGUAGE SQL
AS $$
BEGIN
    LET output := '';
    FOR i IN REVERSE start_val TO end_val DO
        output := output || i || ' ';
    END FOR;
    RETURN TRIM(output);
END;
$$;

CALL PROCEDURE sp_reverse_count(1, 5);
```

#### `FOR ... IN` Queries

Iterate directly over the result of a query. The loop variable exposes columns as fields.

```sql
CREATE OR REPLACE PROCEDURE sp_sum_query(limit_rows INT)
RETURNS BIGINT
LANGUAGE SQL
AS $$
BEGIN
    LET total := 0;
    FOR rec IN SELECT number FROM numbers(:limit_rows) DO
        total := total + rec.number;
    END FOR;
    RETURN total;
END;
$$;

CALL PROCEDURE sp_sum_query(5);
```

`FOR` can also iterate over previously declared result-set variables or cursors (see [Working with Query Results](#working-with-query-results)).

### `WHILE`

```sql
CREATE OR REPLACE PROCEDURE sp_factorial(n INT)
RETURNS INT
LANGUAGE SQL
AS $$
BEGIN
    LET result := 1;
    WHILE n > 0 DO
        result := result * n;
        n := n - 1;
    END WHILE;
    RETURN result;
END;
$$;

CALL PROCEDURE sp_factorial(5);
```

### `REPEAT`

```sql
CREATE OR REPLACE PROCEDURE sp_repeat_sum(limit_val INT)
RETURNS INT
LANGUAGE SQL
AS $$
BEGIN
    LET counter := 0;
    LET total := 0;

    REPEAT
        counter := counter + 1;
        total := total + counter;
    UNTIL counter >= limit_val END REPEAT;

    RETURN total;
END;
$$;

CALL PROCEDURE sp_repeat_sum(3);
```

### `LOOP`

```sql
CREATE OR REPLACE PROCEDURE sp_retry_counter(max_attempts INT)
RETURNS INT
LANGUAGE SQL
AS $$
BEGIN
    LET retries := 0;
    LOOP
        retries := retries + 1;
        IF retries >= max_attempts THEN
            BREAK;
        END IF;
    END LOOP;

    RETURN retries;
END;
$$;

CALL PROCEDURE sp_retry_counter(5);
```

### Break and Continue

Use `BREAK` to exit a loop early and `CONTINUE` to skip to the next iteration.

```sql
CREATE OR REPLACE PROCEDURE sp_break_example(limit_val INT)
RETURNS INT
LANGUAGE SQL
AS $$
BEGIN
    LET counter := 0;
    LET total := 0;

    WHILE TRUE DO
        counter := counter + 1;
        IF counter > limit_val THEN
            BREAK;
        END IF;
        IF counter % 2 = 0 THEN
            CONTINUE;
        END IF;
        total := total + counter;
    END WHILE;

    RETURN total;
END;
$$;

CALL PROCEDURE sp_break_example(5);
```

Use `BREAK <label>` or `CONTINUE <label>` to exit or skip to the next iteration of a labeled loop. Declare the label by appending it after the closing keyword, for example `END LOOP main_loop;`.

## Working with Query Results

### Result-Set Variables

Use `RESULTSET` to materialize query results for later iteration.

```sql
CREATE OR REPLACE PROCEDURE sp_total_active_salary()
RETURNS DECIMAL(18, 2)
LANGUAGE SQL
AS $$
BEGIN
    -- Assume table hr_employees(id, salary, active) exists.
    LET employees RESULTSET := SELECT id, salary FROM hr_employees WHERE active = TRUE;
    LET total := 0;

    FOR emp IN employees DO
        total := total + emp.salary;
    END FOR;

    RETURN total;
END;
$$;

CALL PROCEDURE sp_total_active_salary();
```

### Cursors

Declare a cursor when you need to fetch rows on demand.

```sql
CREATE OR REPLACE PROCEDURE sp_fetch_two()
RETURNS INT
LANGUAGE SQL
AS $$
BEGIN
    -- Assume table stocks(sku, quantity) exists.
    LET cur CURSOR FOR SELECT quantity FROM stocks ORDER BY quantity;
    OPEN cur;

    LET first := 0;
    LET second := 0;

    FETCH cur INTO first;
    FETCH cur INTO second;

    CLOSE cur;
    RETURN first + second;
END;
$$;

CALL PROCEDURE sp_fetch_two();
```

Alternatively, derive a cursor from a `RESULTSET`.

```sql
CREATE OR REPLACE PROCEDURE sp_first_number()
RETURNS INT
LANGUAGE SQL
AS $$
BEGIN
    LET recent RESULTSET := SELECT number FROM numbers(5);
    LET num_cursor CURSOR FOR recent;

    OPEN num_cursor;
    LET first_value := NULL;
    FETCH num_cursor INTO first_value;
    CLOSE num_cursor;

    RETURN first_value;
END;
$$;

CALL PROCEDURE sp_first_number();
```

### Iterating Rows

Result-set variables and cursors can be traversed with a `FOR ... IN` loop.

```sql
CREATE OR REPLACE PROCEDURE sp_low_stock_count()
RETURNS INT
LANGUAGE SQL
AS $$
BEGIN
    LET inventory RESULTSET := SELECT sku, quantity FROM stocks;
    LET low_stock := 0;

    FOR item IN inventory DO
        IF item.quantity < 5 THEN
            low_stock := low_stock + 1;
        END IF;
    END FOR;

    RETURN low_stock;
END;
$$;

CALL PROCEDURE sp_low_stock_count();
```

### Returning Tables

Use `RETURN TABLE(<query>)` to emit a tabular result.

```sql
CREATE OR REPLACE PROCEDURE sp_sales_summary()
RETURNS STRING
LANGUAGE SQL
AS $$
BEGIN
    RETURN TABLE(
        SELECT product_id, SUM(quantity) AS total_quantity
        FROM sales_detail
        WHERE sale_date = today()
        GROUP BY product_id
        ORDER BY product_id
    );
END;
$$;

CALL PROCEDURE sp_sales_summary();
```

Returning a stored result set uses the same syntax:

```sql
CREATE OR REPLACE PROCEDURE sp_return_cached()
RETURNS STRING
LANGUAGE SQL
AS $$
BEGIN
    LET latest RESULTSET := SELECT number FROM numbers(3);
    RETURN TABLE(latest);
END;
$$;

CALL PROCEDURE sp_return_cached();
```

## Dynamic SQL

### Executing Statements

### Dynamic Blocks with Variables

The dynamic block returns its result to the caller of `EXECUTE IMMEDIATE`. Use `RETURN TABLE` inside the block to produce a result set.

You can also run a single SQL string and capture its output:

```sql
EXECUTE IMMEDIATE $$
BEGIN
    LET recent RESULTSET := EXECUTE IMMEDIATE 'SELECT number FROM numbers(3)';
    RETURN TABLE(recent);
END;
$$;

CREATE OR REPLACE PROCEDURE sp_dynamic_resultset()
RETURNS STRING
LANGUAGE SQL
AS $$
BEGIN
    LET recent RESULTSET := EXECUTE IMMEDIATE 'SELECT number FROM numbers(3)';
    RETURN TABLE(recent);
END;
$$;

CALL PROCEDURE sp_dynamic_resultset();
```

## Notes and Limitations

- Stored procedures execute in a single transaction; any error rolls back the work performed inside the procedure.
- Returned values surface as strings at the client, even if a numeric type is declared.
- There is no `TRY ... CATCH` construct; validate inputs and anticipate error conditions explicitly.
- Validate identifiers before concatenating them into dynamic SQL text to avoid executing unintended statements.
- Scripts are limited by the `script_max_steps` setting (default 10,000). Increase it before running long loops:

  ```sql
  SET script_max_steps = 100000;
  ```

## Related Commands

- [`CREATE PROCEDURE`](/sql/sql-commands/ddl/procedure/create-procedure)
- [`CALL`](/sql/sql-commands/ddl/procedure/call-procedure)
- [`SHOW PROCEDURES`](/sql/sql-commands/ddl/procedure/show-procedures)
- [`DESCRIBE PROCEDURE`](/sql/sql-commands/ddl/procedure/desc-procedure)
- [`EXECUTE IMMEDIATE`](/sql/sql-commands/administration-cmds/execute-immediate)
