---
title: RETENTION
summary: 聚合函数。
---

# RETENTION

聚合函数

`RETENTION()` 函数接受一组条件作为参数，参数个数可以是 1 到 32 个，类型为 UInt8，用于指示某个事件是否满足特定条件。

任意条件都可以作为参数指定（与 `WHERE` 中类似）。

除第一个条件外，其余条件按配对方式生效：如果第一个和第二个条件都为 true，则第二个结果为 true；如果第一个和第三个条件都为 true，则第三个结果为 true；以此类推。

## 语法 {#syntax}

```sql
RETENTION( <cond1> , <cond2> , ..., <cond32> );
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|---------------------------------------------|
| `<cond>`  | 返回布尔结果的表达式 |

## 返回类型 {#return-type}

返回由 1 或 0 组成的数组。

## 示例 {#example}

**创建表并插入示例数据**

```sql
CREATE TABLE user_events (
  id INT,
  user_id INT,
  event_date DATE,
  event_type VARCHAR
);

INSERT INTO user_events (id, user_id, event_date, event_type)
VALUES (1, 1, '2022-01-01', 'signup'),
       (2, 1, '2022-01-02', 'login'),
       (3, 2, '2022-01-01', 'signup'),
       (4, 2, '2022-01-03', 'purchase'),
       (5, 3, '2022-01-01', 'signup'),
       (6, 3, '2022-01-02', 'login');
```

**查询示例：基于 signup、login 和 purchase 事件计算用户留存**

```sql
SELECT
  user_id,
  RETENTION(event_type = 'signup', event_type = 'login', event_type = 'purchase') AS retention
FROM user_events
GROUP BY user_id;
```

**结果**

```sql
| user_id | retention |
|---------|-----------|
|   1     | [1, 1, 0] |
|   2     | [1, 0, 1] |
|   3     | [1, 1, 0] |
```