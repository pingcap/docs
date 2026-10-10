---
title: サブクエリ演算子
summary: サブクエリは、別のクエリの中にネストされたクエリです。{{{ .lake }}} は、以下のサブクエリタイプをサポートしています。
---

# サブクエリ演算子

サブクエリは、別のクエリの中にネストされたクエリです。{{{ .lake }}} は、以下のサブクエリタイプをサポートしています。

- [スカラーサブクエリ](#scalar-subquery)
- [EXISTS / NOT EXISTS](#exists--not-exists)
- [IN / NOT IN](#in--not-in)
- [ANY (SOME)](#any-some)
- [ALL](#all)

## スカラーサブクエリ {#scalar-subquery}

スカラーサブクエリは、1 つのカラムまたは式だけを選択し、最大でも 1 行だけを返します。SQL クエリでは、カラムまたは式が期待されるあらゆる場所でスカラーサブクエリを使用できます。

- スカラーサブクエリが 0 行を返した場合、{{{ .lake }}} はサブクエリの出力として NULL を使用します。
- スカラーサブクエリが複数行を返した場合、{{{ .lake }}} はエラーを返します。

### 例 {#examples}

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

EXISTS サブクエリは、WHERE 句に記述できるブール式です。

* EXISTS 式は、サブクエリによって 1 行でも生成される場合に TRUE と評価されます。
* NOT EXISTS 式は、サブクエリによって 1 行も生成されない場合に TRUE と評価されます。

### 構文 {#syntax}

```sql
[ NOT ] EXISTS ( <query> )
```

> **Note:**
>
> * 相関 EXISTS サブクエリは、現在のところ WHERE 句でのみサポートされています。

### 例 {#examples}

```sql
SELECT number FROM numbers(10) WHERE number>5 AND exists(SELECT number FROM numbers(5) WHERE number>4);
```

`SELECT number FROM numbers(5) WHERE number>4` では行が生成されないため、`exists(SELECT number FROM numbers(5) WHERE number>4)` は FALSE です。

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

`EXISTS(SELECT NUMBER FROM NUMBERS(5) WHERE NUMBER>3)` は TRUE です。

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

`not exists(SELECT number FROM numbers(5) WHERE number>4)` は TRUE です。

## IN / NOT IN {#in-not-in}

IN または NOT IN を使用すると、式がサブクエリによって返されるリスト内のいずれかの値に一致するかどうかを確認できます。

- IN または NOT IN を使用する場合、サブクエリは値の単一カラムを返す必要があります。

### 構文 {#syntax}

```sql
[ NOT ] IN ( <query> )
```

### 例 {#examples}

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

ANY（または SOME）を使用すると、比較がサブクエリによって返される値のいずれかに対して真になるかどうかを確認できます。

- キーワード ANY（または SOME）は、[比較演算子](/tidb-cloud-lake/sql/comparison-operators.md) のいずれかの後に続く必要があります。
- サブクエリが値を返さない場合、比較結果は false になります。
- SOME は ANY と同じように動作します。

### 構文 {#syntax}

```sql
-- ANY
comparison_operator ANY ( <query> )

-- SOME
comparison_operator SOME ( <query> )
```

### 例 {#examples}

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

ALL を使用すると、サブクエリが返すすべての値に対して比較が真であるかどうかを確認できます。

- キーワード ALL は、[比較演算子](/tidb-cloud-lake/sql/comparison-operators.md) のいずれかの後に置く必要があります。
- サブクエリが値を返さない場合、この比較は true と評価されます。

### 構文 {#syntax}

```sql
comparison_operator ALL ( <query> )
```

### 例 {#examples}

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