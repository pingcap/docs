---
title: ST_CENTROID
summary: GEOMETRY オブジェクトの重心を返します。
---

# ST_CENTROID

GEOMETRY オブジェクトの重心を返します。

この関数は GEOMETRY 値のみをサポートします。

## 構文 {#syntax}

```sql
ST_CENTROID(<geometry>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|--------------|--------------------------------------------------------|
| `<geometry>` | 引数は GEOMETRY 型の式である必要があります。 |

## 戻り値の型 {#return-type}

GEOMETRY。

## 例 {#examples}

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