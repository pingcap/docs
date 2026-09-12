---
title: ST_INTERSECTION
summary: 返回两个 GEOMETRY 对象的共享部分。
---

# ST_INTERSECTION

返回两个 GEOMETRY 对象的共享部分。

此函数仅支持 GEOMETRY 值。

## 语法 {#syntax}

```sql
ST_INTERSECTION(<geometry1>, <geometry2>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|---------------|--------------------------------------------------------|
| `<geometry1>` | 该参数必须是 GEOMETRY 类型的表达式。 |
| `<geometry2>` | 该参数必须是 GEOMETRY 类型的表达式。 |

> **注意：**
>
> 如果两个输入的 GEOMETRY 对象具有不同的 SRID，则该函数会报错。

## 返回类型 {#return-type}

GEOMETRY。

## 示例 {#examples}

```sql
SELECT ST_ASWKT(ST_INTERSECTION(TO_GEOMETRY('LINESTRING(0 0, 1 1)'), TO_GEOMETRY('LINESTRING(0 0, 1 1)')));

╭─────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ st_aswkt(st_intersection(to_geometry('LINESTRING(0 0, 1 1)'), to_geometry('LINESTRING(0 0, 1 1)'))) │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ LINESTRING(0 0,1 1)                                                                                 │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯
```