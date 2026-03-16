---
title: REFRESH VECTOR INDEX
sidebar_position: 2
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.777"/>

Builds a Vector index for existing data that was inserted before the index was created.

## Syntax

```sql
REFRESH VECTOR INDEX <index_name> ON [<database>.]<table_name>
```

## When to Use REFRESH

`REFRESH VECTOR INDEX` is **only needed in one specific scenario**: when you create a Vector index on a table that **already contains data**.

The existing rows (written before the index was created) will not be automatically indexed. You must run `REFRESH VECTOR INDEX` to build the index for this pre-existing data. After the refresh completes, all subsequent data writes will automatically generate the index.

## Examples

### Example: Index Existing Data

```sql
-- Step 1: Create a table without an index
CREATE TABLE products (
    id INT,
    name VARCHAR,
    embedding VECTOR(4)
) ENGINE = FUSE;

-- Step 2: Insert data (without index)
INSERT INTO products VALUES
    (1, 'Product A', [0.1, 0.2, 0.3, 0.4]),
    (2, 'Product B', [0.5, 0.6, 0.7, 0.8]),
    (3, 'Product C', [0.9, 1.0, 1.1, 1.2]);

-- Step 3: Create vector index on existing data
CREATE VECTOR INDEX idx_embedding ON products(embedding) distance='cosine';

-- Step 4: Refresh to build index for the 3 existing rows
REFRESH VECTOR INDEX idx_embedding ON products;

-- Step 5: New insertions are automatically indexed (no refresh needed)
INSERT INTO products VALUES (4, 'Product D', [1.3, 1.4, 1.5, 1.6]);
```
