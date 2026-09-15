---
title: 聚合函数
summary: 本页按功能对 {{{ .lake }}} 中的聚合函数进行了全面概览，便于快速查阅。
---

# 聚合函数

本页按功能对 {{{ .lake }}} 中的聚合函数进行了全面概览，便于快速查阅。

## 基本聚合 {#basic-aggregation}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [COUNT](/tidb-cloud-lake/sql/count.md) | 统计行数或非 NULL 值的数量 | `COUNT(*)` → `10` |
| [COUNT_DISTINCT](/tidb-cloud-lake/sql/count-distinct.md) | 统计不同值的数量 | `COUNT(DISTINCT city)` → `5` |
| [APPROX_COUNT_DISTINCT](/tidb-cloud-lake/sql/approx-count-distinct.md) | 近似统计不同值的数量 | `APPROX_COUNT_DISTINCT(user_id)` → `9955` |
| [SUM](/tidb-cloud-lake/sql/sum.md) | 计算值的总和 | `SUM(sales)` → `1250.75` |
| [AVG](/tidb-cloud-lake/sql/avg.md) | 计算值的平均值 | `AVG(temperature)` → `72.5` |
| [MIN](/tidb-cloud-lake/sql/min.md) | 返回最小值 | `MIN(price)` → `9.99` |
| [MAX](/tidb-cloud-lake/sql/max.md) | 返回最大值 | `MAX(price)` → `99.99` |
| [ANY_VALUE](/tidb-cloud-lake/sql/any-value.md) | 返回组中的任意一个值 | `ANY_VALUE(status)` → `'active'` |

## 条件聚合 {#conditional-aggregation}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [COUNT_IF](/tidb-cloud-lake/sql/count-if.md) | 统计满足条件的行数 | `COUNT_IF(price > 100)` → `5` |
| [SUM_IF](/tidb-cloud-lake/sql/sum-if.md) | 对满足条件的值求和 | `SUM_IF(amount, status = 'completed')` → `750.25` |
| [AVG_IF](/tidb-cloud-lake/sql/avg-if.md) | 计算满足条件的值的平均值 | `AVG_IF(score, passed = true)` → `85.6` |
| [MIN_IF](/tidb-cloud-lake/sql/min-if.md) | 在条件为 true 时返回最小值 | `MIN_IF(temp, location = 'outside')` → `45.2` |
| [MAX_IF](/tidb-cloud-lake/sql/max-if.md) | 在条件为 true 时返回最大值 | `MAX_IF(speed, vehicle = 'car')` → `120.5` |

## 统计函数 {#statistical-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [VAR_POP](/tidb-cloud-lake/sql/var-pop.md) / [VARIANCE_POP](/tidb-cloud-lake/sql/variance-pop.md) | 总体方差 | `VAR_POP(height)` → `10.25` |
| [VAR_SAMP](/tidb-cloud-lake/sql/var-samp.md) / [VARIANCE_SAMP](/tidb-cloud-lake/sql/variance-samp.md) | 样本方差 | `VAR_SAMP(height)` → `12.3` |
| [STDDEV_POP](/tidb-cloud-lake/sql/stddev-pop.md) | 总体标准差 | `STDDEV_POP(height)` → `3.2` |
| [STDDEV_SAMP](/tidb-cloud-lake/sql/stddev-samp.md) | 样本标准差 | `STDDEV_SAMP(height)` → `3.5` |
| [COVAR_POP](/tidb-cloud-lake/sql/covar-pop.md) | 总体协方差 | `COVAR_POP(x, y)` → `2.5` |
| [COVAR_SAMP](/tidb-cloud-lake/sql/covar-samp.md) | 样本协方差 | `COVAR_SAMP(x, y)` → `2.7` |
| [KURTOSIS](/tidb-cloud-lake/sql/kurtosis.md) | 衡量分布的峰度 | `KURTOSIS(values)` → `2.1` |
| [SKEWNESS](/tidb-cloud-lake/sql/skewness.md) | 衡量分布的偏斜程度 | `SKEWNESS(values)` → `0.2` |

## 百分位与分布 {#percentile-and-distribution}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [MEDIAN](/tidb-cloud-lake/sql/median.md) | 计算中位数 | `MEDIAN(response_time)` → `125` |
| [MODE](/tidb-cloud-lake/sql/mode.md) | 返回出现频率最高的值 | `MODE(category)` → `'electronics'` |
| [QUANTILE_CONT](/tidb-cloud-lake/sql/quantile-cont.md) | 连续插值分位数 | `QUANTILE_CONT(0.95)(response_time)` → `350.5` |
| [QUANTILE_DISC](/tidb-cloud-lake/sql/quantile-disc.md) | 离散分位数 | `QUANTILE_DISC(0.5)(age)` → `35` |
| [QUANTILE_TDIGEST](/tidb-cloud-lake/sql/quantile-tdigest.md) | 使用 t-digest 近似计算分位数 | `QUANTILE_TDIGEST(0.9)(values)` → `95.2` |
| [QUANTILE_TDIGEST_WEIGHTED](/tidb-cloud-lake/sql/quantile-tdigest-weighted.md) | 加权 t-digest 分位数 | `QUANTILE_TDIGEST_WEIGHTED(0.5)(values, weights)` → `50.5` |
| [MEDIAN_TDIGEST](/tidb-cloud-lake/sql/median-tdigest.md) | 使用 t-digest 近似计算中位数 | `MEDIAN_TDIGEST(response_time)` → `124.5` |
| [HISTOGRAM](/tidb-cloud-lake/sql/histogram.md) | 创建直方图存储桶 | `HISTOGRAM(10)(values)` → `[{...}]` |

## 数组与集合聚合 {#array-and-collection-aggregation}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [ARRAY_AGG](/tidb-cloud-lake/sql/array-agg.md) | 将值收集到数组中 | `ARRAY_AGG(product)` → `['A', 'B', 'C']` |
| [GROUP_ARRAY_MOVING_AVG](/tidb-cloud-lake/sql/group-array-moving-avg.md) | 计算数组上的移动平均值 | `GROUP_ARRAY_MOVING_AVG(3)(values)` → `[null, null, 3.0, 6.0, 9.0]` |
| [GROUP_ARRAY_MOVING_SUM](/tidb-cloud-lake/sql/group-array-moving-sum.md) | 计算数组上的移动和 | `GROUP_ARRAY_MOVING_SUM(2)(values)` → `[null, 3, 7, 11, 15]` |

## 地理空间聚合 {#geospatial-aggregation}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [ST_UNION_AGG](/tidb-cloud-lake/sql/st-union-agg.md) | 对组内的 GEOMETRY 值执行联合体操作 | `ST_UNION_AGG(geom)` → `MULTIPOINT(...)` |
| [ST_INTERSECTION_AGG](/tidb-cloud-lake/sql/st-intersection-agg.md) | 对组内的 GEOMETRY 值执行相交操作 | `ST_INTERSECTION_AGG(geom)` → `POLYGON(...)` |
| [ST_ENVELOPE_AGG](/tidb-cloud-lake/sql/st-envelope-agg.md) | 返回组内 GEOMETRY 值的外接矩形 | `ST_ENVELOPE_AGG(geom)` → `POLYGON(...)` |
| [ST_COLLECT](/tidb-cloud-lake/sql/st-collect.md) | 将 GEOMETRY 值收集为一个 GEOMETRY 结果 | `ST_COLLECT(geom)` → `GEOMETRYCOLLECTION(...)` |

## 字符串聚合 {#string-aggregation}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [GROUP_CONCAT](/tidb-cloud-lake/sql/group-concat.md) | 使用分隔符连接值 | `GROUP_CONCAT(city, ', ')` → `'New York, London, Tokyo'` |
| [STRING_AGG](/tidb-cloud-lake/sql/string-agg.md) | 使用分隔符连接字符串 | `STRING_AGG(tag, ',')` → `'red,green,blue'` |
| [LISTAGG](/tidb-cloud-lake/sql/listagg.md) | 使用分隔符连接值 | `LISTAGG(name, ', ')` → `'Alice, Bob, Charlie'` |

## JSON 聚合 {#json-aggregation}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [JSON_ARRAY_AGG](/tidb-cloud-lake/sql/json-array-agg.md) | 将值聚合为 JSON 数组 | `JSON_ARRAY_AGG(name)` → `'["Alice", "Bob", "Charlie"]'` |
| [JSON_OBJECT_AGG](/tidb-cloud-lake/sql/json-object-agg.md) | 从键值对创建 JSON 对象 | `JSON_OBJECT_AGG(name, score)` → `'{"Alice": 95, "Bob": 87}'` |

## 参数选择 {#argument-selection}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [ARG_MAX](/tidb-cloud-lake/sql/arg-max.md) | 返回 expr2 最大时对应的 expr1 值 | `ARG_MAX(name, score)` → `'Alice'` |
| [ARG_MIN](/tidb-cloud-lake/sql/arg-min.md) | 返回 expr2 最小时对应的 expr1 值 | `ARG_MIN(name, score)` → `'Charlie'` |

## 漏斗分析 {#funnel-analysis}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [RETENTION](/tidb-cloud-lake/sql/retention.md) | 计算留存率 | `RETENTION(action = 'signup', action = 'purchase')` → `[100, 40]` |
| [WINDOWFUNNEL](/tidb-cloud-lake/sql/window-funnel.md) | 在时间窗口内搜索事件序列 | `WINDOWFUNNEL(1800)(timestamp, event='view', event='click', event='purchase')` → `2` |

## 匿名化 {#anonymization}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [MARKOV_TRAIN](/tidb-cloud-lake/sql/markov-train.md) | 训练 markov 模型 | `MARKOV_TRAIN(address)` |