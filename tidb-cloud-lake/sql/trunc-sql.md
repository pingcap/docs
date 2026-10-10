---
title: TRUNC
summary: 日付またはタイムスタンプを指定した精度に切り捨てます。この関数は広く採用されている日付切り捨て構文に従っているため、他のデータベースシステムから移行するユーザーにとって使いやすくなっています。
---

# TRUNC

> **Note:**
>
> v1.2.745 で導入されました。

日付またはタイムスタンプを指定した精度に切り捨てます。この関数は広く採用されている日付切り捨て構文に従っているため、他のデータベースシステムから移行するユーザーにとって使いやすくなっています。

## 構文 {#syntax}

```sql
TRUNC(<date_or_timestamp>, <datetime_interval_type>)
```

| パラメータ | 説明 |
|----------------------------|------------------------------------------------------------------------------------------------------------|
| `<date_or_timestamp>`      | `DATE` または `TIMESTAMP` 型の値です。                                                                     |
| `<datetime_interval_type>` | 次のいずれかの値である必要があります: `YEAR`, `QUARTER`, `MONTH`, `WEEK`, `DAY`, `HOUR`, `MINUTE`, `SECOND`。 |

## 週の開始日の設定 {#week-start-configuration}

datetime interval type として `WEEK` を使用する場合、結果は週の最初の日を定義する `week_start` 設定に依存します。

- `week_start = 1` (default): 月曜日が週の最初の日と見なされます
- `week_start = 0`: 日曜日が週の最初の日と見なされます

特定のクエリに対してこの設定を変更するには、`SETTINGS` 句を使用できます。

```sql
-- Set Sunday as the first day of the week
SETTINGS (week_start = 0) SELECT TRUNC(to_date('2024-04-05'), 'WEEK');

-- Set Monday as the first day of the week (default)
SETTINGS (week_start = 1) SELECT TRUNC(to_date('2024-04-05'), 'WEEK');
```

## 戻り値の型 {#return-type}

`<date_or_timestamp>` と同じです。

## 例 {#examples}

```sql
-- Truncate to different precisions
SELECT
    TRUNC(to_date('2022-07-07'), 'MONTH'),
    TRUNC(to_date('2022-07-07'), 'WEEK'),
    TRUNC(to_date('2022-07-07'), 'YEAR');

┌────────────────────────────────────────────────────────────────────────────────────┐
│ TRUNC(to_date('2022-07-07'), 'MONTH') │ TRUNC(to_date('2022-07-07'), 'WEEK') │ TRUNC(to_date('2022-07-07'), 'YEAR') │
├──────────────────────────────────────┼─────────────────────────────────────┼─────────────────────────────────────┤
│ 2022-07-01                           │ 2022-07-04                          │ 2022-01-01                          │
└────────────────────────────────────────────────────────────────────────────────────┘
```

次の例は、`week_start` 設定が `WEEK` 精度の `TRUNC` の結果にどのように影響するかを示しています。

```sql
-- Default: week_start = 1 (Monday as first day of week)
SELECT TRUNC(to_date('2024-04-03'), 'WEEK');  -- Wednesday

┌─────────────────────────────────────┐
│ TRUNC(to_date('2024-04-03'), 'WEEK') │
├─────────────────────────────────────┤
│ 2024-04-01                          │ -- Monday
└─────────────────────────────────────┘

-- Setting week_start = 0 (Sunday as first day of week)
SETTINGS (week_start = 0) SELECT TRUNC(to_date('2024-04-03'), 'WEEK');  -- Wednesday

┌─────────────────────────────────────┐
│ TRUNC(to_date('2024-04-03'), 'WEEK') │
├─────────────────────────────────────┤
│ 2024-03-31                          │ -- Sunday
└─────────────────────────────────────┘
```

タイムスタンプ値で `TRUNC` を使用する例:

```sql
SELECT TRUNC(to_timestamp('2022-07-07 15:30:45.123456'), 'DAY');

┌───────────────────────────────────────────────────────┐
│ TRUNC(to_timestamp('2022-07-07 15:30:45.123456'), 'DAY') │
├───────────────────────────────────────────────────────┤
│ 2022-07-07 00:00:00.000000                            │
└───────────────────────────────────────────────────────┘
```