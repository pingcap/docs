---
title: SHOW CHARACTER SET | TiDB SQL Statement Reference
summary: TiDB データベースの SHOW CHARACTER SET の使用法の概要。
---

# 文字セットを表示 {#show-character-set}

このステートメントは、TiDBで使用可能な文字セットの静的リストを提供します。出力には、現在の接続またはユーザーの属性は反映されません。

## 概要 {#synopsis}

```ebnf+diagram
ShowCharsetStmt ::=
    "SHOW" ( ("CHARACTER" | "CHAR") "SET" | "CHARSET" ) ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 例 {#examples}

```sql
SHOW CHARACTER SET;
```

    +---------+-------------------------------------+-------------------+--------+
    | Charset | Description                         | Default collation | Maxlen |
    +---------+-------------------------------------+-------------------+--------+
    | ascii   | US ASCII                            | ascii_bin         |      1 |
    | binary  | binary                              | binary            |      1 |
    | gbk     | Chinese Internal Code Specification | gbk_chinese_ci    |      2 |
    | latin1  | Latin1                              | latin1_bin        |      1 |
    | utf8    | UTF-8 Unicode                       | utf8_bin          |      3 |
    | utf8mb4 | UTF-8 Unicode                       | utf8mb4_bin       |      4 |
    +---------+-------------------------------------+-------------------+--------+
    6 rows in set (0.00 sec)

```sql
SHOW CHARACTER SET LIKE 'utf8%';
```

    +---------+---------------+-------------------+--------+
    | Charset | Description   | Default collation | Maxlen |
    +---------+---------------+-------------------+--------+
    | utf8    | UTF-8 Unicode | utf8_bin          |      3 |
    | utf8mb4 | UTF-8 Unicode | utf8mb4_bin       |      4 |
    +---------+---------------+-------------------+--------+
    2 rows in set (0.00 sec)

```sql
SHOW CHARACTER SET WHERE Description='UTF-8 Unicode';
```

    +---------+---------------+-------------------+--------+
    | Charset | Description   | Default collation | Maxlen |
    +---------+---------------+-------------------+--------+
    | utf8    | UTF-8 Unicode | utf8_bin          |      3 |
    | utf8mb4 | UTF-8 Unicode | utf8mb4_bin       |      4 |
    +---------+---------------+-------------------+--------+
    2 rows in set (0.00 sec)

## MySQLの互換性 {#mysql-compatibility}

TiDBの`SHOW CHARACTER SET`文の使用方法はMySQLと完全に互換性があります。ただし、TiDBの文字セットはMySQLと比較してデフォルトの照合順序が異なる場合があります。詳細については[MySQLとの互換性](/mysql-compatibility.md)参照してください。互換性に関する相違点が見つかった場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support)参照してください。

## 参照 {#see-also}

-   [照合順序を表示](/sql-statements/sql-statement-show-collation.md)
-   [文字セットと照合順序](/character-set-and-collation.md)
