---
title: TiDB 3.0.0 Beta.1 Release Notes
summary: TiDB 3.0.0 Beta.1は2019年3月26日にリリースされ、安定性、ユーザビリティ、機能、SQLオプティマイザー、統計、実行エンジンが改善されました。このリリースには、さまざまなSQL関数のサポート、権限管理、サーバーの機能強化、DDLの改善、PDおよびTiKVの最適化が含まれています。TiDB Binlog、Lightning、データレプリケーション比較ツールなどのツールも、新機能と改善が追加されてアップデートされました。
---

# TiDB 3.0.0 ベータ.1 リリースノート {#tidb-3-0-0-beta-1-release-notes}

リリース日：2019年3月26日

TiDB バージョン: 3.0.0-beta.1

TiDB Ansible バージョン: 3.0.0-beta.1

## 概要 {#overview}

2019年3月26日にTiDB 3.0.0 Beta.1がリリースされました。対応するTiDB Ansibleバージョンは3.0.0 Beta.1です。TiDB 3.0.0 Betaと比較して、このリリースでは安定性、使いやすさ、機能、SQLオプティマイザー、統計、実行エンジンが大幅に向上しています。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   `Sort Merge Join` [＃9032](https://github.com/pingcap/tidb/pull/9037)を使用して直積を計算することをサポートします
    -   スカイラインプルーニングをサポートし、実行計画が統計情報に過度に依存しないようにするいくつかのルールを備えています[＃9337](https://github.com/pingcap/tidb/pull/9337)

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

    -   クエリコンテキストに基づいてChunkサイズを最適化し、SQL文の実行時間とクラスタのリソース消費を削減します[＃6489](https://github.com/pingcap/tidb/issues/6489)
-   権限管理
    -   サポート`SET ROLE`と`CURRENT_ROLE` [＃9581](https://github.com/pingcap/tidb/pull/9581)
    -   サポート`DROP ROLE` [＃9616](https://github.com/pingcap/tidb/pull/9616)
    -   サポート`CREATE ROLE` [＃9461](https://github.com/pingcap/tidb/pull/9461)
-   サーバ
    -   現在のTiDBインスタンス[＃9651](https://github.com/pingcap/tidb/pull/9651)の情報を取得するためのHTTPインターフェース`/debug/zip`を追加する
    -   PumpまたはDrainerのステータスを確認するためのSQL文`show pump status`と`show drainer status`サポートします[＃9456](https://github.com/pingcap/tidb/pull/9456)
    -   SQL文を使用してPumpまたはDrainerのステータスを変更する機能をサポート[＃9789](https://github.com/pingcap/tidb/pull/9789)
    -   遅いSQL文を簡単に追跡できるように、SQLテキストにHASHフィンガープリントを追加することをサポート[＃9662](https://github.com/pingcap/tidb/pull/9662)
    -   binlogの有効化状態を制御するための`log_bin`システム変数 (デフォルトでは &quot;0&quot;) を追加します。現在は状態の確認のみをサポートしています[＃9343](https://github.com/pingcap/tidb/pull/9343)
    -   設定ファイル[＃9864](https://github.com/pingcap/tidb/pull/9864)を使用して送信binlog戦略の管理をサポート
    -   `INFORMATION_SCHEMA.SLOW_QUERY`メモリテーブル[＃9290](https://github.com/pingcap/tidb/pull/9290)を使用してスローログのクエリをサポート
    -   TiDBに表示されるMySQLのバージョンを5.7.10から5.7.25に変更する[＃9553](https://github.com/pingcap/tidb/pull/9553)
    -   [ログ形式](https://github.com/tikv/rfcs/blob/master/text/0018-unified-log-format.md)統合してツールによる収集と分析を容易にする
    -   統計[＃9209](https://github.com/pingcap/tidb/pull/9209)に基づいて実際のデータ量と推定データ量の差を記録するための監視項目`high_error_rate_feedback_total`追加します。
    -   データベースディメンションにQPS監視項目を追加します。これは、構成項目[＃9151](https://github.com/pingcap/tidb/pull/9151)使用して有効にできます。
-   DDL
    -   DDLタスクの再試行回数を制限するために、 `ddl_error_count_limit`グローバル変数（デフォルトでは「512」）を追加します（この回数が制限を超えると、DDLタスクはキャンセルされます） [＃9295](https://github.com/pingcap/tidb/pull/9295)
    -   ALTER ALGORITHM `INPLACE` / `INSTANT` [＃8811](https://github.com/pingcap/tidb/pull/8811)をサポート
    -   `SHOW CREATE VIEW`ステートメント[＃9309](https://github.com/pingcap/tidb/pull/9309)支持する
    -   `SHOW CREATE USER`ステートメント[＃9240](https://github.com/pingcap/tidb/pull/9240)支持する

## PD {#pd}

-   [ログ形式](https://github.com/tikv/rfcs/blob/master/text/0018-unified-log-format.md)統合してツールによる収集と分析を容易にする
-   シミュレーター
    -   異なる店舗で異なるハートビート間隔をサポート[＃1418](https://github.com/pingcap/pd/pull/1418)
    -   データのインポートに関するケースを追加[＃1263](https://github.com/pingcap/pd/pull/1263)
-   ホットスポットのスケジュールを設定可能にする[＃1412](https://github.com/pingcap/pd/pull/1412)
-   以前の店舗ID [＃1429](https://github.com/pingcap/pd/pull/1429)を置き換えるために、ディメンション監視項目として店舗住所を追加します。
-   `GetStores`オーバーヘッドを最適化して、リージョン検査サイクル[＃1410](https://github.com/pingcap/pd/pull/1410)高速化します。
-   トゥームストーンストア[＃1472](https://github.com/pingcap/pd/pull/1472)を削除するためのインターフェースを追加する

## TiKV {#tikv}

-   コプロセッサーの計算実行フレームワークを最適化し、TableScanセクションを実装することで、単一のTableScanのパフォーマンスが5％〜30％向上しました。
    -   `BatchRows`行目と`BatchColumn`列目の[＃3660](https://github.com/tikv/tikv/pull/3660)の定義を実装する
    -   `VectorLike`実装して、エンコードされたデータとデコードされたデータに同じ方法でアクセスできるようにする[＃4242](https://github.com/tikv/tikv/pull/4242)
    -   `BatchExecutor`インターフェースに定義し、リクエストを`BatchExecutor` [＃4243](https://github.com/tikv/tikv/pull/4243)に変換する方法を実装する
    -   式ツリーをRPN形式に変換する実装[＃4329](https://github.com/tikv/tikv/pull/4329)
    -   計算を高速化するためにベクトル化演算子`BatchTableScanExecutor`実装する[＃4351](https://github.com/tikv/tikv/pull/4351)
-   [ログ形式](https://github.com/tikv/rfcs/blob/master/text/0018-unified-log-format.md)統合してツールによる収集と分析を容易にする
-   ローカルリーダーを使用してRaw Readインターフェース[＃4222](https://github.com/tikv/tikv/pull/4222)で読み取ることをサポート
-   構成情報に関するメトリックを追加する[＃4206](https://github.com/tikv/tikv/pull/4206)
-   境界[＃4255](https://github.com/tikv/tikv/pull/4255)を超えるキーに関するメトリックを追加する
-   キーの境界超過エラーが発生したときにpanicを制御するかエラーを返すオプションを追加します[＃4254](https://github.com/tikv/tikv/pull/4254)
-   `INSERT`操作のサポートを追加し、キーが存在しない場合にのみ事前書き込みを成功させ、 `Batch Get` [＃4085](https://github.com/tikv/tikv/pull/4085)を削除します。
-   バッチシステム[＃4200](https://github.com/tikv/tikv/pull/4200)でより公平なバッチ戦略を使用する
-   tikv-ctl [＃3825](https://github.com/tikv/tikv/pull/3825)で Raw スキャンをサポート

## ツール {#tools}

-   TiDBBinlog
    -   Kafka からbinlogを読み取り、データを MySQL に複製する Arbiter ツールを追加します。
    -   複製する必要のないファイルのフィルタリングをサポート
    -   生成された列の複製をサポート
-   稲妻
    -   TiKVの定期的なレベル1圧縮を無効にすることをサポートし、TiKVクラスタバージョンが2.1.4以降の場合、レベル1圧縮はインポートモード[＃119](https://github.com/pingcap/tidb-lightning/pull/119)で自動的に実行されます[＃4199](https://github.com/tikv/tikv/pull/4199)
    -   `table_concurrency`構成項目を追加して、インポートエンジンの数（デフォルトでは「16」）を制限し、インポーターのディスクスペース[＃119](https://github.com/pingcap/tidb-lightning/pull/119)過剰な使用を回避します。
    -   メモリ使用量を削減するために、中間状態SSTをディスクに保存することをサポート[＃4369](https://github.com/tikv/tikv/pull/4369)
    -   TiKV-Importer のインポートパフォーマンスを最適化し、大規模なテーブルのデータとインデックスの個別インポートをサポートします[＃132](https://github.com/pingcap/tidb-lightning/pull/132)
    -   CSVファイルのインポートをサポート[＃111](https://github.com/pingcap/tidb-lightning/pull/111)
-   データ複製比較ツール (sync-diff-inspector)
    -   TiDB 統計を使用して比較するチャンクを分割するサポート[＃197](https://github.com/pingcap/tidb-tools/pull/197)
    -   比較するチャンクを分割するために複数の列の使用をサポート[＃197](https://github.com/pingcap/tidb-tools/pull/197)
