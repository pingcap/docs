---
title: 'Conditional Functions'
---

This page provides a comprehensive overview of Conditional functions in Databend, organized by functionality for easy reference.

## Basic Conditional Functions

| Function | Description | Example |
|----------|-------------|---------|
| [IF](if.md) / [IFF](iff.md) | Returns a value based on a condition | `IF(1 > 0, 'yes', 'no')` → `'yes'` |
| [CASE](case.md) | Evaluates conditions and returns a matching result | `CASE WHEN 1 > 0 THEN 'yes' ELSE 'no' END` → `'yes'` |
| [DECODE](decode.md) | Compares expression to search values and returns result | `DECODE(2, 1, 'one', 2, 'two', 'other')` → `'two'` |
| [COALESCE](coalesce.md) | Returns the first non-NULL expression | `COALESCE(NULL, 'hello', 'world')` → `'hello'` |
| [NULLIF](nullif.md) | Returns NULL if two expressions are equal, otherwise the first expression | `NULLIF(5, 5)` → `NULL` |
| [IFNULL](ifnull.md) | Returns the first expression if not NULL, otherwise the second | `IFNULL(NULL, 'default')` → `'default'` |
| [NVL](nvl.md) | Returns the first non-NULL expression | `NVL(NULL, 'default')` → `'default'` |
| [NVL2](nvl2.md) | Returns expr2 if expr1 is not NULL, otherwise expr3 | `NVL2('value', 'not null', 'is null')` → `'not null'` |

## Comparison Functions

| Function | Description | Example |
|----------|-------------|---------|
| [GREATEST](greatest.md) | Returns the largest value from a list | `GREATEST(1, 5, 3)` → `5` |
| [LEAST](least.md) | Returns the smallest value from a list | `LEAST(1, 5, 3)` → `1` |
| [GREATEST_IGNORE_NULLS](greatest-ignore-nulls.md) | Returns the largest non-NULL value | `GREATEST_IGNORE_NULLS(NULL, 5, 3)` → `5` |
| [LEAST_IGNORE_NULLS](least-ignore-nulls.md) | Returns the smallest non-NULL value | `LEAST_IGNORE_NULLS(NULL, 5, 3)` → `3` |
| [BETWEEN](between.md) | Checks if a value is within a range | `5 BETWEEN 1 AND 10` → `true` |
| [IN](in.md) | Checks if a value matches any value in a list | `5 IN (1, 5, 10)` → `true` |

## NULL and Error Handling Functions

| Function | Description | Example |
|----------|-------------|---------|
| [IS_NULL](is-null.md) | Checks if a value is NULL | `IS_NULL(NULL)` → `true` |
| [IS_NOT_NULL](is-not-null.md) | Checks if a value is not NULL | `IS_NOT_NULL('value')` → `true` |
| [IS_DISTINCT_FROM](is-distinct-from.md) | Checks if two values are different, treating NULLs as equal | `NULL IS DISTINCT FROM 0` → `true` |
| [IS_ERROR](is-error.md) | Checks if an expression evaluation resulted in an error | `IS_ERROR(1/0)` → `true` |
| [IS_NOT_ERROR](is-not-error.md) | Checks if an expression evaluation did not result in an error | `IS_NOT_ERROR(1/1)` → `true` |
| [ERROR_OR](error-or.md) | Returns the first expression if it's not an error, otherwise the second | `ERROR_OR(1/0, 0)` → `0` |
