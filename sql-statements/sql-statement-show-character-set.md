---
title: SHOW CHARACTER SET | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW CHARACTER SET for the TiDB database.
---

# キャラクターセットを表示 {#show-character-set}

このステートメントは、TiDB で使用可能な文字セットの静的なリストを提供します。出力には、現在の接続またはユーザーの属性は反映されません。

## あらすじ {#synopsis}

**ShowCharsetStmt:**

![ShowCharsetStmt](/media/sqlgram/ShowCharsetStmt.png)

**文字セットKw:**

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

このステートメントの使用法は、MySQL と完全な互換性があると理解されています。ただし、TiDB の文字セットには、MySQL と比較してデフォルトの照合順序が異なる場合があります。詳細は[<a href="/mysql-compatibility.md">MySQLとの互換性</a>](/mysql-compatibility.md)を参照してください。その他の互換性の違いは、GitHub では[<a href="https://github.com/pingcap/tidb/issues/new/choose">問題を通じて報告されました</a>](https://github.com/pingcap/tidb/issues/new/choose)である必要があります。

## こちらも参照 {#see-also}

-   [<a href="/sql-statements/sql-statement-show-collation.md">照合順序を表示</a>](/sql-statements/sql-statement-show-collation.md)
-   [<a href="/character-set-and-collation.md">文字セットと照合順序</a>](/character-set-and-collation.md)
