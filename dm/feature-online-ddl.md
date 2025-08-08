---
title: Migrate from Databases that Use GH-ost/PT-osc
summary: このドキュメントでは、DM の online-ddl/online-ddl-scheme` 機能について説明します。
---

# GH-ost/PT-osc を使用するデータベースからの移行 {#migrate-from-databases-that-use-gh-ost-pt-osc}

本番環境では、DDL実行中のテーブルロックによって、データベースからの読み取りまたは書き込みがある程度ブロックされる可能性があります。そのため、読み取りと書き込みへの影響を最小限に抑えるため、オンラインDDLツールを使用してDDLを実行することがよくあります。一般的なDDLツールは[おばけ](https://github.com/github/gh-ost)と[pt-osc](https://www.percona.com/doc/percona-toolkit/3.0/pt-online-schema-change.html)です。

DMを使用してMySQLからTiDBにデータを移行する場合、online-ddlを有効にすると、DMとgh-ostまたはpt-oscの連携が可能になります。online-ddlの有効化方法と、このオプション有効化後のワークフローの詳細については、 [gh-ost または pt-osc による継続的なレプリケーション](/migrate-with-pt-ghost.md)参照してください。このドキュメントでは、DMとオンラインDDLツールの連携の詳細に焦点を当てています。

## オンライン DDL ツールを使用した DM の動作詳細 {#working-details-for-dm-with-online-ddl-tools}

このセクションでは、オンライン スキーマ変更を実装する場合の、オンライン DDL ツール[おばけ](https://github.com/github/gh-ost)および[pt-osc](https://www.percona.com/doc/percona-toolkit/3.0/pt-online-schema-change.html)を使用した DM の動作の詳細について説明します。

## オンラインスキーマ変更: gh-ost {#online-schema-change-gh-ost}

gh-ost がオンライン スキーマ変更を実装すると、次の 3 種類のテーブルが作成されます。

-   gho: DDLの適用に使用されます。データが完全に複製され、ghoテーブルが元のテーブルと整合性が取れている場合、元のテーブルは名前変更によって置き換えられます。
-   ghc: オンライン スキーマ変更に関連する情報を保存するために使用されます。
-   del: 元のテーブルの名前を変更して作成されました。

移行プロセスでは、DM は上記のテーブルを 3 つのカテゴリに分割します。

-   ゴーストテーブル: `_*_gho`
-   ゴミ箱テーブル: `_*_ghc` , `_*_del`
-   realTable: online-ddl を実行する元のテーブル。

gh-ost で主に使用される SQL ステートメントとそれに対応する DM の操作は次のとおりです。

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

    DMは`_test4_gho`テーブルを作成しません。DMは`ghost_schema` 、および`dm_worker` `ghost_table` `server_id`に従って下流の`dm_meta.{task_name}_onlineddl`レコードを削除し、メモリ内の関連情報をクリアします。

        DELETE FROM dm_meta.{task_name}_onlineddl WHERE id = {server_id} and ghost_schema = {ghost_schema} and ghost_table = {ghost_table};

3.  `_gho`テーブルで実行する必要がある DDL を適用します。

    ```sql
    Alter /* gh-ost */ table `test`.`_test4_gho` add column cl1 varchar(20) not null ;
    ```

    DMは`_test4_gho`のDDL操作を実行しません。このDDLは`dm_meta.{task_name}_onlineddl`とメモリに記録されます。

    ```sql
    REPLACE INTO dm_meta.{task_name}_onlineddl (id, ghost_schema , ghost_table , ddls) VALUES (......);
    ```

4.  `_ghc`テーブルにデータを書き込み、元のテーブルのデータを`_gho`テーブルに複製します。

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

    -   DM は上記の`rename`操作を 2 つの SQL 文に分割します。

        ```sql
        rename test.test4 to test._test4_del;
        rename test._test4_gho to test.test4;
        ```

    -   DMは`rename to _test4_del`を実行しません。3 `rename ghost_table to origin table`実行する場合、DMは以下の手順を実行します。

        -   ステップ3でメモリに記録されたDDLを読み取ります
        -   `ghost_table`と`ghost_schema` `origin_table`とそれに対応するスキーマに置き換えます
        -   置き換えられたDDLを実行する

        ```sql
        alter table test._test4_gho add column cl1 varchar(20) not null;
        -- Replaced with:
        alter table test.test4 add column cl1 varchar(20) not null;
        ```

> **注記：**
>
> gh-ost の具体的なSQL文は、実行時に使用するパラメータによって異なります。このドキュメントでは主要なSQL文のみを記載しています。詳細については、 [gh-ost ドキュメント](https://github.com/github/gh-ost#gh-ost)を参照してください。

## オンラインスキーマ変更: pt {#online-schema-change-pt}

pt-osc がオンライン スキーマ変更を実装すると、次の 2 種類のテーブルが作成されます。

-   `new` : DDLの適用に使用されます。データが完全に複製され、 `new`テーブルが元のテーブルと整合性が取れている場合、元のテーブルは名前変更によって置き換えられます。
-   `old` : 元のテーブルの名前を変更して作成されました。
-   3種類`pt_osc_*_del`トリガー： `pt_osc_*_ins`のプロセスでは、元のテーブルで生成された新しいデータ`pt_osc_*_upd`トリガーによって`new`に複製されます。

移行プロセスでは、DM は上記のテーブルを 3 つのカテゴリに分割します。

-   ゴーストテーブル: `_*_new`
-   ゴミ箱テーブル: `_*_old`
-   realTable: online-ddl を実行する元のテーブル。

pt-osc で主に使用される SQL 文とそれに対応する DM の操作は次のとおりです。

1.  `_new`テーブルを作成します。

    ```sql
    CREATE TABLE `test`.`_test4_new` ( id int NOT NULL AUTO_INCREMENT,
    date date DEFAULT NULL, account_id bigint DEFAULT NULL, conversion_price decimal(20,3) DEFAULT NULL, ocpc_matched_conversions bigint DEFAULT NULL, ad_cost decimal(20,3) DEFAULT NULL,cl2 varchar(20) COLLATE utf8mb4_bin NOT NULL,cl1 varchar(20) COLLATE utf8mb4_bin NOT NULL,PRIMARY KEY (id) ) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ;
    ```

    DMは`_test4_new`テーブルを作成しません。DMは`ghost_schema` 、および`dm_worker` `ghost_table` `server_id`に従って下流の`dm_meta.{task_name}_onlineddl`レコードを削除し、メモリ内の関連情報をクリアします。

    ```sql
    DELETE FROM dm_meta.{task_name}_onlineddl WHERE id = {server_id} and ghost_schema = {ghost_schema} and ghost_table = {ghost_table};
    ```

2.  `_new`テーブルで DDL を実行します。

    ```sql
    ALTER TABLE `test`.`_test4_new` add column c3 int;
    ```

    DMは`_test4_new`のDDL操作を実行しません。代わりに、このDDLを`dm_meta.{task_name}_onlineddl`とメモリに記録します。

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

4.  元のテーブルのデータを`_new`テーブルに複製します。

    ```sql
    INSERT LOW_PRIORITY IGNORE INTO `test`.`_test4_new` (`id`, `date`, `account_id`, `conversion_price`, `ocpc_matched_conversions`, `ad_cost`, `cl2`, `cl1`) SELECT `id`, `date`, `account_id`, `conversion_price`, `ocpc_matched_conversions`, `ad_cost`, `cl2`, `cl1` FROM `test`.`test4` LOCK IN SHARE MODE /*pt-online-schema-change 3227 copy table*/
    ```

    DM は、 **realtable**用ではない DML ステートメントを実行しません。

5.  データ移行が完了すると、元のテーブルと`_new`テーブルの名前が変更され、オンライン DDL 操作が完了します。

    ```sql
    RENAME TABLE `test`.`test4` TO `test`.`_test4_old`, `test`.`_test4_new` TO `test`.`test4`
    ```

    DM は次の 2 つの操作を実行します。

    -   DM は上記の`rename`操作を 2 つの SQL 文に分割します。

        ```sql
        rename test.test4 to test._test4_old;
        rename test._test4_new to test.test4;
        ```

    -   DMは`rename to _test4_old`を実行しません。3 `rename ghost_table to origin table`実行する場合、DMは以下の手順を実行します。

        -   ステップ2でメモリに記録されたDDLを読み取ります
        -   `ghost_table`と`ghost_schema` `origin_table`とそれに対応するスキーマに置き換えます
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

    DM は`_test4_old`とトリガーを削除しません。

> **注記：**
>
> pt-osc の具体的なSQL文は、実行時に使用するパラメータによって異なります。このドキュメントでは主要なSQL文のみを記載しています。詳細については、 [pt-osc ドキュメント](https://www.percona.com/doc/percona-toolkit/2.2/pt-online-schema-change.html)を参照してください。

## その他のオンラインスキーマ変更ツール {#other-online-schema-change-tools}

場合によっては、オンラインスキーマ変更ツールのデフォルトの動作を変更する必要があるかもしれません。例えば、 `ghost table`と`trash table`にカスタマイズされた名前を使用する場合などです。また、gh-ost や pt-osc の代わりに、同じ動作原理と変更プロセスを持つ他のツールを使用する必要がある場合もあります。

このようなカスタマイズされたニーズを実現するには、 `ghost table`と`trash table`名前に一致する正規表現を記述する必要があります。

バージョン2.0.7以降、DMは改良されたオンラインスキーマ変更ツールを試験的にサポートしています。DMタスク設定で`online-ddl=true`設定し、 `shadow-table-rules`と`trash-table-rules`設定することで、変更された一時テーブルを正規表現で照合できます。

たとえば、 `ghost table`の名前が`_{origin_table}_pcnew` 、 `trash table`名前が`_{origin_table}_pcold`であるカスタマイズされた pt-osc を使用する場合、次のようにカスタム ルールを設定できます。

```yaml
online-ddl: true
shadow-table-rules: ["^_(.+)_(?:pcnew)$"]
trash-table-rules: ["^_(.+)_(?:pcold)$"]
```
