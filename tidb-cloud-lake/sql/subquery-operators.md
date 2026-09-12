---
title: 子查询运算符
summary: 子查询是嵌套在另一个查询中的查询。{{{ .lake }}} 支持以下子查询类型。
---

# 子查询运算符

子查询是嵌套在另一个查询中的查询。{{{ .lake }}} 支持以下子查询类型：

- [标量子查询](#scalar-subquery)
- [EXISTS / NOT EXISTS](#exists--not-exists)
- [IN / NOT IN](#in--not-in)
- [ANY (SOME)](#any-some)
- [ALL](#all)

## 标量子查询 {#scalar-subquery}

标量子查询只选择一列或一个表达式，并且最多只返回一行。SQL 查询可以在任何需要列或表达式的位置使用标量子查询。

- 如果标量子查询返回 0 行，{{{ .lake }}} 会使用 NULL 作为子查询输出。
- 如果标量子查询返回多于一行，{{{ .lake }}} 会抛出错误。

### 示例 {#examples}

```sql
CREATE TABLE t1 (a int);
CREATE TABLE t2 (a int);

INSERT INTO t1 VALUES (1);
INSERT INTO t1 VALUES (2);
INSERT INTO t1 VALUES (3);

INSERT INTO t2 VALUES (3);
INSERT INTO t2 VALUES (4);
INSERT INTO t2 VALUES (5);

SELECT *
FROM   t1
WHERE  t1.a < (SELECT Min(t2.a)
               FROM   t2);

--
+--------+
|      a |
+--------+
|      1 |
|      2 |
+--------+
```

## EXISTS / NOT EXISTS {#exists-not-exists}

EXISTS 子查询是一个可以出现在 WHERE 子句中的布尔表达式：

* 如果子查询产生了任意行，EXISTS 表达式的计算结果为 TRUE。
* 如果子查询没有产生任何行，NOT EXISTS 表达式的计算结果为 TRUE。

### 语法 {#syntax}

```sql
[ NOT ] EXISTS ( <query> )
```

> **注意：**
>
> * 目前，相关 EXISTS 子查询仅支持在 WHERE 子句中使用。

### 示例 {#examples}

```sql
SELECT number FROM numbers(10) WHERE number>5 AND exists(SELECT number FROM numbers(5) WHERE number>4);
```

`SELECT number FROM numbers(5) WHERE number>4` 不会产生任何行，因此 `exists(SELECT number FROM numbers(5) WHERE number>4)` 为 FALSE。

```sql
SELECT number FROM numbers(10) WHERE number>5 and exists(SELECT number FROM numbers(5) WHERE number>3);
+--------+
| number |
+--------+
|      6 |
|      7 |
|      8 |
|      9 |
+--------+
```

`EXISTS(SELECT NUMBER FROM NUMBERS(5) WHERE NUMBER>3)` 为 TRUE。

```sql
SELECT number FROM numbers(10) WHERE number>5 AND not exists(SELECT number FROM numbers(5) WHERE number>4);
+--------+
| number |
+--------+
|      6 |
|      7 |
|      8 |
|      9 |
+--------+
```

`not exists(SELECT number FROM numbers(5) WHERE number>4)` 为 TRUE。

## IN / NOT IN {#in-not-in}

使用 IN 或 NOT IN，可以检查某个表达式是否与子查询返回的值列表中的任意值匹配。

- 使用 IN 或 NOT IN 时，子查询必须返回单列值。

### 语法 {#syntax}

```sql
[ NOT ] IN ( <query> )
```

### 示例 {#examples}

```sql
CREATE TABLE t1 (a int);
CREATE TABLE t2 (a int);

INSERT INTO t1 VALUES (1);
INSERT INTO t1 VALUES (2);
INSERT INTO t1 VALUES (3);

INSERT INTO t2 VALUES (3);
INSERT INTO t2 VALUES (4);
INSERT INTO t2 VALUES (5);

-- IN example
SELECT *
FROM   t1
WHERE  t1.a IN (SELECT *
               FROM   t2);

--
+--------+
|      a |
+--------+
|      3 |
+--------+

-- NOT IN example
SELECT *
FROM   t1
WHERE  t1.a NOT IN (SELECT *
               FROM   t2);

--
+--------+
|      a |
+--------+
|      1 |
|      2 |
+--------+
```

## ANY (SOME) {#any-some}

可以使用 ANY（或 SOME）来检查某个比较对于子查询返回的任意一个值是否为真。

- 关键字 ANY（或 SOME）必须跟在某个[比较运算符](/tidb-cloud-lake/sql/comparison-operators.md)之后。
- 如果子查询未返回任何值，则该比较的计算结果为 false。
- SOME 的工作方式与 ANY 相同。

### 语法 {#syntax}

```sql
-- ANY
comparison_operator ANY ( <query> )

-- SOME
comparison_operator SOME ( <query> )
```

### 示例 {#examples}

```sql
CREATE TABLE t1 (a int);
CREATE TABLE t2 (a int);

INSERT INTO t1 VALUES (1);
INSERT INTO t1 VALUES (2);
INSERT INTO t1 VALUES (3);

INSERT INTO t2 VALUES (3);
INSERT INTO t2 VALUES (4);
INSERT INTO t2 VALUES (5);

SELECT *
FROM   t1
WHERE  t1.a < ANY (SELECT *
                   FROM   t2);

--
+--------+
|      a |
+--------+
|      1 |
|      2 |
|      3 |
+--------+
```

## ALL {#all}

你可以使用 ALL 来检查某个比较对于子查询返回的所有值是否都为 true。

- 关键字 ALL 必须跟在某个[比较运算符](/tidb-cloud-lake/sql/comparison-operators.md)之后。
- 如果子查询未返回任何值，则该比较的计算结果为 true。

### 语法 {#syntax}

```sql
comparison_operator ALL ( <query> )
```

### 示例 {#examples}

```sql
CREATE TABLE t1 (a int);
CREATE TABLE t2 (a int);

INSERT INTO t1 VALUES (1);
INSERT INTO t1 VALUES (2);
INSERT INTO t1 VALUES (3);

INSERT INTO t2 VALUES (3);
INSERT INTO t2 VALUES (4);
INSERT INTO t2 VALUES (5);

SELECT *
FROM   t1
WHERE  t1.a < ALL (SELECT *
                   FROM   t2);

--
+--------+
|      a |
+--------+
|      1 |
|      2 |
+--------+
```