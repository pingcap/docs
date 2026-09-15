---
title: CREATE SPATIAL INDEX
summary: "在 {{{ .lake }}} 中创建一个新的空间索引。"
---

# CREATE SPATIAL INDEX

在 {{{ .lake }}} 中创建一个新的空间索引。

## 语法 {#syntax}

```sql
CREATE [ OR REPLACE ] SPATIAL INDEX [IF NOT EXISTS] <index>
    ON [<database>.]<table>( <geometry_column>[, <geometry_column> ...] )
```

| 参数 | 描述 |
|-----------|-------------|
| `[ OR REPLACE ]` | 如果索引已存在，则替换现有索引。 |
| `[ IF NOT EXISTS ]` | 仅当不存在同名索引时才创建该索引。 |
| `<index>` | 空间索引的名称。 |
| `[<database>.]<table>` | 拥有被索引列的表。 |
| `<geometry_column>` | 索引中包含的 `GEOMETRY` 列。语句中列出的每一列都必须唯一。 |

## 使用说明 {#usage-notes}

- 仅 Fuse 表支持空间索引。
- 空间索引仅支持 `GEOMETRY` 列，不支持 `GEOGRAPHY` 列。
- 单个空间索引定义中可以为多列创建索引，但这些列都必须是 `GEOMETRY` 列。
- 为了获得更好的裁剪效果，建议使用 `CLUSTER BY` 和 `ST_HILBERT` 对地理空间数据进行物理聚簇，这样相邻对象更有可能被写入同一个数据块。

## 示例 {#examples}

创建一个包含空间列的表：

```sql
CREATE TABLE stores (
    store_id INT,
    store_name STRING,
    location GEOMETRY
) CLUSTER BY (
    ST_HILBERT(location, [-180, -90, 180, 90])
);
```

在 `location` 列上创建空间索引：

```sql
CREATE SPATIAL INDEX stores_location_idx ON stores(location);
```

查看表定义：

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

加载一个稍丰富一些的数据集以进行空间过滤，并运行 RECLUSTER 命令：

```sql
INSERT INTO stores VALUES
  (1, 'Starbucks', TO_GEOMETRY('POINT(10 10)')),
  (2, 'Costa', TO_GEOMETRY('POINT(11 11)')),
  (3, 'Gong Cha', TO_GEOMETRY('POINT(20 20)')),
  (4, 'Dunkin', TO_GEOMETRY('POINT(-10 -10)'));

ALTER TABLE stores RECLUSTER FINAL;
```

### 使用 `ST_WITHIN`、`ST_INTERSECTS` 和 `ST_CONTAINS` 进行过滤 {#filter-with-st-within-st-intersects-and-st-contains}

这些谓词是常见的地理围栏式过滤条件，可以从空间索引中受益。

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

### 使用 `ST_DWITHIN` 进行过滤 {#filter-with-st-dwithin}

使用 `ST_DWITHIN` 执行半径式查找。这对于“查找附近位置”类查询非常有用。

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

### 使用空间连接进行过滤 {#filter-with-spatial-joins}

当连接条件是受支持的空间谓词时，空间索引在连接查询中同样很有用。

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