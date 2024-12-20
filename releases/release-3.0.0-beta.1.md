---
title: TiDB 3.0.0 Beta.1 Release Notes
summary: TiDB 3.0.0 Beta.1 は、安定性、使いやすさ、機能、SQL オプティマイザー、統計、実行エンジンが改善され、2019 年 3 月 26 日にリリースされました。このリリースには、さまざまな SQL関数のサポート、権限管理、サーバーの機能強化、DDL の改善、PD および TiKV の最適化が含まれています。TiDB Binlog、Lightning、データ レプリケーション比較ツールなどのツールも、新しい機能と改善を加えて更新されました。
---

# TiDB 3.0.0 Beta.1 リリースノート {#tidb-3-0-0-beta-1-release-notes}

リリース日：2019年3月26日

TiDB バージョン: 3.0.0-beta.1

TiDB Ansible バージョン: 3.0.0-beta.1

## 概要 {#overview}

2019 年 3 月 26 日に、TiDB 3.0.0 Beta.1 がリリースされました。対応する TiDB Ansible バージョンは 3.0.0 Beta.1 です。TiDB 3.0.0 Beta と比較して、このリリースでは、安定性、使いやすさ、機能、SQL オプティマイザー、統計、実行エンジンが大幅に改善されています。

## ティビ {#tidb}

-   SQL オプティマイザー
    -   `Sort Merge Join` [＃9032](https://github.com/pingcap/tidb/pull/9037)使用して直積を計算することをサポートする
    -   実行計画が統計に過度に依存しないようにするためのいくつかのルールを備えた Skyline Pruning をサポートします[＃9337](https://github.com/pingcap/tidb/pull/9337)

    <!---->

    -   ウィンドウ関数のサポート
        -   `NTILE` [＃9682](https://github.com/pingcap/tidb/pull/9682)
        -   `LEAD`と`LAG` [＃9672](https://github.com/pingcap/tidb/pull/9672)
        -   `PERCENT_RANK` [＃9671](https://github.com/pingcap/tidb/pull/9671)
        -   `NTH_VALUE` [＃9596](https://github.com/pingcap/tidb/pull/9596)
        -   `CUME_DIST` [＃9619](https://github.com/pingcap/tidb/pull/9619)
        -   `FIRST_VALUE`と`LAST_VALUE` [＃9560](https://github.com/pingcap/tidb/pull/9560)
        -   `RANK`と`DENSE_RANK` [＃9500](https://github.com/pingcap/tidb/pull/9500)
        -   `RANGE FRAMED` [＃9450](https://github.com/pingcap/tidb/pull/9450)
        -   `ROW FRAMED` [＃9358](https://github.com/pingcap/tidb/pull/9358)
        -   `ROW NUMBER` [＃9098](https://github.com/pingcap/tidb/pull/9098)

    <!---->

    -   列とハンドル列[＃9315](https://github.com/pingcap/tidb/pull/9315)の間の順序相関を示す統計の種類を追加します。
-   SQL実行エンジン
    -   組み込み関数を追加する
        -   `JSON_QUOTE` [＃7832](https://github.com/pingcap/tidb/pull/7832)
        -   `JSON_ARRAY_APPEND` [＃9609](https://github.com/pingcap/tidb/pull/9609)
        -   `JSON_MERGE_PRESERVE` [＃8931](https://github.com/pingcap/tidb/pull/8931)
        -   `BENCHMARK` [＃9252](https://github.com/pingcap/tidb/pull/9252)
        -   `COALESCE` [＃9087](https://github.com/pingcap/tidb/pull/9087)
        -   `NAME_CONST` [＃9261](https://github.com/pingcap/tidb/pull/9261)

    <!---->

    -   クエリコンテキストに基づいてChunkサイズを最適化し、SQL文の実行時間とクラスターのリソース消費を削減します[＃6489](https://github.com/pingcap/tidb/issues/6489)
-   権限管理
    -   サポート`SET ROLE`と`CURRENT_ROLE` [＃9581](https://github.com/pingcap/tidb/pull/9581)
    -   サポート`DROP ROLE` [＃9616](https://github.com/pingcap/tidb/pull/9616)
    -   サポート`CREATE ROLE` [＃9461](https://github.com/pingcap/tidb/pull/9461)
-   サーバ
    -   現在のTiDBインスタンス[＃9651](https://github.com/pingcap/tidb/pull/9651)の情報を取得するためのHTTPインターフェース`/debug/zip`を追加する
    -   PumpまたはDrainerのステータスを確認するためのSQL文`show pump status`と`show drainer status`をサポートします[＃9456](https://github.com/pingcap/tidb/pull/9456)
    -   SQL文を使用してPumpまたはDrainerのステータスを変更する機能をサポート[＃9789](https://github.com/pingcap/tidb/pull/9789)
    -   遅いSQL文を簡単に追跡できるように、SQLテキストにHASHフィンガープリントを追加することをサポート[＃9662](https://github.com/pingcap/tidb/pull/9662)
    -   binlogの有効化状態を制御するための`log_bin`システム変数 (デフォルトでは &quot;0&quot;) を追加します。現在は状態の確認のみをサポートしています[＃9343](https://github.com/pingcap/tidb/pull/9343)
    -   設定ファイル[＃9864](https://github.com/pingcap/tidb/pull/9864)を使用して送信binlog戦略の管理をサポート
    -   `INFORMATION_SCHEMA.SLOW_QUERY`メモリテーブル[＃9290](https://github.com/pingcap/tidb/pull/9290)使用してスローログのクエリをサポート
    -   TiDBに表示されるMySQLバージョンを5.7.10から5.7.25に変更する[＃9553](https://github.com/pingcap/tidb/pull/9553)
    -   [ログ形式](https://github.com/tikv/rfcs/blob/master/text/0018-unified-log-format.md)統合してツールによる収集と分析を容易にする
    -   統計[＃9209](https://github.com/pingcap/tidb/pull/9209)に基づいて実際のデータ量と推定データ量の差を記録するための監視項目`high_error_rate_feedback_total`を追加します。
    -   データベースディメンションにQPS監視項目を追加します。これは、構成項目[＃9151](https://github.com/pingcap/tidb/pull/9151)を使用して有効にできます。
-   DDL
    -   DDLタスクの再試行回数を制限するために、 `ddl_error_count_limit`グローバル変数（デフォルトでは「512」）を追加します（この回数が制限を超えると、DDLタスクはキャンセルされます） [＃9295](https://github.com/pingcap/tidb/pull/9295)
    -   ALTER ALGORITHM `INPLACE` / `INSTANT` [＃8811](https://github.com/pingcap/tidb/pull/8811)をサポート
    -   `SHOW CREATE VIEW`ステートメント[＃9309](https://github.com/pingcap/tidb/pull/9309)支持する
    -   `SHOW CREATE USER`ステートメント[＃9240](https://github.com/pingcap/tidb/pull/9240)支持する

## PD {#pd}

-   [ログ形式](https://github.com/tikv/rfcs/blob/master/text/0018-unified-log-format.md)統合してツールによる収集と分析を容易にする
-   シミュレーター
    -   異なるストアで異なるハートビート間隔をサポート[＃1418](https://github.com/pingcap/pd/pull/1418)
    -   データのインポートに関する事例を追加[＃1263](https://github.com/pingcap/pd/pull/1263)
-   ホットスポットのスケジュールを設定可能にする[＃1412](https://github.com/pingcap/pd/pull/1412)
-   以前のストアID [＃1429](https://github.com/pingcap/pd/pull/1429)置き換えるために、ディメンション監視項目としてストアアドレスを追加します。
-   `GetStores`オーバーヘッドを最適化して、リージョン検査サイクル[＃1410](https://github.com/pingcap/pd/pull/1410)を高速化します。
-   トゥームストーンストア[＃1472](https://github.com/pingcap/pd/pull/1472)を削除するためのインターフェースを追加する

## ティクヴ {#tikv}

-   コプロセッサーの計算実行フレームワークを最適化し、TableScanセクションを実装することで、単一のTableScanのパフォーマンスが5%～30%向上しました。
    -   `BatchRows`行目と`BatchColumn`列目[＃3660](https://github.com/tikv/tikv/pull/3660)の定義を実装する
    -   `VectorLike`実装して、エンコードされたデータとデコードされたデータに同じ方法でアクセスできるようにする[＃4242](https://github.com/tikv/tikv/pull/4242)
    -   `BatchExecutor`をインターフェースに定義し、リクエストを`BatchExecutor` [＃4243](https://github.com/tikv/tikv/pull/4243)に変換する方法を実装する
    -   式ツリーをRPN形式に変換する実装[＃4329](https://github.com/tikv/tikv/pull/4329)
    -   計算を高速化するために`BatchTableScanExecutor`ベクトル化演算子を実装する[＃4351](https://github.com/tikv/tikv/pull/4351)
-   [ログ形式](https://github.com/tikv/rfcs/blob/master/text/0018-unified-log-format.md)統合してツールによる収集と分析を容易にする
-   ローカルリーダーを使用してRaw Readインターフェース[＃4222](https://github.com/tikv/tikv/pull/4222)で読み取ることをサポート
-   構成情報に関するメトリックを追加する[＃4206](https://github.com/tikv/tikv/pull/4206)
-   境界[＃4255](https://github.com/tikv/tikv/pull/4255)超えるキーに関するメトリックを追加します
-   キーの境界超過エラーが発生したときにpanicを制御するかエラーを返すオプションを追加します[＃4254](https://github.com/tikv/tikv/pull/4254)
-   `INSERT`操作のサポートを追加し、キーが存在しない場合にのみ事前書き込みを成功させ、 `Batch Get` [＃4085](https://github.com/tikv/tikv/pull/4085)を削除します。
-   バッチシステム[＃4200](https://github.com/tikv/tikv/pull/4200)でより公平なバッチ戦略を使用する
-   tikv-ctl [＃3825](https://github.com/tikv/tikv/pull/3825)で Raw スキャンをサポート

## ツール {#tools}

-   TiDBBinlog
    -   Kafka からbinlog を読み取り、データを MySQL に複製する Arbiter ツールを追加します。
    -   複製する必要のないファイルのフィルタリングをサポート
    -   生成された列の複製をサポート
-   稲妻
    -   TiKV の定期的なレベル 1 圧縮を無効にすることをサポートし、TiKV クラスターのバージョンが 2.1.4 以降の場合、インポート モード[＃119](https://github.com/pingcap/tidb-lightning/pull/119)でレベル 1 圧縮が自動的に実行されます[＃4199](https://github.com/tikv/tikv/pull/4199)
    -   `table_concurrency`構成項目を追加して、インポート エンジンの数 (デフォルトでは「16」) を制限し、インポーターのディスク領域[＃119](https://github.com/pingcap/tidb-lightning/pull/119)の過剰使用を回避します。
    -   メモリ使用量を削減するために、中間状態のSSTをディスクに保存することをサポートします[＃4369](https://github.com/tikv/tikv/pull/4369)
    -   TiKV-Importer のインポートパフォーマンスを最適化し、大規模なテーブルのデータとインデックスの個別インポートをサポートします[＃132](https://github.com/pingcap/tidb-lightning/pull/132)
    -   CSVファイルのインポートをサポート[＃111](https://github.com/pingcap/tidb-lightning/pull/111)
-   データ複製比較ツール (sync-diff-inspector)
    -   TiDB 統計を使用して比較するチャンクを分割するサポート[＃197](https://github.com/pingcap/tidb-tools/pull/197)
    -   比較するチャンクを分割するために複数の列の使用をサポート[＃197](https://github.com/pingcap/tidb-tools/pull/197)
