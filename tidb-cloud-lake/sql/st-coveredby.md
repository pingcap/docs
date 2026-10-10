---
title: ST_COVEREDBY
summary: 最初の GEOMETRY オブジェクトのどの点も、2 番目の GEOMETRY オブジェクトの外側に存在しない場合に TRUE を返します。
---

# ST_COVEREDBY

最初の GEOMETRY オブジェクトのどの点も、2 番目の GEOMETRY オブジェクトの外側に存在しない場合に TRUE を返します。

関連項目: [ST_COVERS](/tidb-cloud-lake/sql/st-covers.md)

## 構文 {#syntax}

```sql
ST_COVEREDBY(<geometry1>, <geometry2>)
```

## 引数 {#arguments}

| 引数          | 説明                                                 |
|---------------|------------------------------------------------------|
| `<geometry1>` | GEOMETRY 式（判定対象のオブジェクト）。              |
| `<geometry2>` | GEOMETRY 式（包含する側のオブジェクト）。            |

## 戻り値の型 {#return-type}

Boolean。

## 例 {#examples}

```sql
SELECT ST_COVEREDBY(
  TO_GEOMETRY('POINT(1 1)'),
  TO_GEOMETRY('POLYGON((0 0, 3 0, 3 3, 0 3, 0 0))')
);

┌────────┐
│ result │
├────────┤
│ true   │
└────────┘

SELECT ST_COVEREDBY(
  TO_GEOMETRY('POLYGON((1 1, 2 1, 2 2, 1 2, 1 1))'),
  TO_GEOMETRY('POLYGON((0 0, 3 0, 3 3, 0 3, 0 0))')
);

┌────────┐
│ result │
├────────┤
│ true   │
└────────┘

SELECT ST_COVEREDBY(
  TO_GEOMETRY('POINT(5 5)'),
  TO_GEOMETRY('POLYGON((0 0, 3 0, 3 3, 0 3, 0 0))')
);

┌────────┐
│ result │
├────────┤
│ false  │
└────────┘
```