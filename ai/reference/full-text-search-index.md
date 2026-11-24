---
title: Full-Text Search Index
summary: Learn how to create and manage full-text indexes in TiDB, including syntax modes, column attributes, parsers, and DDL restrictions.
---

# Full-Text Search Index

This document describes how to create and manage full-text indexes in TiDB, including the two index definition syntaxes, column attributes, parsers, multiple indexes on one table, and DDL restrictions on indexed columns and tables.

To run full-text queries against a full-text index, see [Full-Text Search Functions](/ai/reference/full-text-search-functions-tidb.md).

## Prerequisites

Full-text search is still in the early stages, and we are continuously rolling it out to more customers. Currently, full-text search is **available only on {{{ .starter }}}** in the following regions:

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
> - In syntax sugar mode, specifying an index name is optional for the `MULTILINGUAL` parser. If you use the `NGRAM` parser or column-property mode, you must specify an index name explicitly. See [Index naming](#index-naming).
> - The `ADD_COLUMNAR_REPLICA_ON_DEMAND` clause is optional. When specified, TiDB creates a TiFlash replica for the table on demand. If you omit it, make sure that a TiFlash replica is already created for the table before you use full-text search.

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
- **Filter attributes**: `exact` and `path_hierarchy`. Columns with filter attributes are filter columns. Filter conditions on these columns are evaluated during the full-text index scan, without accessing the table rows.

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
| `path_hierarchy` | `delimiter` | `delimiter='/'` | Hierarchical prefix matching for path-like values. Supports `col LIKE '/src/%'` and `col UNDER '/src/'`. The prefix must align with a delimiter boundary.

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

To search across multiple scored columns, list them in the `FTS_MATCH_WORD()` call. For details, see [Full-Text Search Functions](/ai/reference/full-text-search-functions-tidb.md).

## Multiple indexes on one table

A table can have multiple full-text indexes. The same column can participate in multiple full-text indexes, each with a different parser.

```sql
ALTER TABLE t ADD FULLTEXT INDEX idx_fts_ml
    (content_text) WITH PARSER MULTILINGUAL;

ALTER TABLE t ADD FULLTEXT INDEX idx_fts_ng
    (content_text) WITH PARSER NGRAM(min_gram=3, max_gram=3);
```

At query time, you can select the index with the `USE_INDEX` or `IGNORE_INDEX` optimizer hint, or let the optimizer choose automatically. See [Choose a full-text index at query time](/ai/reference/full-text-search-functions-tidb.md#choose-a-full-text-index-at-query-time).

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

Columns that participate in a full-text index are subject to DDL restrictions. Common table-level operations on a table that contains a full-text index are not blocked, but creating and maintaining a full-text index has its own restrictions.

### Restrictions on indexed columns

Full-text indexes validate scored columns and filter columns in the same way, because both belong to the indexed column set. The two kinds of columns differ only in the column types that their parser or attribute accepts. See [Parser and column type compatibility](#parser-and-column-type-compatibility).

| DDL operation | Allowed | Notes |
| :-- | :-- | :-- |
| `DROP COLUMN` | No | TiDB rejects the statement when a full-text index covers the column, even if the index contains only that column. Drop the full-text index first, and then drop the column. You cannot combine `DROP INDEX` and `DROP COLUMN` in one `ALTER TABLE` statement, because TiDB validates every clause against the original schema. |
| `RENAME COLUMN` | Yes | TiDB updates the column name in the index automatically, and you do not need to rebuild the index. Renaming a column with `CHANGE COLUMN` while keeping the same type is also allowed. |
| `MODIFY COLUMN` or `CHANGE COLUMN` (no data rewrite) | Conditional | Allowed only when all four conditions in [Conditions for a type change](#conditions-for-a-type-change) are met. Typical examples are `VARCHAR(20)` to `VARCHAR(40)` and `INT` to `BIGINT`. |
| `MODIFY COLUMN` or `CHANGE COLUMN` (data rewrite required) | No | TiDB rejects changes such as reducing a length or a type range, `CHAR` to `VARCHAR`, `FLOAT` to `DOUBLE`, and conversions between signed and unsigned types. |
| `MODIFY COLUMN` or `CHANGE COLUMN` (type incompatible with the parser) | No | TiDB validates the new type against the parser that the column uses, even when the change does not rewrite data. For example, changing a column to `VARBINARY`, or to a `BINARY` collation, is rejected. |
| `ALTER COLUMN SET DEFAULT` and `ALTER COLUMN DROP DEFAULT` | Yes | No full-text index restriction applies. |
| Change the column collation | No | This is a general restriction for any indexed column and is not specific to full-text indexes. |
| Inline `FULLTEXT` column option in `MODIFY COLUMN` or `CHANGE COLUMN` | No | You cannot add a full-text index through a column definition. Use `ALTER TABLE ... ADD FULLTEXT INDEX` instead. |

#### Conditions for a type change

A `MODIFY COLUMN` or `CHANGE COLUMN` operation that does not rewrite data is allowed only when all of the following conditions are met:

1. TiDB supports the type conversion.
2. The conversion does not require rewriting the column data. This is the key criterion, and it replaces a simple widening-versus-narrowing rule.
3. The new type is still compatible with the parser that is bound to the column.
4. The conversion does not trigger other general DDL restrictions, such as a collation change, a generated column dependency, or a partition column constraint.

#### Common type changes

| Type change | Supported | Reason |
| :-- | :-- | :-- |
| `VARCHAR(20)` to `VARCHAR(40)` | Yes | Expands the length without rewriting data. The column remains a non-binary string. |
| `CHAR(20)` to `CHAR(40)` | Yes | Expands the length within the same non-binary `CHAR` type without rewriting data. |
| `INT` to `BIGINT` | Yes | Expands the integer range without rewriting data. |
| `INT UNSIGNED` to `BIGINT UNSIGNED` | Yes | Expands the integer range without changing signedness. |
| `INT` to `BIGINT UNSIGNED` | No | Changes signedness, which requires a data rewrite. |
| `CHAR(20)` to `VARCHAR(40)` | No | Requires a data rewrite. |
| `FLOAT` to `DOUBLE` | No | Requires a data rewrite. |
| `VARCHAR(20)` to `VARCHAR(40) BINARY` | No | The new type is not compatible with a full-text string parser. |
| `VARCHAR(20)` to `VARBINARY(40)` | No | The new type is not compatible with a full-text string parser. |
| `VARCHAR(40)` to `VARCHAR(20)` | No | Reduces the length, which requires a data rewrite. |
| `INT` to `SMALLINT` | No | Narrows the type, which requires a data rewrite. |
| `TEXT` to `INT` | No | Changes the type across categories, which requires a data rewrite. |

This table is not exhaustive. The four conditions in [Conditions for a type change](#conditions-for-a-type-change) are the authoritative criteria. When you modify any column of a multi-column full-text index, TiDB re-validates the whole column set of that index.

#### Parser and column type compatibility

| Parser or attribute | Allowed column types |
| :-- | :-- |
| `STANDARD`, `MULTILINGUAL`, `NGRAM`, and `path_hierarchy` | Non-binary string types only, which means a string type whose collation is not `binary`. |
| `exact` | Non-binary string types, or the following native types: `TINYINT`, `SMALLINT`, `MEDIUMINT`, `INT`, `BIGINT`, `BIT`, `YEAR`, `FLOAT`, `DOUBLE`, `DATE`, `DATETIME`, `TIMESTAMP`, `TIME`, and `ENUM`. `DECIMAL` is not supported. |

### Restrictions on tables with full-text indexes

TiDB applies no full-text-specific validation to the operations in the following table, and you do not need to drop the full-text index before you run them.

| DDL operation | Allowed | Notes |
| :-- | :-- | :-- |
| `TRUNCATE TABLE` | Yes | No full-text index validation applies. |
| `DROP TABLE` | Yes | TiDB removes the full-text index together with the table. |
| `RENAME TABLE` and `ALTER TABLE ... RENAME TO` | Yes | The full-text index moves with the table. |
| `ADD COLUMN` | Yes | TiDB does not add the new column to an existing full-text index automatically. |
| `ADD COLUMN` with an inline `FULLTEXT` column option | Yes, with a warning | TiDB ignores the column option and returns a warning that the table type does not support full-text indexes. Use `ALTER TABLE ... ADD FULLTEXT INDEX` instead. |
| `ALTER TABLE ... SET TIFLASH REPLICA 0` | Yes | TiDB does not reject the statement because a full-text index exists. |
| `DROP INDEX` for a full-text index | Yes | You can combine this clause with other `DROP INDEX` clauses in one `ALTER TABLE` statement. TiDB reclaims the index data on the storage side asynchronously. |

These operations are not the only table-level statements that affect a table with a full-text index. Full-text indexes do not support partitioned, temporary, or cached tables, so if you plan to convert a table that has a full-text index into one of these types, drop the index first and re-create it after the change.

### Restrictions on index creation and maintenance

The following restrictions apply when you create a full-text index or run maintenance statements. They are not table-level DDL blocks.

| Operation | Allowed | Notes |
| :-- | :-- | :-- |
| Create a full-text index on a partitioned, temporary, or cached table | No | TiDB validates this restriction in both `CREATE TABLE` and `ALTER TABLE ... ADD FULLTEXT INDEX`. |
| Combine `ADD FULLTEXT INDEX` with other `ALTER TABLE` clauses | No | Full-text indexes do not support merged schema changes. Run `ADD FULLTEXT INDEX` as a standalone statement. |
| `ALTER INDEX ... INVISIBLE` | No | You cannot set a full-text index to invisible. `ALTER INDEX ... VISIBLE` is allowed. |
| `ADMIN CLEANUP INDEX` | No | Full-text indexes do not support cleanup. |
| `ADMIN CHECK TABLE` and `ADMIN CHECK INDEX` | Skipped | Full-text indexes do not participate in consistency checks. TiDB skips them and does not return an error. |

For the full list of functional limitations, see [Full-Text Search Limitations](/ai/reference/full-text-search-limitations.md).

## See also

- [Full-Text Search with SQL](/ai/guides/vector-search-full-text-search-sql.md)
- [Full-Text Search Functions](/ai/reference/full-text-search-functions-tidb.md)
- [Full-Text Search Limitations](/ai/reference/full-text-search-limitations.md)
