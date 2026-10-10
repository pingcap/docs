---
title: TIME_SLICE
summary: TIME_SLICE は、単一の日付/タイムスタンプ値を固定のカレンダー間隔（スライスまたはバケット）にマッピングするために使用されるスカラー関数です。
---

# TIME_SLICE

TIME_SLICE は、単一の日付/タイムスタンプ値を固定のカレンダー間隔（スライスまたはバケット）にマッピングするために使用されるスカラー関数です。

この関数は、指定した時点を含むカレンダー間隔の境界（開始点または終了点）を返します。2 週間、3 か月、15 分といったカスタムのカレンダー期間ごとに時系列データをグループ化、集計、レポートする際によく使用されます。

## 構文 {#syntax}

```sql
TIME_SLICE(<date_or_time_expr>, <slice_length>, <IntervalKind> [, <start_or_end>])
```

| パラメータ             | 説明                                                                                                 |
|-----------------------|-------------------------------------------------------------------------------------------------------------|
| `<date_or_time_expr>` | DATE、TIME、TIMESTAMP、またはその他の日付/時刻式です。可能な場合、戻り値の型は入力型に一致します。 |
| `<slice_length>`      | INTEGER >= 1。1 つのスライスに含まれる連続した IntervalKind 単位の数です（例: 2 週間スライスの場合は 2）。           |
| `<IntervalKind>`      | 次のいずれかです（大文字と小文字は区別されません）: YEAR, QUARTER, MONTH, WEEK, DAY, HOUR, MINUTE, SECOND。             |
| `<start_or_end>`      | 文字列 'START' または 'END'（大文字と小文字は区別されません）です。省略した場合のデフォルトは 'START' です。                                |

## セマンティクス {#semantics}

- 指定された呼び出し TIME_SLICE(value, slice_length, IntervalKind, start_or_end) について:
    - START は、そのスライスの開始境界（包含）となる正確なカレンダー境界を返します。
    - END は、そのスライスの直後の境界（排他的な上限）を返します。入力型とシステム精度によっては、最小の時間単位を減算して包含的な終端に変換することで、END をそのスライスで表現可能な最後の時点として解釈することもできます。

- サポートされる IntervalKind と入力型の対応:
    - DATE 入力: YEAR, QUARTER, MONTH, WEEK, DAY。
    - TIMESTAMP / TIMESTAMPTZ 入力: YEAR, QUARTER, MONTH, WEEK, DAY, HOUR, MINUTE, SECOND（すべての IntervalKind 値）。

- アラインメントルール（カレンダー境界）:
    - 年は 1 月 1 日に始まります。
    - 四半期は四半期の境界（1 月 1 日、4 月 1 日、7 月 1 日、10 月 1 日）に始まります。
    - 月はその月の 1 日に始まります。
    - 週は実装の週規則に従って揃えられます（デフォルトでは月曜日が週の開始です）。
    - 日は 00:00:00 に始まります。
    - Hour/Minute/Second のスライスは、それぞれの単位の自然な境界から始まります。

## 戻り値の型 {#return-type}

- DATE 入力 → DATE を返します。
- TIMESTAMP 入力 → TIMESTAMP を返します。

## 例 {#examples}

```sql
SELECT
    '2019-02-28'::DATE AS "DATE",
        TIME_SLICE("DATE", 4, 'MONTH', 'START') AS "start",
    TIME_SLICE("DATE", 4, 'MONTH', 'END') AS "end";

╭──────────────────────────────────────╮
│    DATE    │    start   │     end    │
├────────────┼────────────┼────────────┤
│ 2019-02-28 │ 2019-01-01 │ 2019-05-01 │
╰──────────────────────────────────────╯

```

```sql
CREATE OR REPLACE TABLE accounts (
  id INT,
  billing_date DATE,
  balance_due DECIMAL(11, 2)
)

INSERT INTO
  accounts (id, billing_date, balance_due)
VALUES
  (1, '2018-07-31', 100.00),
  (2, '2018-08-01', 200.00),
  (3, '2018-08-25', 400.00);

-- Group by 2-week slices:
SELECT
    TIME_SLICE(billing_date, 2, 'WEEK', 'START') AS slice_start,
    TIME_SLICE(billing_date, 2, 'WEEK', 'END') AS slice_end,
    COUNT(*) AS num_late_bills,
    SUM(balance_due) AS total_due
FROM
    accounts
WHERE
    balance_due > 0
GROUP BY 1, 2
ORDER BY
    total_due;

╭─────────────────────────────────────────────────────────────────────────────╮
│   slice_start  │    slice_end   │ num_late_bills │         total_due        │
├────────────────┼────────────────┼────────────────┼──────────────────────────┤
│ 2018-07-23     │ 2018-08-06     │              2 │                   300.00 │
│ 2018-08-20     │ 2018-09-03     │              1 │                   400.00 │
╰─────────────────────────────────────────────────────────────────────────────╯

```

## 関連情報 {#see-also}

- [DATE_TRUNC](/tidb-cloud-lake/sql/date-trunc.md): より高い SQL 標準互換性を実現するために、異なる構文で類似の機能を提供します。