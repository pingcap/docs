---
title: Object Naming Convention
summary: TiDB におけるオブジェクトの命名規則について学習します。
aliases: ['/tidb/stable/dev-guide-object-naming-guidelines/','/tidb/dev/dev-guide-object-naming-guidelines/','/tidbcloud/dev-guide-object-naming-guidelines/']
---

# オブジェクトの命名規則 {#object-naming-convention}

このドキュメントでは、データベース、テーブル、インデックス、ユーザーなどのデータベース オブジェクトの命名規則について説明します。

## 一般的なルール {#general-rules}

-   意味のある英語の単語をアンダースコアで区切って使用することをお勧めします。
-   名前には文字、数字、アンダースコアのみを使用してください。
-   `group`や`order`などの TiDB 予約語を列名として使用しないでください。
-   すべてのデータベース オブジェクトには小文字を使用することをお勧めします。

## データベースの命名規則 {#database-naming-convention}

データベース名は、ビジネス、製品、その他の指標ごとに区別し、20文字以内にすることをお勧めします。例えば、一時ライブラリには`tmp_crm` 、テストライブラリには`test_crm`という名前を付けることができます。

## テーブルの命名規則 {#table-naming-convention}

-   同じビジネスまたはモジュールのテーブルには同じプレフィックスを使用し、テーブル名が可能な限りわかりやすいものにします。
-   名前内の単語はアンダースコアで区切ります。テーブル名は32文字以内にすることをお勧めします。
-   理解を深めるために、表の目的を注釈で示すことをお勧めします。例えば：
    -   一時テーブル: `tmp_t_crm_relation_0425`
    -   バックアップテーブル: `bak_t_crm_relation_20170425`
    -   事業運営の暫定表： `tmp_st_{business code}_{creator abbreviation}_{date}`
    -   会計期間の記録表: `t_crm_ec_record_YYYY{MM}{dd}`
-   異なるビジネス モジュールのテーブルごとに個別のデータベースを作成し、それに応じて注釈を追加します。

## カラムの命名規則 {#column-naming-convention}

-   列の命名は、列の実際の意味または略語です。
-   同じ意味を持つテーブル間では同じ列名を使用することをお勧めします。
-   列に注釈を追加し、「0: オフライン、1: オンライン」などの列挙型の名前付きの値を指定することをお勧めします。
-   ブール列の名前は`is_{description}`にすることをお勧めします。例えば、 `member`テーブルの、メンバーが有効かどうかを示す列の名前は`is_enabled`にすることができます。
-   列名を 30 文字以上にすることは推奨されません。また、列の数は 60 未満にする必要があります。
-   `order` 、 `from` 、 `desc`などのTiDB予約語を列名として使用しないでください。キーワードが予約されているかどうかを確認するには、 [TiDBキーワード](/keywords.md)参照してください。

## インデックスの命名規則 {#index-naming-convention}

-   主キーインデックス: `pk_{table_name_abbreviation}_{field_name_abbreviation}`
-   ユニークインデックス: `uk_{table_name_abbreviation}_{field_name_abbreviation}`
-   共通インデックス: `idx_{table_name_abbreviation}_{field_name_abbreviation}`
-   複数の単語を含むカラム名: 意味のある略語を使用してください

## ヘルプが必要ですか? {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに問い合わせてください。
-   [TiDB Cloudのサポートチケットを送信する](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDBセルフマネージドのサポートチケットを送信する](/support.md)
