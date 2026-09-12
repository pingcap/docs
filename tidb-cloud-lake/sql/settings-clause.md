---
title: SETTINGS 子句
summary: SETTINGS 子句用于配置会影响其前置 SQL 语句执行行为的特定设置。要查看 {{{ .lake }}} 中可用的设置及其值，请使用 SHOW SETTINGS。
---

# SETTINGS 子句

SETTINGS 子句用于配置会影响其前置 SQL 语句执行行为的特定设置。要查看 {{{ .lake }}} 中可用的设置及其值，请使用 [SHOW SETTINGS](/tidb-cloud-lake/sql/show-settings.md)。

另请参阅：[SET](/tidb-cloud-lake/sql/set.md)

## 语法 {#syntax}

```sql
SETTINGS ( <setting> = <value> [, <setting> = <value>, ...] ) <statement>
```

## 支持的语句 {#supported-statements}

SETTINGS 子句可用于以下 SQL 语句：

- [SELECT](/tidb-cloud-lake/sql/select.md)
- [INSERT](/tidb-cloud-lake/sql/insert.md)
- [INSERT（多表）](/tidb-cloud-lake/sql/insert-multi-table.md)
- [MERGE](/tidb-cloud-lake/sql/merge.md)
- [`COPY INTO <table>`](/tidb-cloud-lake/sql/copy-into-table.md)
- [`COPY INTO <location>`](/tidb-cloud-lake/sql/copy-into-location.md)
- [UPDATE](/tidb-cloud-lake/sql/update.md)
- [DELETE](/tidb-cloud-lake/sql/delete.md)
- [CREATE TABLE](/tidb-cloud-lake/sql/create-table.md)
- [EXPLAIN](/tidb-cloud-lake/sql/explain.md)

## 示例 {#examples}

以下示例演示了如何在 SELECT 查询中使用 SETTINGS 子句调整 timezone 参数，从而影响 `now()` 的显示结果：

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

以下示例演示了如何使用 date_format_style 设置在 MySQL 和 Oracle 日期格式样式之间切换：

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

以下示例展示了 week_start 设置如何影响与周相关的日期函数：

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

以下示例允许 COPY INTO 操作最多使用 100 个线程进行并行处理：

```sql
SETTINGS (max_threads = 100) COPY INTO ...
```