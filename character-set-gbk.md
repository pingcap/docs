---
title: GBK
summary: This document provides details about the TiDB support of the GBK character set.
---

# GBK {#gbk}

v5.4.0 以降、TiDB は GBK 文字セットをサポートしています。このドキュメントでは、TiDB のサポートと GBK 文字セットの互換性に関する情報を提供します。

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

このセクションでは、MySQL と TiDB の間の互換性情報を提供します。

### 照合順序 {#collations}

MySQL の GBK 文字セットのデフォルトの照合順序は`gbk_chinese_ci`です。 MySQL とは異なり、TiDB の GBK 文字セットのデフォルトの照合順序は`gbk_bin`です。さらに、TiDB は GBK を UTF8MB4 に変換し、バイナリ照合順序を使用するため、TiDB の`gbk_bin`照合順序は MySQL の`gbk_bin`照合順序と同じではありません。

<CustomContent platform="tidb">

TiDB を MySQL GBK 文字セットの照合順序と互換性を持たせるには、最初に TiDB クラスターを初期化するときに、TiDB オプション[`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)から`true`を設定して[照合順序の新しいフレームワーク](/character-set-and-collation.md#new-framework-for-collations)を有効にする必要があります。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB を MySQL GBK 文字セットの照合順序と互換にするために、最初に TiDB クラスターを初期化するときに、 TiDB Cloud はデフォルトで[照合順序の新しいフレームワーク](/character-set-and-collation.md#new-framework-for-collations)を有効にします。

</CustomContent>

新しいフレームワークの照合順序を有効にした後、GBK 文字セットに対応する照合順序を確認すると、TiDB GBK のデフォルトの照合順序が`gbk_chinese_ci`に変更されていることがわかります。

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

-   システム変数[`character_set_client`](/system-variables.md#character_set_client)と[`character_set_connection`](/system-variables.md#character_set_connection)が同時に`gbk`に設定されていない場合、TiDB は MySQL と同じ方法で不正な文字を処理します。
-   `character_set_client`と`character_set_connection`が両方とも`gbk`に設定されている場合、TiDB は MySQL とは異なる方法で不正な文字を処理します。

    -   MySQL は、読み取り操作と書き込み操作で不正な GBK 文字セットを別々に処理します。
    -   TiDB は、読み取りおよび書き込み操作において不正な GBK 文字セットを同じ方法で処理します。 SQL 厳密モードでは、TiDB は不正な GBK 文字の読み取りまたは書き込み時にエラーを報告します。非厳密モードでは、TiDB は、不正な GBK 文字の読み取りまたは書き込み時に、不正な GBK 文字を`?`に置き換えます。

たとえば、 `SET NAMES gbk`の後、MySQL と TiDB でそれぞれ`CREATE TABLE gbk_table(a VARCHAR(32) CHARACTER SET gbk)`ステートメントを使用してテーブルを作成し、次の表の SQL ステートメントを実行すると、詳細な違いがわかります。

| データベース | 設定された SQL モードに`STRICT_ALL_TABLES`または`STRICT_TRANS_TABLES`が含まれている場合                                                | 設定された SQL モードに`STRICT_ALL_TABLES`も`STRICT_TRANS_TABLES`含まれていない場合                                                                     |
| ------ | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| MySQL  | `SELECT HEX('一a');`<br/> `e4b88061`<br/><br/> `INSERT INTO gbk_table values('一a');`<br/> `Incorrect Error`        | `SELECT HEX('一a');`<br/> `e4b88061`<br/><br/> `INSERT INTO gbk_table VALUES('一a');`<br/> `SELECT HEX(a) FROM gbk_table;`<br/> `e4b8` |
| TiDB   | `SELECT HEX('一a');`<br/> `Incorrect Error`<br/><br/> `INSERT INTO gbk_table VALUES('一a');`<br/> `Incorrect Error` | `SELECT HEX('一a');`<br/> `e4b83f`<br/><br/> `INSERT INTO gbk_table VALUES('一a');`<br/> `SELECT HEX(a) FROM gbk_table;`<br/> `e4b83f` |

上の表では、 `utf8mb4`バイト セットの`SELECT HEX('a');`の結果は`e4b88061`です。

### その他の MySQL との互換性 {#other-mysql-compatibility}

-   現在、TiDB は、 `ALTER TABLE`ステートメントを使用して他のキャラクタ セット タイプを`gbk` 、または`gbk`から他のキャラクタ セット タイプに変換することをサポートしていません。

<!---->

-   TiDB は`_gbk`の使用をサポートしていません。例えば：

    ```sql
    CREATE TABLE t(a CHAR(10) CHARSET BINARY);
    Query OK, 0 rows affected (0.00 sec)
    INSERT INTO t VALUES (_gbk'啊');
    ERROR 1115 (42000): Unsupported character introducer: 'gbk'
    ```

<!---->

-   現在、TiDB では`ENUM`および`SET`タイプのバイナリ文字を`utf8mb4`文字セットとして扱います。

-   述語に`LIKE 'prefix%'`などの文字列接頭辞の`LIKE`が含まれており、ターゲット列が GBK照合順序( `gbk_bin`または`gbk_chinese_ci` ) に設定されている場合、オプティマイザーは現在、この述語を範囲スキャンに変換できません。代わりに、フルスキャンが実行されます。その結果、このような SQL クエリは予期しないリソースの消費につながる可能性があります。

## コンポーネントの互換性 {#component-compatibility}

-   現在、 TiFlash はGBK 文字セットをサポートしていません。

-   TiDB データ移行 (DM) は、v5.4.0 より前の TiDB クラスターへの`charset=GBK`テーブルの移行をサポートしていません。

-   TiDB Lightning は、 v5.4.0 より前の TiDB クラスターへの`charset=GBK`テーブルのインポートをサポートしていません。

-   v6.1.0 より前の TiCDC バージョンは、 `charset=GBK`テーブルの複製をサポートしていません。 v6.1.0 より前のバージョンの TiCDC は、TiDB クラスターへの`charset=GBK`テーブルのレプリケートをサポートしていません。

-   v5.4.0 より前のバックアップ &amp; リストア (BR) バージョンは、 `charset=GBK`テーブルのリカバリをサポートしていません。 v5.4.0 より前のバージョンのBR は、 TiDB クラスターへの`charset=GBK`テーブルのリカバリをサポートしていません。
