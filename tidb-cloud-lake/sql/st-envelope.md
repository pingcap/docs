---
title: ST_ENVELOPE
summary: 以多边形形式返回 GEOMETRY 对象的最小外接矩形。
---

# ST_ENVELOPE

以多边形形式返回 GEOMETRY 对象的最小外接矩形。

该函数仅支持 GEOMETRY 值。

## 语法 {#syntax}

```sql
ST_ENVELOPE(<geometry>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|--------------|--------------------------------------------------------|
| `<geometry>` | 该参数必须是 GEOMETRY 类型的表达式。 |

## 返回类型 {#return-type}

GEOMETRY。

## 示例 {#examples}

```sql
SELECT ST_ASWKT(ST_ENVELOPE(TO_GEOMETRY('LINESTRING(0 0, 2 3)')));

╭────────────────────────────────────────────────────────────╮
│ st_aswkt(st_envelope(to_geometry('LINESTRING(0 0, 2 3)'))) │
│                           String                           │
├────────────────────────────────────────────────────────────┤
│ POLYGON((0 0,2 0,2 3,0 3,0 0))                             │
╰────────────────────────────────────────────────────────────╯
```