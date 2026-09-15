---
title: 向量索引
summary: {{{ .lake }}} 中的向量索引使用 HNSW（Hierarchical Navigable Small World）算法，可对高维向量数据进行高效的相似度搜索。它支持语义搜索、推荐系统和 AI 应用等使用场景。
---

# 向量索引

{{{ .lake }}} 中的向量索引使用 HNSW（Hierarchical Navigable Small World）算法，可对高维向量数据进行高效的相似度搜索。它支持语义搜索、推荐系统和 AI 应用等使用场景。

> **提示：**
>
> 向量索引会在数据写入时**自动构建**。当你向带有向量索引的表中插入或导入数据时，系统会自动生成索引，无需手动干预。只有当你在已包含数据的表上创建索引时，才需要运行 `REFRESH VECTOR INDEX`。

## 向量索引管理 {#vector-index-management}

| 命令                                         | 描述                                               |
|-------------------------------------------------|-----------------------------------------------------------|
| [CREATE VECTOR INDEX](/tidb-cloud-lake/sql/create-vector-index.md)   | 创建新的向量索引，以实现高效的相似度搜索 |
| [REFRESH VECTOR INDEX](/tidb-cloud-lake/sql/refresh-vector-index.md) | 为索引创建前已存在的数据构建索引  |
| [DROP VECTOR INDEX](/tidb-cloud-lake/sql/drop-vector-index.md)       | 删除向量索引                                    |