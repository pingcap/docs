---
title: AGE
summary: age() 関数は、2 つのタイムスタンプ間の差、またはタイムスタンプと現在の日時との差を計算します。
---

# AGE

age() 関数は、2 つのタイムスタンプ間の差、またはタイムスタンプと現在の日時との差を計算します。

## 構文 {#syntax}

```sql
AGE(<end_timestamp>, <start_timestamp>)
```

| パラメータ | 説明 |
|----------------------|-----------------------------------------------------------------------------|
| `<end_timestamp>`   | 終了タイムスタンプ |
| `<start_timestamp>` | 開始タイムスタンプ |

## 戻り値の型 {#return-type}

INTERVAL 型を返します。

## 計算ロジック {#calculation-logic}

この関数は、次の内容を計算します。

1. 完全な年の差分（うるう年を考慮）
2. 残りの月の差分（月ごとの日数の違いを考慮）
3. 残りの日の差分（時刻コンポーネントを含む）

`<end_timestamp>` が `<start_timestamp>` より前の場合は、負の interval が返されます。

## 例 {#examples}

### 基本的な age の計算 {#basic-age-calculation}

```sql
SELECT AGE('2023-03-15'::TIMESTAMP, '2020-01-20'::TIMESTAMP);
├─────────────────────────┤
│ 3 years 1 month 26 days │
╰─────────────────────────╯
```

### 逆順の時系列 {#reverse-chronology}

```sql
SELECT AGE('2018-12-25'::TIMESTAMP, '2022-05-10'::TIMESTAMP);
├─────────────────────────────┤
│ -3 years -4 months -16 days │
╰─────────────────────────────╯
```

### 時刻コンポーネントを含む場合 {#with-time-components}

```sql
SELECT AGE('2023-02-28 14:00:00'::TIMESTAMP, '2023-02-27 08:30:00'::TIMESTAMP);
├───────────────┤
│ 1 day 5:30:00 │
╰───────────────╯
```

### テーブルデータの処理 {#table-data-processing}

```sql
CREATE TABLE projects (
    name String,
    start_date TIMESTAMP,
    end_date TIMESTAMP
);

INSERT INTO projects VALUES
    ('Alpha', '2020-06-01', '2023-09-30'),
    ('Beta', '2022-01-15', '2022-11-01');

SELECT
    name,
    AGE(end_date, start_date) AS duration
FROM projects;
╭─────────────────────────────────────────────╮
│       name       │         duration         │
│ Nullable(String) │    Nullable(Interval)    │
├──────────────────┼──────────────────────────┤
│ Alpha            │ 3 years 3 months 29 days │
│ Beta             │ 9 months 17 days         │
╰─────────────────────────────────────────────╯
```

## 関連項目 {#see-also}

- [DATE_DIFF](/tidb-cloud-lake/sql/date-diff.md): 特定の時間単位の差分を計算するための代替関数