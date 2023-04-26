---
title: SQL Development Specifications
summary: Learn about the SQL development specifications for TiDB.
---

# SQL開発仕様 {#sql-development-specifications}

このドキュメントでは、SQL を使用するための一般的な開発仕様をいくつか紹介します。

## テーブルの作成と削除 {#create-and-delete-tables}

-   基本原則：テーブルの命名規則に従うことを前提に、業務プロセスの異常中断を防ぐために、テーブルの作成文と削除文をアプリケーション内部でパッケージ化し、判定ロジックを追加することを推奨します。
-   詳細: アプリケーション側での SQL コマンドの異常実行による異常中断を回避するために、 `create table if not exists table_name`または`drop table if exists table_name`ステートメントを追加して`if`判定を追加することをお勧めします。

## <code>SELECT *</code>使用法 {#code-select-code-usage}

-   基本原則: クエリに`SELECT *`を使用しないでください。
-   詳細: 必要に応じて適切な列を選択し、すべてのフィールドを読み取るために`SELECT *`を使用しないでください。このような操作はネットワーク帯域幅を消費するためです。カバリング インデックスを効果的に使用するために、クエリされたフィールドをインデックスに追加することを検討してください。

## フィールドで関数を使用する {#use-functions-on-fields}

-   基本原則: クエリされたフィールドで関連する関数を使用できます。インデックス エラーを回避するには、データ型変換関数を含め、 `WHERE`句のフィルター処理されたフィールドで関数を使用しないでください。式インデックスの使用を検討してください。
-   詳細な説明：

    非推奨:

    {{< copyable "" >}}

    ```sql
    SELECT gmt_create
    FROM ...
    WHERE DATE_FORMAT(gmt_create, '%Y%m%d %H:%i:%s') = '20090101 00:00:00'
    ```

    おすすめされた：

    {{< copyable "" >}}

    ```sql
    SELECT DATE_FORMAT(gmt_create, '%Y%m%d %H:%i:%s')
    FROM ...
    WHERE gmt_create = str_to_date('20090101 00:00:00', '%Y%m%d %H:%i:%s')
    ```

## その他の仕様 {#other-specifications}

-   `WHERE`条件のインデックス列に対して数学演算や関数を実行しないでください。
-   `OR` `IN`または`UNION`に置き換えます。 `IN`の数は`300`未満でなければなりません。
-   あいまいなプレフィックス クエリに`%`プレフィックスを使用しないでください。
-   アプリケーションが**マルチ ステートメント**を使用して SQL を実行する場合、つまり、複数の SQL がセミコロンで結合され、一度に実行するためにクライアントに送信される場合、TiDB は最初の SQL 実行の結果のみを返します。
-   式を使用する場合は、式がstorageレイヤー(TiKV またはTiFlash) へのコンピューティング プッシュダウンをサポートしているかどうかを確認します。そうでない場合は、より多くのメモリ消費と、TiDBレイヤーでの OOM も予想されるはずです。storageレイヤーをプッシュダウンできるコンピューティングは次のとおりです。
    -   [TiFlash対応のプッシュダウン計算](/tiflash/tiflash-supported-pushdown-calculations.md) .
    -   [TiKV - プッシュダウンの式のリスト](/functions-and-operators/expressions-pushed-down.md) .
    -   [述語プッシュダウン](/predicate-push-down.md) .
