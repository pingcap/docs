---
title: TiDB 3.0.0 Beta.1 Release Notes
---

# TiDB 3.0.0 Beta.1 リリースノート {#tidb-3-0-0-beta-1-release-notes}

リリース日：2019年3月26日

TiDB バージョン: 3.0.0-beta.1

TiDB アンシブル バージョン: 3.0.0-beta.1

## 概要 {#overview}

2019 年 3 月 26 日に、TiDB 3.0.0 Beta.1 がリリースされました。対応する TiDB Ansible のバージョンは 3.0.0 Beta.1 です。 TiDB 3.0.0 Beta と比較して、このリリースでは、安定性、使いやすさ、機能、SQL オプティマイザー、統計、および実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQL オプティマイザー
    -   `Sort Merge Join` [#9032](https://github.com/pingcap/tidb/pull/9037)を使用したデカルト積の計算をサポート
    -   Skyline Pruning をサポートし、実行計画が統計に過度に依存するのを防ぐいくつかのルールを使用します[#9337](https://github.com/pingcap/tidb/pull/9337)

    <!---->

    -   サポート窓口機能
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

    -   列とハンドル列[#9315](https://github.com/pingcap/tidb/pull/9315)の間の順序相関を示す統計の種類を追加します。
-   SQL 実行エンジン
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
    -   現在の TiDB インスタンスの情報を取得するための`/debug/zip` HTTP インターフェイスを追加します[#9651](https://github.com/pingcap/tidb/pull/9651)
    -   PumpまたはDrainerのステータスをチェックするための`show pump status`および`show drainer status` SQL ステートメントのサポート[#9456](https://github.com/pingcap/tidb/pull/9456)
    -   SQL ステートメントを使用したPumpまたはDrainerのステータスの変更のサポート[#9789](https://github.com/pingcap/tidb/pull/9789)
    -   遅い SQL ステートメントを簡単に追跡できるように、SQL テキストへの HASH フィンガープリントの追加をサポート[#9662](https://github.com/pingcap/tidb/pull/9662)
    -   binlogの有効化状態を制御するために、 `log_bin`システム変数 (デフォルトでは「0」) を追加します。現在の状態の確認のみをサポート[#9343](https://github.com/pingcap/tidb/pull/9343)
    -   構成ファイル[#9864](https://github.com/pingcap/tidb/pull/9864)を使用した送信binlog戦略の管理のサポート
    -   `INFORMATION_SCHEMA.SLOW_QUERY`メモリテーブルを使用したスロー ログのクエリのサポート[#9290](https://github.com/pingcap/tidb/pull/9290)
    -   TiDB に表示される MySQL のバージョンを 5.7.10 から 5.7.25 に変更する[#9553](https://github.com/pingcap/tidb/pull/9553)
    -   ツールによる簡単な収集と分析のために[ログ形式](https://github.com/tikv/rfcs/blob/master/text/0018-unified-log-format.md)を統合する
    -   実際のデータ量と統計に基づく推定データ量の差を記録する監視項目を`high_error_rate_feedback_total`追加[#9209](https://github.com/pingcap/tidb/pull/9209)
    -   データベース ディメンションに QPS 監視項目を追加します。これは、構成項目[#9151](https://github.com/pingcap/tidb/pull/9151)を使用して有効にすることができます。
-   DDL
    -   `ddl_error_count_limit`グローバル変数 (デフォルトでは「512」) を追加して、DDL タスクの再試行回数を制限します (この回数が制限を超えると、DDL タスクはキャンセルされます) [#9295](https://github.com/pingcap/tidb/pull/9295)
    -   ALTER ALGORITHM `INPLACE` / `INSTANT` [#8811](https://github.com/pingcap/tidb/pull/8811)をサポート
    -   `SHOW CREATE VIEW`ステートメント[#9309](https://github.com/pingcap/tidb/pull/9309)をサポート
    -   `SHOW CREATE USER`ステートメント[#9240](https://github.com/pingcap/tidb/pull/9240)をサポート

## PD {#pd}

-   ツールによる簡単な収集と分析のために[ログ形式](https://github.com/tikv/rfcs/blob/master/text/0018-unified-log-format.md)を統合する
-   シミュレーター
    -   店舗ごとに異なるハートビート間隔をサポート[#1418](https://github.com/pingcap/pd/pull/1418)
    -   データのインポートに関するケースを追加する[#1263](https://github.com/pingcap/pd/pull/1263)
-   ホットスポットのスケジューリングを構成可能にする[#1412](https://github.com/pingcap/pd/pull/1412)
-   以前のストア ID [#1429](https://github.com/pingcap/pd/pull/1429)を置き換えるディメンション監視項目としてストア アドレスを追加します。
-   `GetStores`オーバーヘッドを最適化してリージョン検査サイクルを高速化する[#1410](https://github.com/pingcap/pd/pull/1410)
-   Tombstone Store [#1472](https://github.com/pingcap/pd/pull/1472)を削除するためのインターフェイスを追加します。

## TiKV {#tikv}

-   コプロセッサー計算実行フレームワークを最適化し、TableScan セクションを実装すると、Single TableScan のパフォーマンスが 5% ~ 30% 向上します。
    -   `BatchRows`行`BatchColumn`列[#3660](https://github.com/tikv/tikv/pull/3660)の定義を実装する
    -   `VectorLike`を実装して、同じ方法でエンコードされたデータとデコードされたデータへのアクセスをサポートする[#4242](https://github.com/tikv/tikv/pull/4242)
    -   インターフェイスに`BatchExecutor`を定義し、リクエストを`BatchExecutor` [#4243](https://github.com/tikv/tikv/pull/4243)に変換する方法を実装する
    -   式ツリーを RPN 形式に変換する実装[#4329](https://github.com/tikv/tikv/pull/4329)
    -   `BatchTableScanExecutor`ベクトル化演算子を実装して計算を高速化[#4351](https://github.com/tikv/tikv/pull/4351)
-   ツールによる簡単な収集と分析のために[ログ形式](https://github.com/tikv/rfcs/blob/master/text/0018-unified-log-format.md)を統合する
-   ローカル リーダーを使用した Raw Read インターフェイスでの読み取りのサポート[#4222](https://github.com/tikv/tikv/pull/4222)
-   構成情報に関するメトリックを追加する[#4206](https://github.com/tikv/tikv/pull/4206)
-   バウンド[#4255](https://github.com/tikv/tikv/pull/4255)を超えるキーに関するメトリクスを追加
-   バインドされたエラーを超えるキーに遭遇したときにpanicを制御するか、エラーを返すオプションを追加します[#4254](https://github.com/tikv/tikv/pull/4254)
-   `INSERT`操作のサポートを追加し、キーが存在しない場合にのみ事前書き込みが成功するようにし、 `Batch Get` [#4085](https://github.com/tikv/tikv/pull/4085)を排除します。
-   バッチ システム[#4200](https://github.com/tikv/tikv/pull/4200)でより公正なバッチ戦略を使用する
-   tikv-ctl [#3825](https://github.com/tikv/tikv/pull/3825)で Raw スキャンをサポート

## ツール {#tools}

-   TiDBBinlog
    -   Kafka からのbinlog の読み取りをサポートする Arbiter ツールを追加し、データを MySQL にレプリケートします。
    -   レプリケートする必要のないファイルのフィルタリングをサポート
    -   生成された列の複製をサポート
-   雷
    -   TiKV の定期的なレベル 1 コンパクションの無効化をサポートし、TiKV クラスターのバージョンが 2.1.4 以降の場合、レベル 1 コンパクションはインポート モードで自動的に実行されます[#119](https://github.com/pingcap/tidb-lightning/pull/119) , [#4199](https://github.com/tikv/tikv/pull/4199)
    -   `table_concurrency`構成項目を追加して、インポート エンジンの数を制限し (デフォルトでは「16」)、インポーターのディスク領域を使いすぎないようにします[#119](https://github.com/pingcap/tidb-lightning/pull/119)
    -   中間状態の SST のディスクへの保存をサポートし、メモリ使用量を削減します[#4369](https://github.com/tikv/tikv/pull/4369)
    -   TiKV-Importer のインポート パフォーマンスを最適化し、大きなテーブルのデータとインデックスの個別インポートをサポートします[#132](https://github.com/pingcap/tidb-lightning/pull/132)
    -   CSV ファイルのインポートをサポート[#111](https://github.com/pingcap/tidb-lightning/pull/111)
-   データ複製比較ツール (sync-diff-inspector)
    -   比較するチャンクを分割するための TiDB 統計を使用したサポート[#197](https://github.com/pingcap/tidb-tools/pull/197)
    -   複数の列を使用してチャンクを分割して比較するサポート[#197](https://github.com/pingcap/tidb-tools/pull/197)
