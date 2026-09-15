---
title: GREAT_CIRCLE_DISTANCE
summary: 返回球面上两点之间的大圆距离，单位为米。
---

# GREAT_CIRCLE_DISTANCE

返回球面上两点之间的大圆距离，单位为米。点的位置使用以度为单位的经度和纬度指定。

## 语法 {#syntax}

```sql
GREAT_CIRCLE_DISTANCE(<lon1>, <lat1>, <lon2>, <lat2>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|-------------|
| `<lon1>` | 第一个点的经度，单位为度。 |
| `<lat1>` | 第一个点的纬度，单位为度。 |
| `<lon2>` | 第二个点的经度，单位为度。 |
| `<lat2>` | 第二个点的纬度，单位为度。 |

## 返回类型 {#return-type}

Float32。

## 示例 {#examples}

```sql
SELECT GREAT_CIRCLE_DISTANCE(55.755831, 37.617673, -55.755831, -37.617673) AS distance;

╭────────────╮
│  distance  │
├────────────┤
│ 14128353.0 │
╰────────────╯
```