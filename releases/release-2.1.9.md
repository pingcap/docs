---
title: TiDB 2.1.9 Release Notes
---

# TiDB 2.1.9 リリースノート {#tidb-2-1-9-release-notes}

発売日：2019年5月6日

TiDB バージョン: 2.1.9

TiDB Ansible バージョン: 2.1.9

## TiDB {#tidb}

-   符号なし型オーバーフロー時の`MAKETIME`関数の互換性を修正[#10089](https://github.com/pingcap/tidb/pull/10089)
-   場合によっては定数フォールディングによって引き起こされるスタック オーバーフローを修正しました[#10189](https://github.com/pingcap/tidb/pull/10189)
-   場合によってはエイリアスが存在する場合の`Update`の権限チェックの問題を修正[#10157](https://github.com/pingcap/tidb/pull/10157) 、 [#10326](https://github.com/pingcap/tidb/pull/10326)
-   DistSQL [#10197](https://github.com/pingcap/tidb/pull/10197)でのメモリ使用量の追跡と制御
-   照合順序を`utf8mb4_0900_ai_ci` [#10201](https://github.com/pingcap/tidb/pull/10201)として指定することをサポート
-   主キーが符号なしタイプ[#10209](https://github.com/pingcap/tidb/pull/10209)である場合の`MAX`関数の間違った結果の問題を修正
-   非厳密 SQL モード[#10254](https://github.com/pingcap/tidb/pull/10254)で NULL 値を NOT NULL 列に挿入できる問題を修正します。
-   `DISTINCT` [#10270](https://github.com/pingcap/tidb/pull/10270)に複数の列が存在する場合の`COUNT`関数の結果が間違っている問題を修正
-   `LOAD DATA`不規則な CSV ファイルを解析するときに発生するpanic問題を修正[#10269](https://github.com/pingcap/tidb/pull/10269)
-   外部結合キーと内部結合キーのタイプが`Index Lookup Join` [#10244](https://github.com/pingcap/tidb/pull/10244)で一致しない場合のオーバーフロー エラーを無視します。
-   場合によっては誤ってポイントゲットと判定されてしまう問題を修正[#10299](https://github.com/pingcap/tidb/pull/10299)
-   場合によっては時間タイプがタイムゾーンを変換しない場合の間違った結果の問題を修正します[#10345](https://github.com/pingcap/tidb/pull/10345)
-   TiDB の文字セットの大文字と小文字が一致しない場合がある問題を修正[#10354](https://github.com/pingcap/tidb/pull/10354)
-   演算子[#9166](https://github.com/pingcap/tidb/issues/9166)によって返される行数の制御をサポートします。
    -   選択と投影[#10110](https://github.com/pingcap/tidb/pull/10110)
    -   `StreamAgg` &amp; `HashAgg` [#10133](https://github.com/pingcap/tidb/pull/10133)
    -   `TableReader` &amp; `IndexReader` &amp; `IndexLookup` [#10169](https://github.com/pingcap/tidb/pull/10169)
-   遅いクエリログを改善する
    -   類似した SQL を区別するには`SQL Digest`を追加します[#10093](https://github.com/pingcap/tidb/pull/10093)
    -   スロークエリステートメントで使用される統計のバージョン情報を追加します[#10220](https://github.com/pingcap/tidb/pull/10220)
    -   スロークエリログ[#10246](https://github.com/pingcap/tidb/pull/10246)のステートメントのメモリ消費量を表示します。
    -   コプロセッサー関連情報の出力形式を調整して、pt-query-digest [#10300](https://github.com/pingcap/tidb/pull/10300)で解析できるようにします。
    -   遅いクエリステートメントの`#`文字の問題を修正[#10275](https://github.com/pingcap/tidb/pull/10275)
    -   低速クエリ ステートメントのメモリテーブルにいくつかの情報列を追加します[#10317](https://github.com/pingcap/tidb/pull/10317)
    -   低速クエリ ログ[#10310](https://github.com/pingcap/tidb/pull/10310)にトランザクションのコミット時間を追加します。
    -   一部の時刻形式が pt-query-digest [#10323](https://github.com/pingcap/tidb/pull/10323)で解析できない問題を修正

## PD {#pd}

-   GetOperator サービスのサポート[#1514](https://github.com/pingcap/pd/pull/1514)

## TiKV {#tikv}

-   リーダー[#4604](https://github.com/tikv/tikv/pull/4604)を転送する際の潜在的なクォーラム変更を修正

## ツール {#tools}

-   TiDBBinlog
    -   主キー列のunsigned int型のデータがマイナス[#574](https://github.com/pingcap/tidb-binlog/pull/574)のため、データレプリケーションが中断される問題を修正
    -   ダウンストリームが`pb`の場合、圧縮オプションを削除し、ダウンストリーム名を`pb`から`file`に変更します[#597](https://github.com/pingcap/tidb-binlog/pull/575)
    -   2.1.7 で導入されたReparoが間違った`UPDATE`ステートメント[#576](https://github.com/pingcap/tidb-binlog/pull/576)を生成するバグを修正
-   TiDB Lightning
    -   パーサー[#164](https://github.com/pingcap/tidb-lightning/pull/164)でカラムデータのビット型が正しく解析されないバグを修正
    -   行 ID またはデフォルトの列値[#174](https://github.com/pingcap/tidb-lightning/pull/174)を使用して、ダンプ ファイル内の不足している列データを埋めます。
    -   一部の SST ファイルのインポートに失敗しても、成功したインポート結果が返されるというインポーターのバグを修正しました[#4566](https://github.com/tikv/tikv/pull/4566)
    -   SST ファイルを TiKV [#4607](https://github.com/tikv/tikv/pull/4607)にアップロードする際のインポーターでの速度制限設定のサポート
    -   インポーター RocksDB SST 圧縮方式を`lz4`に変更して、CPU 消費量を削減します[#4624](https://github.com/tikv/tikv/pull/4624)
-   同期差分インスペクター
    -   サポートチェックポイント[#227](https://github.com/pingcap/tidb-tools/pull/227)

## TiDB Ansible {#tidb-ansible}

-   ドキュメントのリファクタリング[#740](https://github.com/pingcap/tidb-ansible/pull/740) 、 [#741](https://github.com/pingcap/tidb-ansible/pull/741)に従って tidb-ansible ドキュメントのリンクを更新します。
-   `inventory.ini`ファイルの`enable_slow_query_log`パラメータを削除し、デフォルトでスロー クエリ ログを別のログ ファイルに出力します[#742](https://github.com/pingcap/tidb-ansible/pull/742)
