---
title: SHOW COLLATION | TiDB SQL Statement Reference
summary: TiDB データベースの SHOW COLLATION の使用法の概要。
---

# 照合順序を表示 {#show-collation}

このステートメントは照合の静的リストを提供し、MySQL クライアント ライブラリとの互換性を提供するために含まれています。

> **注記：**
>
> [「新しい照合順序フレームワーク」](/character-set-and-collation.md#new-framework-for-collations)有効になっている場合、 `SHOW COLLATION`の結果は異なります。新しい照合順序フレームワークの詳細については、 [文字セットと照合順序](/character-set-and-collation.md)を参照してください。

## 概要 {#synopsis}

```ebnf+diagram
ShowCollationStmt ::=
    "SHOW" "COLLATION" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 例 {#examples}

<CustomContent platform="tidb">

[新しい照合順序ワーク](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)が有効になっている場合 (デフォルト)、出力例は次のようになります。

</CustomContent>

```sql
SHOW COLLATION;
```

    +--------------------+---------+-----+---------+----------+---------+---------------+
    | Collation          | Charset | Id  | Default | Compiled | Sortlen | Pad_attribute |
    +--------------------+---------+-----+---------+----------+---------+---------------+
    | ascii_bin          | ascii   |  65 | Yes     | Yes      |       1 | PAD SPACE     |
    | binary             | binary  |  63 | Yes     | Yes      |       1 | NO PAD        |
    | gbk_bin            | gbk     |  87 |         | Yes      |       1 | PAD SPACE     |
    | gbk_chinese_ci     | gbk     |  28 | Yes     | Yes      |       1 | PAD SPACE     |
    | latin1_bin         | latin1  |  47 | Yes     | Yes      |       1 | PAD SPACE     |
    | utf8_bin           | utf8    |  83 | Yes     | Yes      |       1 | PAD SPACE     |
    | utf8_general_ci    | utf8    |  33 |         | Yes      |       1 | PAD SPACE     |
    | utf8_unicode_ci    | utf8    | 192 |         | Yes      |       8 | PAD SPACE     |
    | utf8mb4_0900_ai_ci | utf8mb4 | 255 |         | Yes      |       0 | NO PAD        |
    | utf8mb4_0900_bin   | utf8mb4 | 309 |         | Yes      |       1 | NO PAD        |
    | utf8mb4_bin        | utf8mb4 |  46 | Yes     | Yes      |       1 | PAD SPACE     |
    | utf8mb4_general_ci | utf8mb4 |  45 |         | Yes      |       1 | PAD SPACE     |
    | utf8mb4_unicode_ci | utf8mb4 | 224 |         | Yes      |       8 | PAD SPACE     |
    +--------------------+---------+-----+---------+----------+---------+---------------+
    13 rows in set (0.00 sec)

<CustomContent platform="tidb">

新しい照合順序フレームワークが無効になっている場合は、バイナリ照合のみがリストされます。

```sql
SHOW COLLATION;
```

    +-------------+---------+----+---------+----------+---------+---------------+
    | Collation   | Charset | Id | Default | Compiled | Sortlen | Pad_attribute |
    +-------------+---------+----+---------+----------+---------+---------------+
    | utf8mb4_bin | utf8mb4 | 46 | Yes     | Yes      |       1 | PAD SPACE     |
    | latin1_bin  | latin1  | 47 | Yes     | Yes      |       1 | PAD SPACE     |
    | binary      | binary  | 63 | Yes     | Yes      |       1 | NO PAD        |
    | ascii_bin   | ascii   | 65 | Yes     | Yes      |       1 | PAD SPACE     |
    | utf8_bin    | utf8    | 83 | Yes     | Yes      |       1 | PAD SPACE     |
    | gbk_bin     | gbk     | 87 | Yes     | Yes      |       1 | PAD SPACE     |
    +-------------+---------+----+---------+----------+---------+---------------+
    6 rows in set (0.00 sec)

</CustomContent>

文字セットでフィルタリングするには、 `WHERE`句を追加できます。

```sql
SHOW COLLATION WHERE Charset="utf8mb4";
```

```sql
+--------------------+---------+-----+---------+----------+---------+---------------+
| Collation          | Charset | Id  | Default | Compiled | Sortlen | Pad_attribute |
+--------------------+---------+-----+---------+----------+---------+---------------+
| utf8mb4_0900_ai_ci | utf8mb4 | 255 |         | Yes      |       0 | NO PAD        |
| utf8mb4_0900_bin   | utf8mb4 | 309 |         | Yes      |       1 | NO PAD        |
| utf8mb4_bin        | utf8mb4 |  46 | Yes     | Yes      |       1 | PAD SPACE     |
| utf8mb4_general_ci | utf8mb4 |  45 |         | Yes      |       1 | PAD SPACE     |
| utf8mb4_unicode_ci | utf8mb4 | 224 |         | Yes      |       8 | PAD SPACE     |
+--------------------+---------+-----+---------+----------+---------+---------------+
5 rows in set (0.001 sec)
```

## MySQLの互換性 {#mysql-compatibility}

TiDBにおける`SHOW COLLATION`文の使用法はMySQLと完全に互換性があります。ただし、TiDBの文字セットはMySQLと比較してデフォルトの照合順序が異なる場合があります。詳細については[MySQLとの互換性](/mysql-compatibility.md)参照してください。互換性に関する相違点が見つかった場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support)参照してください。

## 参照 {#see-also}

-   [文字セットを表示](/sql-statements/sql-statement-show-character-set.md)
-   [文字セットと照合順序](/character-set-and-collation.md)
