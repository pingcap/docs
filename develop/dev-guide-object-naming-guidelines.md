---
title: Object Naming Convention
summary: Learn the object naming convention in TiDB.
---

# オブジェクト命名規則 {#object-naming-convention}

このドキュメントでは、データベース、テーブル、インデックス、ユーザーなどのデータベース オブジェクトに名前を付ける規則を紹介します。

## 一般的なルール {#general-rules}

-   アンダースコアで区切られた意味のある英単語を使用することをお勧めします。
-   名前には文字、数字、アンダースコアのみを使用してください。
-   `group`や`order`などの TiDB 予約語を列名として使用しないでください。
-   すべてのデータベース オブジェクトに小文字を使用することをお勧めします。

## データベースの命名規則 {#database-naming-convention}

ビジネス、製品、またはその他の指標によってデータベース名を区別し、データベース名に 20 文字以内で使用することをお勧めします。たとえば、一時ライブラリに`tmp_crm` 、テスト ライブラリに`test_crm`という名前を付けることができます。

## テーブルの命名規則 {#table-naming-convention}

-   同じビジネスまたはモジュールのテーブルには同じプレフィックスを使用し、テーブル名ができるだけ自明であることを確認してください。
-   名前の単語はアンダースコアで区切ります。テーブル名には 32 文字以下を使用することをお勧めします。
-   理解を深めるために、表の目的に注釈を付けることをお勧めします。例えば：
    -   一時テーブル: `tmp_t_crm_relation_0425`
    -   バックアップテーブル: `bak_t_crm_relation_20170425`
    -   業務一時表： `tmp_st_{business code}_{creator abbreviation}_{date}`
    -   決算期： `t_crm_ec_record_YYYY{MM}{dd}`
-   異なるビジネス モジュールのテーブルに対して個別のデータベースを作成し、それに応じて注釈を追加します。

## カラムの命名規則 {#column-naming-convention}

-   列の命名は、列の実際の意味または省略形です。
-   同じ意味を持つテーブル間で同じ列名を使用することをお勧めします。
-   列に注釈を追加し、「0: オフライン、1: オンライン」などの列挙型に名前付きの値を指定することをお勧めします。
-   ブール列に`is_{description}`という名前を付けることをお勧めします。たとえば、メンバーが有効かどうかを示す`member`テーブルの列には、 `is_enabled`という名前を付けることができます。
-   列に 30 文字を超える名前を付けることはお勧めできません。また、列の数は 60 未満にする必要があります。
-   `order` 、 `from` 、 `desc`などの TiDB 予約語を列名として使用しないでください。キーワードが予約されているかどうかを確認するには、 [TiDB キーワード](/keywords.md)参照してください。

## インデックスの命名規則 {#index-naming-convention}

-   主キー インデックス: `pk_{table_name_abbreviation}_{field_name_abbreviation}`
-   一意のインデックス: `uk_{table_name_abbreviation}_{field_name_abbreviation}`
-   共通インデックス: `idx_{table_name_abbreviation}_{field_name_abbreviation}`
-   複数の単語を含むカラム名: 意味のある略語を使用してください
