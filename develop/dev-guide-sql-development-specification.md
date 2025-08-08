---
title: SQL Development Specifications
summary: TiDB の SQL 開発仕様について学習します。
---

# SQL開発仕様 {#sql-development-specifications}

このドキュメントでは、SQL を使用するための一般的な開発仕様をいくつか紹介します。

## テーブルの作成と削除 {#create-and-delete-tables}

-   基本原則: テーブル命名規則に従うことを前提として、アプリケーションがテーブルの作成および削除ステートメントを内部的にパッケージ化し、ビジネスプロセスの異常な中断を防ぐための判断ロジックを追加することをお勧めします。
-   詳細: アプリケーション側で異常に実行された SQL コマンドによる異常な中断を回避するために、 `if`判断を追加するには、 `create table if not exists table_name`または`drop table if exists table_name`ステートメントを推奨します。

## <code>SELECT *</code>の使用法 {#code-select-code-usage}

-   基本原則: クエリに`SELECT *`使用しないでください。
-   詳細：必要に応じて適切な列を選択し、 `SELECT *`使用してすべてのフィールドを読み取る操作はネットワーク帯域幅を消費するため、避けてください。カバーインデックスを効果的に活用するには、クエリ対象のフィールドをインデックスに追加することを検討してください。

## フィールドで関数を使用する {#use-functions-on-fields}

-   基本原則：クエリ対象のフィールドに対して関連関数を使用できます。インデックスの失敗を避けるため、 `WHERE`のフィルタリング対象フィールドに対しては、データ型変換関数を含むいかなる関数も使用しないでください。式インデックスの使用を検討してください。
-   詳細な説明:

    推奨されません:

    ```sql
    SELECT gmt_create
    FROM ...
    WHERE DATE_FORMAT(gmt_create, '%Y%m%d %H:%i:%s') = '20090101 00:00:00'
    ```

    推奨：

    ```sql
    SELECT DATE_FORMAT(gmt_create, '%Y%m%d %H:%i:%s')
    FROM ...
    WHERE gmt_create = str_to_date('20090101 00:00:00', '%Y%m%d %H:%i:%s')
    ```

## その他の仕様 {#other-specifications}

-   条件`WHERE`インデックス列に対して数学演算や関数を実行しないでください。
-   `OR` `IN`または`UNION`に置き換えてください。7 `IN`数は`300`未満でなければなりません。
-   あいまいプレフィックスクエリにはプレフィックス`%`使用しないでください。
-   アプリケーションが**マルチステートメント**を使用して SQL を実行する場合、つまり複数の SQL がセミコロンで結合され、一度にクライアントに送信されて実行される場合、TiDB は最初の SQL 実行の結果のみを返します。
-   式を使用する場合は、その式がstorageレイヤー（TiKVまたはTiFlash ）へのコンピューティングのプッシュダウンをサポートしているかどうかを確認してください。サポートされていない場合は、TiDBレイヤーでメモリ消費量が増加し、OOMが発生する可能性が高くなります。storageレイヤーにプッシュダウンできるコンピューティングは以下の通りです。
    -   [TiFlashはプッシュダウン計算をサポート](/tiflash/tiflash-supported-pushdown-calculations.md) 。
    -   [TiKV - プッシュダウンの式のリスト](/functions-and-operators/expressions-pushed-down.md) 。
    -   [述語プッシュダウン](/predicate-push-down.md) 。

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>
