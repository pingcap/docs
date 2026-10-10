---
title: ROW_NUMBER
summary: 各パーティション内の各行に、1 から始まる連番を割り当てます。
---

# ROW_NUMBER

各パーティション内の各行に、1 から始まる連番を割り当てます。

## 構文 {#syntax}

```sql
ROW_NUMBER()
OVER (
    [ PARTITION BY partition_expression ]
    ORDER BY sort_expression [ ASC | DESC ]
)
```

**引数:**

- `PARTITION BY`: 任意。行をパーティションに分割します
- `ORDER BY`: 必須。行番号の付与順序を決定します
- `ASC | DESC`: 任意。ソート方向です（デフォルト: ASC）

**Notes:**

- 1 から始まる連続した整数を返します
- 各パーティションでは番号付けが 1 から再開されます
- ランキングやページネーションでよく使用されます

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
    ('Bob', 'Math', 78),
    ('Bob', 'English', 85),
    ('Bob', 'Science', 80),
    ('Charlie', 'Math', 88),
    ('Charlie', 'English', 90),
    ('Charlie', 'Science', 85);
```

**すべての行に連番を付与する（スコアが同じ場合でも）:**

```sql
SELECT student, subject, score,
       ROW_NUMBER() OVER (ORDER BY score DESC, student, subject) AS row_num
FROM scores
ORDER BY score DESC, student, subject;
```

結果:

```
student | subject | score | row_num
--------+---------+-------+--------
Alice   | Math    |    95 | 1
Alice   | Science |    92 | 2
Charlie | English |    90 | 3
Charlie | Math    |    88 | 4
Alice   | English |    87 | 5
Bob     | English |    85 | 6
Charlie | Science |    85 | 7
Bob     | Science |    80 | 8
Bob     | Math    |    78 | 9
```

**各 student ごとに行へ番号を付与する（ページネーション/上位 N 件向け）:**

```sql
SELECT student, subject, score,
       ROW_NUMBER() OVER (PARTITION BY student ORDER BY score DESC) AS subject_rank
FROM scores
ORDER BY student, score DESC;
```

結果:

```
student | subject | score | subject_rank
--------+---------+-------+-------------
Alice   | Math    |    95 | 1
Alice   | Science |    92 | 2
Alice   | English |    87 | 3
Bob     | English |    85 | 1
Bob     | Science |    80 | 2
Bob     | Math    |    78 | 3
Charlie | English |    90 | 1
Charlie | Math    |    88 | 2
Charlie | Science |    85 | 3
```