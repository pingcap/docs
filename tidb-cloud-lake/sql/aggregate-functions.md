---
title: 'Aggregate Functions'
---

This page provides a comprehensive overview of aggregate functions in Databend, organized by functionality for easy reference.

## Basic Aggregation

| Function | Description | Example |
|----------|-------------|---------|
| [COUNT](aggregate-count.md) | Counts the number of rows or non-NULL values | `COUNT(*)` → `10` |
| [COUNT_DISTINCT](aggregate-count-distinct.md) | Counts distinct values | `COUNT(DISTINCT city)` → `5` |
| [APPROX_COUNT_DISTINCT](aggregate-approx-count-distinct.md) | Approximates count of distinct values | `APPROX_COUNT_DISTINCT(user_id)` → `9955` |
| [SUM](aggregate-sum.md) | Calculates the sum of values | `SUM(sales)` → `1250.75` |
| [AVG](aggregate-avg.md) | Calculates the average of values | `AVG(temperature)` → `72.5` |
| [MIN](aggregate-min.md) | Returns the minimum value | `MIN(price)` → `9.99` |
| [MAX](aggregate-max.md) | Returns the maximum value | `MAX(price)` → `99.99` |
| [ANY_VALUE](aggregate-any-value.md) | Returns any value from the group | `ANY_VALUE(status)` → `'active'` |

## Conditional Aggregation

| Function | Description | Example |
|----------|-------------|---------|
| [COUNT_IF](aggregate-count-if.md) | Counts rows that match a condition | `COUNT_IF(price > 100)` → `5` |
| [SUM_IF](aggregate-sum-if.md) | Sums values that match a condition | `SUM_IF(amount, status = 'completed')` → `750.25` |
| [AVG_IF](aggregate-avg-if.md) | Averages values that match a condition | `AVG_IF(score, passed = true)` → `85.6` |
| [MIN_IF](aggregate-min-if.md) | Returns minimum where condition is true | `MIN_IF(temp, location = 'outside')` → `45.2` |
| [MAX_IF](aggregate-max-if.md) | Returns maximum where condition is true | `MAX_IF(speed, vehicle = 'car')` → `120.5` |

## Statistical Functions

| Function | Description | Example |
|----------|-------------|---------|
| [VAR_POP](aggregate-var-pop.md) / [VARIANCE_POP](aggregate-variance-pop.md) | Population variance | `VAR_POP(height)` → `10.25` |
| [VAR_SAMP](aggregate-var-samp.md) / [VARIANCE_SAMP](aggregate-variance-samp.md) | Sample variance | `VAR_SAMP(height)` → `12.3` |
| [STDDEV_POP](aggregate-stddev-pop.md) | Population standard deviation | `STDDEV_POP(height)` → `3.2` |
| [STDDEV_SAMP](aggregate-stddev-samp.md) | Sample standard deviation | `STDDEV_SAMP(height)` → `3.5` |
| [COVAR_POP](aggregate-covar-pop.md) | Population covariance | `COVAR_POP(x, y)` → `2.5` |
| [COVAR_SAMP](aggregate-covar-samp.md) | Sample covariance | `COVAR_SAMP(x, y)` → `2.7` |
| [KURTOSIS](aggregate-kurtosis.md) | Measures peakedness of distribution | `KURTOSIS(values)` → `2.1` |
| [SKEWNESS](aggregate-skewness.md) | Measures asymmetry of distribution | `SKEWNESS(values)` → `0.2` |

## Percentile and Distribution

| Function | Description | Example |
|----------|-------------|---------|
| [MEDIAN](aggregate-median.md) | Calculates the median value | `MEDIAN(response_time)` → `125` |
| [MODE](aggregate-mode.md) | Returns the most frequent value | `MODE(category)` → `'electronics'` |
| [QUANTILE_CONT](aggregate-quantile-cont.md) | Continuous interpolation quantile | `QUANTILE_CONT(0.95)(response_time)` → `350.5` |
| [QUANTILE_DISC](aggregate-quantile-disc.md) | Discrete quantile | `QUANTILE_DISC(0.5)(age)` → `35` |
| [QUANTILE_TDIGEST](aggregate-quantile-tdigest.md) | Approximate quantile using t-digest | `QUANTILE_TDIGEST(0.9)(values)` → `95.2` |
| [QUANTILE_TDIGEST_WEIGHTED](aggregate-quantile-tdigest-weighted.md) | Weighted t-digest quantile | `QUANTILE_TDIGEST_WEIGHTED(0.5)(values, weights)` → `50.5` |
| [MEDIAN_TDIGEST](aggregate-median-tdigest.md) | Approximate median using t-digest | `MEDIAN_TDIGEST(response_time)` → `124.5` |
| [HISTOGRAM](aggregate-histogram.md) | Creates histogram buckets | `HISTOGRAM(10)(values)` → `[{...}]` |

## Array and Collection Aggregation

| Function | Description | Example |
|----------|-------------|---------|
| [ARRAY_AGG](aggregate-array-agg.md) | Collects values into an array | `ARRAY_AGG(product)` → `['A', 'B', 'C']` |
| [GROUP_ARRAY_MOVING_AVG](aggregate-group-array-moving-avg.md) | Moving average over array | `GROUP_ARRAY_MOVING_AVG(3)(values)` → `[null, null, 3.0, 6.0, 9.0]` |
| [GROUP_ARRAY_MOVING_SUM](aggregate-group-array-moving-sum.md) | Moving sum over array | `GROUP_ARRAY_MOVING_SUM(2)(values)` → `[null, 3, 7, 11, 15]` |

## String Aggregation

| Function | Description | Example |
|----------|-------------|---------|
| [GROUP_CONCAT](aggregate-group-concat.md) | Concatenates values with separator | `GROUP_CONCAT(city, ', ')` → `'New York, London, Tokyo'` |
| [STRING_AGG](aggregate-string-agg.md) | Concatenates strings with separator | `STRING_AGG(tag, ',')` → `'red,green,blue'` |
| [LISTAGG](aggregate-listagg.md) | Concatenates values with separator | `LISTAGG(name, ', ')` → `'Alice, Bob, Charlie'` |

## JSON Aggregation

| Function | Description | Example |
|----------|-------------|---------|
| [JSON_ARRAY_AGG](aggregate-json-array-agg.md) | Aggregates values as JSON array | `JSON_ARRAY_AGG(name)` → `'["Alice", "Bob", "Charlie"]'` |
| [JSON_OBJECT_AGG](aggregate-json-object-agg.md) | Creates JSON object from key-value pairs | `JSON_OBJECT_AGG(name, score)` → `'{"Alice": 95, "Bob": 87}'` |

## Argument Selection

| Function | Description | Example |
|----------|-------------|---------|
| [ARG_MAX](aggregate-arg-max.md) | Returns value of expr1 at maximum expr2 | `ARG_MAX(name, score)` → `'Alice'` |
| [ARG_MIN](aggregate-arg-min.md) | Returns value of expr1 at minimum expr2 | `ARG_MIN(name, score)` → `'Charlie'` |

## Funnel Analysis

| Function | Description | Example |
|----------|-------------|---------|
| [RETENTION](aggregate-retention.md) | Calculates retention rates | `RETENTION(action = 'signup', action = 'purchase')` → `[100, 40]` |
| [WINDOWFUNNEL](aggregate-windowfunnel.md) | Searches for event sequences within time window | `WINDOWFUNNEL(1800)(timestamp, event='view', event='click', event='purchase')` → `2` |

## Anonymization

| Function | Description | Example |
|----------|-------------|---------|
| [MARKOV_TRAIN](aggregate-markov-train.md) | train markov model | `MARKOV_TRAIN(address)` |
