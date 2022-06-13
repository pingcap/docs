---
title: Subquery
summary: Learn how to use subquery in TiDB.
---

# サブクエリ {#subquery}

このドキュメントでは、TiDBのサブクエリステートメントとカテゴリを紹介します。

## 概要 {#overview}

サブクエリは、別のSQLクエリ内のクエリです。サブクエリを使用すると、クエリ結果を別のクエリで使用できます。

以下では、サブクエリを導入するための例として[書店](/develop/dev-guide-bookshop-schema-design.md)のアプリケーションを取り上げます。

## サブクエリステートメント {#subquery-statement}

ほとんどの場合、サブクエリには5つのタイプがあります。

-   `SELECT (SELECT s1 FROM t2) FROM t1`などのスカラーサブクエリ。
-   `SELECT t1.s1 FROM (SELECT s1 FROM t2) t1`などの派生テーブル。
-   `WHERE NOT EXISTS(SELECT ... FROM t2)`などの`WHERE t1.a IN (SELECT ... FROM t2)`的テスト。
-   `WHERE t1.a = ANY(SELECT ... FROM t2)`などの`WHERE t1.a = ANY(SELECT ... FROM t2)`化された比較。
-   `WHERE t1.a > (SELECT ... FROM t2)`などの比較演算子オペランドとしてのサブクエリ。

## サブクエリのカテゴリ {#category-of-subquery}

サブクエリは、 [相関サブクエリ](https://en.wikipedia.org/wiki/Correlated_subquery)と自己完結型サブクエリに分類できます。 TiDBは、これら2つのタイプを異なる方法で処理します。

サブクエリが相関しているかどうかは、外部クエリで使用されている列を参照しているかどうかによって異なります。

### 自己完結型サブクエリ {#self-contained-subquery}

比較演算子（ `>` 、または`<=` ）のオペランドとしてサブクエリを使用する自己完結型サブクエリの`! =` 、内部サブクエリは`<` `>=`だけクエリを実行し、 `=`は実行プランフェーズで定数として書き換えます。

たとえば、年齢が平均年齢よりも大きい`authors`テーブルの作成者にクエリを実行するには、比較演算子のオペランドとしてサブクエリを使用できます。

{{< copyable "" >}}

```sql
SELECT * FROM authors a1 WHERE (IFNULL(a1.death_year, YEAR(NOW())) - a1.birth_year) > (
    SELECT
        AVG(IFNULL(a2.death_year, YEAR(NOW())) - a2.birth_year) AS average_age
    FROM
        authors a2
)
```

内部サブクエリは、TiDBが上記のクエリを実行する前に実行されます。

{{< copyable "" >}}

```sql
SELECT AVG(IFNULL(a2.death_year, YEAR(NOW())) - a2.birth_year) AS average_age FROM authors a2;
```

クエリの結果が34、つまり平均年齢が34であり、34が元のサブクエリを置き換える定数として使用されるとします。

{{< copyable "" >}}

```sql
SELECT * FROM authors a1
WHERE (IFNULL(a1.death_year, YEAR(NOW())) - a1.birth_year) > 34;
```

結果は次のとおりです。

```
+--------+-------------------+--------+------------+------------+
| id     | name              | gender | birth_year | death_year |
+--------+-------------------+--------+------------+------------+
| 13514  | Kennith Kautzer   | 1      | 1956       | 2018       |
| 13748  | Dillon Langosh    | 1      | 1985       | NULL       |
| 99184  | Giovanny Emmerich | 1      | 1954       | 2012       |
| 180191 | Myrtie Robel      | 1      | 1958       | 2009       |
| 200969 | Iva Renner        | 0      | 1977       | NULL       |
| 209671 | Abraham Ortiz     | 0      | 1943       | 2016       |
| 229908 | Wellington Wiza   | 1      | 1932       | 1969       |
| 306642 | Markus Crona      | 0      | 1969       | NULL       |
| 317018 | Ellis McCullough  | 0      | 1969       | 2014       |
| 322369 | Mozelle Hand      | 0      | 1942       | 1977       |
| 325946 | Elta Flatley      | 0      | 1933       | 1986       |
| 361692 | Otho Langosh      | 1      | 1931       | 1997       |
| 421294 | Karelle VonRueden | 0      | 1977       | NULL       |
...
```

ExistentialTestやQuantifiedComparisonなどの自己完結型のサブクエリの場合、TiDBはそれらを書き換えて同等のクエリに置き換え、パフォーマンスを向上させます。詳細については、 [サブクエリ関連の最適化](/subquery-optimization.md)を参照してください。

### 相関サブクエリ {#correlated-subquery}

相関サブクエリの場合、内部サブクエリは外部クエリの列を参照するため、各サブクエリは外部クエリの行ごとに1回実行されます。つまり、外部クエリが1,000万件の結果を取得すると仮定すると、サブクエリも1,000万回実行されるため、より多くの時間とリソースが消費されます。

したがって、処理の過程で、TiDBは実行プランレベルでクエリの効率を向上させるために[相関サブクエリの非相関](/correlated-subquery-optimization.md)を試みます。

次のステートメントは、同じ性別の他の著者の平均年齢よりも年上の著者にクエリを実行するためのものです。

{{< copyable "" >}}

```sql
SELECT * FROM authors a1 WHERE (IFNULL(a1.death_year, YEAR(NOW())) - a1.birth_year) > (
    SELECT
        AVG(
            IFNULL(a2.death_year, YEAR(NOW())) - IFNULL(a2.birth_year, YEAR(NOW()))
        ) AS average_age
    FROM
        authors a2
    WHERE a1.gender = a2.gender
);
```

TiDBはそれを同等の`join`クエリに書き換えます。

{{< copyable "" >}}

```sql
SELECT *
FROM
    authors a1,
    (
        SELECT
            gender, AVG(
                IFNULL(a2.death_year, YEAR(NOW())) - IFNULL(a2.birth_year, YEAR(NOW()))
            ) AS average_age
        FROM
            authors a2
        GROUP BY gender
    ) a2
WHERE
    a1.gender = a2.gender
    AND (IFNULL(a1.death_year, YEAR(NOW())) - a1.birth_year) > a2.average_age;
```

ベストプラクティスとして、実際の開発では、パフォーマンスが向上した別の同等のクエリを作成できる場合は、相関サブクエリによるクエリを回避することをお勧めします。

## 続きを読む {#read-more}

-   [サブクエリ関連の最適化](/subquery-optimization.md)
-   [相関サブクエリの無相関化](/correlated-subquery-optimization.md)
-   [TiDBでのサブクエリの最適化](https://en.pingcap.com/blog/subquery-optimization-in-tidb/)
