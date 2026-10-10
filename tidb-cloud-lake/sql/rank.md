---
title: RANK
summary: パーティション内の各行に順位を割り当てます。同じ値を持つ行には同じ順位が付与され、その後の順位には欠番が生じます。
---

# RANK

パーティション内の各行に順位を割り当てます。同じ値を持つ行には同じ順位が付与され、その後の順位には欠番が生じます。

## 構文 {#syntax}

```sql
RANK()
OVER (
    [ PARTITION BY partition_expression ]
    ORDER BY sort_expression [ ASC | DESC ]
)
```

**引数:**

- `PARTITION BY`: 任意。行をパーティションに分割します
- `ORDER BY`: 必須。順位付けの順序を決定します
- `ASC | DESC`: 任意。ソート方向（デフォルト: ASC）

**Notes:**

- 順位は 1 から始まります
- 同じ値には同じ順位が付与されます
- 同順位の後の順位には欠番が生じます
- 例: 1, 2, 2, 4, 5（1, 2, 2, 3, 4 ではありません）

## 例 {#examples}

```sql
-- Create sample data
CREATE TABLE scores (
    student VARCHAR(20),
    subject VARCHAR(20),
    score INT
);

INSERT INTO scores VALUES
    ('Alice', 'Math', 95),
    ('Alice', 'English', 87),
    ('Alice', 'Science', 92),
    ('Bob', 'Math', 85),
    ('Bob', 'English', 85),
    ('Bob', 'Science', 80),
    ('Charlie', 'Math', 88),
    ('Charlie', 'English', 85),
    ('Charlie', 'Science', 85);
```

**すべてのスコアを順位付けする（同順位による欠番の処理を表示）:**

```sql
SELECT student, subject, score,
       RANK() OVER (ORDER BY score DESC) AS score_rank
FROM scores
ORDER BY score DESC, student, subject;
```

結果:

```
student | subject | score | score_rank
--------+---------+-------+-----------
Alice   | Math    |    95 | 1
Alice   | Science |    92 | 2
Charlie | Math    |    88 | 3
Alice   | English |    87 | 4
Bob     | English |    85 | 5
Bob     | Math    |    85 | 5
Charlie | English |    85 | 5
Charlie | Science |    85 | 5
Bob     | Science |    80 | 9
```

**各 student 内でスコアを順位付けする（パーティション内の同順位を表示）:**

```sql
SELECT student, subject, score,
       RANK() OVER (PARTITION BY student ORDER BY score DESC) AS subject_rank
FROM scores
ORDER BY student, score DESC, subject;
```

結果:

```
student | subject | score | subject_rank
--------+---------+-------+-------------
Alice   | Math    |    95 | 1
Alice   | Science |    92 | 2
Alice   | English |    87 | 3
Bob     | English |    85 | 1
Bob     | Math    |    85 | 1
Bob     | Science |    80 | 3
Charlie | Math    |    88 | 1
Charlie | English |    85 | 2
Charlie | Science |    85 | 2
```