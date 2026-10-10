---
title: CUME_DIST
summary: 各行の値の累積分布を計算します。現在の行の値以下の値を持つ行の割合を返します。
---

# CUME_DIST

> **Note:**
>
> v1.2.7 で導入されました。

各行の値の累積分布を計算します。現在の行の値以下の値を持つ行の割合を返します。

関連情報: [PERCENT_RANK](/tidb-cloud-lake/sql/percent-rank.md)

## 構文 {#syntax}

```sql
CUME_DIST()
OVER (
    [ PARTITION BY partition_expression ]
    ORDER BY sort_expression [ ASC | DESC ]
)
```

**引数:**

- `PARTITION BY`: 任意。行をパーティションに分割します
- `ORDER BY`: 必須。分布の順序を決定します
- `ASC | DESC`: 任意。ソート方向（デフォルト: ASC）

**注意事項:**

- 0 から 1 までの値を返します（0 は含まず、1 は含みます）
- 公式: （現在の値以下の行数）/（総行数）
- 最大値に対しては常に 1.0 を返します
- パーセンタイルや累積百分率の計算に役立ちます

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

**累積分布を計算します（各スコア以下を取った学生の割合を表示）:**

```sql
SELECT student, score,
       CUME_DIST() OVER (ORDER BY score) AS cume_dist,
       ROUND(CUME_DIST() OVER (ORDER BY score) * 100) AS cumulative_percent
FROM scores
ORDER BY score;
```

結果:

```
student | score | cume_dist | cumulative_percent
--------+-------+-----------+-------------------
Eve     |    78 |       0.2 |                20
David   |    82 |       0.4 |                40
Bob     |    87 |       0.8 |                80
Charlie |    87 |       0.8 |                80
Alice   |    95 |       1.0 |               100
```