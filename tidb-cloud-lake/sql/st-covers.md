---
title: ST_COVERS
summary: 如果第二个 GEOMETRY 对象中没有任何点位于第一个 GEOMETRY 对象之外，则返回 TRUE。
---

# ST_COVERS

如果第二个 GEOMETRY 对象中没有任何点位于第一个 GEOMETRY 对象之外，则返回 TRUE。

另请参阅：[ST_COVEREDBY](/tidb-cloud-lake/sql/st-coveredby.md)

## 语法 {#syntax}

```sql
ST_COVERS(<geometry1>, <geometry2>)
```

## 参数 {#arguments}

| 参数          | 描述                                         |
|---------------|----------------------------------------------|
| `<geometry1>` | 一个 GEOMETRY 表达式（覆盖对象）。           |
| `<geometry2>` | 一个 GEOMETRY 表达式（被测试的对象）。       |

## 返回类型 {#return-type}

布尔型。

## 示例 {#examples}

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