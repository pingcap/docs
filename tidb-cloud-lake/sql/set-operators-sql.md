---
title: 集合运算符
summary: 集合运算符将两个查询的结果组合为单个结果。{{{ .lake }}} 支持以下集合运算符。
---

# 集合运算符

集合运算符将两个查询的结果组合为单个结果。{{{ .lake }}} 支持以下集合运算符：

- [INTERSECT](#intersect)
- [EXCEPT](#except)
- [UNION [ALL]](#union-all)

## INTERSECT {#intersect}

返回两个查询都选中的所有去重行。

### 语法 {#syntax}

```sql
SELECT column1 , column2 ....
FROM table_names
WHERE condition

INTERSECT

SELECT column1 , column2 ....
FROM table_names
WHERE condition
```

### 示例 {#example}

```sql
create table t1(a int, b int);
create table t2(c int, d int);

insert into t1 values(1, 2), (2, 3), (3 ,4), (2, 3);
insert into t2 values(2,2), (3, 5), (7 ,8), (2, 3), (3, 4);

select * from t1 intersect select * from t2;
```

输出：

```sql
2|3
3|4
```

## EXCEPT {#except}

返回第一个查询选中但第二个查询未选中的所有去重行。

### 语法 {#syntax}

```sql
SELECT column1 , column2 ....
FROM table_names
WHERE condition

EXCEPT

SELECT column1 , column2 ....
FROM table_names
WHERE condition
```

### 示例 {#example}

```sql
create table t1(a int, b int);
create table t2(c int, d int);

insert into t1 values(1, 2), (2, 3), (3 ,4), (2, 3);
insert into t2 values(2,2), (3, 5), (7 ,8), (2, 3), (3, 4);

select * from t1 except select * from t2;
```

输出：

```sql
1|2
```

## UNION [ALL] {#union-all}

将两个或多个结果集中的行组合在一起。每个结果集必须返回相同数量的列，并且对应列必须具有相同或兼容的数据类型。

在组合结果集时，该命令默认会去除重复行。若要包含重复行，请使用 **UNION ALL**。

### 语法 {#syntax}

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

### 示例 {#example}

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

输出：

```sql
Davis|1000
Alice|1000
```