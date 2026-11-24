---
title: TiDB Full-Text Search Functions
summary: Learn how to search text with the FTS_MATCH_WORD() function, including multi-column queries and full-text index selection.
---

# TiDB Full-Text Search Functions

This document describes the `FTS_MATCH_WORD()` function for full-text search in TiDB, including multi-column search, multi-word queries, and how to select the full-text index that a query runs on.

For how to create the full-text indexes that these functions use, see [Full-Text Search Index](/ai/reference/full-text-search-index.md).

> **Note:**
>
> Currently, full-text search is **available only on {{{ .starter }}}** in [select regions](/ai/reference/full-text-search-index.md#prerequisites).

## FTS_MATCH_WORD()

`FTS_MATCH_WORD()` performs a keyword search against one or more scored columns of a full-text index and returns a BM25 relevance score.

```
FTS_MATCH_WORD('query', col [, col...])
```

| Parameter | Description |
| :-- | :-- |
| `query` | The search text. It is tokenized according to the parser of the full-text index that the query runs on. |
| `col [, col...]` | One or more scored columns. The columns can be a subset of the scored columns of a full-text index. |

To search the same column with different parsers, create one full-text index per parser and select the index with the `USE_INDEX` hint. See [Select a parser for a scored column](#select-a-parser-for-a-scored-column).

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

A single call is the way to search several columns at once, because multiple calls in one `WHERE` clause can only be combined with `OR`. To require all columns to match (**AND** semantics), intersect the row set of one call per column:

```sql
SELECT id FROM t WHERE FTS_MATCH_WORD('database', content_text)
INTERSECT
SELECT id FROM t WHERE FTS_MATCH_WORD('database', description);
```

In a multi-column query, each column is tokenized by the parser defined for that column in the index, and the BM25 scores are fused at the index level. A query can also use a subset of the scored columns of an index. For example, if an index covers `content_text` and `description`, `FTS_MATCH_WORD('query', content_text)` still uses that index.

## Multi-word query semantics

When the query string contains multiple words, it is tokenized according to the parser rules, and each token is matched independently. `FTS_MATCH_WORD()` uses **OR** semantics across tokens: a document matches if it contains any of the tokens, and matching more tokens increases the relevance score.

```sql
-- This query is tokenized into two tokens: "Alice" and "Smith".
-- It returns all rows where name contains "Alice" or "Smith" or both.
SELECT * FROM users WHERE FTS_MATCH_WORD('Alice Smith', name);
```

Multiple calls combined with `OR` are merged into one index scan:

```sql
SELECT * FROM t
WHERE FTS_MATCH_WORD('database', content_text)
   OR FTS_MATCH_WORD('vector', content_text);
```

Combining multiple calls with `AND` at the top level of `WHERE` is not supported. TiDB reports the following error, even when the two calls use different words or different columns:

```
ERROR 1221 (HY000): Currently 'FTS_MATCH_WORD()' must be used alone. It cannot be placed inside any other function or expression as a parameter, or used multiple times.
```

To require multiple words to match (**AND** semantics), or to exclude documents that match a word (**NOT** semantics), use a compound statement:

```sql
-- AND: both words match
SELECT id FROM t WHERE FTS_MATCH_WORD('database', content_text)
INTERSECT
SELECT id FROM t WHERE FTS_MATCH_WORD('vector', content_text);

-- NOT: matches the first word but not the second
SELECT id FROM t WHERE FTS_MATCH_WORD('database', content_text)
EXCEPT
SELECT id FROM t WHERE FTS_MATCH_WORD('obsolete', content_text);
```

To keep the table columns in the output, put the compound statement in a subquery:

```sql
SELECT * FROM t
WHERE id IN (
    SELECT id FROM t WHERE FTS_MATCH_WORD('database', content_text)
    INTERSECT
    SELECT id FROM t WHERE FTS_MATCH_WORD('vector', content_text)
);
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

## Select a parser for a scored column

A query is tokenized by the parser of the full-text index it runs on. To search one column with more than one parser, create a separate full-text index for each parser, then select the index with the `USE_INDEX` hint:

```sql
ALTER TABLE t ADD FULLTEXT INDEX idx_fts_ml (content_text) WITH PARSER MULTILINGUAL;
ALTER TABLE t ADD FULLTEXT INDEX idx_fts_ngram (content_text)
    WITH PARSER NGRAM(min_gram=3, max_gram=3);
```

```sql
-- Substring matching: the NGRAM index matches 'hand' inside 'HandleRequest'
SELECT /*+ USE_INDEX(t, idx_fts_ngram) */ * FROM t
WHERE FTS_MATCH_WORD('hand', content_text);

-- Complete token matching: the MULTILINGUAL index matches whole tokens only
SELECT /*+ USE_INDEX(t, idx_fts_ml) */ * FROM t
WHERE FTS_MATCH_WORD('database', content_text);
```

The `WITH PARSER` clause is accepted only in an index definition, as part of `FULLTEXT INDEX (col) WITH PARSER parser_name`. It is not supported inside `FTS_MATCH_WORD()`, and writing it there returns a syntax error.

An index provides only one parser per column, so separate indexes are the only way to search one column with both complete-token and substring matching. For the underlying restriction, see [Index limitations](/ai/reference/full-text-search-limitations.md#index-limitations).

> **Note:**
>
> Selecting the index selects the parser, which changes the result set. This makes parser selection part of query semantics, not performance tuning. Automatic index selection does not compare parsers, so when a scored column has indexes with different parsers, always specify the index with `USE_INDEX`. See [Automatic index selection](#automatic-index-selection).

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
| The indexes differ only in parser | The hint selects the parser, so the result set changes. This is the supported way to route a query between parsers. |
| The indexes use the same parser | A pure execution-path choice. The result set is unchanged. |
| The specified index does not exist | The hint is silently ignored, and the optimizer selects an index automatically. |
| The specified index does not cover a column that the query uses | TiDB reports the index and the column in the error, for example: `ERROR 1221 (HY000): full-text search index idx_fts_ng does not cover column test.docs.ext`. |

### IGNORE_INDEX: exclude an index

```sql
SELECT /*+ IGNORE_INDEX(t, idx_fts_ngram) */ *
FROM t WHERE FTS_MATCH_WORD('handle', content_text);
```

If `IGNORE_INDEX` excludes every full-text index that could serve the query, TiDB returns an error instead of scanning the table:

```
ERROR 1221 (HY000): full text search can only be used with a matching current TiFlash full-text index path
```

### Automatic index selection

Without hints, the optimizer selects a full-text index by the following priorities:

| Priority | Rule |
| :-- | :-- |
| 1 | Column coverage: prefer the index whose scored columns overlap most with the columns in the query. |
| 2 | Filter column coverage: prefer the index that matches more filter conditions in the `WHERE` clause. |
| 3 | Index size: prefer the smaller index to reduce scan cost. |

These priorities do not compare parsers. When one column has full-text indexes with different parsers, the automatically selected index determines the matching behavior of the query without any warning, so specify the index with `USE_INDEX`.

A query that uses `FTS_MATCH_WORD()` always runs on a full-text index. If no full-text index covers the queried columns, TiDB returns an error rather than falling back to a table scan or a regular index scan.

## Supported query patterns

- Single-table queries with filter conditions, aggregation, ordering, and pagination:

    ```sql
    SELECT category, COUNT(*) FROM t
    WHERE FTS_MATCH_WORD('query', content_text) GROUP BY category;

    SELECT * FROM t WHERE FTS_MATCH_WORD('query', content_text)
    ORDER BY FTS_MATCH_WORD('query', content_text) DESC LIMIT 10;
    ```

    Ordering by `FTS_MATCH_WORD()` requires a `LIMIT` clause. Without one, TiDB reports:

    ```
    ERROR 1221 (HY000): 'FTS_MATCH_WORD()' in ORDER BY without a LIMIT clause is not supported, try specify a very large LIMIT as a workaround
    ```

    To return the complete ranking in a single statement, specify a large `LIMIT` value. Ordering by a regular column needs no `LIMIT`.

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
