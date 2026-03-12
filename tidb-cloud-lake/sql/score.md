---
title: SCORE
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.425"/>

`SCORE()` returns the relevance score assigned to the current row by the inverted index search. Use it together with [MATCH](match) or [QUERY](query) in a `WHERE` clause.

:::info
Databend's SCORE function is inspired by Elasticsearch's [SCORE](https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-functions-search.html#sql-functions-search-score).
:::

## Syntax

```sql
SCORE()
```

## Examples

### Example: Prepare Text Notes for MATCH

```sql
CREATE OR REPLACE TABLE frame_notes (
  id INT,
  camera STRING,
  summary STRING,
  tags STRING,
  INVERTED INDEX idx_notes (summary, tags)
);

INSERT INTO frame_notes VALUES
  (1, 'dashcam_front',
      'Green light at Market & 5th with pedestrian entering the crosswalk',
      'downtown commute green-light pedestrian'),
  (2, 'dashcam_front',
      'Vehicle stopped at Mission & 6th red traffic light with cyclist ahead',
      'stop urban red-light cyclist'),
  (3, 'dashcam_front',
      'School zone caution sign in SOMA with pedestrian waiting near crosswalk',
      'school-zone caution pedestrian');
```

### Example: Score MATCH Results

```sql
SELECT summary, SCORE()
FROM frame_notes
WHERE MATCH('summary^2, tags', 'traffic light red', 'operator=AND')
ORDER BY SCORE() DESC;
```

### Example: Score QUERY Results

Reusing the `frames` table from the [QUERY](query) examples:

```sql
SELECT id, SCORE()
FROM frames
WHERE QUERY('meta.detections.label:pedestrian^3 AND meta.scene.time_of_day:day');
```
