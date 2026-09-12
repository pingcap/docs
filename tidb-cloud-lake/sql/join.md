---
title: JOIN
summary: 连接将两个或多个表中的列组合成一个结果集。{{{ .lake }}} 同时实现了 ANSI SQL 连接和 Lake 特有扩展，使你能够使用相同的语法处理维度数据、缓慢变化的事实数据以及时间序列流。
---

# JOIN

## 概述 {#overview}

连接将两个或多个表中的列组合成一个结果集。{{{ .lake }}} 同时实现了 ANSI SQL 连接和 Lake 特有扩展，使你能够使用相同的语法处理维度数据、缓慢变化的事实数据以及时间序列流。

## 支持的连接类型 {#supported-join-types}

* [Inner Join](#inner-join)
* [自然连接](#natural-join)
* [交叉连接](#cross-join)
* [左连接](#left-join)
* [右连接](#right-join)
* [全外连接](#full-outer-join)
* [左 / 右半连接](#left--right-semi-join)
* [左 / 右反连接](#left--right-anti-join)
* [Asof Join](#asof-join)

## 示例数据 {#sample-data}

### 准备表 {#prepare-the-tables}

运行以下 SQL 一次，以创建并填充本页中会反复使用的表：

```sql
-- VIP profile tables
CREATE OR REPLACE TABLE vip_info (client_id INT, region VARCHAR);
INSERT INTO vip_info VALUES
    (101, 'Toronto'),
    (102, 'Quebec'),
    (103, 'Vancouver');

CREATE OR REPLACE TABLE purchase_records (client_id INT, item VARCHAR, qty INT);
INSERT INTO purchase_records VALUES
    (100, 'Croissant', 2000),
    (102, 'Donut',     3000),
    (103, 'Coffee',    6000),
    (106, 'Soda',      4000);

CREATE OR REPLACE TABLE gift (gift VARCHAR);
INSERT INTO gift VALUES
    ('Croissant'), ('Donut'), ('Coffee'), ('Soda');

-- IoT-style readings for ASOF examples
CREATE OR REPLACE TABLE sensor_readings (
    room VARCHAR,
    reading_time TIMESTAMP,
    temperature DOUBLE
);
INSERT INTO sensor_readings VALUES
    ('LivingRoom', '2024-01-01 09:55:00', 22.8),
    ('LivingRoom', '2024-01-01 10:00:00', 23.1),
    ('LivingRoom', '2024-01-01 10:05:00', 23.3),
    ('LivingRoom', '2024-01-01 10:10:00', 23.8),
    ('LivingRoom', '2024-01-01 10:15:00', 24.0);

CREATE OR REPLACE TABLE hvac_mode (
    room VARCHAR,
    mode_time TIMESTAMP,
    mode VARCHAR
);
INSERT INTO hvac_mode VALUES
    ('LivingRoom', '2024-01-01 09:58:00', 'Cooling'),
    ('LivingRoom', '2024-01-01 10:06:00', 'Fan'),
    ('LivingRoom', '2024-01-01 10:30:00', 'Heating');
```

### 预览数据 {#preview-the-data}

除非另有说明，下面的示例都会复用相同的表，以便你可以直接比较每种连接类型的效果。

```text
vip_info
+-----------+-----------+
| client_id | region    |
+-----------+-----------+
| 101       | Toronto   |
| 102       | Quebec    |
| 103       | Vancouver |
+-----------+-----------+

purchase_records
+-----------+-----------+------+
| client_id | item      | qty  |
+-----------+-----------+------+
| 100       | Croissant | 2000 |
| 102       | Donut     | 3000 |
| 103       | Coffee    | 6000 |
| 106       | Soda      | 4000 |
+-----------+-----------+------+

gift
+-----------+
| gift      |
+-----------+
| Croissant |
| Donut     |
| Coffee    |
| Soda      |
+-----------+
```

```text
sensor_readings
+-----------+---------------------+-------------+
| room      | reading_time        | temperature |
+-----------+---------------------+-------------+
| LivingRoom| 2024-01-01 09:55:00 | 22.8        |
| LivingRoom| 2024-01-01 10:00:00 | 23.1        |
| LivingRoom| 2024-01-01 10:05:00 | 23.3        |
| LivingRoom| 2024-01-01 10:10:00 | 23.8        |
| LivingRoom| 2024-01-01 10:15:00 | 24.0        |
+-----------+---------------------+-------------+

hvac_mode
+-----------+---------------------+----------+
| room      | mode_time           | mode     |
+-----------+---------------------+----------+
| LivingRoom| 2024-01-01 09:58:00 | Cooling  |
| LivingRoom| 2024-01-01 10:06:00 | Fan      |
| LivingRoom| 2024-01-01 10:30:00 | Heating  |
+-----------+---------------------+----------+
```

## Inner Join {#inner-join}

内连接返回满足所有连接谓词的行。

### 可视化 {#visual}

```text
┌──────────────────────────────┐
│ vip_info (left)              │
├──────────────────────────────┤
│ client_id | region           │
│ 101       | Toronto          │
│ 102       | Quebec           │
│ 103       | Vancouver        │
└──────────────────────────────┘
           │ client_id = client_id
           ▼
┌──────────────────────────────┐
│ purchase_records (right)     │
├──────────────────────────────┤
│ client_id | item     | qty   │
│ 100       | Croissant | 2000 │
│ 102       | Donut     | 3000 │
│ 103       | Coffee    | 6000 │
│ 106       | Soda      | 4000 │
└──────────────────────────────┘
           │ 仅保留匹配行
           ▼
┌──────────────────────────────┐
│ INNER JOIN RESULT            │
├──────────────────────────────┤
│ 102 | Donut  | 3000          │
│ 103 | Coffee | 6000          │
└──────────────────────────────┘
```

### 语法 {#syntax}

```sql
SELECT select_list
FROM table_a
     [INNER] JOIN table_b
              ON join_condition
```

> **Tip:**
>
> `INNER` 是可选的。当连接列具有相同名称时，可以使用 `USING(column_name)` 替代 `ON table_a.column = table_b.column`。

### 示例 {#example}

```sql
SELECT p.client_id, p.item, p.qty
FROM vip_info AS v
INNER JOIN purchase_records AS p
        ON v.client_id = p.client_id;
```

结果：

```text
+-----------+--------+------+
| client_id | item   | qty  |
+-----------+--------+------+
| 102       | Donut  | 3000 |
| 103       | Coffee | 6000 |
+-----------+--------+------+
```

## 自然连接 {#natural-join}

自然连接会自动匹配两个表中名称相同的列。结果中每个匹配列只会出现一份。

### 图示 {#visual}

```text
┌──────────────────────────────┐
│ vip_info                     │
├──────────────────────────────┤
│ client_id | region           │
│ 101       | Toronto          │
│ 102       | Quebec           │
│ 103       | Vancouver        │
└──────────────────────────────┘
           │ 自动匹配共享的列名
           ▼
┌──────────────────────────────┐
│ purchase_records             │
├──────────────────────────────┤
│ client_id | item     | qty   │
│ 100       | Croissant | 2000 │
│ 102       | Donut     | 3000 │
│ 103       | Coffee    | 6000 │
│ 106       | Soda      | 4000 │
└──────────────────────────────┘
           │ 共享列只输出一次
           ▼
┌──────────────────────────────┐
│ NATURAL JOIN RESULT          │
├──────────────────────────────┤
│ 102: Quebec + Donut + 3000   │
│ 103: Vanc. + Coffee + 6000   │
└──────────────────────────────┘
```

### 语法 {#syntax}

```sql
SELECT select_list
FROM table_a
NATURAL JOIN table_b;
```

### 示例 {#example}

```sql
SELECT client_id, item, qty
FROM vip_info
NATURAL JOIN purchase_records;
```

结果：

```text
+-----------+--------+------+
| client_id | item   | qty  |
+-----------+--------+------+
| 102       | Donut  | 3000 |
| 103       | Coffee | 6000 |
+-----------+--------+------+
```

## 交叉连接 {#cross-join}

交叉连接（笛卡尔积）会返回参与连接的表中所有行的每一种组合。

### 图示 {#visual}

```text
┌──────────────────────────────┐
│ vip_info (3 行)              │
├──────────────────────────────┤
│ 101 | Toronto                │
│ 102 | Quebec                 │
│ 103 | Vancouver              │
└──────────────────────────────┘
           │ 与每个 gift 配对
           ▼
┌──────────────────────────────┐
│ gift (4 行)                  │
├──────────────────────────────┤
│ Croissant                    │
│ Donut                        │
│ Coffee                       │
│ Soda                         │
└──────────────────────────────┘
           │ 3 × 4 种组合
           ▼
┌──────────────────────────────┐
│ CROSS JOIN RESULT (示例)     │
├──────────────────────────────┤
│ 101 | Toronto  | Croissant   │
│ 101 | Toronto  | Donut       │
│ 101 | Toronto  | Coffee      │
│ ... | ...      | ...         │
└──────────────────────────────┘
```

### 语法 {#syntax}

```sql
SELECT select_list
FROM table_a
CROSS JOIN table_b;
```

### 示例 {#example}

```sql
SELECT v.client_id, v.region, g.gift
FROM vip_info AS v
CROSS JOIN gift AS g;
```

结果（前几行）：

```text
+-----------+----------+-----------+
| client_id | region   | gift      |
+-----------+----------+-----------+
| 101       | Toronto  | Croissant |
| 101       | Toronto  | Donut     |
| 101       | Toronto  | Coffee    |
| 101       | Toronto  | Soda      |
| ...       | ...      | ...       |
+-----------+----------+-----------+
```

## 左连接 {#left-join}

左连接会返回左表中的每一行，以及右表中与之匹配的行。如果不存在匹配项，则右侧列为 `NULL`。

### 图示 {#visual}

```text
┌──────────────────────────────┐
│ vip_info (保留左表全部行)    │
├──────────────────────────────┤
│ 101 | Toronto                │
│ 102 | Quebec                 │
│ 103 | Vancouver              │
└──────────────────────────────┘
           │ 基于 client_id 连接
           ▼
┌──────────────────────────────┐
│ purchase_records             │
├──────────────────────────────┤
│ 100 | Croissant | 2000       │
│ 102 | Donut     | 3000       │
│ 103 | Coffee    | 6000       │
│ 106 | Soda      | 4000       │
└──────────────────────────────┘
           │ 右表中未匹配的列 -> NULL
           ▼
┌──────────────────────────────┐
│ LEFT JOIN RESULT             │
├──────────────────────────────┤
│ 101 | Toronto | NULL | NULL  │
│ 102 | Quebec  | Donut | 3000 │
│ 103 | Vanc.   | Coffee | 6000│
└──────────────────────────────┘
```

### 语法 {#syntax}

```sql
SELECT select_list
FROM table_a
LEFT [OUTER] JOIN table_b
             ON join_condition;
```

> **提示：**
>
> `OUTER` 是可选的。

### 示例 {#example}

```sql
SELECT v.client_id, p.item, p.qty
FROM vip_info AS v
LEFT JOIN purchase_records AS p
       ON v.client_id = p.client_id;
```

结果：

```text
+-----------+--------+------+
| client_id | item   | qty  |
+-----------+--------+------+
| 101       | NULL   | NULL |
| 102       | Donut  | 3000 |
| 103       | Coffee | 6000 |
+-----------+--------+------+
```

## 右连接 {#right-join}

右连接与左连接相对应：右表中的所有行都会出现，而左表中未匹配的行会产生 `NULL`。

### 图示 {#visual}

```text
┌──────────────────────────────┐
│ purchase_records (right)     │
├──────────────────────────────┤
│ 100 | Croissant | 2000       │
│ 102 | Donut     | 3000       │
│ 103 | Coffee    | 6000       │
│ 106 | Soda      | 4000       │
└──────────────────────────────┘
           ▲ 保留右表
           │ 按 client_id 连接
┌──────────────────────────────┐
│ vip_info                     │
├──────────────────────────────┤
│ 101 | Toronto                │
│ 102 | Quebec                 │
│ 103 | Vancouver              │
└──────────────────────────────┘
           ▼ 缺失的 VIP 数据用 NULL 填充
┌──────────────────────────────┐
│ RIGHT JOIN RESULT            │
├──────────────────────────────┤
│ 100 | Croissant | vip=NULL   │
│ 102 | Donut | region=Quebec  │
│ 103 | Coffee | region=Vanc.  │
│ 106 | Soda | vip=NULL        │
└──────────────────────────────┘
```

### 语法 {#syntax}

```sql
SELECT select_list
FROM table_a
RIGHT [OUTER] JOIN table_b
              ON join_condition;
```

### 示例 {#example}

```sql
SELECT v.client_id, v.region
FROM vip_info AS v
RIGHT JOIN purchase_records AS p
       ON v.client_id = p.client_id;
```

结果：

```text
+-----------+-----------+
| client_id | region    |
+-----------+-----------+
| NULL      | NULL      |
| 102       | Quebec    |
| 103       | Vancouver |
| NULL      | NULL      |
+-----------+-----------+
```

## 全外连接 {#full-outer-join}

全外连接返回左连接和右连接的联合体：两张表中的每一行都会返回，在没有匹配时用 `NULL` 填充。

### 图示 {#visual}

```text
┌──────────────────────────────┐
│ vip_info                     │
├──────────────────────────────┤
│ 101 | Toronto                │
│ 102 | Quebec                 │
│ 103 | Vancouver              │
└──────────────────────────────┘
┌──────────────────────────────┐
│ purchase_records             │
├──────────────────────────────┤
│ 100 | Croissant | 2000       │
│ 102 | Donut     | 3000       │
│ 103 | Coffee    | 6000       │
│ 106 | Soda      | 4000       │
└──────────────────────────────┘
           │ 合并匹配行 + 仅左侧行 + 仅右侧行
           ▼
┌──────────────────────────────┐
│ FULL OUTER JOIN RESULT       │
├──────────────────────────────┤
│ Toronto  | NULL              │
│ Quebec   | Donut             │
│ Vanc.    | Coffee            │
│ NULL     | Croissant         │
│ NULL     | Soda              │
└──────────────────────────────┘
```

### 语法 {#syntax}

```sql
SELECT select_list
FROM table_a
FULL [OUTER] JOIN table_b
             ON join_condition;
```

### 示例 {#example}

```sql
SELECT v.region, p.item
FROM vip_info AS v
FULL OUTER JOIN purchase_records AS p
            ON v.client_id = p.client_id;
```

结果：

```text
+-----------+-----------+
| region    | item      |
+-----------+-----------+
| Toronto   | NULL      |
| Quebec    | Donut     |
| Vancouver | Coffee    |
| NULL      | Croissant |
| NULL      | Soda      |
+-----------+-----------+
```

## 左 / 右半连接 {#left-right-semi-join}

半连接会将左表（或右表）过滤为在另一张表中至少有一条匹配记录的行。与内连接不同，半连接只返回被保留一侧的列。

### 图示 {#visual}

```text
LEFT SEMI JOIN
┌──────────────────────────────┐
│ vip_info                     │
├──────────────────────────────┤
│ 101 | Toronto                │
│ 102 | Quebec                 │
│ 103 | Vancouver              │
└──────────────────────────────┘
           │ 保留能找到匹配的行
           ▼
┌──────────────────────────────┐
│ purchase_records             │
├──────────────────────────────┤
│ 100 | Croissant | 2000       │
│ 102 | Donut     | 3000       │
│ 103 | Coffee    | 6000       │
│ 106 | Soda      | 4000       │
└──────────────────────────────┘
           ▼
┌──────────────────────────────┐
│ LEFT SEMI RESULT             │
├──────────────────────────────┤
│ 102 | Quebec                 │
│ 103 | Vanc.                  │
└──────────────────────────────┘

RIGHT SEMI JOIN
┌──────────────────────────────┐
│ purchase_records             │
├──────────────────────────────┤
│ 100 | Croissant | 2000       │
│ 102 | Donut     | 3000       │
│ 103 | Coffee    | 6000       │
│ 106 | Soda      | 4000       │
└──────────────────────────────┘
           │ 保留与 VIP 匹配的行
           ▼
┌──────────────────────────────┐
│ vip_info                     │
├──────────────────────────────┤
│ 101 | Toronto                │
│ 102 | Quebec                 │
│ 103 | Vancouver              │
└──────────────────────────────┘
           ▼
┌──────────────────────────────┐
│ RIGHT SEMI RESULT            │
├──────────────────────────────┤
│ 102 | Donut | 3000           │
│ 103 | Coffee | 6000          │
└──────────────────────────────┘
```

### 语法 {#syntax}

```sql
-- Left Semi Join
SELECT select_list
FROM table_a
LEFT SEMI JOIN table_b
           ON join_condition;

-- Right Semi Join
SELECT select_list
FROM table_a
RIGHT SEMI JOIN table_b
            ON join_condition;
```

### 示例 {#examples}

左半连接——返回有购买记录的 VIP 客户端：

```sql
SELECT *
FROM vip_info
LEFT SEMI JOIN purchase_records
           ON vip_info.client_id = purchase_records.client_id;
```

结果：

```text
+-----------+-----------+
| client_id | region    |
+-----------+-----------+
| 102       | Quebec    |
| 103       | Vancouver |
+-----------+-----------+
```

右半连接——返回属于 VIP 客户端的购买记录行：

```sql
SELECT *
FROM vip_info
RIGHT SEMI JOIN purchase_records
            ON vip_info.client_id = purchase_records.client_id;
```

结果：

```text
+-----------+--------+------+
| client_id | item   | qty  |
+-----------+--------+------+
| 102       | Donut  | 3000 |
| 103       | Coffee | 6000 |
+-----------+--------+------+
```

## Left / Right Anti Join {#left-right-anti-join}

反连接会返回在另一侧**没有**匹配行的记录，因此非常适合用于存在性检查。

### 图示 {#visual}

```text
LEFT ANTI JOIN
┌──────────────────────────────┐
│ vip_info                     │
├──────────────────────────────┤
│ 101 | Toronto                │
│ 102 | Quebec                 │
│ 103 | Vancouver              │
└──────────────────────────────┘
           │ remove rows with matches
           ▼
┌──────────────────────────────┐
│ purchase_records             │
├──────────────────────────────┤
│ 100 | Croissant | 2000       │
│ 102 | Donut     | 3000       │
│ 103 | Coffee    | 6000       │
│ 106 | Soda      | 4000       │
└──────────────────────────────┘
           ▼
┌──────────────────────────────┐
│ LEFT ANTI RESULT             │
├──────────────────────────────┤
│ 101 | Toronto                │
└──────────────────────────────┘

RIGHT ANTI JOIN
┌──────────────────────────────┐
│ purchase_records             │
├──────────────────────────────┤
│ 100 | Croissant | 2000       │
│ 102 | Donut     | 3000       │
│ 103 | Coffee    | 6000       │
│ 106 | Soda      | 4000       │
└──────────────────────────────┘
           │ remove rows with VIP matches
           ▼
┌──────────────────────────────┐
│ vip_info                     │
├──────────────────────────────┤
│ 101 | Toronto                │
│ 102 | Quebec                 │
│ 103 | Vancouver              │
└──────────────────────────────┘
           ▼
┌──────────────────────────────┐
│ RIGHT ANTI RESULT            │
├──────────────────────────────┤
│ 100 | Croissant | 2000       │
│ 106 | Soda | 4000            │
└──────────────────────────────┘
```

### 语法 {#syntax}

```sql
-- Left Anti Join
SELECT select_list
FROM table_a
LEFT ANTI JOIN table_b
           ON join_condition;

-- Right Anti Join
SELECT select_list
FROM table_a
RIGHT ANTI JOIN table_b
            ON join_condition;
```

### 示例 {#examples}

左反连接——没有购买记录的 VIP 客户端：

```sql
SELECT *
FROM vip_info
LEFT ANTI JOIN purchase_records
           ON vip_info.client_id = purchase_records.client_id;
```

结果：

```text
+-----------+---------+
| client_id | region  |
+-----------+---------+
| 101       | Toronto |
+-----------+---------+
```

右反连接——不属于 VIP 客户端的购买记录：

```sql
SELECT *
FROM vip_info
RIGHT ANTI JOIN purchase_records
            ON vip_info.client_id = purchase_records.client_id;
```

结果：

```text
+-----------+-----------+------+
| client_id | item      | qty  |
+-----------+-----------+------+
| 100       | Croissant | 2000 |
| 106       | Soda      | 4000 |
+-----------+-----------+------+
```

## Asof Join {#asof-join}

ASOF（Approximate Sort-Merge）连接会将左侧有序流中的每一行，与右侧时间戳**小于或等于**左侧时间戳的最近一行进行匹配。可选的等值谓词（例如 `symbol` 这样的键）还可以进一步限制匹配范围。ASOF 连接常用于分析场景，例如为每笔交易附加最新的报价。

可以将 ASOF 理解为：“给我在这个事件**发生之前或发生当时**的最新上下文行。”

### 匹配规则 {#matching-rules}

1. 按等值键（例如 `symbol`）对两个表进行分区。
2. 在每个分区内，确保两个表都按不等式列（例如 `time`）进行排序。
3. 访问左表某一行时，附加右表中时间戳 `<=` 左侧时间戳的最新一行；如果不存在，则右侧列为 `NULL`。

### 快速示例（室温 vs HVAC 模式） {#quick-example-room-temperature-vs-hvac-mode}

```text
┌──────────────────────────────┐
│ sensor_readings（左表）      │
├──────────────────────────────┤
│ room | time  | temperature   │
│ LR   | 09:55 | 22.8C         │
│ LR   | 10:00 | 23.1C         │
│ LR   | 10:05 | 23.3C         │
│ LR   | 10:10 | 23.8C         │
│ LR   | 10:15 | 24.0C         │
└──────────────────────────────┘

┌──────────────────────────────┐
│ hvac_mode（右表）            │
├──────────────────────────────┤
│ room | time  | mode          │
│ LR   | 09:58 | Cooling       │
│ LR   | 10:06 | Fan           │
│ LR   | 10:30 | Heating       │
└──────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│ ASOF JOIN ON r.room = m.room 的结果                        │
│                     AND r.reading_time >= m.mode_time      │
├────────────────────────────────────────────────────────────┤
│ 10:00 的读数 -> 匹配 09:58 的模式（最新且 <= 10:00）       │
│ 10:05 的读数 -> 仍匹配 09:58（还没有更新的模式）           │
│ 10:10 的读数 -> 匹配 10:06 的模式                          │
│ 10:15 的读数 -> 匹配 10:06 的模式                          │
│ 09:55 的读数 -> 无行（ASOF 的行为类似 INNER JOIN）         │
└────────────────────────────────────────────────────────────┘
```

在 LEFT ASOF join 中，每条传感器读数都会被保留（例如，09:55 的读数会保留 `NULL`，因为此时还没有任何 HVAC 模式开始）。在 RIGHT ASOF join 中，会保留所有 HVAC 变更（即使此时还没有任何读数可以引用它们）。

### 语法 {#syntax}

```sql
SELECT select_list
FROM table_a
ASOF [LEFT | RIGHT] JOIN table_b
       ON table_a.time >= table_b.time
      [AND table_a.key = table_b.key];
```

### 示例表 {#example-tables}

运行以下语句一次，以重现下面展示的 HVAC 场景：

```sql
CREATE OR REPLACE TABLE sensor_readings (
    reading_time TIMESTAMP,
    temperature  DOUBLE
);
INSERT INTO sensor_readings VALUES
    ('2024-01-01 10:00:00', 23.1),
    ('2024-01-01 10:05:00', 23.3),
    ('2024-01-01 10:10:00', 23.8),
    ('2024-01-01 10:15:00', 24.0);

CREATE OR REPLACE TABLE hvac_mode (
    mode_time TIMESTAMP,
    mode      VARCHAR
);
INSERT INTO hvac_mode VALUES
    ('2024-01-01 09:58:00', 'Cooling'),
    ('2024-01-01 10:06:00', 'Fan'),
    ('2024-01-01 10:30:00', 'Heating');
```

### 示例 {#examples}

将每条温度读数与它之前开始的最新 HVAC 模式进行匹配：

```sql
SELECT r.reading_time, r.temperature, m.mode
FROM sensor_readings AS r
ASOF JOIN hvac_mode AS m
       ON r.room = m.room
      AND r.reading_time >= m.mode_time
ORDER BY r.reading_time;
```

结果：

```text
┌─────────────────────┬─────────────┬────────────┐
│ reading_time        │ temperature │ mode       │
├─────────────────────┼─────────────┼────────────┤
│ 2024-01-01 10:00:00 │ 23.1C       │ Cooling    │
│ 2024-01-01 10:05:00 │ 23.3C       │ Cooling    │
│ 2024-01-01 10:10:00 │ 23.8C       │ Fan        │
│ 2024-01-01 10:15:00 │ 24.0C       │ Fan        │
└─────────────────────┴─────────────┴────────────┘
```

ASOF left join——即使尚未有任何 HVAC 模式处于活动状态，也保留所有传感器读数：

```sql
SELECT r.reading_time, r.temperature, m.mode
FROM sensor_readings AS r
ASOF LEFT JOIN hvac_mode AS m
       ON r.room = m.room
      AND r.reading_time >= m.mode_time
ORDER BY r.reading_time;
```

结果：

```text
┌─────────────────────┬─────────────┬────────────┐
│ reading_time        │ temperature │ mode       │
├─────────────────────┼─────────────┼────────────┤
│ 2024-01-01 09:55:00 │ 22.8C       │ NULL       │ ← 在第一个 HVAC 模式之前
│ 2024-01-01 10:00:00 │ 23.1C       │ Cooling    │
│ 2024-01-01 10:05:00 │ 23.3C       │ Cooling    │
│ 2024-01-01 10:10:00 │ 23.8C       │ Fan        │
│ 2024-01-01 10:15:00 │ 24.0C       │ Fan        │
└─────────────────────┴─────────────┴────────────┘
```

ASOF right join——即使后续没有任何传感器读数引用它们，也保留所有 HVAC 模式变更：

```sql
SELECT r.reading_time, r.temperature, m.mode_time, m.mode
FROM sensor_readings AS r
ASOF RIGHT JOIN hvac_mode AS m
        ON r.room = m.room
       AND r.reading_time >= m.mode_time
ORDER BY m.mode_time, r.reading_time;
```

结果：

```text
┌─────────────────────┬─────────────┬─────────────────────┬────────────┐
│ reading_time        │ temperature │ mode_time           │ mode       │
├─────────────────────┼─────────────┼─────────────────────┼────────────┤
│ 2024-01-01 10:00:00 │ 23.1C       │ 2024-01-01 09:58:00 │ Cooling    │
│ 2024-01-01 10:05:00 │ 23.3C       │ 2024-01-01 09:58:00 │ Cooling    │
│ 2024-01-01 10:10:00 │ 23.8C       │ 2024-01-01 10:06:00 │ Fan        │
│ 2024-01-01 10:15:00 │ 24.0C       │ 2024-01-01 10:06:00 │ Fan        │
│ NULL                │ NULL        │ 2024-01-01 10:30:00 │ Heating    │ ← 等待读数
└─────────────────────┴─────────────┴─────────────────────┴────────────┘
```

多个读数可能落在同一个 HVAC 时间区间内，因此 RIGHT ASOF join 对每个 mode 可能会输出多行；最后一行 `NULL` 表示新调度的 `Heating` 模式尚未匹配到任何读数。