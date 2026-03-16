---
title: MATCH
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.619"/>

`MATCH` searches for rows that contain the supplied keywords within the listed columns. The function can only appear in a `WHERE` clause.

:::info
Databend's MATCH function is inspired by Elasticsearch's [MATCH](https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-functions-search.html#sql-functions-search-match).
:::

## Syntax

```sql
MATCH('<columns>', '<keywords>'[, '<options>'])
```

- `<columns>`: A comma-separated list of columns to search. Append `^<boost>` to weight a column higher than the others.
- `<keywords>`: The terms to search for. Append `*` for suffix matching, for example `rust*`.
- `<options>`: An optional semicolon-separated list of `key=value` pairs fine-tuning the search.

## Options

| Option | Values | Description | Example |
|--------|--------|-------------|---------|
| `fuzziness` | `1` or `2` | Matches keywords within the specified Levenshtein distance. | `MATCH('summary, tags', 'pedestrain', 'fuzziness=1')` matches rows that contain the correctly spelled `pedestrian`. |
| `operator` | `OR` (default) or `AND` | Controls how multiple keywords are combined when no boolean operator is specified. | `MATCH('summary, tags', 'traffic light red', 'operator=AND')` requires both words. |
| `lenient` | `true` or `false` | When `true`, suppresses parsing errors and returns an empty result set. | `MATCH('summary, tags', '()', 'lenient=true')` returns no rows instead of an error. |

## Examples

In many AI pipelines you may capture structured metadata in a `VARIANT` column while also materializing human-readable summaries for search. The following example stores dashcam frame summaries and tags that were extracted from the JSON payload.

### Example: Build Searchable Summaries

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

### Example: Boolean AND

```sql
SELECT id, summary
FROM frame_notes
WHERE MATCH('summary, tags', 'traffic light red', 'operator=AND');
-- Returns id 2
```

### Example: Fuzzy Matching

```sql
SELECT id, summary
FROM frame_notes
WHERE MATCH('summary^2, tags', 'pedestrain', 'fuzziness=1');
-- Returns ids 1 and 3
```
