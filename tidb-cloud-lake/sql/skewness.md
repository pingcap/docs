---
title: SKEWNESS
summary: 聚合函数。
---

# SKEWNESS

聚合函数。

`SKEWNESS()` 函数返回所有输入值的偏度。

## 语法 {#syntax}

```sql
SKEWNESS(<expr>)
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
CREATE TABLE temperature_data (
                                  id INT,
                                  city_id INT,
                                  temperature FLOAT
);

INSERT INTO temperature_data (id, city_id, temperature)
VALUES (1, 1, 60),
       (2, 1, 65),
       (3, 1, 62),
       (4, 2, 70),
       (5, 2, 75);
```

**查询演示：计算温度数据的偏度**

```sql
SELECT SKEWNESS(temperature) AS temperature_skewness
FROM temperature_data;
```

**结果**

```sql
| temperature_skewness |
|----------------------|
|      0.68            |
```