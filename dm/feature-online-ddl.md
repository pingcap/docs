---
title: Migrate from Databases that Use GH-ost/PT-osc
summary: データベースのオンライン DDL ツールであるGH-ostとpt-oscを使用して、DDL実行中のテーブルロックによる影響を最小限に抑えながら、MySQLからTiDBにデータを移行することができます。DMは、これらのツールとの連携を許可し、移行プロセスを詳細に分類します。また、カスタマイズされたオンラインスキーマ変更ツールを実験的にサポートし、正規表現を使用して一時テーブルの名前を照合できます。
---

# GH-ost/PT-osc を使用するデータベースからの移行 {#migrate-from-databases-that-use-gh-ost-pt-osc}

本番シナリオでは、DDL 実行中のテーブル ロックにより、データベースへの読み取りまたは書き込みがある程度ブロックされる可能性があります。したがって、読み取りと書き込みへの影響を最小限に抑えるために、オンライン DDL ツールを使用して DDL を実行することがよくあります。一般的な DDL ツールは[おばけ](https://github.com/github/gh-ost)と[pt-osc](https://www.percona.com/doc/percona-toolkit/3.0/pt-online-schema-change.html)です。

DM を使用して MySQL から TiDB にデータを移行する場合、online-ddl を有効にして、DM と gh-ost または pt-osc のコラボレーションを許可できます。 online-ddl を有効にする方法と、このオプションを有効にした後のワークフローの詳細については、 [gh-ost または pt-osc による継続的レプリケーション](/migrate-with-pt-ghost.md)を参照してください。このドキュメントでは、DM とオンライン DDL ツールのコラボレーションの詳細に焦点を当てます。

## オンライン DDL ツールを使用した DM の動作の詳細 {#working-details-for-dm-with-online-ddl-tools}

このセクションでは、online-schema-change を実装する場合のオンライン DDL ツール[おばけ](https://github.com/github/gh-ost)および[pt-osc](https://www.percona.com/doc/percona-toolkit/3.0/pt-online-schema-change.html)を使用した DM の動作の詳細について説明します。

## オンラインスキーマ変更: gh-ost {#online-schema-change-gh-ost}

gh-ost が online-schema-change を実装すると、3 種類のテーブルが作成されます。

-   gho: DDL を適用するために使用されます。データが完全にレプリケートされ、gho テーブルが元のテーブルと一貫性がある場合、元のテーブルは名前変更によって置き換えられます。
-   ghc: online-schema-change に関連する情報を保存するために使用されます。
-   del: 元のテーブルの名前を変更して作成されます。

移行の過程で、DM は上記のテーブルを 3 つのカテゴリに分類します。

-   ゴーストテーブル: `_*_gho`
-   ゴミテーブル: `_*_ghc` 、 `_*_del`
-   realTable: online-ddl を実行する元のテーブル。

gh-ost で主に使用される SQL ステートメントと、それに対応する DM の操作は次のとおりです。

1.  `_ghc`テーブルを作成します。

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

    DM は`_test4_ghc`テーブルを作成しません。

2.  `_gho`テーブルを作成します。

    ```sql
    Create /* gh-ost */ table `test`.`_test4_gho` like `test`.`test4` ;
    ```

    DM は`_test4_gho`テーブルを作成しません。 DM は、 `ghost_table`の`ghost_schema` 、および`server_id`に従って、ダウン`dm_worker`の`dm_meta.{task_name}_onlineddl`レコードを削除し、メモリ内の関連情報をクリアします。

        DELETE FROM dm_meta.{task_name}_onlineddl WHERE id = {server_id} and ghost_schema = {ghost_schema} and ghost_table = {ghost_table};

3.  `_gho`テーブルで実行する必要がある DDL を適用します。

    ```sql
    Alter /* gh-ost */ table `test`.`_test4_gho` add column cl1 varchar(20) not null ;
    ```

    DM は`_test4_gho`の DDL 操作を実行しません。この DDL を`dm_meta.{task_name}_onlineddl`とメモリに記録します。

    ```sql
    REPLACE INTO dm_meta.{task_name}_onlineddl (id, ghost_schema , ghost_table , ddls) VALUES (......);
    ```

4.  データを`_ghc`テーブルに書き込み、元のテーブルのデータを`_gho`テーブルにレプリケートします。

    ```sql
    INSERT /* gh-ost */ INTO `test`.`_test4_ghc` VALUES (......);
    INSERT /* gh-ost `test`.`test4` */ ignore INTO `test`.`_test4_gho` (`id`, `date`, `account_id`, `conversion_price`, `ocpc_matched_conversions`, `ad_cost`, `cl2`)
      (SELECT `id`, `date`, `account_id`, `conversion_price`, `ocpc_matched_conversions`, `ad_cost`, `cl2` FROM `test`.`test4` FORCE INDEX (`PRIMARY`)
        WHERE (((`id` > _binary'1') OR ((`id` = _binary'1'))) AND ((`id` < _binary'2') OR ((`id` = _binary'2')))) lock IN share mode
      )   ;
    ```

    DM は、 **realtable**用ではない DML ステートメントを実行しません。

5.  移行が完了すると、元のテーブルと`_gho`テーブルの両方の名前が変更され、オンライン DDL 操作が完了します。

    ```sql
    Rename /* gh-ost */ table `test`.`test4` to `test`.`_test4_del`, `test`.`_test4_gho` to `test`.`test4`;
    ```

    DM は次の 2 つの操作を実行します。

    -   DM は、上記の`rename`操作を 2 つの SQL ステートメントに分割します。

        ```sql
        rename test.test4 to test._test4_del;
        rename test._test4_gho to test.test4;
        ```

    -   DM は実行されません`rename to _test4_del` 。 `rename ghost_table to origin table`を実行すると、DM は次の手順を実行します。

        -   ステップ 3 でメモリに記録された DDL を読み取ります。
        -   `ghost_table`と`ghost_schema` `origin_table`とそれに対応するスキーマに置き換えます。
        -   置き換えられたDDLを実行する

        ```sql
        alter table test._test4_gho add column cl1 varchar(20) not null;
        -- Replaced with:
        alter table test.test4 add column cl1 varchar(20) not null;
        ```

> **注記：**
>
> gh-ost の特定の SQL ステートメントは、実行時に使用されるパラメータによって異なります。このドキュメントでは、主要な SQL ステートメントのみをリストします。詳細については、 [gh-ost ドキュメント](https://github.com/github/gh-ost#gh-ost)を参照してください。

## オンラインスキーマ変更: ポイント {#online-schema-change-pt}

pt-osc が online-schema-change を実装すると、2 種類のテーブルが作成されます。

-   `new` : DDL の適用に使用されます。データが完全にレプリケートされ、 `new`テーブルが元のテーブルと一貫性がある場合、元のテーブルは名前変更によって置き換えられます。
-   `old` : 元のテーブルの名前を変更して作成されます。
-   トリガーは`pt_osc_*_ins` 、 `pt_osc_*_upd` 、 `pt_osc_*_del`の 3 種類。 pt_osc のプロセスでは、元のテーブルによって生成された新しいデータがトリガーによって`new`に複製されます。

移行の過程で、DM は上記のテーブルを 3 つのカテゴリに分類します。

-   ゴーストテーブル: `_*_new`
-   ゴミテーブル: `_*_old`
-   realTable: online-ddl を実行する元のテーブル。

pt-osc で主に使用される SQL ステートメントと、それに対応する DM の操作は次のとおりです。

1.  `_new`テーブルを作成します。

    ```sql
    CREATE TABLE `test`.`_test4_new` ( id int(11) NOT NULL AUTO_INCREMENT,
    date date DEFAULT NULL, account_id bigint(20) DEFAULT NULL, conversion_price decimal(20,3) DEFAULT NULL, ocpc_matched_conversions bigint(20) DEFAULT NULL, ad_cost decimal(20,3) DEFAULT NULL,cl2 varchar(20) COLLATE utf8mb4_bin NOT NULL,cl1 varchar(20) COLLATE utf8mb4_bin NOT NULL,PRIMARY KEY (id) ) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ;
    ```

    DM は`_test4_new`テーブルを作成しません。 DM は、 `ghost_table`の`ghost_schema` 、および`server_id`に従って、ダウン`dm_worker`の`dm_meta.{task_name}_onlineddl`レコードを削除し、メモリ内の関連情報をクリアします。

    ```sql
    DELETE FROM dm_meta.{task_name}_onlineddl WHERE id = {server_id} and ghost_schema = {ghost_schema} and ghost_table = {ghost_table};
    ```

2.  `_new`テーブルで DDL を実行します。

    ```sql
    ALTER TABLE `test`.`_test4_new` add column c3 int;
    ```

    DM は`_test4_new`の DDL 操作を実行しません。代わりに、この DDL を`dm_meta.{task_name}_onlineddl`とメモリに記録します。

    ```sql
    REPLACE INTO dm_meta.{task_name}_onlineddl (id, ghost_schema , ghost_table , ddls) VALUES (......);
    ```

3.  データ移行に使用する 3 つのトリガーを作成します。

    ```sql
    CREATE TRIGGER `pt_osc_test_test4_del` AFTER DELETE ON `test`.`test4` ...... ;
    CREATE TRIGGER `pt_osc_test_test4_upd` AFTER UPDATE ON `test`.`test4` ...... ;
    CREATE TRIGGER `pt_osc_test_test4_ins` AFTER INSERT ON `test`.`test4` ...... ;
    ```

    DM は、TiDB でサポートされていないトリガー操作を実行しません。

4.  元のテーブルのデータを`_new`テーブルにレプリケートします。

    ```sql
    INSERT LOW_PRIORITY IGNORE INTO `test`.`_test4_new` (`id`, `date`, `account_id`, `conversion_price`, `ocpc_matched_conversions`, `ad_cost`, `cl2`, `cl1`) SELECT `id`, `date`, `account_id`, `conversion_price`, `ocpc_matched_conversions`, `ad_cost`, `cl2`, `cl1` FROM `test`.`test4` LOCK IN SHARE MODE /*pt-online-schema-change 3227 copy table*/
    ```

    DM は、 **realtable**用ではない DML ステートメントを実行しません。

5.  データ移行が完了すると、元のテーブルと`_new`テーブルの名前が変更され、オンライン DDL 操作が完了します。

    ```sql
    RENAME TABLE `test`.`test4` TO `test`.`_test4_old`, `test`.`_test4_new` TO `test`.`test4`
    ```

    DM は次の 2 つの操作を実行します。

    -   DM は、上記の`rename`操作を 2 つの SQL ステートメントに分割します。

        ```sql
        rename test.test4 to test._test4_old;
        rename test._test4_new to test.test4;
        ```

    -   DM は実行されません`rename to _test4_old` 。 `rename ghost_table to origin table`を実行すると、DM は次の手順を実行します。

        -   ステップ 2 でメモリに記録された DDL を読み取ります。
        -   `ghost_table`と`ghost_schema` `origin_table`とそれに対応するスキーマに置き換えます。
        -   置き換えられたDDLを実行する

        ```sql
        ALTER TABLE `test`.`_test4_new` add column c3 int;
        -- Replaced with:
        ALTER TABLE `test`.`test4` add column c3 int;
        ```

6.  オンライン DDL 操作の`_old`テーブルと 3 つのトリガーを削除します。

    ```sql
    DROP TABLE IF EXISTS `test`.`_test4_old`;
    DROP TRIGGER IF EXISTS `pt_osc_test_test4_del` AFTER DELETE ON `test`.`test4` ...... ;
    DROP TRIGGER IF EXISTS `pt_osc_test_test4_upd` AFTER UPDATE ON `test`.`test4` ...... ;
    DROP TRIGGER IF EXISTS `pt_osc_test_test4_ins` AFTER INSERT ON `test`.`test4` ...... ;
    ```

    DMは`_test4_old`とトリガーを削除しません。

> **注記：**
>
> pt-osc の特定の SQL ステートメントは、実行時に使用されるパラメーターによって異なります。このドキュメントでは、主要な SQL ステートメントのみをリストします。詳細については、 [pt-osc ドキュメント](https://www.percona.com/doc/percona-toolkit/2.2/pt-online-schema-change.html)を参照してください。

## その他のオンライン スキーマ変更ツール {#other-online-schema-change-tools}

場合によっては、オンライン スキーマ変更ツールのデフォルトの動作を変更する必要があるかもしれません。たとえば、 `ghost table`と`trash table`にカスタマイズした名前を使用できます。場合によっては、gh-ost や pt-osc の代わりに、同じ動作原則と変更プロセスを持つ他のツールを使用することもできます。

このようなカスタマイズされたニーズを実現するには、 `ghost table`と`trash table`の名前に一致する正規表現を作成する必要があります。

v2.0.7 以降、DM は、変更されたオンライン スキーマ変更ツールを実験的にサポートします。 DM タスク構成で`online-ddl=true`設定し、 `shadow-table-rules`および`trash-table-rules`を構成すると、変更された一時テーブルを正規表現と照合できます。

たとえば、 `ghost table`の名前が`_{origin_table}_pcnew` 、 `trash table`の名前が`_{origin_table}_pcold`であるカスタマイズされた pt-osc を使用する場合、カスタム ルールを次のように設定できます。

```yaml
online-ddl: true
shadow-table-rules: ["^_(.+)_(?:pcnew)$"]
trash-table-rules: ["^_(.+)_(?:pcold)$"]
```
