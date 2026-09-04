---
title: Full-Text Search Index
summary: Learn how to create and manage full-text indexes in TiDB, including syntax modes, column attributes, parsers, and DDL restrictions.
aliases: ['/tidb/stable/full-text-search-index/','/tidbcloud/full-text-search-index/']
---

# Full-Text Search Index

This document describes how to create and manage full-text indexes in TiDB, including the two index definition syntaxes, column attributes, parsers, multiple indexes on one table, and DDL restrictions on indexed columns and tables.

To run full-text queries against a full-text index, see [Full-Text Search Functions](/ai/reference/full-text-search-functions.md).

## Restrictions

Full-text search is still in the early stages, and we are continuously rolling it out to more customers. Currently, full-text search is only available on {{{ .starter }}} in the following regions:

- AWS: `Oregon (us-west-2)`, `N. Virginia (us-east-1)`, `Tokyo (ap-northeast-1)`, `Frankfurt (eu-central-1)`, and `Singapore (ap-southeast-1)`

## Create a full-text index

You can create a full-text index on a new table with `CREATE TABLE`, or add one to an existing table with `ALTER TABLE`. TiDB supports two definition syntaxes:

- [Syntax sugar mode](#syntax-sugar-mode): `(col) WITH PARSER parser_name`. A simple form for single-purpose indexes.
- [Column-property mode](#column-property-mode): `col WITH (attribute1, attribute2(param=value))`. Configures tokenizers and filter attributes per column.

The two modes are mutually exclusive within one index definition. Mixing them in the same `FULLTEXT INDEX` definition returns an error.

### Syntax sugar mode

```sql
ALTER TABLE t ADD FULLTEXT INDEX idx_fts (content_text) WITH PARSER MULTILINGUAL;
```

| Clause | Description |
| :-- | :-- |
| `(content_text)` | The scored column. It participates in the BM25 inverted index and relevance scoring. |
| `WITH PARSER MULTILINGUAL` | The tokenizer (parser) used to tokenize text for indexing and querying. |

Accepted parsers in the `WITH PARSER <parser_name>` clause:

- `STANDARD`: fast, works for English content, splitting words by spaces and punctuation. All text is lowercased for indexing and search (case-insensitive matching).
- `MULTILINGUAL`: supports multiple languages, including English, Chinese, Japanese, and Korean. Case-insensitive for both indexing and querying.
- `NGRAM`: a character-level n-gram tokenizer that supports substring matching. See [The NGRAM parser](#the-ngram-parser) for parameters.

```sql
ALTER TABLE t ADD FULLTEXT INDEX idx_fts_ngram (content_text)
    WITH PARSER NGRAM(min_gram=3, max_gram=3);
```

Syntax sugar mode is equivalent to column-property mode with a single parser attribute: `(col) WITH PARSER MULTILINGUAL` equals `col WITH (multilingual)`. Syntax sugar mode does not support filter columns. To define filter columns, use column-property mode.

> **Note:**
>
> In syntax sugar mode, specifying an index name is optional for the `MULTILINGUAL` parser. If you use the `NGRAM` parser or column-property mode, you must specify an index name explicitly. See [Index naming](#index-naming).

> **Note:**
>
> The `ADD_COLUMNAR_REPLICA_ON_DEMAND` clause is optional. When specified, TiDB creates a TiFlash replica for the table on demand. If you omit it, make sure that a TiFlash replica is already created for the table before you use full-text search.

### Column-property mode

In column-property mode, each column declares one or more attributes in a `WITH (...)` clause:

```sql
ALTER TABLE t ADD FULLTEXT INDEX idx_fts (
    content_text WITH (multilingual, ngram(min_gram=3, max_gram=3)),
    path         WITH (exact, path_hierarchy),
    name         WITH (exact),
    ext          WITH (exact)
);
```

Attributes fall into two categories:

- **Parser attributes**: `multilingual` and `ngram`. Columns with parser attributes are scored columns that participate in BM25 scoring.
- **Filter attributes**: `exact` and `path_hierarchy`. Columns with filter attributes are filter columns. Filter conditions on these columns are evaluated during the full-text index scan, without accessing the table rows. See [Filter attributes](#filter-attributes).

Rules for column attributes:

- A column can have multiple attributes, separated by commas inside `WITH (...)`. For example, `content_text WITH (multilingual, ngram(...))` builds two tokenizer structures for the same column, and `path WITH (exact, path_hierarchy)` makes the column support both equality filters and path prefix filters.
- The same type of parser can appear only once per column. You cannot define two parsers of the same type with different parameters on one column.
- Parser attributes and filter attributes cannot coexist on the same column. A column is either a scored column or a filter column, not both.
- Attribute parameters have default values. You can omit any parameter to use its default. See [Column attribute reference](#column-attribute-reference).
- Filter attribute columns inherit the collation of the corresponding TiDB column. Case sensitivity of filter matching is determined by the column collation. For example, with `utf8mb4_bin` filters are case-sensitive; with `utf8mb4_general_ci` they are case-insensitive.

#### Column attribute reference

| Attribute | Parameters | Default values | Description |
| :-- | :-- | :-- | :-- |
| `multilingual` | None | - | Language-aware tokenizer that matches complete tokens. Case-insensitive. |
| `ngram` | `min_gram`, `max_gram`, `granularity`, `lower_case` | `min_gram=3`, `max_gram=3`, `granularity='word'`, `lower_case=true` | Character-level n-gram tokenizer that supports prefix, infix, and suffix substring matching. See [The NGRAM parser](#the-ngram-parser). |
| `exact` | None | - | Exact-value matching using inverted posting lists. Supports `=` and `IN`. Used for tenant IDs, status, tags, and other low-cardinality filters. |
| `path_hierarchy` | `delimiter` | `delimiter='/'` | Hierarchical prefix matching for path-like values. Supports `col LIKE '/src/%'` and `col UNDER '/src/'`. The prefix must align with a delimiter boundary. See [path_hierarchy prefix alignment](#path_hierarchy-prefix-alignment). |

To customize the delimiter of `path_hierarchy`:

```sql
ALTER TABLE t ADD FULLTEXT INDEX idx_fts (
    content_text WITH (multilingual),
    path         WITH (exact, path_hierarchy(delimiter='$'))
);
```

## The NGRAM parser

The `NGRAM` parser builds character-level n-grams so that queries can match substrings. For example, searching `handle` matches documents containing `HandleRequest`, `RequestHandler`, or `handle_error`, which complete-token parsers such as `MULTILINGUAL` cannot match.

| Parameter | Type | Valid values | Default | Description |
| :-- | :-- | :-- | :-- | :-- |
| `min_gram` | INTEGER | [2, `max_gram`] | `3` | The minimum n-gram length. |
| `max_gram` | INTEGER | [`min_gram`, 5] | `3` | The maximum n-gram length. |
| `granularity` | STRING | `'word'` or `'char'` | `'word'` | Controls how n-grams are generated. See below. |
| `lower_case` | BOOLEAN | `true` or `false` | `true` | Whether text is lowercased at indexing and query time. `true` means case-insensitive matching; `false` preserves the original case. |

The `granularity` parameter controls n-gram generation:

| granularity | Behavior | Output for `hello world` (`min_gram=max_gram=3`) |
| :-- | :-- | :-- |
| `word` (default) | Tokenizes the text into words first, then applies a character sliding window inside each word. Avoids meaningless n-grams crossing word boundaries. | `hel`, `ell`, `llo`, `wor`, `orl`, `rld` |
| `char` | Applies a character sliding window over the entire text, ignoring word or space boundaries. Suitable for languages without space-separated words, or for matching across symbols. | `hel`, `ell`, `llo`, `lo_`, `o_w`, `_wo`, `wor`, `orl`, `rld` |

Examples:

```sql
-- Defaults: 3-gram, word granularity, case-insensitive
WITH PARSER NGRAM(min_gram=3, max_gram=3)

-- Character-level sliding window (includes spaces and symbols)
WITH PARSER NGRAM(min_gram=3, max_gram=3, granularity='char')

-- Case-sensitive matching
WITH PARSER NGRAM(min_gram=3, max_gram=3, lower_case=false)

-- All parameters can be omitted to use defaults
WITH PARSER NGRAM
```

### MULTILINGUAL versus NGRAM

| Aspect | MULTILINGUAL | NGRAM |
| :-- | :-- | :-- |
| Tokenization | Language-aware segmentation | Character-level sliding window |
| Matching scope | Complete tokens | Prefix / infix / suffix substrings |
| Recall | Precise | Loose |
| Index size | Moderate | Larger |
| Suitable scenarios | Complete keyword search | Partial-recall and code snippet search |

You can build both a `MULTILINGUAL` index and an `NGRAM` index on the same column and route queries to either one at query time. See [Multiple indexes on one table](#multiple-indexes-on-one-table).

## Multi-column full-text indexes

A full-text index can contain multiple scored columns. BM25 scores are fused at the index level in a single scan, which replaces the pattern of scanning one index per column and merging results with `UNION ALL` in the application.

```sql
-- Syntax sugar mode: all columns share the same parser
ALTER TABLE t ADD FULLTEXT INDEX idx_fts_multi
    (content_text, description) WITH PARSER MULTILINGUAL;

-- Column-property mode: scored columns and filter columns in one index
ALTER TABLE t ADD FULLTEXT INDEX idx_fts_multi (
    content_text WITH (multilingual),
    description  WITH (multilingual),
    path         WITH (exact, path_hierarchy),
    name         WITH (exact)
);
```

To search across multiple scored columns, list them in the `FTS_MATCH_WORD()` call. For details, see [Full-Text Search Functions](/ai/reference/full-text-search-functions.md).

## Multiple indexes on one table

A table can have multiple full-text indexes. The same column can participate in multiple full-text indexes, each with a different parser.

```sql
ALTER TABLE t ADD FULLTEXT INDEX idx_fts_ml
    (content_text) WITH PARSER MULTILINGUAL;

ALTER TABLE t ADD FULLTEXT INDEX idx_fts_ng
    (content_text) WITH PARSER NGRAM(min_gram=3, max_gram=3);
```

At query time, you can select the index with the `USE_INDEX` or `IGNORE_INDEX` optimizer hint, or let the optimizer choose automatically. See [Choose a full-text index at query time](/ai/reference/full-text-search-functions.md#choose-a-full-text-index-at-query-time).

### Index naming

If you do not specify an index name, TiDB generates one automatically:

1. By default, TiDB uses the name of the first indexed column as the index name.
2. If that name already exists, TiDB tries the `_2`, `_3`, and subsequent suffixes until the name is unique.
3. If the first indexed column name is the reserved word `PRIMARY`, TiDB starts from `primary_2`.

The generated name can be referenced in the `USE_INDEX` hint.

## View and drop full-text indexes

`SHOW CREATE TABLE` outputs the full index definition, including the parser and per-column attributes:

```sql
SHOW CREATE TABLE t;
```

```
CREATE TABLE `t` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content_text` text DEFAULT NULL,
  `description` text DEFAULT NULL,
  `path` varchar(512) DEFAULT NULL,
  `name` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`),
  FULLTEXT KEY `idx_fts_multi` (`content_text` WITH (multilingual), `description` WITH (multilingual), `path` WITH (exact, path_hierarchy), `name` WITH (exact))
);
```

In column-property mode, every column's parser and filter attributes are shown in the `WITH (...)` clause after the column name.

`SHOW INDEX` reports `FULLTEXT` in the `Index_type` column, compatible with MySQL:

```sql
SHOW INDEX FROM t WHERE Key_name = 'idx_fts';
```

You can also query `INFORMATION_SCHEMA`:

- `INFORMATION_SCHEMA.STATISTICS`: `INDEX_TYPE` returns `FULLTEXT`.
- `INFORMATION_SCHEMA.TIDB_INDEXES`: `index_type` returns `FULLTEXT`.
- `INFORMATION_SCHEMA.TIDB_INDEX_USAGE`: reports access statistics for full-text indexes.

To drop a full-text index:

```sql
ALTER TABLE t DROP INDEX idx_fts;
```

## DDL restrictions

Columns that participate in a full-text index and tables that contain a full-text index are subject to the following DDL restrictions.

### Restrictions on indexed columns

| DDL operation | Allowed | Notes |
| :-- | :-- | :-- |
| `DROP COLUMN` | No | Drop the full-text index first, then drop the column. |
| `RENAME COLUMN` | No | Drop the full-text index first, rename the column, and then re-create the index. |
| `MODIFY COLUMN` (narrowing) | No | For example, `INT` to `SMALLINT`, or `VARCHAR(40)` to `VARCHAR(20)`. |
| `MODIFY COLUMN` (widening) | Yes | For example, `INT` to `BIGINT`, or `VARCHAR(20)` to `VARCHAR(40)`. |
| `MODIFY COLUMN` (incompatible type) | No | For example, `TEXT` to `INT`. |

### Restrictions on tables with full-text indexes

| DDL operation | Allowed | Notes |
| :-- | :-- | :-- |
| `TRUNCATE TABLE` | No | Drop the full-text index first, then truncate the table. |
| `DROP TABLE` | No | Drop the full-text index first, then drop the table. |
| `RENAME TABLE` | No | Drop the full-text index first, rename the table, and then re-create the index. |

For the full list of functional limitations, see [Full-Text Search Limitations](/ai/reference/full-text-search-limitations.md).

## See also

- [Full-Text Search with SQL](/ai/guides/vector-search-full-text-search-sql.md)
- [Full-Text Search Functions](/ai/reference/full-text-search-functions.md)
- [Full-Text Search Limitations](/ai/reference/full-text-search-limitations.md)
