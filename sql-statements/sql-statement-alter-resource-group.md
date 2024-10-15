---
title: ALTER RESOURCE GROUP
summary: Learn the usage of ALTER RESOURCE GROUP in TiDB.
---

# ALTER RESOURCE GROUP

The `ALTER RESOURCE GROUP` statement is used to modify a resource group in a database.

> **Note:**
>
> This feature is not available on [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) clusters.

## Synopsis

```ebnf+diagram
AlterResourceGroupStmt ::=
   "ALTER" "RESOURCE" "GROUP" IfExists ResourceGroupName ResourceGroupOptionList

IfExists ::=
    ('IF' 'EXISTS')?

ResourceGroupName ::=
    Identifier
|   "DEFAULT"

ResourceGroupOptionList ::=
    DirectResourceGroupOption
|   ResourceGroupOptionList DirectResourceGroupOption
|   ResourceGroupOptionList ',' DirectResourceGroupOption

DirectResourceGroupOption ::=
    "RU_PER_SEC" EqOpt LengthNum
|   "PRIORITY" EqOpt ResourceGroupPriorityOption
|   "BURSTABLE"
|   "BURSTABLE" EqOpt Boolean
|   "QUERY_LIMIT" EqOpt '(' ResourceGroupRunawayOptionList ')'
|   "QUERY_LIMIT" EqOpt '(' ')'
|   "QUERY_LIMIT" EqOpt "NULL"
|   "BACKGROUND" EqOpt '(' BackgroundOptionList ')'
|   "BACKGROUND" EqOpt '(' ')'
|   "BACKGROUND" EqOpt "NULL"

ResourceGroupPriorityOption ::=
    LOW
|   MEDIUM
|   HIGH

ResourceGroupRunawayOptionList ::=
    DirectResourceGroupRunawayOption
|   ResourceGroupRunawayOptionList DirectResourceGroupRunawayOption
|   ResourceGroupRunawayOptionList ',' DirectResourceGroupRunawayOption

DirectResourceGroupRunawayOption ::=
    "EXEC_ELAPSED" EqOpt stringLit
|   "ACTION" EqOpt ResourceGroupRunawayActionOption
|   "WATCH" EqOpt ResourceGroupRunawayWatchOption "DURATION" EqOpt stringLit

ResourceGroupRunawayWatchOption ::=
    EXACT
|   SIMILAR

ResourceGroupRunawayActionOption ::=
    DRYRUN
|   COOLDOWN
|   KILL

BackgroundOptionList ::=
    DirectBackgroundOption
|   BackgroundOptionList DirectBackgroundOption
|   BackgroundOptionList ',' DirectBackgroundOption

DirectBackgroundOption ::=
    "TASK_TYPES" EqOpt stringLit
|   "UTILIZATION_LIMIT" EqOpt LengthNum
```

TiDB supports the following `DirectResourceGroupOption`, where [Request Unit (RU)](/tidb-resource-control.md#what-is-request-unit-ru) is a unified abstraction unit in TiDB for CPU, IO, and other system resources.

| Option     | Description                         | Example                |
|---------------|-------------------------------------|------------------------|
| `RU_PER_SEC` | Rate of RU backfilling per second | `RU_PER_SEC = 500` indicates that this resource group is backfilled with 500 RUs per second |
| `PRIORITY`    | The absolute priority of tasks to be processed on TiKV  | `PRIORITY = HIGH` indicates that the priority is high. If not specified, the default value is `MEDIUM`. |
| `BURSTABLE`   | If the `BURSTABLE` attribute is set, TiDB allows the corresponding resource group to use the available system resources when the quota is exceeded. |
| `QUERY_LIMIT` | When the query execution meets this condition, the query is identified as a runaway query and the corresponding action is executed. | `QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=KILL, WATCH=EXACT DURATION='10m')` indicates that the query is identified as a runaway query when the execution time exceeds 60 seconds. The query is terminated. All SQL statements with the same SQL text will be terminated immediately in the coming 10 minutes. `QUERY_LIMIT=()` or `QUERY_LIMIT=NULL` means that runaway control is not enabled. See [Runaway Queries](/tidb-resource-control.md#manage-queries-that-consume-more-resources-than-expected-runaway-queries). |
| `BACKGROUND`  | Configure the background tasks. For more details, see [Manage background tasks](/tidb-resource-control.md#manage-background-tasks). | `BACKGROUND=(TASK_TYPES="br,stats", UTILIZATION_LIMIT=30)` indicates that the backup and restore and statistics collection related tasks are scheduled as background tasks, and background tasks can consume 30% of the TiKV resources at most. |

> **Note:**
>
> - The `ALTER RESOURCE GROUP` statement can only be executed when the global variable [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660) is set to `ON`.
> - The `ALTER RESOURCE GROUP` statement supports incremental changes, leaving unspecified parameters unchanged. However, both `QUERY_LIMIT` and `BACKGROUND` are used as a whole and cannot be partially modified.
> - Currently, only the `default` resource group supports modifying the `BACKGROUND` configuration.

## Examples

Create a resource group named `rg1` and modify its properties.

```sql
DROP RESOURCE GROUP IF EXISTS rg1;
```

```
Query OK, 0 rows affected (0.22 sec)
```

```sql
CREATE RESOURCE GROUP IF NOT EXISTS rg1
  RU_PER_SEC = 100
  BURSTABLE;
```

```sql
Query OK, 0 rows affected (0.08 sec)
```

```sql
SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1';
```

```sql
+------+------------+----------+-----------+-------------+------------+
| NAME | RU_PER_SEC | PRIORITY | BURSTABLE | QUERY_LIMIT | BACKGROUND |
+------+------------+----------+-----------+-------------+------------+
| rg1  | 100        | MEDIUM   | NO        | NULL        | NULL       |
+------+------------+----------+-----------+-------------+------------+
1 rows in set (1.30 sec)
```

```sql
ALTER RESOURCE GROUP rg1
  RU_PER_SEC = 200
  PRIORITY = LOW
  QUERY_LIMIT = (EXEC_ELAPSED='1s' ACTION=COOLDOWN WATCH=EXACT DURATION '30s');
```

```sql
Query OK, 0 rows affected (0.08 sec)
```

```sql
SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1';
```

```sql
+------+------------+----------+-----------+----------------------------------------------------------------+------------+
| NAME | RU_PER_SEC | PRIORITY | BURSTABLE | QUERY_LIMIT                                                    | BACKGROUND |
+------+------------+----------+-----------+----------------------------------------------------------------+------------+
| rg1  | 200        | LOW      | NO        | EXEC_ELAPSED='1s', ACTION=COOLDOWN, WATCH=EXACT DURATION='30s' | NULL       |
+------+------------+----------+-----------+----------------------------------------------------------------+------------+
1 rows in set (1.30 sec)
```

Modify the `BACKGROUND` option for the `default` resource group.

```sql
ALTER RESOURCE GROUP default BACKGROUND = (TASK_TYPES = "br,ddl", UTILIZATION_LIMIT=30);
```

```sql
Query OK, 0 rows affected (0.08 sec)
```

```sql
SELECT * FROM information_schema.resource_groups WHERE NAME ='default';
```

```sql
+---------+------------+----------+-----------+-------------+-------------------------------------------+
| NAME    | RU_PER_SEC | PRIORITY | BURSTABLE | QUERY_LIMIT | BACKGROUND                                |
+---------+------------+----------+-----------+-------------+-------------------------------------------+
| default | UNLIMITED  | MEDIUM   | YES       | NULL        | TASK_TYPES='br,ddl', UTILIZATION_LIMIT=30 |
+---------+------------+----------+-----------+-------------+-------------------------------------------+
1 rows in set (1.30 sec)
```

## MySQL compatibility

MySQL also supports [ALTER RESOURCE GROUP](https://dev.mysql.com/doc/refman/8.0/en/alter-resource-group.html). However, the acceptable parameters are different from that of TiDB so that they are not compatible.

## See also

* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
* [CREATE RESOURCE GROUP](/sql-statements/sql-statement-create-resource-group.md)
* [Request Unit (RU)](/tidb-resource-control.md#what-is-request-unit-ru)
