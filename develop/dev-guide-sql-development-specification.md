---
title: SQL Development Specifications
summary: Learn about the SQL development specifications for TiDB.
---

# SQL開発仕様 {#sql-development-specifications}

このドキュメントでは、SQL を使用するための一般的な開発仕様をいくつか紹介します。

## テーブルの作成と削除 {#create-and-delete-tables}

-   基本原則: テーブルの命名規則に従うことを前提として、業務プロセスの異常中断を防ぐため、アプリケーション内部でテーブルの作成文と削除文をパッケージ化し、判断ロジックを追加することを推奨します。
-   詳細: アプリケーション側のSQLコマンド異常実行による異常中断を避けるため、 `if`判定を追加するには`create table if not exists table_name`または`drop table if exists table_name`文を推奨します。

## <code>SELECT *</code>の使用法 {#code-select-code-usage}

-   基本原則: クエリには`SELECT *`を使用しないでください。
-   詳細: 必要に応じて適切な列を選択し、すべてのフィールドを読み取るために`SELECT *`を使用するのは避けてください。このような操作はネットワーク帯域幅を消費するためです。カバーするインデックスを効果的に使用するには、クエリ対象のフィールドをインデックスに追加することを検討してください。

## フィールドで関数を使用する {#use-functions-on-fields}

-   基本原則: クエリされたフィールドに対して関連する関数を使用できます。インデックスの失敗を回避するには、 `WHERE`句のフィルターされたフィールドに対して、データ型変換関数などの関数を使用しないでください。式インデックスの使用を検討してください。
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

-   `WHERE`条件のインデックス列に対して数学演算や関数を実行しないでください。
-   `OR` `IN`または`UNION`に置き換えます。 `IN`の数は`300`未満でなければなりません。
-   ファジープレフィックスクエリには`%`プレフィックスを使用しないでください。
-   アプリケーションが SQL を実行するために**マルチ ステートメント**を使用する場合、つまり、複数の SQL がセミコロンで結合され、一度に実行するためにクライアントに送信される場合、TiDB は最初の SQL 実行の結果のみを返します。
-   式を使用する場合は、その式がstorageレイヤー(TiKV またはTiFlash) へのコンピューティング プッシュダウンをサポートしているかどうかを確認してください。そうでない場合は、より多くのメモリ消費が発生し、さらには TiDBレイヤーでの OOM が発生することが予想されます。storageレイヤーにプッシュできるコンピューティングは次のとおりです。
    -   [TiFlashがサポートするプッシュダウン計算](/tiflash/tiflash-supported-pushdown-calculations.md) 。
    -   [TiKV - プッシュダウンの式のリスト](/functions-and-operators/expressions-pushed-down.md) 。
    -   [述語のプッシュダウン](/predicate-push-down.md) 。
