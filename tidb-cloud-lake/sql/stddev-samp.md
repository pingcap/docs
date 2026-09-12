---
title: STDDEV_SAMP
summary: 返回表达式的样本标准差（VAR_SAMP() 的平方根）。
---

# STDDEV_SAMP

返回表达式的样本标准差（VAR_SAMP() 的平方根）。

- 会忽略 `NULL` 值。
- 当只有一条输入记录时，STDDEV_SAMP() 返回 `NULL` 而不是 `0`。

## 语法 {#syntax}

```sql
STDDEV_SAMP(<expr>)
```

## 参数 {#arguments}

| 参数 | 描述 |
| --------- | ------------------------ |
| `<expr>`  | 任意数值表达式 |

## 返回类型 {#return-type}

Double。

## 示例 {#example}

**创建表并插入示例数据**

```sql
CREATE TABLE height_data (
  id INT,
  person_id INT,
  height FLOAT
);

INSERT INTO height_data (id, person_id, height)
VALUES (1, 1, 5.8),
       (2, 2, 6.1),
       (3, 3, 5.9),
       (4, 4, 5.7),
       (5, 5, 6.3);
```

**查询示例：计算身高的样本标准差**

```sql
SELECT STDDEV_SAMP(height) AS height_stddev_samp
FROM height_data;
```

**结果**

```sql
| height_stddev_samp |
|--------------------|
|      0.240         |
```