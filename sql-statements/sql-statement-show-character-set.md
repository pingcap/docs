---
title: SHOW CHARACTER SET | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW CHARACTER SET for the TiDB database.
---

# キャラクターセットを表示 {#show-character-set}

このステートメントは、TiDB で使用可能な文字セットの静的リストを提供します。出力には、現在の接続またはユーザーの属性は反映されません。

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

## MySQL の互換性 {#mysql-compatibility}

このステートメントの使用法は、MySQL と完全に互換性があると理解されています。ただし、TiDB の文字セットは、MySQL とは異なるデフォルトの照合を持つ場合があります。詳細については、 [MySQL との互換性](/mysql-compatibility.md)を参照してください。その他の互換性の違いは、GitHub で[問題を介して報告された](https://github.com/pingcap/tidb/issues/new/choose)にする必要があります。

## こちらもご覧ください {#see-also}

-   [照合を表示](/sql-statements/sql-statement-show-collation.md)
-   [文字セットと照合順序](/character-set-and-collation.md)
