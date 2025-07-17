---
title: SHOW PLUGINS
summary: 关于 TiDB 数据库中使用 SHOW PLUGINS 的概述。
---

# SHOW PLUGINS

`SHOW PLUGINS` 显示 TiDB 中所有已安装的插件，包括每个插件的状态和版本信息。

> **Note:**
>
> 该功能在 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

## Synopsis

```ebnf+diagram
ShowPluginsStmt ::=
    "SHOW" "PLUGINS" ShowLikeOrWhere?
```

## Examples

```sql
SHOW PLUGINS;
```

```
+-------+--------------+-------+-----------------------------+---------+---------+
| Name  | Status       | Type  | Library                     | License | Version |
+-------+--------------+-------+-----------------------------+---------+---------+
| audit | Ready-enable | Audit | /tmp/tidb/plugin/audit-1.so |         | 1       |
+-------+--------------+-------+-----------------------------+---------+---------+
1 row in set (0.000 sec)
```

```sql
SHOW PLUGINS LIKE 'a%';
```

```
+-------+--------------+-------+-----------------------------+---------+---------+
| Name  | Status       | Type  | Library                     | License | Version |
+-------+--------------+-------+-----------------------------+---------+---------+
| audit | Ready-enable | Audit | /tmp/tidb/plugin/audit-1.so |         | 1       |
+-------+--------------+-------+-----------------------------+---------+---------+
1 row in set (0.000 sec)
```

## MySQL compatibility

TiDB 中的 `SHOW PLUGINS` 语句与 MySQL 完全兼容。如果你发现任何兼容性差异，[请报告一个 bug](https://docs.pingcap.com/tidb/stable/support)。

## See also

- [`ADMIN PLUGINS`](/sql-statements/sql-statement-admin.md#admin-plugins-related-statement)