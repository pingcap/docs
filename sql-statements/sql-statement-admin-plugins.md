---
title: ADMIN | TiDB SQL Statement Reference
summary: An overview of the usage of ADMIN for the TiDB database.
category: reference
---

# ADMIN

TODO

## Synopsis

TODO

## Examples

## `ADMIN PLUGINS` related statement

{{< copyable "sql" >}}

```sql
ADMIN PLUGINS ENABLE plugin_name [, plugin_name] ...;
```

The above statement is used to enable the `plugin_name` plugin.

{{< copyable "sql" >}}

```sql
ADMIN PLUGINS DISABLE plugin_name [, plugin_name] ...;
```

The above statement is used to disable the `plugin_name` plugin.

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* 