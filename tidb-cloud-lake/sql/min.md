---
title: MIN
summary: 聚合函数。
---

# MIN

聚合函数。

`MIN()` 函数返回一组值中的最小值。

## 语法 {#syntax}

```
MIN(<expr>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|----------------|
| `<expr>`  | 任意表达式 |

## 返回类型 {#return-type}

最小值，类型与该值的类型相同。

## 示例 {#example}

**创建表并插入示例数据**

```sql
CREATE TABLE gas_prices (
  id INT,
  station_id INT,
  price FLOAT
);

INSERT INTO gas_prices (id, station_id, price)
VALUES (1, 1, 3.50),
       (2, 1, 3.45),
       (3, 1, 3.55),
       (4, 2, 3.40),
       (5, 2, 3.35);
```

**查询示例：查找站点 1 的最低油价**

```sql
SELECT station_id, MIN(price) AS min_price
FROM gas_prices
WHERE station_id = 1
GROUP BY station_id;
```

**结果**

```sql
| station_id | min_price |
|------------|-----------|
|     1      |   3.45    |
```