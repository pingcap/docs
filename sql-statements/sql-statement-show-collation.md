---
title: SHOW COLLATION | TiDB SQL Statement Reference
summary: TiDB データベースの SHOW COLLATION の使用法の概要。
---

# 照合を表示 {#show-collation}

このステートメントは照合順序の静的リストを提供し、MySQL クライアント ライブラリとの互換性を提供するために含まれています。

> **注記：**
>
> `SHOW COLLATION`の結果は、 [「新しい照合順序フレームワーク」](/character-set-and-collation.md#new-framework-for-collations)が有効な場合に変わります。新しい照合順序フレームワークの詳細については、 [文字セットと照合順序](/character-set-and-collation.md)を参照してください。

## 概要 {#synopsis}

```ebnf+diagram
ShowCollationStmt ::=
    "SHOW" "COLLATION" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 例 {#examples}

新しい照合順序フレームワークが無効になっている場合は、バイナリ照合のみが表示されます。

```sql
SHOW COLLATION;
```

    +-------------+---------+------+---------+----------+---------+
    | Collation   | Charset | Id   | Default | Compiled | Sortlen |
    +-------------+---------+------+---------+----------+---------+
    | utf8mb4_bin | utf8mb4 |   46 | Yes     | Yes      |       1 |
    | latin1_bin  | latin1  |   47 | Yes     | Yes      |       1 |
    | binary      | binary  |   63 | Yes     | Yes      |       1 |
    | ascii_bin   | ascii   |   65 | Yes     | Yes      |       1 |
    | utf8_bin    | utf8    |   83 | Yes     | Yes      |       1 |
    +-------------+---------+------+---------+----------+---------+
    5 rows in set (0.02 sec)

新しい照合順序フレームワークが有効になっている場合、 `utf8_general_ci`と`utf8mb4_general_ci`追加でサポートされます。

```sql
SHOW COLLATION;
```

    +--------------------+---------+------+---------+----------+---------+
    | Collation          | Charset | Id   | Default | Compiled | Sortlen |
    +--------------------+---------+------+---------+----------+---------+
    | ascii_bin          | ascii   |   65 | Yes     | Yes      |       1 |
    | binary             | binary  |   63 | Yes     | Yes      |       1 |
    | gbk_bin            | gbk     |   87 |         | Yes      |       1 |
    | gbk_chinese_ci     | gbk     |   28 | Yes     | Yes      |       1 |
    | latin1_bin         | latin1  |   47 | Yes     | Yes      |       1 |
    | utf8_bin           | utf8    |   83 | Yes     | Yes      |       1 |
    | utf8_general_ci    | utf8    |   33 |         | Yes      |       1 |
    | utf8_unicode_ci    | utf8    |  192 |         | Yes      |       1 |
    | utf8mb4_bin        | utf8mb4 |   46 | Yes     | Yes      |       1 |
    | utf8mb4_general_ci | utf8mb4 |   45 |         | Yes      |       1 |
    | utf8mb4_unicode_ci | utf8mb4 |  224 |         | Yes      |       1 |
    +--------------------+---------+------+---------+----------+---------+
    11 rows in set (0.001 sec)

文字セットでフィルタリングするには、 `WHERE`句を追加できます。

```sql
SHOW COLLATION WHERE Charset="utf8mb4";
```

```sql
+--------------------+---------+-----+---------+----------+---------+
| Collation          | Charset | Id  | Default | Compiled | Sortlen |
+--------------------+---------+-----+---------+----------+---------+
| utf8mb4_0900_ai_ci | utf8mb4 | 255 |         | Yes      |       1 |
| utf8mb4_0900_bin   | utf8mb4 | 309 |         | Yes      |       1 |
| utf8mb4_bin        | utf8mb4 |  46 | Yes     | Yes      |       1 |
| utf8mb4_general_ci | utf8mb4 |  45 |         | Yes      |       1 |
| utf8mb4_unicode_ci | utf8mb4 | 224 |         | Yes      |       1 |
+--------------------+---------+-----+---------+----------+---------+
5 rows in set (0.00 sec)
```

## MySQL 互換性 {#mysql-compatibility}

TiDB の`SHOW COLLATION`ステートメントの使用法は、MySQL と完全に互換性があります。ただし、TiDB の文字セットは、MySQL と比較してデフォルトの照合順序が異なる場合があります。詳細については、 [MySQLとの互換性](/mysql-compatibility.md)を参照してください。互換性の違いが見つかった場合は、 [バグを報告](https://docs.pingcap.com/tidb/stable/support)を参照してください。

## 参照 {#see-also}

-   [文字セットを表示](/sql-statements/sql-statement-show-character-set.md)
-   [文字セットと照合順序](/character-set-and-collation.md)
