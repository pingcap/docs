---
title: 集合演算子
summary: 集合演算子は、2 つのクエリの結果を 1 つの結果に結合します。{{{ .lake }}} は次の集合演算子をサポートしています。
---

# 集合演算子

集合演算子は、2 つのクエリの結果を 1 つの結果に結合します。{{{ .lake }}} は次の集合演算子をサポートしています。

- [INTERSECT](#intersect)
- [EXCEPT](#except)
- [UNION [ALL]](#union-all)

## INTERSECT {#intersect}

両方のクエリで選択された、重複のないすべての行を返します。

### 構文 {#syntax}

```sql
SELECT column1 , column2 ....
FROM table_names
WHERE condition

INTERSECT

SELECT column1 , column2 ....
FROM table_names
WHERE condition
```

### 例 {#example}

```sql
create table t1(a int, b int);
create table t2(c int, d int);

insert into t1 values(1, 2), (2, 3), (3 ,4), (2, 3);
insert into t2 values(2,2), (3, 5), (7 ,8), (2, 3), (3, 4);

select * from t1 intersect select * from t2;
```

Output:

```sql
2|3
3|4
```

## EXCEPT {#except}

最初のクエリで選択され、2 番目のクエリでは選択されない、重複のないすべての行を返します。

### 構文 {#syntax}

```sql
SELECT column1 , column2 ....
FROM table_names
WHERE condition

EXCEPT

SELECT column1 , column2 ....
FROM table_names
WHERE condition
```

### 例 {#example}

```sql
create table t1(a int, b int);
create table t2(c int, d int);

insert into t1 values(1, 2), (2, 3), (3 ,4), (2, 3);
insert into t2 values(2,2), (3, 5), (7 ,8), (2, 3), (3, 4);

select * from t1 except select * from t2;
```

Output:

```sql
1|2
```

## UNION [ALL] {#union-all}

2 つ以上の結果セットの行を結合します。各結果セットは同じ数のカラムを返す必要があり、対応するカラムは同じデータ型、または互換性のあるデータ型である必要があります。

結果セットを結合する際、デフォルトでは重複行が削除されます。重複行を含めるには、**UNION ALL** を使用します。

### 構文 {#syntax}

```sql
SELECT column1 , column2 ...
FROM table_names
WHERE condition

UNION [ALL]

SELECT column1 , column2 ...
FROM table_names
WHERE condition

[UNION [ALL]

SELECT column1 , column2 ...
FROM table_names
WHERE condition]...

[ORDER BY ...]
```

### 例 {#example}

```sql
CREATE TABLE support_team
  (
     NAME   STRING,
     salary UINT32
  );

CREATE TABLE hr_team
  (
     NAME   STRING,
     salary UINT32
  );

INSERT INTO support_team
VALUES      ('Alice',
             1000),
            ('Bob',
             3000),
            ('Carol',
             5000);

INSERT INTO hr_team
VALUES      ('Davis',
             1000),
            ('Eva',
             4000);

-- The following code returns the employees in both teams who are paid less than 2,000 dollars:

SELECT NAME AS SelectedEmployee,
       salary
FROM   support_team
WHERE  salary < 2000
UNION
SELECT NAME AS SelectedEmployee,
       salary
FROM   hr_team
WHERE  salary < 2000
ORDER  BY selectedemployee DESC;
```

Output:

```sql
Davis|1000
Alice|1000
```