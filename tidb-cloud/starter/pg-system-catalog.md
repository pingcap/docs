---
title: PostgreSQL System Catalog
summary: Learn how to inspect database objects using PostgreSQL-compatible system catalogs on PostgreSQL-compatible TiDB Cloud Starter.
---

# PostgreSQL System Catalog

PostgreSQL-compatible {{{ .starter }}} provides PostgreSQL-compatible `pg_catalog` relations and `information_schema` views for inspecting databases, schemas, tables, columns, indexes, constraints, functions, roles, and other database objects.

## `pg_catalog` relations

The following commonly used `pg_catalog` relations are available:

| Relation | Description |
| --- | --- |
| `pg_tables` | User tables. |
| `pg_views` | Views. |
| `pg_class` | Tables, indexes, sequences, and views. |
| `pg_attribute` | Table columns. |
| `pg_attrdef` | Column default values. |
| `pg_namespace` | Schemas. |
| `pg_type` | Data types. |
| `pg_index` | Index metadata. |
| `pg_indexes` | Index definitions, including `indexdef`. |
| `pg_constraint` | Primary key, foreign key, check, unique, and not-null constraints. |
| `pg_proc` | Functions and procedures. |
| `pg_trigger` | Trigger metadata. |
| `pg_enum` | Enum values. |
| `pg_sequence` | Sequence metadata. |
| `pg_extension` | Extensions registered in the database. |
| `pg_collation` | Built-in collations. |
| `pg_roles` | Database roles. |
| `pg_user` | Login users. |
| `pg_auth_members` | Role membership. |
| `pg_db_role_setting` | Per-role session parameter defaults. |
| `pg_database` | Databases. |
| `pg_description` | Object comments and descriptions. |
| `pg_depend` | Object dependency metadata. |
| `pg_am` | Index access methods. |
| `pg_stat_user_tables` | User-table statistics. |
| `pg_inherits` | Table inheritance metadata. |
| `pg_range` | Range type metadata. |
| `pg_opclass` | Operator classes. |
| `pg_policy` | Row-level security policy metadata. |
| `pg_policies` | Readable row-level security policy definitions. |
| `pg_settings` | Runtime parameters. |
| `pg_timezone_names` | Time zone names and UTC offsets. |
| `pg_rewrite` | Rewrite rules used by views. |
| `pg_aggregate` | Aggregate function metadata. |

Some catalog relations exist primarily for PostgreSQL compatibility even when the corresponding PostgreSQL feature is not supported. Do not treat the presence of a catalog relation as proof that the underlying PostgreSQL feature is available.

For example, logical replication is not supported even though some replication-related catalog objects can be present. 

## `information_schema` views

The following `information_schema` views are available:

| View | Description |
| --- | --- |
| `tables` | Tables and views. |
| `columns` | Table columns, including generated-column metadata. |
| `schemata` | Schemas. |
| `sequences` | Sequences. |
| `routines` | Functions and procedures. |
| `table_constraints` | Primary key, foreign key, check, and unique constraints. |
| `key_column_usage` | Primary-key and foreign-key columns. |
| `referential_constraints` | Foreign-key relationships. |
| `check_constraints` | Check constraints. |
| `constraint_column_usage` | Columns referenced by constraints. |
| `table_privileges` | Table privileges. |
| `triggers` | Trigger definitions, timing, and orientation. |

> **Note:**
>
> `information_schema.views` is not available. To list views, query `pg_views` or filter `information_schema.tables` by `table_type = 'VIEW'`.

For column nullability, use `information_schema.columns.is_nullable` or `pg_attribute.attnotnull`.

## List tables in a schema

Use `pg_tables`:

```sql
SELECT
    tablename AS table,
    tableowner AS owner,
    hasindexes AS indexed,
    hastriggers AS has_triggers
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;
```

For a more portable query, use `information_schema.tables`:

```sql
SELECT
    table_name,
    table_type
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_type = 'BASE TABLE'
ORDER BY table_name;
```

## List columns of a table

Use `information_schema.columns`:

```sql
SELECT
    column_name,
    data_type,
    character_maximum_length,
    is_nullable,
    column_default,
    ordinal_position
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'my_table'
ORDER BY ordinal_position;
```

For lower-level metadata, query `pg_attribute`:

```sql
SELECT
    a.attname AS column_name,
    pg_catalog.format_type(a.atttypid, a.atttypmod) AS data_type,
    a.attnotnull AS not_null,
    a.attnum AS position
FROM pg_attribute AS a
JOIN pg_class AS c
    ON c.oid = a.attrelid
JOIN pg_namespace AS n
    ON n.oid = c.relnamespace
WHERE n.nspname = 'public'
  AND c.relname = 'my_table'
  AND a.attnum > 0
  AND NOT a.attisdropped
ORDER BY a.attnum;
```

## Find indexes on a table

Use `pg_indexes`:

```sql
SELECT
    indexname AS index_name,
    indexdef AS definition
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename = 'my_table'
ORDER BY indexname;
```

For more detailed index metadata:

```sql
SELECT
    i.relname AS index_name,
    ix.indisunique AS is_unique,
    ix.indisprimary AS is_primary
FROM pg_index AS ix
JOIN pg_class AS t
    ON t.oid = ix.indrelid
JOIN pg_class AS i
    ON i.oid = ix.indexrelid
JOIN pg_namespace AS n
    ON n.oid = t.relnamespace
WHERE n.nspname = 'public'
  AND t.relname = 'my_table'
ORDER BY i.relname;
```

## Check table constraints

Use `information_schema` for common constraints:

```sql
SELECT
    tc.constraint_name,
    tc.constraint_type,
    kcu.column_name,
    cc.check_clause
FROM information_schema.table_constraints AS tc
LEFT JOIN information_schema.key_column_usage AS kcu
    ON kcu.constraint_name = tc.constraint_name
    AND kcu.table_schema = tc.table_schema
LEFT JOIN information_schema.check_constraints AS cc
    ON cc.constraint_name = tc.constraint_name
    AND cc.constraint_schema = tc.constraint_schema
WHERE tc.table_schema = 'public'
  AND tc.table_name = 'my_table'
ORDER BY tc.constraint_type, tc.constraint_name;
```

Use `pg_constraint` for a concise definition:

```sql
SELECT
    conname AS constraint_name,
    contype AS constraint_type,
    pg_get_constraintdef(oid) AS definition
FROM pg_constraint
WHERE conrelid = 'public.my_table'::regclass
ORDER BY contype, conname;
```

`pg_constraint` also exposes not-null constraints. To check column nullability in a PostgreSQL-portable way, prefer `information_schema.columns.is_nullable`.

## Find foreign keys

Use `information_schema` to inspect outbound foreign keys:

```sql
SELECT
    tc.constraint_name,
    kcu.column_name AS fk_column,
    ccu.table_name AS referenced_table,
    ccu.column_name AS referenced_column,
    rc.update_rule,
    rc.delete_rule
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON kcu.constraint_name = tc.constraint_name
    AND kcu.table_schema = tc.table_schema
JOIN information_schema.referential_constraints AS rc
    ON rc.constraint_name = tc.constraint_name
    AND rc.constraint_schema = tc.constraint_schema
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = rc.unique_constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND tc.table_schema = 'public'
  AND tc.table_name = 'my_table'
ORDER BY tc.constraint_name;
```

## List functions and procedures

Use `information_schema.routines`:

```sql
SELECT
    routine_name,
    routine_type,
    data_type AS return_type
FROM information_schema.routines
WHERE routine_schema = 'public'
ORDER BY routine_name;
```

For additional metadata, query `pg_proc`:

```sql
SELECT
    p.proname AS function_name,
    format_type(p.prorettype, NULL) AS return_type,
    p.prokind AS kind
FROM pg_proc AS p
JOIN pg_namespace AS n
    ON n.oid = p.pronamespace
WHERE n.nspname = 'public'
ORDER BY p.proname;
```

## Inspect roles and privileges

List roles:

```sql
SELECT
    rolname,
    rolcanlogin,
    rolinherit,
    rolbypassrls
FROM pg_roles
ORDER BY rolname;
```

List table privileges:

```sql
SELECT
    grantee,
    table_schema,
    table_name,
    privilege_type
FROM information_schema.table_privileges
WHERE table_schema = 'public'
ORDER BY table_name, grantee, privilege_type;
```

## Inspect row-level security

List policies for a table:

```sql
SELECT
    policyname AS policy,
    cmd AS command,
    roles AS applies_to,
    qual AS using_expression,
    with_check AS check_expression
FROM pg_policies
WHERE schemaname = 'public'
  AND tablename = 'my_table'
ORDER BY policyname;
```

Check whether row-level security is enabled or forced:

```sql
SELECT
    relname,
    relrowsecurity,
    relforcerowsecurity
FROM pg_class
WHERE oid = 'public.my_table'::regclass;
```

## Inspect extensions

List extensions registered in the current database:

```sql
SELECT
    extname,
    extversion
FROM pg_extension
ORDER BY extname;
```


## System catalog compatibility

PostgreSQL-compatible {{{ .starter }}} implements the catalog surface needed by common PostgreSQL tools and introspection workflows, but catalog contents and columns can differ from upstream PostgreSQL.

In particular:

- Not every upstream `pg_catalog` or `information_schema` relation is available.
- Some catalog relations exist for compatibility even when the underlying PostgreSQL feature is unsupported.
- Some catalog relations expose a subset of upstream PostgreSQL columns.
- `information_schema.views` is not available.
- Custom collations can be used but are not listed in `pg_collation`.
- Trigger timing and row/statement orientation should be read from `information_schema.triggers`.