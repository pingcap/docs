---
title: ADD_MONTHS
summary: add_months() 関数は、指定した月数を指定した日付またはタイムスタンプに加算します。
---

# ADD_MONTHS

add_months() 関数は、指定した月数を指定した日付またはタイムスタンプに加算します。

入力日付が月末である場合、または加算後の月の日数を超える場合、結果は新しい月の末日に調整されます。それ以外の場合は、元の日が保持されます。

## 構文 {#syntax}

```sql
ADD_MONTHS(<date_or_timestamp>, <number_of_months>)
```

| Parameter            | 説明                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `<date_or_timestamp>` | 月を加算する基準となる開始日付またはタイムスタンプ               |
| `<number_of_months>`  | 加算する月数を表す整数（負の値を指定すると月を減算可能）   |

## 戻り値の型 {#return-type}

TIMESTAMP または DATE 型を返します

## 例 {#examples}

### 基本的な月の加算 {#basic-month-addition}

```sql
SELECT ADD_MONTHS('2023-01-15'::DATE, 3);
├───────────────────────────────────┤
│ 2023-04-15                        │
╰───────────────────────────────────╯
```

### 月の減算 {#subtracting-months}

```sql
SELECT ADD_MONTHS('2023-06-20'::DATE, -4);
├─────────────────────────────────────┤
│ 2023-02-20                          │
╰─────────────────────────────────────╯
```

### 月末調整 {#month-end-adjustment}

```sql
SELECT ADD_MONTHS('2023-01-31'::DATE, 1);
├───────────────────────────────────┤
│ 2023-02-28                        │
╰───────────────────────────────────╯
```

### タイムスタンプを保持する場合 {#with-timestamp-preservation}

```sql
SELECT ADD_MONTHS('2023-03-15 14:30:00'::TIMESTAMP, 5);
├─────────────────────────────────────────────────┤
│ 2023-08-15 14:30:00.000000                      │
╰─────────────────────────────────────────────────╯
```

### 月末日を使用する場合 {#with-last-day-of-month}

```sql
CREATE TABLE contracts (
    id INT,
    sign_date DATE,
    duration_months INT
);

INSERT INTO contracts VALUES
    (1, '2023-01-15', 12),
    (2, '2024-02-28', 6),
    (3, '2023-11-30', 3);

SELECT
    id,
    sign_date,
    ADD_MONTHS(sign_date, duration_months) AS end_date
FROM contracts;
├─────────────────┼────────────────┼────────────────┤
│               1 │ 2023-01-15     │ 2024-01-15     │
│               2 │ 2024-02-28     │ 2024-08-28     │
│               3 │ 2023-11-30     │ 2024-02-29     │
╰───────────────────────────────────────────────────╯

```

## 関連項目 {#see-also}

- [DATE_ADD](/tidb-cloud-lake/sql/date-add.md): 特定の時間間隔を加算するための代替関数
- [DATE_SUB](/tidb-cloud-lake/sql/date-sub.md): 時間間隔を減算する関数