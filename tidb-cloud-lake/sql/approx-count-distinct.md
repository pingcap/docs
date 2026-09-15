---
title: APPROX_COUNT_DISTINCT
summary: 使用 HyperLogLog 算法估算数据集中不同值的数量。
---

# APPROX_COUNT_DISTINCT

使用 [HyperLogLog](https://en.wikipedia.org/wiki/HyperLogLog) 算法估算数据集中不同值的数量。

HyperLogLog 算法能够以较少的内存和时间近似计算唯一元素的数量。在处理大型数据集且可以接受估算结果时，建议使用此函数。它以牺牲一定准确性为代价，提供了一种快速且高效的返回去重计数的方法。

如需获得准确结果，请使用 [COUNT_DISTINCT](/tidb-cloud-lake/sql/count-distinct.md)。更多说明请参见[示例](#example)。

## 语法 {#syntax}

```sql
APPROX_COUNT_DISTINCT(<expr>)
```

## 返回类型 {#return-type}

整数型。

## 示例 {#example}

**创建表并插入示例数据**

```sql
CREATE TABLE user_events (
  id INT,
  user_id INT,
  event_name VARCHAR
);

INSERT INTO user_events (id, user_id, event_name)
VALUES (1, 1, 'Login'),
       (2, 2, 'Login'),
       (3, 3, 'Login'),
       (4, 1, 'Logout'),
       (5, 2, 'Logout'),
       (6, 4, 'Login'),
       (7, 1, 'Login');
```

**查询演示：估算不同用户 ID 的数量**

```sql
SELECT APPROX_COUNT_DISTINCT(user_id) AS approx_distinct_user_count
FROM user_events;
```

**结果**

```sql
| approx_distinct_user_count |
|----------------------------|
|             4              |
```