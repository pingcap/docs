---
title: TiDB 2.1.5 Release Notes
---

# TiDB 2.1.5 リリースノート {#tidb-2-1-5-release-notes}

2019 年 2 月 28 日に、TiDB 2.1.5 がリリースされました。対応する TiDB Ansible 2.1.5 もリリースされています。 TiDB 2.1.4 と比較して、このリリースでは安定性、SQL オプティマイザー、統計、および実行エンジンが大幅に向上しています。

## TiDB {#tidb}

-   SQL オプティマイザー/エグゼキューター
    -   `SHOW CREATE TABLE`のカラムの文字セット情報がテーブルの文字セット情報と同じである場合、カラムの文字セット情報を出力しないようにして、 `SHOW CREATE TABLE`と MySQL [#9306](https://github.com/pingcap/tidb/pull/9306)の互換性を向上させます。
    -   `Sort` [#9319](https://github.com/pingcap/tidb/pull/9319)の計算panicを簡素化するために、 `Sort`から`ScalarFunc`抽出して`Projection`演算子に計算することで、場合によっては`Sort`演算子のパニックや誤った結果が修正されました。
    -   `Sort`演算子[#9335](https://github.com/pingcap/tidb/pull/9335) 、 [#9440](https://github.com/pingcap/tidb/pull/9440)の定数値を含む並べ替えフィールドを削除します。
    -   符号なし整数列[#9339](https://github.com/pingcap/tidb/pull/9339)にデータを挿入するときのデータ オーバーフローの問題を修正します。
    -   対象バイナリの長さが`max_allowed_packet` [#9349](https://github.com/pingcap/tidb/pull/9349)を超える場合は`cast_as_binary` ～ `NULL`を設定します。
    -   `IF`と`IFNULL`の定数折り込みプロセスを最適化する[#9351](https://github.com/pingcap/tidb/pull/9351)
    -   スカイライン プルーニングを使用して TiDB のインデックス選択を最適化し、単純なクエリの安定性を向上させます[#9356](https://github.com/pingcap/tidb/pull/9356)
    -   `DNF`式[#9405](https://github.com/pingcap/tidb/pull/9405)の選択性の計算をサポートします。
    -   場合によっては`!=ANY()`と`=ALL()`の間違った SQL クエリ結果を修正[#9403](https://github.com/pingcap/tidb/pull/9403)
    -   `Merge Join`操作が実行される 2 つのテーブルの結合キーの種類が異なる場合にpanicまたは間違った結果が発生する問題を修正[#9438](https://github.com/pingcap/tidb/pull/9438)
    -   `RAND()`関数の結果が MySQL [#9446](https://github.com/pingcap/tidb/pull/9446)と互換性がない問題を修正
    -   `Semi Join`処理`NULL`と空の結果セットのロジックをリファクタリングして正しい結果を取得し、MySQL [#9449](https://github.com/pingcap/tidb/pull/9449)との互換性を向上させます。
-   サーバ
    -   `tidb_constraint_check_in_place`システム変数を追加して、 `INSERT`ステートメントの実行時にデータの一意性制約をチェックします[#9401](https://github.com/pingcap/tidb/pull/9401)
    -   `tidb_force_priority`システム変数の値が設定ファイルに設定されている値と異なる問題を修正[#9347](https://github.com/pingcap/tidb/pull/9347)
    -   一般ログに`current_db`フィールドを追加して、現在使用されているデータベースの名前を出力します[#9346](https://github.com/pingcap/tidb/pull/9346)
    -   テーブル[#9408](https://github.com/pingcap/tidb/pull/9408)のテーブル情報を取得するHTTP APIを追加
    -   `LOAD DATA`場合によっては不正なデータが読み込まれる問題を修正[#9414](https://github.com/pingcap/tidb/pull/9414)
    -   MySQL クライアントと TiDB 間の接続の構築に時間がかかる場合がある問題を修正[#9451](https://github.com/pingcap/tidb/pull/9451)
-   DDL
    -   `DROP COLUMN`操作[#9352](https://github.com/pingcap/tidb/pull/9352)をキャンセルする際のいくつかの問題を修正
    -   `DROP`または`ADD`パーティションテーブル操作をキャンセルするときのいくつかの問題を修正します[#9376](https://github.com/pingcap/tidb/pull/9376)
    -   `ADMIN CHECK TABLE`場合によってはデータインデックスの不一致を誤って報告する問題を修正[#9399](https://github.com/pingcap/tidb/pull/9399)
    -   `TIMESTAMP`デフォルト値[#9108](https://github.com/pingcap/tidb/pull/9108)のタイムゾーンの問題を修正

## PD {#pd}

-   返された結果からトゥームストーン ストアを削除するには、インターフェイス`GetAllStores`で`exclude_tombstone_stores`オプションを指定します[#1444](https://github.com/pingcap/pd/pull/1444)

## TiKV {#tikv}

-   インポーターがデータのインポートに失敗する場合がある問題を修正[#4223](https://github.com/tikv/tikv/pull/4223)
-   場合によっては`KeyNotInRegion`エラーを修正します[#4125](https://github.com/tikv/tikv/pull/4125)
-   場合によってはリージョンのマージによって引き起こされるpanicの問題を修正[#4235](https://github.com/tikv/tikv/pull/4235)
-   詳細`StoreNotMatch`エラー メッセージ[#3885](https://github.com/tikv/tikv/pull/3885)を追加

## ツール {#tools}

-   稲妻
    -   クラスターにトゥームストーン ストアが存在する場合、エラーを報告したり終了したりしません[#4223](https://github.com/tikv/tikv/pull/4223)
-   TiDBBinlog
    -   DDLbinlogレプリケーション プランを更新して、DDL イベント レプリケーション[#9304](https://github.com/pingcap/tidb/issues/9304)の正確さを保証します。
