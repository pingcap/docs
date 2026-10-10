---
title: ST_COVERS
summary: 2 番目の GEOMETRY オブジェクトのどの点も、1 番目の GEOMETRY オブジェクトの外側に存在しない場合に TRUE を返します。
---

# ST_COVERS

2 番目の GEOMETRY オブジェクトのどの点も、1 番目の GEOMETRY オブジェクトの外側に存在しない場合に TRUE を返します。

関連情報: [ST_COVEREDBY](/tidb-cloud-lake/sql/st-coveredby.md)

## 構文 {#syntax}

```sql
ST_COVERS(<geometry1>, <geometry2>)
```

## 引数 {#arguments}

| 引数          | 説明                                                   |
|---------------|--------------------------------------------------------|
| `<geometry1>` | GEOMETRY 式（包含するオブジェクト）。                  |
| `<geometry2>` | GEOMETRY 式（判定対象のオブジェクト）。                |

## 戻り値の型 {#return-type}

Boolean。

## 例 {#examples}

```sql
-- A polygon covers a smaller polygon inside it
SELECT ST_COVERS(
  TO_GEOMETRY('POLYGON((-2 0, 0 2, 2 0, -2 0))'),
  TO_GEOMETRY('POLYGON((-1 0, 0 1, 1 0, -1 0))')
);

┌────────┐
│ result │
├────────┤
│ true   │
└────────┘

-- A polygon covers a linestring on its boundary
SELECT ST_COVERS(
  TO_GEOMETRY('POLYGON((-2 0, 0 2, 2 0, -2 0))'),
  TO_GEOMETRY('LINESTRING(-1 1, 0 2, 1 1)')
);

┌────────┐
│ result │
├────────┤
│ true   │
└────────┘

-- A point outside the polygon is not covered
SELECT ST_COVERS(
  TO_GEOMETRY('POLYGON((0 0, 3 0, 3 3, 0 3, 0 0))'),
  TO_GEOMETRY('POINT(5 5)')
);

┌────────┐
│ result │
├────────┤
│ false  │
└────────┘
```