---
title: CREATE SPATIAL INDEX
summary: "{{{ .lake }}} に新しい空間インデックスを作成します。"
---

# CREATE SPATIAL INDEX

{{{ .lake }}} に新しい空間インデックスを作成します。

## 構文 {#syntax}

```sql
CREATE [ OR REPLACE ] SPATIAL INDEX [IF NOT EXISTS] <index>
    ON [<database>.]<table>( <geometry_column>[, <geometry_column> ...] )
```

| パラメーター | 説明 |
|-----------|-------------|
| `[ OR REPLACE ]` | 既存のインデックスがすでに存在する場合は、それを置き換えます。 |
| `[ IF NOT EXISTS ]` | 同じ名前のインデックスがまだ存在しない場合にのみ、インデックスを作成します。 |
| `<index>` | 空間インデックスの名前です。 |
| `[<database>.]<table>` | インデックス対象のカラムを持つテーブルです。 |
| `<geometry_column>` | インデックスに含まれる `GEOMETRY` カラムです。指定する各カラムは、この文の中で一意である必要があります。 |

## 使用上の注意 {#usage-notes}

- 空間インデックスは Fuse テーブルでのみサポートされます。
- 空間インデックスは `GEOMETRY` カラムのみをサポートします。`GEOGRAPHY` カラムはサポートされません。
- 単一の空間インデックス定義で複数のカラムをインデックス化できますが、すべて `GEOMETRY` カラムである必要があります。
- より効果的にプルーニングするために、`CLUSTER BY` と `ST_HILBERT` を使用して地理空間データを物理的にクラスター化することを推奨します。これにより、近接するオブジェクトが同じブロックに書き込まれやすくなります。

## 例 {#examples}

空間カラムを持つテーブルを作成します。

```sql
CREATE TABLE stores (
    store_id INT,
    store_name STRING,
    location GEOMETRY
) CLUSTER BY (
    ST_HILBERT(location, [-180, -90, 180, 90])
);
```

`location` カラムに空間インデックスを作成します。

```sql
CREATE SPATIAL INDEX stores_location_idx ON stores(location);
```

テーブル定義を確認します。

```sql
SHOW CREATE TABLE stores;

┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│ Table  │ Create Table                                                                      │
├──────────────────────────────────────────────────────────────────────────────────────────────┤
│ stores │ CREATE TABLE stores (                                                             │
│        │   store_id INT NULL,                                                              │
│        │   store_name VARCHAR NULL,                                                        │
│        │   location GEOMETRY NULL,                                                         │
│        │   SYNC SPATIAL INDEX stores_location_idx (location)                               │
│        │ ) ENGINE=FUSE CLUSTER BY linear(st_hilbert(location, [-180, -90, 180, 90]))       │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
```

空間フィルタリング用に少し充実したデータセットをロード (load) し、RECLUSTER コマンドを実行します。

```sql
INSERT INTO stores VALUES
  (1, 'Starbucks', TO_GEOMETRY('POINT(10 10)')),
  (2, 'Costa', TO_GEOMETRY('POINT(11 11)')),
  (3, 'Gong Cha', TO_GEOMETRY('POINT(20 20)')),
  (4, 'Dunkin', TO_GEOMETRY('POINT(-10 -10)'));

ALTER TABLE stores RECLUSTER FINAL;
```

### `ST_WITHIN`、`ST_INTERSECTS`、`ST_CONTAINS` によるフィルタリング {#filter-with-st-within-st-intersects-and-st-contains}

これらの述語は、ジオフェンス形式のフィルタとして一般的であり、空間インデックスの恩恵を受けられます。

```sql
-- Rows whose locations are within a polygon
SELECT store_id, store_name
FROM stores
WHERE ST_WITHIN(
    location,
    TO_GEOMETRY('POLYGON((9 9, 9 12, 12 12, 12 9, 9 9))')
)
ORDER BY store_id;
```

```sql
-- Rows whose locations intersect a polygon
SELECT store_id, store_name
FROM stores
WHERE ST_INTERSECTS(
    location,
    TO_GEOMETRY('POLYGON((9 9, 9 12, 12 12, 12 9, 9 9))')
)
ORDER BY store_id;
```

```sql
-- Polygons that contain a point
SELECT store_id, store_name
FROM stores
WHERE ST_CONTAINS(
    TO_GEOMETRY('POLYGON((9 9, 9 12, 12 12, 12 9, 9 9))'),
    location
)
ORDER BY store_id;
```

### `ST_DWITHIN` によるフィルタリング {#filter-with-st-dwithin}

半径ベースの検索には `ST_DWITHIN` を使用します。これは「近くの場所を探す」クエリに便利です。

```sql
SELECT store_id, store_name
FROM stores
WHERE ST_DWITHIN(
    location,
    TO_GEOMETRY('POINT(10 10)'),
    1.5
)
ORDER BY store_id;
```

### 空間テーブル結合によるフィルタリング {#filter-with-spatial-joins}

空間インデックスは、結合条件がサポートされている空間述語であるテーブル結合でも有用です。

```sql
CREATE TABLE districts (
    district_id INT,
    district_name STRING,
    geom GEOMETRY
) CLUSTER BY (
    ST_HILBERT(geom, [-180, -90, 180, 90])
);

INSERT INTO districts VALUES
  (1, 'Central', TO_GEOMETRY('POLYGON((8 8, 8 13, 13 13, 13 8, 8 8))')),
  (2, 'West', TO_GEOMETRY('POLYGON((-2 -2, -2 2, 2 2, 2 -2, -2 -2))'));
```

```sql
SELECT d.district_name, s.store_name
FROM districts AS d
JOIN stores AS s
  ON ST_WITHIN(s.location, d.geom)
ORDER BY d.district_name, s.store_name;
```