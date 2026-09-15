---
title: ST_EQUALS
summary: 如果两个 GEOMETRY 对象在空间上相等，则返回 TRUE。
---

# ST_EQUALS

如果两个 GEOMETRY 对象在空间上相等，则返回 TRUE。

## 语法 {#syntax}

```sql
ST_EQUALS(<geometry1>, <geometry2>)
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
SELECT ST_EQUALS(
  TO_GEOMETRY('POINT(1 1)'),
  TO_GEOMETRY('POINT(1 1)')
) AS equals;

╭────────╮
│ equals │
├────────┤
│ true   │
╰────────╯

SELECT ST_EQUALS(
  TO_GEOMETRY('POINT(1 1)'),
  TO_GEOMETRY('POINT(1 2)')
) AS equals;

╭────────╮
│ equals │
├────────┤
│ false  │
╰────────╯
```