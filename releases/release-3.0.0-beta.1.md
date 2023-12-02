---
title: TiDB 3.0.0 Beta.1 Release Notes
---

# TiDB 3.0.0 ベータ.1 リリースノート {#tidb-3-0-0-beta-1-release-notes}

リリース日：2019年3月26日

TiDB バージョン: 3.0.0-beta.1

TiDB Ansible バージョン: 3.0.0-beta.1

## 概要 {#overview}

2019 年 3 月 26 日に、TiDB 3.0.0 Beta.1 がリリースされました。対応する TiDB Ansible バージョンは 3.0.0 Beta.1 です。 TiDB 3.0.0 ベータと比較して、このリリースでは安定性、使いやすさ、機能、SQL オプティマイザー、統計、実行エンジンが大幅に向上しています。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   `Sort Merge Join` [#9032](https://github.com/pingcap/tidb/pull/9037)を使用したデカルト積の計算をサポート
    -   Skyline Pruning をサポートし、実行計画が統計に過度に依存することを防ぐいくつかのルールを備えています[#9337](https://github.com/pingcap/tidb/pull/9337)

    <!---->

    -   サポートウィンドウの機能
        -   `NTILE` [#9682](https://github.com/pingcap/tidb/pull/9682)
        -   `LEAD`と`LAG` [#9672](https://github.com/pingcap/tidb/pull/9672)
        -   `PERCENT_RANK` [#9671](https://github.com/pingcap/tidb/pull/9671)
        -   `NTH_VALUE` [#9596](https://github.com/pingcap/tidb/pull/9596)
        -   `CUME_DIST` [#9619](https://github.com/pingcap/tidb/pull/9619)
        -   `FIRST_VALUE`と`LAST_VALUE` [#9560](https://github.com/pingcap/tidb/pull/9560)
        -   `RANK`と`DENSE_RANK` [#9500](https://github.com/pingcap/tidb/pull/9500)
        -   `RANGE FRAMED` [#9450](https://github.com/pingcap/tidb/pull/9450)
        -   `ROW FRAMED` [#9358](https://github.com/pingcap/tidb/pull/9358)
        -   `ROW NUMBER` [#9098](https://github.com/pingcap/tidb/pull/9098)

    <!---->

    -   列とハンドル列[#9315](https://github.com/pingcap/tidb/pull/9315)の間の順序相関を示すタイプの統計を追加します。
-   SQL実行エンジン
    -   組み込み関数を追加する
        -   `JSON_QUOTE` [#7832](https://github.com/pingcap/tidb/pull/7832)
        -   `JSON_ARRAY_APPEND` [#9609](https://github.com/pingcap/tidb/pull/9609)
        -   `JSON_MERGE_PRESERVE` [#8931](https://github.com/pingcap/tidb/pull/8931)
        -   `BENCHMARK` [#9252](https://github.com/pingcap/tidb/pull/9252)
        -   `COALESCE` [#9087](https://github.com/pingcap/tidb/pull/9087)
        -   `NAME_CONST` [#9261](https://github.com/pingcap/tidb/pull/9261)

    <!---->

    -   クエリ コンテキストに基づいてChunkサイズを最適化し、SQL ステートメントの実行時間とクラスターのリソース消費を削減します[#6489](https://github.com/pingcap/tidb/issues/6489)
-   権限管理
    -   サポート`SET ROLE`および`CURRENT_ROLE` [#9581](https://github.com/pingcap/tidb/pull/9581)
    -   サポート`DROP ROLE` [#9616](https://github.com/pingcap/tidb/pull/9616)
    -   サポート`CREATE ROLE` [#9461](https://github.com/pingcap/tidb/pull/9461)
-   サーバ
    -   `/debug/zip`現在の TiDB インスタンスの情報を取得するための HTTP インターフェースを追加します[#9651](https://github.com/pingcap/tidb/pull/9651)
    -   PumpまたはDrainerのステータスを確認するための`show pump status`および`show drainer status` SQL ステートメントをサポートします[#9456](https://github.com/pingcap/tidb/pull/9456)
    -   SQL ステートメントを使用したPumpまたはDrainerのステータス変更のサポート[#9789](https://github.com/pingcap/tidb/pull/9789)
    -   遅い SQL ステートメントを簡単に追跡できるように、SQL テキストへの HASH フィンガープリントの追加をサポートします[#9662](https://github.com/pingcap/tidb/pull/9662)
    -   `log_bin`システム変数 (デフォルトでは「0」) を追加して、 binlogの有効状態を制御します。現在の状態のチェックのみをサポートします[#9343](https://github.com/pingcap/tidb/pull/9343)
    -   構成ファイル[#9864](https://github.com/pingcap/tidb/pull/9864)を使用した送信binlog戦略の管理のサポート
    -   `INFORMATION_SCHEMA.SLOW_QUERY`メモリテーブル[#9290](https://github.com/pingcap/tidb/pull/9290)を使用した低速ログのクエリのサポート
    -   TiDB に表示される MySQL バージョンを 5.7.10 から 5.7.25 に変更します[#9553](https://github.com/pingcap/tidb/pull/9553)
    -   [ログ形式](https://github.com/tikv/rfcs/blob/master/text/0018-unified-log-format.md)統合してツールによる収集と分析を容易にする
    -   実際のデータ量と統計に基づく推定データ量の差を記録する監視項目`high_error_rate_feedback_total`を追加[#9209](https://github.com/pingcap/tidb/pull/9209)
    -   データベース ディメンションに QPS 監視項目を追加します。これは、構成項目[#9151](https://github.com/pingcap/tidb/pull/9151)を使用して有効にできます。
-   DDL
    -   `ddl_error_count_limit`グローバル変数 (デフォルトでは「512」) を追加して、DDL タスクの再試行数を制限します (この数が制限を超えると、DDL タスクはキャンセルされます) [#9295](https://github.com/pingcap/tidb/pull/9295)
    -   ALTER Algorithm `INPLACE` / `INSTANT` [#8811](https://github.com/pingcap/tidb/pull/8811)をサポート
    -   `SHOW CREATE VIEW`ステートメント[#9309](https://github.com/pingcap/tidb/pull/9309)をサポートします
    -   `SHOW CREATE USER`ステートメント[#9240](https://github.com/pingcap/tidb/pull/9240)をサポートします

## PD {#pd}

-   [ログ形式](https://github.com/tikv/rfcs/blob/master/text/0018-unified-log-format.md)統合してツールによる収集と分析を容易にする
-   シミュレータ
    -   異なるストアで異なるハートビート間隔をサポート[#1418](https://github.com/pingcap/pd/pull/1418)
    -   データのインポートに関するケースを追加[#1263](https://github.com/pingcap/pd/pull/1263)
-   ホットスポットのスケジュールを構成可能にする[#1412](https://github.com/pingcap/pd/pull/1412)
-   店舗アドレスをディメンション監視項目として追加し、以前の店舗 ID [#1429](https://github.com/pingcap/pd/pull/1429)を置き換えます。
-   `GetStores`オーバーヘッドを最適化してリージョン検査サイクルを高速化します[#1410](https://github.com/pingcap/pd/pull/1410)
-   Tombstone Store [#1472](https://github.com/pingcap/pd/pull/1472)を削除するためのインターフェイスの追加

## TiKV {#tikv}

-   コプロセッサー計算実行フレームワークを最適化し、TableScan セクションを実装し、Single TableScan のパフォーマンスが 5% ～ 30% 向上しました。
    -   `BatchRows`行`BatchColumn`列の定義を実装する[#3660](https://github.com/tikv/tikv/pull/3660)
    -   エンコードされたデータとデコードされたデータへの同じ方法でのアクセスをサポートするために`VectorLike`を実装します[#4242](https://github.com/tikv/tikv/pull/4242)
    -   `BatchExecutor`からインターフェイスを定義し、リクエストを`BatchExecutor` [#4243](https://github.com/tikv/tikv/pull/4243)に変換する方法を実装します。
    -   式ツリーのRPN形式への変換の実装[#4329](https://github.com/tikv/tikv/pull/4329)
    -   `BatchTableScanExecutor`ベクトル化演算子を実装して計算を高速化する[#4351](https://github.com/tikv/tikv/pull/4351)
-   [ログ形式](https://github.com/tikv/rfcs/blob/master/text/0018-unified-log-format.md)統合してツールによる収集と分析を容易にする
-   Local Reader を使用した Raw Read インターフェイスでの読み取りのサポート[#4222](https://github.com/tikv/tikv/pull/4222)
-   構成情報に関するメトリックの追加[#4206](https://github.com/tikv/tikv/pull/4206)
-   境界[#4255](https://github.com/tikv/tikv/pull/4255)を超えるキーに関するメトリクスを追加します
-   キー超過エラー[#4254](https://github.com/tikv/tikv/pull/4254)が発生したときにpanicを制御するかエラーを返すオプションを追加します。
-   `INSERT`操作のサポートを追加し、キーが存在しない場合にのみ事前書き込みが成功するようにし、 `Batch Get` [#4085](https://github.com/tikv/tikv/pull/4085)を削除します。
-   バッチ システム[#4200](https://github.com/tikv/tikv/pull/4200)でより公平なバッチ戦略を使用する
-   tikv-ctl [#3825](https://github.com/tikv/tikv/pull/3825)での Raw スキャンのサポート

## ツール {#tools}

-   TiDBBinlog
    -   Kafka からのbinlogの読み取りをサポートする Arbiter ツールを追加し、データを MySQL にレプリケートします
    -   レプリケートする必要のないファイルのフィルタリングをサポート
    -   生成された列のレプリケートをサポート
-   稲妻
    -   TiKV の定期的なレベル 1 コンパクションの無効化をサポートし、TiKV クラスターのバージョンが 2.1.4 以降の場合、インポート モード[#119](https://github.com/pingcap/tidb-lightning/pull/119) 、 [#4199](https://github.com/tikv/tikv/pull/4199)でレベル 1 コンパクションが自動的に実行されます。
    -   `table_concurrency`構成項目を追加して、インポート エンジンの数 (デフォルトでは「16」) を制限し、インポーターのディスク領域の過剰使用を回避します[#119](https://github.com/pingcap/tidb-lightning/pull/119)
    -   メモリ使用量を削減するために、中間状態の SST をディスクに保存するサポート[#4369](https://github.com/tikv/tikv/pull/4369)
    -   TiKV-Importer のインポート パフォーマンスを最適化し、大きなテーブルのデータとインデックスの個別のインポートをサポートします[#132](https://github.com/pingcap/tidb-lightning/pull/132)
    -   CSV ファイルのインポートをサポート[#111](https://github.com/pingcap/tidb-lightning/pull/111)
-   データ複製比較ツール (sync-diff-inspector)
    -   TiDB 統計を使用した比較対象のチャンクの分割のサポート[#197](https://github.com/pingcap/tidb-tools/pull/197)
    -   複数の列を使用して比較するチャンクを分割するサポート[#197](https://github.com/pingcap/tidb-tools/pull/197)
