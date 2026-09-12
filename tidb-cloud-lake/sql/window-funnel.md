---
title: WINDOW_FUNNEL
summary: 漏斗分析。
---

# WINDOW_FUNNEL

`WINDOW_FUNNEL` 函数与 ClickHouse 中的 `windowFunnel` 类似（它们由同一位作者创建），用于在滑动时间窗口中搜索事件链，并计算该链中事件的最大数量。

该函数按照以下算法工作：

- 函数会搜索触发链中第一个条件的数据，并将事件计数器设为 1。此时滑动窗口开始。

- 如果链中的事件在窗口内按顺序依次发生，则计数器递增。如果事件顺序被打断，则计数器不会递增。

- 如果数据中存在多个事件链，且完成程度不同，则函数只会输出最长链的大小。

```sql
WINDOW_FUNNEL( <window> )( <timestamp>, <cond1>, <cond2>, ..., <condN> )
```

**参数**

- `<timestamp>` — 包含时间戳的列名。支持的数据类型：整数类型和 datetime 类型。
- `<cond>` — 描述事件链的条件或数据。必须为 `Boolean` 数据类型。

**Parameters**

- `<window>` — 滑动窗口的长度，即第一个条件与最后一个条件之间的时间间隔。`window` 的单位取决于 `timestamp` 本身，因此可能不同。通过表达式 `timestamp of cond1 <= timestamp of cond2 <= ... <= timestamp of condN <= timestamp of cond1 + window` 来确定。

**返回值**

滑动时间窗口内，事件链中连续触发条件的最大数量。会分析所选数据中的所有链。

类型：`UInt8`。

**示例**

判断在给定时间段内，用户是否有足够时间在网店中选择一部手机并完成两次购买。

设置如下事件链：

1. 用户登录其商店账户（`event_name = 'login'`）。
2. 用户访问页面（`event_name = 'visit'`）。
3. 用户将商品加入购物车（`event_name = 'cart'`）。
4. 用户完成购买（`event_name = 'purchase'`）。

```sql
CREATE TABLE events(user_id BIGINT, event_name VARCHAR, event_timestamp TIMESTAMP);

INSERT INTO events VALUES(100123, 'login', '2022-05-14 10:01:00');
INSERT INTO events VALUES(100123, 'visit', '2022-05-14 10:02:00');
INSERT INTO events VALUES(100123, 'cart', '2022-05-14 10:04:00');
INSERT INTO events VALUES(100123, 'purchase', '2022-05-14 10:10:00');

INSERT INTO events VALUES(100125, 'login', '2022-05-15 11:00:00');
INSERT INTO events VALUES(100125, 'visit', '2022-05-15 11:01:00');
INSERT INTO events VALUES(100125, 'cart', '2022-05-15 11:02:00');

INSERT INTO events VALUES(100126, 'login', '2022-05-15 12:00:00');
INSERT INTO events VALUES(100126, 'visit', '2022-05-15 12:01:00');
```

输入表：

```sql
+---------+------------+----------------------------+
| user_id | event_name | event_timestamp            |
+---------+------------+----------------------------+
|  100123 | login      | 2022-05-14 10:01:00.000000 |
|  100123 | visit      | 2022-05-14 10:02:00.000000 |
|  100123 | cart       | 2022-05-14 10:04:00.000000 |
|  100123 | purchase   | 2022-05-14 10:10:00.000000 |
|  100125 | login      | 2022-05-15 11:00:00.000000 |
|  100125 | visit      | 2022-05-15 11:01:00.000000 |
|  100125 | cart       | 2022-05-15 11:02:00.000000 |
|  100126 | login      | 2022-05-15 12:00:00.000000 |
|  100126 | visit      | 2022-05-15 12:01:00.000000 |
+---------+------------+----------------------------+
```

找出用户 `user_id` 在按小时滑动的窗口中，最多能完成事件链的哪一步。

查询：

```sql
SELECT
    level,
    count() AS count
FROM
(
    SELECT
        user_id,
        window_funnel(3600000000)(event_timestamp, event_name = 'login', event_name = 'visit', event_name = 'cart', event_name = 'purchase') AS level
    FROM events
    GROUP BY user_id
)
GROUP BY level ORDER BY level ASC;
```

> **Tip:**
>
> `event_timestamp` 的类型是 timestamp，`3600000000` 表示 1 小时的时间窗口。

结果：

```sql
+-------+-------+
| level | count |
+-------+-------+
|     2 |     1 |
|     3 |     1 |
|     4 |     1 |
+-------+-------+
```

- 用户 `100126` 的 level 为 2（`login -> visit`）。
- 用户 `100125` 的 level 为 3（`login -> visit -> cart`）。
- 用户 `100123` 的 level 为 4（`login -> visit -> cart -> purchase`）。