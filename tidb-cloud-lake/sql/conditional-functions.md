---
title: 条件函数
summary: 本页按功能分类，全面概述了 {{{ .lake }}} 中的条件函数，便于参考。
---

# 条件函数

本页按功能分类，全面概述了 {{{ .lake }}} 中的条件函数，便于参考。

## 基本条件函数 {#basic-conditional-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [IF](/tidb-cloud-lake/sql/if.md) / [IFF](/tidb-cloud-lake/sql/iff.md) | 根据条件返回一个值 | `IF(1 > 0, 'yes', 'no')` → `'yes'` |
| [CASE](/tidb-cloud-lake/sql/case.md) | 对条件进行求值并返回匹配的结果 | `CASE WHEN 1 > 0 THEN 'yes' ELSE 'no' END` → `'yes'` |
| [DECODE](/tidb-cloud-lake/sql/decode.md) | 将表达式与搜索值进行比较并返回结果 | `DECODE(2, 1, 'one', 2, 'two', 'other')` → `'two'` |
| [COALESCE](/tidb-cloud-lake/sql/coalesce.md) | 返回第一个非 NULL 表达式 | `COALESCE(NULL, 'hello', 'world')` → `'hello'` |
| [NULLIF](/tidb-cloud-lake/sql/nullif.md) | 如果两个表达式相等则返回 NULL，否则返回第一个表达式 | `NULLIF(5, 5)` → `NULL` |
| [IFNULL](/tidb-cloud-lake/sql/ifnull.md) | 如果第一个表达式不是 NULL，则返回该表达式，否则返回第二个表达式 | `IFNULL(NULL, 'default')` → `'default'` |
| [NVL](/tidb-cloud-lake/sql/nvl.md) | 返回第一个非 NULL 表达式 | `NVL(NULL, 'default')` → `'default'` |
| [NVL2](/tidb-cloud-lake/sql/nvl2.md) | 如果 expr1 不是 NULL，则返回 expr2，否则返回 expr3 | `NVL2('value', 'not null', 'is null')` → `'not null'` |

## 比较函数 {#comparison-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [GREATEST](/tidb-cloud-lake/sql/greatest.md) | 返回列表中的最大值 | `GREATEST(1, 5, 3)` → `5` |
| [LEAST](/tidb-cloud-lake/sql/least.md) | 返回列表中的最小值 | `LEAST(1, 5, 3)` → `1` |
| [GREATEST_IGNORE_NULLS](/tidb-cloud-lake/sql/greatest-ignore-nulls.md) | 返回最大的非 NULL 值 | `GREATEST_IGNORE_NULLS(NULL, 5, 3)` → `5` |
| [LEAST_IGNORE_NULLS](/tidb-cloud-lake/sql/least-ignore-nulls.md) | 返回最小的非 NULL 值 | `LEAST_IGNORE_NULLS(NULL, 5, 3)` → `3` |
| [BETWEEN](/tidb-cloud-lake/sql/between.md) | 检查某个值是否位于指定范围内 | `5 BETWEEN 1 AND 10` → `true` |
| [IN](/tidb-cloud-lake/sql/in.md) | 检查某个值是否与列表中的任一值匹配 | `5 IN (1, 5, 10)` → `true` |

## NULL 和错误处理函数 {#null-and-error-handling-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [IS_NULL](/tidb-cloud-lake/sql/is-null.md) | 检查某个值是否为 NULL | `IS_NULL(NULL)` → `true` |
| [IS_NOT_NULL](/tidb-cloud-lake/sql/is-not-null.md) | 检查某个值是否不为 NULL | `IS_NOT_NULL('value')` → `true` |
| [IS_DISTINCT_FROM](/tidb-cloud-lake/sql/is-distinct-from.md) | 检查两个值是否不同，并将 NULL 视为相等 | `NULL IS DISTINCT FROM 0` → `true` |
| [IS_ERROR](/tidb-cloud-lake/sql/is-error.md) | 检查表达式求值是否产生错误 | `IS_ERROR(1/0)` → `true` |
| [IS_NOT_ERROR](/tidb-cloud-lake/sql/is-not-error.md) | 检查表达式求值是否未产生错误 | `IS_NOT_ERROR(1/1)` → `true` |
| [ERROR_OR](/tidb-cloud-lake/sql/error-or.md) | 如果第一个表达式不是错误，则返回该表达式，否则返回第二个表达式 | `ERROR_OR(1/0, 0)` → `0` |