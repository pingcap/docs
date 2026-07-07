---
title: TiCDC Table Routing
summary: Learn about table routing configuration in the TiCDC new architecture, including how to rewrite downstream database and table names using target-schema and target-table, how to handle DDL rewriting and routing conflicts, and how to troubleshoot common issues.
---

# TiCDC Table Routing <span class="version-mark">New in v8.5.7</span>

TiCDC table routing allows you to map upstream tables to specified downstream database names or table names through changefeed configuration. This feature applies only to the [TiCDC new architecture](/ticdc/ticdc-architecture.md) and is not supported by the [TiCDC classic architecture](/ticdc/ticdc-classic-architecture.md).

Table routing changes only the database and table names that TiCDC outputs downstream. It does not change row data, column names, table schema, table filter rules, topic dispatch rules, partition dispatch rules, or column selector rules.

## Usage scenarios

Table routing is suitable for the following scenarios:

- Replicating `sales.orders` to `archive.sales_orders`, or to a table that follows other downstream naming conventions.
- Replicating multiple source databases to the same target database while keeping target table names unique to distinguish the source, for example, replicating `tenant_001.orders` to `tenant_mirror.tenant_001_orders`.
- Building migration, disaster recovery, archiving, or shadow Changefeeds to avoid writing to downstream objects with the same names as upstream ones.
- Exposing stable database and table names to MQ consumer applications or storage services.

> **Note:**
>
> Table routing supports only one-to-one mapping from an upstream table to a downstream target table. It does not support merging multiple upstream tables into the same downstream table.
> Table routing does not support splitting one upstream table into multiple downstream tables, nor transforming row data content.

## Configure table routing

Before configuring table routing, enable the TiCDC new architecture. For details, see [`newarch`](/ticdc-server-config.md#newarch-new-in-v854-release1).

The following example routes `sales.orders` to `archive.sales_orders`:

```toml
[sink]
[[sink.dispatchers]]
matcher = ["sales.orders"]
target-schema = "archive"
target-table = "{schema}_{table}"
```

After the changefeed starts, TiCDC writes the DML and DDL events of `sales.orders` to the downstream `archive.sales_orders`.

> **Note:**
>
> Different tables in the same upstream database can route to different target databases. This kind of configuration applies only to DML and table-level DDL.

> - For database-level DDL such as `CREATE DATABASE`, `DROP DATABASE`, and `ALTER DATABASE`, TiCDC must be able to determine a unique target database based on the routing rules. Otherwise, replication of that DDL fails.
> - If you want to route different tables in the same upstream database to different target databases, you need to create the downstream target databases in advance and avoid executing upstream database-level DDL that requires automatic replication.

## Configuration fields

The table routing feature uses [`sink.dispatchers`](/ticdc/ticdc-changefeed-config.md#dispatchers) as the configuration entry.

| Field | Description |
| :--- | :--- |
| `matcher` | Matches upstream databases and tables. The syntax is the same as [table filter syntax](/table-filter.md#syntax), including wildcard matches such as `sales.*` and exclusion matches such as `!sales.tmp_*`. |
| `target-schema` | Specifies the downstream database name. If this field is not set, TiCDC keeps the upstream database name unchanged. |
| `target-table` | Specifies the downstream table name. If this field is not set, TiCDC keeps the upstream table name unchanged. |

The matching behavior is as follows:

- Only `sink.dispatchers` rules with `target-schema` or `target-table` set participate in table routing.
- If a table matches multiple table routing rules, only the first matching rule in `sink.dispatchers` takes effect.
- `matcher` always matches upstream database and table names, not the routed target database and table names.
- The Changefeed configuration item `case-sensitive` affects only whether the `matcher` in table routing is case-sensitive. It does not rewrite the expansion results of `{schema}` and `{table}`. For details, see [`case-sensitive`](/ticdc/ticdc-changefeed-config.md#case-sensitive).

### Placeholders

You can use the following placeholders in `target-schema` and `target-table`:

| Placeholder | Description |
| :--- | :--- |
| `{schema}` | The upstream database name, preserving the actual matched database name case. |
| `{table}` | The upstream table name, preserving the actual matched table name case. |

The values of `target-schema` and `target-table` can contain only literal text, `{schema}`, and `{table}`. If you use an unknown placeholder such as `{db}`, TiCDC rejects the Changefeed configuration and returns the `CDC:ErrInvalidTableRoutingRule` error.

Using the source table `sales.orders` as an example:

| Configuration | Target table |
| :--- | :--- |
| `target-schema = "archive"` | `archive.orders` |
| `target-table = "{table}_bak"` | `sales.orders_bak` |
| `target-schema = "{schema}_mirror"` | `sales_mirror.orders` |
| `target-schema = "archive"` and `target-table = "{schema}_{table}"` | `archive.sales_orders` |

## Examples

### Route all tables in one database

The following configuration routes all tables in the `sales` database to the `archive` database and appends `_bak` to the target table names:

```toml
[filter]
rules = ["sales.*"]

[sink]
[[sink.dispatchers]]
matcher = ["sales.*"]
target-schema = "archive"
target-table = "{table}_bak"
```

Example routing results:

- `sales.orders` is routed to `archive.orders_bak`.
- `sales.order_items` is routed to `archive.order_items_bak`.

### Route multiple databases to the same target database

When routing multiple databases to the same target database, it is recommended to include `{schema}` in `target-table` to ensure unique target table names.

```toml
[filter]
rules = ["sales.*", "crm.*", "finance.*"]

[sink]
[[sink.dispatchers]]
matcher = ["sales.*", "crm.*", "finance.*"]
target-schema = "archive"
target-table = "{schema}_{table}"
```

Example routing results:

- `sales.orders` is routed to `archive.sales_orders`.
- `crm.orders` is routed to `archive.crm_orders`.
- `finance.orders` is routed to `archive.finance_orders`.

> **Note:**
>
> This configuration applies only to database merging, not table merging. Table routing does not support merging same-named tables from multiple different databases into the same downstream table.

### Use table routing together with Kafka sink topic and partition dispatchers

The same dispatcher rule can include both table routing fields and existing dispatch fields:

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

In the preceding example, table routing changes the database and table names exposed in downstream data to `public.orders`.

Table routing does not change the dispatch results of Topic or Partition. The `topic` and `partition` dispatchers still perform matching and dispatch calculation based on the upstream table `sales.orders`.

## Output behavior

| Sink | Behavior |
| :--- | :--- |
| MySQL sink | TiCDC writes DDL and DML statements to the routed target database and table. When the Redo feature is enabled, executing `redo apply` replays events to the routed target table. |
| Kafka sink and Pulsar sink | The values of the `payload` field in the protocol and the `query` field in DDL events use the routed target database and table names; the values of the `schema` and `table` fields in the encoding protocol also use the routed target database and table names. |
| Cloud storage sink | TiCDC generates the corresponding storage paths, schema files, table definition files, and data files based on the routed target database and table names. |

## DDL behavior

After you enable table routing, TiCDC rewrites DDL statements so that the database and table names in structured DDL metadata remain consistent with those in the SQL text.

For example, if the following rule is configured:

```toml
[[sink.dispatchers]]
matcher = ["sales.*"]
target-schema = "archive"
target-table = "{table}_routed"
```

TiCDC rewrites the following upstream DDL:

```sql
RENAME TABLE `sales`.`temp_table` TO `sales`.`renamed_table`;
```

into the following downstream DDL:

```sql
RENAME TABLE `archive`.`temp_table_routed` TO `archive`.`renamed_table_routed`;
```

If a DDL statement contains table references and those table references match table routing rules, TiCDC also rewrites the referenced table names. For example, TiCDC can rewrite table references in `CREATE VIEW` statements and foreign key references in `ALTER TABLE` statements.

For database-level DDL such as `CREATE DATABASE`, `DROP DATABASE`, and `ALTER DATABASE ... CHARACTER SET/COLLATE`, if the database name matches table routing rules, TiCDC rewrites the database name. **If the same upstream database matches multiple table routing rules and these rules resolve to different target database names, TiCDC cannot determine a unique target database for that database-level DDL, and the Changefeed returns a table routing error.**

When creating or updating a changefeed, TiCDC checks for target table conflicts based on the tables currently within the replication scope. During runtime, TiCDC updates the conflict detection state when replicating DDL such as `CREATE TABLE`, `RENAME TABLE`, `DROP TABLE`, and `DROP DATABASE`. TiCDC evaluates whether a database-level DDL can determine a unique target database when replicating the corresponding DDL.

## Route conflict detection

A route conflict occurs when two different upstream tables are routed to the same downstream `(schema, table)` within a single Changefeed. TiCDC does not support merging multiple upstream tables into the same downstream table.

For example, the following configuration might cause a conflict:

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

If both `sales.orders` and `crm.orders` are within the replication scope, both tables route to `archive.orders`. TiCDC rejects the creation or update of the Changefeed and returns the `CDC:ErrTableRouteConflict` error.

While the Changefeed is running, if a DDL statement such as `CREATE TABLE` or `RENAME TABLE` causes two upstream tables currently within the replication scope to route to the same target table, the Changefeed fails and returns the `CDC:ErrTableRouteConflict` error.

If an upstream table is dropped or renamed, TiCDC removes the routing relationship between that upstream table and the target table. After that, a new upstream table can continue to use that target table. However, at any given time, the same target table can correspond to only one upstream table being replicated by the current Changefeed.

> **Warning:**
>
> Route conflict detection takes effect within a single changefeed. If multiple Changefeeds write to the same downstream system, make sure that the table routing rules of these Changefeeds do not write to the same target object.

## Troubleshooting

| Symptom | Possible cause | Solution |
| :--- | :--- | :--- |
| TiCDC reports the `CDC:ErrInvalidTableRoutingRule` error when you create or update a Changefeed. | The `matcher` syntax is invalid, or `target-schema` or `target-table` contains unknown placeholders or mismatched braces. | Check whether `matcher` conforms to the [table filter syntax](/table-filter.md#syntax), and make sure that `target-schema` and `target-table` use only literal text, `{schema}`, and `{table}`. |
| The MQ topic name still uses the upstream schema and table name. | Table routing does not change topic or partition dispatch rules. | If you need to change the topic name, configure `topic` separately in `sink.dispatchers`. |
| TiCDC reports the `CDC:ErrTableRoutingFailed` error during DDL replication. | TiCDC cannot safely rewrite the DDL for table routing, or a schema-level DDL has ambiguity in the target schema. | Check the DDL type and routing rules. For schema-level DDL, make sure the same upstream schema can be parsed to only one target schema. |
| The Changefeed fails during runtime and TiCDC reports the `CDC:ErrTableRouteConflict` error. | After a table is created or renamed, two different upstream tables route to the same downstream table. | Adjust the table routing rules or upstream DDL to ensure that, within a single Changefeed, each target table corresponds to only one upstream table being replicated by the current Changefeed at any given time. |

## Related documentation

- [CLI and Configuration Parameters of TiCDC Changefeeds](/ticdc/ticdc-changefeed-config.md)
- [Changefeed Log Filters](/ticdc/ticdc-filter.md)
- [Replicate Data to MySQL-compatible Databases](/ticdc/ticdc-sink-to-mysql.md)
- [Replicate Data to Kafka](/ticdc/ticdc-sink-to-kafka.md)
- [Replicate Data to Pulsar](/ticdc/ticdc-sink-to-pulsar.md)
- [Replicate Data to Storage Services](/ticdc/ticdc-sink-to-cloud-storage.md)