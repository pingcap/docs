---
title: SHOW CHARACTER SET | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW CHARACTER SET for the TiDB database.
---

# 文字セットを表示 {#show-character-set}

このステートメントは、TiDBで使用可能な文字セットの静的リストを提供します。出力には、現在の接続またはユーザーの属性は反映されません。

## あらすじ {#synopsis}

**ShowCharsetStmt：**

![ShowCharsetStmt](/media/sqlgram/ShowCharsetStmt.png)

**CharsetKw：**

![CharsetKw](/media/sqlgram/CharsetKw.png)

## 例 {#examples}

```sql
mysql> SHOW CHARACTER SET;
+---------+---------------+-------------------+--------+
| Charset | Description   | Default collation | Maxlen |
+---------+---------------+-------------------+--------+
| utf8    | UTF-8 Unicode | utf8_bin          |      3 |
| utf8mb4 | UTF-8 Unicode | utf8mb4_bin       |      4 |
| ascii   | US ASCII      | ascii_bin         |      1 |
| latin1  | Latin1        | latin1_bin        |      1 |
| binary  | binary        | binary            |      1 |
+---------+---------------+-------------------+--------+
5 rows in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントの使用法は、MySQLと完全に互換性があると理解されています。ただし、TiDBの文字セットは、MySQLと比較してデフォルトの照合が異なる場合があります。詳しくは[MySQLとの互換性](/mysql-compatibility.md)をご覧ください。その他の互換性の違いは、GitHub [問題を介して報告された](https://github.com/pingcap/tidb/issues/new/choose)である必要があります。

## も参照してください {#see-also}

-   [照合を表示](/sql-statements/sql-statement-show-collation.md)
-   [文字セットと照合](/character-set-and-collation.md)
