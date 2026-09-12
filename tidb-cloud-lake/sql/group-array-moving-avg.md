---
title: GROUP_ARRAY_MOVING_AVG
summary: GROUP_ARRAY_MOVING_AVG 函数用于计算输入值的移动平均值。该函数可以将窗口大小作为参数传入。如果未指定，则函数将窗口大小设为输入值的数量。
---

# GROUP_ARRAY_MOVING_AVG

GROUP_ARRAY_MOVING_AVG 函数用于计算输入值的移动平均值。该函数可以将窗口大小作为参数传入。如果未指定，则函数将窗口大小设为输入值的数量。

## 语法 {#syntax}

```sql
GROUP_ARRAY_MOVING_AVG(<expr>)

GROUP_ARRAY_MOVING_AVG(<window_size>)(<expr>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|------------------| ------------------------ |
| `<window_size>`  | 任意数值表达式 |
| `<expr>`         | 任意数值表达式 |

## 返回类型 {#return-type}

返回一个 [数组](/tidb-cloud-lake/sql/array.md)，其元素类型根据源数据类型为 double 或 decimal。

## 示例 {#examples}

```sql
-- Create a table and insert sample data
CREATE TABLE hits (
  user_id INT,
  request_num INT
);

INSERT INTO hits (user_id, request_num)
VALUES (1, 10),
       (2, 15),
       (3, 20),
       (1, 13),
       (2, 21),
       (3, 25),
       (1, 30),
       (2, 41),
       (3, 45);

SELECT user_id, GROUP_ARRAY_MOVING_AVG(2)(request_num) AS avg_request_num
FROM hits
GROUP BY user_id;

| user_id | avg_request_num  |
|---------|------------------|
|       1 | [5.0,11.5,21.5]  |
|       3 | [10.0,22.5,35.0] |
|       2 | [7.5,18.0,31.0]  |
```