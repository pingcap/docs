---
title: 権限
summary: 権限とは、ある操作を実行するための許可です。ユーザーが {{{ .lake }}} 内で特定の操作を実行するには、対応する権限が必要です。たとえば、テーブルをクエリするには、そのテーブルに対する SELECT 権限が必要です。同様に、stage 内のデータセットを読み取るには、READ 権限が必要です。
---

# 権限

権限とは、ある操作を実行するための許可です。ユーザーが {{{ .lake }}} 内で特定の操作を実行するには、対応する権限が必要です。たとえば、テーブルをクエリするには、そのテーブルに対する `SELECT` 権限が必要です。同様に、stage 内のデータセットを読み取るには、`READ` 権限が必要です。

{{{ .lake }}} では、権限はロールに付与されます。ユーザーは、自身に割り当てられたロールを通じて権限を取得します。

![Alt text](/media/tidb-cloud-lake/access-control-2.png)

## 権限の管理 {#managing-privileges}

ロールの権限を管理するには、次のコマンドを使用します。

- [GRANT](/tidb-cloud-lake/sql/grant.md)
- [REVOKE](/tidb-cloud-lake/sql/revoke.md)
- [SHOW GRANTS](/tidb-cloud-lake/sql/show-grants.md)

### ロールへの権限の付与 {#granting-privileges-to-roles}

権限を付与するには、ロールを作成し、そのロールに権限を付与してから、その権限を必要とするユーザーにそのロールを付与します。次の例では、`writer` という名前の新しいロールを作成し、`default` スキーマ内のオブジェクトに対するすべての権限を付与しています。続いて、パスワード `abc123` を持つ新しいユーザー `david` を作成し、`writer` ロールを `david` に付与します。最後に、`writer` に付与された権限を表示します。

```sql title='Example:'
-- Create a new role named 'writer'
CREATE ROLE writer;

-- Grant all privileges on all objects in the 'default' schema to the role 'writer'
GRANT ALL ON default.* TO ROLE writer;

-- Create a new user named 'david' with the password 'abc123' and set the default role
CREATE USER david IDENTIFIED BY 'abc123' WITH DEFAULT_ROLE = 'writer';

-- Grant the role 'writer' to the user 'david'
GRANT ROLE writer TO david;

-- Show the granted privileges for the role 'writer'
SHOW GRANTS FOR ROLE writer;

┌───────────────────────────────────────────────────────┐
│                      Grants                           │
├───────────────────────────────────────────────────────┤
│ GRANT ALL ON 'default'.'default'.* TO ROLE 'writer'   │
└───────────────────────────────────────────────────────┘
```

### ロールからの権限の取り消し {#revoking-privileges-from-roles}

アクセス制御の文脈では、権限はロールから取り消されます。次の例では、`default` スキーマ内のすべてのオブジェクトに対するすべての権限を `writer` ロールから取り消し、その後 `writer` ロールに付与されている権限を表示します。

```sql title='Example (Continued):'
-- Revoke all privileges on all objects in the 'default' schema from role 'writer'
REVOKE ALL ON default.* FROM ROLE writer;

-- Show the granted privileges for the role 'writer'
SHOW GRANTS FOR ROLE writer;
```

## アクセス制御の権限 {#access-control-privileges}

{{{ .lake }}} では、データベースオブジェクトに対してきめ細かな制御を行うためのさまざまな権限が提供されています。{{{ .lake }}} の権限は、次の種類に分類できます。

- グローバル権限: この権限セットには、システム内の特定のオブジェクトではなく、データベース管理システム全体に適用される権限が含まれます。グローバル権限では、データベースの作成や削除、ユーザーやロールの管理、システムレベル設定の変更など、データベース全体の機能や管理に影響する操作が許可されます。含まれる権限については、[グローバル権限](#global-privileges) を参照してください。

- オブジェクト固有の権限: オブジェクト固有の権限には複数のセットがあり、それぞれ特定のデータベースオブジェクトに適用されます。これには次が含まれます。
    - [テーブル権限](#table-privileges)
    - [ビュー権限](#view-privileges)
    - [データベース権限](#database-privileges)
    - [セッションポリシー権限](#session-policy-privileges)
    - [stage 権限](#stage-privileges)
    - [UDF 権限](#udf-privileges)
    - [シーケンス権限](#sequence-privileges)
    - [Connection 権限](#connection-privileges)
    - [Procedure 権限](#procedure-privileges)
    - [Catalog 権限](#catalog-privileges)
    - [Share 権限](#share-privileges)

### すべての権限 {#all-privileges}

| 権限         | オブジェクトタイプ                   | 説明                                                                                                                                        |
|:------------------|:------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------|
| ALL               | すべて                           | 指定したオブジェクトタイプに対するすべての権限を付与します。                                                                                           |
| APPLY MASKING POLICY | Global, Masking Policy     | マスキングポリシーのアタッチ、デタッチ、記述、または削除を行います。*.* に対して付与された場合、被付与者は任意のマスキングポリシーを管理できます。                          |
| APPLY ROW ACCESS POLICY | Global, Row Access Policy | テーブルに行アクセスポリシーを追加または削除し、任意のポリシーに対する DESCRIBE/DROP 操作を許可します。*.* に対して付与された場合、被付与者はすべての行アクセスポリシーを管理できます。 |
| ALTER             | Global, Database, Table, View | データベース、テーブル、ユーザー、または UDF を変更します。                                                                                                             |
| CREATE            | Global, Table                 | テーブルまたは UDF を作成します。                                                                                                                            |
| CREATE DATABASE   | Global                        | データベースまたは UDF を作成します。                                                                                                                         |
| CREATE WAREHOUSE  | Global                        | Warehouse を作成します。                                                                                                                               |
| CREATE CONNECTION | Global                        | 接続を作成します。                                                                                                                              |
| CREATE SEQUENCE   | Global                        | シーケンスを作成します。                                                                                                                                |
| CREATE PROCEDURE  | PROCEDURE                     | プロシージャを作成します。                                                                                                                               |
| CREATE MASKING POLICY | Global                    | マスキングポリシーを作成します。                                                                                                                          |
| CREATE ROW ACCESS POLICY | Global                 | 行アクセスポリシーを作成します。                                                                                                                       |
| DELETE            | Table                         | テーブル内の行を削除または切り捨てます。                                                                                                              |
| DROP              | Global, Database, Table, View | データベース、テーブル、ビュー、または UDF を削除します。テーブルの削除取り消しも行います。                                                                                             |
| INSERT            | Table                         | テーブルに行を挿入します。                                                                                                                         |
| SELECT            | Database, Table               | テーブルから行を選択します。データベースを表示または使用します。                                                                                               |
| UPDATE            | Table                         | テーブル内の行を更新します。                                                                                                                           |
| GRANT             | Global                        | ロールに対して権限を付与 / 取り消しします。                                                                                                      |
| SUPER             | Global, Table                 | クエリを強制終了します。グローバル設定を設定します。テーブルを最適化します。テーブルを分析します。stage（stage の一覧表示、作成、削除）、catalog、または share を操作します。 |
| USAGE             | Global                        | 「権限なし」の同義語です。                                                                                                                       |
| CREATE ROLE       | Global                        | ロールを作成します。                                                                                                                                    |
| DROP ROLE         | Global                        | ロールを削除します。                                                                                                                                      |
| CREATE USER       | Global                        | SQL ユーザーを作成します。                                                                                                                                |
| DROP USER         | Global                        | SQL ユーザーを削除します。                                                                                                                                  |
| WRITE             | Stage                         | stage に書き込みます。                                                                                                                                |
| READ              | Stage                         | stage を読み取ります。                                                                                                                                      |
| USAGE             | UDF                           | udf を使用します。                                                                                                                                           |
| ACCESS CONNECTION | CONNECTION                    | 接続にアクセスします。                                                                                                                                 |
| ACCESS SEQUENCE   | SEQUENCE                      | シーケンスにアクセスします。                                                                                                                                   |
| ACCESS PROCEDURE  | PROCEDURE                     | プロシージャにアクセスします。                                                                                                                                  |

### グローバル権限 {#global-privileges}

| 権限         | 説明                                                                                                       |
|:------------------|:------------------------------------------------------------------------------------------------------------------|
| ALL               | 指定したオブジェクトタイプに対するすべての権限を付与します。                                                          |
| ALTER             | テーブルカラムを追加または削除します。クラスターキーを変更します。テーブルを再クラスタリングします。                                          |
| CREATEROLE        | ロールを作成します。                                                                                                   |
| CREAT DATABASE    | DATABASE を作成します。                                                                                               |
| CREATE WAREHOUSE  | WAREHOUSE を作成します。                                                                                              |
| CREATE CONNECTION | CONNECTION を作成します。                                                                                             |
| DROPUSER          | ユーザーを削除します。                                                                                                     |
| CREATEUSER        | ユーザーを作成します。                                                                                                   |
| DROPROLE          | ロールを削除します。                                                                                                     |
| SUPER             | クエリを強制終了します。設定を有効化または無効化します。stage、catalog、または share を操作します。関数を呼び出します。stage への COPY INTO を実行します。 |
| USAGE             | {{{ .lake }}} のクエリにのみ接続します。                                                                             |
| CREATE            | UDF を作成します。                                                                                                    |
| DROP              | UDF を削除します。                                                                                                      |
| ALTER             | UDF を変更します。SQL ユーザーを変更します。                                                                                  |

### テーブル権限 {#table-privileges}

| 権限 | 説明                                                                                                      |
|:----------|:-----------------------------------------------------------------------------------------------------------------|
| ALL       | 指定したオブジェクトタイプに対するすべての権限を付与します。                                                         |
| ALTER     | テーブルカラムを追加または削除します。クラスターキーを変更します。テーブルを再クラスタリングします。                                         |
| CREATE    | テーブルを作成します。                                                                                                 |
| DELETE    | テーブル内の行を削除します。テーブルを切り捨てます。                                                                      |
| DROP      | テーブルを削除または削除取り消しします。削除されたテーブルの最新バージョンを復元します。                                        |
| INSERT    | テーブルに行を挿入します。テーブルへの COPY INTO を実行します。                                                                    |
| SELECT    | テーブルから行を選択します。テーブルの SHOW CREATE を実行します。テーブルの DESCRIBE を実行します。                                                |
| UPDATE    | テーブル内の行を更新します。                                                                                         |
| SUPER     | テーブルを最適化または分析します。                                                                                   |
| OWNERSHIP | データベースに対する完全な制御を付与します。特定のオブジェクトに対して、この権限を同時に保持できるロールは 1 つだけです。 |

### ビュー権限 {#view-privileges}

| 権限 | 説明                                                            |
|:----------|:-----------------------------------------------------------------------|
| ALL       | 指定したオブジェクトタイプに対するすべての権限を付与します                |
| ALTER     | ビューを作成または削除します。別の QUERY を使用して既存のビューを変更します。 |
| DROP      | ビューを削除します。                                                          |

### データベース権限 {#database-privileges}

次のいずれかの権限をデータベースに対して持っている場合、またはそのデータベース内のテーブルに対する何らかの権限を持っている場合は、[USE DATABASE](/tidb-cloud-lake/sql/use-database.md) コマンドを使用してデータベースを指定できます。

| 権限 | 説明                                                                                                      |
|:----------|:-----------------------------------------------------------------------------------------------------------------|
| ALTER     | データベース名を変更します。                                                                                              |
| DROP      | データベースを削除または削除取り消しします。削除されたデータベースの最新バージョンを復元します。                                  |
| SELECT    | データベースの SHOW CREATE を実行します。                                                                                          |
| OWNERSHIP | データベースに対する完全な制御を付与します。特定のオブジェクトに対して、この権限を同時に保持できるロールは 1 つだけです。 |
| USAGE     | 含まれるオブジェクトへのアクセス権を付与せずに、`USE <database>` を使用してデータベースに入ることを許可します。             |

> Note:
>
> 1. ロールがデータベースを所有している場合、そのロールはそのデータベース内のすべてのテーブルにアクセスできます。

### セッションポリシー権限 {#session-policy-privileges}

| 権限 | 説明 |
| :--                 | :--                  |
| SUPER       |    クエリを強制終了します。設定を有効化または無効化します。 |
| ALL   |  指定したオブジェクトタイプに対するすべての権限を付与します。 |

### stage 権限 {#stage-privileges}

| 権限 | 説明                                                                                                   |
|:----------|:--------------------------------------------------------------------------------------------------------------|
| WRITE     | stage に書き込みます。たとえば、stage への copy、presign upload、または stage の削除を行います。                         |
| READ      | stage を読み取ります。たとえば、stage の一覧表示、stage のクエリ、stage からテーブルへの copy、presign download を行います。              |
| ALL       | 指定したオブジェクトタイプに対する READ、WRITE 権限を付与します。                                                  |
| OWNERSHIP | stage に対する完全な制御を付与します。特定のオブジェクトに対して、この権限を同時に保持できるロールは 1 つだけです。 |

> Note:
>
> 1. 外部ロケーション認証は確認しません。

### UDF 権限 {#udf-privileges}

| Privilege | 説明                                                                                                 |
|:----------|:-----------------------------------------------------------------------------------------------------|
| USAGE     | UDF を使用できます。たとえば、stage への copy や presign upload です。                               |
| ALL       | 指定したオブジェクトタイプに対する READ、WRITE 権限を付与します。                                   |
| OWNERSHIP | UDF に対する完全な制御を付与します。特定のオブジェクトに対して、この権限を同時に保持できるロールは 1 つだけです。 |

> Note:
>
> 1. すでに定数畳み込みされている場合は、udf auth をチェックしません。
> 2. insert 内の値である場合は、udf auth をチェックしません。

### Catalog 権限 {#catalog-privileges}

| Privilege | 説明                                              |
|:----------|:--------------------------------------------------|
| SUPER     | SHOW CREATE catalog を実行できます。catalog を作成または削除できます。 |
| ALL       | 指定したオブジェクトタイプに対するすべての権限を付与します。 |

### Share 権限 {#share-privileges}

Share オブジェクトに対する権限は、同じ SQL 権限モデル（`GRANT`/`REVOKE`）を使用して付与および取り消しできます。

### Connection 権限 {#connection-privileges}

| 権限              | 説明                                                                                                         |
|:------------------|:-------------------------------------------------------------------------------------------------------------|
| Access Connection | Connection にアクセスできます。                                                                              |
| ALL               | 指定したオブジェクトタイプに対する Access Connection 権限を付与します。                                      |
| OWNERSHIP         | Connection に対する完全な制御を付与します。特定のオブジェクトに対して、この権限を同時に保持できるロールは 1 つだけです。 |

### シーケンス権限 {#sequence-privileges}

| 権限            | 説明                                                                                                      |
|:----------------|:----------------------------------------------------------------------------------------------------------|
| Access Sequence | シーケンスにアクセスできます（例: Drop、Desc）。                                                         |
| ALL             | 指定したオブジェクトタイプに対する Access Sequence 権限を付与します。                                     |
| OWNERSHIP       | シーケンスに対する完全な制御を付与します。特定のオブジェクトに対して、この権限を同時に保持できるロールは 1 つだけです。 |

### Procedure 権限 {#procedure-privileges}

| 権限             | 説明                                                                                                       |
|:-----------------|:-----------------------------------------------------------------------------------------------------------|
| Access Procedure | Procedure にアクセスできます（例: Drop、Call、Desc）。                                                     |
| ALL              | 指定したオブジェクトタイプに対する Access Procedure 権限を付与します。                                     |
| OWNERSHIP        | Procedure に対する完全な制御を付与します。特定のオブジェクトに対して、この権限を同時に保持できるロールは 1 つだけです。 |

### Masking Policy 権限 {#masking-policy-privileges}

グローバルな `CREATE MASKING POLICY` 権限および `APPLY MASKING POLICY` 権限に加えて、個々の masking policy へのアクセスを付与できます。

| Privilege | 説明                                                                                                                           |
|:----------|:--------------------------------------------------------------------------------------------------------------------------------|
| APPLY     | masking policy をカラムにアタッチまたはデタッチし、policy に対する DESC/DROP 操作を許可します。                                |
| OWNERSHIP | masking policy に対する完全な制御を付与します。{{{ .lake }}} は、policy を作成したロールに OWNERSHIP を付与し、policy が削除されると自動的に取り消します。 |

### Row Access Policy 権限 {#row-access-policy-privileges}

Row access policy は同じガバナンスモデルを共有します。グローバルな `CREATE ROW ACCESS POLICY` 権限および `APPLY ROW ACCESS POLICY` 権限に加えて、必要に応じて policy ごとにアクセスを付与します。

| Privilege | 説明                                                                                                                                        |
|:----------|:-----------------------------------------------------------------------------------------------------------------------------------------------|
| APPLY     | row access policy をテーブルに追加またはテーブルから削除し、policy に対する DESC/DROP 操作を許可します。                                     |
| OWNERSHIP | row access policy に対する完全な制御を付与します。{{{ .lake }}} は、作成者ロールに OWNERSHIP を付与し、policy が削除されると自動的に取り消します。 |