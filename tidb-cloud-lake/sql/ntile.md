---
title: NTILE
summary: 行を指定した数のバケットに分割し、各行にバケット番号を割り当てます。行はできるだけ均等に各バケットへ分配されます。
---

# NTILE

> **Note:**
>
> v1.1.50 で導入されました。

行を指定した数のバケットに分割し、各行にバケット番号を割り当てます。行はできるだけ均等に各バケットへ分配されます。

## 構文 {#syntax}

```sql
NTILE(bucket_count)
OVER (
    [ PARTITION BY partition_expression ]
    ORDER BY sort_expression [ ASC | DESC ]
)
```

**引数:**

- `bucket_count`: 必須。作成するバケット数（正の整数である必要があります）
- `PARTITION BY`: 任意。行をパーティションに分割します
- `ORDER BY`: 必須。分配順序を決定します
- `ASC | DESC`: 任意。ソート方向（デフォルト: ASC）

**注意事項:**

- バケット番号の範囲は 1 から `bucket_count` です
- 行はできるだけ均等に分配されます
- 行数を均等に割り切れない場合、前のバケットに 1 行ずつ多く割り当てられます
- パーセンタイルや同じサイズのグループを作成するのに便利です

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

**すべてのスコアを 3 つのバケット（三分位）に分割する:**

```sql
SELECT student, subject, score,
       NTILE(3) OVER (ORDER BY score DESC) AS score_bucket
FROM scores
ORDER BY score DESC, student, subject;
```

結果:

```
student | subject | score | score_bucket
--------+---------+-------+-------------
Alice   | Math    |    95 | 1
Alice   | Science |    92 | 1
Charlie | Math    |    88 | 1
Alice   | English |    87 | 2
Bob     | English |    85 | 2
Bob     | Math    |    85 | 2
Charlie | English |    85 | 3
Charlie | Science |    85 | 3
Bob     | Science |    80 | 3
```

**各 student 内でスコアを四分位に分割する:**

```sql
SELECT student, subject, score,
       NTILE(2) OVER (PARTITION BY student ORDER BY score DESC) AS performance_half
FROM scores
ORDER BY student, score DESC, subject;
```

結果:

```
student | subject | score | performance_half
--------+---------+-------+-----------------
Alice   | Math    |    95 | 1
Alice   | Science |    92 | 1
Alice   | English |    87 | 2
Bob     | English |    85 | 1
Bob     | Math    |    85 | 1
Bob     | Science |    80 | 2
Charlie | Math    |    88 | 1
Charlie | English |    85 | 2
Charlie | Science |    85 | 2
```