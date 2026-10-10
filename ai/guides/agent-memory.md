---
title: Store AI Agent Memory in TiDB
summary: Learn how to store AI agent memory in one TiDB table with SQL, using vector search, transactions, per-user recall, and automatic expiry.
---

# Store AI Agent Memory in TiDB

An AI agent that remembers users across sessions needs four things from its memory store: find memories by meaning, narrow them by user and type, replace an outdated memory without leaving a half-written state, and forget memories when they expire or a user asks. In TiDB, one table and plain SQL cover all four, because vector search, secondary indexes, transactions, and row expiry live in the same database.

This document walks through that table step by step. For a complete chat application built on the same idea with the `pytidb` Python SDK, see [AI Agent Memory Example](/ai/guides/memory-with-pytidb.md).

## Prerequisites

- A {{{ .starter }}} instance. You can create a free {{{ .starter }}} instance on [TiDB Cloud](https://tidbcloud.com/free-trial).
- A MySQL client connected to the instance. In the [TiDB Cloud console](https://tidbcloud.com/), open your instance and click **Connect** for the connection parameters.

The examples use 3-dimensional vectors so that the output is easy to read. In your application, set the vector dimension to the output size of your embedding model, for example `VECTOR(1536)`, and generate each embedding with that model.

## Step 1. Create the memory table

Select a database first. This example uses the `test` database that every {{{ .starter }}} instance has:

```sql
USE test;

CREATE TABLE agent_memory (
    id          BIGINT PRIMARY KEY AUTO_RANDOM,
    user_id     VARCHAR(64) NOT NULL,
    kind        ENUM('fact', 'preference', 'episode') NOT NULL,
    content     TEXT NOT NULL,
    embedding   VECTOR(3) NOT NULL,
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    KEY idx_user (user_id, is_active),
    VECTOR INDEX idx_embedding ((VEC_COSINE_DISTANCE(embedding)))
) TTL = `created_at` + INTERVAL 90 DAY TTL_ENABLE = 'ON';
```

Each part of the table serves one memory operation:

- `embedding` and the vector index `idx_embedding` let you find memories by meaning.
- `user_id` and `kind` let you narrow memories to one user and one type. The secondary index `idx_user` on `(user_id, is_active)` makes reading one user's active memories fast.
- `is_active` lets you retire an outdated memory without deleting it.
- The `TTL` clause makes TiDB delete memories automatically 90 days after `created_at`. For details, see [TTL (Time to Live)](/time-to-live.md).

## Step 2. Write memories

```sql
INSERT INTO agent_memory (user_id, kind, content, embedding) VALUES
  ('alice', 'fact',       'Alice is a data engineer at a fintech company.',    '[0.9, 0.1, 0.2]'),
  ('alice', 'preference', 'Alice prefers answers in Python.',                  '[0.2, 0.9, 0.1]'),
  ('alice', 'episode',    'Alice asked how to tune a slow join on 2026-10-01.', '[0.5, 0.4, 0.7]'),
  ('bob',   'fact',       'Bob runs a small online bookstore.',                '[0.8, 0.2, 0.3]'),
  ('bob',   'preference', 'Bob prefers short answers.',                        '[0.1, 0.8, 0.3]');
```

## Step 3. Replace an outdated memory in a transaction

When a user changes a preference, retire the old memory and write the new one in a single transaction. Either both changes take effect or neither does, so the agent never sees two conflicting active preferences or none at all.

```sql
BEGIN;
UPDATE agent_memory SET is_active = FALSE
 WHERE user_id = 'alice' AND kind = 'preference' AND is_active;
INSERT INTO agent_memory (user_id, kind, content, embedding)
VALUES ('alice', 'preference', 'Alice now prefers answers in Go.', '[0.25, 0.85, 0.15]');
COMMIT;
```

Check the result:

```sql
SELECT content, is_active FROM agent_memory
WHERE user_id = 'alice' AND kind = 'preference'
ORDER BY is_active DESC;
```

```
+----------------------------------+-----------+
| content                          | is_active |
+----------------------------------+-----------+
| Alice now prefers answers in Go. |         1 |
| Alice prefers answers in Python. |         0 |
+----------------------------------+-----------+
```

If a statement in the transaction fails, for example because a value does not fit its column, run `ROLLBACK` instead of `COMMIT`. A failed statement does not end the transaction: the statements that succeeded are still pending, and `COMMIT` would save them, for example leaving the user with the old preference retired and no new one. After `ROLLBACK`, the memory stays as it was.

## Step 4. Recall memories for one user

Most agent requests need the memories of the current user only. Filter by user first, then rank by distance to the embedding of the current request:

```sql
SELECT kind, content, VEC_COSINE_DISTANCE(embedding, '[0.2, 0.9, 0.2]') AS distance
FROM agent_memory
WHERE user_id = 'alice' AND is_active
ORDER BY distance
LIMIT 3;
```

```
+------------+----------------------------------------------------+-----------------------+
| kind       | content                                            | distance              |
+------------+----------------------------------------------------+-----------------------+
| preference | Alice now prefers answers in Go.                   | 0.0032403313698232683 |
| episode    | Alice asked how to tune a slow join on 2026-10-01. |    0.3295984359391211 |
| fact       | Alice is a data engineer at a fintech company.     |     0.645662235088144 |
+------------+----------------------------------------------------+-----------------------+
```

This query does not use the vector index, because the `WHERE` filter is applied before the nearest-neighbor search. It uses the secondary index `idx_user` to read only this user's active memories and computes the exact distance for each one. The result is exact, and the cost depends on how many memories one user has, not on the size of the table. This is usually the right pattern for per-user agent memory.

## Step 5. Recall memories across all users

Some features, such as finding similar past conversations from any user, search the whole table. Use the vector index to find the nearest memories first, and then filter. Fetch more candidates than you need, because the filter can remove some of them:

```sql
SELECT * FROM (
  SELECT user_id, kind, content, is_active,
         VEC_COSINE_DISTANCE(embedding, '[0.85, 0.15, 0.25]') AS distance
  FROM agent_memory
  ORDER BY distance
  LIMIT 20
) t
WHERE is_active
ORDER BY distance
LIMIT 3;
```

```
+---------+---------+----------------------------------------------------+-----------+-----------------------+
| user_id | kind    | content                                            | is_active | distance              |
+---------+---------+----------------------------------------------------+-----------+-----------------------+
| alice   | fact    | Alice is a data engineer at a fintech company.     |         1 | 0.0040039807124229165 |
| bob     | fact    | Bob runs a small online bookstore.                 |         1 | 0.0044730676562374505 |
| alice   | episode | Alice asked how to tune a slow join on 2026-10-01. |         1 |     0.225803083881864 |
+---------+---------+----------------------------------------------------+-----------+-----------------------+
```

Run `EXPLAIN` on this query to confirm it uses the vector index: the `operator info` column shows `annIndex:COSINE(embedding..[0.85,0.15,0.25], limit:20)`. On a table with only a few rows, the optimizer might read from TiKV instead and skip the vector index; with a realistic number of memories, the query uses it. For how the placement of a filter affects the vector index, see [Use the vector index with filters](/ai/reference/vector-search-index.md#use-the-vector-index-with-filters).

## Step 6. Forget memories

To delete everything the agent remembers about a user, for example when the user asks to be forgotten, delete by `user_id`:

```sql
DELETE FROM agent_memory WHERE user_id = 'bob';
```

Memories older than 90 days are deleted automatically by the `TTL` clause from Step 1. TiDB removes expired rows in a background job that runs every hour by default, so a memory can remain for a while after it expires. You can change the interval with the `TTL_JOB_INTERVAL` table option. To exclude expired memories from recall at once, filter on `created_at`. In the Step 4 query, add `AND created_at > NOW() - INTERVAL 90 DAY` to the `WHERE` clause. In the Step 5 query, select `created_at` in the subquery and filter on it in the outer `WHERE` clause, next to `is_active`:

```sql
SELECT * FROM (
  SELECT user_id, kind, content, is_active, created_at,
         VEC_COSINE_DISTANCE(embedding, '[0.85, 0.15, 0.25]') AS distance
  FROM agent_memory
  ORDER BY distance
  LIMIT 20
) t
WHERE is_active AND created_at > NOW() - INTERVAL 90 DAY
ORDER BY distance
LIMIT 3;
```

Do not put the `created_at` filter inside the subquery. A filter inside the subquery is applied before the nearest-neighbor search, so the vector index is not used.

> **Note:**
>
> After a `DELETE`, the deleted rows can still be read for a short time with a [stale read](/stale-read.md) such as `SELECT ... AS OF TIMESTAMP`, until garbage collection removes the old row versions. TiDB keeps old versions for at least the time set by [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50), which is 10 minutes by default.

## See also

- [AI Agent Memory Example](/ai/guides/memory-with-pytidb.md)
- [Vector Search Index](/ai/reference/vector-search-index.md)
- [Transactions](/ai/guides/transactions.md)
- [TTL (Time to Live)](/time-to-live.md)
