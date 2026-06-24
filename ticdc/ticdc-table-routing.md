---
title: TiCDC Table Routing
summary: Learn how to configure table routing in TiCDC new architecture to rewrite downstream schema and table names, detect conflicts, and handle DDL.
---

# TiCDC Table Routing

TiCDC table routing lets you map an upstream table to a specified downstream schema name or table name through changefeed configuration. This feature applies only to [TiCDC new architecture](/ticdc/ticdc-architecture.md) and is not supported in [TiCDC classic architecture](/ticdc/ticdc-classic-architecture.md).

Table routing only changes the schema and table names that TiCDC outputs to the downstream. It does not change row data, column names, table structures, table filter rules, topic dispatch rules, partition dispatch rules, or column selector rules.

## Usage scenarios

Table routing is suitable for the following scenarios:

- Replicate `sales.orders` to `archive.sales_orders`, or to a table that follows another downstream naming convention.
- Replicate multiple source schemas to one downstream namespace while keeping target table names unique, such as replicating `tenant_001.orders` to `tenant_mirror.tenant_001_orders`.
- Build migration, disaster recovery, archive, or shadow changefeeds to avoid writing to downstream objects that have the same names as upstream objects.
- Expose stable schema and table names to MQ consumers or storage service consumers.

> **Note:**
>
> Table routing supports only one-to-one table name mappings. It does not support merging multiple upstream tables into one downstream table.
> Table routing does not support splitting one upstream table into multiple downstream tables or transforming row data.

## Configure table routing

Before you configure table routing, enable TiCDC new architecture. For more information, see [`newarch`](/ticdc/ticdc-server-config.md#newarch-new-in-v854-release1).

The following example routes `sales.orders` to `archive.sales_orders`:

```toml
[sink]
[[sink.dispatchers]]
matcher = ["sales.orders"]
target-schema = "archive"
target-table = "{schema}_{table}"
```

After the changefeed starts, DML and DDL events for `sales.orders` are written to `archive.sales_orders` in the downstream.

> **Note:**
>
> Different tables in the same upstream schema can be routed to different target schemas. This type of configuration applies only to DML and table-level DDL.
>
> For schema-level DDL statements such as `CREATE DATABASE`, `DROP DATABASE`, and `ALTER DATABASE`, TiCDC must be able to determine one unique target schema from the routing rules. Otherwise, the DDL synchronization fails.
> If one upstream schema maps to multiple downstream target schemas, create the downstream target schemas in advance, or make sure that the upstream does not generate schema-level DDL statements that need to be synchronized automatically.

## Configuration fields

Table routing uses `sink.dispatchers` as the configuration entry.

| Field | Description |
| :--- | :--- |
| `matcher` | Matches upstream schemas and tables. The syntax is the same as [table filter syntax](/table-filter.md#syntax), including wildcard patterns such as `sales.*` and exclusion patterns such as `!sales.tmp_*`. |
| `target-schema` | Specifies the downstream schema name. If this field is not set, TiCDC keeps the upstream schema name. |
| `target-table` | Specifies the downstream table name. If this field is not set, TiCDC keeps the upstream table name. |

The matching behavior is as follows:

- Only dispatcher rules that set `target-schema` or `target-table` participate in table routing.
- If a table matches multiple table routing rules, the first matching rule in `sink.dispatchers` takes effect.
- `matcher` always matches the upstream schema and table names, not the routed target schema and table names.
- The `case-sensitive` changefeed configuration item only determines whether the table routing `matcher` is case-sensitive. It does not change the expansion result of `{schema}` or `{table}`. For more information, see [`case-sensitive`](/ticdc/ticdc-changefeed-config.md#case-sensitive).

### Placeholders

You can use the following placeholders in `target-schema` and `target-table`:

| Placeholder | Description |
| :--- | :--- |
| `{schema}` | The upstream schema name. TiCDC preserves the letter case of the matched schema name. |
| `{table}` | The upstream table name. TiCDC preserves the letter case of the matched table name. |

The value of `target-schema` and `target-table` can contain only literal text, `{schema}`, and `{table}`. If you use an unknown placeholder such as `{db}`, TiCDC rejects the changefeed configuration and returns the `CDC:ErrInvalidTableRoutingRule` error.

For example, for the source table `sales.orders`:

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

> **Note:**
>
> This configuration merges schemas, not tables. This feature does not support merging same-name tables from different schemas into one downstream table.

### Use table routing with Kafka Sink topic and partition dispatchers

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

In this example, table routing changes the schema and table names exposed in the downstream data to `public.orders`.

Table routing does not change the topic or partition dispatch result. The `topic` and `partition` dispatchers still use the upstream table `sales.orders` for matching and dispatch calculation.

## Output behavior

| Sink | Behavior |
| :--- | :--- |
| MySQL Sink | DDL and DML statements are written to the routed target schema and table. If Redo is enabled, executing `redo apply` replays events to the routed target table. |
| Kafka Sink and Pulsar Sink | The protocol `payload` and DDL `query` use the routed target schema and table names. The `schema` and `table` field values in the encoding protocol are also the routed target schema and table. |
| Cloud Storage Sink | TiCDC outputs the corresponding storage paths, schema files, table definition files, and data files according to the routed target schema and table names. |

## DDL behavior

When table routing is enabled, TiCDC rewrites DDL statements so that the structured DDL fields and SQL text use consistent target names.

For example, if you configure the following rule:

```toml
[[sink.dispatchers]]
matcher = ["sales.*"]
target-schema = "archive"
target-table = "{table}_routed"
```

TiCDC routes the following upstream DDL:

```sql
RENAME TABLE `sales`.`temp_table` TO `sales`.`renamed_table`;
```

to the following downstream DDL:

```sql
RENAME TABLE `archive`.`temp_table_routed` TO `archive`.`renamed_table_routed`;
```

If a DDL statement contains table references and those table references match table routing rules, TiCDC also rewrites the referenced table names. For example, table references in `CREATE VIEW` statements and foreign key references in `ALTER TABLE` statements can be routed.

For schema-level DDL statements such as `CREATE DATABASE`, `DROP DATABASE`, and `ALTER DATABASE ... CHARACTER SET/COLLATE`, if the schema name matches table routing rules, TiCDC rewrites the schema name. **If the same upstream schema matches multiple table routing rules but these rules resolve to different target schema names, TiCDC cannot determine one unique target schema for the schema-level DDL, and the changefeed reports a table routing error.**

When you create or update a changefeed, TiCDC checks target table conflicts based on tables in the current replication scope. During changefeed runtime, TiCDC updates the conflict detection state when it replicates DDL statements such as `CREATE TABLE`, `RENAME TABLE`, `DROP TABLE`, and `DROP DATABASE`. Whether a schema-level DDL can be routed to one unique target schema is checked when TiCDC replicates the corresponding DDL.

## Route conflict detection

A route conflict occurs when two different upstream tables are routed to the same downstream `(schema, table)`. TiCDC does not support merging multiple upstream tables into one downstream table.

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

During changefeed runtime, if a DDL statement such as `CREATE TABLE` or `RENAME TABLE` causes two active upstream tables to route to the same target table, the changefeed fails and returns the `CDC:ErrTableRouteConflict` error.

After an upstream table is dropped or renamed, TiCDC releases the target table occupied by the old source table name. A new source table name can then use the same target table, as long as no two active upstream tables are routed to that target table at the same time.

> **Warning:**
>
> Route conflict detection is scoped to a single changefeed. If multiple changefeeds write to the same downstream system, make sure that their table routing rules do not write to the same target objects.

## Troubleshooting

| Symptom | Possible cause | Solution |
| :--- | :--- | :--- |
| Changefeed creation fails with the `CDC:ErrInvalidTableRoutingRule` error. | `target-schema` or `target-table` contains an invalid placeholder or invalid braces. | Use only literal text, `{schema}`, and `{table}`. |
| The MQ topic name still uses the upstream schema and table names. | Table routing does not change topic or partition dispatching. | If you need to change topic names, configure `topic` separately in `sink.dispatchers`. |
| A DDL statement fails with the `CDC:ErrTableRoutingFailed` error. | The DDL statement cannot be safely rewritten for table routing, or schema-level routing is ambiguous. | Adjust the routing rules. |
| A running changefeed fails with the `CDC:ErrTableRouteConflict` error. | After a table is created or renamed, two different upstream tables are routed to the same downstream table. | Adjust the table routing rules or upstream DDL, and make sure each target table in a single changefeed maps to only one active upstream table. |

## Related documents

- [CLI and Configuration Parameters of TiCDC Changefeeds](/ticdc/ticdc-changefeed-config.md)
- [Changefeed Log Filters](/ticdc/ticdc-filter.md)
- [Replicate Data to MySQL-compatible Databases](/ticdc/ticdc-sink-to-mysql.md)
- [Replicate Data to Kafka](/ticdc/ticdc-sink-to-kafka.md)
- [Replicate Data to Pulsar](/ticdc/ticdc-sink-to-pulsar.md)
- [Replicate Data to Storage Services](/ticdc/ticdc-sink-to-cloud-storage.md)
