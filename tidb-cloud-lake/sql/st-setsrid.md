---
title: ST_SETSRID
summary: SRID（空間参照系識別子）が指定した値に設定された GEOMETRY オブジェクトを返します。この関数は、オブジェクトの座標に影響を与えずに SRID のみを変更します。新しい SRS（空間参照系）に合わせて座標も変更する必要がある場合は、代わりに ST_TRANSFORM を使用してください。
---

# ST_SETSRID

[SRID（空間参照系識別子）](https://en.wikipedia.org/wiki/Spatial_reference_system#Identifier) が指定した値に設定された GEOMETRY オブジェクトを返します。この関数は、オブジェクトの座標に影響を与えずに SRID のみを変更します。新しい SRS（空間参照系）に合わせて座標も変更する必要がある場合は、代わりに [ST_TRANSFORM](/tidb-cloud-lake/sql/st-transform.md) を使用してください。

## 構文 {#syntax}

```sql
ST_SETSRID(<geometry>, <srid>)
```

## 引数 {#arguments}

| 引数         | 説明                                                        |
|--------------|-------------------------------------------------------------|
| `<geometry>` | 引数は GEOMETRY オブジェクト型の式である必要があります。   |
| `<srid>`     | 返される GEOMETRY オブジェクトに設定する SRID の整数値。   |

## 戻り値の型 {#return-type}

Geometry。

## 例 {#examples}

```sql
SET GEOMETRY_OUTPUT_FORMAT = 'EWKT'

SELECT ST_SETSRID(TO_GEOMETRY('POINT(13 51)'), 4326) AS geometry

┌────────────────────────┐
│        geometry        │
├────────────────────────┤
│ SRID=4326;POINT(13 51) │
└────────────────────────┘

```