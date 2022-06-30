---
title: TiDB 3.0.0 Beta.1 Release Notes
---

# TiDB3.0.0Beta.1リリースノート {#tidb-3-0-0-beta-1-release-notes}

発売日：2019年3月26日

TiDBバージョン：3.0.0-beta.1

TiDB Ansibleバージョン：3.0.0-beta.1

## 概要 {#overview}

2019年3月26日、TiDB3.0.0Beta.1がリリースされました。対応するTiDBAnsibleのバージョンは3.0.0Beta.1です。 TiDB 3.0.0 Betaと比較して、このリリースでは、安定性、使いやすさ、機能、SQLオプティマイザー、統計、および実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   `Sort Merge Join`を使用したデカルト積の計算をサポートし[＃9032](https://github.com/pingcap/tidb/pull/9037)
    -   実行プランが統計に過度に依存することを防ぐためのいくつかのルールを使用して、スカイラインプルーニングをサポートします[＃9337](https://github.com/pingcap/tidb/pull/9337)

    <!---->

    -   ウィンドウ関数のサポート
        -   [＃9682](https://github.com/pingcap/tidb/pull/9682) `NTILE`
        -   `LEAD` [＃9672](https://github.com/pingcap/tidb/pull/9672) `LAG`
        -   [＃9671](https://github.com/pingcap/tidb/pull/9671) `PERCENT_RANK`
        -   [＃9596](https://github.com/pingcap/tidb/pull/9596) `NTH_VALUE`
        -   [＃9619](https://github.com/pingcap/tidb/pull/9619) `CUME_DIST`
        -   `FIRST_VALUE` [＃9560](https://github.com/pingcap/tidb/pull/9560) `LAST_VALUE`
        -   `RANK` [＃9500](https://github.com/pingcap/tidb/pull/9500) `DENSE_RANK`
        -   [＃9450](https://github.com/pingcap/tidb/pull/9450) `RANGE FRAMED`
        -   [＃9358](https://github.com/pingcap/tidb/pull/9358) `ROW FRAMED`
        -   [＃9098](https://github.com/pingcap/tidb/pull/9098) `ROW NUMBER`

    <!---->

    -   列とハンドル列[＃9315](https://github.com/pingcap/tidb/pull/9315)の間の順序相関を示すタイプの統計を追加します。
-   SQL実行エンジン
    -   組み込み関数を追加する
        -   [＃7832](https://github.com/pingcap/tidb/pull/7832) `JSON_QUOTE`
        -   [＃9609](https://github.com/pingcap/tidb/pull/9609) `JSON_ARRAY_APPEND`
        -   [＃8931](https://github.com/pingcap/tidb/pull/8931) `JSON_MERGE_PRESERVE`
        -   [＃9252](https://github.com/pingcap/tidb/pull/9252) `BENCHMARK`
        -   [＃9087](https://github.com/pingcap/tidb/pull/9087) `COALESCE`
        -   [＃9261](https://github.com/pingcap/tidb/pull/9261) `NAME_CONST`

    <!---->

    -   クエリコンテキストに基づいてチャンクサイズを最適化し、SQLステートメントの実行時間とクラスタのリソース消費を削減します[＃6489](https://github.com/pingcap/tidb/issues/6489)
-   特権管理
    -   サポート`SET ROLE` [＃9581](https://github.com/pingcap/tidb/pull/9581) `CURRENT_ROLE`
    -   [＃9616](https://github.com/pingcap/tidb/pull/9616) `DROP ROLE`
    -   [＃9461](https://github.com/pingcap/tidb/pull/9461) `CREATE ROLE`
-   サーバ
    -   `/debug/zip`のHTTPインターフェースを追加して、現在のTiDBインスタンスの情報を取得します[＃9651](https://github.com/pingcap/tidb/pull/9651)
    -   `show pump status`および`show drainer status`のSQLステートメントをサポートして、ポンプまたはドレイナーのステータスを確認します[＃9456](https://github.com/pingcap/tidb/pull/9456)
    -   SQLステートメントを使用したPumpまたはDrainerステータスの変更のサポート[＃9789](https://github.com/pingcap/tidb/pull/9789)
    -   遅いSQLステートメントを簡単に追跡できるようにSQLテキストへのHASHフィンガープリントの追加をサポート[＃9662](https://github.com/pingcap/tidb/pull/9662)
    -   `log_bin`のシステム変数（デフォルトでは「0」）を追加して、binlogの有効化状態を制御します。現在の状態のチェックのみをサポート[＃9343](https://github.com/pingcap/tidb/pull/9343)
    -   構成ファイルを使用したbinlog送信戦略の管理のサポート[＃9864](https://github.com/pingcap/tidb/pull/9864)
    -   `INFORMATION_SCHEMA.SLOW_QUERY`メモリテーブル[＃9290](https://github.com/pingcap/tidb/pull/9290)を使用した低速ログのクエリのサポート
    -   TiDBに表示されるMySQLのバージョンを5.7.10から[＃9553](https://github.com/pingcap/tidb/pull/9553)に変更します。
    -   ツールによる収集と分析を容易にするために[ログ形式](https://github.com/tikv/rfcs/blob/master/text/2018-12-19-unified-log-format.md)を統合します
    -   `high_error_rate_feedback_total`の監視項目を追加して、統計に基づいて実際のデータ量と推定データ量の差を記録します[＃9209](https://github.com/pingcap/tidb/pull/9209)
    -   QPS監視項目をデータベースディメンションに追加します。これは、構成項目[＃9151](https://github.com/pingcap/tidb/pull/9151)を使用して有効にできます。
-   DDL
    -   `ddl_error_count_limit`のグローバル変数（デフォルトでは「512」）を追加して、DDLタスクの再試行回数を制限します（この回数が制限を超えると、DDLタスクはキャンセルされます） [＃9295](https://github.com/pingcap/tidb/pull/9295)
    -   ALTER [＃8811](https://github.com/pingcap/tidb/pull/8811) `INPLACE` `INSTANT`をサポート
    -   `SHOW CREATE VIEW`ステートメント[＃9309](https://github.com/pingcap/tidb/pull/9309)をサポートする
    -   `SHOW CREATE USER`ステートメント[＃9240](https://github.com/pingcap/tidb/pull/9240)をサポートする

## PD {#pd}

-   ツールによる収集と分析を容易にするために[ログ形式](https://github.com/tikv/rfcs/blob/master/text/2018-12-19-unified-log-format.md)を統合します
-   シミュレーター
    -   さまざまな店舗でさまざまな心拍間隔をサポートする[＃1418](https://github.com/pingcap/pd/pull/1418)
    -   データのインポートに関するケースを追加する[＃1263](https://github.com/pingcap/pd/pull/1263)
-   ホットスポットのスケジューリングを構成可能にする[＃1412](https://github.com/pingcap/pd/pull/1412)
-   以前のストア[＃1429](https://github.com/pingcap/pd/pull/1429)を置き換えるために、ディメンション監視アイテムとしてストアアドレスを追加します
-   `GetStores`のオーバーヘッドを最適化して、リージョンの検査サイクル[＃1410](https://github.com/pingcap/pd/pull/1410)をスピードアップします。
-   トゥームストーンストアを削除するためのインターフェイスを追加する[＃1472](https://github.com/pingcap/pd/pull/1472)

## TiKV {#tikv}

-   コプロセッサー計算実行フレームワークを最適化し、TableScanセクションを実装します。単一のTableScanのパフォーマンスが5％〜30％向上します。
    -   `BatchRows`行`BatchColumn`列の定義を実装する[＃3660](https://github.com/tikv/tikv/pull/3660)
    -   同じ方法でエンコードおよびデコードされたデータへのアクセスをサポートするために`VectorLike`を実装します[＃4242](https://github.com/tikv/tikv/pull/4242)
    -   インターフェースに`BatchExecutor`を定義し、リクエストを[＃4243](https://github.com/tikv/tikv/pull/4243)に変換する方法を実装し`BatchExecutor`
    -   式ツリーをRPN形式に変換する実装[＃4329](https://github.com/tikv/tikv/pull/4329)
    -   計算を高速化するために`BatchTableScanExecutor`のベクトル化演算子を実装します[＃4351](https://github.com/tikv/tikv/pull/4351)
-   ツールによる収集と分析を容易にするために[ログ形式](https://github.com/tikv/rfcs/blob/master/text/2018-12-19-unified-log-format.md)を統合します
-   ローカルリーダーを使用したRawReadインターフェイスでの読み取りのサポート[＃4222](https://github.com/tikv/tikv/pull/4222)
-   構成情報に関するメトリックを追加する[＃4206](https://github.com/tikv/tikv/pull/4206)
-   境界[＃4255](https://github.com/tikv/tikv/pull/4255)を超えるキーに関するメトリックを追加します
-   バインドされたエラーを超えるキーに遭遇したときにパニックを制御するか、エラーを返すオプションを追加します[＃4254](https://github.com/tikv/tikv/pull/4254)
-   `INSERT`操作のサポートを追加し、キーが存在しない場合にのみ事前書き込みを成功させ、 [＃4085](https://github.com/tikv/tikv/pull/4085)を削除し`Batch Get` 。
-   バッチシステム[＃4200](https://github.com/tikv/tikv/pull/4200)でより公平なバッチ戦略を使用する
-   tikv- [＃3825](https://github.com/tikv/tikv/pull/3825)でRawスキャンをサポートする

## ツール {#tools}

-   TiDB Binlog
    -   Kafkaからのbinlogの読み取りをサポートするアービターツールを追加し、データをMySQLに複製します
    -   複製する必要のないフィルタリングファイルをサポートする
    -   生成された列の複製をサポート
-   雷
    -   TiKVの定期的なレベル1圧縮の無効化をサポートし、TiKVクラスタのバージョンが2.1.4以降の場合、レベル1の圧縮はインポートモード[＃119](https://github.com/pingcap/tidb-lightning/pull/119)で自動的に実行され[＃4199](https://github.com/tikv/tikv/pull/4199) 。
    -   `table_concurrency`の構成アイテムを追加して、インポートエンジンの数（デフォルトでは「16」）を制限し、インポーターのディスク領域を使いすぎないようにします[＃119](https://github.com/pingcap/tidb-lightning/pull/119)
    -   メモリ使用量を削減するために、中間状態のSSTをディスクに保存することをサポートします[＃4369](https://github.com/tikv/tikv/pull/4369)
    -   TiKV-Importerのインポートパフォーマンスを最適化し、大きなテーブルのデータとインデックスの個別のインポートをサポートします[＃132](https://github.com/pingcap/tidb-lightning/pull/132)
    -   CSVファイルのインポートをサポート[＃111](https://github.com/pingcap/tidb-lightning/pull/111)
-   データ複製比較ツール（sync-diff-inspector）
    -   比較するチャンクを分割するためのTiDB統計の使用をサポート[＃197](https://github.com/pingcap/tidb-tools/pull/197)
    -   比較するチャンクを分割するために複数の列を使用することをサポート[＃197](https://github.com/pingcap/tidb-tools/pull/197)
