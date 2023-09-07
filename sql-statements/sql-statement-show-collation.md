---
title: SHOW COLLATION | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW COLLATION for the TiDB database.
---

# 照合順序を表示 {#show-collation}

このステートメントは照合順序の静的なリストを提供し、MySQL クライアント ライブラリとの互換性を提供するために組み込まれています。

> **注記：**
>
> [「新しい照合順序ワーク」](/character-set-and-collation.md#new-framework-for-collations)が有効な場合、 `SHOW COLLATION`の結果は異なります。新しい照合順序フレームワークの詳細については、 [文字セットと照合順序](/character-set-and-collation.md)を参照してください。

## あらすじ {#synopsis}

**照合順序の表示:**

![ShowCollationStmt](/media/sqlgram/ShowCollationStmt.png)

## 例 {#examples}

新しい照合順序順序フレームワークが無効になっている場合、バイナリ照合順序のみが表示されます。

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

## MySQLの互換性 {#mysql-compatibility}

TiDB での`SHOW COLLATION`ステートメントの使用は、MySQL と完全に互換性があります。ただし、TiDB の文字セットには、MySQL と比較してデフォルトの照合順序が異なる場合があります。詳細は[MySQLとの互換性](/mysql-compatibility.md)を参照してください。互換性の違いが見つかった場合は、 [バグを報告](https://docs.pingcap.com/tidb/stable/support) .

## こちらも参照 {#see-also}

-   [キャラクターセットを表示](/sql-statements/sql-statement-show-character-set.md)
-   [文字セットと照合順序](/character-set-and-collation.md)
