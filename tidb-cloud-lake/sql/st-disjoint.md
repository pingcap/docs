---
title: ST_DISJOINT
summary: 如果两个 GEOMETRY 对象不相交，则返回 TRUE。
---

# ST_DISJOINT

如果两个 GEOMETRY 对象不相交，则返回 TRUE。

## 语法 {#syntax}

```sql
ST_DISJOINT(<geometry1>, <geometry2>)
```

## 参数 {#arguments}

| 参数          | 描述                                  |
|---------------|---------------------------------------|
| `<geometry1>` | 该参数必须是 GEOMETRY 类型的表达式。 |
| `<geometry2>` | 该参数必须是 GEOMETRY 类型的表达式。 |

> **注意：**
>
> 如果两个输入的 GEOMETRY 对象具有不同的 SRID，则该函数会报错。

## 返回类型 {#return-type}

布尔值。

## 示例 {#examples}

```sql
SELECT ST_DISJOINT(
  TO_GEOMETRY('POINT(3 3)'),
  TO_GEOMETRY('POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))')
) AS disjoint;

╭──────────╮
│ disjoint │
├──────────┤
│ true     │
╰──────────╯

SELECT ST_DISJOINT(
  TO_GEOMETRY('LINESTRING(0 0, 2 2)'),
  TO_GEOMETRY('LINESTRING(0 2, 2 0)')
) AS disjoint;

╭──────────╮
│ disjoint │
├──────────┤
│ false    │
╰──────────╯
```