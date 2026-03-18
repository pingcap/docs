---
title: Aggregate Functions
summary: This page provides a comprehensive overview of aggregate functions in Databend, organized by functionality for easy reference.
---
This page provides a comprehensive overview of aggregate functions in Databend, organized by functionality for easy reference.

## Basic Aggregation

| Function | Description | Example |
|----------|-------------|---------|
| [COUNT](/tidb-cloud-lake/sql/count.md) | Counts the number of rows or non-NULL values | `COUNT(*)` → `10` |
| [COUNT_DISTINCT](/tidb-cloud-lake/sql/count-distinct.md) | Counts distinct values | `COUNT(DISTINCT city)` → `5` |
| [APPROX_COUNT_DISTINCT](/tidb-cloud-lake/sql/approx-count-distinct.md) | Approximates count of distinct values | `APPROX_COUNT_DISTINCT(user_id)` → `9955` |
| [SUM](/tidb-cloud-lake/sql/sum.md) | Calculates the sum of values | `SUM(sales)` → `1250.75` |
| [AVG](/tidb-cloud-lake/sql/avg.md) | Calculates the average of values | `AVG(temperature)` → `72.5` |
| [MIN](/tidb-cloud-lake/sql/min.md) | Returns the minimum value | `MIN(price)` → `9.99` |
| [MAX](/tidb-cloud-lake/sql/max.md) | Returns the maximum value | `MAX(price)` → `99.99` |
| [ANY_VALUE](/tidb-cloud-lake/sql/any-value.md) | Returns any value from the group | `ANY_VALUE(status)` → `'active'` |

## Conditional Aggregation

| Function | Description | Example |
|----------|-------------|---------|
| [COUNT_IF](/tidb-cloud-lake/sql/count-if.md) | Counts rows that match a condition | `COUNT_IF(price > 100)` → `5` |
| [SUM_IF](/tidb-cloud-lake/sql/sum-if.md) | Sums values that match a condition | `SUM_IF(amount, status = 'completed')` → `750.25` |
| [AVG_IF](/tidb-cloud-lake/sql/avg-if.md) | Averages values that match a condition | `AVG_IF(score, passed = true)` → `85.6` |
| [MIN_IF](/tidb-cloud-lake/sql/min-if.md) | Returns minimum where condition is true | `MIN_IF(temp, location = 'outside')` → `45.2` |
| [MAX_IF](/tidb-cloud-lake/sql/max-if.md) | Returns maximum where condition is true | `MAX_IF(speed, vehicle = 'car')` → `120.5` |

## Statistical Functions

| Function | Description | Example |
|----------|-------------|---------|
| [VAR_POP](/tidb-cloud-lake/sql/var-pop.md) / [VARIANCE_POP](/tidb-cloud-lake/sql/variance-pop.md) | Population variance | `VAR_POP(height)` → `10.25` |
| [VAR_SAMP](/tidb-cloud-lake/sql/var-samp.md) / [VARIANCE_SAMP](/tidb-cloud-lake/sql/variance-samp.md) | Sample variance | `VAR_SAMP(height)` → `12.3` |
| [STDDEV_POP](/tidb-cloud-lake/sql/stddev-pop.md) | Population standard deviation | `STDDEV_POP(height)` → `3.2` |
| [STDDEV_SAMP](/tidb-cloud-lake/sql/stddev-samp.md) | Sample standard deviation | `STDDEV_SAMP(height)` → `3.5` |
| [COVAR_POP](/tidb-cloud-lake/sql/covar-pop.md) | Population covariance | `COVAR_POP(x, y)` → `2.5` |
| [COVAR_SAMP](/tidb-cloud-lake/sql/covar-samp.md) | Sample covariance | `COVAR_SAMP(x, y)` → `2.7` |
| [KURTOSIS](/tidb-cloud-lake/sql/kurtosis.md) | Measures peakedness of distribution | `KURTOSIS(values)` → `2.1` |
| [SKEWNESS](/tidb-cloud-lake/sql/skewness.md) | Measures asymmetry of distribution | `SKEWNESS(values)` → `0.2` |

## Percentile and Distribution

| Function | Description | Example |
|----------|-------------|---------|
| [MEDIAN](/tidb-cloud-lake/sql/median.md) | Calculates the median value | `MEDIAN(response_time)` → `125` |
| [MODE](/tidb-cloud-lake/sql/mode.md) | Returns the most frequent value | `MODE(category)` → `'electronics'` |
| [QUANTILE_CONT](/tidb-cloud-lake/sql/quantile-cont.md) | Continuous interpolation quantile | `QUANTILE_CONT(0.95)(response_time)` → `350.5` |
| [QUANTILE_DISC](/tidb-cloud-lake/sql/quantile-disc.md) | Discrete quantile | `QUANTILE_DISC(0.5)(age)` → `35` |
| [QUANTILE_TDIGEST](/tidb-cloud-lake/sql/quantile-tdigest.md) | Approximate quantile using t-digest | `QUANTILE_TDIGEST(0.9)(values)` → `95.2` |
| [QUANTILE_TDIGEST_WEIGHTED](/tidb-cloud-lake/sql/quantile-tdigest-weighted.md) | Weighted t-digest quantile | `QUANTILE_TDIGEST_WEIGHTED(0.5)(values, weights)` → `50.5` |
| [MEDIAN_TDIGEST](/tidb-cloud-lake/sql/median-tdigest.md) | Approximate median using t-digest | `MEDIAN_TDIGEST(response_time)` → `124.5` |
| [HISTOGRAM](/tidb-cloud-lake/sql/histogram.md) | Creates histogram buckets | `HISTOGRAM(10)(values)` → `[{...}]` |

## Array and Collection Aggregation

| Function | Description | Example |
|----------|-------------|---------|
| [ARRAY_AGG](/tidb-cloud-lake/sql/array-agg.md) | Collects values into an array | `ARRAY_AGG(product)` → `['A', 'B', 'C']` |
| [GROUP_ARRAY_MOVING_AVG](/tidb-cloud-lake/sql/group-array-moving-avg.md) | Moving average over array | `GROUP_ARRAY_MOVING_AVG(3)(values)` → `[null, null, 3.0, 6.0, 9.0]` |
| [GROUP_ARRAY_MOVING_SUM](/tidb-cloud-lake/sql/group-array-moving-sum.md) | Moving sum over array | `GROUP_ARRAY_MOVING_SUM(2)(values)` → `[null, 3, 7, 11, 15]` |

## String Aggregation

| Function | Description | Example |
|----------|-------------|---------|
| [GROUP_CONCAT](/tidb-cloud-lake/sql/group-concat.md) | Concatenates values with separator | `GROUP_CONCAT(city, ', ')` → `'New York, London, Tokyo'` |
| [STRING_AGG](/tidb-cloud-lake/sql/string-agg.md) | Concatenates strings with separator | `STRING_AGG(tag, ',')` → `'red,green,blue'` |
| [LISTAGG](/tidb-cloud-lake/sql/listagg.md) | Concatenates values with separator | `LISTAGG(name, ', ')` → `'Alice, Bob, Charlie'` |

## JSON Aggregation

| Function | Description | Example |
|----------|-------------|---------|
| [JSON_ARRAY_AGG](/tidb-cloud-lake/sql/json-array-agg.md) | Aggregates values as JSON array | `JSON_ARRAY_AGG(name)` → `'["Alice", "Bob", "Charlie"]'` |
| [JSON_OBJECT_AGG](/tidb-cloud-lake/sql/json-object-agg.md) | Creates JSON object from key-value pairs | `JSON_OBJECT_AGG(name, score)` → `'{"Alice": 95, "Bob": 87}'` |

## Argument Selection

| Function | Description | Example |
|----------|-------------|---------|
| [ARG_MAX](/tidb-cloud-lake/sql/arg-max.md) | Returns value of expr1 at maximum expr2 | `ARG_MAX(name, score)` → `'Alice'` |
| [ARG_MIN](/tidb-cloud-lake/sql/arg-min.md) | Returns value of expr1 at minimum expr2 | `ARG_MIN(name, score)` → `'Charlie'` |

## Funnel Analysis

| Function | Description | Example |
|----------|-------------|---------|
| [RETENTION](/tidb-cloud-lake/sql/retention.md) | Calculates retention rates | `RETENTION(action = 'signup', action = 'purchase')` → `[100, 40]` |
| [WINDOWFUNNEL](/tidb-cloud-lake/sql/window-funnel.md) | Searches for event sequences within time window | `WINDOWFUNNEL(1800)(timestamp, event='view', event='click', event='purchase')` → `2` |

## Anonymization

| Function | Description | Example |
|----------|-------------|---------|
| [MARKOV_TRAIN](/tidb-cloud-lake/sql/markov-train.md) | train markov model | `MARKOV_TRAIN(address)` |
