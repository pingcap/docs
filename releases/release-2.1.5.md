---
title: TiDB 2.1.5 Release Notes
---

# TiDB2.1.5リリースノート {#tidb-2-1-5-release-notes}

2019年2月28日、TiDB2.1.5がリリースされました。対応するTiDBAnsible2.1.5もリリースされています。 TiDB 2.1.4と比較して、このリリースでは、安定性、SQLオプティマイザー、統計、および実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQLオプティマイザー/エグゼキューター
    -   列の文字セット情報がテーブルの文字セット情報と同じである場合、 `SHOW CREATE TABLE`を作成して列の文字セット情報を出力しないようにします。これにより、 `SHOW CREATE TABLE`と[＃9306](https://github.com/pingcap/tidb/pull/9306)の互換性が向上します。
    -   場合によっては、計算用に`Sort`から`Projection`の演算子に`ScalarFunc`を抽出して、 `Sort` [＃9319](https://github.com/pingcap/tidb/pull/9319)の計算ロジックを単純化することにより、 `Sort`演算子のパニックまたは誤った結果を修正します。
    -   `Sort`演算子[＃9335](https://github.com/pingcap/tidb/pull/9335)の定数値を持つ並べ替えフィールドを削除し[＃9440](https://github.com/pingcap/tidb/pull/9440)
    -   符号なし整数列[＃9339](https://github.com/pingcap/tidb/pull/9339)にデータを挿入するときのデータオーバーフローの問題を修正しました
    -   ターゲットバイナリの長さが`NULL` [＃9349](https://github.com/pingcap/tidb/pull/9349) `cast_as_binary`し`max_allowed_packet` 。
    -   `IF`と`IFNULL`の[＃9351](https://github.com/pingcap/tidb/pull/9351)プロセスを最適化する
    -   スカイラインプルーニングを使用してTiDBのインデックス選択を最適化し、単純なクエリの安定性を向上させます[＃9356](https://github.com/pingcap/tidb/pull/9356)
    -   `DNF`式[＃9405](https://github.com/pingcap/tidb/pull/9405)の選択性の計算をサポート
    -   `!=ANY()`と`=ALL()`の間違ったSQLクエリ結果を修正する場合があります[＃9403](https://github.com/pingcap/tidb/pull/9403)
    -   `Merge Join`操作が実行される2つのテーブルの結合キータイプが異なる場合のパニックまたは間違った結果を修正します[＃9438](https://github.com/pingcap/tidb/pull/9438)
    -   `RAND()`関数の結果がMySQL3と互換性がないという問題を修正し[＃9446](https://github.com/pingcap/tidb/pull/9446)
    -   `Semi Join`処理`NULL`のロジックと空の結果セットをリファクタリングして、正しい結果を取得し、 [＃9449](https://github.com/pingcap/tidb/pull/9449)との互換性を向上させます
-   サーバ
    -   `tidb_constraint_check_in_place`システム変数を追加して、 `INSERT`ステートメント[＃9401](https://github.com/pingcap/tidb/pull/9401)を実行するときにデータの一意性制約を確認します。
    -   `tidb_force_priority`システム変数の値が構成ファイル[＃9347](https://github.com/pingcap/tidb/pull/9347)で設定された値と異なる問題を修正します。
    -   一般ログに`current_db`フィールドを追加して、現在使用されているデータベースの名前を出力します[＃9346](https://github.com/pingcap/tidb/pull/9346)
    -   テーブル[＃9408](https://github.com/pingcap/tidb/pull/9408)のテーブル情報を取得するHTTPAPIを追加します
    -   `LOAD DATA`が誤ったデータをロードする場合があるという問題を修正します[＃9414](https://github.com/pingcap/tidb/pull/9414)
    -   MySQLクライアントとTiDB間の接続を構築するのに時間がかかる場合があるという問題を修正します[＃9451](https://github.com/pingcap/tidb/pull/9451)
-   DDL
    -   `DROP COLUMN`の操作をキャンセルするときのいくつかの問題を修正します[＃9352](https://github.com/pingcap/tidb/pull/9352)
    -   `DROP`つまたは`ADD`のパーティションテーブル操作をキャンセルするときのいくつかの問題を修正します[＃9376](https://github.com/pingcap/tidb/pull/9376)
    -   `ADMIN CHECK TABLE`がデータインデックスの不整合を誤って報告する場合があるという問題を修正します[＃9399](https://github.com/pingcap/tidb/pull/9399)
    -   `TIMESTAMP`デフォルト値[＃9108](https://github.com/pingcap/tidb/pull/9108)のタイムゾーンの問題を修正します

## PD {#pd}

-   返された結果からトゥームストーンストアを削除するには、 `GetAllStores`のインターフェイスに`exclude_tombstone_stores`のオプションを指定します[＃1444](https://github.com/pingcap/pd/pull/1444)

## TiKV {#tikv}

-   Importerがデータのインポートに失敗する場合がある問題を修正します[＃4223](https://github.com/tikv/tikv/pull/4223)
-   場合によっては`KeyNotInRegion`エラーを修正します[＃4125](https://github.com/tikv/tikv/pull/4125)
-   場合によってはリージョンマージによって引き起こされるパニックの問題を修正します[＃4235](https://github.com/tikv/tikv/pull/4235)
-   詳細な`StoreNotMatch`エラーメッセージを追加します[＃3885](https://github.com/tikv/tikv/pull/3885)

## ツール {#tools}

-   雷
    -   トゥームストーンストアがクラスタ[＃4223](https://github.com/tikv/tikv/pull/4223)に存在する場合は、エラーを報告したり終了したりしないでください。
-   TiDB Binlog
    -   DDLイベントレプリケーションの正確性を保証するために、DDLbinlogレプリケーションプランを更新します[＃9304](https://github.com/pingcap/tidb/issues/9304)
