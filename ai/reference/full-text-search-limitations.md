---
title: Full-Text Search Limitations
summary: Learn the limitations of full-text search in TiDB, including index definition, filter pushdown, query syntax, and DDL restrictions.
aliases: ['/tidb/stable/full-text-search-limitations/','/tidbcloud/full-text-search-limitations/']
---

# Full-Text Search Limitations

This document describes the known limitations of full-text search in TiDB.

> **Note:**
>
> Full-text search is still in the early stages, and we are continuously rolling it out to more customers. Currently, full-text search is only available on {{{ .starter }}} in selected regions. See [Restrictions](/ai/reference/full-text-search-index.md#restrictions) for the region list.

## Index limitations

- In one full-text index definition, the syntax sugar mode `(col) WITH PARSER parser_name` and the column-property mode `col WITH (...)` are mutually exclusive. Mixing both modes in the same index definition returns an error.
- On a single column, the same type of parser can appear only once. You cannot define multiple parsers of the same type with different parameters on one column.
- Parser attributes (`multilingual`, `ngram`) and filter attributes (`exact`, `path_hierarchy`) cannot coexist on the same column. A column is either a scored column or a filter column.
- Syntax sugar mode does not support filter columns. To define filter columns, use column-property mode.

## Filter pushdown limitations

- The `exact` attribute supports equality matching (`=` and `IN`) in the index scan. Range predicates (`<`, `>`, `BETWEEN`, and similar) on `exact` columns are not pushed down into the index scan. They are evaluated as residual predicates after row lookup, so query results remain correct but the filtering happens outside the index.
- `LIKE` conditions on `exact` columns are not pushed down into the index scan and are evaluated as residual predicates. `LIKE` prefix matching is pushed down only on columns with the `path_hierarchy` attribute.
- For `path_hierarchy` columns, a pushed-down prefix must align with a delimiter boundary. For example, with the default delimiter `/`, `path LIKE '/src/%'` is pushed down, but `path LIKE '/src/par%'` is not, because the prefix ends inside a directory name. Such conditions are evaluated as residual predicates after row lookup.
- Filter conditions that cannot match any filter column of the selected index are evaluated as residual predicates after row lookup.

## Query limitations

- `ORDER BY` with a match function is only supported when the `WHERE` clause contains a single match function call. When the `WHERE` clause contains multiple match functions (for example, multi-word AND or OR combinations), ordering by a match function in the same query is not supported.

    ```sql
    -- Not supported: multiple match functions in WHERE and ORDER BY on a match function
    SELECT * FROM t
    WHERE FTS_MATCH_WORD('database', col) AND FTS_MATCH_WORD('vector', col)
    ORDER BY FTS_MATCH_WORD('database', col) DESC;
    ```

- `FTS_MATCH_WORD()` cannot appear in `GROUP BY` or `HAVING` clauses.
- Exact phrase matching, where all query tokens must appear consecutively and in the specified order, is not supported yet.
- Only `INNER JOIN` is supported with full-text search. Outer joins (`LEFT`, `RIGHT`, and `FULL`) are not supported yet.
- In compound statements (`UNION`, `UNION ALL`, `EXCEPT`, and `INTERSECT`), each branch matches its full-text index independently. Branches do not share a single index scan, and the outer `ORDER BY` and `LIMIT` are not pushed into the full-text scans.

## DDL limitations

See [DDL restrictions](/ai/reference/full-text-search-index.md#ddl-restrictions) in [Full-Text Search Index](/ai/reference/full-text-search-index.md).

## Feedback

We value your feedback and are always here to help:

- Ask the community on [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) or [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs).
- [Submit a support ticket for TiDB Cloud](https://tidb.support.pingcap.com/servicedesk/customer/portals)
