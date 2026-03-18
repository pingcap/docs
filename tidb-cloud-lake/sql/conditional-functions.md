---
title: Conditional Functions
summary: This page provides a comprehensive overview of Conditional functions in Databend, organized by functionality for easy reference.
---

# Conditional Functions

This page provides a comprehensive overview of Conditional functions in Databend, organized by functionality for easy reference.

## Basic Conditional Functions

| Function | Description | Example |
|----------|-------------|---------|
| [IF](/tidb-cloud-lake/sql/if.md) / [IFF](/tidb-cloud-lake/sql/iff.md) | Returns a value based on a condition | `IF(1 > 0, 'yes', 'no')` → `'yes'` |
| [CASE](/tidb-cloud-lake/sql/case.md) | Evaluates conditions and returns a matching result | `CASE WHEN 1 > 0 THEN 'yes' ELSE 'no' END` → `'yes'` |
| [DECODE](/tidb-cloud-lake/sql/decode.md) | Compares expression to search values and returns result | `DECODE(2, 1, 'one', 2, 'two', 'other')` → `'two'` |
| [COALESCE](/tidb-cloud-lake/sql/coalesce.md) | Returns the first non-NULL expression | `COALESCE(NULL, 'hello', 'world')` → `'hello'` |
| [NULLIF](/tidb-cloud-lake/sql/nullif.md) | Returns NULL if two expressions are equal, otherwise the first expression | `NULLIF(5, 5)` → `NULL` |
| [IFNULL](/tidb-cloud-lake/sql/ifnull.md) | Returns the first expression if not NULL, otherwise the second | `IFNULL(NULL, 'default')` → `'default'` |
| [NVL](/tidb-cloud-lake/sql/nvl.md) | Returns the first non-NULL expression | `NVL(NULL, 'default')` → `'default'` |
| [NVL2](/tidb-cloud-lake/sql/nvl2.md) | Returns expr2 if expr1 is not NULL, otherwise expr3 | `NVL2('value', 'not null', 'is null')` → `'not null'` |

## Comparison Functions

| Function | Description | Example |
|----------|-------------|---------|
| [GREATEST](/tidb-cloud-lake/sql/greatest.md) | Returns the largest value from a list | `GREATEST(1, 5, 3)` → `5` |
| [LEAST](/tidb-cloud-lake/sql/least.md) | Returns the smallest value from a list | `LEAST(1, 5, 3)` → `1` |
| [GREATEST_IGNORE_NULLS](/tidb-cloud-lake/sql/greatest-ignore-nulls.md) | Returns the largest non-NULL value | `GREATEST_IGNORE_NULLS(NULL, 5, 3)` → `5` |
| [LEAST_IGNORE_NULLS](/tidb-cloud-lake/sql/least-ignore-nulls.md) | Returns the smallest non-NULL value | `LEAST_IGNORE_NULLS(NULL, 5, 3)` → `3` |
| [BETWEEN](/tidb-cloud-lake/sql/between.md) | Checks if a value is within a range | `5 BETWEEN 1 AND 10` → `true` |
| [IN](/tidb-cloud-lake/sql/in.md) | Checks if a value matches any value in a list | `5 IN (1, 5, 10)` → `true` |

## NULL and Error Handling Functions

| Function | Description | Example |
|----------|-------------|---------|
| [IS_NULL](/tidb-cloud-lake/sql/is-null.md) | Checks if a value is NULL | `IS_NULL(NULL)` → `true` |
| [IS_NOT_NULL](/tidb-cloud-lake/sql/is-not-null.md) | Checks if a value is not NULL | `IS_NOT_NULL('value')` → `true` |
| [IS_DISTINCT_FROM](/tidb-cloud-lake/sql/is-distinct-from.md) | Checks if two values are different, treating NULLs as equal | `NULL IS DISTINCT FROM 0` → `true` |
| [IS_ERROR](/tidb-cloud-lake/sql/is-error.md) | Checks if an expression evaluation resulted in an error | `IS_ERROR(1/0)` → `true` |
| [IS_NOT_ERROR](/tidb-cloud-lake/sql/is-not-error.md) | Checks if an expression evaluation did not result in an error | `IS_NOT_ERROR(1/1)` → `true` |
| [ERROR_OR](/tidb-cloud-lake/sql/error-or.md) | Returns the first expression if it's not an error, otherwise the second | `ERROR_OR(1/0, 0)` → `0` |
