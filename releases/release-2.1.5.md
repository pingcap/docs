---
title: TiDB 2.1.5 Release Notes
---

# TiDB 2.1.5 リリースノート {#tidb-2-1-5-release-notes}

2019 年 2 月 28 日に、TiDB 2.1.5 がリリースされました。対応する TiDB Ansible 2.1.5 もリリースされています。 TiDB 2.1.4 と比較して、このリリースでは安定性、SQL オプティマイザー、統計、実行エンジンが大幅に向上しています。

## TiDB {#tidb}

-   SQL オプティマイザー/エグゼキューター
    -   `SHOW CREATE TABLE`のカラムの文字セット情報がテーブルの文字セット情報と同じである場合、カラムの文字セット情報を出力しないようにして、 `SHOW CREATE TABLE`と MySQL [<a href="https://github.com/pingcap/tidb/pull/9306">#9306</a>](https://github.com/pingcap/tidb/pull/9306)の互換性を向上させます。
    -   `Sort` [<a href="https://github.com/pingcap/tidb/pull/9319">#9319</a>](https://github.com/pingcap/tidb/pull/9319)の計算panicを簡素化するために、 `Sort`から`ScalarFunc`抽出して`Projection`演算子として計算することにより、場合によっては`Sort`演算子のパニックや誤った結果が修正されました。
    -   `Sort`演算子[<a href="https://github.com/pingcap/tidb/pull/9335">#9335</a>](https://github.com/pingcap/tidb/pull/9335) 、 [<a href="https://github.com/pingcap/tidb/pull/9440">#9440</a>](https://github.com/pingcap/tidb/pull/9440)の定数値を含む並べ替えフィールドを削除します。
    -   符号なし整数列[<a href="https://github.com/pingcap/tidb/pull/9339">#9339</a>](https://github.com/pingcap/tidb/pull/9339)にデータを挿入するときのデータ オーバーフローの問題を修正します。
    -   対象バイナリの長さが`max_allowed_packet` [<a href="https://github.com/pingcap/tidb/pull/9349">#9349</a>](https://github.com/pingcap/tidb/pull/9349)を超える場合は`cast_as_binary` ～ `NULL`を設定します。
    -   `IF`と`IFNULL`の定数折り込みプロセスを最適化する[<a href="https://github.com/pingcap/tidb/pull/9351">#9351</a>](https://github.com/pingcap/tidb/pull/9351)
    -   スカイライン プルーニングを使用して TiDB のインデックス選択を最適化し、単純なクエリの安定性を向上させます[<a href="https://github.com/pingcap/tidb/pull/9356">#9356</a>](https://github.com/pingcap/tidb/pull/9356)
    -   `DNF`式[<a href="https://github.com/pingcap/tidb/pull/9405">#9405</a>](https://github.com/pingcap/tidb/pull/9405)の選択性の計算をサポートします。
    -   場合によっては`!=ANY()`と`=ALL()`の間違った SQL クエリ結果を修正[<a href="https://github.com/pingcap/tidb/pull/9403">#9403</a>](https://github.com/pingcap/tidb/pull/9403)
    -   `Merge Join`操作が実行される 2 つのテーブルの結合キーの種類が異なる場合にpanicまたは間違った結果が発生する問題を修正[<a href="https://github.com/pingcap/tidb/pull/9438">#9438</a>](https://github.com/pingcap/tidb/pull/9438)
    -   `RAND()`関数の結果が MySQL [<a href="https://github.com/pingcap/tidb/pull/9446">#9446</a>](https://github.com/pingcap/tidb/pull/9446)と互換性がない問題を修正
    -   `Semi Join`処理`NULL`と空の結果セットのロジックをリファクタリングして正しい結果を取得し、MySQL [<a href="https://github.com/pingcap/tidb/pull/9449">#9449</a>](https://github.com/pingcap/tidb/pull/9449)との互換性を向上させます。
-   サーバ
    -   `tidb_constraint_check_in_place`システム変数を追加して、 `INSERT`ステートメントの実行時にデータの一意性制約をチェックします[<a href="https://github.com/pingcap/tidb/pull/9401">#9401</a>](https://github.com/pingcap/tidb/pull/9401)
    -   `tidb_force_priority`システム変数の値が設定ファイルに設定されている値と異なる問題を修正[<a href="https://github.com/pingcap/tidb/pull/9347">#9347</a>](https://github.com/pingcap/tidb/pull/9347)
    -   一般ログに`current_db`フィールドを追加して、現在使用されているデータベースの名前を出力します[<a href="https://github.com/pingcap/tidb/pull/9346">#9346</a>](https://github.com/pingcap/tidb/pull/9346)
    -   テーブル[<a href="https://github.com/pingcap/tidb/pull/9408">#9408</a>](https://github.com/pingcap/tidb/pull/9408)のテーブル情報を取得するHTTP APIを追加
    -   `LOAD DATA`場合によっては不正なデータが読み込まれる問題を修正[<a href="https://github.com/pingcap/tidb/pull/9414">#9414</a>](https://github.com/pingcap/tidb/pull/9414)
    -   MySQL クライアントと TiDB 間の接続の構築に時間がかかる場合がある問題を修正[<a href="https://github.com/pingcap/tidb/pull/9451">#9451</a>](https://github.com/pingcap/tidb/pull/9451)
-   DDL
    -   `DROP COLUMN`操作[<a href="https://github.com/pingcap/tidb/pull/9352">#9352</a>](https://github.com/pingcap/tidb/pull/9352)をキャンセルする際のいくつかの問題を修正
    -   `DROP`または`ADD`パーティションテーブル操作をキャンセルするときのいくつかの問題を修正します[<a href="https://github.com/pingcap/tidb/pull/9376">#9376</a>](https://github.com/pingcap/tidb/pull/9376)
    -   `ADMIN CHECK TABLE`場合によってはデータインデックスの不一致を誤って報告する問題を修正[<a href="https://github.com/pingcap/tidb/pull/9399">#9399</a>](https://github.com/pingcap/tidb/pull/9399)
    -   `TIMESTAMP`デフォルト値[<a href="https://github.com/pingcap/tidb/pull/9108">#9108</a>](https://github.com/pingcap/tidb/pull/9108)のタイムゾーンの問題を修正

## PD {#pd}

-   返された結果からトゥームストーン ストアを削除するには、インターフェイス`GetAllStores`で`exclude_tombstone_stores`オプションを指定します[<a href="https://github.com/pingcap/pd/pull/1444">#1444</a>](https://github.com/pingcap/pd/pull/1444)

## TiKV {#tikv}

-   インポーターがデータのインポートに失敗する場合がある問題を修正[<a href="https://github.com/tikv/tikv/pull/4223">#4223</a>](https://github.com/tikv/tikv/pull/4223)
-   場合によっては`KeyNotInRegion`エラーを修正します[<a href="https://github.com/tikv/tikv/pull/4125">#4125</a>](https://github.com/tikv/tikv/pull/4125)
-   場合によってはリージョンのマージによって引き起こされるpanicの問題を修正[<a href="https://github.com/tikv/tikv/pull/4235">#4235</a>](https://github.com/tikv/tikv/pull/4235)
-   詳細`StoreNotMatch`エラー メッセージ[<a href="https://github.com/tikv/tikv/pull/3885">#3885</a>](https://github.com/tikv/tikv/pull/3885)を追加

## ツール {#tools}

-   雷
    -   クラスターにトゥームストーン ストアが存在する場合、エラーを報告したり終了したりしません[<a href="https://github.com/tikv/tikv/pull/4223">#4223</a>](https://github.com/tikv/tikv/pull/4223)
-   TiDBBinlog
    -   DDLbinlogレプリケーション プランを更新して、DDL イベント レプリケーション[<a href="https://github.com/pingcap/tidb/issues/9304">#9304</a>](https://github.com/pingcap/tidb/issues/9304)の正確さを保証します。
