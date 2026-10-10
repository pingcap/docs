---
title: MIN
summary: 集約関数。
---

# MIN

集約関数。

`MIN()` 関数は、値の集合の中から最小値を返します。

## 構文 {#syntax}

```
MIN(<expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|----------------|
| `<expr>`  | 任意の式 |

## 戻り値の型 {#return-type}

値の型における最小値です。

## 例 {#example}

**Create a Table and Insert Sample Data**

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

**Query Demo: Find Minimum Gas Price for Station 1**

```sql
SELECT station_id, MIN(price) AS min_price
FROM gas_prices
WHERE station_id = 1
GROUP BY station_id;
```

**結果**

```sql
| station_id | min_price |
|------------|-----------|
|     1      |   3.45    |
```