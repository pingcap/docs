---
title: ST_CONTAINS
summary: 如果第二个 GEOMETRY 对象完全位于第一个 GEOMETRY 对象内部，则返回 TRUE。
---

# ST_CONTAINS

如果第二个 GEOMETRY 对象完全位于第一个 GEOMETRY 对象内部，则返回 TRUE。

## 语法 {#syntax}

```sql
ST_CONTAINS(<geometry1>, <geometry2>)
```

## 参数 {#arguments}

| 参数          | 描述                                                                 |
|---------------|----------------------------------------------------------------------|
| `<geometry1>` | 该参数必须是 GEOMETRY 对象类型的表达式，且不能是 GeometryCollection。 |
| `<geometry2>` | 该参数必须是 GEOMETRY 对象类型的表达式，且不能是 GeometryCollection。 |

> **注意：**
>
> - 如果两个输入的 GEOMETRY 对象具有不同的 SRID，则该函数会报错。

## 返回类型 {#return-type}

Boolean。

## 示例 {#examples}

```sql
SELECT ST_CONTAINS(TO_GEOMETRY('POLYGON((-2 0, 0 2, 2 0, -2 0))'), TO_GEOMETRY('POLYGON((-1 0, 0 1, 1 0, -1 0))')) AS contains

┌──────────┐
│ contains │
├──────────┤
│ true     │
└──────────┘

SELECT ST_CONTAINS(TO_GEOMETRY('POLYGON((-2 0, 0 2, 2 0, -2 0))'), TO_GEOMETRY('LINESTRING(-1 1, 0 2, 1 1)')) AS contains

┌──────────┐
│ contains │
├──────────┤
│ false    │
└──────────┘

SELECT ST_CONTAINS(TO_GEOMETRY('POLYGON((-2 0, 0 2, 2 0, -2 0))'), TO_GEOMETRY('LINESTRING(-2 0, 0 0, 0 1)')) AS contains

┌──────────┐
│ contains │
├──────────┤
│ true     │
└──────────┘

```