---
title: DROP INVERTED INDEX
summary: Removes an inverted index in Databend.
---

# DROP INVERTED INDEX

> **Note:**
>
> Introduced or updated in v1.2.405.

Removes an inverted index in Databend.

## Syntax

```sql
DROP INVERTED INDEX [IF EXISTS] <index> ON [<database>.]<table>
```

## Examples

```sql
-- Drop the inverted index 'customer_feedback_idx' on the 'customer_feedback' table
DROP INVERTED INDEX customer_feedback_idx ON customer_feedback;
```
