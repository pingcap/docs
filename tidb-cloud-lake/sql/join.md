---
title: JOIN
---

## Overview

Joins combine columns from two or more tables into one result set. Databend implements both ANSI SQL joins and Databend-specific extensions, allowing you to work with dimensional data, slowly changing facts, and time-series streams using the same syntax.

## Supported Join Types

* [Inner Join](#inner-join)
* [Natural Join](#natural-join)
* [Cross Join](#cross-join)
* [Left Join](#left-join)
* [Right Join](#right-join)
* [Full Outer Join](#full-outer-join)
* [Left / Right Semi Join](#left--right-semi-join)
* [Left / Right Anti Join](#left--right-anti-join)
* [Asof Join](#asof-join)

## Sample Data

### Prepare the Tables

Run the following SQL once to create and populate the tables used throughout this page:

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

### Preview the Data

Unless stated otherwise, the examples below reuse the same tables so that you can compare the effect of each join type directly.

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

## Inner Join

An inner join returns rows that satisfy all join predicates.

### Visual

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
           │ keep matches only
           ▼
┌──────────────────────────────┐
│ INNER JOIN RESULT            │
├──────────────────────────────┤
│ 102 | Donut  | 3000          │
│ 103 | Coffee | 6000          │
└──────────────────────────────┘
```

### Syntax

```sql
SELECT select_list
FROM table_a
     [INNER] JOIN table_b
              ON join_condition
```

:::tip
`INNER` is optional. When the join columns share the same name, `USING(column_name)` can replace `ON table_a.column = table_b.column`.
:::

### Example

```sql
SELECT p.client_id, p.item, p.qty
FROM vip_info AS v
INNER JOIN purchase_records AS p
        ON v.client_id = p.client_id;
```

Result:

```text
+-----------+--------+------+
| client_id | item   | qty  |
+-----------+--------+------+
| 102       | Donut  | 3000 |
| 103       | Coffee | 6000 |
+-----------+--------+------+
```

## Natural Join

A natural join automatically matches columns that have the same name in both tables. Only one copy of each matched column appears in the result.

### Visual

```text
┌──────────────────────────────┐
│ vip_info                     │
├──────────────────────────────┤
│ client_id | region           │
│ 101       | Toronto          │
│ 102       | Quebec           │
│ 103       | Vancouver        │
└──────────────────────────────┘
           │ auto-match shared column names
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
           │ emit shared columns once
           ▼
┌──────────────────────────────┐
│ NATURAL JOIN RESULT          │
├──────────────────────────────┤
│ 102: Quebec + Donut + 3000   │
│ 103: Vanc. + Coffee + 6000   │
└──────────────────────────────┘
```

### Syntax

```sql
SELECT select_list
FROM table_a
NATURAL JOIN table_b;
```

### Example

```sql
SELECT client_id, item, qty
FROM vip_info
NATURAL JOIN purchase_records;
```

Result:

```text
+-----------+--------+------+
| client_id | item   | qty  |
+-----------+--------+------+
| 102       | Donut  | 3000 |
| 103       | Coffee | 6000 |
+-----------+--------+------+
```

## Cross Join

A cross join (Cartesian product) returns every combination of rows from the participating tables.

### Visual

```text
┌──────────────────────────────┐
│ vip_info (3 rows)            │
├──────────────────────────────┤
│ 101 | Toronto                │
│ 102 | Quebec                 │
│ 103 | Vancouver              │
└──────────────────────────────┘
           │ pair with every gift
           ▼
┌──────────────────────────────┐
│ gift (4 rows)                │
├──────────────────────────────┤
│ Croissant                    │
│ Donut                        │
│ Coffee                       │
│ Soda                         │
└──────────────────────────────┘
           │ 3 × 4 combinations
           ▼
┌──────────────────────────────┐
│ CROSS JOIN RESULT (snippet)  │
├──────────────────────────────┤
│ 101 | Toronto  | Croissant   │
│ 101 | Toronto  | Donut       │
│ 101 | Toronto  | Coffee      │
│ ... | ...      | ...         │
└──────────────────────────────┘
```

### Syntax

```sql
SELECT select_list
FROM table_a
CROSS JOIN table_b;
```

### Example

```sql
SELECT v.client_id, v.region, g.gift
FROM vip_info AS v
CROSS JOIN gift AS g;
```

Result (first few rows):

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

## Left Join

A left join returns every row from the left table and the matching rows from the right table. When no match exists, the right-side columns are `NULL`.

### Visual

```text
┌──────────────────────────────┐
│ vip_info (left preserved)    │
├──────────────────────────────┤
│ 101 | Toronto                │
│ 102 | Quebec                 │
│ 103 | Vancouver              │
└──────────────────────────────┘
           │ join on client_id
           ▼
┌──────────────────────────────┐
│ purchase_records             │
├──────────────────────────────┤
│ 100 | Croissant | 2000       │
│ 102 | Donut     | 3000       │
│ 103 | Coffee    | 6000       │
│ 106 | Soda      | 4000       │
└──────────────────────────────┘
           │ unmatched right rows -> NULLs
           ▼
┌──────────────────────────────┐
│ LEFT JOIN RESULT             │
├──────────────────────────────┤
│ 101 | Toronto | NULL | NULL  │
│ 102 | Quebec  | Donut | 3000 │
│ 103 | Vanc.   | Coffee | 6000│
└──────────────────────────────┘
```

### Syntax

```sql
SELECT select_list
FROM table_a
LEFT [OUTER] JOIN table_b
             ON join_condition;
```

:::tip
`OUTER` is optional.
:::

### Example

```sql
SELECT v.client_id, p.item, p.qty
FROM vip_info AS v
LEFT JOIN purchase_records AS p
       ON v.client_id = p.client_id;
```

Result:

```text
+-----------+--------+------+
| client_id | item   | qty  |
+-----------+--------+------+
| 101       | NULL   | NULL |
| 102       | Donut  | 3000 |
| 103       | Coffee | 6000 |
+-----------+--------+------+
```

## Right Join

A right join mirrors the left join: all rows from the right table appear, and unmatched rows from the left table produce `NULL`s.

### Visual

```text
┌──────────────────────────────┐
│ purchase_records (right)     │
├──────────────────────────────┤
│ 100 | Croissant | 2000       │
│ 102 | Donut     | 3000       │
│ 103 | Coffee    | 6000       │
│ 106 | Soda      | 4000       │
└──────────────────────────────┘
           ▲ right table preserved
           │ join on client_id
┌──────────────────────────────┐
│ vip_info                     │
├──────────────────────────────┤
│ 101 | Toronto                │
│ 102 | Quebec                 │
│ 103 | Vancouver              │
└──────────────────────────────┘
           ▼ fill missing VIP data with NULL
┌──────────────────────────────┐
│ RIGHT JOIN RESULT            │
├──────────────────────────────┤
│ 100 | Croissant | vip=NULL   │
│ 102 | Donut | region=Quebec  │
│ 103 | Coffee | region=Vanc.  │
│ 106 | Soda | vip=NULL        │
└──────────────────────────────┘
```

### Syntax

```sql
SELECT select_list
FROM table_a
RIGHT [OUTER] JOIN table_b
              ON join_condition;
```

### Example

```sql
SELECT v.client_id, v.region
FROM vip_info AS v
RIGHT JOIN purchase_records AS p
       ON v.client_id = p.client_id;
```

Result:

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

## Full Outer Join

A full outer join returns the union of left and right joins: every row from both tables, with `NULL`s where no match exists.

### Visual

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
           │ combine matches + left-only + right-only
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

### Syntax

```sql
SELECT select_list
FROM table_a
FULL [OUTER] JOIN table_b
             ON join_condition;
```

### Example

```sql
SELECT v.region, p.item
FROM vip_info AS v
FULL OUTER JOIN purchase_records AS p
            ON v.client_id = p.client_id;
```

Result:

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

## Left / Right Semi Join

Semi joins filter the left (or right) table to rows that have at least one match in the opposite table. Unlike inner joins, only columns from the preserved side are returned.

### Visual

```text
LEFT SEMI JOIN
┌──────────────────────────────┐
│ vip_info                     │
├──────────────────────────────┤
│ 101 | Toronto                │
│ 102 | Quebec                 │
│ 103 | Vancouver              │
└──────────────────────────────┘
           │ keep rows that find matches
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
           │ keep rows with VIP matches
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

### Syntax

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

### Examples

Left semi join—return VIP clients with purchases:

```sql
SELECT *
FROM vip_info
LEFT SEMI JOIN purchase_records
           ON vip_info.client_id = purchase_records.client_id;
```

Result:

```text
+-----------+-----------+
| client_id | region    |
+-----------+-----------+
| 102       | Quebec    |
| 103       | Vancouver |
+-----------+-----------+
```

Right semi join—return purchase rows that belong to VIP clients:

```sql
SELECT *
FROM vip_info
RIGHT SEMI JOIN purchase_records
            ON vip_info.client_id = purchase_records.client_id;
```

Result:

```text
+-----------+--------+------+
| client_id | item   | qty  |
+-----------+--------+------+
| 102       | Donut  | 3000 |
| 103       | Coffee | 6000 |
+-----------+--------+------+
```

## Left / Right Anti Join

Anti joins return rows that do **not** have a matching row on the other side, making them ideal for existence checks.

### Visual

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

### Syntax

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

### Examples

Left anti join—VIP clients with no purchases:

```sql
SELECT *
FROM vip_info
LEFT ANTI JOIN purchase_records
           ON vip_info.client_id = purchase_records.client_id;
```

Result:

```text
+-----------+---------+
| client_id | region  |
+-----------+---------+
| 101       | Toronto |
+-----------+---------+
```

Right anti join—purchase records that do not belong to a VIP client:

```sql
SELECT *
FROM vip_info
RIGHT ANTI JOIN purchase_records
            ON vip_info.client_id = purchase_records.client_id;
```

Result:

```text
+-----------+-----------+------+
| client_id | item      | qty  |
+-----------+-----------+------+
| 100       | Croissant | 2000 |
| 106       | Soda      | 4000 |
+-----------+-----------+------+
```

## Asof Join

An ASOF (Approximate Sort-Merge) join matches each row in a left-ordered stream to the most recent row on the right whose timestamp is **less than or equal to** the left timestamp. Optional equality predicates (for keys such as `symbol`) can further constrain the match. ASOF joins power analytics like attaching the latest quote to each trade.

Think of ASOF as "give me the latest contextual row that happened **before or at** this event."

### Matching Rules

1. Partition both tables by the equality keys (for example, `symbol`).
2. Within each partition, ensure both tables are sorted by the inequality column (for example, `time`).
3. When visiting a left row, attach the latest right row whose timestamp is `<=` the left timestamp; if none exists, the right columns are `NULL`.

### Quick Example (Room Temperature vs HVAC Mode)

```text
┌──────────────────────────────┐
│ sensor_readings (left table) │
├──────────────────────────────┤
│ room | time  | temperature   │
│ LR   | 09:55 | 22.8C         │
│ LR   | 10:00 | 23.1C         │
│ LR   | 10:05 | 23.3C         │
│ LR   | 10:10 | 23.8C         │
│ LR   | 10:15 | 24.0C         │
└──────────────────────────────┘

┌──────────────────────────────┐
│ hvac_mode (right table)      │
├──────────────────────────────┤
│ room | time  | mode          │
│ LR   | 09:58 | Cooling       │
│ LR   | 10:06 | Fan           │
│ LR   | 10:30 | Heating       │
└──────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│ Result of ASOF JOIN ON r.room = m.room                      │
│                     AND r.reading_time >= m.mode_time       │
├────────────────────────────────────────────────────────────┤
│ 10:00 reading -> matches 09:58 mode (latest <= 10:00)      │
│ 10:05 reading -> still matches 09:58 (no newer mode yet)   │
│ 10:10 reading -> matches 10:06 mode                        │
│ 10:15 reading -> matches 10:06 mode                        │
│ 09:55 reading -> no row (ASOF behaves like INNER JOIN)     │
└────────────────────────────────────────────────────────────┘
```

In LEFT ASOF joins every sensor reading stays (for example, the 09:55 reading keeps `NULL` because no HVAC mode has started yet). In RIGHT ASOF joins you keep all HVAC changes (even if no reading has happened yet to reference them).

### Syntax

```sql
SELECT select_list
FROM table_a
ASOF [LEFT | RIGHT] JOIN table_b
       ON table_a.time >= table_b.time
      [AND table_a.key = table_b.key];
```

### Example Tables

Run the following once to reproduce the HVAC scenario shown below:

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

### Examples

Match each temperature reading with the latest HVAC mode that started before it:

```sql
SELECT r.reading_time, r.temperature, m.mode
FROM sensor_readings AS r
ASOF JOIN hvac_mode AS m
       ON r.room = m.room
      AND r.reading_time >= m.mode_time
ORDER BY r.reading_time;
```

Result:

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

ASOF left join—keep all sensor readings even if no HVAC mode was active yet:

```sql
SELECT r.reading_time, r.temperature, m.mode
FROM sensor_readings AS r
ASOF LEFT JOIN hvac_mode AS m
       ON r.room = m.room
      AND r.reading_time >= m.mode_time
ORDER BY r.reading_time;
```

Result:

```text
┌─────────────────────┬─────────────┬────────────┐
│ reading_time        │ temperature │ mode       │
├─────────────────────┼─────────────┼────────────┤
│ 2024-01-01 09:55:00 │ 22.8C       │ NULL       │ ← before first HVAC mode
│ 2024-01-01 10:00:00 │ 23.1C       │ Cooling    │
│ 2024-01-01 10:05:00 │ 23.3C       │ Cooling    │
│ 2024-01-01 10:10:00 │ 23.8C       │ Fan        │
│ 2024-01-01 10:15:00 │ 24.0C       │ Fan        │
└─────────────────────┴─────────────┴────────────┘
```

ASOF right join—keep all HVAC mode changes even if no later sensor reading references them:

```sql
SELECT r.reading_time, r.temperature, m.mode_time, m.mode
FROM sensor_readings AS r
ASOF RIGHT JOIN hvac_mode AS m
        ON r.room = m.room
       AND r.reading_time >= m.mode_time
ORDER BY m.mode_time, r.reading_time;
```

Result:

```text
┌─────────────────────┬─────────────┬─────────────────────┬────────────┐
│ reading_time        │ temperature │ mode_time           │ mode       │
├─────────────────────┼─────────────┼─────────────────────┼────────────┤
│ 2024-01-01 10:00:00 │ 23.1C       │ 2024-01-01 09:58:00 │ Cooling    │
│ 2024-01-01 10:05:00 │ 23.3C       │ 2024-01-01 09:58:00 │ Cooling    │
│ 2024-01-01 10:10:00 │ 23.8C       │ 2024-01-01 10:06:00 │ Fan        │
│ 2024-01-01 10:15:00 │ 24.0C       │ 2024-01-01 10:06:00 │ Fan        │
│ NULL                │ NULL        │ 2024-01-01 10:30:00 │ Heating    │ ← waiting for reading
└─────────────────────┴─────────────┴─────────────────────┴────────────┘
```

Multiple readings can land in the same HVAC interval, so a RIGHT ASOF join can emit more than one row per mode; the final `NULL` row shows the newly scheduled `Heating` mode that has not yet matched a reading.
