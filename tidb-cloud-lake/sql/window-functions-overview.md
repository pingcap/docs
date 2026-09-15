---
title: 窗口函数
summary: 窗口函数在一组相关行上执行计算，同时为每个输入行返回一个结果。与聚合函数不同，窗口函数不会将多行折叠为单个输出。
---

# 窗口函数

## 概述 {#overview}

窗口函数在一组相关行上执行计算，同时为每个输入行返回一个结果。与聚合函数不同，窗口函数不会将多行折叠为单个输出。

**主要特性：**

- 在与当前行相关的“窗口”行集上执行操作
- 为每个输入行返回一个值（不进行分组/折叠）
- 可以访问窗口中其他行的值
- 支持分区和排序，以实现灵活的计算

**关于本文档中 SQL 示例的说明：**

- ✅ **完整 SQL 语句** 已在 {{{ .lake }}} 上验证
- ⚠️ **语法示例** 展示的是窗口框架模式（不是完整语句）
- 📋 所有示例均使用 {{{ .lake }}} 支持的标准 SQL 语法
- 🔍 标记为“Complete example”的示例可直接完整执行

## 窗口函数类别 {#window-function-categories}

{{{ .lake }}} 支持两大类窗口函数：

### 1. 专用窗口函数 {#1-dedicated-window-functions}

这些函数专门为窗口操作设计。

**排名函数：**

| Function | 描述 | 并列值处理 | 示例输出 |
|----------|-------------|---------------|----------------|
| [ROW_NUMBER](/tidb-cloud-lake/sql/row-number.md) | 顺序编号 | 始终唯一 | `1, 2, 3, 4, 5` |
| [RANK](/tidb-cloud-lake/sql/rank.md) | 带间隔的排名 | 相同排名，后续有间隔 | `1, 2, 2, 4, 5` |
| [DENSE_RANK](/tidb-cloud-lake/sql/dense-rank.md) | 不带间隔的排名 | 相同排名，无间隔 | `1, 2, 2, 3, 4` |

**分布函数：**

| Function | 描述 | 范围 | 示例输出 |
|----------|-------------|-------|----------------|
| [PERCENT_RANK](/tidb-cloud-lake/sql/percent-rank.md) | 以百分比表示的相对排名 | 0.0 到 1.0 | `0.0, 0.25, 0.5, 0.75, 1.0` |
| [CUME_DIST](/tidb-cloud-lake/sql/cume-dist.md) | 累积分布 | 0.0 到 1.0 | `0.2, 0.4, 0.6, 0.8, 1.0` |
| [NTILE](/tidb-cloud-lake/sql/ntile.md) | 划分为 N 个存储桶 | 1 到 N | `1, 1, 2, 2, 3, 3` |

**值访问函数：**

| Function | 描述 | 使用场景 |
|----------|-------------|----------|
| [FIRST_VALUE](/tidb-cloud-lake/sql/first-value.md) | 窗口中的第一个值 | 获取最高/最早的值 |
| [LAST_VALUE](/tidb-cloud-lake/sql/last-value.md) | 窗口中的最后一个值 | 获取最低/最新的值 |
| [NTH_VALUE](/tidb-cloud-lake/sql/nth-value.md) | 窗口中的第 N 个值 | 获取特定位置的值 |
| [LAG](/tidb-cloud-lake/sql/lag.md) | 前一行的值 | 与前一行比较 |
| [LEAD](/tidb-cloud-lake/sql/lead.md) | 后一行的值 | 与后一行比较 |

**别名：**

| 函数 | 别名 |
|----------|----------|
| [FIRST](/tidb-cloud-lake/sql/first.md) | FIRST_VALUE |
| [LAST](/tidb-cloud-lake/sql/last.md) | LAST_VALUE |

### 2. 作为窗口函数使用的聚合函数 {#2-aggregate-functions-used-as-window-functions}

这些是标准聚合函数，可以与 OVER 子句一起使用以执行窗口操作。

| Function | 描述 | 支持窗口框架 | 示例 |
|----------|-------------|---------------------|---------|
| [SUM](/tidb-cloud-lake/sql/sum.md) | 计算窗口上的总和 | ✓ | `SUM(sales) OVER (PARTITION BY region ORDER BY date)` |
| [AVG](/tidb-cloud-lake/sql/avg.md) | 计算窗口上的平均值 | ✓ | `AVG(score) OVER (ORDER BY id ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)` |
| [COUNT](/tidb-cloud-lake/sql/count.md) | 统计窗口中的行数 | ✓ | `COUNT(*) OVER (PARTITION BY department)` |
| [MIN](/tidb-cloud-lake/sql/min.md) | 返回窗口中的最小值 | ✓ | `MIN(price) OVER (PARTITION BY category)` |
| [MAX](/tidb-cloud-lake/sql/max.md) | 返回窗口中的最大值 | ✓ | `MAX(price) OVER (PARTITION BY category)` |
| [ARRAY_AGG](/tidb-cloud-lake/sql/array-agg.md) | 将值收集到数组中 | | `ARRAY_AGG(product) OVER (PARTITION BY category)` |
| [STDDEV_POP](/tidb-cloud-lake/sql/stddev-pop.md) | 总体标准差 | ✓ | `STDDEV_POP(value) OVER (PARTITION BY group)` |
| [STDDEV_SAMP](/tidb-cloud-lake/sql/stddev-samp.md) | 样本标准差 | ✓ | `STDDEV_SAMP(value) OVER (PARTITION BY group)` |
| [MEDIAN](/tidb-cloud-lake/sql/median.md) | 中位数 | ✓ | `MEDIAN(response_time) OVER (PARTITION BY server)` |

**条件变体**

| Function | 描述 | 支持窗口框架 | 示例 |
|----------|-------------|---------------------|---------|
| [COUNT_IF](/tidb-cloud-lake/sql/count-if.md) | 条件计数 | ✓ | `COUNT_IF(status = 'complete') OVER (PARTITION BY dept)` |
| [SUM_IF](/tidb-cloud-lake/sql/sum-if.md) | 条件求和 | ✓ | `SUM_IF(amount, status = 'paid') OVER (PARTITION BY customer)` |
| [AVG_IF](/tidb-cloud-lake/sql/avg-if.md) | 条件平均值 | ✓ | `AVG_IF(score, passed = true) OVER (PARTITION BY class)` |
| [MIN_IF](/tidb-cloud-lake/sql/min-if.md) | 条件最小值 | ✓ | `MIN_IF(temp, location = 'outside') OVER (PARTITION BY day)` |
| [MAX_IF](/tidb-cloud-lake/sql/max-if.md) | 条件最大值 | ✓ | `MAX_IF(speed, vehicle = 'car') OVER (PARTITION BY test)` |

## 基本语法 {#basic-syntax}

所有窗口函数都遵循以下模式：

```sql
FUNCTION() OVER (
    [ PARTITION BY column ]
    [ ORDER BY column ]
    [ window_frame ]
)
```

- **PARTITION BY**：将数据划分为多个组
- **ORDER BY**：对每个分区内的行进行排序
- **window_frame**：定义要包含哪些行（可选）

## 窗口框架说明 {#window-frame-specification}

窗口框架定义了对每一行进行计算时应包含哪些行。{{{ .lake }}} 支持两种类型的窗口框架：

### 1. ROWS BETWEEN {#1-rows-between}

使用物理行数定义窗口框架。

**语法：**

```sql
ROWS BETWEEN frame_start AND frame_end
```

**示例：**

- `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` - 运行总计
- `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` - 3 天移动平均
- `ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING` - 居中窗口

有关详细示例和用法，请参见 [ROWS BETWEEN](/tidb-cloud-lake/sql/rows-between.md)。

### 2. RANGE BETWEEN {#2-range-between}

使用逻辑值范围定义窗口框架。

**语法：**

```sql
RANGE BETWEEN frame_start AND frame_end
```

**示例：**

- `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` - 按值累积
- `RANGE BETWEEN INTERVAL '7' DAY PRECEDING AND CURRENT ROW` - 7 天窗口

有关详细示例和用法，请参见 [RANGE BETWEEN](/tidb-cloud-lake/sql/range-between.md)。

## 常见使用场景 {#common-use-cases}

- **排名**：创建排行榜和 Top-N 列表
- **分析**：计算运行总计、移动平均、百分位数
- **比较**：比较当前值与前一个/后一个值
- **分组**：在不丢失明细的情况下将数据划分为多个存储桶

有关详细语法和示例，请参见上方各个函数的单独文档。