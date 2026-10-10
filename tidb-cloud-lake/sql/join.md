---
title: JOIN
summary: テーブル結合は、2 つ以上のテーブルのカラムを 1 つの結果セットに結合します。{{{ .lake }}} は ANSI SQL の JOIN と Lake 固有の拡張の両方を実装しており、同じ構文でディメンショナルデータ、緩やかに変化するファクト、時系列ストリームを扱えます。
---

# JOIN

## 概要 {#overview}

テーブル結合は、2 つ以上のテーブルのカラムを 1 つの結果セットに結合します。{{{ .lake }}} は ANSI SQL の JOIN と Lake 固有の拡張の両方を実装しており、同じ構文でディメンショナルデータ、緩やかに変化するファクト、時系列ストリームを扱えます。

## サポートされる JOIN の種類 {#supported-join-types}

* [内部結合](#inner-join)
* [Natural Join](#natural-join)
* [Cross Join](#cross-join)
* [Left Join](#left-join)
* [Right Join](#right-join)
* [Full Outer Join](#full-outer-join)
* [左 / 右セミ結合](#left--right-semi-join)
* [左 / 右アンチ結合](#left--right-anti-join)
* [Asof Join](#asof-join)

## サンプルデータ {#sample-data}

### テーブルを準備する {#prepare-the-tables}

このページ全体で使用するテーブルを作成し、データを投入するために、次の SQL を 1 回実行します。

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

### データをプレビューする {#preview-the-data}

特に明記しない限り、以下の例では同じテーブルを再利用するため、各 JOIN の種類による効果を直接比較できます。

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

## 内部結合 {#inner-join}

内部結合は、すべての結合条件を満たす行を返します。

### 図解 {#visual}

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
           │ 一致した行のみを保持
           ▼
┌──────────────────────────────┐
│ INNER JOIN RESULT            │
├──────────────────────────────┤
│ 102 | Donut  | 3000          │
│ 103 | Coffee | 6000          │
└──────────────────────────────┘
```

### 構文 {#syntax}

```sql
SELECT select_list
FROM table_a
     [INNER] JOIN table_b
              ON join_condition
```

> **Tip:**
>
> `INNER` は省略可能です。結合に使うカラム名が同じ場合は、`ON table_a.column = table_b.column` の代わりに `USING(column_name)` を使用できます。

### 例 {#example}

```sql
SELECT p.client_id, p.item, p.qty
FROM vip_info AS v
INNER JOIN purchase_records AS p
        ON v.client_id = p.client_id;
```

結果:

```text
+-----------+--------+------+
| client_id | item   | qty  |
+-----------+--------+------+
| 102       | Donut  | 3000 |
| 103       | Coffee | 6000 |
+-----------+--------+------+
```

## Natural Join {#natural-join}

Natural Join は、両方のテーブルで同じ名前を持つカラムを自動的に対応付けます。一致した各カラムは、結果に 1 回だけ表示されます。

### Visual {#visual}

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

### Syntax {#syntax}

```sql
SELECT select_list
FROM table_a
NATURAL JOIN table_b;
```

### Example {#example}

```sql
SELECT client_id, item, qty
FROM vip_info
NATURAL JOIN purchase_records;
```

結果:

```text
+-----------+--------+------+
| client_id | item   | qty  |
+-----------+--------+------+
| 102       | Donut  | 3000 |
| 103       | Coffee | 6000 |
+-----------+--------+------+
```

## Cross Join {#cross-join}

Cross Join（直積）は、結合に参加するテーブルの行のあらゆる組み合わせを返します。

### Visual {#visual}

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

### Syntax {#syntax}

```sql
SELECT select_list
FROM table_a
CROSS JOIN table_b;
```

### Example {#example}

```sql
SELECT v.client_id, v.region, g.gift
FROM vip_info AS v
CROSS JOIN gift AS g;
```

結果（先頭の数行）:

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

## Left Join {#left-join}

Left Join は、左側のテーブルのすべての行と、右側のテーブルで一致する行を返します。一致する行がない場合、右側のカラムは `NULL` になります。

### Visual {#visual}

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

### Syntax {#syntax}

```sql
SELECT select_list
FROM table_a
LEFT [OUTER] JOIN table_b
             ON join_condition;
```

> **Tip:**
>
> `OUTER` は省略可能です。

### Example {#example}

```sql
SELECT v.client_id, p.item, p.qty
FROM vip_info AS v
LEFT JOIN purchase_records AS p
       ON v.client_id = p.client_id;
```

結果:

```text
+-----------+--------+------+
| client_id | item   | qty  |
+-----------+--------+------+
| 101       | NULL   | NULL |
| 102       | Donut  | 3000 |
| 103       | Coffee | 6000 |
+-----------+--------+------+
```

## Right Join {#right-join}

Right Join は Left Join を左右反転したものです。右側のテーブルのすべての行が結果に含まれ、左側のテーブルで一致しない行は `NULL` になります。

### Visual {#visual}

```text
┌──────────────────────────────┐
│ purchase_records (right)     │
├──────────────────────────────┤
│ 100 | Croissant | 2000       │
│ 102 | Donut     | 3000       │
│ 103 | Coffee    | 6000       │
│ 106 | Soda      | 4000       │
└──────────────────────────────┘
           ▲ 右側のテーブルが保持される
           │ client_id で結合
┌──────────────────────────────┐
│ vip_info                     │
├──────────────────────────────┤
│ 101 | Toronto                │
│ 102 | Quebec                 │
│ 103 | Vancouver              │
└──────────────────────────────┘
           ▼ 一致しない VIP データは NULL で埋める
┌──────────────────────────────┐
│ RIGHT JOIN RESULT            │
├──────────────────────────────┤
│ 100 | Croissant | vip=NULL   │
│ 102 | Donut | region=Quebec  │
│ 103 | Coffee | region=Vanc.  │
│ 106 | Soda | vip=NULL        │
└──────────────────────────────┘
```

### Syntax {#syntax}

```sql
SELECT select_list
FROM table_a
RIGHT [OUTER] JOIN table_b
              ON join_condition;
```

### Example {#example}

```sql
SELECT v.client_id, v.region
FROM vip_info AS v
RIGHT JOIN purchase_records AS p
       ON v.client_id = p.client_id;
```

結果:

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

## Full Outer Join {#full-outer-join}

Full Outer Join は Left Join と Right Join の和集合を返します。両方のテーブルのすべての行が結果に含まれ、一致しない場合は `NULL` になります。

### Visual {#visual}

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
           │ 一致する行 + 左側のみにある行 + 右側のみにある行を結合
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

### Syntax {#syntax}

```sql
SELECT select_list
FROM table_a
FULL [OUTER] JOIN table_b
             ON join_condition;
```

### Example {#example}

```sql
SELECT v.region, p.item
FROM vip_info AS v
FULL OUTER JOIN purchase_records AS p
            ON v.client_id = p.client_id;
```

結果:

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

## Left / Right Semi Join {#left-right-semi-join}

Semi Join は、反対側のテーブルに少なくとも 1 件一致する行があるものだけを左側（または右側）のテーブルから抽出します。Inner Join と異なり、返されるのは保持される側のカラムだけです。

### Visual {#visual}

```text
LEFT SEMI JOIN
┌──────────────────────────────┐
│ vip_info                     │
├──────────────────────────────┤
│ 101 | Toronto                │
│ 102 | Quebec                 │
│ 103 | Vancouver              │
└──────────────────────────────┘
           │ 一致する行があるものだけを残す
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
           │ VIP に一致する行だけを残す
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

### 構文 {#syntax}

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

### 例 {#examples}

Left semi join—購入履歴のある VIP 顧客を返します:

```sql
SELECT *
FROM vip_info
LEFT SEMI JOIN purchase_records
           ON vip_info.client_id = purchase_records.client_id;
```

結果:

```text
+-----------+-----------+
| client_id | region    |
+-----------+-----------+
| 102       | Quebec    |
| 103       | Vancouver |
+-----------+-----------+
```

Right semi join—VIP 顧客に属する購入行を返します:

```sql
SELECT *
FROM vip_info
RIGHT SEMI JOIN purchase_records
            ON vip_info.client_id = purchase_records.client_id;
```

結果:

```text
+-----------+--------+------+
| client_id | item   | qty  |
+-----------+--------+------+
| 102       | Donut  | 3000 |
| 103       | Coffee | 6000 |
+-----------+--------+------+
```

## Left / Right Anti Join {#left-right-anti-join}

Anti join は、反対側に一致する行が**存在しない**行を返すため、存在チェックに最適です。

### 図解 {#visual}

```text
LEFT ANTI JOIN
┌──────────────────────────────┐
│ vip_info                     │
├──────────────────────────────┤
│ 101 | Toronto                │
│ 102 | Quebec                 │
│ 103 | Vancouver              │
└──────────────────────────────┘
           │ 一致する行を削除
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
           │ VIP と一致する行を削除
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

### 構文 {#syntax}

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

### 例 {#examples}

Left anti join—購入履歴のない VIP 顧客:

```sql
SELECT *
FROM vip_info
LEFT ANTI JOIN purchase_records
           ON vip_info.client_id = purchase_records.client_id;
```

結果:

```text
+-----------+---------+
| client_id | region  |
+-----------+---------+
| 101       | Toronto |
+-----------+---------+
```

Right anti join—VIP 顧客に属さない購入レコード:

```sql
SELECT *
FROM vip_info
RIGHT ANTI JOIN purchase_records
            ON vip_info.client_id = purchase_records.client_id;
```

結果:

```text
+-----------+-----------+------+
| client_id | item      | qty  |
+-----------+-----------+------+
| 100       | Croissant | 2000 |
| 106       | Soda      | 4000 |
+-----------+-----------+------+
```

## Asof Join {#asof-join}

ASOF (Approximate Sort-Merge) join は、左側の順序付けされたストリームの各行を、タイムスタンプが左側のタイムスタンプ以下である右側の最新行に対応付けます。`symbol` のようなキーに対する任意の等価述語を使うことで、さらに一致条件を絞り込めます。ASOF join は、各取引に最新の気配値を付加するような分析処理で役立ちます。

ASOF は、「このイベントの**前または同時点**で発生した最新のコンテキスト行を返す」と考えると分かりやすいです。

### 一致ルール {#matching-rules}

1. 両方のテーブルを等価キー（たとえば `symbol`）でパーティション分割します。
2. 各パーティション内で、両方のテーブルが不等号に使うカラム（たとえば `time`）でソートされていることを確認します。
3. 左側の行を処理するとき、タイムスタンプが左側のタイムスタンプ `<=` である右側の最新行を対応付けます。該当する行が存在しない場合、右側のカラムは `NULL` になります。

### クイック例（室温と HVAC モード） {#quick-example-room-temperature-vs-hvac-mode}

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

LEFT ASOF テーブル結合では、すべてのセンサー読み取り値が保持されます（たとえば、09:55 の読み取り値は、まだ HVAC モードが開始されていないため `NULL` のままです）。RIGHT ASOF テーブル結合では、すべての HVAC の変更が保持されます（それらを参照する読み取り値がまだ発生していなくても保持されます）。

### 構文 {#syntax}

```sql
SELECT select_list
FROM table_a
ASOF [LEFT | RIGHT] JOIN table_b
       ON table_a.time >= table_b.time
      [AND table_a.key = table_b.key];
```

### 例のテーブル {#example-tables}

以下を 1 回実行すると、下に示す HVAC シナリオを再現できます。

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

### 例 {#examples}

各温度読み取り値を、それより前に開始された最新の HVAC モードに対応付けます。

```sql
SELECT r.reading_time, r.temperature, m.mode
FROM sensor_readings AS r
ASOF JOIN hvac_mode AS m
       ON r.room = m.room
      AND r.reading_time >= m.mode_time
ORDER BY r.reading_time;
```

結果:

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

ASOF LEFT JOIN—まだ有効な HVAC モードが存在しない場合でも、すべてのセンサー読み取り値を保持します。

```sql
SELECT r.reading_time, r.temperature, m.mode
FROM sensor_readings AS r
ASOF LEFT JOIN hvac_mode AS m
       ON r.room = m.room
      AND r.reading_time >= m.mode_time
ORDER BY r.reading_time;
```

結果:

```text
┌─────────────────────┬─────────────┬────────────┐
│ reading_time        │ temperature │ mode       │
├─────────────────────┼─────────────┼────────────┤
│ 2024-01-01 09:55:00 │ 22.8C       │ NULL       │ ← 最初の HVAC モードより前
│ 2024-01-01 10:00:00 │ 23.1C       │ Cooling    │
│ 2024-01-01 10:05:00 │ 23.3C       │ Cooling    │
│ 2024-01-01 10:10:00 │ 23.8C       │ Fan        │
│ 2024-01-01 10:15:00 │ 24.0C       │ Fan        │
└─────────────────────┴─────────────┴────────────┘
```

ASOF RIGHT JOIN—後続のセンサー読み取り値がそれらを参照しない場合でも、すべての HVAC モード変更を保持します。

```sql
SELECT r.reading_time, r.temperature, m.mode_time, m.mode
FROM sensor_readings AS r
ASOF RIGHT JOIN hvac_mode AS m
        ON r.room = m.room
       AND r.reading_time >= m.mode_time
ORDER BY m.mode_time, r.reading_time;
```

結果:

```text
┌─────────────────────┬─────────────┬─────────────────────┬────────────┐
│ reading_time        │ temperature │ mode_time           │ mode       │
├─────────────────────┼─────────────┼─────────────────────┼────────────┤
│ 2024-01-01 10:00:00 │ 23.1C       │ 2024-01-01 09:58:00 │ Cooling    │
│ 2024-01-01 10:05:00 │ 23.3C       │ 2024-01-01 09:58:00 │ Cooling    │
│ 2024-01-01 10:10:00 │ 23.8C       │ 2024-01-01 10:06:00 │ Fan        │
│ 2024-01-01 10:15:00 │ 24.0C       │ 2024-01-01 10:06:00 │ Fan        │
│ NULL                │ NULL        │ 2024-01-01 10:30:00 │ Heating    │ ← 読み取り待ち
└─────────────────────┴─────────────┴─────────────────────┴────────────┘
```

複数の読み取り値が同じ HVAC 区間に入ることがあるため、RIGHT ASOF テーブル結合では 1 つのモードに対して複数行が出力される場合があります。最後の `NULL` 行は、まだ読み取り値と一致していない、新たに予定された `Heating` モードを示しています。