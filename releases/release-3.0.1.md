---
title: TiDB 3.0.1 Release Notes
---

# TiDB 3.0.1 リリースノート {#tidb-3-0-1-release-notes}

発売日：2019年7月16日

TiDB バージョン: 3.0.1

TiDB Ansible バージョン: 3.0.1

## TiDB {#tidb}

-   `MAX_EXECUTION_TIME`機能[#11026](https://github.com/pingcap/tidb/pull/11026)のサポートを追加
-   `tidb_wait_split_region_finish_backoff`セッション変数を追加して、リージョン[#11166](https://github.com/pingcap/tidb/pull/11166)を分割するバックオフ時間を制御します。
-   負荷に基づいて自動インクリメント ID によって割り当てられた増分ギャップの自動調整をサポートし、増分ギャップの自動調整範囲は 1000 ～ 2000000 です[#11006](https://github.com/pingcap/tidb/pull/11006)
-   `ADMIN PLUGINS ENABLE` / `ADMIN PLUGINS DISABLE` SQL ステートメントを追加して、プラグインを動的に有効または無効にします[#11157](https://github.com/pingcap/tidb/pull/11157)
-   監査プラグイン[#11013](https://github.com/pingcap/tidb/pull/11013)にセッション接続情報を追加します。
-   リージョンの分割期間中のデフォルトの動作を、PD のスケジュール[#11166](https://github.com/pingcap/tidb/pull/11166)が完了するまで待機するように変更します。
-   場合によっては不正確な結果が生じるのを避けるために、ウィンドウ関数が Prepare Plan Cache にキャッシュされることを禁止します[#11048](https://github.com/pingcap/tidb/pull/11048)
-   `ALTER`ステートメントによる格納された生成列の定義の変更を禁止する[#11068](https://github.com/pingcap/tidb/pull/11068)
-   仮想生成列を保存された生成列への変更を禁止する[#11068](https://github.com/pingcap/tidb/pull/11068)
-   インデックス[#11068](https://github.com/pingcap/tidb/pull/11068)を使用して生成された列式の変更を禁止します。
-   ARM64アーキテクチャでの TiDB のコンパイルのサポート[#11150](https://github.com/pingcap/tidb/pull/11150)
-   データベースまたはテーブルの照合順序の変更をサポートしますが、データベース/テーブルの文字セットは UTF-8 または utf8mb4 である必要があります[#11086](https://github.com/pingcap/tidb/pull/11086)
-   `UPDATE … SELECT`ステートメントの`SELECT`サブクエリが`UPDATE`式の列の解析に失敗し、列が誤ってプルーニングされた場合にエラーが報告される問題を修正します[#11252](https://github.com/pingcap/tidb/pull/11252)
-   ポイント クエリ中に列が複数回クエリされ、返された結果が NULL である場合に発生するpanicの問題を修正します[#11226](https://github.com/pingcap/tidb/pull/11226)
-   `RAND`関数[#11169](https://github.com/pingcap/tidb/pull/11169)の使用時に非スレッド セーフ`rand.Rand`によって引き起こされるデータ競合の問題を修正します。
-   `oom-action="cancel"`を設定した場合、SQL文のメモリ使用量が閾値を超えても実行がキャンセルされず、返される結果が正しくない場合がある不具合を[#11004](https://github.com/pingcap/tidb/pull/11004)
-   MemTracker のメモリ使用量が正しくクリーンアップされていないため、メモリ使用量が`0`ではないことが`SHOW PROCESSLIST`表示される問題を修正[#10970](https://github.com/pingcap/tidb/pull/10970)
-   整数と非整数の比較結果が正しくない場合があるバグを修正[#11194](https://github.com/pingcap/tidb/pull/11194)
-   明示的なトランザクション[#11196](https://github.com/pingcap/tidb/pull/11196)でテーブルパーティションに対するクエリに述語が含まれる場合、クエリ結果が正しくないバグを修正
-   `infoHandle` `NULL` [#11022](https://github.com/pingcap/tidb/pull/11022)になる可能性があるため、DDL ジョブのpanic問題を修正
-   クエリ対象の列がサブクエリで参照されておらず、ネストされた集計クエリの実行時に誤ってプルーニングされるため、クエリ結果が正しくない問題を修正します[#11020](https://github.com/pingcap/tidb/pull/11020)
-   `Sleep`関数が[#11028](https://github.com/pingcap/tidb/pull/11028)時点で`KILL`ステートメントに応答しない問題を修正します。
-   `SHOW PROCESSLIST`コマンドで表示される`DB`と`INFO`列が MySQL [#11003](https://github.com/pingcap/tidb/pull/11003)と互換性がない問題を修正
-   `skip-grant-table=true`が設定されている場合に`FLUSH PRIVILEGES`ステートメントによって引き起こされるシステムpanicの問題を修正します[#11027](https://github.com/pingcap/tidb/pull/11027)
-   テーブルの主キーが`UNSIGNED`整数[#11099](https://github.com/pingcap/tidb/pull/11099)の場合、 `FAST ANALYZE`によって収集された主キー統計が正しくない問題を修正します。
-   場合によっては「無効なキー」エラーが`FAST ANALYZE`ステートメントによって報告される問題を修正します[#11098](https://github.com/pingcap/tidb/pull/11098)
-   カラムのデフォルト値として`CURRENT_TIMESTAMP`使用し、float 精度を[#11088](https://github.com/pingcap/tidb/pull/11088)に指定した場合、 `SHOW CREATE TABLE`ステートメントで示される精度が不完全になる問題を修正します。
-   MySQL [#11118](https://github.com/pingcap/tidb/pull/11118)と互換性を持たせるために、ウィンドウ関数がエラーを報告するときに関数名が小文字にならない問題を修正しました。
-   TiKV クライアント バッチ gRPC のバックグラウンド スレッドがパニックになった後、TiDB が TiKV への接続に失敗し、サービスを提供できなくなる問題を修正します[#11101](https://github.com/pingcap/tidb/pull/11101)
-   文字列[#11044](https://github.com/pingcap/tidb/pull/11044)の浅いコピーにより、変数が誤って`SetVar`に設定される問題を修正します。
-   `INSERT … ON DUPLICATE`ステートメントがテーブル パーティション[#11231](https://github.com/pingcap/tidb/pull/11231)に適用されると、実行が失敗し、エラーが報告される問題を修正します。
-   悲観的ロック (実験的機能)
    -   悲観的ロックを使用してポイント クエリを実行し、返されるデータが空である場合に、行の無効なロックが原因で間違った結果が返される問題を修正します[#10976](https://github.com/pingcap/tidb/pull/10976)
    -   クエリ[#11015](https://github.com/pingcap/tidb/pull/11015)で悲観的ロックを使用する場合、 `SELECT … FOR UPDATE`が正しい TSO を使用しないため、クエリ結果が正しくない問題を修正します。
    -   ロック競合の悪化を避けるために、検出動作を即時競合検出から、楽観的トランザクションが悲観悲観的ロックに遭遇したときに待機するように変更します[#11051](https://github.com/pingcap/tidb/pull/11051)

## TiKV {#tikv}

-   統計情報[#5060](https://github.com/tikv/tikv/pull/5060)に BLOB ファイルのサイズの統計を追加します。
-   プロセス終了時にメモリリソースが誤ってクリーンアップされることによって引き起こされるコア ダンプの問題を修正します[#5053](https://github.com/tikv/tikv/pull/5053)
-   Titan エンジン[#4772](https://github.com/tikv/tikv/pull/4772) 、 [#4836](https://github.com/tikv/tikv/pull/4836)に関連するすべての監視メトリクスを追加します。
-   ファイル ハンドルの統計が不正確であるために使用可能なファイル ハンドルがないという問題を回避するために、開いているファイル ハンドルの数をカウントするときに Titan の開いているファイル ハンドルの数を追加します[#5026](https://github.com/tikv/tikv/pull/5026)
-   特定の CF [#4991](https://github.com/tikv/tikv/pull/4991)で Titan エンジンを有効にするかどうかを決定するには、 `blob_run_mode`を設定します。
-   読み取り操作で悲観的トランザクションのコミット情報を取得できない問題を修正[#5067](https://github.com/tikv/tikv/pull/5067)
-   Titan エンジンの実行モードを制御するには`blob-run-mode`構成パラメータを追加します。その値は`normal` 、 `read-only` 、または`fallback` [#4865](https://github.com/tikv/tikv/pull/4865)です。
-   デッドロックの検出パフォーマンスの向上[#5089](https://github.com/tikv/tikv/pull/5089)

## PD {#pd}

-   PD がホット リージョン[#1552](https://github.com/pingcap/pd/pull/1552)をスケジュールすると、スケジュール制限が自動的に 0 に調整される問題を修正します。
-   etcd [#1596](https://github.com/pingcap/pd/pull/1596)の gRPC ゲートウェイ機能を有効にするための`enable-grpc-gateway`構成オプションを追加します。
-   `store-balance-rate` 、 `hot-region-schedule-limit`およびスケジューラ構成に関連するその他の統計を追加[#1601](https://github.com/pingcap/pd/pull/1601)
-   ホットリージョンのスケジューリング戦略を最適化し、スケジューリング中にレプリカが不足しているリージョンをスキップして、複数のレプリカが同じ IDC [#1609](https://github.com/pingcap/pd/pull/1609)にスケジュールされるのを防ぎます。
-   リージョンのマージ処理ロジックを最適化し、より小さいサイズのリージョンのマージを優先してリージョンのマージを高速化します[#1613](https://github.com/pingcap/pd/pull/1613)
-   過剰なスケジュール タスクがシステム リソースを占有し、パフォーマンスに影響を与えることを防ぐために、一度に実行できるホットリージョンスケジュールのデフォルト制限を 64 に調整します[#1616](https://github.com/pingcap/pd/pull/1616)
-   リージョンのスケジューリング戦略を最適化し、 `Pending`ステータス[#1617](https://github.com/pingcap/pd/pull/1617)のリージョンのスケジューリングに高い優先順位を与えることをサポートします。
-   `random-merge`と`admin-merge-region`演算子を追加できない問題を修正[#1634](https://github.com/pingcap/pd/pull/1634)
-   ログ内のリージョンキーの形式を 16 進表記に調整して見やすくしました[#1639](https://github.com/pingcap/pd/pull/1639)

## ツール {#tools}

TiDBBinlog

-   PumpGC 戦略を最適化し、未消費のbinlogをクリーンアップできないという制限を削除して、リソースが長時間占有されないようにする[#646](https://github.com/pingcap/tidb-binlog/pull/646)

TiDB Lightning

-   SQL ダンプで指定された列名が小文字ではない場合に発生するインポート エラーを修正[#210](https://github.com/pingcap/tidb-lightning/pull/210)

## TiDB Ansible {#tidb-ansible}

-   ansible コマンドとその`jmespath`および`jinja2`依存関係パッケージ[#803](https://github.com/pingcap/tidb-ansible/pull/803) 、 [#813](https://github.com/pingcap/tidb-ansible/pull/813)の事前チェック機能を追加します。
-   Pumpに`stop-write-at-available-space`パラメータ (デフォルトでは 10 GiB) を追加して、利用可能なディスク容量がパラメータ値[#806](https://github.com/pingcap/tidb-ansible/pull/806)未満の場合にPumpでのbinlogファイルの書き込みを停止します。
-   TiKV監視情報のI/O監視項目を更新し、新バージョン[#820](https://github.com/pingcap/tidb-ansible/pull/820)の監視コンポーネントに対応させます。
-   PD監視情報を更新し、ディスクパフォ​​ーマンスダッシュボード[#817](https://github.com/pingcap/tidb-ansible/pull/817)でDisk Latencyが空になる異常を修正
-   TiKV 詳細ダッシュボードに Titan の監視項目を追加します[#824](https://github.com/pingcap/tidb-ansible/pull/824)
