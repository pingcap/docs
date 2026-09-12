---
title: CHAR
summary: 返回为每个传入的整数对应的字符。该函数会将每个整数转换为其对应的 Unicode 字符。
---

# CHAR

返回为每个传入的整数对应的字符。该函数会将每个整数转换为其对应的 Unicode 字符。

## 语法 {#syntax}

```sql
CHAR(N, ...)
CHR(N)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|----------------------------------------------------------------|
| N         | 表示 Unicode 码点的整数值（0 到 2^32-1） |

## 返回类型 {#return-type}

`STRING`

## 说明 {#remarks}

- 接受任意整数类型（自动转换为 Int64）。
- 对于无效的码点，返回空字符串（''）并记录错误日志。
- `chr` 是 `char` 的别名。
- 输入为 NULL 时，输出结果为 NULL。

## 示例 {#examples}

```sql
-- Basic usage
SELECT CHAR(65, 66, 67);
┌───────┐
│ char  │
│ String│
├───────┤
│ ABC   │
└───────┘

-- Using the CHR alias
SELECT CHR(68);
┌───────┐
│ chr   │
│ String│
├───────┤
│ D     │
└───────┘

-- Creating a string from multiple code points
SELECT CHAR(77,121,83,81,76);
┌───────┐
│ char  │
│ String│
├───────┤
│ MySQL │
└───────┘

-- Auto-casting from different integer types
SELECT CHAR(CAST(65 AS UInt16));
┌───────┐
│ char  │
│ String│
├───────┤
│ A     │
└───────┘

-- NULL handling
SELECT CHAR(NULL);
┌───────┐
│ char  │
│ String│
├───────┤
│ NULL  │
└───────┘
```