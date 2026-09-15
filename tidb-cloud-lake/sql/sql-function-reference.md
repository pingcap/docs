---
title: SQL 函数参考
summary: "{{{ .lake }}} 提供了适用于各类数据处理场景的全面 SQL 函数。函数按重要性和使用频率进行组织。"
---

# SQL 函数参考

{{{ .lake }}} 提供了适用于各类数据处理场景的全面 SQL 函数。函数按重要性和使用频率进行组织。

> **提示：**
>
> **找不到你需要的函数？** 如果下面的内置函数都无法覆盖你的逻辑需求，你可以使用 [用户定义函数（UDF）](/tidb-cloud-lake/sql/user-defined-function.md) 定义自己的函数。UDF 允许你使用 SQL 表达式、Python 或 JavaScript 实现自定义标量函数、聚合函数和表函数，然后像调用任何内置函数一样调用它们。参见下文的[使用 User-Defined Functions 扩展](#extending-with-user-defined-functions)。

## 核心数据函数 {#core-data-functions}

| 类别 | 描述 |
|----------|-------------|
| [数值函数](/tidb-cloud-lake/sql/numeric-functions.md) | 数学运算与计算 |
| [字符串函数](/tidb-cloud-lake/sql/string-functions-overview.md) | 文本处理与字符串处理 |
| [日期和时间函数](/tidb-cloud-lake/sql/date-time-functions.md) | 日期、时间和时态操作 |
| [转换函数](/tidb-cloud-lake/sql/conversion-functions.md) | 类型转换与数据格式转换 |
| [条件函数](/tidb-cloud-lake/sql/conditional-functions.md) | 逻辑与控制流操作 |

## 分析函数 {#analytics-functions}

| 类别 | 描述 |
|----------|-------------|
| [聚合函数](/tidb-cloud-lake/sql/aggregate-functions.md) | 跨多行的统计计算 |
| [窗口函数](/tidb-cloud-lake/sql/window-functions-overview.md) | 使用窗口操作进行高级分析 |

## 结构化与半结构化数据 {#structured-semi-structured-data}

| 类别 | 描述 |
|----------|-------------|
| [结构化和半结构化函数](/tidb-cloud-lake/sql/structured-semi-structured-functions.md) | JSON、数组、对象和嵌套数据处理 |

## 搜索函数 {#search-functions}

| 类别 | 描述 |
|----------|-------------|
| [全文搜索函数](/tidb-cloud-lake/sql/full-text-search-functions.md) | 全文搜索与相关性评分 |

## 向量函数 {#vector-functions}

| 类别 | 描述 |
|----------|-------------|
| [向量函数](/tidb-cloud-lake/sql/vector-functions.md) | 向量相似度与距离计算 |

## 地理空间函数 {#geospatial-functions}

| 类别 | 描述 |
|----------|-------------|
| [Geospatial Functions](/tidb-cloud-lake/sql/geospatial-functions.md) | 几何、GeoHash 和 H3 空间操作 |

## 数据管理 {#data-management}

| 类别 | 描述 |
|----------|-------------|
| [表函数](/tidb-cloud-lake/sql/table-functions.md) | 文件检查、数据生成和系统信息 |
| [系统函数](/tidb-cloud-lake/sql/system-functions.md) | 系统信息与管理操作 |
| [上下文函数](/tidb-cloud-lake/sql/context-functions.md) | 当前会话、用户和数据库信息 |

## 安全性与完整性 {#security-integrity}

| 类别 | 描述 |
|----------|-------------|
| [散列函数](/tidb-cloud-lake/sql/hash-functions.md) | 数据散列与完整性验证 |
| [位图函数](/tidb-cloud-lake/sql/bitmap-functions.md) | 高性能位图操作与分析 |
| [UUID 函数](/tidb-cloud-lake/sql/uuid-functions.md) | 通用唯一标识符生成 |
| [IP 地址函数](/tidb-cloud-lake/sql/ip-address-functions.md) | 网络地址处理与验证 |

## 实用函数 {#utility-functions}

| 类别 | 描述 |
|----------|-------------|
| [区间函数](/tidb-cloud-lake/sql/interval-functions.md) | 时间单位转换与区间创建 |
| [序列函数](/tidb-cloud-lake/sql/sequence-functions-overview.md) | 自增序列值生成 |
| [数据匿名化函数](/tidb-cloud-lake/sql/data-anonymization-functions.md) | 数据脱敏与匿名化工具 |
| [测试函数](/tidb-cloud-lake/sql/test-functions.md) | 测试与调试工具 |
| [其他函数](/tidb-cloud-lake/sql/other-functions.md) | 其他辅助函数与工具 |

## 使用 User-Defined Functions 扩展 {#extending-with-user-defined-functions}

当上述内置函数无法覆盖你的特定逻辑时，可以使用 [用户定义函数（UDF）](/tidb-cloud-lake/sql/user-defined-function.md) 定义自己的函数。创建后，UDF 在查询中的调用方式与内置函数完全相同。

| 函数类型                                                                                 | 适用场景                                                                  |
| --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| [标量函数 (SQL)](/tidb-cloud-lake/sql/create-scalar-function.md)              | 你希望在多个查询中复用某个 SQL 表达式（如数学计算、字符串格式化）。 |
| [标量函数 (Python/JavaScript)](/tidb-cloud-lake/sql/create-scalar-function.md) | 你的逻辑需要控制流、外部库或高级算法。   |
| [聚合函数](/tidb-cloud-lake/sql/create-aggregate-function.md)       | 你需要内置聚合函数无法表达的自定义聚合。        |
| [表函数](/tidb-cloud-lake/sql/create-table-function.md)               | 你希望使用可复用、带参数的查询来返回结果集。          |

如需了解 UDF 类型和语法的完整对比，请参见 [用户定义函数](/tidb-cloud-lake/sql/user-defined-function.md)。