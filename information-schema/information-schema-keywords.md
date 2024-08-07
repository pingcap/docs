---
title: KEYWORDS
summary: KEYWORDS` INFORMATION_SCHEMA テーブルについて学習します。
---

# キーワード {#keywords}

v7.5.3 以降、TiDB は`KEYWORDS`テーブルを提供します。このテーブルを使用して、TiDB の[キーワード](/keywords.md)に関する情報を取得できます。

```sql
USE INFORMATION_SCHEMA;
DESC keywords;
```

出力は次のようになります。

    +----------+--------------+------+------+---------+-------+
    | Field    | Type         | Null | Key  | Default | Extra |
    +----------+--------------+------+------+---------+-------+
    | WORD     | varchar(128) | YES  |      | NULL    |       |
    | RESERVED | int(11)      | YES  |      | NULL    |       |
    +----------+--------------+------+------+---------+-------+
    2 rows in set (0.00 sec)

フィールドの説明:

-   `WORD` : キーワード。
-   `RESERVED` : キーワードが予約されているかどうか。

次のステートメントは、キーワード`ADD`と`USER`に関する情報を照会します。

```sql
SELECT * FROM INFORMATION_SCHEMA.KEYWORDS WHERE WORD IN ('ADD','USER');
```

出力から、 `ADD`予約済みキーワードであり、 `USER`非予約済みキーワードであることがわかります。

    +------+----------+
    | WORD | RESERVED |
    +------+----------+
    | ADD  |        1 |
    | USER |        0 |
    +------+----------+
    2 rows in set (0.00 sec)
