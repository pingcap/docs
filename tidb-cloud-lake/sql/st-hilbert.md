---
title: ST_HILBERT
summary: GEOMETRY または GEOGRAPHY オブジェクトを Hilbert 曲線インデックスにエンコードします。
---

# ST_HILBERT

GEOMETRY または GEOGRAPHY オブジェクトを Hilbert 曲線インデックスにエンコードします。この関数は、エンコードする点としてジオメトリのバウンディングボックスの中心を使用します。bounds が指定されている場合、エンコード前にその点は指定されたバウンディングボックス内に正規化されます。

## 構文 {#syntax}

```sql
ST_HILBERT(<geometry_or_geography>)
ST_HILBERT(<geometry_or_geography>, <bounds>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|-------------|
| `<geometry_or_geography>` | 引数は GEOMETRY または GEOGRAPHY 型の式である必要があります。 |
| `<bounds>` | オプション。エンコード前に点を正規化するために使用する配列 `[xmin, ymin, xmax, ymax]` です。 |

> **Note:**
>
> - Geometry: バウンディングボックスが指定されていない場合、GEOMETRY 座標は特定のバウンディングボックスに正規化されません。代わりに、中心点の値が `float32` の全ドメインにマッピングされ、その後 Hilbert インデックスにエンコードされます。
> - Geography: バウンディングボックスが指定されていない場合、デフォルトの bounds は `[-180, -90, 180, 90]` です。

## 戻り値の型 {#return-type}

UInt64。

## 例 {#examples}

### GEOMETRY の例 {#geometry-examples}

```sql
SELECT ST_HILBERT(TO_GEOMETRY('POINT(1 2)')) AS hilbert1, ST_HILBERT(TO_GEOMETRY('POINT(5 5)')) AS hilbert2;

╭───────────────────────────╮
│   hilbert1  │   hilbert2  │
├─────────────┼─────────────┤
│  3355443200 │  2155872256 │
╰───────────────────────────╯

SELECT ST_HILBERT(TO_GEOMETRY('POINT(1 2)'), [0, 0, 1, 1]) AS hilbert1, ST_HILBERT(TO_GEOMETRY('POINT(5 5)'), [0, 0, 5, 5]) AS hilbert2;

╭───────────────────────────╮
│   hilbert1  │   hilbert2  │
├─────────────┼─────────────┤
│  2863311530 │  2863311530 │
╰───────────────────────────╯
```

### GEOGRAPHY の例 {#geography-examples}

```sql
SELECT ST_HILBERT(TO_GEOGRAPHY('POINT(113.15 23.06)')) AS hilbert1, ST_HILBERT(TO_GEOGRAPHY('POINT(116.25 39.54)')) AS hilbert2;

╭───────────────────────────╮
│   hilbert1  │   hilbert2  │
├─────────────┼─────────────┤
│  3070259060 │  3033451300 │
╰───────────────────────────╯

SELECT ST_HILBERT(TO_GEOGRAPHY('POINT(113.15 23.06)'), [73, 4, 135, 53]) AS hilbert1, ST_HILBERT(TO_GEOGRAPHY('POINT(116.25 39.54)'), [73, 4, 135, 53]) AS hilbert2;

╭───────────────────────────╮
│   hilbert1  │   hilbert2  │
├─────────────┼─────────────┤
│  3533607194 │  2330429279 │
╰───────────────────────────╯
```