---
title: ST_ISVALID
summary: 如果 GEOMETRY 对象在几何上有效（由 OGC 规范定义），则返回 TRUE。
---

# ST_ISVALID

如果 GEOMETRY 对象在几何上有效（由 OGC 规范定义），则返回 TRUE。

## 语法 {#syntax}

```sql
ST_ISVALID(<geometry>)
```

## 参数 {#arguments}

| 参数         | 描述                  |
|--------------|-----------------------|
| `<geometry>` | 一个 GEOMETRY 表达式。 |

## 返回类型 {#return-type}

布尔型。

## 示例 {#examples}

```sql
SELECT ST_ISVALID(TO_GEOMETRY('POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))'));

┌──────────────────────────────────────────────────────────┐
│ st_isvalid(to_geometry('polygon((0 0, 1 0, 1 1, 0 1, 0 0))')) │
├──────────────────────────────────────────────────────────┤
│ true                                                          │
└──────────────────────────────────────────────────────────┘

-- Self-intersecting polygon (bowtie shape) is invalid
SELECT ST_ISVALID(TO_GEOMETRY('POLYGON((0 0, 2 2, 2 0, 0 2, 0 0))'));

┌──────────────────────────────────────────────────────────────┐
│ st_isvalid(to_geometry('polygon((0 0, 2 2, 2 0, 0 2, 0 0))')) │
├──────────────────────────────────────────────────────────────┤
│ false                                                             │
└──────────────────────────────────────────────────────────────┘
```