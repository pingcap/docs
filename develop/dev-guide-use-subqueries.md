---
title: Subquery
summary: Learn how to use subquery in TiDB.
---

# サブクエリ {#subquery}

このドキュメントでは、TiDB のサブクエリ ステートメントとカテゴリを紹介します。

## 概要 {#overview}

サブクエリは、別の SQL クエリ内のクエリです。サブクエリを使用すると、クエリ結果を別のクエリで使用できます。

以下では、 [書店](/develop/dev-guide-bookshop-schema-design.md)アプリケーションを例として、サブクエリを紹介します。

## サブクエリ文 {#subquery-statement}

ほとんどの場合、サブクエリには次の 5 種類があります。

-   スカラー サブクエリ ( `SELECT (SELECT s1 FROM t2) FROM t1`など)。
-   派生テーブル ( `SELECT t1.s1 FROM (SELECT s1 FROM t2) t1`など)。
-   存在テスト ( `WHERE NOT EXISTS(SELECT ... FROM t2)` 、 `WHERE t1.a IN (SELECT ... FROM t2)`など)。
-   `WHERE t1.a = ANY(SELECT ... FROM t2)` 、 `WHERE t1.a = ANY(SELECT ... FROM t2)`などの定量化された比較。
-   比較演算子のオペランドとしてのサブクエリ ( `WHERE t1.a > (SELECT ... FROM t2)`など)。

## サブクエリのカテゴリ {#category-of-subquery}

サブクエリは[相関サブクエリ](https://en.wikipedia.org/wiki/Correlated_subquery)と自己完結型サブクエリに分類できます。 TiDB は、これら 2 つのタイプを別々に扱います。

サブクエリが相関しているかどうかは、サブクエリがその外側のクエリで使用されている列を参照しているかどうかによって決まります。

### 自己完結型サブクエリ {#self-contained-subquery}

subquery を比較演算子のオペランド ( `>` 、 `>=` 、 `<` 、 `<=` 、 `=` 、または`! =` ) として使用する自己完結型サブクエリの場合、内部サブクエリは 1 回だけクエリを実行し、TiDB は実行計画フェーズ中にそれを定数として書き換えます。

たとえば、平均年齢よりも年齢が高い`authors`テーブルの著者をクエリするには、サブクエリを比較演算子のオペランドとして使用できます。

```sql
SELECT * FROM authors a1 WHERE (IFNULL(a1.death_year, YEAR(NOW())) - a1.birth_year) > (
    SELECT
        AVG(IFNULL(a2.death_year, YEAR(NOW())) - a2.birth_year) AS average_age
    FROM
        authors a2
)
```

内部サブクエリは、TiDB が上記のクエリを実行する前に実行されます。

```sql
SELECT AVG(IFNULL(a2.death_year, YEAR(NOW())) - a2.birth_year) AS average_age FROM authors a2;
```

クエリの結果が 34、つまり平均年齢が 34 歳であるとします。34 は元のサブクエリを置き換える定数として使用されます。

```sql
SELECT * FROM authors a1
WHERE (IFNULL(a1.death_year, YEAR(NOW())) - a1.birth_year) > 34;
```

結果は次のとおりです。

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

Existential Test や Quantified Comparison などの自己完結型サブクエリの場合、TiDB はパフォーマンスを向上させるためにそれらを書き換えて同等のクエリに置き換えます。詳細については、 [サブクエリ関連の最適化](/subquery-optimization.md)を参照してください。

### 相関サブクエリ {#correlated-subquery}

相関サブクエリの場合、内部サブクエリは外部クエリの列を参照するため、各サブクエリは外部クエリの行ごとに 1 回実行されます。つまり、外側のクエリが 1,000 万件の結果を取得すると仮定すると、サブクエリも 1,000 万回実行され、より多くの時間とリソースが消費されます。

したがって、処理の過程で、TiDB は実行プラン レベルでのクエリ効率の[相関サブクエリの相関解除](/correlated-subquery-optimization.md)を試みます。

次のステートメントは、同性の他の著者の平均年齢よりも年上の著者を照会するものです。

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

TiDB はこれを同等の`join`クエリに書き換えます。

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

ベスト プラクティスとして、実際の開発では、パフォーマンスが向上する別の同等のクエリを作成できる場合は、相関サブクエリを介したクエリを回避することをお勧めします。

## 続きを読む {#read-more}

-   [サブクエリ関連の最適化](/subquery-optimization.md)
-   [相関サブクエリの相関解除](/correlated-subquery-optimization.md)
-   [TiDB でのサブクエリの最適化](https://en.pingcap.com/blog/subquery-optimization-in-tidb/)
