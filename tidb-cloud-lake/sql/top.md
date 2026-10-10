---
title: TOP
summary: クエリが返す行数の最大数を制限します。
---

# TOP

クエリが返す行数の最大数を制限します。

関連情報: [Limit Clause](/tidb-cloud-lake/sql/select.md#limit-clause)

## 構文 {#syntax}

```sql
SELECT
    [ TOP <n> ] <column1>, <column2>, ...
FROM ...
[ ORDER BY ... ]
```

| パラメータ | 説明 |
|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| n         | 結果として返される行数の最大上限を表し、非負整数である必要があります。 |

- `TOP` と `LIMIT` は、クエリが返す行数を制限するための同等のキーワードですが、同じクエリ内で同時に使用することはできません。
- `ORDER BY` 句なしで `TOP` を使用すると、先頭行を選択するための意味のある順序がクエリに存在しないため、一貫しない結果や予期しない結果になる可能性があります。

## 例 {#examples}

次の例では、スコアの降順に基づいて上位 3 人の学生を返します。

```sql
CREATE TABLE Students (
    ID INT,
    Name VARCHAR(50),
    Score INT
);

INSERT INTO Students (ID, Name, Score) VALUES
(1, 'John', 85),
(2, 'Emily', 92),
(3, 'Michael', 78),
(4, 'Sophia', 95),
(5, 'William', 88),
(6, 'Emma', 90),
(7, 'James', 82),
(8, 'Olivia', 96),
(9, 'Alexander', 75),
(10, 'Ava', 96);

SELECT TOP 3 * FROM Students ORDER BY Score DESC;

┌──────────────────────────────────────────────────────┐
│        id       │       name       │      score      │
├─────────────────┼──────────────────┼─────────────────┤
│               8 │ Olivia           │              96 │
│              10 │ Ava              │              96 │
│               4 │ Sophia           │              95 │
└──────────────────────────────────────────────────────┘
```

上記のクエリは、次のクエリと同等です。

```sql
SELECT * FROM Students ORDER BY Score DESC LIMIT 3;

┌──────────────────────────────────────────────────────┐
│        id       │       name       │      score      │
├─────────────────┼──────────────────┼─────────────────┤
│               8 │ Olivia           │              96 │
│              10 │ Ava              │              96 │
│               4 │ Sophia           │              95 │
└──────────────────────────────────────────────────────┘
```

次の例では、上位 3 人の学生の名前とスコアのみを返します。

```sql
SELECT TOP 3 name, score FROM Students ORDER BY Score DESC;

┌────────────────────────────────────┐
│       name       │      score      │
├──────────────────┼─────────────────┤
│ Olivia           │              96 │
│ Ava              │              96 │
│ Sophia           │              95 │
└────────────────────────────────────┘
```

同じクエリ内で `TOP` と `LIMIT` の両方を使用すると、エラーになります。

```sql
SELECT TOP 3 name, score FROM Students ORDER BY Score DESC LIMIT 3;
error: APIError: ResponseError with 1065: Duplicate LIMIT: TopN and Limit cannot be used together
```