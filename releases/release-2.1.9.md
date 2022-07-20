---
title: TiDB 2.1.9 Release Notes
---

# TiDB2.1.9リリースノート {#tidb-2-1-9-release-notes}

発売日：2019年5月6日

TiDBバージョン：2.1.9

TiDB Ansibleバージョン：2.1.9

## TiDB {#tidb}

-   符号なし型がオーバーフローした場合の`MAKETIME`関数の互換性を修正[＃10089](https://github.com/pingcap/tidb/pull/10089)
-   場合によっては定数畳み込みによって引き起こされるスタックオーバーフローを修正します[＃10189](https://github.com/pingcap/tidb/pull/10189)
-   場合によってはエイリアスが存在する場合の`Update`の特権チェックの問題を修正し[＃10326](https://github.com/pingcap/tidb/pull/10326) [＃10157](https://github.com/pingcap/tidb/pull/10157)
-   [＃10197](https://github.com/pingcap/tidb/pull/10197)でのメモリ使用量の追跡と制御
-   照合順序を`utf8mb4_0900_ai_ci`として指定することを[＃10201](https://github.com/pingcap/tidb/pull/10201)
-   主キーが符号なしタイプ[＃10209](https://github.com/pingcap/tidb/pull/10209)の場合の`MAX`関数の誤った結果の問題を修正します
-   非厳密SQLモード[＃10254](https://github.com/pingcap/tidb/pull/10254)でNULL値がNOTNULL列に挿入される可能性がある問題を修正します。
-   `DISTINCT` [＃10270](https://github.com/pingcap/tidb/pull/10270)に複数の列が存在する場合の、 `COUNT`関数の誤った結果の問題を修正します。
-   `LOAD DATA`が不規則なCSVファイルを解析するときに発生したpanicの問題を修正します[＃10269](https://github.com/pingcap/tidb/pull/10269)
-   [＃10244](https://github.com/pingcap/tidb/pull/10244)で外部結合キータイプと内部結合キータイプが矛盾している場合のオーバーフローエラーを無視し`Index Lookup Join` 。
-   ステートメントが誤ってポイントと判断される問題を修正します-場合によっては[＃10299](https://github.com/pingcap/tidb/pull/10299)を取得します
-   場合によっては、タイムタイプがタイムゾーンを変換しない場合の誤った結果の問題を修正します[＃10345](https://github.com/pingcap/tidb/pull/10345)
-   TiDB文字セットのケースが一貫していない場合がある問題を修正します[＃10354](https://github.com/pingcap/tidb/pull/10354)
-   演算子[＃9166](https://github.com/pingcap/tidb/issues/9166)によって返される行数の制御をサポートします
    -   選択と投影[＃10110](https://github.com/pingcap/tidb/pull/10110)
    -   `StreamAgg` ＆ `HashAgg` [＃10133](https://github.com/pingcap/tidb/pull/10133)
    -   `TableReader` ＆ `IndexReader` ＆ `IndexLookup` [＃10169](https://github.com/pingcap/tidb/pull/10169)
-   遅いクエリログを改善する
    -   類似のSQL3を区別するために`SQL Digest`を追加し[＃10093](https://github.com/pingcap/tidb/pull/10093)
    -   低速クエリステートメントで使用される統計のバージョン情報を追加する[＃10220](https://github.com/pingcap/tidb/pull/10220)
    -   遅いクエリログ[＃10246](https://github.com/pingcap/tidb/pull/10246)にステートメントのメモリ消費量を表示する
    -   コプロセッサー関連情報の出力形式を調整して、pt-query- [＃10300](https://github.com/pingcap/tidb/pull/10300)で解析できるようにします。
    -   遅いクエリステートメントの`#`文字の問題を修正[＃10275](https://github.com/pingcap/tidb/pull/10275)
    -   遅いクエリステートメントのメモリテーブルにいくつかの情報列を追加します[＃10317](https://github.com/pingcap/tidb/pull/10317)
    -   トランザクションコミット時間を追加して、クエリログ[＃10310](https://github.com/pingcap/tidb/pull/10310)を遅くします
    -   一部の時間形式がpt-query-digest1で解析できない問題を修正し[＃10323](https://github.com/pingcap/tidb/pull/10323)

## PD {#pd}

-   GetOperatorサービスをサポートする[＃1514](https://github.com/pingcap/pd/pull/1514)

## TiKV {#tikv}

-   リーダー[＃4604](https://github.com/tikv/tikv/pull/4604)を転送する際の潜在的なクォーラムの変更を修正

## ツール {#tools}

-   TiDB Binlog
    -   unsigned intタイプの主キー列のデータがマイナス[＃574](https://github.com/pingcap/tidb-binlog/pull/574)であるために、データ複製が中断される問題を修正します。
    -   ダウンストリームが`pb`の場合は圧縮オプションを削除し、ダウンストリーム名を`pb`から[＃597](https://github.com/pingcap/tidb-binlog/pull/575)に変更し`file` 。
    -   2.1.7で導入されたReparoが間違った`UPDATE`ステートメントを生成するバグを修正します[＃576](https://github.com/pingcap/tidb-binlog/pull/576)
-   TiDB Lightning
    -   列データのビットタイプがパーサーによって誤って解析されるバグを修正します[＃164](https://github.com/pingcap/tidb-lightning/pull/164)
    -   行IDまたはデフォルトの列値[＃174](https://github.com/pingcap/tidb-lightning/pull/174)を使用して、不足している列データをダンプファイルに入力します
    -   一部のSSTファイルがインポートに失敗するが、インポート結果[＃4566](https://github.com/tikv/tikv/pull/4566)が正常に返されるというインポーターのバグを修正します。
    -   SSTファイルを[＃4607](https://github.com/tikv/tikv/pull/4607)にアップロードする際のインポーターでの速度制限の設定をサポート
    -   Importer RocksDB SST圧縮方式を`lz4`に変更して、CPU消費量を削減します[＃4624](https://github.com/tikv/tikv/pull/4624)
-   sync-diff-inspector
    -   チェックポイント[＃227](https://github.com/pingcap/tidb-tools/pull/227)をサポート

## TiDB Ansible {#tidb-ansible}

-   ドキュメントのリファクタリングに従って、tidb-ansibleドキュメントのリンクを更新し[＃741](https://github.com/pingcap/tidb-ansible/pull/741) [＃740](https://github.com/pingcap/tidb-ansible/pull/740)
-   `inventory.ini`ファイルの`enable_slow_query_log`パラメータを削除し、デフォルトで低速クエリログを別のログファイルに出力します[＃742](https://github.com/pingcap/tidb-ansible/pull/742)
