---
title: PERCENT_RANK
summary: 各行の相対順位をパーセンテージとして計算します。0 から 1 までの値を返し、0 は最も低い順位、1 は最も高い順位を表します。
---

# PERCENT_RANK

各行の相対順位をパーセンテージとして計算します。0 から 1 までの値を返し、0 は最も低い順位、1 は最も高い順位を表します。

関連情報: [CUME_DIST](/tidb-cloud-lake/sql/cume-dist.md)

## 構文 {#syntax}

```sql
PERCENT_RANK()
OVER (
    [ PARTITION BY partition_expression ]
    ORDER BY sort_expression [ ASC | DESC ]
)
```

**引数:**

- `PARTITION BY`: 任意。行をパーティションに分割します
- `ORDER BY`: 必須。順位付けの順序を決定します
- `ASC | DESC`: 任意。ソート方向（デフォルト: ASC）

**注意:**

- 0 から 1 までの値（両端を含む）を返します
- 最初の行の PERCENT_RANK は常に 0 です
- 最後の行の PERCENT_RANK は常に 1 です
- 式: (rank - 1) / (total_rows - 1)
- パーセンタイル値を取得するには 100 を掛けます

## 例 {#examples}

```sql
-- Create sample data
CREATE TABLE scores (
    student VARCHAR(20),
    score INT
);

INSERT INTO scores VALUES
    ('Alice', 95),
    ('Bob', 87),
    ('Charlie', 87),
    ('David', 82),
    ('Eve', 78);
```

**パーセント順位を計算する（パーセンタイル位置を表示）:**

```sql
SELECT student, score,
       PERCENT_RANK() OVER (ORDER BY score DESC) AS percent_rank,
       ROUND(PERCENT_RANK() OVER (ORDER BY score DESC) * 100) AS percentile
FROM scores
ORDER BY score DESC, student;
```

結果:

```
student | score | percent_rank | percentile
--------+-------+--------------+-----------
Alice   |    95 |          0.0 |          0
Bob     |    87 |         0.25 |         25
Charlie |    87 |         0.25 |         25
David   |    82 |         0.75 |         75
Eve     |    78 |          1.0 |        100
```