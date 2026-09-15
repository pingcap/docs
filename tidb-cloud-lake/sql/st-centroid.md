---
title: ST_CENTROID
summary: 返回 GEOMETRY 对象的质心。
---

# ST_CENTROID

返回 GEOMETRY 对象的质心。

此函数仅支持 GEOMETRY 值。

## 语法 {#syntax}

```sql
ST_CENTROID(<geometry>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|--------------|--------------------------------------------------------|
| `<geometry>` | 该参数必须是 GEOMETRY 类型的表达式。 |

## 返回类型 {#return-type}

GEOMETRY。

## 示例 {#examples}

```sql
SELECT ST_ASWKT(ST_CENTROID(TO_GEOMETRY('POINT(1 2)')));

╭──────────────────────────────────────────────────╮
│ st_aswkt(st_centroid(to_geometry('POINT(1 2)'))) │
├──────────────────────────────────────────────────┤
│ POINT(1 2)                                       │
╰──────────────────────────────────────────────────╯
```

```sql
SELECT ST_ASWKT(ST_CENTROID(TO_GEOMETRY('LINESTRING(0 0, 2 0)')));

╭────────────────────────────────────────────────────────────╮
│ st_aswkt(st_centroid(to_geometry('LINESTRING(0 0, 2 0)'))) │
├────────────────────────────────────────────────────────────┤
│ POINT(1 0)                                                 │
╰────────────────────────────────────────────────────────────╯
```