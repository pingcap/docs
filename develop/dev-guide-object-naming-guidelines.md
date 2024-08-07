---
title: Object Naming Convention
summary: TiDB のオブジェクト命名規則について学習します。
---

# オブジェクトの命名規則 {#object-naming-convention}

このドキュメントでは、データベース、テーブル、インデックス、ユーザーなどのデータベース オブジェクトの命名規則について説明します。

## 一般的なルール {#general-rules}

-   意味のある英語の単語をアンダースコアで区切って使用することをお勧めします。
-   名前には文字、数字、アンダースコアのみを使用してください。
-   `group`や`order`などの TiDB 予約語を列名として使用しないでください。
-   すべてのデータベース オブジェクトには小文字を使用することをお勧めします。

## データベースの命名規則 {#database-naming-convention}

データベース名はビジネス、製品、その他の基準ごとに区別し、データベース名には 20 文字以内を使用することをお勧めします。たとえば、一時ライブラリには`tmp_crm` 、テスト ライブラリには`test_crm`という名前を付けることができます。

## テーブル命名規則 {#table-naming-convention}

-   同じビジネスまたはモジュールのテーブルには同じプレフィックスを使用し、テーブル名が可能な限りわかりやすいようにします。
-   名前内の単語はアンダースコアで区切ります。テーブル名には 32 文字以下を使用することをお勧めします。
-   理解を深めるために、表の目的を注釈で示すことをお勧めします。例:
    -   一時テーブル: `tmp_t_crm_relation_0425`
    -   バックアップテーブル: `bak_t_crm_relation_20170425`
    -   事業運営の暫定表： `tmp_st_{business code}_{creator abbreviation}_{date}`
    -   会計期間の記録表: `t_crm_ec_record_YYYY{MM}{dd}`
-   異なるビジネス モジュールのテーブルごとに個別のデータベースを作成し、それに応じて注釈を追加します。

## カラムの命名規則 {#column-naming-convention}

-   列の名前は、列の実際の意味または略語です。
-   同じ意味を持つテーブル間では同じ列名を使用することをお勧めします。
-   列に注釈を追加し、列挙型に「0: オフライン、1: オンライン」などの名前付きの値を指定することをお勧めします。
-   ブール列の名前は`is_{description}`にすることをお勧めします。たとえば、メンバーが有効かどうかを示す`member`テーブルの列の名前は`is_enabled`にすることができます。
-   列の名前を 30 文字以上にすることは推奨されません。また、列の数は 60 未満にする必要があります。
-   `order` 、 `from` 、 `desc`などの TiDB 予約語を列名として使用しないでください。キーワードが予約されているかどうかを確認するには、 [TiDBキーワード](/keywords.md)を参照してください。

## インデックスの命名規則 {#index-naming-convention}

-   主キーインデックス: `pk_{table_name_abbreviation}_{field_name_abbreviation}`
-   ユニークインデックス: `uk_{table_name_abbreviation}_{field_name_abbreviation}`
-   共通インデックス: `idx_{table_name_abbreviation}_{field_name_abbreviation}`
-   複数の単語を含むカラム名: 意味のある略語を使用してください

## 助けが必要？ {#need-help}

<CustomContent platform="tidb">

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](/support.md)について質問します。

</CustomContent>

<CustomContent platform="tidb-cloud">

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](https://support.pingcap.com/)について質問します。

</CustomContent>
