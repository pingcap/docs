---
title: PostgreSQL Session Parameters
summary: Learn how to view and configure PostgreSQL session parameters on PostgreSQL-compatible TiDB Cloud Starter.
---

# PostgreSQL Session Parameters

PostgreSQL-compatible {{{ .starter }}} supports PostgreSQL-compatible session parameters that control transaction behavior, schema resolution, time zones, query timeouts, output formats, and other session settings.


## Set and view parameters

Use `SET` to change a parameter for the current session:

```sql
SET statement_timeout = '120s';
```

Use `SET LOCAL` to change a parameter only for the current transaction:

```sql
BEGIN;

SET LOCAL statement_timeout = '30s';

SELECT *
FROM large_table;

COMMIT;
```

Use `SHOW` to view the current value:

```sql
SHOW statement_timeout;
```

List all recognized parameters:

```sql
SHOW ALL;
```

Use `RESET` to restore one parameter to its default value:

```sql
RESET statement_timeout;
```

Reset all session parameters:

```sql
RESET ALL;
```

## Configuration functions

Use `current_setting()` to read a parameter:

```sql
SELECT current_setting('statement_timeout');
```

Use `set_config()` to change a parameter:

```sql
SELECT set_config(
    'statement_timeout',
    '120s',
    false
);
```

The third argument controls scope:

- `false`: session scope.
- `true`: transaction-local scope.

## Common PostgreSQL-compatible parameters

The following commonly used parameters are supported:

| Parameter | Default | Mutable | Description |
| --- | --- | --- | --- |
| `application_name` | Empty | Yes | Application name associated with the session. |
| `bytea_output` | `hex` | Yes | Output format for `BYTEA` values. |
| `client_encoding` | `UTF8` | Yes | Client character encoding. |
| `client_min_messages` | `notice` | Yes | Minimum message severity sent to the client. |
| `datestyle` | `ISO, MDY` | No | Date display format. |
| `default_transaction_isolation` | `read committed` | Yes | Default isolation level for new transactions. |
| `default_transaction_read_only` | `off` | Yes | Default read-only state for new transactions. |
| `extra_float_digits` | `1` | Yes | Extra precision for floating-point output. |
| `search_path` | `$user, public` | Yes | Schema search order. |
| `server_encoding` | `UTF8` | No | Server-side character encoding. |
| `standard_conforming_strings` | `on` | No | Treats backslashes literally in string constants. |
| `statement_timeout` | `60000ms` | Yes | Query timeout. Set to `0` for no timeout. |
| `timezone` | `UTC` | Yes | Session time zone. |
| `transaction_isolation` | `read committed` | Yes | Current transaction isolation level. |
| `lock_timeout` | `0` | Yes | Lock acquisition timeout. |
| `password_encryption` | `scram-sha-256` | Yes | Password hashing algorithm. |
| `max_identifier_length` | `63` | No | Maximum identifier length in bytes. |
| `lc_messages` | `C` | Yes | Locale used for server messages. |

`SHOW ALL` is the best way to inspect the complete parameter set available in the current PostgreSQL-compatible {{{ .starter }}} instance.

## Search path

The `search_path` parameter controls the schema resolution order.

View the current search path:

```sql
SHOW search_path;
```

Change it for the current session:

```sql
SET search_path = app, public;
```

After this change, an unqualified name is resolved against `app` before `public`.

## Time zone

View the current time zone:

```sql
SHOW timezone;
```

Set the session time zone:

```sql
SET timezone = 'America/Los_Angeles';
```

Or:

```sql
SET TIME ZONE 'UTC';
```

The session time zone affects display and interpretation of `TIMESTAMPTZ` values.

## Statement timeout

The default statement timeout is 60 seconds.

Increase it for a long-running operation:

```sql
SET statement_timeout = '180s';
```

Disable the statement timeout for the current session:

```sql
SET statement_timeout = 0;
```

Use a larger timeout carefully for operations such as index creation or large data migrations.

## Transaction parameters

Set the default isolation level for subsequent transactions:

```sql
SET default_transaction_isolation = 'repeatable read';
```

Make new transactions read-only by default:

```sql
SET default_transaction_read_only = on;
```

View the current transaction settings:

```sql
SHOW transaction_isolation;
SHOW transaction_read_only;
```


## Other accepted PostgreSQL parameters

The following PostgreSQL-compatible parameters are also recognized:

- `default_table_access_method`
- `default_tablespace`
- `default_text_search_config`
- `default_transaction_deferrable`
- `idle_in_transaction_session_timeout`
- `in_hot_standby`
- `integer_datetimes`
- `intervalstyle`
- `lc_monetary`
- `lc_numeric`
- `lc_time`
- `max_index_keys`
- `row_security`
- `xmloption`

The following additional parameters are readable with `SHOW`:

- `is_superuser`
- `listen_addresses`
- `max_connections`
- `port`
- `role`
- `server_version`
- `server_version_num`
- `session_authorization`
- `transaction_deferrable`
- `transaction_read_only`

Some values are exposed for PostgreSQL client and tool compatibility and do not imply that all corresponding upstream PostgreSQL server functionality is available.

## Compatibility-only parameters

Some PostgreSQL parameters are accepted so that PostgreSQL clients and frameworks can initialize sessions successfully, but changing them does not change query behavior.

### `work_mem`

`work_mem` is accepted and its session value can be changed:

```sql
SET work_mem = '64MB';
SHOW work_mem;
```

The configured value does not control query execution memory in PostgreSQL-compatible {{{ .starter }}}.

### `check_function_bodies`

`check_function_bodies` is accepted, but it does not control function-body validation in the same way as PostgreSQL.

SQL statements inside PL/pgSQL function bodies might be validated only when the function is called. Test functions after creating them.

## `session_replication_role`

`session_replication_role = 'replica'` is not supported.

The following statement is rejected:

```sql
SET session_replication_role = 'replica';
```

Triggers continue to execute with normal `origin` behavior.

Do not rely on `session_replication_role` to suppress triggers during bulk loading.

## Full-text search parameter

The `default_text_search_config` parameter controls the default full-text search configuration.

View the current value:

```sql
SHOW default_text_search_config;
```

Set it for the current session:

```sql
SET default_text_search_config = 'simple';
```


## Vector search parameter

The `hnsw.ef_search` parameter controls the HNSW candidate list size for the current session.

View it:

```sql
SHOW hnsw.ef_search;
```

Set it:

```sql
SET hnsw.ef_search = 100;
```

The default value is `40`. A higher value can improve recall at the cost of additional query latency.


## Embedding parameter

After you enable the `embedding` extension, the `embedding.dimensions` parameter controls the output dimension used by supported server-side embedding functions.

For example:

```sql
SET embedding.dimensions = 512;
```

