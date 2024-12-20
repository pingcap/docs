---
title: GBK
summary: このドキュメントでは、GBK 文字セットの TiDB サポートについて詳しく説明します。
---

# イギリス {#gbk}

v5.4.0 以降、TiDB は GBK 文字セットをサポートしています。このドキュメントでは、TiDB の GBK 文字セットのサポートと互換性に関する情報を提供します。

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

## MySQL 互換性 {#mysql-compatibility}

このセクションでは、MySQL と TiDB 間の互換性に関する情報を提供します。

### 照合順序 {#collations}

MySQL の GBK 文字セットのデフォルトの照合照合順序は`gbk_chinese_ci`です。MySQL とは異なり、TiDB の GBK 文字セットのデフォルトの照合照合順序は`gbk_bin`です。また、TiDB は GBK を UTF8MB4 に変換してからバイナリ照合順序を使用するため、TiDB の`gbk_bin`照合順序は MySQL の`gbk_bin`照合順序と同じではありません。

<CustomContent platform="tidb">

TiDB を MySQL GBK 文字セットの照合順序と互換性を持たせるには、最初に TiDB クラスターを初期化するときに、TiDB オプション[`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)を`true`に設定して[照合のための新しいフレームワーク](/character-set-and-collation.md#new-framework-for-collations)を有効にする必要があります。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB を MySQL GBK 文字セットの照合順序と互換性を持たせるために、TiDB クラスターを最初に初期化するときに、 TiDB Cloud はデフォルトで[照合のための新しいフレームワーク](/character-set-and-collation.md#new-framework-for-collations)有効にします。

</CustomContent>

照合の新しいフレームワークを有効にした後、GBK 文字セットに対応する照合を確認すると、TiDB GBK のデフォルトの照合順序が`gbk_chinese_ci`に変更されていることがわかります。

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

-   システム変数[`character_set_client`](/system-variables.md#character_set_client)と[`character_set_connection`](/system-variables.md#character_set_connection)同時に`gbk`に設定されていない場合、TiDB は MySQL と同じ方法で不正な文字を処理します。
-   `character_set_client`と`character_set_connection`両方が`gbk`に設定されている場合、TiDB は不正な文字を MySQL とは異なる方法で処理します。

    -   MySQL は、読み取り操作と書き込み操作で不正な GBK 文字セットを異なる方法で処理します。
    -   TiDB は、読み取り操作と書き込み操作で不正な GBK 文字セットを同じ方法で処理します。SQL 厳密モードでは、不正な GBK 文字の読み取りまたは書き込みを行うと、TiDB はエラーを報告します。非厳密モードでは、不正な GBK 文字の読み取りまたは書き込みを行うと、TiDB は不正な GBK 文字を`?`に置き換えます。

例えば、 `SET NAMES gbk`後に、 MySQL と TiDB でそれぞれ`CREATE TABLE gbk_table(a VARCHAR(32) CHARACTER SET gbk)`ステートメントを使用してテーブルを作成し、次の表の SQL ステートメントを実行すると、詳細な違いを確認できます。

| データベース   | 設定されたSQLモードに`STRICT_ALL_TABLES`または`STRICT_TRANS_TABLES`含まれている場合                                                   | 設定されたSQLモードに`STRICT_ALL_TABLES`も`STRICT_TRANS_TABLES`含まれていない場合                                                                       |
| -------- | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| マイグレーション | `SELECT HEX('一a');`<br/> `e4b88061`<br/><br/> `INSERT INTO gbk_table values('一a');`<br/> `Incorrect Error`        | `SELECT HEX('一a');`<br/> `e4b88061`<br/><br/> `INSERT INTO gbk_table VALUES('一a');`<br/> `SELECT HEX(a) FROM gbk_table;`<br/> `e4b8` |
| ティビ      | `SELECT HEX('一a');`<br/> `Incorrect Error`<br/><br/> `INSERT INTO gbk_table VALUES('一a');`<br/> `Incorrect Error` | `SELECT HEX('一a');`<br/> `e4b83f`<br/><br/> `INSERT INTO gbk_table VALUES('一a');`<br/> `SELECT HEX(a) FROM gbk_table;`<br/> `e4b83f` |

上記の表では、 `utf8mb4`バイト セットの`SELECT HEX('a');`の結果は`e4b88061`なります。

### その他のMySQL互換性 {#other-mysql-compatibility}

-   現在、TiDB は、 `ALTER TABLE`ステートメントを使用して他の文字セット タイプを`gbk`に変換したり、 `gbk`を他の文字セット タイプに変換したりすることはサポートしていません。

<!---->

-   TiDB は`_gbk`の使用をサポートしていません。例:

    ```sql
    CREATE TABLE t(a CHAR(10) CHARSET BINARY);
    Query OK, 0 rows affected (0.00 sec)
    INSERT INTO t VALUES (_gbk'啊');
    ERROR 1115 (42000): Unsupported character introducer: 'gbk'
    ```

<!---->

-   現在、 `ENUM`および`SET`タイプのバイナリ文字については、TiDB は`utf8mb4`文字セットとして処理します。

## コンポーネントの互換性 {#component-compatibility}

-   現在、 TiFlash はGBK 文字セットをサポートしていません。

-   TiDB データ移行 (DM) は、v5.4.0 より前の TiDB クラスターへの`charset=GBK`テーブルの移行をサポートしていません。

-   TiDB Lightning は、 v5.4.0 より前の TiDB クラスターへの`charset=GBK`のテーブルのインポートをサポートしていません。

-   v6.1.0 より前のバージョンの TiCDC では、 `charset=GBK`テーブルのレプリケーションはサポートされていません。v6.1.0 より前のバージョンの TiCDC では、 `charset=GBK`テーブルの TiDB クラスターへのレプリケーションはサポートされていません。

-   v5.4.0 より前のバージョンのバックアップと復元 (BR) では、 `charset=GBK`テーブルの復元はサポートされていません。v5.4.0 より前のバージョンのBRでは、 `charset=GBK`テーブルの TiDB クラスターへの復元はサポートされていません。
