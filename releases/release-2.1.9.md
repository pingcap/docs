---
title: TiDB 2.1.9 Release Notes
---

# TiDB 2.1.9 リリースノート {#tidb-2-1-9-release-notes}

発売日：2019年5月6日

TiDB バージョン: 2.1.9

TiDB アンシブル バージョン: 2.1.9

## TiDB {#tidb}

-   符号なし型オーバーフロー時の`MAKETIME`関数の互換性を修正[#10089](https://github.com/pingcap/tidb/pull/10089)
-   場合によっては定数フォールディングによって引き起こされるスタック オーバーフローを修正します[#10189](https://github.com/pingcap/tidb/pull/10189)
-   場合によってはエイリアスが存在する場合の`Update`の権限チェックの問題を修正します[#10157](https://github.com/pingcap/tidb/pull/10157) 、 [#10326](https://github.com/pingcap/tidb/pull/10326)
-   DistSQL [#10197](https://github.com/pingcap/tidb/pull/10197)でのメモリ使用量の追跡と制御
-   照合順序を`utf8mb4_0900_ai_ci` [#10201](https://github.com/pingcap/tidb/pull/10201)としてサポート
-   主キーが Unsigned タイプ[#10209](https://github.com/pingcap/tidb/pull/10209)の場合の`MAX`関数の間違った結果の問題を修正
-   非厳密な SQL モード[#10254](https://github.com/pingcap/tidb/pull/10254)で、NOT NULL 列に NULL 値を挿入できる問題を修正します。
-   `DISTINCT` [#10270](https://github.com/pingcap/tidb/pull/10270)に複数の列が存在する場合の`COUNT`関数の間違った結果の問題を修正
-   `LOAD DATA`不規則な CSV ファイルを解析するときに発生したpanicの問題を修正します[#10269](https://github.com/pingcap/tidb/pull/10269)
-   `Index Lookup Join` [#10244](https://github.com/pingcap/tidb/pull/10244)で外部結合キーと内部結合キーの型が一致しない場合のオーバーフロー エラーを無視する
-   場合によっては文がポイントゲットと誤判定される問題を修正[#10299](https://github.com/pingcap/tidb/pull/10299)
-   時間タイプがタイム ゾーンを変換しない場合に間違った結果が返される問題を修正します[#10345](https://github.com/pingcap/tidb/pull/10345)
-   場合によっては TiDB 文字セットの大文字と小文字が一致しない問題を修正します[#10354](https://github.com/pingcap/tidb/pull/10354)
-   演算子[#9166](https://github.com/pingcap/tidb/issues/9166)によって返される行数の制御のサポート
    -   選択と投影[#10110](https://github.com/pingcap/tidb/pull/10110)
    -   `StreamAgg` &amp; `HashAgg` [#10133](https://github.com/pingcap/tidb/pull/10133)
    -   `TableReader` &amp; `IndexReader` &amp; `IndexLookup` [#10169](https://github.com/pingcap/tidb/pull/10169)
-   スロー クエリ ログを改善する
    -   同様の SQL を区別するために`SQL Digest`を追加します[#10093](https://github.com/pingcap/tidb/pull/10093)
    -   スロー クエリ ステートメントで使用される統計のバージョン情報を追加します[#10220](https://github.com/pingcap/tidb/pull/10220)
    -   スロー クエリ ログ[#10246](https://github.com/pingcap/tidb/pull/10246)でステートメントのメモリ消費量を表示する
    -   pt-query-digest [#10300](https://github.com/pingcap/tidb/pull/10300)で解析できるように、コプロセッサー関連情報の出力形式を調整します。
    -   遅いクエリ ステートメントでの`#`文字の問題を修正します[#10275](https://github.com/pingcap/tidb/pull/10275)
    -   低速クエリ ステートメントのメモリテーブルにいくつかの情報列を追加します[#10317](https://github.com/pingcap/tidb/pull/10317)
    -   スロー クエリ ログ[#10310](https://github.com/pingcap/tidb/pull/10310)にトランザクション コミット時間を追加します。
    -   pt-query-digest [#10323](https://github.com/pingcap/tidb/pull/10323)で一部の時刻形式を解析できない問題を修正

## PD {#pd}

-   GetOperator サービスのサポート[#1514](https://github.com/pingcap/pd/pull/1514)

## TiKV {#tikv}

-   リーダー[#4604](https://github.com/tikv/tikv/pull/4604)を転送するときのクォーラム変更の可能性を修正

## ツール {#tools}

-   TiDBBinlog
    -   主キー列のunsigned int型のデータがマイナス[#574](https://github.com/pingcap/tidb-binlog/pull/574)でデータ複製が中断される問題を修正
    -   ダウンストリームが`pb`場合の圧縮オプションを削除し、ダウンストリーム名を`pb`から`file` [#597](https://github.com/pingcap/tidb-binlog/pull/575)に変更します。
    -   2.1.7 で導入されたReparoが間違った`UPDATE`ステートメントを生成するバグを修正[#576](https://github.com/pingcap/tidb-binlog/pull/576)
-   TiDB Lightning
    -   列データのビット型がパーサーで正しく解析されないバグを修正[#164](https://github.com/pingcap/tidb-lightning/pull/164)
    -   行 ID またはデフォルトの列値[#174](https://github.com/pingcap/tidb-lightning/pull/174)を使用して、ダンプ ファイル内の不足している列データを埋めます。
    -   一部の SST ファイルのインポートに失敗するが、インポート結果が正常に返されるというインポーターのバグを修正します[#4566](https://github.com/tikv/tikv/pull/4566)
    -   SST ファイルを TiKV [#4607](https://github.com/tikv/tikv/pull/4607)にアップロードする際の Importer での速度制限の設定をサポート
    -   Importer RocksDB SST 圧縮方式を`lz4`に変更して、CPU 消費を削減します[#4624](https://github.com/tikv/tikv/pull/4624)
-   同期差分インスペクター
    -   サポート チェックポイント[#227](https://github.com/pingcap/tidb-tools/pull/227)

## TiDB アンシブル {#tidb-ansible}

-   ドキュメントのリファクタリングに従って、tidb-ansible ドキュメントのリンクを更新します[#740](https://github.com/pingcap/tidb-ansible/pull/740) 、 [#741](https://github.com/pingcap/tidb-ansible/pull/741)
-   `inventory.ini`ファイルの`enable_slow_query_log`パラメータを削除し、スロー クエリ ログをデフォルトで別のログ ファイルに出力します[#742](https://github.com/pingcap/tidb-ansible/pull/742)
