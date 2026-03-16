---
title: REFRESH NGRAM INDEX
sidebar_position: 2
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.726"/>

Databend automatically refreshes NGRAM indexes when data is ingested. Use `REFRESH NGRAM INDEX` when you need to backfill data that existed before the index was defined.

## Syntax

```sql
REFRESH NGRAM INDEX [IF EXISTS] <index_name>
ON [<database>.]<table_name>;
```

## Examples

```sql
-- Table already populated before the NGRAM index exists
CREATE TABLE IF NOT EXISTS amazon_reviews_ngram(review_id INT, review STRING);
INSERT INTO amazon_reviews_ngram VALUES
  (1, 'coffee beans from Colombia'),
  (2, 'best roasting kit');

-- Declare the NGRAM index afterward
CREATE NGRAM INDEX idx1 ON amazon_reviews_ngram(review) WITH (ngram_size = 3);

-- Refresh so the pre-existing rows are indexed
REFRESH NGRAM INDEX idx1 ON amazon_reviews_ngram;

-- Subsequent inserts refresh automatically in SYNC mode
```
