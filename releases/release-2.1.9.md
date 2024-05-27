---
title: TiDB 2.1.9 Release Notes
summary: TiDB 2.1.9 は、2019 年 5 月 6 日にリリースされました。互換性の問題、権限チェックの問題、誤った結果の問題の修正など、さまざまなバグ修正と改善が含まれています。このリリースには、スロー クエリ ログの改善と、演算子によって返される行数の制御のサポートも含まれています。さらに、PD、TiKV、TiDB Binlog、 TiDB Lightning、sync-diff-inspector が更新されています。TiDB Ansible も更新され、ドキュメント リンクとパラメーターの削除が行われています。
---

# TiDB 2.1.9 リリースノート {#tidb-2-1-9-release-notes}

発売日: 2019年5月6日

TiDB バージョン: 2.1.9

TiDB Ansible バージョン: 2.1.9

## ティビ {#tidb}

-   符号なし型がオーバーフローした場合の`MAKETIME`関数の互換性を修正[＃10089](https://github.com/pingcap/tidb/pull/10089)
-   一部のケースで定数の折り畳みによって発生するスタックオーバーフローを修正[＃10189](https://github.com/pingcap/tidb/pull/10189)
-   エイリアスが存在する場合の`Update`の権限チェックの問題を修正[＃10157](https://github.com/pingcap/tidb/pull/10157) 、 [＃10326](https://github.com/pingcap/tidb/pull/10326)
-   DistSQL [＃10197](https://github.com/pingcap/tidb/pull/10197)でメモリ使用量を追跡および制御する
-   照合順序を`utf8mb4_0900_ai_ci` [＃10201](https://github.com/pingcap/tidb/pull/10201)として指定するサポート
-   主キーが符号なし型[＃10209](https://github.com/pingcap/tidb/pull/10209)の場合の`MAX`関数の誤った結果の問題を修正
-   非厳密SQLモード[＃10254](https://github.com/pingcap/tidb/pull/10254)でNOT NULL列にNULL値が挿入される問題を修正
-   `DISTINCT` [＃10270](https://github.com/pingcap/tidb/pull/10270)に複数の列が存在する場合の`COUNT`関数の誤った結果の問題を修正しました
-   `LOAD DATA`不規則な CSV ファイルを解析するときに発生するpanic問題を修正[＃10269](https://github.com/pingcap/tidb/pull/10269)
-   `Index Lookup Join` [＃10244](https://github.com/pingcap/tidb/pull/10244)で外部結合キーと内部結合キーの型が一致しない場合は、オーバーフローエラーを無視します。
-   一部のケースでステートメントが誤ってポイント取得と判断される問題を修正[＃10299](https://github.com/pingcap/tidb/pull/10299)
-   時間型がタイムゾーンを変換しない場合に誤った結果になる問題を修正[＃10345](https://github.com/pingcap/tidb/pull/10345)
-   TiDB 文字セットの大文字と小文字が一致しないケースがある問題を修正[＃10354](https://github.com/pingcap/tidb/pull/10354)
-   演算子[＃9166](https://github.com/pingcap/tidb/issues/9166)によって返される行数の制御をサポート
    -   選択と投影[＃10110](https://github.com/pingcap/tidb/pull/10110)
    -   `StreamAgg`と`HashAgg` [＃10133](https://github.com/pingcap/tidb/pull/10133)
    -   `TableReader`と`IndexReader`と`IndexLookup` [＃10169](https://github.com/pingcap/tidb/pull/10169)
-   スロークエリログの改善
    -   類似のSQL [＃10093](https://github.com/pingcap/tidb/pull/10093)を区別するために`SQL Digest`追加します
    -   低速クエリステートメントで使用される統計のバージョン情報を追加する[＃10220](https://github.com/pingcap/tidb/pull/10220)
    -   スロークエリログ[＃10246](https://github.com/pingcap/tidb/pull/10246)でステートメントのメモリ消費量を表示する
    -   コプロセッサー関連情報の出力形式を調整し、pt-query-digest [＃10300](https://github.com/pingcap/tidb/pull/10300)で解析できるようにします。
    -   遅いクエリステートメント[＃10275](https://github.com/pingcap/tidb/pull/10275)の`#`文字の問題を修正
    -   遅いクエリステートメントのメモリテーブルにいくつかの情報列を追加する[＃10317](https://github.com/pingcap/tidb/pull/10317)
    -   スロークエリログ[＃10310](https://github.com/pingcap/tidb/pull/10310)にトランザクションコミット時間を追加する
    -   一部の時間形式が pt-query-digest [＃10323](https://github.com/pingcap/tidb/pull/10323)で解析できない問題を修正

## PD {#pd}

-   GetOperator サービス[＃1514](https://github.com/pingcap/pd/pull/1514)サポートする

## ティクヴ {#tikv}

-   リーダー[＃4604](https://github.com/tikv/tikv/pull/4604)を移行する際の潜在的なクォーラム変更を修正

## ツール {#tools}

-   TiDBBinlog
    -   主キー列のunsigned int型のデータがマイナス数[＃574](https://github.com/pingcap/tidb-binlog/pull/574)であるため、データレプリケーションが中断される問題を修正
    -   ダウンストリームが`pb`場合、圧縮オプションを削除し、ダウンストリーム名を`pb`から`file` [＃597](https://github.com/pingcap/tidb-binlog/pull/575)に変更します。
    -   2.1.7で導入されたReparoが間違った`UPDATE`文[＃576](https://github.com/pingcap/tidb-binlog/pull/576)を生成するバグを修正
-   TiDB Lightning
    -   列データのビット型がパーサー[＃164](https://github.com/pingcap/tidb-lightning/pull/164)によって誤って解析されるバグを修正
    -   行IDまたはデフォルトの列値[＃174](https://github.com/pingcap/tidb-lightning/pull/174)を使用して、ダンプファイル内の不足している列データを入力します。
    -   一部の SST ファイルのインポートに失敗するものの、インポート結果[＃4566](https://github.com/tikv/tikv/pull/4566)が成功して返されるというインポーターのバグを修正しました。
    -   SST ファイルを TiKV [＃4607](https://github.com/tikv/tikv/pull/4607)にアップロードするときに、インポーターで速度制限を設定できるようになりました。
    -   インポーター RocksDB SST 圧縮方式を`lz4`に変更して CPU 消費量を削減[＃4624](https://github.com/tikv/tikv/pull/4624)
-   同期差分インスペクター
    -   サポートチェックポイント[＃227](https://github.com/pingcap/tidb-tools/pull/227)

## TiDB アンシブル {#tidb-ansible}

-   ドキュメントのリファクタリング[＃740](https://github.com/pingcap/tidb-ansible/pull/740)に従って tidb-ansible ドキュメントのリンクを更新します[＃741](https://github.com/pingcap/tidb-ansible/pull/741)
-   `inventory.ini`ファイル内の`enable_slow_query_log`パラメータを削除し、スロークエリログをデフォルトで別のログファイルに出力します[＃742](https://github.com/pingcap/tidb-ansible/pull/742)
