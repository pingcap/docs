---
title: GREAT_CIRCLE_ANGLE
summary: 返回球面上两点之间的中心角（以度为单位）。
---

# GREAT_CIRCLE_ANGLE

返回球面上两点之间的中心角（以度为单位）。这两个点使用经度和纬度（单位为度）指定。

## 语法 {#syntax}

```sql
GREAT_CIRCLE_ANGLE(<lon1>, <lat1>, <lon2>, <lat2>)
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
SELECT GREAT_CIRCLE_ANGLE(55.755831, 37.617673, -55.755831, -37.617673) AS angle;

╭───────────╮
│   angle   │
├───────────┤
│ 127.05919 │
╰───────────╯
```