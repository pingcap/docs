---
title: ST_ENVELOPE
summary: GEOMETRY オブジェクトの最小外接矩形を polygon として返します。
---

# ST_ENVELOPE

GEOMETRY オブジェクトの最小外接矩形を polygon として返します。

この関数は GEOMETRY 値のみをサポートします。

## 構文 {#syntax}

```sql
ST_ENVELOPE(<geometry>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|--------------|--------------------------------------------------------|
| `<geometry>` | 引数は GEOMETRY 型の式である必要があります。 |

## 戻り値の型 {#return-type}

GEOMETRY。

## 例 {#examples}

```sql
SELECT ST_ASWKT(ST_ENVELOPE(TO_GEOMETRY('LINESTRING(0 0, 2 3)')));

╭────────────────────────────────────────────────────────────╮
│ st_aswkt(st_envelope(to_geometry('LINESTRING(0 0, 2 3)'))) │
│                           String                           │
├────────────────────────────────────────────────────────────┤
│ POLYGON((0 0,2 0,2 3,0 3,0 0))                             │
╰────────────────────────────────────────────────────────────╯
```