---
title: KURTOSIS
summary: 聚合函数。
---

# KURTOSIS

聚合函数。

`KURTOSIS()` 函数返回所有输入值的超额峰度。

## 语法 {#syntax}

```sql
KURTOSIS(<expr>)
```

## 参数 {#arguments}

| 参数 | 描述                     |
|-----------| -----------                     |
| `<expr>`  | 任意数值表达式        |

## 返回类型 {#return-type}

可为空的 Float64。

## 示例 {#example}

**创建表并插入示例数据**

```sql
CREATE TABLE stock_prices (
  id INT,
  stock_symbol VARCHAR,
  price FLOAT
);

INSERT INTO stock_prices (id, stock_symbol, price)
VALUES (1, 'AAPL', 150),
       (2, 'AAPL', 152),
       (3, 'AAPL', 148),
       (4, 'AAPL', 160),
       (5, 'AAPL', 155);
```

**查询演示：计算 Apple 股票价格的超额峰度**

```sql
SELECT KURTOSIS(price) AS excess_kurtosis
FROM stock_prices
WHERE stock_symbol = 'AAPL';
```

**结果**

```sql
|     excess_kurtosis     |
|-------------------------|
| 0.06818181325581445     |
```