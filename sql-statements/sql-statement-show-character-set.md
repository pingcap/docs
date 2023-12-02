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

TiDB での`SHOW CHARACTER SET`ステートメントの使用は、MySQL と完全に互換性があります。ただし、TiDB の文字セットには、MySQL と比較してデフォルトの照合順序が異なる場合があります。詳細は[MySQLとの互換性](/mysql-compatibility.md)を参照してください。互換性の違いが見つかった場合は、 [バグを報告](https://docs.pingcap.com/tidb/stable/support) .

## こちらも参照 {#see-also}

-   [照合順序を表示](/sql-statements/sql-statement-show-collation.md)
-   [文字セットと照合順序](/character-set-and-collation.md)
