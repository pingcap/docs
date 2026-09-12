---
title: 性能优化
summary: "{{{ .lake }}} 主要通过**多种索引技术**来加速查询性能，包括数据聚簇、结果缓存和专用索引，帮助你显著提升查询响应时间。"
---

# 性能优化

{{{ .lake }}} 主要通过**多种索引技术**来加速查询性能，包括数据聚簇、结果缓存和专用索引，帮助你显著提升查询响应时间。

## 优化功能 {#optimization-features}

| 功能 | 用途 | 适用场景 |
|---------|---------|------------|
| [**Cluster Key**](/tidb-cloud-lake/sql/cluster-key.md) | 自动以物理方式组织数据，以获得最佳查询性能 | 当你拥有大型表，并且经常基于特定列进行过滤时，尤其适用于时序数据或分类数据 |
| [**查询结果缓存**](/tidb-cloud-lake/guides/query-result-cache.md) | 自动存储并复用相同查询的结果 | 当你的应用会重复运行相同的分析查询时，例如在仪表板或定时报告中 |
| [**虚拟列**](/tidb-cloud-lake/guides/virtual-column.md) | 自动加速对 JSON/VARIANT 数据内部字段的访问 | 当你经常查询半结构化数据中的特定路径，并且需要亚秒级响应时间时 |
| [**聚合索引**](/tidb-cloud-lake/guides/aggregating-index.md) | 预计算并存储常见聚合结果 | 当你的分析负载经常在大型数据集上运行 SUM、COUNT、AVG 查询时 |
| [**全文索引**](/tidb-cloud-lake/guides/full-text-index.md) | 提供极快的语义文本搜索能力 | 当你需要高级文本搜索功能（如相关性评分和模糊匹配）时 |
| [**Ngram 索引**](/tidb-cloud-lake/guides/ngram-index.md) | 加速带有通配符的模式匹配 | 当你的查询在大型文本列上使用带通配符的 LIKE 运算符时（尤其是 '%keyword%'） |

## 功能可用性 {#feature-availability}

| 功能 | 社区版 | 企业版 | 云版 |
|---------|-----------|------------|-------|
| cluster key | ✅ | ✅ | ✅ |
| 查询结果缓存 | ✅ | ✅ | ✅ |
| 虚拟列 | ❌ | ✅ | ✅ |
| 聚合索引 | ✅ | ✅ | ✅ |
| 全文索引 | ✅ | ✅ | ✅ |
| Ngram 索引 | ✅ | ✅ | ✅ |