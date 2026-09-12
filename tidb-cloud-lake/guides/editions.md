---
title: 版本
summary: "{{{ .lake }}} 提供三个版本：Personal、Business 和 Dedicated，您可以根据不同需求进行选择，以满足广泛的使用场景并确保不同用例下的最佳性能。"
---

# 版本

{{{ .lake }}} 提供三个版本：**Personal**、**Business** 和 **Dedicated**，您可以根据不同需求进行选择，以满足广泛的使用场景并确保不同用例下的最佳性能。

有关定价信息，请参见 [价格与计费](/tidb-cloud-lake/guides/pricing-billing.md)。有关这些版本之间的详细功能列表，请参见 [功能列表](#feature-lists)。

## 功能列表 {#feature-lists}

以下是 {{{ .lake }}} 不同版本的功能列表：

### 发布管理 {#release-management}

| 功能 | Personal | Business | Dedicated |
|----------|----------|----------|-----------|
| 提前访问每周发布的新版本，可在每次版本部署到生产账户之前用于额外的测试/验证。 | | ✓ | ✓ |

### 安全与治理 {#security-governance}

| 功能 | Personal | Business | Dedicated |
|----------|----------|----------|-----------|
| SOC 2 Type II 认证。 | ✓ | ✓ | ✓ |
| GDPR | ✓ | ✓ | ✓ |
| 所有数据自动加密。 | ✓ | ✓ | ✓ |
| 对象级访问控制。 | ✓ | ✓ | ✓ |
| 标准 Time Travel（最长 1 天），用于访问/恢复已修改和已删除的数据。 | ✓ | ✓ | ✓ |
| 通过 Fail-Safe 对已修改/已删除的数据进行容灾（在 Time Travel 之外额外保留 7 天）。 | ✓ | ✓ | ✓ |
| **扩展 Time Travel**。 | | 90 days | 90 days |
| 列级安全，可对表或视图中的列应用脱敏策略。 | ✓ | ✓ | ✓ |
| 通过 Account Usage ACCESS_HISTORY 视图审计用户访问历史。 | ✓ | ✓ | ✓ |
| **支持使用 AWS PrivateLink 私有连接到 {{{ .lake }}} 服务**。 | | ✓ | ✓ |
| **专用元信息存储和计算资源池（用于虚拟计算集群 (Warehouse)）**。 | | | ✓ |

### 计算资源 {#compute-resource}

| 功能 | Personal | Business | Dedicated |
|----------|----------|----------|-----------|
| 虚拟计算集群 (Warehouse)，用于隔离查询和数据加载工作负载的独立计算集群。 | ✓ | ✓ | ✓ |
| 多集群扩缩容 | | ✓ | ✓ |
| 用于监控虚拟 Warehouse credit 使用情况的资源监视器。 | ✓ | ✓ | ✓ |

### SQL 支持 {#sql-support}

| 功能 | Personal | Business | Dedicated |
|----------|----------|----------|-----------|
| 标准 SQL，包括 SQL:1999 中定义的大多数 DDL 和 DML。 | ✓ | ✓ | ✓ |
| 高级 DML，例如多表 INSERT、MERGE 和 multi-merge。 | ✓ | ✓ | ✓ |
| 广泛支持标准数据类型。 | ✓ | ✓ | ✓ |
| 原生支持半结构化数据（JSON、ORC、Parquet）。 | ✓ | ✓ | ✓ |
| 原生支持地理空间数据。 | ✓ | ✓ | ✓ |
| 原生支持非结构化数据。 | ✓ | ✓ | ✓ |
| 表列中字符串/文本数据的排序规则。 | ✓ | ✓ | ✓ |
| 多语句事务。 | ✓ | ✓ | ✓ |
| 用户定义函数（UDF），支持 JavaScript、Python 和 WebAssembly。 | | ✓ | ✓ |
| 外部函数，用于将 {{{ .lake }}} 扩展到其他开发平台。 | ✓ | ✓ | ✓ |
| 用于外部函数的 Amazon API Gateway 私有端点。 | ✓ | ✓ | ✓ |
| 外部表，用于引用云存储数据湖中的数据。 | ✓ | ✓ | ✓ |
| 支持对超大表中的数据进行聚簇以提升查询性能，并自动维护聚簇。 | ✓ | ✓ | ✓ |
| 针对点查查询的搜索优化，并自动维护。 | ✓ | ✓ | ✓ |
| 物化视图，并自动维护结果。 | ✓ | ✓ | ✓ |
| Iceberg 表，用于引用云存储数据湖中的数据。 | ✓ | ✓ | ✓ |
| Schema detection，用于自动检测 staged 半结构化数据文件集合中的 schema 并获取列定义。 | ✓ | ✓ | ✓ |
| Schema evolution，用于自动演进表结构，以支持从数据源接收到的新数据结构。 | ✓ | ✓ | ✓ |
| 支持[使用外部位置创建表](/tidb-cloud-lake/sql/create-external-table.md)。 | ✓ | ✓ | ✓ |
| 支持 [ATTACH TABLE](/tidb-cloud-lake/sql/attach-table.md)。 | ✓ | ✓ | ✓ |

### 接口与工具 {#interfaces-tools}

| 功能 | Personal | Business | Dedicated |
|----------|----------|----------|-----------|
| 新一代 SQL 工作区，用于高级查询开发、数据分析和可视化。 | ✓ | ✓ | ✓ |
| LakeSQL，一种命令行客户端，用于构建/测试查询、加载/卸载批量数据以及自动化 DDL 操作。 | ✓ | ✓ | ✓ |
| Rust、Python、Java、Node.js、.js、PHP 和 Go 的编程接口。 | ✓ | ✓ | ✓ |
| 原生支持 JDBC。 | ✓ | ✓ | ✓ |
| 丰富的生态系统，可连接 ETL、BI 以及其他第三方供应商和技术。 | ✓ | ✓ | ✓ |

### 数据导入与导出 {#data-import-export}

| 功能 | Personal | Business | Dedicated |
|----------|----------|----------|-----------|
| 从分隔符平面文件（CSV、TSV 等）和半结构化数据文件（JSON、ORC、Parquet）进行批量加载。 | ✓ | ✓ | ✓ |
| 批量卸载到分隔符平面文件和 JSON 文件。 | ✓ | ✓ | ✓ |
| 持续微批加载。 | ✓ | ✓ | ✓ |
| 用于低延时加载流式数据的流式处理。 | ✓ | ✓ | ✓ |
| 用于从 Apache Kafka topic 加载数据的 {{{ .lake }}} Connector for Kafka。 | ✓ | ✓ | ✓ |

### 数据管道 {#data-pipelines}

| 功能 | Personal | Business | Dedicated |
|----------|----------|----------|-----------|
| 用于跟踪表变更的 Streams。 | ✓ | ✓ | ✓ |
| 用于调度执行 SQL 语句的 Tasks，通常与表 Streams 配合使用。 | ✓ | ✓ | ✓ |
