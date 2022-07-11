---
title: SQL Development Specifications
summary: Learn about the SQL development specifications for TiDB.
---

# SQL開発仕様 {#sql-development-specification}

このドキュメントでは、SQLを使用するための一般的な開発仕様をいくつか紹介します。

## テーブルの作成と削除 {#create-and-delete-tables}

-   基本原則：テーブルの命名規則に従うことを前提として、アプリケーションがテーブルの作成および削除ステートメントを内部的にパッケージ化し、ビジネスプロセスの異常な中断を防ぐために判断ロジックを追加することをお勧めします。
-   詳細：アプリケーション側でSQLコマンドが異常に実行されることによって引き起こされる異常な中断を回避するために、 `if`の判断を追加するために`create table if not exists table_name`つまたは`drop table if exists table_name`のステートメントをお勧めします。

## <code>SELECT *</code>使用法 {#code-select-code-usage}

-   基本原則：クエリに`SELECT *`を使用しないでください。
-   詳細：必要に応じて適切な列を選択し、 `SELECT *`を使用してすべてのフィールドを読み取ることは避けてください。このような操作は、ネットワーク帯域幅を消費するためです。カバーするインデックスを効果的に利用するために、クエリされたフィールドをインデックスに追加することを検討してください。

## フィールドで関数を使用する {#use-functions-on-fields}

-   基本原則：照会されたフィールドで関連する関数を使用できます。インデックスの失敗を回避するために、データ型変換関数など、 `WHERE`句のフィルター処理されたフィールドで関数を使用しないでください。式インデックスの使用を検討してください。
-   詳細な説明：

    推奨されません：

    {{< copyable "" >}}

    ```sql
    SELECT gmt_create
    FROM ...
    WHERE DATE_FORMAT(gmt_create, '%Y%m%d %H:%i:%s') = '20090101 00:00:0'
    ```

    おすすめされた：

    {{< copyable "" >}}

    ```sql
    SELECT DATE_FORMAT(gmt_create, '%Y%m%d %H:%i:%s')
    FROM .. .
    WHERE gmt_create = str_to_date('20090101 00:00:00', '%Y%m%d %H:%i:s')
    ```

## その他の仕様 {#other-specifications}

-   `WHERE`条件のインデックス列に対して数学演算または関数を実行しないでください。
-   `OR`を`IN`または`UNION`に置き換えます。 `IN`の数は`300`未満でなければなりません。
-   ファジープレフィックスクエリに`%`プレフィックスを使用することは避けてください。
-   アプリケーションが**マルチステートメント**を使用してSQLを実行する場合、つまり、複数のSQLがセミコロンで結合され、一度に実行するためにクライアントに送信される場合、TiDBは最初のSQL実行の結果のみを返します。
-   式を使用する場合は、式がストレージレイヤー（TiKVまたはTiFlash）へのプッシュダウンの計算をサポートしているかどうかを確認してください。そうでない場合は、TiDBレイヤーでさらに多くのメモリ消費とOOMを期待する必要があります。ストレージレイヤーをプッシュダウンできるコンピューティングは次のとおりです。
    -   [TiFlashはプッシュダウン計算をサポートしていました](/tiflash/tiflash-supported-pushdown-calculations.md) 。
    -   [TiKV-プッシュダウンの式のリスト](/functions-and-operators/expressions-pushed-down.md) 。
    -   [述語プッシュダウン](/predicate-push-down.md) 。
