---
title: TiCDC Table Routing
summary: Learn how to configure TiCDC table routing to rename downstream schemas and tables while keeping existing dispatch rules unchanged.
---

# TiCDC Table Routing

TiCDC table routing lets you map an upstream table to a downstream schema name or table name by adding `target-schema` and `target-table` to `sink.dispatchers`. Use table routing when the downstream naming convention differs from the upstream naming convention, such as when you replicate data to an archive schema, a shadow schema, or a shared downstream system that requires unique target names.

Table routing only changes the schema and table names that TiCDC outputs to the downstream. It does not change row values, column names, table structures, table filter rules, topic dispatch rules, partition dispatch rules, or column selector rules.

## Usage scenarios

Table routing is suitable for the following scenarios:

- Replicating `sales.orders` to `archive.sales_orders` or another downstream naming convention.
- Replicating multiple source schemas to one downstream namespace while preserving unique table names, such as `tenant_001.orders` to `tenant_mirror.tenant_001_orders`.
- Building migration, disaster recovery, archive, or shadow changefeeds that must not write to objects with the same names as the upstream objects.
- Exposing stable schema and table names to MQ consumers or storage consumers without changing existing topic, partition, or storage sink configuration.

Table routing is not suitable for merging multiple upstream tables into one downstream table, splitting one upstream table into multiple downstream tables, or transforming row contents.

## Configure table routing

1. Prepare the downstream environment.

    Make sure that TiCDC has the required downstream permissions. If the changefeed starts after the upstream schema or table is created, create compatible target schemas and tables manually. If the changefeed captures the corresponding upstream DDL events, TiCDC routes the DDL statements to the target names.

2. Create a changefeed configuration file.

    The following example routes `sales.orders` to `archive.sales_orders`:

    ```toml
    [filter]
    rules = ["sales.orders"]

    [sink]
    [[sink.dispatchers]]
    matcher = ["sales.orders"]
    target-schema = "archive"
    target-table = "{schema}_{table}"
    ```

3. Create the changefeed with the configuration file.

    ```shell
    cdc cli changefeed create \
        --server=http://127.0.0.1:8300 \
        --changefeed-id="table-route-demo" \
        --sink-uri="mysql://root:password@127.0.0.1:3306/" \
        --config=changefeed.toml
    ```

After the changefeed starts, DML and DDL events for `sales.orders` are written to `archive.sales_orders` in the downstream.

## Configuration fields

Table routing reuses `sink.dispatchers` as the configuration entry. You can use either `dispatchers = [...]` or `[[sink.dispatchers]]`.

| Field | Description |
| :--- | :--- |
| `matcher` | Matches upstream schemas and tables. The syntax is the same as [table filter syntax](/table-filter.md#syntax), including wildcard patterns such as `sales.*` and exclusion patterns such as `!sales.tmp_*`. |
| `target-schema` | Specifies the downstream schema name. If this field is not set, TiCDC keeps the upstream schema name. |
| `target-table` | Specifies the downstream table name. If this field is not set, TiCDC keeps the upstream table name. |

The matching behavior is as follows:

- Only dispatcher rules that set `target-schema` or `target-table` participate in table routing.
- If a table matches multiple table routing rules, the first matching rule in `sink.dispatchers` takes effect.
- `matcher` always matches the upstream schema and table names, not the routed target names.
- The `case-sensitive` changefeed configuration also applies to table routing matchers. For more information, see [`case-sensitive`](/ticdc/ticdc-changefeed-config.md#case-sensitive).

### Placeholders

You can use the following placeholders in `target-schema` and `target-table`:

| Placeholder | Description |
| :--- | :--- |
| `{schema}` | The upstream schema name. |
| `{table}` | The upstream table name. |

The value of `target-schema` and `target-table` can contain only literal text, `{schema}`, and `{table}`. If you use an unknown placeholder such as `{db}`, TiCDC rejects the changefeed configuration and returns the `CDC:ErrInvalidTableRoutingRule` error.

For example, for the upstream table `sales.orders`:

| Configuration | Target table |
| :--- | :--- |
| `target-schema = "archive"` | `archive.orders` |
| `target-table = "{table}_bak"` | `sales.orders_bak` |
| `target-schema = "{schema}_mirror"` | `sales_mirror.orders` |
| `target-schema = "archive"` and `target-table = "{schema}_{table}"` | `archive.sales_orders` |

## Examples

### Route all tables in one schema

The following configuration routes all tables in the `sales` schema to the `archive` schema and appends `_bak` to the target table names:

```toml
[filter]
rules = ["sales.*"]

[sink]
[[sink.dispatchers]]
matcher = ["sales.*"]
target-schema = "archive"
target-table = "{table}_bak"
```

Example route results:

- `sales.orders` is routed to `archive.orders_bak`.
- `sales.order_items` is routed to `archive.order_items_bak`.

### Route multiple schemas to one target schema

When you route multiple schemas to one target schema, include `{schema}` in `target-table` to keep target table names unique.

```toml
[filter]
rules = ["sales.*", "crm.*", "finance.*"]

[sink]
[[sink.dispatchers]]
matcher = ["sales.*", "crm.*", "finance.*"]
target-schema = "archive"
target-table = "{schema}_{table}"
```

Example route results:

- `sales.orders` is routed to `archive.sales_orders`.
- `crm.orders` is routed to `archive.crm_orders`.
- `finance.orders` is routed to `archive.finance_orders`.

### Use table routing with topic and partition dispatchers

The same dispatcher rule can include table routing fields and existing dispatch fields:

```toml
[filter]
rules = ["sales.orders"]

[sink]
[[sink.dispatchers]]
matcher = ["sales.orders"]
topic = "order-events"
partition = "index-value"
target-schema = "public"
target-table = "orders"
```

In this example, table routing changes the schema and table names exposed in the downstream data to `public.orders`. The `topic` and `partition` dispatchers still use the upstream table `sales.orders` for matching and dispatch calculation.

## Output behavior

Table routing affects sink output as follows:

| Sink type | Output behavior |
| :--- | :--- |
| MySQL-compatible database and TiDB | DML events are written to the target schema and table. DDL statements are rewritten to operate on the target objects. |
| Kafka | Message payload fields that represent schema or table names use the target names. DDL message fields and DDL query text use the target names. Topic and partition dispatching still use upstream names. |
| Pulsar | Canal-JSON payload fields that represent schema or table names use the target names. Topic and partition dispatching still use upstream names. |
| Storage services | Storage paths, schema files, table definition files, and data files use the target schema and table names. |
| Redo log | Redo records preserve the target schema and table names. When you apply redo logs, events are replayed to the routed target objects. |

For MQ sinks, table routing does not change the topic or partition dispatch result. For example, if `topic = "{schema}_{table}"` and the source table is `sales.orders`, TiCDC still dispatches the event to the topic `sales_orders` even if the payload table name is routed to `archive.sales_orders`.

## DDL behavior

When table routing is enabled, TiCDC rewrites parser-supported DDL statements so that the structured DDL fields and the SQL text use the same target names.

For example, if you configure the following rule:

```toml
[[sink.dispatchers]]
matcher = ["sales.*"]
target-schema = "archive"
target-table = "{table}_routed"
```

TiCDC routes this upstream DDL:

```sql
RENAME TABLE `sales`.`temp_table` TO `sales`.`renamed_table`;
```

to the following downstream DDL:

```sql
RENAME TABLE `archive`.`temp_table_routed` TO `archive`.`renamed_table_routed`;
```

If a DDL statement contains table references, TiCDC also rewrites the referenced table names when they match table routing rules. For example, table references in `CREATE VIEW` statements and foreign key references in `ALTER TABLE` statements can be routed.

For schema-level DDL statements, such as `CREATE DATABASE` and `DROP DATABASE`, TiCDC rewrites the schema name when the schema matches table routing rules. If multiple table routing rules match the same upstream schema but resolve to different target schemas, TiCDC cannot determine one target schema for the schema-level DDL and the changefeed reports a table routing error.

> **Note:**
>
> Table routing DDL rewrite relies on TiDB parser support. If TiCDC cannot parse and restore a DDL statement for table routing, the changefeed reports a `CDC:ErrTableRoutingFailed` error instead of silently sending the original DDL to the downstream. DDL statements that TiCDC identifies as full-text index or hybrid index DDLs are not routed.

## Route conflict detection

A route conflict occurs when two different upstream tables are routed to the same downstream `(schema, table)` pair. TiCDC does not support merging multiple upstream tables into one downstream table.

For example, the following configuration can cause a conflict:

```toml
[filter]
rules = ["sales.*", "crm.*"]

[sink]
[[sink.dispatchers]]
matcher = ["sales.*"]
target-schema = "archive"
target-table = "{table}"

[[sink.dispatchers]]
matcher = ["crm.*"]
target-schema = "archive"
target-table = "{table}"
```

If both `sales.orders` and `crm.orders` are in the replication scope, both tables are routed to `archive.orders`. TiCDC rejects the changefeed create or update operation and returns the `CDC:ErrTableRouteConflict` error.

TiCDC also detects conflicts that appear after a changefeed starts. For example, if a wildcard rule starts replicating a newly created table, or a `RENAME TABLE` statement changes a source table name, and the new route result conflicts with an existing target table, the changefeed enters the failed state with `CDC:ErrTableRouteConflict`.

> **Warning:**
>
> Route conflict detection is scoped to a single changefeed. If multiple changefeeds write to the same downstream system, make sure their table routing rules do not write to the same target objects.

## Limitations

- Table routing supports one-to-one table name mapping only. It does not support merging multiple upstream tables into one downstream table.
- Table routing does not transform row values, column names, column types, or table schemas.
- `filter.rules`, `matcher`, `topic`, `partition`, and `columns` continue to use upstream schema and table names.
- Removing table routing configuration or rolling back TiCDC does not rename downstream tables, move storage files, rewrite MQ messages, or clean up redo logs that have already been generated with target names.
- If the source and target are in the same database instance, make sure that the routed target schemas are not included in the same changefeed replication scope. Otherwise, the changefeed might replicate its own downstream writes.

## Troubleshooting

| Symptom | Possible cause | Solution |
| :--- | :--- | :--- |
| Changefeed creation fails with `CDC:ErrInvalidTableRoutingRule`. | `target-schema` or `target-table` contains an invalid placeholder or invalid braces. | Use only literal text, `{schema}`, and `{table}`. |
| Changefeed creation, update, or runtime replication fails with `CDC:ErrTableRouteConflict`. | Two upstream tables are routed to the same downstream schema and table. | Change the routing rule so each upstream table maps to a unique target table, such as by adding `{schema}` to `target-table`. |
| The MQ topic name still uses the upstream schema and table names. | Table routing does not change topic or partition dispatching. | If you need to change topic names, configure `topic` separately in `sink.dispatchers`. |
| A DDL statement fails with `CDC:ErrTableRoutingFailed`. | The DDL statement cannot be safely rewritten for table routing, or schema-level routing is ambiguous. | Adjust the routing rules, filter out the unsupported DDL, or handle the DDL manually in the downstream. |

## Related documents

- [CLI and Configuration Parameters of TiCDC Changefeeds](/ticdc/ticdc-changefeed-config.md)
- [Changefeed Log Filters](/ticdc/ticdc-filter.md)
- [Replicate Data to MySQL-compatible Databases](/ticdc/ticdc-sink-to-mysql.md)
- [Replicate Data to Kafka](/ticdc/ticdc-sink-to-kafka.md)
- [Replicate Data to Pulsar](/ticdc/ticdc-sink-to-pulsar.md)
- [Replicate Data to Storage Services](/ticdc/ticdc-sink-to-cloud-storage.md)
