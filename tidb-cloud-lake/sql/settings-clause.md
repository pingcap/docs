---
title: SETTINGS 句
summary: SETTINGS 句は、直後に続く SQL 文の実行動作に影響する特定の設定を構成します。{{{ .lake }}} で利用可能な設定とその値を確認するには、SHOW SETTINGS を使用します。
---

# SETTINGS 句

SETTINGS 句は、直後に続く SQL 文の実行動作に影響する特定の設定を構成します。{{{ .lake }}} で利用可能な設定とその値を確認するには、[SHOW SETTINGS](/tidb-cloud-lake/sql/show-settings.md) を使用します。

関連情報: [SET](/tidb-cloud-lake/sql/set.md)

## 構文 {#syntax}

```sql
SETTINGS ( <setting> = <value> [, <setting> = <value>, ...] ) <statement>
```

## サポートされる文 {#supported-statements}

SETTINGS 句は、次の SQL 文で使用できます。

- [SELECT](/tidb-cloud-lake/sql/select.md)
- [INSERT](/tidb-cloud-lake/sql/insert.md)
- [INSERT (multi-table)](/tidb-cloud-lake/sql/insert-multi-table.md)
- [MERGE](/tidb-cloud-lake/sql/merge.md)
- [`COPY INTO <table>`](/tidb-cloud-lake/sql/copy-into-table.md)
- [`COPY INTO <location>`](/tidb-cloud-lake/sql/copy-into-location.md)
- [UPDATE](/tidb-cloud-lake/sql/update.md)
- [DELETE](/tidb-cloud-lake/sql/delete.md)
- [CREATE TABLE](/tidb-cloud-lake/sql/create-table.md)
- [EXPLAIN](/tidb-cloud-lake/sql/explain.md)

## 例 {#examples}

この例では、SETTINGS 句を使用して SELECT クエリ内の timezone パラメータを調整し、`now()` の表示結果に影響を与える方法を示します。

```sql
-- When no timezone is set, {{{ .lake }}} defaults to UTC, so now() returns the current UTC timestamp
SELECT timezone(), now();

┌─────────────────────────────────────────┐
│ timezone() │            now()           │
│   String   │          Timestamp         │
├────────────┼────────────────────────────┤
│ UTC        │ 2024-11-04 19:42:28.424925 │
└─────────────────────────────────────────┘

-- By setting the timezone to Asia/Shanghai, the now() function returns the local time in Shanghai, which is 8 hours ahead of UTC.
SETTINGS (timezone = 'Asia/Shanghai') SELECT timezone(), now();

┌────────────────────────────────────────────┐
│   timezone()  │            now()           │
├───────────────┼────────────────────────────┤
│ Asia/Shanghai │ 2024-11-05 03:42:42.209404 │
└────────────────────────────────────────────┘

--  Setting the timezone to America/Toronto adjusts the now() output to the local time in Toronto, reflecting the Eastern Time Zone (UTC-5 or UTC-4 during daylight saving time).
SETTINGS (timezone = 'America/Toronto') SELECT timezone(), now();

┌──────────────────────────────────────────────┐
│    timezone()   │            now()           │
│      String     │          Timestamp         │
├─────────────────┼────────────────────────────┤
│ America/Toronto │ 2024-11-04 14:42:48.353577 │
└──────────────────────────────────────────────┘
```

この例では、date_format_style 設定を使用して、MySQL と Oracle の日付フォーマットスタイルを切り替える方法を示します。

```sql
-- Default MySQL style date formatting
SELECT to_string('2024-04-05'::DATE, '%b');

┌────────────────────────────────┐
│ to_string('2024-04-05', '%b')  │
├────────────────────────────────┤
│ Apr                            │
└────────────────────────────────┘

-- Oracle style date formatting
SETTINGS (date_format_style = 'Oracle') SELECT to_string('2024-04-05'::DATE, 'MON');

┌────────────────────────────────┐
│ to_string('2024-04-05', 'MON') │
├────────────────────────────────┤
│ Apr                            │
└────────────────────────────────┘
```

この例では、week_start 設定が週関連の日付関数にどのように影響するかを示します。

```sql
-- Default week_start = 1 (Monday as first day of week)
SELECT date_trunc(WEEK, to_date('2024-04-03'));  -- Wednesday

┌────────────────────────────────────────┐
│ date_trunc(WEEK, to_date('2024-04-03')) │
├────────────────────────────────────────┤
│ 2024-04-01                             │
└────────────────────────────────────────┘

-- Setting week_start = 0 (Sunday as first day of week)
SETTINGS (week_start = 0) SELECT date_trunc(WEEK, to_date('2024-04-03'));  -- Wednesday

┌────────────────────────────────────────┐
│ date_trunc(WEEK, to_date('2024-04-03')) │
├────────────────────────────────────────┤
│ 2024-03-31                             │
└────────────────────────────────────────┘
```

この例では、COPY INTO 操作で並列処理に最大 100 スレッドを使用できるようにします。

```sql
SETTINGS (max_threads = 100) COPY INTO ...
```