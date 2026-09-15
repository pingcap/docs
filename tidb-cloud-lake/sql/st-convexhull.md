---
title: ST_CONVEXHULL
summary: 返回 GEOMETRY 对象的凸包。
---

# ST_CONVEXHULL

返回 GEOMETRY 对象的凸包。

## 语法 {#syntax}

```sql
ST_CONVEXHULL(<geometry>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-------------|-------------------------------------------------------|
| `<geometry>` | 该参数必须是 GEOMETRY 类型的表达式。 |

## 返回类型 {#return-type}

GEOMETRY。

## 示例 {#examples}

```sql
SELECT ST_ASTEXT(
  ST_CONVEXHULL(
    TO_GEOMETRY('POLYGON((0 0, 2 0, 2 2, 0 2, 0 0))')
  )
) AS hull;

╭────────────────────────────────╮
│              hull              │
├────────────────────────────────┤
│ POLYGON((2 0,2 2,0 2,0 0,2 0)) │
╰────────────────────────────────╯
```