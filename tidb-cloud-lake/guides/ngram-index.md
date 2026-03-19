---
title: Ngram Index
summary: Ngram indexes accelerate pattern matching queries using the LIKE operator with wildcards (%), enabling fast substring searches without full table scans.
---

# Ngram Index

Ngram indexes accelerate pattern matching queries using the `LIKE` operator with wildcards (`%`), enabling fast substring searches without full table scans.

## What Problem Does It Solve?

Pattern matching with `LIKE` queries faces significant performance challenges on large datasets:

| Problem | Impact | Ngram Index Solution |
|---------|--------|---------------------|
| **Slow Wildcard Searches** | `WHERE content LIKE '%keyword%'` scans entire tables | Pre-filter data blocks using n-gram segments |
| **Full Table Scans** | Every pattern search reads all rows | Read only relevant data blocks containing patterns |
| **Poor Search Performance** | Users wait long for substring search results | Sub-second pattern matching response times |
| **Ineffective Traditional Indexes** | B-tree indexes can't optimize middle wildcards | Character-level indexing handles any wildcard position |

**Example**: Searching for `'%error log%'` in 10M log entries. Without ngram index, it scans all 10M rows. With ngram index, it pre-filters to ~1000 relevant blocks instantly.

## Ngram vs Full-Text Index: When to Use Which?

| Feature | Ngram Index | Full-Text Index |
|---------|-------------|-----------------|
| **Primary Use Case** | Pattern matching with `LIKE '%pattern%'` | Semantic text search with `MATCH()` |
| **Search Type** | Exact substring matching | Word-based search with relevance |
| **Query Syntax** | `WHERE column LIKE '%text%'` | `WHERE MATCH(column, 'text')` |
| **Advanced Features** | Case-insensitive matching | Fuzzy search, relevance scoring, boolean operators |
| **Performance Focus** | Accelerate existing LIKE queries | Replace LIKE with advanced search functions |
| **Best For** | Log analysis, code search, exact pattern matching | Document search, content discovery, search engines |

**Choose Ngram Index when:**
- You have existing `LIKE '%pattern%'` queries to optimize
- Need exact substring matching (case-insensitive)
- Working with structured data like logs, codes, or IDs
- Want to improve performance without changing query syntax

**Choose Full-Text Index when:**
- Building search functionality for documents or content
- Need fuzzy search, relevance scoring, or complex queries
- Working with natural language text
- Want advanced search capabilities beyond simple pattern matching

## How Ngram Index Works

Ngram indexes break text into overlapping character substrings (n-grams) for fast pattern lookup:

**Example with `gram_size = 3`:**
```text
Input: "The quick brown"
N-grams: "The", "he ", "e q", " qu", "qui", "uic", "ick", "ck ", "k b", " br", "bro", "row", "own"
```

**Query Processing:**
```sql
SELECT * FROM t WHERE content LIKE '%quick br%'
```
1. Pattern `'quick br'` is tokenized into n-grams: "qui", "uic", "ick", "ck ", "k b", " br"
2. Index filters data blocks containing these n-grams
3. Full `LIKE` filter applied only to pre-filtered blocks

> **Note:**
>
> - Pattern must be at least `gram_size` characters long (short patterns like `'%yo%'` with `gram_size=3` won't use the index)
> - Matches are case-insensitive ("FOO" matches "foo", "Foo", "fOo")
> - Only works with `LIKE` operator, not with other pattern matching functions

## Quick Setup

```sql
-- Create table with text content
CREATE TABLE logs(id INT, message STRING);

-- Create ngram index with 3-character segments
CREATE NGRAM INDEX logs_message_idx ON logs(message) gram_size = 3;

-- Insert data (automatically indexed)
INSERT INTO logs VALUES (1, 'Application error occurred');

-- Search using LIKE - automatically optimized
SELECT * FROM logs WHERE message LIKE '%error%';
```

## Complete Example

This example demonstrates creating an ngram index for log analysis and verifying its performance benefits:

```sql
-- Create table for application logs
CREATE TABLE t_articles (
    id INT,
    content STRING
);

-- Create ngram index with 3-character segments
CREATE NGRAM INDEX ngram_idx_content
ON t_articles(content)
gram_size = 3;

-- Verify index creation
SHOW INDEXES;
```

```sql
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│        name       │  type  │ original │            definition            │         created_on         │      updated_on     │
├───────────────────┼────────┼──────────┼──────────────────────────────────┼────────────────────────────┼─────────────────────┤
│ ngram_idx_content │ NGRAM  │          │ t_articles(content)gram_size='3' │ 2025-05-13 01:02:58.598409 │ NULL                │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```sql
-- Insert test data: 995 irrelevant rows + 5 target rows
INSERT INTO t_articles
SELECT number, CONCAT('Random text number ', number)
FROM numbers(995);

INSERT INTO t_articles VALUES
    (1001, 'The silence was deep and complete'),
    (1002, 'They walked in silence through the woods'),
    (1003, 'Silence fell over the room'),
    (1004, 'A moment of silence was observed'),
    (1005, 'In silence, they understood each other');

-- Search with pattern matching
SELECT id, content FROM t_articles WHERE content LIKE '%silence%';

-- Verify index usage
EXPLAIN SELECT id, content FROM t_articles WHERE content LIKE '%silence%';
```

**Performance Results:**
```sql
-[ EXPLAIN ]-----------------------------------
TableScan
├── table: default.default.t_articles
├── output columns: [id (#0), content (#1)]
├── read rows: 5
├── read size: < 1 KiB
├── partitions total: 2
├── partitions scanned: 1
├── pruning stats: [segments: <range pruning: 2 to 2>, blocks: <range pruning: 2 to 2, bloom pruning: 2 to 1>]
├── push downs: [filters: [is_true(like(t_articles.content (#1), '%silence%'))], limit: NONE]
└── estimated rows: 15.62
```

**Key Performance Indicator:** `bloom pruning: 2 to 1` shows the ngram index successfully filtered out 50% of data blocks before scanning.

## Best Practices

| Practice | Benefit |
|----------|---------|
| **Choose Appropriate gram_size** | `gram_size=3` works well for most cases; larger values for longer patterns |
| **Index Frequently Searched Columns** | Focus on columns used in `LIKE '%pattern%'` queries |
| **Monitor Index Usage** | Use `EXPLAIN` to verify `bloom pruning` statistics |
| **Consider Pattern Length** | Ensure search patterns are at least `gram_size` characters long |

## Essential Commands

For complete command reference, see [Ngram Index](/tidb-cloud-lake/sql/ngram-index-sql.md).

| Command                                                  | Purpose                                      |
|----------------------------------------------------------|----------------------------------------------|
| `CREATE NGRAM INDEX name ON table(column) gram_size = N` | Create ngram index with N-character segments |
| `SHOW INDEXES`                                           | List all indexes including ngram indexes     |
| `REFRESH NGRAM INDEX name ON table`                      | Refresh ngram index                          |
| `DROP NGRAM INDEX name ON table`                         | Remove ngram index                           |

**When to Use Ngram Indexes**

**Ideal for:**
- Log analysis and monitoring systems
- Code search and pattern matching
- Product catalog searches
- Any application with frequent `LIKE '%pattern%'` queries

**Not recommended for:**
- Short pattern searches (less than `gram_size` characters)
- Exact string matching (use equality comparison instead)
- Complex text search requirements (use Full-Text Index instead)

---

*Ngram indexes are essential for applications requiring fast pattern matching with `LIKE` queries on large text datasets.*
