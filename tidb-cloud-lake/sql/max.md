---
title: MAX
summary: 聚合函数。
---

# MAX

聚合函数。

MAX() 函数返回一组值中的最大值。

## 语法 {#syntax}

```
MAX(<expr>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------| ----------- |
| `<expr>`  | 任意表达式 |

## 返回类型 {#return-type}

最大值，类型与该值的类型相同。

## 示例 {#example}

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

**结果**

```sql
|    city    | max_temperature |
|------------|-----------------|
| New York   |       32        |
```