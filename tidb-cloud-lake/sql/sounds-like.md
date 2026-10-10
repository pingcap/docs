---
title: SOUNDS LIKE
summary: 2 つの文字列の発音を、それぞれの Soundex コードを使って比較します。Soundex は、文字列の発音を表すコードを生成する音声学的アルゴリズムで、スペルではなく発音に基づいて文字列をおおよそ一致させることができます。{{{ .lake }}} では、文字列から Soundex コードを取得できる [SOUNDEX](/tidb-cloud-lake/sql/soundex.md) 関数を提供しています。
---

# SOUNDS LIKE

2 つの文字列の発音を、それぞれの Soundex コードを使って比較します。Soundex は、文字列の発音を表すコードを生成する音声学的アルゴリズムで、スペルではなく発音に基づいて文字列をおおよそ一致させることができます。{{{ .lake }}} では、文字列から Soundex コードを取得できる [SOUNDEX](/tidb-cloud-lake/sql/soundex.md) 関数を提供しています。

SOUNDS LIKE は、名前や住所などに対するあいまいな文字列一致を使って行を絞り込むために、SQL クエリの WHERE 句でよく使用されます。詳細は、[例](#examples) の [行のフィルタリング](#filtering-rows) を参照してください。

> **Note:**
>
> この関数は近似的な文字列一致に役立つ場合がありますが、常に正確であるとは限らない点に注意してください。Soundex アルゴリズムは英語の発音規則に基づいているため、他の言語や方言の文字列にはうまく機能しないことがあります。

## 構文 {#syntax}

```sql
<str1> SOUNDS LIKE <str2>
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|-------------|
| str1, 2   | 比較する文字列です。 |

## 戻り値の型 {#return-type}

2 つの文字列の Soundex コードが同じ場合（つまり、発音が似ている場合）は Boolean 値 1 を返し、それ以外の場合は 0 を返します。

## 例 {#examples}

### 文字列の比較 {#comparing-strings}

```sql
SELECT 'two' SOUNDS LIKE 'too'
----
1

SELECT CONCAT('A', 'B') SOUNDS LIKE 'AB';
----
1

SELECT 'Monday' SOUNDS LIKE 'Sunday';
----
0
```

### 行のフィルタリング {#filtering-rows}

```sql
SELECT * FROM  employees;

id|first_name|last_name|age|
--+----------+---------+---+
 0|John      |Smith    | 35|
 0|Mark      |Smythe   | 28|
 0|Johann    |Schmidt  | 51|
 0|Eric      |Doe      | 30|
 0|Sue       |Johnson  | 45|

SELECT * FROM  employees
WHERE  first_name SOUNDS LIKE 'John';

id|first_name|last_name|age|
--+----------+---------+---+
 0|John      |Smith    | 35|
 0|Johann    |Schmidt  | 51|
```