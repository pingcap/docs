---
title: TiDB 3.0.1 Release Notes
---

# TiDB3.0.1リリースノート {#tidb-3-0-1-release-notes}

発売日：2019年7月16日

TiDBバージョン：3.0.1

TiDB Ansibleバージョン：3.0.1

## TiDB {#tidb}

-   `MAX_EXECUTION_TIME`機能[＃11026](https://github.com/pingcap/tidb/pull/11026)のサポートを追加します
-   `tidb_wait_split_region_finish_backoff`セッション変数を追加して、リージョン[＃11166](https://github.com/pingcap/tidb/pull/11166)の分割のバックオフ時間を制御します。
-   負荷に基づいて自動インクリメントIDによって割り当てられた増分ギャップの自動調整をサポートし[＃11006](https://github.com/pingcap/tidb/pull/11006) 。増分ギャップの自動調整範囲は1000〜20000001です。
-   プラグインを動的に有効または無効にするには、 `ADMIN PLUGINS ENABLE` / `ADMIN PLUGINS DISABLE`ステートメントを追加します[＃11157](https://github.com/pingcap/tidb/pull/11157)
-   監査プラグイン[＃11013](https://github.com/pingcap/tidb/pull/11013)にセッション接続情報を追加します
-   リージョンを分割する期間中のデフォルトの動作を変更して、PDがスケジューリングを終了するのを待ちます[＃11166](https://github.com/pingcap/tidb/pull/11166)
-   場合によっては誤った結果を回避するために、ウィンドウ関数がプランキャッシュの準備にキャッシュされないようにします[＃11048](https://github.com/pingcap/tidb/pull/11048)
-   保存された生成列の定義を変更することから`ALTER`ステートメントを禁止する[＃11068](https://github.com/pingcap/tidb/pull/11068)
-   仮想生成列を保存された生成列に変更することを禁止する[＃11068](https://github.com/pingcap/tidb/pull/11068)
-   生成された列式をインデックス[＃11068](https://github.com/pingcap/tidb/pull/11068)で変更することを禁止します
-   ARM64アーキテクチャでのTiDBのコンパイルのサポート[＃11150](https://github.com/pingcap/tidb/pull/11150)
-   データベースまたはテーブルの照合順序の変更をサポートしますが、データベース/テーブルの文字セットはUTF-8または[＃11086](https://github.com/pingcap/tidb/pull/11086)である必要があります。
-   `UPDATE … SELECT`ステートメントの`SELECT`サブクエリが`UPDATE`式の列の解析に失敗し、列が誤ってプルーニングされた場合にエラーが報告される問題を修正します[＃11252](https://github.com/pingcap/tidb/pull/11252)
-   列が複数回クエリされ、ポイントクエリ中に返された結果がNULLである場合に発生するpanicの問題を修正します[＃11226](https://github.com/pingcap/tidb/pull/11226)
-   `RAND`関数[＃11169](https://github.com/pingcap/tidb/pull/11169)を使用するときに非スレッドセーフ`rand.Rand`によって引き起こされるデータ競合の問題を修正します
-   SQLステートメントのメモリ使用量がしきい値を超えているが、 `oom-action="cancel"`が構成されている場合にこのステートメントの実行がキャンセルされず、返される結果が正しくないというバグを修正します[＃11004](https://github.com/pingcap/tidb/pull/11004)
-   MemTrackerのメモリ使用量が正しくクリーンアップされなかったために`SHOW PROCESSLIST`がメモリ使用量が`0`ではないことを示す問題を修正します[＃10970](https://github.com/pingcap/tidb/pull/10970)
-   整数と非整数を比較した結果が正しくない場合があるというバグを修正します[＃11194](https://github.com/pingcap/tidb/pull/11194)
-   テーブルパーティションのクエリに明示的なトランザクションの述語が含まれている場合にクエリ結果が正しくないというバグを修正します[＃11196](https://github.com/pingcap/tidb/pull/11196)
-   `infoHandle`が[＃11022](https://github.com/pingcap/tidb/pull/11022)である可能性があるため、DDLジョブのpanicの問題を修正し`NULL`
-   クエリされた列がサブクエリで参照されておらず、ネストされた集計クエリを実行すると誤ってプルーニングされるため、クエリ結果が正しくない問題を修正します[＃11020](https://github.com/pingcap/tidb/pull/11020)
-   `Sleep`関数が時間[＃11028](https://github.com/pingcap/tidb/pull/11028)の`KILL`ステートメントに応答しない問題を修正します。
-   `SHOW PROCESSLIST`コマンドで表示される`DB`列と`INFO`列がMySQL7と互換性がないという問題を修正し[＃11003](https://github.com/pingcap/tidb/pull/11003)
-   `skip-grant-table=true`が構成されている場合に`FLUSH PRIVILEGES`ステートメントによって引き起こされるシステムpanicの問題を修正します[＃11027](https://github.com/pingcap/tidb/pull/11027)
-   テーブルの主キーが`UNSIGNED`整数[＃11099](https://github.com/pingcap/tidb/pull/11099)の場合、 `FAST ANALYZE`によって収集された主キーの統計が正しくない問題を修正します。
-   「無効なキー」エラーが`FAST ANALYZE`ステートメントによって報告される場合があるという問題を修正します[＃11098](https://github.com/pingcap/tidb/pull/11098)
-   列のデフォルト値として`CURRENT_TIMESTAMP`が使用され、float精度が指定されている場合、 `SHOW CREATE TABLE`ステートメントによって示される精度が不完全であるという問題を修正します[＃11088](https://github.com/pingcap/tidb/pull/11088)
-   ウィンドウ関数がエラーを報告するときに関数名が小文字にならない問題を修正して、 [＃11118](https://github.com/pingcap/tidb/pull/11118)と互換性を持たせる
-   TiDBがTiKVに接続できず、TiKVクライアントバッチgRPCのバックグラウンドスレッドがパニックになった後、サービスを提供できないという問題を修正します[＃11101](https://github.com/pingcap/tidb/pull/11101)
-   文字列[＃11044](https://github.com/pingcap/tidb/pull/11044)のコピーが浅いため、変数が`SetVar`だけ正しく設定されない問題を修正します。
-   `INSERT … ON DUPLICATE`ステートメントがテーブルパーティション[＃11231](https://github.com/pingcap/tidb/pull/11231)に適用されると、実行が失敗し、エラーが報告される問題を修正します。
-   悲観的ロック（実験的機能）
    -   悲観的ロックを使用してポイントクエリが実行され、返されたデータが空の場合に、行のロックが無効であるために誤った結果が返される問題を修正します[＃10976](https://github.com/pingcap/tidb/pull/10976)
    -   クエリ[＃11015](https://github.com/pingcap/tidb/pull/11015)でペシミスティックロックを使用すると、 `SELECT … FOR UPDATE`が正しいTSOを使用しないため、クエリ結果が正しくないという問題を修正します。
    -   ロックの競合が悪化しないように、検出動作を即時の競合検出から楽観的なトランザクションが悲観的なロックに遭遇したときの待機に変更します[＃11051](https://github.com/pingcap/tidb/pull/11051)

## TiKV {#tikv}

-   統計情報[＃5060](https://github.com/tikv/tikv/pull/5060)にblobファイルのサイズの統計を追加します
-   プロセスが終了するときに誤ってクリーンアップされたメモリリソースによって引き起こされるコアダンプの問題を修正します[＃5053](https://github.com/tikv/tikv/pull/5053)
-   Titanエンジン[＃4772](https://github.com/tikv/tikv/pull/4772)に関連するすべての監視メトリックを追加し[＃4836](https://github.com/tikv/tikv/pull/4836)
-   ファイルハンドルの統計が不正確であるためにファイルハンドルが使用できないという問題を回避するために、開いているファイルハンドルの数をカウントするときに、Titanの開いているファイルハンドルの数を追加します[＃5026](https://github.com/tikv/tikv/pull/5026)
-   `blob_run_mode`を設定して、特定の[＃4991](https://github.com/tikv/tikv/pull/4991)でTitanエンジンを有効にするかどうかを決定します。
-   読み取り操作がペシミスティックトランザクションのコミット情報を取得できない問題を修正します[＃5067](https://github.com/tikv/tikv/pull/5067)
-   `blob-run-mode`構成パラメーターを追加して、Titanエンジンの実行モードを制御し[＃4865](https://github.com/tikv/tikv/pull/4865) 。その値は、 `normal` 、または`read-only`になり`fallback` 。
-   デッドロックの検出パフォーマンスを向上させる[＃5089](https://github.com/tikv/tikv/pull/5089)

## PD {#pd}

-   PDがホットリージョン[＃1552](https://github.com/pingcap/pd/pull/1552)をスケジュールするときに、スケジュール制限が自動的に0に調整される問題を修正します。
-   etcd [＃1596](https://github.com/pingcap/pd/pull/1596)のgRPCゲートウェイ機能を有効にするには、 `enable-grpc-gateway`の構成オプションを追加します
-   スケジューラ構成に関連する`store-balance-rate`およびその他の統計を追加し[＃1601](https://github.com/pingcap/pd/pull/1601) `hot-region-schedule-limit`
-   ホットリージョンのスケジューリング戦略を最適化し、スケジューリング中にレプリカが不足しているリージョンをスキップして、複数のレプリカが同じ[＃1609](https://github.com/pingcap/pd/pull/1609)にスケジュールされないようにします。
-   リージョンのマージ処理ロジックを最適化し、小さいサイズのリージョンのマージを優先して、リージョンのマージを高速化することをサポートします[＃1613](https://github.com/pingcap/pd/pull/1613)
-   一度にホットリージョンスケジューリングのデフォルト制限を64に調整して、あまりにも多くのスケジューリングタスクがシステムリソースを占有してパフォーマンスに影響を与えないようにします[＃1616](https://github.com/pingcap/pd/pull/1616)
-   リージョンのスケジューリング戦略を最適化し、 `Pending`ステータス[＃1617](https://github.com/pingcap/pd/pull/1617)のリージョンのスケジューリングに高い優先順位を与えることをサポートします。
-   `random-merge`と`admin-merge-region`の演算子を追加できない問題を修正します[＃1634](https://github.com/pingcap/pd/pull/1634)
-   ログのRegionキーの形式を16進表記に調整して、見やすくします[＃1639](https://github.com/pingcap/pd/pull/1639)

## ツール {#tools}

TiDB Binlog

-   Pump GC戦略を最適化し、未消費のbinlogをクリーンアップできないという制限を取り除き、リソースが長期間使用されないようにします[＃646](https://github.com/pingcap/tidb-binlog/pull/646)

TiDB Lightning

-   SQLダンプで指定された列名が小文字[＃210](https://github.com/pingcap/tidb-lightning/pull/210)でない場合に発生するインポートエラーを修正します

## TiDB Ansible {#tidb-ansible}

-   ansibleコマンドとその`jmespath`および`jinja2`依存関係パッケージ[＃803](https://github.com/pingcap/tidb-ansible/pull/803)の事前チェック機能を追加し[＃813](https://github.com/pingcap/tidb-ansible/pull/813)
-   使用可能なディスク容量がパラメーター値[＃806](https://github.com/pingcap/tidb-ansible/pull/806)未満の場合に、 Pumpに`stop-write-at-available-space`パラメーター（デフォルトでは10 GiB）を追加して、 Pumpでのbinlogファイルの書き込みを停止します。
-   TiKV監視情報のI/O監視項目を更新し、新しいバージョン[＃820](https://github.com/pingcap/tidb-ansible/pull/820)の監視コンポーネントと互換性を持たせる
-   PD監視情報を更新し、ディスクパフォーマンスダッシュボード[＃817](https://github.com/pingcap/tidb-ansible/pull/817)でディスクレイテンシが空であるという異常を修正します。
-   TiKV詳細ダッシュボードにTitanの監視項目を追加する[＃824](https://github.com/pingcap/tidb-ansible/pull/824)
