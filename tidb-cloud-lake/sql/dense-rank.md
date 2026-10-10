---
title: DENSE_RANK
summary: パーティション内の各行に順位を割り当てます。同じ値を持つ行には同じ順位が付与され、その後の順位に欠番は発生しません。
---

# DENSE_RANK

パーティション内の各行に順位を割り当てます。同じ値を持つ行には同じ順位が付与され、その後の順位に欠番は発生しません。

## 構文 {#syntax}

```sql
DENSE_RANK()
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

- 順位は 1 から始まります
- 同じ値には同じ順位が付与されます
- 同順位があっても、その後の順位のシーケンスに欠番は発生しません
- 例: 1, 2, 2, 3, 4（RANK のように 1, 2, 2, 4, 5 にはなりません）

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

**すべてのスコアに対して dense rank を付与する（同順位の後に欠番がないことを示す）:**

```sql
SELECT student, subject, score,
       DENSE_RANK() OVER (ORDER BY score DESC) AS dense_rank
FROM scores
ORDER BY score DESC, student, subject;
```

結果:

```
student | subject | score | dense_rank
--------+---------+-------+-----------
Alice   | Math    |    95 | 1
Alice   | Science |    92 | 2
Charlie | Math    |    88 | 3
Alice   | English |    87 | 4
Bob     | English |    85 | 5
Bob     | Math    |    85 | 5
Charlie | English |    85 | 5
Charlie | Science |    85 | 5
Bob     | Science |    80 | 6
```

**各 student 内でスコアに対して dense rank を付与する:**

```sql
SELECT student, subject, score,
       DENSE_RANK() OVER (PARTITION BY student ORDER BY score DESC) AS subject_dense_rank
FROM scores
ORDER BY student, score DESC, subject;
```

結果:

```
student | subject | score | subject_dense_rank
--------+---------+-------+-------------------
Alice   | Math    |    95 | 1
Alice   | Science |    92 | 2
Alice   | English |    87 | 3
Bob     | English |    85 | 1
Bob     | Math    |    85 | 1
Bob     | Science |    80 | 2
Charlie | Math    |    88 | 1
Charlie | English |    85 | 2
Charlie | Science |    85 | 2
```