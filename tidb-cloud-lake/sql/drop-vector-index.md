---
title: DROP VECTOR INDEX
sidebar_position: 3
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.777"/>

Removes a Vector index from a table.

## Syntax

```sql
DROP VECTOR INDEX [IF EXISTS] <index_name> ON [<database>.]<table_name>
```

## Examples

```sql
-- Create a table with a vector index
CREATE TABLE articles (
    id INT,
    title VARCHAR,
    embedding VECTOR(768),
    VECTOR INDEX idx_embedding(embedding) distance = 'cosine'
);

-- Drop the vector index
DROP VECTOR INDEX idx_embedding ON articles;

-- Drop with IF EXISTS to avoid errors if index doesn't exist
DROP VECTOR INDEX IF EXISTS idx_embedding ON articles;
```
