---
title: REFRESH INVERTED INDEX
sidebar_position: 2
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.405"/>

Databend automatically refreshes inverted indexes in `SYNC` mode whenever new data is written. Use `REFRESH INVERTED INDEX` primarily to backfill rows that existed before the index was declared.

## Syntax

```sql
REFRESH INVERTED INDEX <index> ON [<database>.]<table> [LIMIT <limit>]
```

| Parameter | Description                                                                                                                      |
|-----------|----------------------------------------------------------------------------------------------------------------------------------|
| `<limit>` | Specifies the maximum number of rows to process during index refresh. If not specified, all rows in the table will be processed. |

## Examples

```sql
-- Existing table with data loaded before the index was declared
CREATE TABLE IF NOT EXISTS customer_feedback(id INT, body STRING);
INSERT INTO customer_feedback VALUES
  (1, 'Great coffee beans'),
  (2, 'Needs fresh roasting');

-- Create the inverted index afterward
CREATE INVERTED INDEX customer_feedback_idx ON customer_feedback(body);

-- Backfill historical rows so the index covers earlier inserts
REFRESH INVERTED INDEX customer_feedback_idx ON customer_feedback;

-- Future inserts refresh automatically in SYNC mode
```
