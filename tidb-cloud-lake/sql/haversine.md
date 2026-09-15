---
title: HAVERSINE
summary: 使用 [Haversine formula](https://en.wikipedia.org/wiki/Haversine_formula) 计算地球表面两点之间的大圆距离，单位为千米。这两个点通过其以度为单位的纬度和经度指定。
---

# HAVERSINE

使用 [Haversine formula](https://en.wikipedia.org/wiki/Haversine_formula) 计算地球表面两点之间的大圆距离，单位为千米。这两个点通过其以度为单位的纬度和经度指定。

## 语法 {#syntax}

```sql
HAVERSINE(<lat1>, <lon1>, <lat2>, <lon2>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|------------------------------------|
| `<lat1>`  | 第一个点的纬度。   |
| `<lon1>`  | 第一个点的经度。  |
| `<lat2>`  | 第二个点的纬度。  |
| `<lon2>`  | 第二个点的经度。 |

## 返回类型 {#return-type}

Double。

## 示例 {#examples}

```sql
SELECT
  HAVERSINE(40.7127, -74.0059, 34.0500, -118.2500) AS distance

┌────────────────┐
│    distance    │
├────────────────┤
│ 3936.390533556 │
└────────────────┘
```