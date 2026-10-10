---
title: AVG_IF
summary: 任意の集約関数の名前に接尾辞 -If を付けることができます。この場合、集約関数は追加の引数、つまり条件を受け取ります。
---

# AVG_IF

## AVG_IF {#avg-if}

任意の集約関数の名前に接尾辞 -If を付けることができます。この場合、集約関数は追加の引数、つまり条件を受け取ります。

```sql
AVG_IF(<column>, <cond>)
```

## 例 {#example}

**テーブルを作成し、サンプルデータを挿入する**

```sql
CREATE TABLE employees (
  id INT,
  salary INT,
  department VARCHAR
);

INSERT INTO employees (id, salary, department)
VALUES (1, 50000, 'HR'),
       (2, 60000, 'IT'),
       (3, 55000, 'HR'),
       (4, 70000, 'IT'),
       (5, 65000, 'IT');
```

**クエリのデモ: IT 部門の平均給与を計算する**

```sql
SELECT AVG_IF(salary, department = 'IT') AS avg_salary_it
FROM employees;
```

**結果**

```sql
| avg_salary_it   |
|-----------------|
|     65000.0     |
```