---
title: ST_HILBERT
summary: 将 GEOMETRY 或 GEOGRAPHY 对象编码为 Hilbert 曲线索引。
---

# ST_HILBERT

将 GEOMETRY 或 GEOGRAPHY 对象编码为 Hilbert 曲线索引。该函数使用几何对象边界框中心点作为待编码的点。提供边界时，会先将该点归一化到指定的边界框中，再进行编码。

## 语法 {#syntax}

```sql
ST_HILBERT(<geometry_or_geography>)
ST_HILBERT(<geometry_or_geography>, <bounds>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|-------------|
| `<geometry_or_geography>` | 该参数必须是 GEOMETRY 或 GEOGRAPHY 类型的表达式。 |
| `<bounds>` | 可选。一个数组 `[xmin, ymin, xmax, ymax]`，用于在编码前对点进行归一化。 |

> **注意：**
>
> - Geometry：如果未提供边界框，GEOMETRY 坐标不会被归一化到特定边界框。相反，中心点的值会被映射到完整的 `float32` 域中，然后编码为 Hilbert 索引。
> - Geography：如果未提供边界框，则默认边界为 `[-180, -90, 180, 90]`。

## 返回类型 {#return-type}

UInt64。

## 示例 {#examples}

### GEOMETRY 示例 {#geometry-examples}

```sql
SELECT ST_HILBERT(TO_GEOMETRY('POINT(1 2)')) AS hilbert1, ST_HILBERT(TO_GEOMETRY('POINT(5 5)')) AS hilbert2;

╭───────────────────────────╮
│   hilbert1  │   hilbert2  │
├─────────────┼─────────────┤
│  3355443200 │  2155872256 │
╰───────────────────────────╯

SELECT ST_HILBERT(TO_GEOMETRY('POINT(1 2)'), [0, 0, 1, 1]) AS hilbert1, ST_HILBERT(TO_GEOMETRY('POINT(5 5)'), [0, 0, 5, 5]) AS hilbert2;

╭───────────────────────────╮
│   hilbert1  │   hilbert2  │
├─────────────┼─────────────┤
│  2863311530 │  2863311530 │
╰───────────────────────────╯
```

### GEOGRAPHY 示例 {#geography-examples}

```sql
SELECT ST_HILBERT(TO_GEOGRAPHY('POINT(113.15 23.06)')) AS hilbert1, ST_HILBERT(TO_GEOGRAPHY('POINT(116.25 39.54)')) AS hilbert2;

╭───────────────────────────╮
│   hilbert1  │   hilbert2  │
├─────────────┼─────────────┤
│  3070259060 │  3033451300 │
╰───────────────────────────╯

SELECT ST_HILBERT(TO_GEOGRAPHY('POINT(113.15 23.06)'), [73, 4, 135, 53]) AS hilbert1, ST_HILBERT(TO_GEOGRAPHY('POINT(116.25 39.54)'), [73, 4, 135, 53]) AS hilbert2;

╭───────────────────────────╮
│   hilbert1  │   hilbert2  │
├─────────────┼─────────────┤
│  3533607194 │  2330429279 │
╰───────────────────────────╯
```