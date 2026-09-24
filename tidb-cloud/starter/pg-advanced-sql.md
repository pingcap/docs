---
title: PostgreSQL Advanced SQL
summary: Learn about PL/pgSQL, triggers, sequences, custom types, and collations on PostgreSQL-compatible TiDB Cloud Starter.
---

# PostgreSQL Advanced SQL

PostgreSQL-compatible {{{ .starter }}} supports common advanced PostgreSQL SQL features, including PL/pgSQL functions, triggers, sequences, enum and composite types, and custom collations.

## PL/pgSQL

PostgreSQL-compatible {{{ .starter }}} supports PL/pgSQL functions and `DO` blocks with commonly used procedural constructs.

Supported constructs include:

- Variable declarations and assignments
- `IF`, `ELSIF`, and `ELSE`
- `CASE`
- `FOR` loops
- `LOOP`
- `EXIT` and `CONTINUE`
- `PERFORM`
- `SELECT ... INTO`
- `INSERT`, `UPDATE`, and `DELETE ... RETURNING ... INTO`
- `RAISE`
- `RETURN`
- Dynamic `EXECUTE`, including `INTO` and `USING`

### Create a PL/pgSQL function

For example:

```sql
CREATE FUNCTION increment_value(val INTEGER)
RETURNS INTEGER AS $$
BEGIN
    RETURN val + 1;
END;
$$ LANGUAGE plpgsql;
```

Call the function:

```sql
SELECT increment_value(41);
```

### Declare variables

Use a `DECLARE` block:

```sql
CREATE FUNCTION user_count()
RETURNS INTEGER AS $$
DECLARE
    n INTEGER;
BEGIN
    SELECT count(*) INTO n
    FROM users;

    RETURN n;
END;
$$ LANGUAGE plpgsql;
```

Declarations can span multiple lines.

### Conditional logic

Use `IF`, `ELSIF`, and `ELSE`:

```sql
CREATE FUNCTION size_label(n INTEGER)
RETURNS TEXT AS $$
BEGIN
    IF n > 100 THEN
        RETURN 'large';
    ELSIF n > 10 THEN
        RETURN 'medium';
    ELSE
        RETURN 'small';
    END IF;
END;
$$ LANGUAGE plpgsql;
```

`CASE` statements are also supported:

```sql
CREATE FUNCTION category_label(n INTEGER)
RETURNS TEXT AS $$
BEGIN
    CASE
        WHEN n > 100 THEN RETURN 'large';
        WHEN n > 10 THEN RETURN 'medium';
        ELSE RETURN 'small';
    END CASE;
END;
$$ LANGUAGE plpgsql;
```

> **Note:**
>
> Always include an `ELSE` branch in a PL/pgSQL `CASE` statement. If no branch matches and `ELSE` is omitted, PostgreSQL-compatible {{{ .starter }}} can fall through instead of raising PostgreSQL's `CASE_NOT_FOUND` error.

### `SELECT ... INTO`

Assign a query result to a variable:

```sql
CREATE FUNCTION active_user_count()
RETURNS INTEGER AS $$
DECLARE
    n INTEGER;
BEGIN
    SELECT count(*) INTO n
    FROM users
    WHERE active = true;

    RETURN n;
END;
$$ LANGUAGE plpgsql;
```

### `RETURNING ... INTO`

Capture values returned by DML:

```sql
CREATE FUNCTION create_order(p_item TEXT)
RETURNS BIGINT AS $$
DECLARE
    new_id BIGINT;
BEGIN
    INSERT INTO orders (item)
    VALUES (p_item)
    RETURNING id INTO new_id;

    RETURN new_id;
END;
$$ LANGUAGE plpgsql;
```

`RETURNING ... INTO` is supported with `INSERT`, `UPDATE`, and `DELETE`.

### Dynamic SQL

Use `EXECUTE` for dynamic SQL:

```sql
CREATE FUNCTION count_rows(table_name TEXT)
RETURNS INTEGER AS $$
DECLARE
    n INTEGER;
BEGIN
    EXECUTE
        'SELECT count(*) FROM ' || quote_ident(table_name)
        INTO n;

    RETURN n;
END;
$$ LANGUAGE plpgsql;
```

Parameterize dynamic SQL with `USING`:

```sql
CREATE FUNCTION double_it(p INTEGER)
RETURNS INTEGER AS $$
DECLARE
    result INTEGER;
BEGIN
    EXECUTE 'SELECT $1 * 2'
        INTO result
        USING p;

    RETURN result;
END;
$$ LANGUAGE plpgsql;
```

### Exception handling

`BEGIN ... EXCEPTION` blocks are supported in `DO` blocks:

```sql
DO $$
BEGIN
    EXECUTE 'CREATE TABLE audit_snapshot(id INTEGER)';
EXCEPTION
    WHEN others THEN
        RAISE NOTICE 'setup skipped';
END;
$$;
```

Exception handlers follow PostgreSQL rollback semantics for the protected block.

`BEGIN ... EXCEPTION` and nested procedural `BEGIN ... END` blocks are not supported inside a `CREATE FUNCTION` body. They are supported only in `DO` blocks.

### PL/pgSQL limitations

The following constructs are not supported:

- `WHILE` loops
- `FOREACH` loops
- Cursor operations
- `REFCURSOR`


## Triggers

Row-level `BEFORE` and `AFTER` triggers are supported for:

- `INSERT`
- `UPDATE`
- `DELETE`

### Create an AFTER trigger

Create a trigger function:

```sql
CREATE FUNCTION audit_trigger()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_log (table_name, action, changed_at)
    VALUES (TG_TABLE_NAME, TG_OP, NOW());

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

Create the trigger:

```sql
CREATE TRIGGER users_audit
AFTER INSERT OR UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION audit_trigger();
```

### Create a BEFORE trigger

A `BEFORE` trigger can modify `NEW`, skip a row with `RETURN NULL`, or reject a row with `RAISE EXCEPTION`.

For example:

```sql
CREATE FUNCTION normalize_user_name()
RETURNS TRIGGER AS $$
BEGIN
    NEW.name := upper(NEW.name);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

```sql
CREATE TRIGGER normalize_user
BEFORE INSERT OR UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION normalize_user_name();
```

Reject invalid input:

```sql
CREATE FUNCTION reject_invalid_user()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.name = 'INVALID' THEN
        RAISE EXCEPTION 'invalid user name';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### BEFORE trigger limitations

A `BEFORE` trigger function supports common validation and rewrite logic, including:

- `IF` / `ELSIF` / `ELSE`
- `RAISE`
- `PERFORM`
- Declared local variables
- `SELECT ... INTO`
- Assignments to `NEW`
- DML against other tables
- `TG_OP` and `TG_TABLE_NAME`

The following procedural constructs are not supported in a `BEFORE` trigger function:

- `FOR` loops
- Bare `LOOP`
- `WHILE` and `FOREACH`
- PL/pgSQL `CASE` statements
- Dynamic `EXECUTE`
- Exception handlers
- Nested procedural blocks

A `CASE` expression, such as `NEW.status := CASE WHEN ... END`, can still be used in an assignment.

### AFTER trigger formatting

In an `AFTER` trigger function, keep a bare `RETURN NEW;` or `RETURN OLD;` on its own line.

For example:

```sql
BEGIN
    INSERT INTO audit_log (action) VALUES (TG_OP);
    RETURN NEW;
END;
```

A compact function body that places `RETURN NEW;` or `RETURN OLD;` on the same line as another statement can fail at runtime.

### Statement-level triggers

`FOR EACH STATEMENT` syntax is accepted, but it currently executes with per-row behavior rather than PostgreSQL statement-level behavior.

For predictable behavior, use `FOR EACH ROW` explicitly.

### Drop a trigger

Use `IF EXISTS` when dropping a trigger:

```sql
DROP TRIGGER IF EXISTS users_audit ON users;
```

## Sequences

Create and use a sequence:

```sql
CREATE SEQUENCE order_seq
START WITH 1000
INCREMENT BY 1;

SELECT nextval('order_seq');
SELECT currval('order_seq');
SELECT lastval();
SELECT setval('order_seq', 2000);
```

Drop the sequence:

```sql
DROP SEQUENCE order_seq;
```

The following options can be specified when creating a sequence:

- `START`
- `INCREMENT`
- `MINVALUE`
- `MAXVALUE`
- `CACHE`
- `CYCLE`

`ALTER SEQUENCE` supports ownership operations such as `OWNER TO` and `OWNED BY`. It does not support changing sequence generation options after creation. Use `setval()` when you need to reposition a sequence.

## Custom types

### Enum types

Create an enum type:

```sql
CREATE TYPE mood AS ENUM (
    'happy',
    'sad',
    'neutral'
);
```

Add an enum value:

```sql
ALTER TYPE mood
ADD VALUE 'excited';
```

Use the type in a table:

```sql
CREATE TABLE user_mood (
    id BIGSERIAL PRIMARY KEY,
    mood mood
);
```

> **Note:**
>
> Enum comparison and ordering use the enum label text rather than PostgreSQL declaration order. Equality, `IN`, and grouping are unaffected. If application logic depends on enum order, use an explicit ranking expression.

For example:

```sql
SELECT mood
FROM user_mood
ORDER BY array_position(
    ARRAY['sad', 'neutral', 'happy', 'excited'],
    mood::text
);
```

### Composite types

Create a composite type:

```sql
CREATE TYPE address AS (
    street TEXT,
    city TEXT,
    zip TEXT
);
```

## Collations

Create a collation:

```sql
CREATE COLLATION my_collation (
    LOCALE = 'en_US.utf8'
);
```

Use it on a column:

```sql
CREATE TABLE names (
    value TEXT COLLATE my_collation
);
```

Drop the collation:

```sql
DROP COLLATION my_collation;
```

A custom collation changes plain text comparison and `ORDER BY` behavior.

### Collation limitations

Keep the following differences in mind:

- The specified `LOCALE` value does not select distinct locale-specific behavior. A custom collation uses one locale-aware ordering mode.
- Text without an explicit custom collation uses bytewise ordering.
- Collation is not applied to `ORDER BY` inside aggregate functions.
- Collation is not applied to window-function `ORDER BY`.
- Custom collations are not fully reflected by `pg_collation` or `pg_attribute.attcollation`.
