---
title: 向量函数
summary: {{{ .lake }}} 中用于向量操作和分析的向量函数。
---

# 向量函数

本节提供 {{{ .lake }}} 中向量函数的参考信息。这些函数支持全面的向量操作，包括距离计算、相似度度量以及向量分析，适用于机器学习应用、向量搜索和 AI 驱动的分析。

## 距离函数 {#distance-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [COSINE_DISTANCE](/tidb-cloud-lake/sql/cosine-distance.md) | 计算向量之间的余弦距离（范围：0-1） | `COSINE_DISTANCE([1,2,3]::VECTOR(3), [4,5,6]::VECTOR(3))` |
| [L1_DISTANCE](/tidb-cloud-lake/sql/l1-distance.md) | 计算向量之间的曼哈顿（L1）距离 | `L1_DISTANCE([1,2,3]::VECTOR(3), [4,5,6]::VECTOR(3))` |
| [L2_DISTANCE](/tidb-cloud-lake/sql/l2-distance.md) | 计算欧几里得（直线）距离 | `L2_DISTANCE([1,2,3]::VECTOR(3), [4,5,6]::VECTOR(3))` |
| [INNER_PRODUCT](/tidb-cloud-lake/sql/inner-product.md) | 计算两个向量的内积（点积） | `INNER_PRODUCT([1,2,3]::VECTOR(3), [4,5,6]::VECTOR(3))` |

## 向量分析函数 {#vector-analysis-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [VECTOR_NORM](/tidb-cloud-lake/sql/vector-norm.md) | 计算向量的 L2 范数（模长） | `VECTOR_NORM([1,2,3]::VECTOR(3))` |
| [VECTOR_DIMS](/tidb-cloud-lake/sql/vector-dims.md) | 返回向量的维度数 | `VECTOR_DIMS([1,2,3]::VECTOR(3))` |

## 距离函数对比 {#distance-functions-comparison}

| 函数 | 描述 | 范围 | 最适用场景 | 用例 |
|----------|-------------|-------|----------|-----------|
| [COSINE_DISTANCE](/tidb-cloud-lake/sql/cosine-distance.md) | 向量之间的余弦距离 | [0, 1] | 当方向比模长更重要时 | • 文档相似度<br/>• 语义搜索<br/>• 推荐系统<br/>• 文本分析 |
| [L1_DISTANCE](/tidb-cloud-lake/sql/l1-distance.md) | 向量之间的曼哈顿（L1）距离 | [0, ∞) | 对离群值更稳健 | • 特征比较<br/>• 离群点检测<br/>• 基于网格的路径查找<br/>• 聚类算法 |
| [L2_DISTANCE](/tidb-cloud-lake/sql/l2-distance.md) | 欧几里得（直线）距离 | [0, ∞) | 当模长和绝对差异都很重要时 | • 图像相似度<br/>• 地理数据<br/>• 异常检测<br/>• 基于特征的聚类 |
| [INNER_PRODUCT](/tidb-cloud-lake/sql/inner-product.md) | 两个向量的点积 | (-∞, ∞) | 当模长和方向都很重要时 | • 神经网络<br/>• 机器学习<br/>• 物理计算<br/>• 向量投影 |

## 向量分析函数对比 {#vector-analysis-functions-comparison}

| 函数 | 描述 | 范围 | 最适用场景 | 用例 |
|----------|-------------|-------|----------|-----------|
| [VECTOR_NORM](/tidb-cloud-lake/sql/vector-norm.md) | 向量的 L2 范数（模长） | [0, ∞) | 向量归一化和模长计算 | • 向量归一化<br/>• 特征缩放<br/>• 模长计算<br/>• 物理应用 |
| [VECTOR_DIMS](/tidb-cloud-lake/sql/vector-dims.md) | 向量维度数量 | [1, 4096] | 向量校验和处理 | • 数据校验<br/>• 动态处理<br/>• 调试<br/>• 兼容性检查 |