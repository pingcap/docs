---
title: Data Check for Tables with Different Schema or Table Names
summary: Learn the data check for different database names or table names.
aliases: ['/docs/dev/sync-diff-inspector/route-diff/','/docs/dev/reference/tools/sync-diff-inspector/route-diff/']
---

# Data Check for Tables with Different Schema or Table Names

When using replication tools such as [TiDB Data Migration](/dm/dm-overview.md), you can set `route-rules` to replicate data to a specified table in the downstream. sync-diff-inspector enables you to verify tables with different schema names or table names by setting `rules`.

The following is a simple configuration example. To learn the complete configuration, refer to [Sync-diff-inspector User Guide](/sync-diff-inspector/sync-diff-inspector-overview.md).

```toml
######################### Datasource config #########################
[data-sources.mysql1]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""
    route-rules = ["rule1"]

[data-sources.tidb0]
    host = "127.0.0.1"
    port = 4000
    user = "root"
    password = ""
########################### Routes ###########################
[routes.rule1]
schema-pattern = "test_1"      # Matches the schema name of the data source. Supports the wildcards "*" and "?"
table-pattern = "t_1"          # Matches the table name of the data source. Supports the wildcards "*" and "?"
target-schema = "test_2"       # The name of the schema in the target database
target-table = "t_2"           # The name of the target table
```

This configuration can be used to check `test_2.t_2` in the downstream and `test_1.t_1` in the `mysql1` instance.

To check a large number of tables with different schema names or table names, you can simplify the configuration by setting the mapping relationship by using `rules`. You can configure the mapping relationship of either schema or table, or of both. For example, all the tables in the upstream `test_1` database are replicated to the downstream `test_2` database, which can be checked through the following configuration:

```toml
######################### Datasource config #########################
[data-sources.mysql1]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""
    route-rules = ["rule1"]

[data-sources.tidb0]
    host = "127.0.0.1"
    port = 4000
    user = "root"
    password = ""
########################### Routes ###########################
[routes.rule1]
schema-pattern = "test_1"      # Matches the schema name of the data source. Supports the wildcards "*" and "?"
table-pattern = "*"            # Matches the table name of the data source. Supports the wildcards "*" and "?"
target-schema = "test_2"       # The name of the schema in the target database
target-table = "t_2"           # The name of the target table
```

## Note

Say that we have rule pattern in the config like this:

```toml
[routes.rule1]
schema-pattern = "schema*"  # schema to match. Support wildcard characters * and ?.
table-pattern = "table_*"   # table to match. Support wildcard characters * and ?.
target-schema = "schema"    # target schema
target-table = "table"      # target table
```

For the above rule, we can say that the rule matches `schema2.table_3 -> schema.table`.

**The initialization of table router works in the following ways:**

* Given a `target-schema/target-table` table named `schema.table` in the rules,

    a. If there is a rule matches `schema.table -> schema.table`, do nothing.
   
    b. If there is not rule matches `schema.table -> schema.table`, we think the config wants to mask this match, so we add a new rule `schema.table -> _no__exists__db_._no__exists__table_` to the table router. After that, sync-diff-inspector will regard table `schema.table` as table `_no__exists__db_._no__exists__table_` instead of itself.

* Given a `target-schema` only in the rules, such like,

```toml
[routes.rule1]
schema-pattern = "schema_*"  # schema to match. Support wildcard characters * and ?.
target-schema = "schema"     # target schema
```

a. If there is a rule matches `schema -> schema`, do nothing.

b. If there is not rule matches `schema -> schema`, we think the config wants to mask this match, so we add a new rule `schema -> _no__exists__db_` to the table router. After that, sync-diff-inspector will regard table `schema` as table `_no__exists__db_` instead of itself.

* Given `target-schema.target-table` does not exist in the rules, we add the rule `target-schema.target-table -> target-schema.target-table` to make it case-insensitive (that's because the table router is case-insensitive).

**Here are some examples:**

Suppose there are seven tables, which are `inspector_mysql_0.tb_emp1`, `Inspector_mysql_0.tb_emp1`, `inspector_mysql_0.Tb_emp1`, `inspector_mysql_1.tb_emp1`, `Inspector_mysql_1.tb_emp1`, `inspector_mysql_1.Tb_emp1` and `Inspector_mysql_1.Tb_emp1`.

In config, upstream has `Source.rule1`, and target table is `inspector_mysql_1.tb_emp1`.

* If we have the following config:

```toml
[Source.rule1]
schema-pattern = "inspector_mysql_0"
table-pattern = "tb_emp1"
target-schema = "inspector_mysql_1"
target-table = "tb_emp1"
```

`inspector_mysql_0.tb_emp1` is routed to `inspector_mysql_1.tb_emp1`,

`Inspector_mysql_0.tb_emp1` is routed to `inspector_mysql_1.tb_emp1`,

`inspector_mysql_0.Tb_emp1` is routed to `inspector_mysql_1.tb_emp1`,

`inspector_mysql_1.tb_emp1` is routed to `_no__exists__db_._no__exists__table_`,

`Inspector_mysql_1.tb_emp1` is routed to `_no__exists__db_._no__exists__table_`,

`inspector_mysql_1.Tb_emp1` is routed to `_no__exists__db_._no__exists__table_`,

`Inspector_mysql_1.Tb_emp1` is routed to `_no__exists__db_._no__exists__table_`.

* If we have the following config:

```toml
[Source.rule1]
schema-pattern = "inspector_mysql_0"
target-schema = "inspector_mysql_1"
```

`inspector_mysql_0.tb_emp1` is routed to `inspector_mysql_1.tb_emp1`,

`Inspector_mysql_0.tb_emp1` is routed to `inspector_mysql_1.tb_emp1`,

`inspector_mysql_0.Tb_emp1` is routed to `inspector_mysql_1.Tb_emp1`,

`inspector_mysql_1.tb_emp1` is routed to `_no__exists__db_._no__exists__table_`,

`Inspector_mysql_1.tb_emp1` is routed to `_no__exists__db_._no__exists__table_`,

`inspector_mysql_1.Tb_emp1` is routed to `_no__exists__db_._no__exists__table_`,

`Inspector_mysql_1.Tb_emp1` is routed to `_no__exists__db_._no__exists__table_`.

* If we have the following config:

```toml
[Source.rule1]
schema-pattern = "other_schema"
target-schema = "other_schema"
```

`inspector_mysql_0.tb_emp1` is routed to `inspector_mysql_0.tb_emp1`,

`Inspector_mysql_0.tb_emp1` is routed to `Inspector_mysql_0.tb_emp1`,

`inspector_mysql_0.Tb_emp1` is routed to `inspector_mysql_0.Tb_emp1`,

`inspector_mysql_1.tb_emp1` is routed to `inspector_mysql_1.tb_emp1`,

`Inspector_mysql_1.tb_emp1` is routed to `inspector_mysql_1.tb_emp1`,

`inspector_mysql_1.Tb_emp1` is routed to `inspector_mysql_1.tb_emp1`,

`Inspector_mysql_1.Tb_emp1` is routed to `inspector_mysql_1.tb_emp1`.

* If we have the following config:

```toml
[Source.rule1]
schema-pattern = "inspector_mysql_?"
table-pattern = "tb_emp1"
target-schema = "inspector_mysql_1"
target-table = "tb_emp1"
```

`inspector_mysql_0.tb_emp1` is routed to `inspector_mysql_1.tb_emp1`,

`Inspector_mysql_0.tb_emp1` is routed to `inspector_mysql_1.tb_emp1`,

`inspector_mysql_0.Tb_emp1` is routed to `inspector_mysql_1.tb_emp1`,

`inspector_mysql_1.tb_emp1` is routed to `inspector_mysql_1.tb_emp1`,

`Inspector_mysql_1.tb_emp1` is routed to `inspector_mysql_1.tb_emp1`,

`inspector_mysql_1.Tb_emp1` is routed to `inspector_mysql_1.tb_emp1`,

`Inspector_mysql_1.Tb_emp1` is routed to `inspector_mysql_1.tb_emp1`.

* If we do not have rules:

`inspector_mysql_0.tb_emp1` is routed to `inspector_mysql_0.tb_emp1`,

`Inspector_mysql_0.tb_emp1` is routed to `Inspector_mysql_0.tb_emp1`,

`inspector_mysql_0.Tb_emp1` is routed to `inspector_mysql_0.Tb_emp1`,

`inspector_mysql_1.tb_emp1` is routed to `inspector_mysql_1.tb_emp1`,

`Inspector_mysql_1.tb_emp1` is routed to `inspector_mysql_1.tb_emp1`,

`inspector_mysql_1.Tb_emp1` is routed to `inspector_mysql_1.tb_emp1`,

`Inspector_mysql_1.Tb_emp1` is routed to `inspector_mysql_1.tb_emp1`.
