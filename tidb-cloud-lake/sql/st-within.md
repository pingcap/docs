---
title: ST_WITHIN
summary: 如果第一个 GEOMETRY 对象完全位于第二个 GEOMETRY 对象之内，则返回 TRUE。
---

# ST_WITHIN

如果第一个 GEOMETRY 对象完全位于第二个 GEOMETRY 对象之内，则返回 TRUE。

## 语法 {#syntax}

```sql
ST_WITHIN(<geometry1>, <geometry2>)
```

## 参数 {#arguments}

| 参数          | 描述                                      |
|---------------|-------------------------------------------|
| `<geometry1>` | 该参数必须是 GEOMETRY 类型的表达式。 |
| `<geometry2>` | 该参数必须是 GEOMETRY 类型的表达式。 |

> **注意：**
>
> 如果两个输入的 GEOMETRY 对象具有不同的 SRID，则该函数会报错。

## 返回类型 {#return-type}

布尔值。

## 示例 {#examples}

```sql
SELECT ST_WITHIN(
  TO_GEOMETRY('POINT(1 1)'),
  TO_GEOMETRY('POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))')
) AS within;

╭─────────╮
│  within │
├─────────┤
│ true    │
╰─────────╯
```