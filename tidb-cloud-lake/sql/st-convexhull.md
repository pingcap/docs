---
title: ST_CONVEXHULL
summary: GEOMETRY オブジェクトの凸包を返します。
---

# ST_CONVEXHULL

GEOMETRY オブジェクトの凸包を返します。

## 構文 {#syntax}

```sql
ST_CONVEXHULL(<geometry>)
```

## 引数 {#arguments}

| 引数   | 説明                                           |
|-------------|-------------------------------------------------------|
| `<geometry>` | 引数は GEOMETRY 型の式である必要があります。 |

## 戻り値の型 {#return-type}

GEOMETRY。

## 例 {#examples}

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