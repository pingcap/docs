---
title: GBK
summary: This document provides details about the TiDB support of the GBK character set.
---

# GBK {#gbk}

v5.4.0以降、TiDBはGBK文字セットをサポートしています。このドキュメントは、GBK文字セットのTiDBサポートと互換性情報を提供します。

```sql
SHOW CHARACTER SET WHERE CHARSET = 'gbk';
+---------+-------------------------------------+-------------------+--------+
| Charset | Description                         | Default collation | Maxlen |
+---------+-------------------------------------+-------------------+--------+
| gbk     | Chinese Internal Code Specification | gbk_bin           |      2 |
+---------+-------------------------------------+-------------------+--------+
1 row in set (0.00 sec)

SHOW COLLATION WHERE CHARSET = 'gbk';
+----------------+---------+------+---------+----------+---------+
| Collation      | Charset | Id   | Default | Compiled | Sortlen |
+----------------+---------+------+---------+----------+---------+
| gbk_bin        | gbk     |   87 |         | Yes      |       1 |
+----------------+---------+------+---------+----------+---------+
1 rows in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このセクションでは、MySQLとTiDB間の互換性情報を提供します。

### 照合 {#collations}

MySQLのGBK文字セットのデフォルトの照合順序は`gbk_chinese_ci`です。 MySQLとは異なり、TiDBのGBK文字セットのデフォルトの照合順序は`gbk_bin`です。さらに、TiDBはGBKをUTF8MB4に変換してから、バイナリ照合順序を使用するため、TiDBの`gbk_bin`照合順序はMySQLの`gbk_bin`照合順序と同じではありません。

TiDBをMySQLGBK文字セットの照合と互換性を持たせるには、最初にTiDBクラスタを初期化するときに、TiDBオプション[`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)から`true`を設定して[照合のための新しいフレームワーク](/character-set-and-collation.md#new-framework-for-collations)を有効にする必要があります。

照合用の新しいフレームワークを有効にした後、GBK文字セットに対応する照合を確認すると、TiDBGBKのデフォルトの照合順序が`gbk_chinese_ci`に変更されていることがわかります。

```sql
SHOW CHARACTER SET WHERE CHARSET = 'gbk';
+---------+-------------------------------------+-------------------+--------+
| Charset | Description                         | Default collation | Maxlen |
+---------+-------------------------------------+-------------------+--------+
| gbk     | Chinese Internal Code Specification | gbk_chinese_ci    |      2 |
+---------+-------------------------------------+-------------------+--------+
1 row in set (0.00 sec)

SHOW COLLATION WHERE CHARSET = 'gbk';
+----------------+---------+------+---------+----------+---------+
| Collation      | Charset | Id   | Default | Compiled | Sortlen |
+----------------+---------+------+---------+----------+---------+
| gbk_bin        | gbk     |   87 |         | Yes      |       1 |
| gbk_chinese_ci | gbk     |   28 | Yes     | Yes      |       1 |
+----------------+---------+------+---------+----------+---------+
2 rows in set (0.00 sec)
```

### 不正な文字の互換性 {#illegal-character-compatibility}

-   システム変数[`character_set_client`](/system-variables.md#character_set_client)と[`character_set_connection`](/system-variables.md#character_set_connection)が同時に`gbk`に設定されていない場合、TiDBはMySQLと同じ方法で不正な文字を処理します。
-   `character_set_client`と`character_set_connection`の両方が`gbk`に設定されている場合、TiDBはMySQLとは異なる方法で不正な文字を処理します。

    -   MySQLは、読み取り操作と書き込み操作で不正なGBK文字セットを異なる方法で処理します。
    -   TiDBは、読み取りおよび書き込み操作で不正なGBK文字セットを同じ方法で処理します。 SQL strictモードでは、不正なGBK文字の読み取りまたは書き込み時にTiDBがエラーを報告します。非厳密モードでは、TiDBは、不正なGBK文字の読み取りまたは書き込み時に、不正なGBK文字を`?`に置き換えます。

たとえば、 `SET NAMES gbk`の後に、MySQLとTiDBでそれぞれ`CREATE TABLE gbk_table(a VARCHAR(32) CHARACTER SET gbk)`ステートメントを使用してテーブルを作成し、次のテーブルのSQLステートメントを実行すると、詳細な違いを確認できます。

| データベース | 構成されたSQLモードに`STRICT_ALL_TABLES`または`STRICT_TRANS_TABLES`が含まれている場合                                                  | 構成されたSQLモードに`STRICT_ALL_TABLES`も`STRICT_TRANS_TABLES`も含まれていない場合                                                                      |
| ------ | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| MySQL  | `SELECT HEX('一a');`<br/> `e4b88061`<br/><br/> `INSERT INTO gbk_table values('一a');`<br/> `Incorrect Error`        | `SELECT HEX('一a');`<br/> `e4b88061`<br/><br/> `INSERT INTO gbk_table VALUES('一a');`<br/> `SELECT HEX(a) FROM gbk_table;`<br/> `e4b8` |
| TiDB   | `SELECT HEX('一a');`<br/> `Incorrect Error`<br/><br/> `INSERT INTO gbk_table VALUES('一a');`<br/> `Incorrect Error` | `SELECT HEX('一a');`<br/> `e4b83f`<br/><br/> `INSERT INTO gbk_table VALUES('一a');`<br/> `SELECT HEX(a) FROM gbk_table;`<br/> `e4b83f` |

上記の表では、 `utf8mb4`バイトセットの`SELECT HEX('a');`の結果は`e4b88061`です。

### その他のMySQL互換性 {#other-mysql-compatibility}

-   現在、TiDBは、 `ALTER TABLE`ステートメントを使用して他の文字セットタイプを`gbk`に変換したり、 `gbk`から他の文字セットタイプに変換したりすることをサポートしていません。

-   TiDBは`_gbk`の使用をサポートしていません。例えば：

    ```sql
    CREATE TABLE t(a CHAR(10) CHARSET BINARY);
    Query OK, 0 rows affected (0.00 sec)
    INSERT INTO t VALUES (_gbk'啊');
    ERROR 1115 (42000): Unsupported character introducer: 'gbk'
    ```

-   現在、 `ENUM`および`SET`タイプのバイナリ文字の場合、TiDBはそれらを`utf8mb4`文字セットとして扱います。

## コンポーネントの互換性 {#component-compatibility}

-   現在、TiCDCとTiFlashはGBK文字セットをサポートしていません。

-   TiDBデータ移行（DM）は、v5.4.0より前のTiDBクラスターへの`charset=GBK`のテーブルの移行をサポートしていません。

-   TiDB Lightningは、v5.4.0より前のTiDBクラスターへの`charset=GBK`のテーブルのインポートをサポートしていません。

-   v5.4.0より前のバージョンのバックアップと復元（BR）は、 `charset=GBK`のテーブルのリカバリーをサポートしていません。 BRのどのバージョンも、v5.4.0より前のTiDBクラスターへの`charset=GBK`のテーブルのリカバリーをサポートしていません。
