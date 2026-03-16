---
title: CREATE NGRAM INDEX
sidebar_position: 1
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.726"/>

Creates an Ngram index on a column for a table.

## Syntax

```sql
-- Create an Ngram index on an existing table
CREATE [OR REPLACE] NGRAM INDEX [IF NOT EXISTS] <index_name>
ON [<database>.]<table_name>(<column>)
[gram_size = <number>] [bloom_size = <number>]

-- Create an Ngram index when creating a table
CREATE [OR REPLACE] TABLE <table_name> (
    <column_definitions>,
    NGRAM INDEX <index_name> (<column>)
        [gram_size = <number>] [bloom_size = <number>]
)...
```

- `gram_size` (defaults to 3) specifies the length of each character-based substring (n-gram) when the column text is indexed. For example, with `gram_size = 3`, the text "hello world" would be split into overlapping substrings like:

  ```text
  "hel", "ell", "llo", "lo ", "o w", " wo", "wor", "orl", "rld"
  ```

- `bloom_size` specifies the size in bytes of the Bloom filter bitmap used to accelerate string matching within each block of data. It controls the trade-off between index accuracy and memory usage:

  - A larger `bloom_size` reduces false positives in string lookups, improving query precision at the cost of more memory.
  - A smaller `bloom_size` saves memory but may increase false positives.
  - If not explicitly set, the default is 1,048,576 bytes (1m) per indexed column per block. The valid range is from 512 bytes to 10,485,760 bytes (10m).

## Examples

### Creating a Table with NGRAM Index

```sql
CREATE TABLE articles (
    id INT,
    title VARCHAR,
    content STRING,
    NGRAM INDEX idx_content (content)
);
```

### Creating an NGRAM Index on an Existing Table

```sql
CREATE TABLE products (
    id INT,
    name VARCHAR,
    description STRING
);

CREATE NGRAM INDEX idx_description
ON products(description);
```

### Viewing Indexes

```sql
SHOW INDEXES;
```

Result:
```
┌─────────────────┬───────┬──────────┬─────────────────────────┬──────────────────────────┐
│ name            │ type  │ original │ definition              │ created_on               │
├─────────────────┼───────┼──────────┼─────────────────────────┼──────────────────────────┤
│ idx_content     │ NGRAM │          │ articles(content)       │ 2025-05-13 01:22:34.123  │
│ idx_description │ NGRAM │          │ products(description)   │ 2025-05-13 01:23:45.678  │
└─────────────────┴───────┴──────────┴─────────────────────────┴──────────────────────────┘
```

### Using NGRAM Index

```sql
-- Create a table with NGRAM index
CREATE TABLE phrases (
    id INT,
    text STRING,
    NGRAM INDEX idx_text (text)
);

-- Insert sample data
INSERT INTO phrases VALUES
(1, 'apple banana cherry'),
(2, 'banana date fig'),
(3, 'cherry elderberry fig'),
(4, 'date grape kiwi');

-- Query using fuzzy matching with the NGRAM index
SELECT * FROM phrases WHERE text LIKE '%banana%';
```

Result:
```
┌────┬─────────────────────┐
│ id │ text                │
├────┼─────────────────────┤
│  1 │ apple banana cherry │
│  2 │ banana date fig     │
└────┴─────────────────────┘
```

### Dropping an NGRAM Index

```sql
DROP NGRAM INDEX idx_text ON phrases;
```
