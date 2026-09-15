---
title: AVG
summary: 聚合函数。
---

# AVG

聚合函数。

`AVG()` 函数返回一个表达式的平均值。

**注意：** 不会统计 `NULL` 值。

## 语法 {#syntax}

```sql
AVG(<expr>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|--------------------------|
| `<expr>`  | 任何数值表达式 |

## 返回类型 {#return-type}

double

## 示例 {#examples}

**创建表并插入示例数据**

让我们创建一个名为 "sales" 的表，并插入一些示例数据：

```sql
CREATE TABLE sales (
  id INTEGER,
  product VARCHAR(50),
  price FLOAT
);

INSERT INTO sales (id, product, price)
VALUES (1, 'Product A', 10.5),
       (2, 'Product B', 20.75),
       (3, 'Product C', 30.0),
       (4, 'Product D', 15.25),
       (5, 'Product E', 25.5);
```

**查询：使用 AVG() 函数**

现在，让我们使用 `AVG()` 函数来查找 "sales" 表中所有产品的平均价格：

```sql
SELECT AVG(price) AS avg_price
FROM sales;
```

结果应如下所示：

```sql
| avg_price |
| --------- |
| 20.4      |
```