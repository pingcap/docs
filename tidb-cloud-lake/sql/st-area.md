---
title: ST_AREA
summary: 返回 GEOMETRY 或 GEOGRAPHY 对象的面积。对于 GEOMETRY 输入，该函数基于 [shoelace formula](https://en.wikipedia.org/wiki/Shoelace_formula) 计算平面面积。对于 GEOGRAPHY 输入，该函数使用 [Karney (2013)](https://arxiv.org/pdf/1109.4448.pdf) 中描述的方法，在地球椭球模型上测量测地面积。
---

# ST_AREA

返回 GEOMETRY 或 GEOGRAPHY 对象的面积。对于 GEOMETRY 输入，该函数基于 [shoelace formula](https://en.wikipedia.org/wiki/Shoelace_formula) 计算平面面积。对于 GEOGRAPHY 输入，该函数使用 [Karney (2013)](https://arxiv.org/pdf/1109.4448.pdf) 中描述的方法，在地球椭球模型上测量测地面积。

## 语法 {#syntax}

```sql
ST_AREA(<geometry_or_geography>)
```

## 参数 {#arguments}

| 参数                      | 描述                                                            |
|---------------------------|-----------------------------------------------------------------|
| `<geometry_or_geography>` | 该参数必须是 GEOMETRY 或 GEOGRAPHY 类型的表达式。 |

## 返回类型 {#return-type}

Double。

## 示例 {#examples}

### GEOMETRY 示例 {#geometry-examples}

```sql
SELECT
  ST_AREA(
    TO_GEOMETRY('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))')
  ) AS area

┌──────┐
│ area │
├──────┤
│ 1.0  │
└──────┘
```

### GEOGRAPHY 示例 {#geography-examples}

```sql
SELECT
  ST_AREA(
    TO_GEOGRAPHY('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))')
  ) AS area

╭────────────────────╮
│        area        │
├────────────────────┤
│ 12308778361.469452 │
╰────────────────────╯
```