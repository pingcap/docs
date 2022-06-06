---
title: SHOW COLLATION | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW COLLATION for the TiDB database.
---

# 照合を表示 {#show-collation}

このステートメントは、照合の静的リストを提供し、MySQLクライアントライブラリとの互換性を提供するために含まれています。

> **ノート：**
>
> [「新しい照合順序フレームワーク」](/character-set-and-collation.md#new-framework-for-collations)を有効にすると、 `SHOW COLLATION`の結果は異なります。新しい照合順序フレームワークの詳細については、 [キャラクターセットと照合](/character-set-and-collation.md)を参照してください。

## あらすじ {#synopsis}

**ShowCollationStmt：**

![ShowCollationStmt](/media/sqlgram/ShowCollationStmt.png)

## 例 {#examples}

新しい照合順序フレームワークを無効にすると、バイナリ照合のみが表示されます。

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

新しい照合順序フレームワークを有効にすると、 `utf8_general_ci`と`utf8mb4_general_ci`が追加でサポートされます。

```sql
mysql> SHOW COLLATION;
+--------------------+---------+------+---------+----------+---------+
| Collation          | Charset | Id   | Default | Compiled | Sortlen |
+--------------------+---------+------+---------+----------+---------+
| utf8mb4_bin        | utf8mb4 |   46 | Yes     | Yes      |       1 |
| latin1_bin         | latin1  |   47 | Yes     | Yes      |       1 |
| binary             | binary  |   63 | Yes     | Yes      |       1 |
| ascii_bin          | ascii   |   65 | Yes     | Yes      |       1 |
| utf8_bin           | utf8    |   83 | Yes     | Yes      |       1 |
| utf8_general_ci    | utf8    |   33 |         | Yes      |       1 |
| utf8mb4_general_ci | utf8    |   45 |         | Yes      |       1 |
+--------------------+---------+------+---------+----------+---------+
7 rows in set (0.02 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントの使用法は、MySQLと完全に互換性があると理解されています。ただし、TiDBの文字セットは、MySQLと比較してデフォルトの照合が異なる場合があります。詳しくは[MySQLとの互換性](/mysql-compatibility.md)をご覧ください。その他の互換性の違いは、GitHub [問題を介して報告](https://github.com/pingcap/tidb/issues/new/choose)である必要があります。

## も参照してください {#see-also}

-   [文字セットを表示](/sql-statements/sql-statement-show-character-set.md)
-   [キャラクターセットと照合](/character-set-and-collation.md)
