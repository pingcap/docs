---
title: MAX
summary: 集約関数。
---

# MAX

集約関数。

MAX() 関数は、値の集合の中から最大値を返します。

## 構文 {#syntax}

```
MAX(<expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------| ----------- |
| `<expr>`  | 任意の式 |

## 戻り値の型 {#return-type}

値の型における最大値を返します。

## 例 {#example}

**Create a Table and Insert Sample Data**

```sql
CREATE TABLE temperatures (
  id INT,
  city VARCHAR,
  temperature FLOAT
);

INSERT INTO temperatures (id, city, temperature)
VALUES (1, 'New York', 30),
       (2, 'New York', 28),
       (3, 'New York', 32),
       (4, 'Los Angeles', 25),
       (5, 'Los Angeles', 27);
```

**Query Demo: Find Maximum Temperature for New York City**

```sql
SELECT city, MAX(temperature) AS max_temperature
FROM temperatures
WHERE city = 'New York'
GROUP BY city;
```

**結果**

```sql
|    city    | max_temperature |
|------------|-----------------|
| New York   |       32        |
```