---
title: 系统表
summary: "{{{ .lake }}} 提供了一组系统表，其中包含有关你的 {{{ .lake }}} 部署、数据库、表、查询和系统性能的元信息。这些表为只读，并由系统自动更新。"
---

# 系统表

{{{ .lake }}} 提供了一组系统表，其中包含有关你的 {{{ .lake }}} 部署、数据库、表、查询和系统性能的元信息。这些表为只读，并由系统自动更新。

系统表组织在 `system` schema 中，可以使用标准 SQL 进行查询。它们为监控、故障排查以及了解你的 {{{ .lake }}} 环境提供了有价值的信息。

## 可用的系统表 {#available-system-tables}

### 数据库和表元信息 {#database-table-metadata}

| 表                                                             | 描述                                                                                       |
|-------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| [system.tables](/tidb-cloud-lake/sql/system-tables.md)                                 | 提供所有表的元信息，包括属性、创建时间、大小等。 |
| [system.tables_with_history](/tidb-cloud-lake/sql/system-tables-with-history.md)       | 提供表的历史元信息，包括已删除的表。                    |
| [system.databases](/tidb-cloud-lake/sql/system-databases.md)                           | 包含系统中所有数据库的信息。                                           |
| [system.views](/tidb-cloud-lake/sql/system-views.md)                                   | 包含系统中所有视图的信息。                                               |
| [system.databases_with_history](/tidb-cloud-lake/sql/system-databases-with-history.md) | 包含数据库的历史信息，包括已删除的数据库。                     |
| [system.columns](/tidb-cloud-lake/sql/system-columns.md)                               | 提供所有表中列的信息。                                                 |
| [system.indexes](/tidb-cloud-lake/sql/system-indexes.md)                               | 包含表索引的信息。                                                         |
| [system.virtual_columns](/tidb-cloud-lake/sql/system-virtual-columns.md)               | 列出系统中可用的虚拟列。                                                    |

### 查询和性能 {#query-performance}

| 表 | 描述 |
|-------|-------------|
| [system.query_log](/tidb-cloud-lake/sql/system-query-log.md) | 包含已执行查询的信息，包括性能指标。 |
| [system.metrics](/tidb-cloud-lake/sql/system-metrics.md) | 包含系统指标事件的信息。 |
| [system.query_cache](/tidb-cloud-lake/sql/system-query-cache.md) | 提供查询缓存的信息。 |
| [system.locks](/tidb-cloud-lake/sql/system-locks.md) | 包含系统中已获取锁的信息。 |

### 函数和设置 {#functions-settings}

| 表 | 描述 |
|-------|-------------|
| [system.functions](/tidb-cloud-lake/sql/system-functions.md) | 列出所有可用的内置函数。 |
| [system.table_functions](/tidb-cloud-lake/sql/system-table-functions.md) | 列出所有可用的表函数。 |
| [system.user_functions](/tidb-cloud-lake/sql/system-user-functions.md) | 包含用户定义函数的信息。 |
| [system.settings](/tidb-cloud-lake/sql/system-settings.md) | 包含系统设置的信息。 |

### 系统信息 {#system-information}

| 表 | 描述 |
|-------|-------------|
| [system.build_options](/tidb-cloud-lake/sql/system-build-options.md) | 包含用于编译 {{{ .lake }}} 的构建选项信息。 |
| [system.clusters](/tidb-cloud-lake/sql/system-clusters.md) | 包含系统中集群的信息。 |
| [system.contributors](/tidb-cloud-lake/sql/system-contributors.md) | 列出 {{{ .lake }}} 项目的贡献者。 |
| [system.credits](/tidb-cloud-lake/sql/system-credits.md) | 包含 {{{ .lake }}} 使用的第三方库信息。 |
| [system.caches](/tidb-cloud-lake/sql/system-caches.md) | 提供系统缓存的信息。 |

### 实用表 {#utility-tables}

| 表 | 描述 |
|-------|-------------|
| [system.numbers](/tidb-cloud-lake/sql/system-numbers.md) | 一个包含单列的表，该列中的整数型值从 0 开始，适用于生成测试数据。 |
| [system.streams](/tidb-cloud-lake/sql/system-streams.md) | 包含系统中流的信息。 |
| [system.temp_tables](/tidb-cloud-lake/sql/system-temporary-tables.md) | 包含临时表的信息。 |
| [system.temp_files](/tidb-cloud-lake/sql/system-temp-files.md) | 包含临时文件的信息。 |