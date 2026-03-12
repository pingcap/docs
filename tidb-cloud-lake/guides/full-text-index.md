---
title: Full-Text Index
---

:::info
Looking for a hands-on walkthrough? See [JSON & Search Guide](/guides/query/json-search).
:::

# Full-Text Index: Automatic Lightning-Fast Text Search

Full-text indexes (inverted indexes) automatically enable lightning-fast text searches across large document collections by mapping terms to documents, eliminating the need for slow table scans.

## What Problem Does It Solve?

Text search operations on large datasets face significant performance challenges:

| Problem | Impact | Full-Text Index Solution |
|---------|--------|-------------------------|
| **Slow LIKE Queries** | `WHERE content LIKE '%keyword%'` scans entire tables | Direct term lookup, skip irrelevant documents |
| **Full Table Scans** | Every text search reads all rows | Read only documents containing search terms |
| **Poor Search Experience** | Users wait seconds/minutes for search results | Sub-second search response times |
| **Limited Search Capabilities** | Basic pattern matching only | Advanced features: fuzzy search, relevance scoring |
| **High Resource Usage** | Text searches consume excessive CPU/memory | Minimal resources for indexed searches |

**Example**: Searching for "kubernetes error" in 10M log entries. Without full-text index, it scans all 10M rows. With full-text index, it directly finds the ~1000 matching documents instantly.

## How It Works

Full-text indexes create an inverted mapping from terms to documents:

| Term | Document IDs |
|------|-------------|
| "kubernetes" | 101, 205, 1847 |
| "error" | 101, 892, 1847 |
| "pod" | 205, 1847, 2901 |

When searching for "kubernetes error", the index finds documents containing both terms (101, 1847) without scanning the entire table.

## Quick Setup

```sql
-- Create table with text content
CREATE TABLE logs(id INT, message TEXT, timestamp TIMESTAMP);

-- Create full-text index - automatically indexes new data
CREATE INVERTED INDEX logs_message_idx ON logs(message);

-- One-time refresh needed only for existing data before index creation
REFRESH INVERTED INDEX logs_message_idx ON logs;

-- Search using MATCH function - fully automatic optimization
SELECT * FROM logs WHERE MATCH(message, 'error kubernetes');
```

**Automatic Index Management**:
- **New Data**: Automatically indexed as it's inserted - no manual action needed
- **Existing Data**: One-time refresh required only for data that existed before index creation
- **Ongoing Maintenance**: Databend automatically maintains optimal search performance

## Search Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `MATCH(column, 'terms')` | Basic text search | `MATCH(content, 'database performance')` |
| `QUERY('column:terms')` | Advanced query syntax | `QUERY('title:"full text" AND content:search')` |
| `SCORE()` | Relevance scoring | `SELECT *, SCORE() FROM docs WHERE MATCH(...)` |

## Advanced Search Features

### Fuzzy Search
```sql
-- Find documents even with typos (fuzziness=1 allows 1 character difference)
SELECT * FROM logs WHERE MATCH(message, 'kubernetes', 'fuzziness=1');
```

### Relevance Scoring
```sql
-- Get results with relevance scores, filter by minimum score
SELECT id, message, SCORE() as relevance 
FROM logs 
WHERE MATCH(message, 'critical error') AND SCORE() > 0.5
ORDER BY SCORE() DESC;
```

### Complex Queries
```sql
-- Advanced query syntax with boolean operators
SELECT * FROM docs WHERE QUERY('title:"user guide" AND content:(tutorial OR example)');
```

## Complete Example

This example demonstrates creating a full-text search index on Kubernetes log data and searching using various functions:

```sql
-- Create a table with a computed column
CREATE TABLE k8s_logs (
    event_id INT,
    event_data VARIANT,
    event_timestamp TIMESTAMP,
    event_message VARCHAR AS (event_data['message']::VARCHAR) STORED
);

-- Create an inverted index on the "event_message" column
CREATE INVERTED INDEX event_message_fulltext ON k8s_logs(event_message);

-- Insert comprehensive sample data
INSERT INTO k8s_logs (event_id, event_data, event_timestamp)
VALUES
    (1,
    PARSE_JSON('{
        "message": "Pod scheduled",
        "object_type": "Pod",
        "name": "frontend-1",
        "namespace": "production",
        "node": "node-01",
        "status": "Scheduled"
    }'),
    '2024-04-08T08:00:00Z');

INSERT INTO k8s_logs (event_id, event_data, event_timestamp)
VALUES
    (2,
    PARSE_JSON('{
        "message": "Deployment scaled",
        "object_type": "Deployment",
        "name": "backend",
        "namespace": "development",
        "replicas": 3
    }'),
    '2024-04-08T09:15:00Z');

INSERT INTO k8s_logs (event_id, event_data, event_timestamp)
VALUES
    (3,
    PARSE_JSON('{
        "message": "Node condition changed",
        "object_type": "Node",
        "name": "node-02",
        "condition": "Ready",
        "status": "True"
    }'),
    '2024-04-08T10:30:00Z');

INSERT INTO k8s_logs (event_id, event_data, event_timestamp)
VALUES
    (4,
    PARSE_JSON('{
        "message": "ConfigMap updated",
        "object_type": "ConfigMap",
        "name": "app-config",
        "namespace": "default",
        "change": "data update"
    }'),
    '2024-04-08T11:45:00Z');

INSERT INTO k8s_logs (event_id, event_data, event_timestamp)
VALUES
    (5,
    PARSE_JSON('{
        "message": "PersistentVolume claim created",
        "object_type": "PVC",
        "name": "storage-claim",
        "namespace": "storage",
        "status": "Bound",
        "volume": "pv-logs"
    }'),
    '2024-04-08T12:00:00Z');

-- Basic search for events containing "PersistentVolume"
SELECT
  event_id,
  event_message
FROM
  k8s_logs
WHERE
  MATCH(event_message, 'PersistentVolume');

-[ RECORD 1 ]-----------------------------------
     event_id: 5
event_message: PersistentVolume claim created

-- Verify index usage with EXPLAIN
EXPLAIN SELECT event_id, event_message FROM k8s_logs WHERE MATCH(event_message, 'PersistentVolume');

-[ EXPLAIN ]-----------------------------------
Filter
├── output columns: [k8s_logs.event_id (#0), k8s_logs.event_message (#3)]
├── filters: [k8s_logs._search_matched (#4)]
├── estimated rows: 5.00
└── TableScan
    ├── table: default.default.k8s_logs
    ├── output columns: [event_id (#0), event_message (#3), _search_matched (#4)]
    ├── read rows: 1
    ├── read size: < 1 KiB
    ├── partitions total: 5
    ├── partitions scanned: 1
    ├── pruning stats: [segments: <range pruning: 5 to 5>, blocks: <range pruning: 5 to 5, inverted pruning: 5 to 1>]
    ├── push downs: [filters: [k8s_logs._search_matched (#4)], limit: NONE]
    └── estimated rows: 5.00

-- Advanced search with relevance scoring
SELECT
  event_id,
  event_message,
  event_timestamp,
  SCORE()
FROM
  k8s_logs
WHERE
  SCORE() > 0.5
  AND QUERY('event_message:"PersistentVolume claim created"');

-[ RECORD 1 ]-----------------------------------
       event_id: 5
  event_message: PersistentVolume claim created
event_timestamp: 2024-04-08 12:00:00
        score(): 0.86304635

-- Fuzzy search example (handles typos)
SELECT
    event_id, event_message, event_timestamp
FROM
    k8s_logs
WHERE
    match('event_message', 'PersistentVolume claim create', 'fuzziness=1');

-[ RECORD 1 ]-----------------------------------
       event_id: 5
  event_message: PersistentVolume claim created
event_timestamp: 2024-04-08 12:00:00
```

**Key Points from the Example:**
- `inverted pruning: 5 to 1` shows the index reduced blocks scanned from 5 to 1
- Relevance scoring helps rank results by match quality
- Fuzzy search finds results even with typos ("create" vs "created")

## Best Practices

| Practice | Benefit |
|----------|---------|
| **Index Frequently Searched Columns** | Focus on columns used in search queries |
| **Use MATCH Instead of LIKE** | Leverage automatic index performance |
| **Monitor Index Usage** | Use EXPLAIN to verify index utilization |
| **Consider Multiple Indexes** | Different columns can have separate indexes |

## Essential Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `CREATE INVERTED INDEX name ON table(column)` | Create new full-text index | Initial setup - automatic for new data |
| `REFRESH INVERTED INDEX name ON table` | Index existing data | One-time only for pre-existing data |
| `DROP INVERTED INDEX name ON table` | Remove index | When index no longer needed |

## Important Notes

:::tip
**When to Use Full-Text Indexes:**
- Large text datasets (documents, logs, comments)
- Frequent text search operations
- Need for advanced search features (fuzzy, scoring)
- Performance-critical search applications

**When NOT to Use:**
- Small text datasets
- Exact string matching only
- Infrequent search operations
:::

## Index Limitations

- Each column can only be in one inverted index
- Requires refresh after data insertion (if data existed before index creation)
- Uses additional storage space for index data

---

*Full-text indexes are essential for applications requiring fast, sophisticated text search capabilities across large document collections.*
