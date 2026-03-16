---
title: SHOW SEQUENCES
sidebar_position: 3
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.742"/>

Returns a list of the created sequences.

## Syntax

```sql
SHOW SEQUENCES [ LIKE '<pattern>' | WHERE <expr> ]
```

| Parameter | Description                                                                                                                 |
|-----------|-----------------------------------------------------------------------------------------------------------------------------|
| LIKE      | Filters the results by their names using case-sensitive pattern matching.                                                   |
| WHERE     | Filters the results using an expression in the WHERE clause. You can filter based on any column in the result set, such as `name`, `start`, `interval`, `current`, `created_on`, `updated_on`, or `comment`. For example: `WHERE start > 0` or `WHERE name LIKE 's%'`. |

## Examples

```sql
-- Create a sequence
CREATE SEQUENCE seq;

-- Show all sequences
SHOW SEQUENCES;

╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│  name  │  start │ interval │ current │         created_on         │         updated_on         │      comment     │
├────────┼────────┼──────────┼─────────┼────────────────────────────┼────────────────────────────┼──────────────────┤
│ seq    │      1 │        1 │       1 │ 2025-05-20 02:48:49.749338 │ 2025-05-20 02:48:49.749338 │ NULL             │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

-- Use the sequence in an INSERT statement
CREATE TABLE tmp(a int, b uint64, c int);
INSERT INTO tmp select 10,nextval(seq),20 from numbers(3);

-- Show sequences after usage
SHOW SEQUENCES;

╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│  name  │  start │ interval │ current │         created_on         │         updated_on         │      comment     │
├────────┼────────┼──────────┼─────────┼────────────────────────────┼────────────────────────────┼──────────────────┤
│ seq    │      1 │        1 │       4 │ 2025-05-20 02:48:49.749338 │ 2025-05-20 02:49:14.302917 │ NULL             │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

-- Filter sequences using WHERE clause
SHOW SEQUENCES WHERE start > 0;

╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│  name  │  start │ interval │ current │         created_on         │         updated_on         │      comment     │
├────────┼────────┼──────────┼─────────┼────────────────────────────┼────────────────────────────┼──────────────────┤
│ seq    │      1 │        1 │       4 │ 2025-05-20 02:48:49.749338 │ 2025-05-20 02:49:14.302917 │ NULL             │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

-- Filter sequences by name pattern
SHOW SEQUENCES LIKE 's%';

╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│  name  │  start │ interval │ current │         created_on         │         updated_on         │      comment     │
├────────┼────────┼──────────┼─────────┼────────────────────────────┼────────────────────────────┼──────────────────┤
│ seq    │      1 │        1 │       4 │ 2025-05-20 02:48:49.749338 │ 2025-05-20 02:49:14.302917 │ NULL             │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯