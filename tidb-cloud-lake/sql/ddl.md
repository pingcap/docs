---
title: DDL（数据定义语言）命令
summary: 本主题提供 {{{ .lake }}} 中 DDL（数据定义语言）命令的参考信息。
---

# DDL（数据定义语言）命令

本主题提供 {{{ .lake }}} 中 DDL（数据定义语言）命令的参考信息。

## 数据库和表管理 {#database-table-management}

| 组件 | 描述 |
|-----------|-------------|
| **[Catalog](/tidb-cloud-lake/sql/catalog.md)** | 创建、删除和列出 catalog |
| **[数据库](/tidb-cloud-lake/sql/ddl-database-overview.md)** | 创建、修改和删除数据库 |
| **[表](/tidb-cloud-lake/sql/ddl-table-overview.md)** | 创建、修改和管理表 |
| **[表版本控制](/tidb-cloud-lake/sql/table-versioning.md)** | 创建用于时间旅行的命名快照标签 |
| **[视图](/tidb-cloud-lake/sql/ddl-view-overview.md)** | 基于查询创建和管理虚拟表 |

## 性能和索引 {#performance-indexing}

| 组件 | 描述 |
|-----------|-------------|
| **[Cluster Key](/tidb-cloud-lake/sql/cluster-key.md)** | 定义数据聚簇以优化查询 |
| **[聚合索引](/tidb-cloud-lake/sql/aggregating-index-sql.md)** | 预计算聚合以加快查询 |
| **[倒排索引](/tidb-cloud-lake/sql/inverted-index.md)** | 用于文本列的全文搜索索引 |
| **[Ngram 索引](/tidb-cloud-lake/sql/ngram-index-sql.md)** | 用于 LIKE 模式的子字符串搜索索引 |
| **[空间索引](/tidb-cloud-lake/sql/spatial-index-overview.md)** | 用于 GEOMETRY 列的空间裁剪索引 |
| **[向量索引](/tidb-cloud-lake/sql/vector-index.md)** | 用于向量嵌入的相似度搜索索引 |
| **[虚拟列](/tidb-cloud-lake/sql/virtual-column-overview.md)** | 将 JSON 字段提取并索引为虚拟列 |

## 安全和访问控制 {#security-access-control}

| 组件 | 描述 |
|-----------|-------------|
| **[用户](/tidb-cloud-lake/sql/user-role.md)** | 创建和管理数据库用户 |
| **[标签](/tidb-cloud-lake/sql/tag-overview.md)** | 将键值元信息附加到对象上，用于治理和分类 |
| **[网络策略](/tidb-cloud-lake/sql/network-policy-sql.md)** | 控制对数据库的网络访问 |
| **[脱敏策略](/tidb-cloud-lake/sql/masking-policy-sql.md)** | 对敏感信息应用数据脱敏 |
| **[密码策略](/tidb-cloud-lake/sql/password-policy-sql.md)** | 强制执行密码要求和轮换 |
| **[行访问策略](/tidb-cloud-lake/sql/row-access-policy-overview.md)** | 使用集中式行级谓词过滤表中的行 |

## 数据集成和处理 {#data-integration-processing}

| 组件 | 描述 |
|-----------|-------------|
| **[Stage](/tidb-cloud-lake/sql/stage.md)** | 定义用于数据加载的存储位置 |
| **[Pipe](/tidb-cloud-lake/sql/pipe.md)** | 管理摄取管道 |
| **[Stream](/tidb-cloud-lake/sql/stream.md)** | 捕获并处理数据变更 |
| **[任务](/tidb-cloud-lake/sql/task.md)** | 调度并自动化 SQL 操作 |
| **[序列](/tidb-cloud-lake/sql/sequence.md)** | 生成唯一的顺序编号 |
| **[Connection](/tidb-cloud-lake/sql/connection.md)** | 配置外部数据源连接 |
| **[文件格式](/tidb-cloud-lake/sql/file-format.md)** | 定义数据导入/导出的格式 |
| **[字典](/tidb-cloud-lake/sql/dictionary.md)** | 定义由外部源支持的字典 |

## 函数和过程 {#functions-procedures}

| 组件 | 描述 |
|-----------|-------------|
| **[UDF](/tidb-cloud-lake/sql/user-defined-function.md)** | 使用 Python 或 JavaScript 创建自定义函数 |
| **[外部函数](/tidb-cloud-lake/sql/external-function.md)** | 将外部 API 集成为 SQL 函数 |
| **[存储过程](/tidb-cloud-lake/sql/stored-procedure.md)** | 创建用于复杂逻辑的存储过程 |
| **[通知](/tidb-cloud-lake/sql/notification.md)** | 设置事件通知和 webhook |

## 资源管理 {#resource-management}

| 组件 | 描述 |
|-----------|-------------|
| **[计算集群 (Warehouse)](/tidb-cloud-lake/sql/warehouse-overview.md)** | 管理用于查询执行的计算资源 |
| **[Worker](/tidb-cloud-lake/sql/worker-overview.md)** | 通过云控制管理沙箱 UDF 执行环境 |
| **[Workload Group](/tidb-cloud-lake/sql/workload-group.md)** | 控制资源分配和优先级 |
| **[事务](/tidb-cloud-lake/sql/transaction.md)** | 管理数据库事务 |
| **[变量](/tidb-cloud-lake/sql/sql-variables.md)** | 设置和使用会话/全局变量 |