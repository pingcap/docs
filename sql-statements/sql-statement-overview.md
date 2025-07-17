---
title: SQL 语句概述
summary: 了解 TiDB 支持的 SQL 语句。
---

# SQL 语句概述

TiDB 使用的 SQL 语句旨在遵循 ISO/IEC SQL 标准，并在必要时扩展支持 MySQL 和 TiDB 特有的语句。

## 模式管理 / 数据定义语言（DDL）语句

| SQL 语句 | 描述 |
|---------------|-------------|
| [`ALTER DATABASE`](/sql-statements/sql-statement-alter-database.md) | 修改数据库。 |
| [`ALTER SEQUENCE`](/sql-statements/sql-statement-alter-sequence.md) | 修改序列。 |
| [`ALTER TABLE ... ADD COLUMN`](/sql-statements/sql-statement-add-column.md) | 向现有表添加列。 |
| [`ALTER TABLE ... ADD INDEX`](/sql-statements/sql-statement-add-index.md) | 向现有表添加索引。 |
| [`ALTER TABLE ... ALTER INDEX`](/sql-statements/sql-statement-alter-index.md) | 更改索引定义。 |
| [`ALTER TABLE ... CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md) | 更改列定义。 |
| [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md) | 压缩表。 |
| [`ALTER TABLE ... DROP COLUMN`](/sql-statements/sql-statement-drop-column.md) | 从表中删除列。 |
| [`ALTER TABLE ... MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md) | 修改列定义。 |
| [`ALTER TABLE ... RENAME INDEX`](/sql-statements/sql-statement-rename-index.md) | 重命名索引。 |
| [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md) | 修改表定义。 |
| [`CREATE DATABASE`](/sql-statements/sql-statement-create-database.md) | 创建新数据库。 |
| [`CREATE INDEX`](/sql-statements/sql-statement-create-index.md) | 在表上创建新索引。 |
| [`CREATE SEQUENCE`](/sql-statements/sql-statement-create-sequence.md) | 创建新序列对象。 |
| [`CREATE TABLE LIKE`](/sql-statements/sql-statement-create-table-like.md) | 复制现有表的定义（不复制数据）。 |
| [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) | 创建新表。 |
| [`CREATE VIEW`](/sql-statements/sql-statement-create-view.md) | 创建新视图。 |
| [`DROP DATABASE`](/sql-statements/sql-statement-drop-database.md) | 删除已存在的数据库。 |
| [`DROP INDEX`](/sql-statements/sql-statement-drop-index.md) | 从表中删除索引。 |
| [`DROP SEQUENCE`](/sql-statements/sql-statement-drop-sequence.md) | 删除序列对象。 |
| [`DROP TABLE`](/sql-statements/sql-statement-drop-table.md) | 删除已存在的表。 |
| [`DROP VIEW`](/sql-statements/sql-statement-drop-view.md) | 删除已存在的视图。 |
| [`RENAME TABLE`](/sql-statements/sql-statement-rename-table.md) | 重命名表。 |
| [`SHOW COLUMNS FROM`](/sql-statements/sql-statement-show-columns-from.md) | 显示表的列信息。 |
| [`SHOW CREATE DATABASE`](/sql-statements/sql-statement-show-create-database.md) | 显示数据库的 CREATE 语句。 |
| [`SHOW CREATE SEQUENCE`](/sql-statements/sql-statement-show-create-sequence.md) | 显示序列的 CREATE 语句。 |
| [`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md) | 显示表的 CREATE 语句。 |
| [`SHOW DATABASES`](/sql-statements/sql-statement-show-databases.md) | 显示当前用户有权限的数据库列表。 |
| [`SHOW FIELDS FROM`](/sql-statements/sql-statement-show-fields-from.md) | 显示表的列信息。 |
| [`SHOW INDEXES`](/sql-statements/sql-statement-show-indexes.md) | 显示表的索引信息。 |
| [`SHOW SCHEMAS`](/sql-statements/sql-statement-show-schemas.md) | `SHOW DATABASES` 的别名，显示当前用户有权限的数据库列表。 |
| [`SHOW TABLE NEXT_ROW_ID`](/sql-statements/sql-statement-show-table-next-rowid.md) | 显示表的下一个行 ID。 |
| [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md) | 显示 TiDB 中表的 Region 信息。 |
| [`SHOW TABLE STATUS`](/sql-statements/sql-statement-show-table-status.md) | 显示 TiDB 中表的各种统计信息。 |
| [`SHOW TABLES`](/sql-statements/sql-statement-show-tables.md) | 显示数据库中的表。 |
| [`TRUNCATE`](/sql-statements/sql-statement-truncate.md) | 清空表中的所有数据。 |

## 数据操作语言（DML）语句

| SQL 语句 | 描述 |
|---------------|-------------|
| [`BATCH`](/sql-statements/sql-statement-batch.md) | 将 DML 语句拆分成多个语句在 TiDB 中执行。 |
| [`DELETE`](/sql-statements/sql-statement-delete.md) | 删除表中的行。 |
| [`INSERT`](/sql-statements/sql-statement-insert.md) | 向表中插入新行。 |
| [`REPLACE`](/sql-statements/sql-statement-replace.md) | 替换已存在的行或插入新行。 |
| [`SELECT`](/sql-statements/sql-statement-select.md) | 从表中读取数据。 |
| [`TABLE`](/sql-statements/sql-statement-table.md) | 获取表中的行。 |
| [`UPDATE`](/sql-statements/sql-statement-update.md) | 更新表中的已存在行。 |
| [`WITH`](/sql-statements/sql-statement-with.md) | 定义公共表表达式。 |

## 事务语句

| SQL 语句 | 描述 |
|---------------|-------------|
| [`BEGIN`](/sql-statements/sql-statement-begin.md) | 开始一个新事务。 |
| [`COMMIT`](/sql-statements/sql-statement-commit.md) | 提交当前事务。 |
| [`ROLLBACK`](/sql-statements/sql-statement-rollback.md) | 回滚当前事务。 |
| [`SAVEPOINT`](/sql-statements/sql-statement-savepoint.md) | 在事务中设置保存点。 |
| [`SET TRANSACTION`](/sql-statements/sql-statement-set-transaction.md) | 改变当前的隔离级别（`GLOBAL` 或 `SESSION` 级别）。 |
| [`START TRANSACTION`](/sql-statements/sql-statement-start-transaction.md) | 启动一个新事务。 |

## 预处理语句

| SQL 语句 | 描述 |
|---------------|-------------|
| [`DEALLOCATE`](/sql-statements/sql-statement-deallocate.md) | 取消预处理语句，释放相关资源。 |
| [`EXECUTE`](/sql-statements/sql-statement-execute.md) | 使用特定参数值执行预处理语句。 |
| [`PREPARE`](/sql-statements/sql-statement-prepare.md) | 创建带有占位符的预处理语句。 |

## 管理员语句

<CustomContent platform="tidb">

| SQL 语句 | 描述 |
|---------------|-------------|
| [`ADMIN ALTER DDL JOBS`](/sql-statements/sql-statement-admin-alter-ddl.md) | 修改单个正在运行的 DDL 任务参数。 |
| [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md) | 取消 DDL 任务。 |
| [`ADMIN CHECK [TABLE\|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) | 检查表或索引的完整性。 |
| [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md) | 计算表的校验和。 |
| [`ADMIN CLEANUP INDEX`](/sql-statements/sql-statement-admin-cleanup.md) | 清理表中的索引。 |
| [`ADMIN PAUSE DDL`](/sql-statements/sql-statement-admin-pause-ddl.md) | 暂停 DDL 操作。 |
| [`ADMIN RESUME DDL`](/sql-statements/sql-statement-admin-resume-ddl.md) | 恢复 DDL 操作。 |
| [`ADMIN SHOW DDL [JOBS\|JOB QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md) | 显示 DDL 任务或任务查询。 |
| [`ADMIN`](/sql-statements/sql-statement-admin.md) | 执行各种管理任务。 |
| [`FLUSH TABLES`](/sql-statements/sql-statement-flush-tables.md) |  包含于 [MySQL 兼容性](/mysql-compatibility.md)。在 TiDB 中没有实际用途。 |
| [`SET <variable>`](/sql-statements/sql-statement-set-variable.md) | 修改系统变量或用户变量。 |
| [`SET [NAMES\|CHARACTER SET]`](/sql-statements/sql-statement-set-names.md) | 设置字符集和校对规则。 |
| [`SPLIT REGION`](/sql-statements/sql-statement-split-region.md) | 将 Region 分割成更小的 Region。 |

</CustomContent>

<CustomContent platform="tidb-cloud">

| SQL 语句 | 描述 |
|---------------|-------------|
| [`ADMIN ALTER DDL JOBS`](/sql-statements/sql-statement-admin-alter-ddl.md) | 修改单个正在运行的 DDL 任务参数。 |
| [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md) | 取消 DDL 任务。 |
| [`ADMIN CHECK [TABLE\|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) | 检查表或索引的完整性。 |
| [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md) | 计算表的校验和。 |
| [`ADMIN CLEANUP INDEX`](/sql-statements/sql-statement-admin-cleanup.md) | 清理表中的索引。 |
| [`ADMIN PAUSE DDL`](/sql-statements/sql-statement-admin-pause-ddl.md) | 暂停 DDL 操作。 |
| [`ADMIN RECOVER INDEX`](/sql-statements/sql-statement-admin-recover.md) | 根据冗余索引恢复一致性。 |
| [`ADMIN RESUME DDL`](/sql-statements/sql-statement-admin-resume-ddl.md) | 恢复 DDL 操作。 |
| [`ADMIN SHOW DDL [JOBS\|JOB QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md) | 显示 DDL 任务或任务查询。 |
| [`ADMIN`](/sql-statements/sql-statement-admin.md) | 执行各种管理任务。 |
| [`FLUSH TABLES`](/sql-statements/sql-statement-flush-tables.md) |  包含于 [MySQL 兼容性](/mysql-compatibility.md)。在 TiDB 中没有实际用途。 |
| [`SET <variable>`](/sql-statements/sql-statement-set-variable.md) | 修改系统变量或用户变量。 |
| [`SET [NAMES\|CHARACTER SET]`](/sql-statements/sql-statement-set-names.md) | 设置字符集和校对规则。 |
| [`SPLIT REGION`](/sql-statements/sql-statement-split-region.md) | 将 Region 分割成更小的 Region。 |

</CustomContent>

## 数据导入与导出

| SQL 语句 | 描述 |
|---------------|-------------|
| [`CANCEL IMPORT JOB`](/sql-statements/sql-statement-cancel-import-job.md) | 取消正在进行的导入任务。 |
| [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) | 通过 TiDB Lightning 的 [Physical Import Mode](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode) 将数据导入表中。 |
| [`LOAD DATA`](/sql-statements/sql-statement-load-data.md) | 从 Amazon S3 或 Google Cloud Storage 加载数据到表中。 |
| [`SHOW IMPORT JOB`](/sql-statements/sql-statement-show-import-job.md) | 显示导入任务的状态。 |

## 备份与还原

| SQL 语句 | 描述 |
|---------------|-------------|
| [`BACKUP`](/sql-statements/sql-statement-backup.md) | 执行 TiDB 集群的分布式备份。 |
| [`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md) | 将集群还原到某个快照。 |
| [`FLASHBACK DATABASE`](/sql-statements/sql-statement-flashback-database.md) | 还原被 `DROP` 语句删除的数据库及其数据。 |
| [`FLASHBACK TABLE`](/sql-statements/sql-statement-flashback-table.md) | 还原被 `DROP` 或 `TRUNCATE` 操作删除的表和数据。 |
| [`RECOVER TABLE`](/sql-statements/sql-statement-recover-table.md) | 还原被删除的表及其数据。 |
| [`RESTORE`](/sql-statements/sql-statement-restore.md) | 从备份中还原数据库。 |
| [`SHOW BACKUPS`](/sql-statements/sql-statement-show-backups.md) | 显示备份任务。 |
| [`SHOW RESTORES`](/sql-statements/sql-statement-show-backups.md) | 显示还原任务。 |

## 放置策略

| SQL 语句 | 描述 |
|---------------|-------------|
| [`ALTER PLACEMENT POLICY`](/sql-statements/sql-statement-alter-placement-policy.md) | 修改放置策略。 |
| [`ALTER RANGE`](/sql-statements/sql-statement-alter-range.md) | 修改放置策略的范围。 |
| [`CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-create-placement-policy.md) | 创建新的放置策略。 |
| [`DROP PLACEMENT POLICY`](/sql-statements/sql-statement-drop-placement-policy.md) | 删除已有的放置策略。 |
| [`SHOW CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-show-create-placement-policy.md) | 显示放置策略的 `CREATE` 语句。 |
| [`SHOW PLACEMENT FOR`](/sql-statements/sql-statement-show-placement-for.md) | 显示特定表的放置规则。 |
| [`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md) | 显示可用的放置标签。 |
| [`SHOW PLACEMENT`](/sql-statements/sql-statement-show-placement.md) | 显示放置规则。 |

## 资源组

<CustomContent platform="tidb">

| SQL 语句 | 描述 |
|---------------|-------------|
| [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md) | 修改资源组。 |
| [`CALIBRATE RESOURCE`](/sql-statements/sql-statement-calibrate-resource.md) | 估算并输出当前集群的 [Request Unit (RU)](/tidb-resource-control-ru-groups.md#what-is-request-unit-ru) 容量。 |
| [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md) | 创建新的资源组。 |
| [`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md) | 删除资源组。 |
| [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md) | 管理超时查询监控列表。 |
| [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) | 设置资源组。 |
| [`SHOW CREATE RESOURCE GROUP`](/sql-statements/sql-statement-show-create-resource-group.md) | 显示资源组的 `CREATE` 语句。 |

</CustomContent>

<CustomContent platform="tidb-cloud">

| SQL 语句 | 描述 |
|---------------|-------------|
| [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md) | 修改资源组。 |
| [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md) | 创建新的资源组。 |
| [`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md) | 删除资源组。 |
| [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md) | 管理超时查询监控列表。 |
| [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) | 设置资源组。 |
| [`SHOW CREATE RESOURCE GROUP`](/sql-statements/sql-statement-show-create-resource-group.md) | 显示资源组的 `CREATE` 语句。 |

</CustomContent>

## 实用语句

| SQL 语句 | 描述 |
|---------------|-------------|
| [`DESC`](/sql-statements/sql-statement-desc.md) | `DESCRIBE` 的别名，显示表的结构。 |
| [`DESCRIBE`](/sql-statements/sql-statement-describe.md) | 显示表的结构。 |
| [`DO`](/sql-statements/sql-statement-do.md) | 执行表达式但不返回任何结果。 |
| [`EXPLAIN`](/sql-statements/sql-statement-explain.md) | 显示查询的执行计划。 |
| [`TRACE`](/sql-statements/sql-statement-trace.md) | 提供查询执行的详细信息。 |
| [`USE`](/sql-statements/sql-statement-use.md) | 设置当前使用的数据库。 |

## 显示语句

<CustomContent platform="tidb">

| SQL 语句 | 描述 |
|---------------|-------------|
| [`SHOW BUILTINS`](/sql-statements/sql-statement-show-builtins.md) | 列出内置函数。 |
| [`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md) | 列出字符集。 |
| [`SHOW COLLATIONS`](/sql-statements/sql-statement-show-collation.md) | 列出校对规则。 |
| [`SHOW ERRORS`](/sql-statements/sql-statement-show-errors.md) | 显示之前执行语句的错误。 |
| [`SHOW STATUS`](/sql-statements/sql-statement-show-status.md) |  包含于 [MySQL 兼容性](/mysql-compatibility.md)。TiDB 使用 [Prometheus 和 Grafana](/tidb-monitoring-framework.md) 进行集中指标采集，大部分指标不使用 `SHOW STATUS`。 |
| [`SHOW VARIABLES`](/sql-statements/sql-statement-show-variables.md) | 显示系统变量。 |
| [`SHOW WARNINGS`](/sql-statements/sql-statement-show-warnings.md) | 显示之前执行语句的警告和备注。 |

</CustomContent>

<CustomContent platform="tidb-cloud">

| SQL 语句 | 描述 |
|---------------|-------------|
| [`SHOW BUILTINS`](/sql-statements/sql-statement-show-builtins.md) | 列出内置函数。 |
| [`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md) | 列出字符集。 |
| [`SHOW COLLATIONS`](/sql-statements/sql-statement-show-collation.md) | 列出校对规则。 |
| [`SHOW ERRORS`](/sql-statements/sql-statement-show-errors.md) | 显示之前执行语句的错误。 |
| [`SHOW STATUS`](/sql-statements/sql-statement-show-status.md) |  包含于 [MySQL 兼容性](/mysql-compatibility.md)。TiDB Cloud 提供 [Monitoring](/tidb-cloud/monitor-tidb-cluster.md) 进行集中指标采集，大部分指标不使用 `SHOW STATUS`。 |
| [`SHOW VARIABLES`](/sql-statements/sql-statement-show-variables.md) | 显示系统变量。 |
| [`SHOW WARNINGS`](/sql-statements/sql-statement-show-warnings.md) | 显示之前执行语句的警告和备注。 |

</CustomContent>

## 实例管理

<CustomContent platform="tidb">

| SQL 语句 | 描述 |
|---------------|-------------|
| [`ALTER INSTANCE`](/sql-statements/sql-statement-alter-instance.md) | 修改实例。 |
| [`FLUSH STATUS`](/sql-statements/sql-statement-flush-status.md) |  包含于 [MySQL 兼容性](/mysql-compatibility.md)。TiDB 使用 [Prometheus 和 Grafana](/tidb-monitoring-framework.md) 进行集中指标采集，大部分指标不使用 `SHOW STATUS`。 |
| [`KILL`](/sql-statements/sql-statement-kill.md) | 终止当前 TiDB 集群中任何实例的连接。 |
| [`SHOW CONFIG`](/sql-statements/sql-statement-show-config.md) | 显示 TiDB 各组件的配置。 |
| [`SHOW ENGINES`](/sql-statements/sql-statement-show-engines.md) | 显示可用的存储引擎。 |
| [`SHOW PLUGINS`](/sql-statements/sql-statement-show-plugins.md) | 显示已安装的插件。 |
| [`SHOW PROCESSLIST`](/sql-statements/sql-statement-show-processlist.md) | 显示当前连接到同一 TiDB 服务器的会话。 |
| [`SHOW PROFILES`](/sql-statements/sql-statement-show-profiles.md) |  包含于 [MySQL 兼容性](/mysql-compatibility.md)。目前仅返回空结果。 |
| [`SHUTDOWN`](/sql-statements/sql-statement-shutdown.md) | 停止客户端连接的 TiDB 实例，不是停止整个 TiDB 集群。 |

</CustomContent>

<CustomContent platform="tidb-cloud">

| SQL 语句 | 描述 |
|---------------|-------------|
| [`ALTER INSTANCE`](/sql-statements/sql-statement-alter-instance.md) | 修改实例。 |
| [`FLUSH STATUS`](/sql-statements/sql-statement-flush-status.md) |  包含于 [MySQL 兼容性](/mysql-compatibility.md)。TiDB Cloud 提供 [Monitoring](/tidb-cloud/monitor-tidb-cluster.md) 进行集中指标采集，大部分指标不使用 `SHOW STATUS`。 |
| [`KILL`](/sql-statements/sql-statement-kill.md) | 终止当前 TiDB 集群中任何实例的连接。 |
| [`SHOW ENGINES`](/sql-statements/sql-statement-show-engines.md) | 显示可用的存储引擎。 |
| [`SHOW PLUGINS`](/sql-statements/sql-statement-show-plugins.md) | 显示已安装的插件。 |
| [`SHOW PROCESSLIST`](/sql-statements/sql-statement-show-processlist.md) | 显示当前连接到同一 TiDB 服务器的会话。 |
| [`SHOW PROFILES`](/sql-statements/sql-statement-show-profiles.md) | 显示查询配置文件。  包含于 [MySQL 兼容性](/mysql-compatibility.md)。目前仅返回空结果。 |

</CustomContent>

## 锁定语句

| SQL 语句 | 描述 |
|---------------|-------------|
| [`LOCK STATS`](/sql-statements/sql-statement-lock-stats.md) | 锁定表或分区的统计信息。 |
| [`LOCK TABLES`](/sql-statements/sql-statement-lock-tables-and-unlock-tables.md) | 锁定当前会话的表。 |
| [`UNLOCK STATS`](/sql-statements/sql-statement-unlock-stats.md) | 解锁表或分区的统计信息。 |
| [`UNLOCK TABLES`](/sql-statements/sql-statement-lock-tables-and-unlock-tables.md) | 解锁表。 |

## 账户管理 / 数据控制语言（DCL）

| SQL 语句 | 描述 |
|---------------|-------------|
| [`ALTER USER`](/sql-statements/sql-statement-alter-user.md) | 修改用户。 |
| [`CREATE ROLE`](/sql-statements/sql-statement-create-role.md) | 创建角色。 |
| [`CREATE USER`](/sql-statements/sql-statement-create-user.md) | 创建新用户。 |
| [`DROP ROLE`](/sql-statements/sql-statement-drop-role.md) | 删除已有角色。 |
| [`DROP USER`](/sql-statements/sql-statement-drop-user.md) | 删除已有用户。 |
| [`FLUSH PRIVILEGES`](/sql-statements/sql-statement-flush-privileges.md) | 重新加载权限表中的权限到内存副本。 |
| [`GRANT <privileges>`](/sql-statements/sql-statement-grant-privileges.md) | 授予权限。 |
| [`GRANT <role>`](/sql-statements/sql-statement-grant-role.md) | 授予角色。 |
| [`RENAME USER`](/sql-statements/sql-statement-rename-user.md) | 重命名已有用户。 |
| [`REVOKE <privileges>`](/sql-statements/sql-statement-revoke-privileges.md) | 撤销权限。 |
| [`REVOKE <role>`](/sql-statements/sql-statement-revoke-role.md) | 撤销角色。 |
| [`SET DEFAULT ROLE`](/sql-statements/sql-statement-set-default-role.md) | 设置默认角色。 |
| [`SET PASSWORD`](/sql-statements/sql-statement-set-password.md) | 修改密码。 |
| [`SET ROLE`](/sql-statements/sql-statement-set-role.md) | 在当前会话中启用角色。 |
| [`SHOW CREATE USER`](/sql-statements/sql-statement-show-create-user.md) | 显示用户的 `CREATE` 语句。 |
| [`SHOW GRANTS`](/sql-statements/sql-statement-show-grants.md) | 显示与用户相关的权限。 |
| [`SHOW PRIVILEGES`](/sql-statements/sql-statement-show-privileges.md) | 显示可用的权限。 |

## TiCDC

<CustomContent platform="tidb">

| SQL 语句 | 描述 |
|---------------|-------------|
| [`ADMIN [SET\|SHOW\|UNSET] BDR ROLE`](/sql-statements/sql-statement-admin-bdr-role.md) | 管理 BDR 角色。 |
| [`SHOW MASTER STATUS`](/sql-statements/sql-statement-show-master-status.md) | 显示集群中的最新 TSO。 |

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview) & [TiDB Binlog](https://docs.pingcap.com/tidb/v8.3/tidb-binlog-overview) 是用于将 TiDB 数据复制到上游的工具，适用于 TiDB 自托管。大部分关于 TiCDC 和 TiDB Binlog 的 SQL 语句不适用于 TiDB Cloud。对于 TiDB Cloud，你可以使用 [Changefeed](/tidb-cloud/changefeed-overview.md) 功能，在 [TiDB Cloud 控制台](https://tidbcloud.com) 中实现数据流。|

| SQL 语句 | 描述 |
|---------------|-------------|
| [`SHOW MASTER STATUS`](/sql-statements/sql-statement-show-master-status.md) | 显示集群中的最新 TSO。 |

</CustomContent>

## 统计信息与执行计划管理

| SQL 语句 | 描述 |
|---------------|-------------|
| [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) | 收集表的统计信息。 |
| [`CREATE BINDING`](/sql-statements/sql-statement-create-binding.md) | 为 SQL 语句创建执行计划绑定。 |
| [`DROP BINDING`](/sql-statements/sql-statement-drop-binding.md) | 从 SQL 语句中删除执行计划绑定。 |
| [`DROP STATS`](/sql-statements/sql-statement-drop-stats.md) | 删除表的统计信息。 |
| [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) | 类似于 `EXPLAIN`，但会执行该语句。 |
| [`LOAD STATS`](/sql-statements/sql-statement-load-stats.md) | 将统计信息加载到 TiDB 中。 |
| [`SHOW ANALYZE STATUS`](/sql-statements/sql-statement-show-analyze-status.md) | 显示统计信息采集任务。 |
| [`SHOW BINDINGS`](/sql-statements/sql-statement-show-bindings.md) | 显示已创建的 SQL 绑定。 |
| [`SHOW COLUMN_STATS_USAGE`](/sql-statements/sql-statement-show-column-stats-usage.md) | 显示列统计的最后使用时间和采集时间。 |
| [`SHOW STATS_BUCKETS`](/sql-statements/sql-statement-show-stats-buckets.md) | 显示统计信息中的桶信息。 |
| [`SHOW STATS_HEALTHY`](/sql-statements/sql-statement-show-stats-healthy.md) | 显示统计信息的估计准确性。 |
| [`SHOW STATS_HISTOGRAMS`](/sql-statements/sql-statement-show-stats-histograms.md) | 显示统计信息中的直方图信息。 |
| [`SHOW STATS_LOCKED`](/sql-statements/sql-statement-show-stats-locked.md) | 显示统计信息被锁定的表。 |
| [`SHOW STATS_META`](/sql-statements/sql-statement-show-stats-meta.md) | 显示表中的行数以及变更的行数。 |
| [`SHOW STATS_TOPN`](/sql-statements/sql-statement-show-stats-topn.md) | 显示统计信息中的 Top-N 信息。 |