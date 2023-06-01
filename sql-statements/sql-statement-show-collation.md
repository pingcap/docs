---
title: SHOW COLLATION | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW COLLATION for the TiDB database.
---

# 照合順序を表示 {#show-collation}

このステートメントは照合順序の静的なリストを提供し、MySQL クライアント ライブラリとの互換性を提供するために組み込まれています。

> **ノート：**
>
> [<a href="/character-set-and-collation.md#new-framework-for-collations">「新しい照合順序ワーク」</a>](/character-set-and-collation.md#new-framework-for-collations)が有効な場合、 `SHOW COLLATION`の結果は異なります。新しい照合順序フレームワークの詳細については、 [<a href="/character-set-and-collation.md">文字セットと照合順序</a>](/character-set-and-collation.md)を参照してください。

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

このステートメントの使用法は、MySQL と完全な互換性があると理解されています。ただし、TiDB の文字セットには、MySQL と比較してデフォルトの照合順序が異なる場合があります。詳細は[<a href="/mysql-compatibility.md">MySQLとの互換性</a>](/mysql-compatibility.md)を参照してください。その他の互換性の違いは、GitHub では[<a href="https://github.com/pingcap/tidb/issues/new/choose">問題を通じて報告されました</a>](https://github.com/pingcap/tidb/issues/new/choose)である必要があります。

## こちらも参照 {#see-also}

-   [<a href="/sql-statements/sql-statement-show-character-set.md">キャラクターセットを表示</a>](/sql-statements/sql-statement-show-character-set.md)
-   [<a href="/character-set-and-collation.md">文字セットと照合順序</a>](/character-set-and-collation.md)
