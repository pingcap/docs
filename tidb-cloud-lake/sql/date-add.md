---
title: DATE_ADD
summary: DATE または TIMESTAMP 値に指定した時間間隔を加算します。
---

# DATE_ADD

DATE または TIMESTAMP 値に指定した時間間隔を加算します。

## 構文 {#syntax}

```sql
DATE_ADD(<unit>, <interval>,  <date_or_time_expr>)
```

| パラメータ | 説明 |
|-----------------------|----------------------------------------------------------------------------------------------------|
| `<unit>`              | 時間単位を指定します: `YEAR`、`QUARTER`、`MONTH`、`WEEK`、`DAY`、`HOUR`、`MINUTE`、`SECOND`。 |
| `<interval>`          | 加算する間隔です。たとえば、単位が `DAY` の場合、2 は 2 日を意味します。 |
| `<date_or_time_expr>` | `DATE` または `TIMESTAMP` 型の値です。 |

## 戻り値の型 {#return-type}

`<date_or_time_expr>` の型に応じて、DATE または TIMESTAMP を返します。

## 例 {#examples}

この例では、現在の日付に異なる時間間隔（年、四半期、月、週、日）を加算します。

```sql
SELECT
    TODAY(),
    DATE_ADD(YEAR, 1, TODAY()),
    DATE_ADD(QUARTER, 1, TODAY()),
    DATE_ADD(MONTH, 1, TODAY()),
    DATE_ADD(WEEK, 1, TODAY()),
    DATE_ADD(DAY, 1, TODAY());

-[ RECORD 1 ]-----------------------------------
                      today(): 2024-10-10
   DATE_ADD(YEAR, 1, today()): 2025-10-10
DATE_ADD(QUARTER, 1, today()): 2025-01-10
  DATE_ADD(MONTH, 1, today()): 2024-11-10
   DATE_ADD(WEEK, 1, today()): 2024-10-17
    DATE_ADD(DAY, 1, today()): 2024-10-11
```

この例では、現在のタイムスタンプに異なる時間間隔（時、分、秒）を加算します。

```sql
SELECT
    NOW(),
    DATE_ADD(HOUR, 1, NOW()),
    DATE_ADD(MINUTE, 1, NOW()),
    DATE_ADD(SECOND, 1, NOW());

-[ RECORD 1 ]-----------------------------------
                     now(): 2024-10-10 01:35:33.601312
  DATE_ADD(HOUR, 1, now()): 2024-10-10 02:35:33.601312
DATE_ADD(MINUTE, 1, now()): 2024-10-10 01:36:33.601312
DATE_ADD(SECOND, 1, now()): 2024-10-10 01:35:34.601312
```

- unit が MONTH の場合、date が月の最終日であるとき、または結果の月の日数が date の日コンポーネントより少ないときは、
- 結果はその結果の月の最終日になります。それ以外の場合、結果は date と同じ日コンポーネントを持ちます。

月を加算した結果が無効な日付になる場合（例: January 31 → February 31）は、結果の月の有効な最終日を返します。

```sql
SELECT DATE_ADD(month, 1, '2023-01-31'::DATE) ;
╭────────────────────────────────────────╮
│ DATE_ADD(MONTH, 1, '2023-01-31'::DATE) │
│                  Date                  │
├────────────────────────────────────────┤
│ 2023-02-28                             │
╰────────────────────────────────────────╯

```

結果の月に十分な日数がある日付に月を加算する場合は、通常の月加算を行います。

```sql
SELECT DATE_ADD(month, 1, '2023-02-28'::DATE);
╭────────────────────────────────────────╮
│ DATE_ADD(MONTH, 1, '2023-02-28'::DATE) │
│                  Date                  │
├────────────────────────────────────────┤
│ 2023-03-28                             │
╰────────────────────────────────────────╯

```

## 関連項目 {#see-also}

- [ADD_MONTH](/tidb-cloud-lake/sql/add-months.md): 月を加算する関数
- [DATE_SUB](/tidb-cloud-lake/sql/date-sub.md): 時間間隔を減算する関数