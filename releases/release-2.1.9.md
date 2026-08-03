---
title: TiDB 2.1.9 Release Notes
summary: TiDB 2.1.9は2019年5月6日にリリースされました。互換性の問題、権限チェックの問題、誤った結果の問題など、さまざまなバグ修正と改善が含まれています。また、スロークエリログの改善と、演算子によって返される行数を制御するためのサポートも含まれています。さらに、PD、TiKV、TiDB Binlog、 TiDB Lightning、sync-diff-inspectorも更新されています。TiDB Ansibleも更新され、ドキュメントへのリンクとパラメータの削除が追加されました。
---

# TiDB 2.1.9 リリースノート {#tidb-2-1-9-release-notes}

発売日：2019年5月6日

TiDB バージョン: 2.1.9

TiDB Ansible バージョン: 2.1.9

## TiDB {#tidb}

-   符号なし型がオーバーフローした場合の`MAKETIME`関数の互換性を修正[＃10089](https://github.com/pingcap/tidb/pull/10089)
-   一部のケースで定数の折り畳みによって発生するスタックオーバーフローを修正[＃10189](https://github.com/pingcap/tidb/pull/10189)
-   エイリアスが存在する場合の権限チェックの問題を修正`Update` [＃10157](https://github.com/pingcap/tidb/pull/10157) , [＃10326](https://github.com/pingcap/tidb/pull/10326)
-   DistSQL でメモリ使用量を追跡および制御する [＃10197](https://github.com/pingcap/tidb/pull/10197)
-   照合順序を`utf8mb4_0900_ai_ci` として指定するサポート [＃10201](https://github.com/pingcap/tidb/pull/10201)
-   主キーが符号なし型の場合の`MAX`関数の誤った結果の問題を修正しました [＃10209](https://github.com/pingcap/tidb/pull/10209)
-   非厳密モードでNOT NULL列にNULL値が挿入される問題を修正 [＃10254](https://github.com/pingcap/tidb/pull/10254)
-   `DISTINCT` に複数の列が存在する場合の`COUNT`関数の誤った結果の問題を修正しました [＃10270](https://github.com/pingcap/tidb/pull/10270)
-   `LOAD DATA`不規則なCSVファイルを解析する際に発生するpanic問題を修正[＃10269](https://github.com/pingcap/tidb/pull/10269)
-   `Index Lookup Join` で外部結合キーと内部結合キーの型が一致しない場合は、オーバーフローエラーを無視します。 [＃10244](https://github.com/pingcap/tidb/pull/10244)
-   一部のケースで誤ってPointGetと判断される問題を修正[＃10299](https://github.com/pingcap/tidb/pull/10299)
-   一部のケースで時間型がタイムゾーンを変換しない場合に誤った結果が出る問題を修正[＃10345](https://github.com/pingcap/tidb/pull/10345)
-   TiDB の文字セットの大文字と小文字が一致しないケースがいくつかある問題を修正[＃10354](https://github.com/pingcap/tidb/pull/10354)
-   演算子によって返される行数を制御するサポート [＃9166](https://github.com/pingcap/tidb/issues/9166)
    -   選択と投影[＃10110](https://github.com/pingcap/tidb/pull/10110)
    -   `StreamAgg`と`HashAgg` [＃10133](https://github.com/pingcap/tidb/pull/10133)
    -   `TableReader` &amp; `IndexReader` &amp; `IndexLookup` [＃10169](https://github.com/pingcap/tidb/pull/10169)
-   スロークエリログの改善
    -   類似したSQL 区別するために`SQL Digest`加算する [＃10093](https://github.com/pingcap/tidb/pull/10093)
    -   スロークエリステートメントで使用される統計のバージョン情報を追加する[＃10220](https://github.com/pingcap/tidb/pull/10220)
    -   スロークエリログでステートメントのメモリ消費量を表示する [＃10246](https://github.com/pingcap/tidb/pull/10246)
    -   コプロセッサー関連情報の出力形式を調整し、pt-query-digest で解析できるようにします。 [＃10300](https://github.com/pingcap/tidb/pull/10300)
    -   スロークエリステートメントの`#`文字の問題を修正 [＃10275](https://github.com/pingcap/tidb/pull/10275)
    -   スロークエリステートメントのメモリテーブルにいくつかの情報列を追加する[＃10317](https://github.com/pingcap/tidb/pull/10317)
    -   スロークエリログにトランザクションコミット時間を追加する [＃10310](https://github.com/pingcap/tidb/pull/10310)
    -   一部の時間形式がpt-query-digest で解析できない問題を修正 [＃10323](https://github.com/pingcap/tidb/pull/10323)

## PD {#pd}

-   GetOperator サービスサポートする [＃1514](https://github.com/pingcap/pd/pull/1514)

## TiKV {#tikv}

-   リーダー移行時に発生する可能性のあるクォーラムの変更を修正 [＃4604](https://github.com/tikv/tikv/pull/4604)

## ツール {#tools}

-   TiDB Binlog
    -   主キー列のunsigned int型のデータがマイナスであるため、データレプリケーションが中断される問題を修正しました。 [＃574](https://github.com/pingcap/tidb-binlog/pull/574)
    -   ダウンストリームが`pb`の場合に圧縮オプションを削除し、ダウンストリーム名を`pb`から`file`に変更します[＃597](https://github.com/pingcap/tidb-binlog/pull/575)
    -   2.1.7で導入されたReparoが間違った`UPDATE`ステートメントを生成するバグを修正しました [＃576](https://github.com/pingcap/tidb-binlog/pull/576)
-   TiDB Lightning
    -   列データのビット型がパーサーによって誤って解析されるバグを修正 [＃164](https://github.com/pingcap/tidb-lightning/pull/164)
    -   行IDまたはデフォルトの列値を使用して、ダンプファイル内の不足している列データを入力します。 [＃174](https://github.com/pingcap/tidb-lightning/pull/174)
    -   一部の SST ファイルのインポートに失敗するものの、インポート結果が成功として返されるというインポーターのバグを修正しました。 [＃4566](https://github.com/tikv/tikv/pull/4566)
    -   SST ファイルを TiKV にアップロードするときに、インポーターで速度制限を設定できるようになりました [＃4607](https://github.com/tikv/tikv/pull/4607)
    -   CPU消費量を削減するために、インポーターのRocksDB SST圧縮方式を`lz4`に変更します[＃4624](https://github.com/tikv/tikv/pull/4624)
-   同期差分インスペクター
    -   サポートチェックポイント[＃227](https://github.com/pingcap/tidb-tools/pull/227)

## TiDB Ansible {#tidb-ansible}

-   ドキュメントのリファクタリングに従って tidb-ansible ドキュメント内のリンク更新します [＃740](https://github.com/pingcap/tidb-ansible/pull/740) [＃741](https://github.com/pingcap/tidb-ansible/pull/741)
-   `inventory.ini`ファイル内の`enable_slow_query_log`パラメータを削除し、スロークエリログをデフォルトで別のログファイルに出力します[＃742](https://github.com/pingcap/tidb-ansible/pull/742)
