---
title: GBK
summary: このドキュメントでは、GBK 文字セットの TiDB サポートについて詳しく説明します。
---

# GBK {#gbk}

TiDBはv5.4.0以降、GBK文字セットをサポートしています。このドキュメントでは、TiDBのGBK文字セットのサポートと互換性に関する情報を提供します。

TiDB v6.0.0以降、デフォルトで[照合のための新しいフレームワーク](/character-set-and-collation.md#new-framework-for-collations)有効になります。TiDB GBK文字セットのデフォルトの照合照合順序は`gbk_chinese_ci`で、これはMySQLと一致しています。

```sql
SHOW CHARACTER SET WHERE CHARSET = 'gbk';
```

    +---------+-------------------------------------+-------------------+--------+
    | Charset | Description                         | Default collation | Maxlen |
    +---------+-------------------------------------+-------------------+--------+
    | gbk     | Chinese Internal Code Specification | gbk_chinese_ci    |      2 |
    +---------+-------------------------------------+-------------------+--------+
    1 row in set (0.00 sec)

```sql
SHOW COLLATION WHERE CHARSET = 'gbk';
```

    +----------------+---------+----+---------+----------+---------+---------------+
    | Collation      | Charset | Id | Default | Compiled | Sortlen | Pad_attribute |
    +----------------+---------+----+---------+----------+---------+---------------+
    | gbk_bin        | gbk     | 87 |         | Yes      |       1 | PAD SPACE     |
    | gbk_chinese_ci | gbk     | 28 | Yes     | Yes      |       1 | PAD SPACE     |
    +----------------+---------+----+---------+----------+---------+---------------+
    2 rows in set (0.00 sec)

## MySQLの互換性 {#mysql-compatibility}

このセクションでは、MySQL と TiDB 間の互換性に関する情報を提供します。

### 照合順序 {#collations}

<CustomContent platform="tidb">

MySQLにおけるGBK文字セットのデフォルトの照合照合順序は`gbk_chinese_ci`です。TiDBにおけるGBK文字セットのデフォルトの照合照合順序は、TiDB設定項目[`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)の値によって異なります。

-   デフォルトでは、 TiDB 構成項目[`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)は`true`に設定されています。つまり、 [照合のための新しいフレームワーク](/character-set-and-collation.md#new-framework-for-collations)が有効になっており、 GBK 文字セットのデフォルトの照合照合順序は`gbk_chinese_ci`です。
-   TiDB 構成項目[`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) `false`に設定されている場合、 [照合のための新しいフレームワーク](/character-set-and-collation.md#new-framework-for-collations)は無効になり、 GBK 文字セットのデフォルトの照合順序は`gbk_bin`になります。

</CustomContent>

<CustomContent platform="tidb-cloud">

デフォルトでは、 TiDB Cloud は[照合のための新しいフレームワーク](/character-set-and-collation.md#new-framework-for-collations)を有効にし、GBK 文字セットのデフォルトの照合順序は`gbk_chinese_ci`です。

</CustomContent>

さらに、TiDB は GBK を`utf8mb4`に変換してからバイナリ照合順序を使用するため、TiDB の`gbk_bin`照合順序はMySQL の`gbk_bin`照合順序と同じではありません。

### 無効な文字互換性 {#invalid-character-compatibility}

-   システム変数[`character_set_client`](/system-variables.md#character_set_client)と[`character_set_connection`](/system-variables.md#character_set_connection)同時に`gbk`に設定されていない場合、TiDB は MySQL と同じ方法で無効な文字を処理します。
-   `character_set_client`と`character_set_connection`両方が`gbk`に設定されている場合、TiDB は無効な文字を MySQL とは異なる方法で処理します。

    -   MySQL は、読み取り操作と書き込み操作で無効な GBK 文字セットを異なる方法で処理します。
    -   TiDBは、読み取り操作と書き込み操作の両方において、無効なGBK文字セットを同じ方法で処理します。SQL厳密モードでは、無効なGBK文字の読み取りまたは書き込み時にエラーが報告されます。非厳密モードでは、無効なGBK文字の読み取りまたは書き込み時に、TiDBは無効なGBK文字を`?`に置き換えます。

例えば、 `SET NAMES gbk`後、 MySQL と TiDB でそれぞれ`CREATE TABLE gbk_table(a VARCHAR(32) CHARACTER SET gbk)`ステートメントを使用してテーブルを作成し、次の表の SQL ステートメントを実行すると、詳細な違いを確認できます。

| データベース | 設定されたSQLモードに`STRICT_ALL_TABLES`または`STRICT_TRANS_TABLES`が含まれている場合                                                  | 設定されたSQLモードに`STRICT_ALL_TABLES`も`STRICT_TRANS_TABLES`も含まれていない場合                                                                     |
| ------ | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| MySQL  | `SELECT HEX('一a');` <br/> `e4b88061`<br/><br/>`INSERT INTO gbk_table values('一a');`<br/> `Incorrect Error`        | `SELECT HEX('一a');` <br/> `e4b88061`<br/><br/>`INSERT INTO gbk_table VALUES('一a');`<br/>`SELECT HEX(a) FROM gbk_table;`<br/> `e4b8` |
| ティドブ   | `SELECT HEX('一a');` <br/> `Incorrect Error`<br/><br/>`INSERT INTO gbk_table VALUES('一a');`<br/> `Incorrect Error` | `SELECT HEX('一a');` <br/> `e4b83f`<br/><br/>`INSERT INTO gbk_table VALUES('一a');`<br/>`SELECT HEX(a) FROM gbk_table;`<br/> `e4b83f` |

上記の表では、 `utf8mb4`バイト セットの`SELECT HEX('a');`の結果は`e4b88061`なります。

### その他のMySQL互換性 {#other-mysql-compatibility}

-   現在、TiDB は、 `ALTER TABLE`ステートメントを使用して他の文字セット タイプを`gbk`に変換したり、 `gbk`を他の文字セット タイプに変換したりすることはサポートしていません。

<!---->

-   TiDBは`_gbk`の使用をサポートしていません。例:

    ```sql
    CREATE TABLE t(a CHAR(10) CHARSET BINARY);
    Query OK, 0 rows affected (0.00 sec)
    INSERT INTO t VALUES (_gbk'啊');
    ```

        ERROR 1115 (42000): Unsupported character introducer: 'gbk'

<!---->

-   現在、 `ENUM`および`SET`タイプのバイナリ文字については、TiDB は`utf8mb4`文字セットとして処理します。

## コンポーネントの互換性 {#component-compatibility}

-   現在、 TiFlash はGBK 文字セットをサポートしていません。

-   TiDB データ移行 (DM) では、 `charset=GBK`テーブルを v5.4.0 より前の TiDB クラスターに移行することはサポートされていません。

-   TiDB Lightning は、v5.4.0 より前の TiDB クラスターへの`charset=GBK`テーブルのインポートをサポートしていません。

-   TiCDC v6.1.0より前のバージョンでは、 `charset=GBK`テーブルのレプリケーションはサポートされていません。v6.1.0より前のバージョンのTiCDCでは、TiDBクラスターへの`charset=GBK`テーブルのレプリケーションはサポートされていません。

-   バックアップ＆リストア（BR）バージョン5.4.0より前のバージョンでは、 `charset=GBK`テーブルのリカバリはサポートされていません。また、 BRのバージョン5.4.0より前のバージョンでは、TiDBクラスターへの`charset=GBK`テーブルのリカバリはサポートされていません。

## 参照 {#see-also}

-   [`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md)
-   [文字セットと照合順序](/character-set-and-collation.md)
