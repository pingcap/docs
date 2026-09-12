---
title: ST_COVEREDBY
summary: 如果第一个 GEOMETRY 对象中没有任何点位于第二个 GEOMETRY 对象之外，则返回 TRUE。
---

# ST_COVEREDBY

如果第一个 GEOMETRY 对象中没有任何点位于第二个 GEOMETRY 对象之外，则返回 TRUE。

另请参阅：[ST_COVERS](/tidb-cloud-lake/sql/st-covers.md)

## 语法 {#syntax}

```sql
ST_COVEREDBY(<geometry1>, <geometry2>)
```

## 参数 {#arguments}

| 参数          | 描述                                 |
|---------------|--------------------------------------|
| `<geometry1>` | 一个 GEOMETRY 表达式（被测试的对象）。 |
| `<geometry2>` | 一个 GEOMETRY 表达式（覆盖对象）。     |

## 返回类型 {#return-type}

布尔型。

## 示例 {#examples}

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