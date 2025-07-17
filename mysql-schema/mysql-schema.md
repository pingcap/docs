---
title: mysql Schema
summary: 了解 TiDB 系统表。
---

# `mysql` Schema

`mysql` schema 包含 TiDB 系统表。其设计类似于 MySQL 中的 `mysql` schema，例如 `mysql.user` 表可以直接编辑。它还包含一些对 MySQL 的扩展表。

> **Note:**
>
> 在大多数场景下，不建议直接使用 `INSERT`、`UPDATE` 或 `DELETE` 修改系统表内容。应使用 [`CREATE USER`](/sql-statements/sql-statement-create-user.md)、[`ALTER USER`](/sql-statements/sql-statement-alter-user.md)、[`DROP USER`](/sql-statements/sql-statement-drop-user.md)、[`GRANT`](/sql-statements/sql-statement-grant-privileges.md)、[`REVOKE`](/sql-statements/sql-statement-revoke-privileges.md) 和 [`SHOW CREATE USER`](/sql-statements/sql-statement-show-create-user.md) 等语句来管理用户和权限。如果必须直接修改系统表，请使用 [`FLUSH PRIVILEGES`](/sql-statements/sql-statement-flush-privileges.md) 使更改生效。

## Grant system tables

这些系统表包含关于用户账户及其权限的授权信息：

- [`user`](/mysql-schema/mysql-schema-user.md): 用户账户、全局权限及其他非权限列
- `db`: 数据库级权限
- `tables_priv`: 表级权限
- `columns_priv`: 列级权限
- `password_history`: 密码变更历史
- `default_roles`: 用户的默认角色
- `global_grants`: 动态权限
- `global_priv`: 基于证书的认证信息
- `role_edges`: 角色之间的关系

## Cluster status system tables

* `tidb` 表包含一些关于 TiDB 的全局信息：

    * `bootstrapped`: TiDB 集群是否已初始化。注意，该值为只读，不能修改。
    * `tidb_server_version`: TiDB 初始化时的版本信息。注意，该值为只读，不能修改。
    * `system_tz`: TiDB 的系统时区。
    * `new_collation_enabled`: TiDB 是否启用了 [新框架的字符集排序](/character-set-and-collation.md#new-framework-for-collations)。注意，该值为只读，不能修改。

## Server-side help system tables

目前，`help_topic` 为空。

## Statistics system tables

- `stats_buckets`: 统计信息的桶
- `stats_histograms`: 统计信息的直方图
- `stats_top_n`: 统计信息的 TopN
- `stats_meta`: 表的元数据信息，如总行数和已更新行数
- `stats_extended`: 扩展统计信息，如列之间的相关性
- `stats_feedback`: 统计信息的查询反馈
- `stats_fm_sketch`: 统计列直方图的 FMSketch 分布
- `stats_table_locked`: 被锁定的统计信息
- `stats_meta_history`: 历史统计信息中的元数据信息
- `stats_history`: 历史统计信息中的其他信息
- `analyze_options`: 每个表的默认 `analyze` 选项
- `column_stats_usage`: 列统计信息的使用情况
- `analyze_jobs`: 正在进行的统计采集任务和过去 7 天内的历史任务记录

## Execution plan-related system tables

- `bind_info`: 执行计划的绑定信息
- `capture_plan_baselines_blacklist`: 执行计划自动绑定的黑名单

## System tables related to PLAN REPLAYER

- `plan_replayer_status`: 用户注册的 [`PLAN REPLAYER CAPTURE`](https://docs.pingcap.com/tidb/stable/sql-plan-replayer#use-plan-replayer-capture) 任务
- `plan_replayer_task`: [`PLAN REPLAYER CAPTURE`](https://docs.pingcap.com/tidb/stable/sql-plan-replayer#use-plan-replayer-capture) 任务的结果

## GC worker system tables

> **Note:**
>
> GC worker 系统表仅适用于 TiDB 自托管，不在 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/) 上提供。

- `gc_delete_range`: 待删除的 KV 范围
- `gc_delete_range_done`: 已删除的 KV 范围

## System tables related to cached tables

- `table_cache_meta` 存储缓存表的元数据。

## TTL related system tables

* `tidb_ttl_table_status`: 所有 TTL 表之前执行的 TTL 作业和正在进行的 TTL 作业
* `tidb_ttl_task`: 当前进行中的 TTL 子任务
* `tidb_ttl_job_history`: 过去 90 天内 TTL 任务的执行历史

## System tables related to runaway queries

* `tidb_runaway_queries`: 过去 7 天内所有识别为 runaway 查询的历史记录
* `tidb_runaway_watch`: runaway 查询的监控列表
* `tidb_runaway_watch_done`: 已删除或过期的 runaway 查询监控列表

## System tables related to metadata locks

* [`tidb_mdl_view`](/mysql-schema/mysql-schema-tidb-mdl-view.md): 元数据锁的视图。你可以用它查看当前阻塞的 DDL 语句信息。另请参见 [Metadata Lock](/metadata-lock.md)。
* `tidb_mdl_info`: TiDB 内部用来在节点间同步元数据锁的信息。

## System tables related to DDL statements

* `tidb_ddl_history`: DDL 语句的历史记录
* `tidb_ddl_job`: 当前由 TiDB 执行的 DDL 语句的元数据
* `tidb_ddl_reorg`: 当前由 TiDB 执行的物理 DDL 语句（如添加索引）的元数据

## System tables related to TiDB Distributed eXecution Framework (DXF)

* `dist_framework_meta`: 分布式执行框架（DXF）任务调度器的元数据
* `tidb_global_task`: 当前 DXF 任务的元数据
* `tidb_global_task_history`: 历史 DXF 任务的元数据，包括成功和失败的任务
* `tidb_background_subtask`: 当前 DXF 子任务的元数据
* `tidb_background_subtask_history`: 历史 DXF 子任务的元数据

## System tables related to Resource Control

* `request_unit_by_group`: 所有资源组的资源单元（RU）消耗历史记录

## System tables related to backup and restore

* `tidb_pitr_id_map`: 点-in-时间恢复（PITR）操作的 ID 映射信息

## Miscellaneous system tables

<CustomContent platform="tidb">

> **Note:**
>
> `tidb`、`expr_pushdown_blacklist`、`opt_rule_blacklist`、`table_cache_meta`、`tidb_import_jobs` 和 `tidb_timers` 系统表仅适用于 TiDB 自托管，不在 [TiDB Cloud](https://docs.pingcap.com/tidbcloud/) 上提供。

- `GLOBAL_VARIABLES`: 全局系统变量表
- `expr_pushdown_blacklist`: 表达式下推的黑名单
- `opt_rule_blacklist`: 逻辑优化规则的黑名单
- `tidb_import_jobs`: [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 任务信息
- `tidb_timers`: 内部定时器的元数据
- `advisory_locks`: 与 [Locking functions](/functions-and-operators/locking-functions.md) 相关的信息

</CustomContent>

<CustomContent platform="tidb-cloud">

- `GLOBAL_VARIABLES`: 全局系统变量表

</CustomContent>