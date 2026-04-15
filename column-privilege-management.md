---
title: Column-Level Privilege Management
summary: TiDBは、MySQL互換の列レベルの権限管理メカニズムをサポートしています。GRANT`または`REVOKE`コマンドを使用することで、テーブルの特定の列に対する`SELECT`、`INSERT`、`UPDATE`、および`REFERENCES`権限を付与または取り消すことができ、よりきめ細かなアクセス制御を実現できます。
---

# 列レベルの権限管理 {#column-level-privilege-management}

バージョン 8.5.6 以降、TiDB は MySQL と互換性のある列レベルの権限管理メカニズムをサポートしています。列レベルの権限を使用すると、指定したテーブルの特定の列に対して`SELECT` 、 `INSERT` `UPDATE` 、および`REFERENCES`権限を付与または取り消すことができ、よりきめ細かなデータアクセス制御を実現できます。

> **注記：**
>
> MySQLの構文では`REFERENCES(col_name)`のような列レベルの構文が使用できますが、 `REFERENCES`自体は外部キー関連の権限チェックに使用されるデータベースレベルまたはテーブルレベルの権限です。そのため、列レベルの`REFERENCES` MySQLでは実際の列レベルの権限効果を生み出しません。TiDBの動作はMySQLと一貫しています。

## 構文 {#syntax}

列レベルの権限を付与および取り消すための構文は、テーブルレベルの権限の構文と似ていますが、以下の点が異なります。

-   列名リストは**、テーブル名**の後ではなく、**権限タイプ**の後に記述してください。
-   複数の列名はカンマで区切られます（ `,` ）。

```sql
GRANT priv_type(col_name [, col_name] ...) [, priv_type(col_name [, col_name] ...)] ...
    ON db_name.tbl_name
    TO 'user'@'host';

REVOKE priv_type(col_name [, col_name] ...) [, priv_type(col_name [, col_name] ...)] ...
    ON db_name.tbl_name
    FROM 'user'@'host';
```

どこ：

-   `priv_type`は`SELECT` 、 `INSERT` 、 `UPDATE` 、および`REFERENCES` 。
-   `ON`句では、例えば`test.tbl`のようにテーブルを指定する必要があります。
-   単一の`GRANT`または`REVOKE`ステートメントには、複数の特権項目を含めることができ、各特権項目は独自の列名のリストを指定できます。

例えば、次のステートメントは`SELECT`の`col1`に対する権限と、 `col2`の`UPDATE`の`col3`に対する権限をユーザーに付与します。

```sql
GRANT SELECT(col1, col2), UPDATE(col3) ON test.tbl TO 'user'@'host';
```

## 例：列レベルの権限を付与する {#example-grant-column-level-privileges}

次の例では、ユーザー`newuser`にテーブル`SELECT`内の`col1`および`col2`に対する`test.tbl`権限を付与し、同じユーザーに`UPDATE`に対する`col3`権限を付与します。

```sql
CREATE DATABASE IF NOT EXISTS test;
USE test;

DROP TABLE IF EXISTS tbl;
CREATE TABLE tbl (col1 INT, col2 INT, col3 INT);

DROP USER IF EXISTS 'newuser'@'%';
CREATE USER 'newuser'@'%';

GRANT SELECT(col1, col2), UPDATE(col3) ON test.tbl TO 'newuser'@'%';
SHOW GRANTS FOR 'newuser'@'%';
```

    +---------------------------------------------------------------------+
    | Grants for newuser@%                                                |
    +---------------------------------------------------------------------+
    | GRANT USAGE ON *.* TO 'newuser'@'%'                                 |
    | GRANT SELECT(col1, col2), UPDATE(col3) ON test.tbl TO 'newuser'@'%' |
    +---------------------------------------------------------------------+

`SHOW GRANTS`を使用する以外にも、 `INFORMATION_SCHEMA.COLUMN_PRIVILEGES`クエリすることで列レベルの権限情報を表示することもできます。

## 例：列レベルの権限を取り消す {#example-revoke-column-level-privileges}

次の例は、ユーザー`SELECT`から列`col2`に対する`newuser`権限を取り消します。

```sql
REVOKE SELECT(col2) ON test.tbl FROM 'newuser'@'%';
SHOW GRANTS FOR 'newuser'@'%';
```

    +---------------------------------------------------------------+
    | Grants for newuser@%                                          |
    +---------------------------------------------------------------+
    | GRANT USAGE ON *.* TO 'newuser'@'%'                           |
    | GRANT SELECT(col1), UPDATE(col3) ON test.tbl TO 'newuser'@'%' |
    +---------------------------------------------------------------+

## 例：列レベルの権限アクセス制御 {#example-column-level-privilege-access-control}

列レベルの権限を付与または取り消した後、TiDB は SQL ステートメントで参照されている列に対して権限チェックを実行します。例:

-   `SELECT`ステートメント: `SELECT`列の権限は、 `SELECT`リストで参照される列、および`WHERE` 、 `ORDER BY` 、その他の句に影響します。
-   `UPDATE`ステートメント: `SET`句で更新される列には`UPDATE`列権限が必要です。式または条件で読み込まれる列には、通常、 `SELECT`列権限も必要です。
-   `INSERT`ステートメント: `INSERT`列の権限を必要とする列が書き込まれます。 `INSERT INTO t VALUES (...)`テーブル定義の順序ですべての列に値を書き込むことと同じです。

次の例では、ユーザー`newuser`は`col1`を照会し、 `col3`を更新することしかできません。

```sql
-- Execute as newuser
SELECT col1 FROM tbl;
SELECT * FROM tbl; -- Error (missing SELECT column privilege for col2, col3)

UPDATE tbl SET col3 = 1;
UPDATE tbl SET col1 = 2; -- Error (missing UPDATE column privilege for col1)

UPDATE tbl SET col3 = col1;
UPDATE tbl SET col3 = col3 + 1; -- Error (missing SELECT column privilege for col3)
UPDATE tbl SET col3 = col1 WHERE col1 > 0;
```

## MySQLとの互換性の違い {#compatibility-differences-with-mysql}

TiDBの列レベルの権限は、一般的にMySQLと互換性があります。ただし、以下のシナリオでは違いがあります。

| シナリオ                      | TiDB                                                                                                              | MySQL                                                                                                                       |
| :------------------------ | :---------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------- |
| ユーザーに付与されていない列レベルの権限を取り消す | `REVOKE`が正常に実行されました。                                                                                              | `IF EXISTS`が使用されていない場合、 `REVOKE`はエラーを返します。                                                                                  |
| 列の削除と`SELECT`権限チェックの実行順序  | `SELECT`列の権限は、列の削除前にチェックされます。たとえば、 `SELECT a FROM (SELECT a, b FROM t) s`を実行するには、 `SELECT`と`t.a`の両方に対して`t.b`列の権限。 | `SELECT`列の権限がチェックされる前に、カラムのプルーニングが実行されます。たとえば、 `SELECT a FROM (SELECT a, b FROM t) s`を実行するには、 `SELECT`に対する`t.a`列の権限のみが必要です。 |

### ビューシナリオにおけるカラムの削除と権限チェック {#column-pruning-and-privilege-checks-in-view-scenarios}

ビューに対して`SELECT`権限チェックを実行する場合、MySQLとTiDBでは以下の点が異なります。

-   MySQLはまずビューの内部クエリ内の列を削除し、次に内部テーブルの列権限をチェックするため、状況によってはチェックが比較的緩やかになる場合があります。
-   TiDBは権限チェックの前に列の削除を行わないため、追加の列権限が必要になる場合があります。

```sql
-- Prepare the environment by logging in as root
DROP USER IF EXISTS 'u'@'%';
CREATE USER 'u'@'%';

DROP TABLE IF EXISTS t;
CREATE TABLE t (a INT, b INT, c INT, d INT);

DROP VIEW IF EXISTS v;
CREATE SQL SECURITY INVOKER VIEW v AS SELECT a, b FROM t WHERE c = 0 ORDER BY d;

GRANT SELECT ON v TO 'u'@'%';

-- Log in as u
SELECT a FROM v;
-- MySQL: Error, missing access privileges for t.a, t.c, t.d
-- TiDB: Error, missing access privileges for t.a, t.b, t.c, t.d

-- Log in as root
GRANT SELECT(a, c, d) ON t TO 'u'@'%';

-- Log in as u
SELECT a FROM v;
-- MySQL: Success (internal query is pruned to `SELECT a FROM t WHERE c = 0 ORDER BY d`)
-- TiDB: Error, missing access privileges for t.b

SELECT * FROM v;
-- MySQL: Error, missing access privileges for t.b
-- TiDB: Error, missing access privileges for t.b

-- Log in as root
GRANT SELECT(b) ON t TO 'u'@'%';

-- Log in as u
SELECT * FROM v;
-- MySQL: Success
-- TiDB: Success
```

## 関連項目 {#see-also}

-   [権限管理](/privilege-management.md)
-   [`GRANT &#x3C;privileges>`](/sql-statements/sql-statement-grant-privileges.md)
-   [`REVOKE &#x3C;privileges>`](/sql-statements/sql-statement-revoke-privileges.md)
