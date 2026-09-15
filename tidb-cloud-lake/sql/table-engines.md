---
title: 表引擎
summary: "{{{ .lake }}} 提供多种表引擎，让你无需移动数据即可在性能与互操作性需求之间取得平衡。每种引擎都针对特定场景进行了优化——从 {{{ .lake }}} 原生的 Fuse 存储到外部数据湖格式。"
---

# 表引擎

{{{ .lake }}} 提供多种表引擎，让你无需移动数据即可在性能与互操作性需求之间取得平衡。每种引擎都针对特定场景进行了优化——从 {{{ .lake }}} 原生的 Fuse 存储到外部数据湖格式。

## 可用引擎 {#available-engines}

| 引擎 | 最适用场景 | 亮点 |
| ------ | -------- | ---------- |
| [Fuse Engine 表](/tidb-cloud-lake/sql/fuse-engine-tables.md) | 原生 {{{ .lake }}} 表 | 基于快照的存储、自动聚簇、变更跟踪 |
| [Apache Iceberg™ Tables](/tidb-cloud-lake/sql/apache-icebergtm-tables.md) | lakehouse 目录 | 时间旅行、Schema Evolution、REST/Hive/Storage 目录 |
| [Apache Hive Tables](/tidb-cloud-lake/sql/apache-hive-tables.md) | Hive metastore 数据 | 通过外部表查询由 Hive 管理的数据存储 |
| [Delta Lake Engine](/tidb-cloud-lake/sql/delta-lake-engine.md) | Delta Lake 数据集 | 在对象存储中读取 Delta 表，并提供 ACID 保证 |

## 如何选择引擎 {#choosing-an-engine}

- 当你直接在 {{{ .lake }}} 中管理数据，并希望获得最佳存储和查询性能时，请使用 **Fuse**。
- 如果你已经通过 Iceberg catalog 管理数据集，并且需要紧密的 lakehouse 集成，请选择 **Iceberg**。
- 如果你依赖现有的 Hive Metastore，但希望使用 {{{ .lake }}} 的查询引擎，请配置 **Hive**。
- 如果你希望原位分析 Delta Lake 表，而不将其导入 Fuse，请选择 **Delta**。