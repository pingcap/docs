---
title: Object Naming Convention
summary: Learn the object naming convention in TiDB.
---

# オブジェクトの命名規則 {#object-naming-convention}

このドキュメントでは、データベース、テーブル、インデックス、ユーザーなどのデータベース オブジェクトに名前を付けるルールを紹介します。

## 一般的なルール {#general-rules}

-   意味のある英単語をアンダースコアで区切って使用することをお勧めします。
-   名前には文字、数字、アンダースコアのみを使用してください。
-   `group`や`order`などの TiDB 予約語を列名として使用しないでください。
-   すべてのデータベース オブジェクトには小文字を使用することをお勧めします。

## データベースの命名規則 {#database-naming-convention}

データベース名をビジネス、製品、またはその他の指標によって区別し、データベース名には 20 文字以内を使用することをお勧めします。たとえば、一時ライブラリに`tmp_crm` 、テスト ライブラリに`test_crm`という名前を付けることができます。

## テーブルの命名規則 {#table-naming-convention}

-   同じビジネスまたはモジュールのテーブルには同じプレフィックスを使用し、テーブル名ができる限り一目瞭然になるようにしてください。
-   名前内の単語はアンダースコアで区切ります。テーブル名には 32 文字以内を使用することをお勧めします。
-   理解を深めるために、表の目的に注釈を付けることをお勧めします。例えば：
    -   一時テーブル： `tmp_t_crm_relation_0425`
    -   バックアップテーブル: `bak_t_crm_relation_20170425`
    -   業務一時表： `tmp_st_{business code}_{creator abbreviation}_{date}`
    -   勘定科目表の期間を記録します: `t_crm_ec_record_YYYY{MM}{dd}`
-   さまざまなビジネス モジュールのテーブルに個別のデータベースを作成し、それに応じて注釈を追加します。

## カラムの命名規則 {#column-naming-convention}

-   列の名前は、列の実際の意味または略称です。
-   同じ意味を持つテーブル間では同じ列名を使用することをお勧めします。
-   列に注釈を追加し、列挙型に「0: オフライン、1: オンライン」などの名前付き値を指定することをお勧めします。
-   ブール列の名前は`is_{description}`にすることをお勧めします。たとえば、メンバーが有効かどうかを示す`member`テーブルの列には、 `is_enabled`という名前を付けることができます。
-   列に 30 文字を超える名前を付けることはお勧めできません。また、列の数は 60 未満にする必要があります。
-   `order` 、 `from` 、 `desc`などの TiDB 予約語を列名として使用しないでください。キーワードが予約されているかどうかを確認するには、 [TiDB キーワード](/keywords.md)参照してください。

## インデックスの命名規則 {#index-naming-convention}

-   主キーインデックス: `pk_{table_name_abbreviation}_{field_name_abbreviation}`
-   一意のインデックス: `uk_{table_name_abbreviation}_{field_name_abbreviation}`
-   共通インデックス： `idx_{table_name_abbreviation}_{field_name_abbreviation}`
-   複数の単語を含むカラム名: 意味のある略語を使用してください
