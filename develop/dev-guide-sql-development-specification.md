---
title: SQL Development Specifications
summary: TiDB の SQL 開発仕様について学習します。
---

# SQL開発仕様 {#sql-development-specifications}

このドキュメントでは、SQL を使用するための一般的な開発仕様をいくつか紹介します。

## テーブルの作成と削除 {#create-and-delete-tables}

-   基本原則: テーブル命名規則に従うことを前提として、アプリケーションがテーブルの作成および削除ステートメントを内部的にパッケージ化し、ビジネス プロセスの異常な中断を防ぐための判断ロジックを追加することをお勧めします。
-   詳細: アプリケーション側で異常に実行された SQL コマンドによる異常な中断を回避するために、 `if`判断を追加するには、 `create table if not exists table_name`または`drop table if exists table_name`ステートメントを推奨します。

## <code>SELECT *</code>使用法 {#code-select-code-usage}

-   基本原則: クエリに`SELECT *`使用しないでください。
-   詳細: 必要に応じて適切な列を選択し、 `SELECT *`使用してすべてのフィールドを読み取ることは避けてください。このような操作はネットワーク帯域幅を消費するためです。カバー インデックスを効果的に使用するには、クエリ対象のフィールドをインデックスに追加することを検討してください。

## フィールドで関数を使用する {#use-functions-on-fields}

-   基本原則: クエリされたフィールドで関連関数を使用できます。インデックスの失敗を回避するには、データ型変換関数を含め、 `WHERE`句のフィルターされたフィールドで関数を使用しないでください。式インデックスの使用を検討してください。
-   詳細な説明：

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

-   条件`WHERE`のインデックス列に対して数学演算や関数を実行しないでください。
-   `OR`を`IN`または`UNION`に置き換えます。 `IN`の数は`300`未満でなければなりません。
-   あいまいプレフィックスクエリには`%`プレフィックスを使用しないでください。
-   アプリケーションが**マルチステートメント**を使用して SQL を実行する場合、つまり、複数の SQL がセミコロンで結合され、一度にクライアントに送信されて実行される場合、TiDB は最初の SQL 実行の結果のみを返します。
-   式を使用する場合は、式がstorageレイヤー(TiKV またはTiFlash ) へのコンピューティングのプッシュダウンをサポートしているかどうかを確認してください。サポートしていない場合は、TiDBレイヤーでメモリ消費量が増え、OOM が発生することも予想されます。storageレイヤーにプッシュダウンできるコンピューティングは次のとおりです。
    -   [TiFlashはプッシュダウン計算をサポート](/tiflash/tiflash-supported-pushdown-calculations.md) 。
    -   [TiKV - プッシュダウンの式のリスト](/functions-and-operators/expressions-pushed-down.md) 。
    -   [述語プッシュダウン](/predicate-push-down.md) 。

## 助けが必要？ {#need-help}

<CustomContent platform="tidb">

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](/support.md)について質問します。

</CustomContent>

<CustomContent platform="tidb-cloud">

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](https://support.pingcap.com/)について質問します。

</CustomContent>
