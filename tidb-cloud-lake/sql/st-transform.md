---
title: ST_TRANSFORM
summary: GEOMETRY オブジェクトをある空間参照系 (SRS) から別の空間参照系へ変換します。座標を変更せずに SRID のみを変更する必要がある場合（たとえば SRID が誤っていた場合）は、代わりに ST_SETSRID を使用してください。
---

# ST_TRANSFORM

GEOMETRY オブジェクトを、ある[空間参照系 (SRS)](https://en.wikipedia.org/wiki/Spatial_reference_system) から別のものへ変換します。座標を変更せずに SRID のみを変更する必要がある場合（たとえば SRID が誤っていた場合）は、代わりに [ST_SETSRID](/tidb-cloud-lake/sql/st-setsrid.md) を使用してください。

## 構文 {#syntax}

```sql
ST_TRANSFORM(<geometry> [, <from_srid>], <to_srid>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| `<geometry>`  | 引数は GEOMETRY オブジェクト型の式である必要があります。 |
| `<from_srid>` | 入力 GEOMETRY オブジェクトの現在の SRS を識別する省略可能な SRID です。この引数を省略した場合は、入力 GEOMETRY オブジェクトで指定されている SRID を使用します。 |
| `<to_srid>`   | 使用する SRS を識別する SRID です。入力 GEOMETRY オブジェクトを、この SRS を使用する新しいオブジェクトに変換します。 |

## 戻り値の型 {#return-type}

Geometry。

## 例 {#examples}

```sql
SET GEOMETRY_OUTPUT_FORMAT = 'EWKT'

SELECT ST_TRANSFORM(ST_GEOMFROMWKT('POINT(389866.35 5819003.03)', 32633), 3857) AS transformed_geom

┌───────────────────────────────────────────────┐
│                transformed_geom               │
├───────────────────────────────────────────────┤
│ SRID=3857;POINT(1489140.093766 6892872.19868) │
└───────────────────────────────────────────────┘

SELECT ST_TRANSFORM(ST_GEOMFROMWKT('POINT(4.500212 52.161170)'), 4326, 28992) AS transformed_geom

┌──────────────────────────────────────────────┐
│               transformed_geom               │
├──────────────────────────────────────────────┤
│ SRID=28992;POINT(94308.670475 464038.168827) │
└──────────────────────────────────────────────┘

```