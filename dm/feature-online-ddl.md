---
title: Migrate from Databases that Use GH-ost/PT-osc
summary: This document introduces the `online-ddl/online-ddl-scheme` feature of DM.
---

# GH-ost/PT-oscを使用するデータベースからの移行 {#migrate-from-databases-that-use-gh-ost-pt-osc}

本番シナリオでは、DDL実行中のテーブルロックにより、データベースからの読み取りまたはデータベースへの書き込みがある程度ブロックされる可能性があります。したがって、オンラインDDLツールは、読み取りと書き込みへの影響を最小限に抑えるためにDDLを実行するためによく使用されます。一般的なDDLツールは[幽霊](https://github.com/github/gh-ost)と[pt-osc](https://www.percona.com/doc/percona-toolkit/3.0/pt-online-schema-change.html)です。

DMを使用してMySQLからTiDBにデータを移行する場合、online-ddlをエンベールして、DMとgh-ostまたはpt-oscのコラボレーションを可能にすることができます。 online-ddlを有効にする方法と、このオプションを有効にした後のワークフローの詳細については、 [gh-ostまたはpt-oscを使用した連続レプリケーション](/migrate-with-pt-ghost.md)を参照してください。このドキュメントでは、DMツールとオンラインDDLツールのコラボレーションの詳細に焦点を当てています。

## オンラインDDLツールを使用したDMの作業の詳細 {#working-details-for-dm-with-online-ddl-tools}

このセクションでは、online-schema-changeを実装する際のオンラインDDLツール[幽霊](https://github.com/github/gh-ost)および[pt-osc](https://www.percona.com/doc/percona-toolkit/3.0/pt-online-schema-change.html)を使用したDMの作業の詳細について説明します。

### online-schema-change：gh-ost {#online-schema-change-gh-ost}

gh-ostがonline-schema-changeを実装すると、次の3種類のテーブルが作成されます。

-   gho：DDLを適用するために使用されます。データが完全に複製され、ghoテーブルがoriginテーブルと一致している場合、originテーブルは名前の変更によって置き換えられます。
-   ghc：online-schema-changeに関連する情報を格納するために使用されます。
-   del：オリジンテーブルの名前を変更して作成されます。

移行の過程で、DMは上記のテーブルを3つのカテゴリに分類します。

-   ghostTable： `_*_gho`
-   `_*_del` ： `_*_ghc`
-   realTable：online-ddlを実行するオリジンテーブル。

gh-ostで主に使用されるSQLステートメントとそれに対応するDMの操作は次のとおりです。

1.  `_ghc`のテーブルを作成します。

    ```sql
    Create /* gh-ost */ table `test`.`_test4_ghc` (
                            id bigint auto_increment,
                            last_update timestamp not null DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                            hint varchar(64) charset ascii not null,
                            value varchar(4096) charset ascii not null,
                            primary key(id),
                            unique key hint_uidx(hint)
                    ) auto_increment=256 ;
    ```

    DMは`_test4_ghc`のテーブルを作成しません。

2.  `_gho`のテーブルを作成します。

    ```sql
    Create /* gh-ost */ table `test`.`_test4_gho` like `test`.`test4` ;
    ```

    DMは`_test4_gho`のテーブルを作成しません。 DMは、 `ghost_schema` 、および`ghost_table` of `server_id` `dm_worker` 、ダウンストリームの`dm_meta.{task_name}_onlineddl`レコードを削除し、メモリ内の関連情報をクリアします。

    ```
    DELETE FROM dm_meta.{task_name}_onlineddl WHERE id = {server_id} and ghost_schema = {ghost_schema} and ghost_table = {ghost_table};
    ```

3.  `_gho`のテーブルで実行する必要のあるDDLを適用します。

    ```sql
    Alter /* gh-ost */ table `test`.`_test4_gho` add column cl1 varchar(20) not null ;
    ```

    DMは`_test4_gho`のDDL操作を実行しません。このDDLを`dm_meta.{task_name}_onlineddl`とメモリに記録します。

    ```sql
    REPLACE INTO dm_meta.{task_name}_onlineddl (id, ghost_schema , ghost_table , ddls) VALUES (......);
    ```

4.  `_ghc`のテーブルにデータを書き込み、元のテーブルのデータを`_gho`のテーブルに複製します。

    ```sql
    INSERT /* gh-ost */ INTO `test`.`_test4_ghc` VALUES (......);
    INSERT /* gh-ost `test`.`test4` */ ignore INTO `test`.`_test4_gho` (`id`, `date`, `account_id`, `conversion_price`, `ocpc_matched_conversions`, `ad_cost`, `cl2`)
      (SELECT `id`, `date`, `account_id`, `conversion_price`, `ocpc_matched_conversions`, `ad_cost`, `cl2` FROM `test`.`test4` FORCE INDEX (`PRIMARY`)
        WHERE (((`id` > _binary'1') OR ((`id` = _binary'1'))) AND ((`id` < _binary'2') OR ((`id` = _binary'2')))) lock IN share mode
      )   ;
    ```

    DMは、 **realtable**用ではないDMLステートメントを実行しません。

5.  移行が完了すると、元のテーブルと`_gho`のテーブルの両方の名前が変更され、オンラインDDL操作が完了します。

    ```sql
    Rename /* gh-ost */ table `test`.`test4` to `test`.`_test4_del`, `test`.`_test4_gho` to `test`.`test4`;
    ```

    DMは、次の2つの操作を実行します。

    -   DMは、上記の`rename`つの操作を2つのSQLステートメントに分割します。

        ```sql
        rename test.test4 to test._test4_del;
        rename test._test4_gho to test.test4;
        ```

    -   DMは`rename to _test4_del`を実行しません。 `rename ghost_table to origin table`を実行する場合、DMは次の手順を実行します。

        -   手順3でメモリに記録されたDDLを読み取ります
        -   `ghost_table`と`ghost_schema`を`origin_table`とそれに対応するスキーマに置き換えます
        -   置き換えられたDDLを実行します

        ```sql
        alter table test._test4_gho add column cl1 varchar(20) not null;
        -- Replaced with:
        alter table test.test4 add column cl1 varchar(20) not null;
        ```

> **ノート：**
>
> gh-ostの特定のSQLステートメントは、実行で使用されるパラメーターによって異なります。このドキュメントには、主要なSQLステートメントのみが記載されています。詳細については、 [gh-ostドキュメント](https://github.com/github/gh-ost#gh-ost)を参照してください。

## online-schema-change：pt {#online-schema-change-pt}

pt-oscがonline-schema-changeを実装すると、次の2種類のテーブルが作成されます。

-   `new` ：DDLを適用するために使用されます。データが完全に複製され、 `new`テーブルが元のテーブルと一致する場合、元のテーブルは名前の変更によって置き換えられます。
-   `old` ：オリジンテーブルの名前を変更して作成されます。
-   `pt_osc_*_upd`種類のトリガー`pt_osc_*_del` `pt_osc_*_ins` 。 pt_oscのプロセスで、オリジンテーブルによって生成された新しいデータがトリガーによって`new`に複製されます。

移行の過程で、DMは上記のテーブルを3つのカテゴリに分類します。

-   ghostTable： `_*_new`
-   trashTable： `_*_old`
-   realTable：online-ddlを実行するオリジンテーブル。

pt-oscで主に使用されるSQLステートメントとそれに対応するDMの操作は次のとおりです。

1.  `_new`のテーブルを作成します。

    ```sql
    CREATE TABLE `test`.`_test4_new` ( id int(11) NOT NULL AUTO_INCREMENT,
    date date DEFAULT NULL, account_id bigint(20) DEFAULT NULL, conversion_price decimal(20,3) DEFAULT NULL,  ocpc_matched_conversions bigint(20) DEFAULT NULL, ad_cost decimal(20,3) DEFAULT NULL,cl2 varchar(20) COLLATE utf8mb4_bin NOT NULL,cl1 varchar(20) COLLATE utf8mb4_bin NOT NULL,PRIMARY KEY (id) ) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ;
    ```

    DMは`_test4_new`のテーブルを作成しません。 DMは、 `ghost_schema` 、および`ghost_table` of `server_id` `dm_worker` 、ダウンストリームの`dm_meta.{task_name}_onlineddl`レコードを削除し、メモリ内の関連情報をクリアします。

    ```sql
    DELETE FROM dm_meta.{task_name}_onlineddl WHERE id = {server_id} and ghost_schema = {ghost_schema} and ghost_table = {ghost_table};
    ```

2.  `_new`のテーブルでDDLを実行します。

    ```sql
    ALTER TABLE `test`.`_test4_new` add column c3 int;
    ```

    DMは`_test4_new`のDDL操作を実行しません。代わりに、このDDLを`dm_meta.{task_name}_onlineddl`とメモリに記録します。

    ```sql
    REPLACE INTO dm_meta.{task_name}_onlineddl (id, ghost_schema , ghost_table , ddls) VALUES (......);
    ```

3.  データ移行に使用する3つのトリガーを作成します。

    ```sql
    CREATE TRIGGER `pt_osc_test_test4_del` AFTER DELETE ON `test`.`test4` ...... ;
    CREATE TRIGGER `pt_osc_test_test4_upd` AFTER UPDATE ON `test`.`test4` ...... ;
    CREATE TRIGGER `pt_osc_test_test4_ins` AFTER INSERT ON `test`.`test4` ...... ;
    ```

    DMは、TiDBでサポートされていないトリガー操作を実行しません。

4.  元のテーブルデータを`_new`のテーブルに複製します。

    ```sql
    INSERT LOW_PRIORITY IGNORE INTO `test`.`_test4_new` (`id`, `date`, `account_id`, `conversion_price`, `ocpc_matched_conversions`, `ad_cost`, `cl2`, `cl1`) SELECT `id`, `date`, `account_id`, `conversion_price`, `ocpc_matched_conversions`, `ad_cost`, `cl2`, `cl1` FROM `test`.`test4` LOCK IN SHARE MODE /*pt-online-schema-change 3227 copy table*/
    ```

    DMは、 **realtable**用ではないDMLステートメントを実行しません。

5.  データ移行が完了すると、元のテーブルと`_new`のテーブルの名前が変更され、オンラインDDL操作が完了します。

    ```sql
    RENAME TABLE `test`.`test4` TO `test`.`_test4_old`, `test`.`_test4_new` TO `test`.`test4`
    ```

    DMは、次の2つの操作を実行します。

    -   DMは、上記の`rename`つの操作を2つのSQLステートメントに分割します。

        ```sql
         rename test.test4 to test._test4_old;
         rename test._test4_new to test.test4;
        ```

    -   DMは`rename to _test4_old`を実行しません。 `rename ghost_table to origin table`を実行する場合、DMは次の手順を実行します。

        -   手順2でメモリに記録されたDDLを読み取ります
        -   `ghost_table`と`ghost_schema`を`origin_table`とそれに対応するスキーマに置き換えます
        -   置き換えられたDDLを実行します

        ```sql
        ALTER TABLE `test`.`_test4_new` add column c3 int;
        -- Replaced with:
        ALTER TABLE `test`.`test4` add column c3 int;
        ```

6.  オンラインDDL操作の`_old`のテーブルと3つのトリガーを削除します。

    ```sql
    DROP TABLE IF EXISTS `test`.`_test4_old`;
    DROP TRIGGER IF EXISTS `pt_osc_test_test4_del` AFTER DELETE ON `test`.`test4` ...... ;
    DROP TRIGGER IF EXISTS `pt_osc_test_test4_upd` AFTER UPDATE ON `test`.`test4` ...... ;
    DROP TRIGGER IF EXISTS `pt_osc_test_test4_ins` AFTER INSERT ON `test`.`test4` ...... ;
    ```

    DMは`_test4_old`とトリガーを削除しません。

> **ノート：**
>
> pt-oscの特定のSQLステートメントは、実行で使用されるパラメーターによって異なります。このドキュメントには、主要なSQLステートメントのみが記載されています。詳細については、 [pt-oscドキュメント](https://www.percona.com/doc/percona-toolkit/2.2/pt-online-schema-change.html)を参照してください。

## その他のオンラインスキーマ変更ツール {#other-online-schema-change-tools}

場合によっては、オンラインスキーマ変更ツールのデフォルトの動作を変更する必要があります。たとえば、 `ghost table`と`trash table`にカスタマイズされた名前を使用できます。それ以外の場合は、gh-ostやpt-oscの代わりに、同じ動作原理と変更プロセスで他のツールを使用することをお勧めします。

このようなカスタマイズされたニーズを実現するには、 `ghost table`と`trash table`の名前に一致する正規表現を作成する必要があります。

v2.0.7以降、DMは変更されたオンラインスキーマ変更ツールを実験的にサポートします。 DMタスク構成で`online-ddl=true`を設定し、 `shadow-table-rules`と`trash-table-rules`を構成することにより、変更された一時テーブルを正規表現と一致させることができます。

たとえば、 `ghost table`の名前が`_{origin_table}_pcnew`で`trash table`の名前が`_{origin_table}_pcold`のカスタマイズされたpt-oscを使用する場合、カスタムルールを次のように設定できます。

```yaml
online-ddl: true
shadow-table-rules: ["^_(.+)_(?:pcnew)$"]
trash-table-rules: ["^_(.+)_(?:pcold)$"]
```
