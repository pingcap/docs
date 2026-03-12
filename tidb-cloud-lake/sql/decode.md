---
title: DECODE
---

The DECODE function compares the select expression to each search expression in order. As soon as a search expression matches the selection expression, the corresponding result expression is returned. If no match is found and a default value is provided, the default value is returned.

## Syntax

```sql
DECODE( <expr>, <search1>, <result1> [, <search2>, <result2> ... ] [, <default> ] )
```

## Arguments

- `expr`: The "select expression" that is compared against each search expression. This is typically a column, but can be a subquery, literal, or other expression.
- `searchN`: The search expressions to compare against the select expression. If a match is found, the corresponding result is returned.
- `resultN`: The values that will be returned if the corresponding search expression matches the select expression.
- `default`: Optional. If provided and no search expression matches, this default value is returned.

## Usage Notes

- Unlike `CASE`, a NULL value in the select expression matches a NULL value in the search expressions.
- If multiple search expressions would match, only the first match's result is returned.

## Examples

```sql
CREATE TABLE t (a VARCHAR);
INSERT INTO t (a) VALUES
    ('1'),
    ('2'),
    (NULL),
    ('4');
```

Example with a default value 'other' (note that NULL equals NULL):

```sql
SELECT a, decode(a,
                       1, 'one',
                       2, 'two',
                       NULL, '-NULL-',
                       'other'
                      ) AS decode_result
    FROM t;
```

result:
```
┌─a─┬─decode_result─┐
│ 1 │ one           │
│ 2 │ two           │
│   │ -NULL-        │
│ 4 │ other         │
└───┴───────────────┘
```