---
title: UPDATE
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.705"/>

Updates rows in a table with new values, optionally using values from other tables.

:::tip atomic operations
Databend ensures data integrity with atomic operations. Inserts, updates, replaces, and deletes either succeed completely or fail entirely.
:::

## Syntax

```sql
UPDATE <target_table>
       SET <col_name> = <value> [ , <col_name> = <value> , ... ] -- Set new values  
        [ FROM <additional_tables> ] -- Use values from other tables  
        [ WHERE <condition> ] -- Filter rows
```

## Configuring `error_on_nondeterministic_update` Setting

The `error_on_nondeterministic_update` setting controls whether an error is returned when an UPDATE statement attempts to update a target row that joins multiple source rows without a deterministic update rule.

- When `error_on_nondeterministic_update` = `true` (default): Databend returns an error if a target row matches multiple source rows and there is no clear rule for selecting which value to use.
- When `error_on_nondeterministic_update` = `false`: The UPDATE statement proceeds even if a target row joins multiple source rows, but the final update result may be non-deterministic.

Example:

Consider the following tables:

```sql
CREATE OR REPLACE TABLE target (
    id INT,
    price DECIMAL(10, 2)
);

INSERT INTO target VALUES
(1, 299.99),
(2, 399.99);

CREATE OR REPLACE TABLE source (
    id INT,
    price DECIMAL(10, 2)
);

INSERT INTO source VALUES
(1, 279.99),
(2, 399.99),
(2, 349.99);  -- Duplicate id in source
```

Executing the following UPDATE statement:

```sql
UPDATE target
SET target.price = source.price
FROM source
WHERE target.id = source.id;
```

- With `error_on_nondeterministic_update = true`, this query fails because id = 2 in target matches multiple rows in source, making the update ambiguous.

  ```sql
  SET error_on_nondeterministic_update = 1;

  root@localhost:8000/default> UPDATE target
  SET target.price = source.price
  FROM source
  WHERE target.id = source.id;

  error: APIError: QueryFailed: [4001]multi rows from source match one and the same row in the target_table multi times
  ```

- With `error_on_nondeterministic_update = false`, the update succeeds, but target.price for id = 2 may be updated to either 399.99 or 349.99, depending on execution order.

  ```sql
  SET error_on_nondeterministic_update = 0;

  root@localhost:8000/default> UPDATE target
  SET target.price = source.price
  FROM source
  WHERE target.id = source.id;

  ┌────────────────────────┐
  │ number of rows updated │
  ├────────────────────────┤
  │                      2 │
  └────────────────────────┘

  SELECT * FROM target;

  ┌────────────────────────────────────────────┐
  │        id       │           price          │
  ├─────────────────┼──────────────────────────┤
  │               1 │ 279.99                   │
  │               2 │ 399.99                   │
  └────────────────────────────────────────────┘
  ```



## Examples

The following example demonstrates how to update rows in a table, both directly and using values from another table. 

We will first create a **bookstore** table and insert some sample data, then update a specific row directly. After that, we will use a second table, **book_updates**, to update rows in the **bookstore** table based on the values from **book_updates**.

#### Step 1: Create the bookstore table and insert initial data

In this step, we create a table called **bookstore** and populate it with some sample book data.

```sql
CREATE TABLE bookstore (
  book_id INT,
  book_name VARCHAR
);

INSERT INTO bookstore VALUES (101, 'After the death of Don Juan');
INSERT INTO bookstore VALUES (102, 'Grown ups');
INSERT INTO bookstore VALUES (103, 'The long answer');
INSERT INTO bookstore VALUES (104, 'Wartime friends');
INSERT INTO bookstore VALUES (105, 'Deconstructed');
```

#### Step 2: View the bookstore table before the update

We can now check the contents of the **bookstore** table to see the initial data.

```sql
SELECT * FROM bookstore;

┌───────────────────────────────────────────────┐
│     book_id     │          book_name          │
├─────────────────┼─────────────────────────────┤
│             102 │ Grown ups                   │
│             103 │ The long answer             │
│             101 │ After the death of Don Juan │
│             105 │ Deconstructed               │
│             104 │ Wartime friends             │
└───────────────────────────────────────────────┘
```

#### Step 3: Update a single row directly

Next, let's update the book with book_id `103` to change its name.

```sql
UPDATE bookstore 
SET book_name = 'The long answer (2nd)' 
WHERE book_id = 103;
```

#### Step 4: View the bookstore table after the update

Now, let's check the table again to see the result of our direct update.

```sql
SELECT book_name FROM bookstore WHERE book_id=103;

┌───────────────────────┐
│       book_name       │
├───────────────────────┤
│ The long answer (2nd) │
└───────────────────────┘
```

#### Step 5: Create a new table for updated values

In this step, we create a second table called **book_updates**, which holds updated book names that we will use to update the **bookstore** table.

```sql
CREATE TABLE book_updates (
  book_id INT,
  new_book_name VARCHAR
);

INSERT INTO book_updates VALUES (103, 'The long answer (Revised)');
INSERT INTO book_updates VALUES (104, 'Wartime friends (Expanded Edition)');
```

#### Step 6: Update the bookstore table using values from book_updates

Now, we will update the **bookstore** table with values from the **book_updates** table.

```sql
UPDATE bookstore
SET book_name = book_updates.new_book_name
FROM book_updates
WHERE bookstore.book_id = book_updates.book_id;
```

#### Step 7: View the bookstore table after the update

Finally, we check the **bookstore** table again to confirm that the names have been updated using the values from **book_updates**.

```sql
SELECT * FROM bookstore;

┌──────────────────────────────────────────────────────┐
│     book_id     │              book_name             │
├─────────────────┼────────────────────────────────────┤
│             105 │ Deconstructed                      │
│             101 │ After the death of Don Juan        │
│             102 │ Grown ups                          │
│             104 │ Wartime friends (Expanded Edition) │
│             103 │ The long answer (Revised)          │
└──────────────────────────────────────────────────────┘
```