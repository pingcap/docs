---
title: FLATTEN
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.213"/>

Transforms nested JSON or array data into a tabular format, where each element or field is represented as a separate row.

## Syntax

```sql
[LATERAL] FLATTEN (
  INPUT => <expr>
  [, PATH => <expr>]
  [, OUTER => TRUE | FALSE]
  [, RECURSIVE => TRUE | FALSE]
  [, MODE => 'OBJECT' | 'ARRAY' | 'BOTH']
)
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `INPUT` | JSON or array data to flatten | Required |
| `PATH` | Path to the array/object to flatten | None |
| `OUTER` | Include rows with zero results (with NULL values) | `FALSE` |
| `RECURSIVE` | Flatten nested elements | `FALSE` |
| `MODE` | Flatten objects, arrays, or both | `'BOTH'` |
| `LATERAL` | Enable cross-referencing with preceding table expressions | Optional |

## Output Columns

| Column | Description |
|--------|-------------|
| `SEQ` | Sequence number for the input |
| `KEY` | Key of the expanded value (NULL if none) |
| `PATH` | Path to the flattened element |
| `INDEX` | Array index (NULL for objects) |
| `VALUE` | Value of the flattened element |
| `THIS` | Element being flattened |

**Note:** When using LATERAL, output columns may vary due to dynamic cross-referencing.

## Examples

### Basic Flattening

```sql
-- Flatten a JSON object with nested structures
SELECT * FROM FLATTEN(
  INPUT => PARSE_JSON(
    '{"name": "John", "languages": ["English", "Spanish"], "address": {"city": "New York"}}'
  )
);
```

Results in top-level keys being flattened:

```text
| seq | key       | path      | index | value                | this                 |
|-----|-----------|-----------|-------|----------------------|----------------------|
| 1   | name      | name      | NULL  | "John"               | {original JSON}      |
| 1   | languages | languages | NULL  | ["English","Spanish"]| {original JSON}      |
| 1   | address   | address   | NULL  | {"city":"New York"}  | {original JSON}      |
```

### Using PATH Parameter

```sql
-- Flatten only the languages array by specifying the PATH
SELECT * FROM FLATTEN(
  INPUT => PARSE_JSON(
    '{"name": "John", "languages": ["English", "Spanish"]}'
  ),
  PATH => 'languages'
);
```

Results in array elements being flattened:

```text
| seq | key  | path         | index | value     | this               |
|-----|------|--------------|-------|-----------|-------------------|
| 1   | NULL | languages[0] | 0     | "English" | ["English","Spanish"] |
| 1   | NULL | languages[1] | 1     | "Spanish" | ["English","Spanish"] |
```

### Recursive Flattening

```sql
-- Recursively flatten nested objects and arrays
SELECT * FROM FLATTEN(
  INPUT => PARSE_JSON(
    '{"name": "John", "address": {"city": "New York", "zip": 10001}}'
  ),
  RECURSIVE => TRUE
);
```

Results in nested objects being flattened:

```text
| seq | key     | path         | index | value       | this            |
|-----|---------|--------------|-------|-------------|-----------------|
| 1   | name    | name         | NULL  | "John"      | {original JSON} |
| 1   | address | address      | NULL  | {"city":...}| {original JSON} |
| 1   | city    | address.city | NULL  | "New York"  | {"city":...}    |
| 1   | zip     | address.zip  | NULL  | 10001       | {"city":...}    |
```

### Using LATERAL FLATTEN

```sql
-- Use LATERAL FLATTEN to transform a JSON array into rows
-- This allows direct access to array elements without a table
SELECT 
  f.value:item::STRING AS item_name,
  f.value:price::FLOAT AS price
FROM 
  LATERAL FLATTEN(
    INPUT => PARSE_JSON('[
      {"item":"coffee", "price":2.50}, 
      {"item":"donut", "price":1.20}
    ]')
  ) f;
```

Results:

```text
| item_name | price |
|-----------|-------|
| coffee    | 2.5   |
| donut     | 1.2   |
```
