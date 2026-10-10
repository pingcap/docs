---
title: LEAD
summary: 結果セット内の後続の行から値を返します。
---

# LEAD

結果セット内の後続の行から値を返します。

関連情報: [LAG](/tidb-cloud-lake/sql/lag.md)

## 構文 {#syntax}

```sql
LEAD(
    expression
    [, offset ]
    [, default ]
)
OVER (
    [ PARTITION BY partition_expression ]
    ORDER BY sort_expression
)
```

**引数:**

- `expression`: 評価するカラムまたは式
- `offset`: 現在の行の後ろにある行数（デフォルト: 1）
- `default`: 次の行が存在しない場合に返す値（デフォルト: NULL）

**注意:**

- 負の offset 値は LAG 関数と同様に動作します
- offset がパーティション境界を超える場合は NULL を返します

## 例 {#examples}

```sql
-- Create sample data
CREATE TABLE scores (
    student VARCHAR(20),
    test_date DATE,
    score INT
);

INSERT INTO scores VALUES
    ('Alice', '2024-01-01', 85),
    ('Alice', '2024-02-01', 90),
    ('Alice', '2024-03-01', 88),
    ('Bob', '2024-01-01', 78),
    ('Bob', '2024-02-01', 82),
    ('Bob', '2024-03-01', 85);
```

**各学生について次回のテストのスコアを取得します:**

```sql
SELECT student, test_date, score,
       LEAD(score) OVER (PARTITION BY student ORDER BY test_date) AS next_score
FROM scores
ORDER BY student, test_date;
```

結果:

```
student | test_date  | score | next_score
--------+------------+-------+-----------
Alice   | 2024-01-01 |    85 | 90
Alice   | 2024-02-01 |    90 | 88
Alice   | 2024-03-01 |    88 | NULL
Bob     | 2024-01-01 |    78 | 82
Bob     | 2024-02-01 |    82 | 85
Bob     | 2024-03-01 |    85 | NULL
```

**2 回後のテストのスコアを取得します:**

```sql
SELECT student, test_date, score,
       LEAD(score, 2, 0) OVER (PARTITION BY student ORDER BY test_date) AS score_2_tests_later
FROM scores
ORDER BY student, test_date;
```

結果:

```
student | test_date  | score | score_2_tests_later
--------+------------+-------+--------------------
Alice   | 2024-01-01 |    85 | 88
Alice   | 2024-02-01 |    90 | 0
Alice   | 2024-03-01 |    88 | 0
Bob     | 2024-01-01 |    78 | 85
Bob     | 2024-02-01 |    82 | 0
Bob     | 2024-03-01 |    85 | 0
```