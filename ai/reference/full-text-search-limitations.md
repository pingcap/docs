---
title: Full-Text Search Limitations
summary: Learn the limitations of full-text search in TiDB, covering index definition, filter pushdown, query behavior, DML, DDL, and observability.
---

# Full-Text Search Limitations

This document describes the known limitations of full-text search in TiDB.

> **Note:**
>
> Full-text search is still in the early stages, and we are continuously rolling it out to more customers. Currently, full-text search is **available only on {{{ .starter }}}** in [select regions](/ai/reference/full-text-search-index.md#prerequisites).

## Index limitations

- In one full-text index definition, the syntax sugar mode `(col) WITH PARSER parser_name` and the column-property mode `col WITH (...)` are mutually exclusive. Mixing both modes in the same index definition returns an error.
- On a single column, the same type of parser can appear only once. You cannot define multiple parsers of the same type with different parameters on one column.
- Parser attributes (`multilingual`, `ngram`) and filter attributes (`exact`, `path_hierarchy`) cannot coexist on the same column. A column is either a scored column or a filter column.
- Syntax sugar mode does not support filter columns. To define filter columns, use column-property mode.
- Declaring more than one parser attribute on a single column of the same index, such as `content_text WITH (multilingual, ngram(...))`, succeeds but does not give you both matching behaviors: a query runs on one of the parsers and cannot select the other. Create one full-text index per parser instead.
- A TiFlash replica and the full-text indexes on it are built asynchronously. A successful `CREATE TABLE` or `ALTER TABLE` statement does not mean the index is queryable, and a query that runs before the index is ready returns no rows rather than an error. Before you rely on the result, confirm that the replica is available and run a query whose match you know:

    ```sql
    SELECT TABLE_NAME, REPLICA_COUNT, AVAILABLE
    FROM INFORMATION_SCHEMA.TIFLASH_REPLICA
    WHERE TABLE_SCHEMA = 'your_database' AND TABLE_NAME = 'your_table';

    SELECT COUNT(*) FROM your_table WHERE FTS_MATCH_WORD('known_term', content_text);
    ```

    `AVAILABLE = 0` means the replica is still being built. When a query returns no rows, rule out the causes in [Query limitations](#query-limitations) before you conclude that data is missing.

## Filter pushdown limitations

- The `exact` attribute supports equality matching (`=` and `IN`) in the index scan. Range predicates (`<`, `>`, `BETWEEN`, and similar) on `exact` columns are not pushed down into the index scan. They are evaluated as residual predicates after row lookup, so query results remain correct but the filtering happens outside the index.
- `LIKE` conditions on `exact` columns are not pushed down into the index scan and are evaluated as residual predicates. `LIKE` prefix matching is pushed down only on columns with the `path_hierarchy` attribute.
- For `path_hierarchy` columns, a pushed-down prefix must align with a delimiter boundary. For example, with the default delimiter `/`, `path LIKE '/src/%'` is pushed down, but `path LIKE '/src/par%'` is not, because the prefix ends inside a directory name. Such conditions are evaluated as residual predicates after row lookup.
- Filter conditions that cannot match any filter column of the selected index are evaluated as residual predicates after row lookup.

## Query limitations

- In the `WHERE` clause, multiple `FTS_MATCH_WORD()` calls can be combined only with `OR`. Combining them with `AND` at the top level returns `ERROR 1221 (HY000): Currently 'FTS_MATCH_WORD()' must be used alone`, even when the calls use different words or different columns. To express AND or NOT semantics, use `INTERSECT` or `EXCEPT`. See [Multi-word query semantics](/ai/reference/full-text-search-functions-tidb.md#multi-word-query-semantics).

- `ORDER BY` with `FTS_MATCH_WORD()` requires a `LIMIT` clause, and is supported only when the `WHERE` clause contains a single `FTS_MATCH_WORD()` call:

    ```sql
    -- Not supported: ORDER BY a match function without a LIMIT clause
    SELECT * FROM t
    WHERE FTS_MATCH_WORD('database', content_text)
    ORDER BY FTS_MATCH_WORD('database', content_text) DESC;

    -- Not supported: multiple match functions in WHERE, ordered by one of them
    SELECT * FROM t
    WHERE FTS_MATCH_WORD('database', content_text)
       OR FTS_MATCH_WORD('vector', content_text)
    ORDER BY FTS_MATCH_WORD('database', content_text) DESC
    LIMIT 10;
    ```

    To rank the complete result set in one statement, specify a large `LIMIT` value. Ordering by a regular column requires no `LIMIT`.

- `FTS_MATCH_WORD()` cannot appear in `GROUP BY` or `HAVING` clauses.
- `FTS_MATCH_WORD()` cannot be nested inside another function or expression. Comparing its score in the same clause, as in `WHERE FTS_MATCH_WORD('database', content_text) > 0.5`, returns `ERROR 1221 (HY000): Currently 'FTS_MATCH_WORD()' must be used alone`. To filter by score, compute it in a derived table and filter in the outer query:

    ```sql
    SELECT * FROM (
        SELECT id, FTS_MATCH_WORD('database', content_text) AS score
        FROM t
        WHERE FTS_MATCH_WORD('database', content_text)
        ORDER BY score DESC
        LIMIT 100
    ) s
    WHERE s.score > 0.5;
    ```

- When `FTS_MATCH_WORD()` appears in the `SELECT` list, the `WHERE` clause must contain the same call, and `ORDER BY` must either repeat that call or reference its alias:

    ```sql
    SELECT id, FTS_MATCH_WORD('database', content_text) AS score
    FROM t
    WHERE FTS_MATCH_WORD('database', content_text)
    ORDER BY score DESC
    LIMIT 10;
    ```

    Otherwise TiDB returns `ERROR 1221 (HY000): 'FTS_MATCH_WORD()' in SELECT requires a matching 'FTS_MATCH_WORD()' in WHERE.`

- Applying `NOT` directly to `FTS_MATCH_WORD()` in the `WHERE` clause returns `ERROR 1221 (HY000): scored pure-negative FTS match expression is not supported`. To exclude matching rows, use `EXCEPT`, or place `NOT` inside an `OR` branch alongside a positive term.
- Calling `FTS_MATCH_WORD()` on a column that carries the `exact` attribute returns `ERROR 1221 (HY000): FTS_MATCH_WORD does not support fields using the EXACT parser; use = or IN predicates instead`. Filter columns take `=` and `IN` predicates.
- A query term shorter than the `min_gram` of an NGRAM index matches no rows, because the index holds no shorter tokens. Wildcards such as `%` have no special meaning inside `FTS_MATCH_WORD()`; such a query returns no rows instead of an error.
- `EXCEPT ALL` and `INTERSECT ALL` are not supported. Use `EXCEPT` and `INTERSECT`, which eliminate duplicate rows:

    ```
    ERROR 1105 (HY000): TiDB do not support except all
    ```

- The default `mysql` client strips optimizer hints such as `USE_INDEX`, which silently changes the index and therefore the parser a query uses. Run the client with `-c` or `--comments` when you test hinted full-text queries, and check `SHOW WARNINGS` or the `EXPLAIN` output to confirm that a hint takes effect.
- Exact phrase matching, where all query tokens must appear consecutively and in the specified order, is not supported yet.
- Only `INNER JOIN` is supported with full-text search. Outer joins (`LEFT`, `RIGHT`, and `FULL`) and comma-separated table lists, which form an implicit `CROSS JOIN`, are not supported yet.
- In compound statements (`UNION`, `UNION ALL`, `EXCEPT`, and `INTERSECT`), each branch matches its full-text index independently. Branches do not share a single index scan, and the outer `ORDER BY` and `LIMIT` are not pushed into the full-text scans.
- A query that uses `FTS_MATCH_WORD()` must match a full-text index that covers the queried columns. When no such index exists, or when `IGNORE_INDEX` excludes all of them, TiDB returns an error instead of falling back to a table scan:

    ```
    ERROR 1221 (HY000): full text search can only be used with a matching current TiFlash full-text index path
    ```

    When a `USE_INDEX` hint names an index that does not cover a column used by the query, TiDB reports the index and the column in the error, for example: `ERROR 1221 (HY000): full-text search index idx_fts_ng does not cover column test.docs.ext`.

## Observability limitations

- Full-text indexes do not report usage or size statistics in this version. TiDB does not record full-text index accesses in `INFORMATION_SCHEMA.TIDB_INDEX_USAGE`, provides no full-text statistics tables, and exposes no full-text query time metrics. Use `EXPLAIN` together with the slow query log to investigate a query.

## DML limitations

- Full-text search is supported in query statements. To change the rows that a full-text search matches, first retrieve the IDs, then run the DML statement with that list:

    ```sql
    -- Step 1. Retrieve the matching IDs
    SELECT id FROM t WHERE FTS_MATCH_WORD('obsolete', content_text);

    -- Step 2. Run the DML statement with the IDs from the previous result
    DELETE FROM t WHERE id IN (5, 8, 11);
    ```

## DDL limitations

See [DDL restrictions](/ai/reference/full-text-search-index.md#ddl-restrictions) in [Full-Text Search Index](/ai/reference/full-text-search-index.md).

## Feedback

We value your feedback and are always here to help:

- Ask the community on [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) or [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs).
- [Submit a support ticket for TiDB Cloud](https://tidb.support.pingcap.com/servicedesk/customer/portals)
