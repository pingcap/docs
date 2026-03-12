---
title: DROP NGRAM INDEX
sidebar_position: 4
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.726"/>

Drops an existing NGRAM index from a table.

## Syntax

```sql
DROP NGRAM INDEX [IF EXISTS] <index_name>
ON [<database>.]<table_name>;
```

## Examples

The following example drops the `idx1` index from the `amazon_reviews_ngram` table:

```sql
DROP NGRAM INDEX idx1 ON amazon_reviews_ngram;
```
