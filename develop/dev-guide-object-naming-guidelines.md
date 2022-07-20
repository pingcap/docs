---
title: Object Naming Convention
summary: Learn the object naming convention in TiDB.
---

# オブジェクト命名規則 {#object-naming-convention}

このドキュメントでは、データベース、テーブル、インデックス、ユーザーなどのデータベースオブジェクトに名前を付けるためのルールを紹介します。

## 一般的なルール {#general-rules}

-   アンダースコアで区切った意味のある英語の単語を使用することをお勧めします。
-   名前には文字、数字、およびアンダースコアのみを使用してください。
-   列名として、 `group`や`order`などのTiDB予約語を使用しないでください。
-   すべてのデータベースオブジェクトには小文字を使用することをお勧めします。

## データベースの命名規則 {#database-naming-convention}

データベース名をビジネス、製品、またはその他のメトリックで区別し、データベース名に使用する文字は20文字以内にすることをお勧めします。たとえば、一時ライブラリに`tmp_crm` 、テストライブラリに`test_crm`という名前を付けることができます。

## テーブルの命名規則 {#table-naming-convention}

-   同じビジネスまたはモジュールのテーブルに同じプレフィックスを使用し、テーブル名ができるだけわかりやすいものであることを確認してください。
-   名前内の単語はアンダースコアで区切ります。テーブル名には32文字以内を使用することをお勧めします。
-   理解を深めるために、表の目的に注釈を付けることをお勧めします。例えば：
    -   一時テーブル： `tmp_t_crm_relation_0425`
    -   バックアップテーブル： `bak_t_crm_relation_20170425`
    -   事業運営の一時表： `tmp_st_{business code}_{creator abbreviation}_{date}`
    -   勘定科目表期間の記録： `t_crm_ec_record_YYYY{MM}{dd}`
-   異なるビジネスモジュールのテーブル用に個別のデータベースを作成し、それに応じて注釈を追加します。

## カラムの命名規則 {#column-naming-convention}

-   列の名前は、列の実際の意味または省略形です。
-   同じ意味を持つテーブル間で同じ列名を使用することをお勧めします。
-   列に注釈を追加し、列挙型に「0：オフライン、1：オンライン」などの名前付きの値を指定することをお勧めします。
-   ブール列に`is_{description}`という名前を付けることをお勧めします。たとえば、メンバーが有効になっているかどうかを示す`member`テーブルの列には、 `is_enabled`という名前を付けることができます。
-   30文字を超える列に名前を付けることはお勧めしません。また、列の数は60未満にする必要があります。
-   `order`などの`from`予約語を列`desc`として使用することは避けてください。キーワードが予約されているかどうかを確認するには、 [TiDBキーワード](/keywords.md)を参照してください。

## インデックスの命名規則 {#index-naming-convention}

-   主キーインデックス： `pk_{table_name_abbreviation}_{field_name_abbreviation}`
-   一意のインデックス： `uk_{table_name_abbreviation}_{field_name_abbreviation}`
-   共通インデックス： `idx_{table_name_abbreviation}_{field_name_abbreviation}`
-   複数の単語を含むカラム名：意味のある略語を使用する
