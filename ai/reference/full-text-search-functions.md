---
title: Full-Text Search Functions
summary: Learn the full-text search functions in TiDB, including query syntax, multi-column search, parser selection, and index selection hints.
aliases: ['/tidb/stable/full-text-search-functions/','/tidbcloud/full-text-search-functions/']
---

# Full-Text Search Functions

This document describes the `FTS_MATCH_WORD()` function for full-text search in TiDB, including multi-column search, query semantics with different parsers, parser selection, and index selection hints.

For how to create the full-text indexes that these functions use, see [Full-Text Search Index](/ai/reference/full-text-search-index.md).

## FTS_MATCH_WORD()

`FTS_MATCH_WORD()` performs a keyword search against one or more scored columns of a full-text index and returns a BM25 relevance score.

```
FTS_MATCH_WORD('query' [WITH PARSER parser_name], col [, col...])
```

| Parameter | Description |
| :-- | :-- |
| `query` | The search text. It is tokenized according to the parser rules of the matched index. |
| `WITH PARSER parser_name` | Optional. Explicitly selects which parser to use when the scored column has multiple parsers. Only a parser name is accepted, such as `multilingual` or `ngram`. Parser parameters are not allowed. See [Select a parser explicitly](#select-a-parser-explicitly). |
| `col [, col...]` | One or more scored columns. The columns can be a subset of the scored columns of a full-text index. |

Filter conditions on filter columns are written outside the function, as independent `WHERE` conditions:

```sql
SELECT * FROM t
WHERE FTS_MATCH_WORD('database', content_text)
  AND path LIKE '/src/%'
  AND name = 'main.go'
ORDER BY FTS_MATCH_WORD('database', content_text) DESC
LIMIT 10;
```

If a column in `col [, col...]` does not exist in the table, TiDB reports `ERROR 1054 (42S22): Unknown column 'xxx' in 'fts_match_word'`.

## Multi-column search

You can search multiple scored columns in a single call. Columns are combined with **OR** semantics: `FTS_MATCH_WORD('query', col1, col2)` matches documents where `col1` matches the query or `col2` matches the query, and BM25 scores are fused at the index level.

```sql
SELECT * FROM t
WHERE FTS_MATCH_WORD('database', content_text, description)
ORDER BY FTS_MATCH_WORD('database', content_text, description) DESC
LIMIT 10;
```

To require all columns to match (**AND** semantics), combine multiple `FTS_MATCH_WORD()` calls with `AND` in the `WHERE` clause:

```sql
SELECT * FROM t
WHERE FTS_MATCH_WORD('database', content_text)
  AND FTS_MATCH_WORD('database', description);
```

In a multi-column query, each column is tokenized by the parser defined for that column in the index, and the BM25 scores are fused at the index level. A query can also use a subset of the scored columns of an index. For example, if an index covers `content_text` and `description`, `FTS_MATCH_WORD('query', content_text)` still uses that index.

## Multi-word query semantics

When the query string contains multiple words, it is tokenized according to the parser rules, and each token is matched independently. `FTS_MATCH_WORD()` uses **OR** semantics across tokens: a document matches if it contains any of the tokens, and matching more tokens increases the relevance score.

```sql
-- This query is tokenized into two tokens: "Alice" and "Smith".
-- It returns all rows where name contains "Alice" or "Smith" or both.
SELECT * FROM users WHERE FTS_MATCH_WORD('Alice Smith', name);
```

To require multiple words to match (**AND** semantics), combine multiple `FTS_MATCH_WORD()` calls with `AND`. The optimizer merges the conditions into a single index scan:

```sql
SELECT * FROM t
WHERE FTS_MATCH_WORD('database', content_text)
  AND FTS_MATCH_WORD('vector', content_text);
```

Similarly, multiple calls combined with `OR` are merged into one scan with OR semantics:

```sql
SELECT * FROM t
WHERE FTS_MATCH_WORD('database', content_text)
  OR FTS_MATCH_WORD('vector', content_text);
```

## Query semantics with the NGRAM parser

When the matched index uses the `NGRAM` parser, `FTS_MATCH_WORD()` performs substring matching. The query string is split into n-grams using the same `min_gram` and `max_gram` settings as the index, and the n-grams are combined with **AND** semantics by default.

For example, with `min_gram=max_gram=3`, searching `apple` is equivalent to searching `app` AND `ppl` AND `ple`: all n-grams must match in the same document.

```sql
SELECT /*+ USE_INDEX(t, idx_fts_ngram) */ *
FROM t
WHERE FTS_MATCH_WORD('handle', content_text);
-- Matches HandleRequest, RequestHandler, and handle_error
```

To use OR semantics between n-grams, combine multiple `FTS_MATCH_WORD()` calls with `OR`:

```sql
SELECT * FROM t
WHERE FTS_MATCH_WORD('app', content_text)
  OR FTS_MATCH_WORD('ppl', content_text);
```

## Relevance scoring

`FTS_MATCH_WORD()` returns a BM25 relevance score. The score is a non-negative floating-point number. A higher value indicates higher relevance. Scores are not directly comparable across different datasets.

If the query string contains repeated terms, the term frequency of that term is counted multiple times in scoring. For example, in `FTS_MATCH_WORD('Alice alice bob', name)`, the term `Alice` contributes twice the weight of `bob`. This is expected BM25 behavior.

For the full scoring formula and parameters, see [Relevance scoring algorithm](/ai/guides/vector-search-full-text-search-sql.md#relevance-scoring-algorithm).

## Select a parser explicitly

When a scored column has multiple parsers (for example, `content_text WITH (multilingual, ngram(...))`), use the `WITH PARSER` clause inside the function to select one explicitly. Only a parser name is accepted. Parser parameters such as `WITH PARSER ngram(min_gram=5)` are not allowed and return an error.

```sql
-- Use the ngram parser explicitly
SELECT * FROM t
WHERE FTS_MATCH_WORD('handle' WITH PARSER ngram, content_text);

-- Without WITH PARSER, the first compatible parser in the index definition is used
SELECT * FROM t
WHERE FTS_MATCH_WORD('database', content_text);
```

Parser selection rules:

| Scenario | Behavior |
| :-- | :-- |
| `WITH PARSER parser_name` is specified, and the column has an index with that parser | The specified parser is used. |
| `WITH PARSER parser_name` is specified, but the column has no index with that parser | An error is returned: `ERROR: Parser 'xxx' not found for column 'yyy' in fts_match_word`. TiDB does not silently fall back to another parser. |
| `WITH PARSER` is omitted, and the column has one compatible parser | That parser is used. |
| `WITH PARSER` is omitted, and the column has multiple compatible parsers | The first compatible parser in the index definition is used. If `USE_INDEX` is also specified, the parser of the specified index is used. See [Choose a full-text index at query time](#choose-a-full-text-index-at-query-time). |

> **Note:**
>
> Parser selection is part of query semantics, not performance tuning. Different parsers return different results. For this reason, you select a parser with `WITH PARSER` inside the function, not with an optimizer hint. If the specified parser does not exist, TiDB reports an error instead of falling back silently, so that results always match the parser you requested.

## Choose a full-text index at query time

When a table has multiple full-text indexes, you can control which index is used:

### USE_INDEX: specify an index explicitly

```sql
-- Use the NGRAM index (substring matching)
SELECT /*+ USE_INDEX(t, idx_fts_ngram) */ *
FROM t WHERE FTS_MATCH_WORD('handle', content_text);

-- Use the MULTILINGUAL index (complete token matching)
SELECT /*+ USE_INDEX(t, idx_fts_ml) */ *
FROM t WHERE FTS_MATCH_WORD('database', content_text);
```

`USE_INDEX` semantics:

| Scenario | Behavior |
| :-- | :-- |
| Intended use case | Select among multiple indexes that use the same parser. This is a pure execution-path choice. |
| Conflicts with `WITH PARSER` in the function (the specified index does not contain that parser) | `USE_INDEX` is ignored. The parser in `WITH PARSER` takes precedence, and TiDB selects another index that contains that parser. |
| `WITH PARSER` is not specified | TiDB follows `USE_INDEX` and uses the specified index and its parser. |
| The specified index does not exist | The hint is silently ignored, and the optimizer selects an index automatically. |

### IGNORE_INDEX: exclude an index

```sql
SELECT /*+ IGNORE_INDEX(t, idx_fts_ngram) */ *
FROM t WHERE FTS_MATCH_WORD('handle', content_text);
```

### Automatic index selection

Without hints, the optimizer selects a full-text index by the following priorities:

| Priority | Rule |
| :-- | :-- |
| 1 | Column coverage: prefer the index whose scored columns overlap most with the columns in the query. |
| 2 | Filter column coverage: prefer the index that matches more filter conditions in the `WHERE` clause. |
| 3 | Index size: prefer the smaller index to reduce scan cost. |

The optimizer also compares the full-text index scan against a full table scan or a regular index scan, and chooses the path with the lowest estimated cost. See [Full-Text Search Observability](/ai/reference/full-text-search-observability.md) for how to check the selected plan.

## Supported query patterns

- Single-table queries with filter conditions, aggregation, ordering, and pagination:

    ```sql
    SELECT category, COUNT(*) FROM t
    WHERE FTS_MATCH_WORD('query', content_text) GROUP BY category;

    SELECT * FROM t WHERE FTS_MATCH_WORD('query', content_text)
    ORDER BY FTS_MATCH_WORD('query', content_text) DESC LIMIT 10;
    ```

- `INNER JOIN`, where the full-text search runs on the driving table and the join runs on the result set:

    ```sql
    SELECT a.*, b.* FROM articles a
    INNER JOIN authors b ON a.author_id = b.id
    WHERE FTS_MATCH_WORD('database', a.content_text);
    ```

- `UNION`, `UNION ALL`, `EXCEPT`, and `INTERSECT`. Each branch matches its full-text index independently, and the branch results are combined by the set operator. The outer `ORDER BY` and `LIMIT` of the compound statement run after the set operation and are not pushed into the full-text scans.

For restrictions such as `ORDER BY` limitations and join support, see [Full-Text Search Limitations](/ai/reference/full-text-search-limitations.md).

## See also

- [Full-Text Search with SQL](/ai/guides/vector-search-full-text-search-sql.md)
- [Full-Text Search Index](/ai/reference/full-text-search-index.md)
- [Full-Text Search Limitations](/ai/reference/full-text-search-limitations.md)
