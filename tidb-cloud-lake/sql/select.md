---
title: SELECT
summary: テーブルからデータを取得します。
---

# SELECT

テーブルからデータを取得します。

## 構文 {#syntax}

```sql
[WITH]
SELECT
    [ALL | DISTINCT]
    [ TOP <n> ]
    <select_expr> | <col_name> [[AS] <alias>] | $<col_position> [, ...] | *
    COLUMNS <expr>
    [EXCLUDE (<col_name1> [, <col_name2>, <col_name3>, ...] ) ]
    [FROM table_references]
    [AT ...]
    [WHERE <expr>]
    [GROUP BY {{<col_name> | <expr> | <col_alias> | <col_position>},
         ... | <extended_grouping_expr>}]
    [HAVING <expr>]
    [ORDER BY {<col_name> | <expr> | <col_alias> | <col_position>} [ASC | DESC],
         [ NULLS { FIRST | LAST }]
    [LIMIT <row_count>]
    [OFFSET <row_count>]
    [IGNORE_RESULT]
```

- SELECT 文では、stage 上のファイルを直接クエリすることもできます。構文と例については、[{{{ .lake }}} による効率的なデータ変換](/tidb-cloud-lake/sql/stage.md) を参照してください。

- このページの例では、テスト用にテーブル `numbers(N)` を使用します。このテーブルには、0 から N-1 までの整数を含む 1 つの UInt64 カラム（名前は `number`）があります。

## SELECT 句 {#select-clause}

### AS キーワード {#as-keyword}

{{{ .lake }}} では、AS キーワードを使用してカラムにエイリアスを割り当てることができます。これにより、SQL 文とクエリ結果の両方で、そのカラムに対してより説明的で理解しやすい名前を付けることができます。

- {{{ .lake }}} では、カラムエイリアスを作成する際に、できるだけ特殊文字を避けることを推奨しています。ただし、場合によって特殊文字が必要なときは、次のようにエイリアスをバッククォートで囲む必要があります: SELECT price AS \`$CA\` FROM ...

- {{{ .lake }}} は、エイリアスを自動的に小文字に変換します。たとえば、カラムに *Total* というエイリアスを付けると、結果では *total* と表示されます。大文字・小文字を区別したい場合は、エイリアスをバッククォートで囲んでください: \`Total\`。

```sql
SELECT number AS Total FROM numbers(3);
+--------+
| total  |
+--------+
|      0 |
|      1 |
|      2 |
+--------+

SELECT number AS `Total` FROM numbers(3);
+--------+
| Total  |
+--------+
|      0 |
|      1 |
|      2 |
+--------+
```

SELECT 句でカラムにエイリアスを付けた場合、そのエイリアスは WHERE、GROUP BY、HAVING 句で参照でき、さらにエイリアスが定義された後であれば SELECT 句内でも参照できます。

```sql
SELECT number * 2 AS a, a * 2 AS double FROM numbers(3) WHERE (a + 1) % 3 = 0;
+---+--------+
| a | double |
+---+--------+
| 2 |      4 |
+---+--------+

SELECT MAX(number) AS b, number % 3 AS c FROM numbers(100) GROUP BY c HAVING b > 8;
+----+---+
| b  | c |
+----+---+
| 99 | 0 |
| 97 | 1 |
| 98 | 2 |
+----+---+
```

カラムにエイリアスを割り当て、そのエイリアス名が元のカラム名と同じ場合、WHERE 句と GROUP BY 句ではそのエイリアスはカラム名として認識されます。一方、HAVING 句ではそのエイリアスはエイリアスそのものとして認識されます。

```sql
SELECT number * 2 AS number FROM numbers(3)
WHERE (number + 1) % 3 = 0
GROUP BY number
HAVING number > 5;

+--------+
| number |
+--------+
|     10 |
|     16 |
+--------+
```

### EXCLUDE キーワード {#exclude-keyword}

結果から、名前を指定して 1 つ以上のカラムを除外します。このキーワードは通常、`SELECT * ...` と組み合わせて使用し、すべてのカラムを取得する代わりに、結果から一部のカラムだけを除外するために使います。

```sql
SELECT * FROM allemployees ORDER BY id;

---
| id | firstname | lastname | gender |
|----|-----------|----------|--------|
| 1  | Ryan      | Tory     | M      |
| 2  | Oliver    | Green    | M      |
| 3  | Noah      | Shuster  | M      |
| 4  | Lily      | McMeant   | F     |
| 5  | Macy      | Lee      | F      |

-- Exclude the column "id" from the result
SELECT * EXCLUDE id FROM allemployees;

---
| firstname | lastname | gender |
|-----------|----------|--------|
| Noah      | Shuster  | M      |
| Ryan      | Tory     | M      |
| Oliver    | Green    | M      |
| Lily      | McMeant   | F     |
| Macy      | Lee      | F      |

-- Exclude the columns "id" and "lastname" from the result
SELECT * EXCLUDE (id,lastname) FROM allemployees;

---
| firstname | gender |
|-----------|--------|
| Oliver    | M      |
| Ryan      | M      |
| Lily      | F      |
| Noah      | M      |
| Macy      | F      |
```

### COLUMNS Keyword {#columns-keyword}

`COLUMNS` キーワードは、リテラルの正規表現パターンおよびラムダ式に基づいてカラムを選択するための柔軟な仕組みを提供します。

```sql
CREATE TABLE employee (
    employee_id INT,
    employee_name VARCHAR(255),
    department VARCHAR(50),
    salary DECIMAL(10, 2)
);

INSERT INTO employee VALUES
(1, 'Alice', 'HR', 60000.00),
(2, 'Bob', 'IT', 75000.00),
(3, 'Charlie', 'Marketing', 50000.00),
(4, 'David', 'Finance', 80000.00);

-- Select columns with names starting with 'employee'
SELECT COLUMNS('employee.*') FROM employee;

┌────────────────────────────────────┐
│   employee_id   │   employee_name  │
├─────────────────┼──────────────────┤
│               1 │ Alice            │
│               2 │ Bob              │
│               3 │ Charlie          │
│               4 │ David            │
└────────────────────────────────────┘

-- Select columns where the name contains the substring 'name'
SELECT COLUMNS(x -> x LIKE '%name%') FROM employee;

┌──────────────────┐
│   employee_name  │
├──────────────────┤
│ Alice            │
│ Bob              │
│ Charlie          │
│ David            │
└──────────────────┘
```

`COLUMNS` キーワードは、`EXCLUDE` と組み合わせて使用することもでき、クエリ結果から特定のカラムを明示的に除外できます。

```sql
-- Select all columns excluding 'salary' from the 'employee' table
SELECT COLUMNS(* EXCLUDE salary) FROM employee;

┌───────────────────────────────────────────────────────┐
│   employee_id   │   employee_name  │    department    │
├─────────────────┼──────────────────┼──────────────────┤
│               1 │ Alice            │ HR               │
│               2 │ Bob              │ IT               │
│               3 │ Charlie          │ Marketing        │
│               4 │ David            │ Finance          │
└───────────────────────────────────────────────────────┘
```

### Column Position {#column-position}

`$N` を使用すると、`SELECT` 句内のカラムを表せます。たとえば、`$2` は 2 番目のカラムを表します。

```sql
CREATE TABLE IF NOT EXISTS t1(a int, b varchar);
INSERT INTO t1 VALUES (1, 'a'), (2, 'b');
SELECT a, $2 FROM t1;

+---+-------+
| a | $2    |
+---+-------+
| 1 | a     |
| 2 | b     |
+---+-------+
```

### Retrieving All Columns {#retrieving-all-columns}

`SELECT *` 文は、テーブルまたはクエリ結果からすべてのカラムを取得するために使用されます。個々のカラム名を指定せずに完全なデータセットを取得できる便利な方法です。

次の例では、`my_table` からすべてのカラムを返します。

```sql
SELECT * FROM my_table;
```

{{{ .lake }}} は SQL 構文を拡張し、`SELECT *` を明示的に使用しなくても、`FROM <table>` でクエリを開始できるようにしています。

```sql
FROM my_table;
```

これは次と同等です。

```sql
SELECT * FROM my_table;
```

## FROM Clause {#from-clause}

`SELECT` 文の `FROM` 句は、データをクエリする元となるテーブルを指定します。特に `SELECT` リストが長い場合や、選択したカラムの由来をすばやく把握したい場合には、`SELECT` 句の前に `FROM` 句を置くことで、コードの可読性を向上させることもできます。

```sql
-- The following two statements are equivalent:

-- Statement 1: Using SELECT clause with FROM clause
SELECT number FROM numbers(3);

-- Statement 2: Equivalent representation with FROM clause preceding SELECT clause
FROM numbers(3) SELECT number;

+--------+
| number |
+--------+
|      0 |
|      1 |
|      2 |
+--------+
```

`FROM` 句では場所を指定することもでき、さまざまなソースのデータをテーブルに最初にロード (load) することなく直接クエリできます。詳細は、[stage 上のファイルのクエリ](/tidb-cloud-lake/sql/stage.md) を参照してください。

## AT Clause {#at-clause}

`AT` 句を使用すると、データの過去のバージョンをクエリできます。詳細は、[AT](/tidb-cloud-lake/sql/at.md) を参照してください。

## WHERE Clause {#where-clause}

```sql
SELECT number FROM numbers(3) WHERE number > 1;
+--------+
| number |
+--------+
|      2 |
+--------+
```

## GROUP BY Clause {#group-by-clause}

```sql
--Group the rows of the result set by column alias
SELECT number%2 as c1, number%3 as c2, MAX(number) FROM numbers(10000) GROUP BY c1, c2;
+------+------+-------------+
| c1   | c2   | MAX(number) |
+------+------+-------------+
|    1 |    2 |        9995 |
|    1 |    1 |        9997 |
|    0 |    2 |        9998 |
|    0 |    1 |        9994 |
|    0 |    0 |        9996 |
|    1 |    0 |        9999 |
+------+------+-------------+

--Group the rows of the result set by column position in the SELECT list
SELECT number%2 as c1, number%3 as c2, MAX(number) FROM numbers(10000) GROUP BY 1, 2;
+------+------+-------------+
| c1   | c2   | MAX(number) |
+------+------+-------------+
|    1 |    2 |        9995 |
|    1 |    1 |        9997 |
|    0 |    2 |        9998 |
|    0 |    1 |        9994 |
|    0 |    0 |        9996 |
|    1 |    0 |        9999 |
+------+------+-------------+

```

## HAVING Clause {#having-clause}

```sql
SELECT
    number % 2 as c1,
    number % 3 as c2,
    MAX(number) as max
FROM
    numbers(10000)
GROUP BY
    c1, c2
HAVING
    max > 9996;

+------+------+------+
| c1   | c2   | max  |
+------+------+------+
|    1 |    0 | 9999 |
|    1 |    1 | 9997 |
|    0 |    2 | 9998 |
+------+------+------+
```

## ORDER BY 句 {#order-by-clause}

```sql
--カラム名で昇順にソートします。
SELECT number FROM numbers(5) ORDER BY number ASC;
+--------+
| number |
+--------+
|      0 |
|      1 |
|      2 |
|      3 |
|      4 |
+--------+

--カラム名で降順にソートします。
SELECT number FROM numbers(5) ORDER BY number DESC;
+--------+
| number |
+--------+
|      4 |
|      3 |
|      2 |
|      1 |
|      0 |
+--------+

--カラムのエイリアスでソートします。
SELECT number%2 AS c1, number%3 AS c2  FROM numbers(5) ORDER BY c1 ASC, c2 DESC;
+------+------+
| c1   | c2   |
+------+------+
|    0 |    2 |
|    0 |    1 |
|    0 |    0 |
|    1 |    1 |
|    1 |    0 |
+------+------+

--SELECT リスト内のカラム位置でソートします
SELECT * FROM t1 ORDER BY 2 DESC;
+------+------+
| a    | b    |
+------+------+
|    2 |    3 |
|    1 |    2 |
+------+------+

SELECT a FROM t1 ORDER BY 1 DESC;
+------+
| a    |
+------+
|    2 |
|    1 |
+------+

--NULLS FIRST または LAST オプションを使用してソートします。

CREATE TABLE t_null (
  number INTEGER
);

INSERT INTO t_null VALUES (1);
INSERT INTO t_null VALUES (2);
INSERT INTO t_null VALUES (3);
INSERT INTO t_null VALUES (NULL);
INSERT INTO t_null VALUES (NULL);

--{{{ .lake }}} では、NULL 値は NULL 以外のどの値よりも大きいものとして扱われます。
--結果を昇順でソートする次の例では、NULL 値は最後に表示されます。

SELECT number FROM t_null order by number ASC;
+--------+
| number |
+--------+
|      1 |
|      2 |
|      3 |
|   NULL |
|   NULL |
+--------+

-- 前の例で NULL 値を先頭に表示するには、NULLS FIRST オプションを使用します。

SELECT number FROM t_null order by number ASC nulls first;
+--------+
| number |
+--------+
|   NULL |
|   NULL |
|      1 |
|      2 |
|      3 |
+--------+

-- NULL 値を降順で最後に表示するには、NULLS LAST オプションを使用します。

SELECT number FROM t_null order by number DESC nulls last;
+--------+
| number |
+--------+
|      3 |
|      2 |
|      1 |
|   NULL |
|   NULL |
+--------+
```

## LIMIT 句 {#limit-clause}

```sql
SELECT number FROM numbers(1000000000) LIMIT 1;
+--------+
| number |
+--------+
|      0 |
+--------+

SELECT number FROM numbers(100000) ORDER BY number LIMIT 2 OFFSET 10;
+--------+
| number |
+--------+
|     10 |
|     11 |
+--------+
```

大きな結果セットに対するクエリ性能を最適化するために、{{{ .lake }}} では `lazy_read_threshold` オプションがデフォルトで有効になっており、デフォルト値は 1,000 です。このオプションは、LIMIT 句を含むクエリ向けに設計されています。`lazy_read_threshold` が有効な場合、指定した LIMIT の数値が設定したしきい値以下のクエリで最適化が有効になります。このオプションを無効にするには、`0` に設定します。

<details>
  <summary>仕組み</summary>
    <div>この最適化は、ORDER BY 句と LIMIT 句を含むクエリの性能を向上させます。有効化されていて、かつクエリ内の LIMIT の数値が指定したしきい値より小さいか等しい場合、結果セット全体ではなく、ORDER BY 句に含まれるカラムだけを取得してソートします。</div><br/><div>システムは、ORDER BY 句に含まれるカラムを取得してソートした後、LIMIT 制約を適用して、ソート済み結果セットから必要な行数を選択します。その後、その制限された行セットをクエリ結果として返します。この方法では、必要なカラムだけを取得してソートすることでリソース使用量を削減し、さらに処理対象の行を必要なサブセットに限定することでクエリ実行を最適化します。</div>
</details>

```sql
SELECT * FROM hits WHERE URL LIKE '%google%' ORDER BY EventTime LIMIT 10 ignore_result;
Empty set (0.300 sec)

set lazy_read_threshold=0;
Query OK, 0 rows affected (0.004 sec)

SELECT * FROM hits WHERE URL LIKE '%google%' ORDER BY EventTime LIMIT 10 ignore_result;
Empty set (0.897 sec)
```

## OFFSET 句 {#offset-clause}

```sql
SELECT number FROM numbers(5) ORDER BY number OFFSET 2;
+--------+
| number |
+--------+
|      2 |
|      3 |
|      4 |
+--------+
```

## IGNORE_RESULT {#ignore-result}

結果セットを出力しません。

```sql
SELECT number FROM numbers(2);
+--------+
| number |
+--------+
|      0 |
|      1 |
+--------+

SELECT number FROM numbers(2) IGNORE_RESULT;
-- Empty set
```

## ネストされたサブ SELECT {#nested-sub-selects}

SELECT 文はクエリ内でネストできます。

```
SELECT ... [SELECT ...[SELECT [...]]]
```

```sql
SELECT MIN(number) FROM (SELECT number%3 AS number FROM numbers(10)) GROUP BY number%2;
+-------------+
| min(number) |
+-------------+
|           1 |
|           0 |
+-------------+
```