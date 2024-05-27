---
title: TiDB 2.1.5 Release Notes
summary: TiDB 2.1.5 および TiDB Ansible 2.1.5 は、2019 年 2 月 28 日にリリースされました。このリリースでは、安定性、SQL オプティマイザー、統計、および実行エンジンが改善されています。修正には、並べ替え、データ オーバーフロー、および SQL クエリ結果に関する問題が含まれます。新機能には、システム変数、HTTP API、および詳細なエラー メッセージが含まれます。PD には、Tombstone ストアを除外するオプションが追加され、TiKV では、リージョンマージによって発生するデータ インポート、エラー、およびpanicに関する問題が修正されています。Lightning や TiDB Binlogなどのツールも更新されます。
---

# TiDB 2.1.5 リリースノート {#tidb-2-1-5-release-notes}

2019 年 2 月 28 日に、TiDB 2.1.5 がリリースされました。対応する TiDB Ansible 2.1.5 もリリースされました。TiDB 2.1.4 と比較して、このリリースでは安定性、SQL オプティマイザー、統計、実行エンジンが大幅に改善されています。

## ティビ {#tidb}

-   SQL オプティマイザー/エグゼキューター
    -   列の文字セット情報がテーブルの文字セット情報と同じ場合、列の文字セット情報を出力し`SHOW CREATE TABLE`ようにし、 `SHOW CREATE TABLE`とMySQL [＃9306](https://github.com/pingcap/tidb/pull/9306)の互換性を向上させます。
    -   `Sort` [＃9319](https://github.com/pingcap/tidb/pull/9319)の計算ロジックを簡素化するために、 `Sort`から`ScalarFunc`を`Projection`演算子に抽出して計算することで、場合によっては`Sort`演算子のpanicや誤った結果を修正しました。
    -   `Sort`演算子[＃9335](https://github.com/pingcap/tidb/pull/9335)の定数値を持つソートフィールドを削除します[＃9440](https://github.com/pingcap/tidb/pull/9440)
    -   符号なし整数列にデータを挿入する際のデータオーバーフローの問題を修正[＃9339](https://github.com/pingcap/tidb/pull/9339)
    -   対象バイナリの長さが`max_allowed_packet` [＃9349](https://github.com/pingcap/tidb/pull/9349)を超える場合は`cast_as_binary` `NULL`に設定する
    -   `IF`と`IFNULL`の定数折り畳みプロセスを最適化する[＃9351](https://github.com/pingcap/tidb/pull/9351)
    -   スカイラインプルーニングを使用して TiDB のインデックス選択を最適化し、単純なクエリの安定性を向上させる[＃9356](https://github.com/pingcap/tidb/pull/9356)
    -   `DNF`式[＃9405](https://github.com/pingcap/tidb/pull/9405)の選択性の計算をサポート
    -   一部のケースで`!=ANY()`と`=ALL()`のSQLクエリ結果が間違っていた問題を修正しました[＃9403](https://github.com/pingcap/tidb/pull/9403)
    -   `Merge Join`操作を実行する 2 つのテーブルの結合キー タイプが異なる場合にpanicまたは誤った結果が発生する問題を修正しました[＃9438](https://github.com/pingcap/tidb/pull/9438)
    -   `RAND()`関数の結果がMySQL [＃9446](https://github.com/pingcap/tidb/pull/9446)と互換性がない問題を修正
    -   `Semi Join`の処理`NULL`と空の結果セットのロジックをリファクタリングして正しい結果を取得し、MySQL [＃9449](https://github.com/pingcap/tidb/pull/9449)との互換性を向上させます。
-   サーバ
    -   `INSERT`ステートメント[＃9401](https://github.com/pingcap/tidb/pull/9401)を実行するときにデータの一意性制約をチェックするための`tidb_constraint_check_in_place`システム変数を追加します。
    -   `tidb_force_priority`システム変数の値が構成ファイル[＃9347](https://github.com/pingcap/tidb/pull/9347)で設定された値と異なる問題を修正
    -   一般ログに`current_db`フィールドを追加して、現在使用されているデータベース[＃9346](https://github.com/pingcap/tidb/pull/9346)の名前を出力します。
    -   テーブルID [＃9408](https://github.com/pingcap/tidb/pull/9408)のテーブル情報を取得するHTTP APIを追加します。
    -   `LOAD DATA`場合によっては誤ったデータを読み込む問題を修正[＃9414](https://github.com/pingcap/tidb/pull/9414)
    -   MySQLクライアントとTiDB間の接続構築に時間がかかる場合がある問題を修正[＃9451](https://github.com/pingcap/tidb/pull/9451)
-   DDL
    -   `DROP COLUMN`操作[＃9352](https://github.com/pingcap/tidb/pull/9352)をキャンセルする際のいくつかの問題を修正
    -   `DROP`または`ADD`にパーティションテーブル操作をキャンセルする際のいくつかの問題を修正[＃9376](https://github.com/pingcap/tidb/pull/9376)
    -   `ADMIN CHECK TABLE`一部のケースでデータインデックスの不整合を誤って報告する問題を修正[＃9399](https://github.com/pingcap/tidb/pull/9399)
    -   `TIMESTAMP`デフォルト値[＃9108](https://github.com/pingcap/tidb/pull/9108)のタイムゾーン問題を修正

## PD {#pd}

-   返される結果からトゥームストーンストアを削除するには、 `GetAllStores`インターフェイスに`exclude_tombstone_stores`オプションを指定します[＃1444](https://github.com/pingcap/pd/pull/1444)

## ティクヴ {#tikv}

-   インポーターがデータのインポートに失敗する場合がある問題を修正[＃4223](https://github.com/tikv/tikv/pull/4223)
-   いくつかのケースで`KeyNotInRegion`エラーを修正[＃4125](https://github.com/tikv/tikv/pull/4125)
-   一部のケースでリージョンのマージによって発生するpanic問題を修正[＃4235](https://github.com/tikv/tikv/pull/4235)
-   詳細な`StoreNotMatch`エラーメッセージ[＃3885](https://github.com/tikv/tikv/pull/3885)を追加

## ツール {#tools}

-   稲妻
    -   クラスター[＃4223](https://github.com/tikv/tikv/pull/4223)に Tombstone ストアが存在する場合、エラーを報告したり終了したりしないでください。
-   TiDBBinlog
    -   DDLbinlogログレプリケーションプランを更新して、DDL イベントレプリケーション[＃9304](https://github.com/pingcap/tidb/issues/9304)の正確性を保証します。
