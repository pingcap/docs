---
title: SHOW COLLATION | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW COLLATION for the TiDB database.
---

# 照合を表示 {#show-collation}

このステートメントは、照合順序の静的リストを提供し、MySQL クライアント ライブラリとの互換性を提供するために含まれています。

> **ノート：**
>
> [「新しい照合順序ワーク」](/character-set-and-collation.md#new-framework-for-collations)が有効な場合、 `SHOW COLLATION`の結果は異なります。新しい照合順序フレームワークの詳細については、 [文字セットと照合順序](/character-set-and-collation.md)を参照してください。

## あらすじ {#synopsis}

**ShowCollationStmt:**

![ShowCollationStmt](/media/sqlgram/ShowCollationStmt.png)

## 例 {#examples}

新しい照合順序フレームワークが無効になっている場合、バイナリ照合のみが表示されます。

```sql
mysql> SHOW COLLATION;
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
```

新しい照合順序フレームワークが有効になっている場合、 `utf8_general_ci`と`utf8mb4_general_ci`が追加でサポートされます。

```sql
mysql> SHOW COLLATION;
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
```

## MySQL の互換性 {#mysql-compatibility}

このステートメントの使用法は、MySQL と完全に互換性があると理解されています。ただし、TiDB の文字セットは、MySQL とは異なるデフォルトの照合を持つ場合があります。詳細については、 [MySQL との互換性](/mysql-compatibility.md)を参照してください。その他の互換性の違いは、GitHub で[問題を介して報告された](https://github.com/pingcap/tidb/issues/new/choose)にする必要があります。

## こちらもご覧ください {#see-also}

-   [キャラクターセットを表示](/sql-statements/sql-statement-show-character-set.md)
-   [文字セットと照合順序](/character-set-and-collation.md)
