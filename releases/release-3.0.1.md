---
title: TiDB 3.0.1 Release Notes
---

# TiDB 3.0.1 リリースノート {#tidb-3-0-1-release-notes}

発売日：2019年7月16日

TiDB バージョン: 3.0.1

TiDB アンシブル バージョン: 3.0.1

## TiDB {#tidb}

-   `MAX_EXECUTION_TIME`機能[#11026](https://github.com/pingcap/tidb/pull/11026)のサポートを追加
-   `tidb_wait_split_region_finish_backoff`セッション変数を追加して、リージョン[#11166](https://github.com/pingcap/tidb/pull/11166)の分割のバックオフ時間を制御します
-   負荷に基づいて自動インクリメント ID によって割り当てられたインクリメンタル ギャップの自動調整をサポートし、インクリメンタル ギャップの自動調整範囲は 1000 ～ 2000000 です[#11006](https://github.com/pingcap/tidb/pull/11006)
-   `ADMIN PLUGINS ENABLE` / `ADMIN PLUGINS DISABLE` SQL ステートメントを追加して、プラグインを動的に有効または無効にします[#11157](https://github.com/pingcap/tidb/pull/11157)
-   Audit プラグインにセッション接続情報を追加します[#11013](https://github.com/pingcap/tidb/pull/11013)
-   PD がスケジューリングを終了するのを待つようにリージョンを分割する期間中のデフォルトの動作を変更します[#11166](https://github.com/pingcap/tidb/pull/11166)
-   場合によっては誤った結果を避けるために、ウィンドウ関数がプラン キャッシュの準備にキャッシュされるのを禁止します[#11048](https://github.com/pingcap/tidb/pull/11048)
-   `ALTER`文が格納された生成列の定義を変更することを禁止する[#11068](https://github.com/pingcap/tidb/pull/11068)
-   仮想生成列の保存生成列への変更を許可しない[#11068](https://github.com/pingcap/tidb/pull/11068)
-   生成された列式をインデックス[#11068](https://github.com/pingcap/tidb/pull/11068)で変更できないようにする
-   ARM64アーキテクチャでの TiDB のコンパイルをサポート[#11150](https://github.com/pingcap/tidb/pull/11150)
-   データベースまたはテーブルの照合順序の変更をサポートしますが、データベース/テーブルの文字セットは UTF-8 または utf8mb4 である必要があります[#11086](https://github.com/pingcap/tidb/pull/11086)
-   `UPDATE … SELECT`ステートメントの`SELECT`サブクエリが`UPDATE`式の列の解析に失敗し、列が誤ってプルーニングされるとエラーが報告される問題を修正します[#11252](https://github.com/pingcap/tidb/pull/11252)
-   列が複数回クエリされ、ポイントクエリ中に返された結果が NULL である場合に発生するpanicの問題を修正します[#11226](https://github.com/pingcap/tidb/pull/11226)
-   `RAND`関数を使用する場合の非スレッドセーフ`rand.Rand`によって引き起こされるデータ競合の問題を修正します[#11169](https://github.com/pingcap/tidb/pull/11169)
-   `oom-action="cancel"`を設定した場合、SQL文のメモリ使用量が閾値を超えても当該文の実行がキャンセルされない場合があり、返される結果が正しくない不具合を修正[#11004](https://github.com/pingcap/tidb/pull/11004)
-   MemTracker のメモリ使用量が正しく消去されていないため、 `SHOW PROCESSLIST`メモリ使用量が`0`ではないことが示される問題を修正します[#10970](https://github.com/pingcap/tidb/pull/10970)
-   整数と非整数の比較結果が正しくない場合がある不具合を修正[#11194](https://github.com/pingcap/tidb/pull/11194)
-   テーブル パーティションのクエリに明示的なトランザクションの述語が含まれている場合、クエリの結果が正しくないバグを修正します[#11196](https://github.com/pingcap/tidb/pull/11196)
-   `infoHandle` `NULL` [#11022](https://github.com/pingcap/tidb/pull/11022)の可能性があるため、DDL ジョブのpanicの問題を修正します。
-   ネストされた集計クエリを実行すると、クエリ対象の列がサブクエリで参照されず、間違ってプルーニングされるため、クエリの結果が正しくない問題を修正します[#11020](https://github.com/pingcap/tidb/pull/11020)
-   `Sleep`関数が時間[#11028](https://github.com/pingcap/tidb/pull/11028)で`KILL`ステートメントに応答しない問題を修正します。
-   `SHOW PROCESSLIST`コマンドで表示される`DB`と`INFO`列が MySQL [#11003](https://github.com/pingcap/tidb/pull/11003)と互換性がない問題を修正
-   `skip-grant-table=true`が構成されている場合に`FLUSH PRIVILEGES`ステートメントによって引き起こされるシステムpanicの問題を修正します[#11027](https://github.com/pingcap/tidb/pull/11027)
-   テーブルの主キーが`UNSIGNED`整数[#11099](https://github.com/pingcap/tidb/pull/11099)の場合、 `FAST ANALYZE`で収集された主キー統計が正しくない問題を修正
-   場合によっては`FAST ANALYZE`ステートメントで「無効なキー」エラーが報告される問題を修正します[#11098](https://github.com/pingcap/tidb/pull/11098)
-   カラムのデフォルト値として`CURRENT_TIMESTAMP`使用し、float 精度を[#11088](https://github.com/pingcap/tidb/pull/11088)に指定すると、 `SHOW CREATE TABLE`ステートメントで示される精度が不完全になる問題を修正します。
-   ウィンドウ関数がエラーを報告するときに関数名が小文字にならない問題を修正して、MySQL [#11118](https://github.com/pingcap/tidb/pull/11118)と互換性を持たせました。
-   TiDB が TiKV への接続に失敗し、TiKV クライアント バッチ gRPC パニック[#11101](https://github.com/pingcap/tidb/pull/11101)のバックグラウンド スレッドの後にサービスを提供できない問題を修正します。
-   文字列[#11044](https://github.com/pingcap/tidb/pull/11044)の浅いコピーのために、変数が`SetVar`によって誤って設定される問題を修正します
-   `INSERT … ON DUPLICATE`ステートメントがテーブル パーティション[#11231](https://github.com/pingcap/tidb/pull/11231)に適用されると、実行が失敗し、エラーが報告される問題を修正します。
-   悲観的ロック (実験的機能)
    -   悲観的ロックを使用してポイント クエリを実行し、返されたデータが空の場合、行の無効なロックが原因で誤った結果が返される問題を修正します[#10976](https://github.com/pingcap/tidb/pull/10976)
    -   クエリで悲観的ロックを使用すると、 `SELECT … FOR UPDATE` TSO が使用されないため、クエリの結果が正しくない問題を修正します。 [#11015](https://github.com/pingcap/tidb/pull/11015)
    -   ロック競合の悪化を避けるために、楽観的トランザクションが悲観的ロックに遭遇したときに検出動作を即時の競合検出から待機に変更します[#11051](https://github.com/pingcap/tidb/pull/11051)

## TiKV {#tikv}

-   統計情報[#5060](https://github.com/tikv/tikv/pull/5060)に BLOB ファイルのサイズの統計を追加します。
-   プロセスの終了[#5053](https://github.com/tikv/tikv/pull/5053)にメモリリソースが正しく消去されないために発生するコア ダンプの問題を修正します。
-   Titan エンジンに関連するすべてのモニタリング メトリックを追加します[#4772](https://github.com/tikv/tikv/pull/4772) 、 [#4836](https://github.com/tikv/tikv/pull/4836)
-   ファイル ハンドルの統計が不正確なためにファイル ハンドルが使用できないという問題を回避するために、開いているファイル ハンドルの数をカウントするときに、Titan の開いているファイル ハンドルの数を追加します[#5026](https://github.com/tikv/tikv/pull/5026)
-   特定の CF [#4991](https://github.com/tikv/tikv/pull/4991)で Titan エンジンを有効にするかどうかを決定するには、 `blob_run_mode`を設定します。
-   読み取り操作で悲観的トランザクションのコミット情報を取得できない問題を修正します[#5067](https://github.com/tikv/tikv/pull/5067)
-   `blob-run-mode`構成パラメーターを追加して、Titan エンジンの実行モードを制御します。その値は`normal` 、 `read-only`または`fallback` [#4865](https://github.com/tikv/tikv/pull/4865)です。
-   デッドロック検出のパフォーマンスを改善する[#5089](https://github.com/tikv/tikv/pull/5089)

## PD {#pd}

-   PD がホット リージョン[#1552](https://github.com/pingcap/pd/pull/1552)をスケジュールすると、スケジュール制限が自動的に 0 に調整される問題を修正します。
-   `enable-grpc-gateway`構成オプションを追加して、etcd [#1596](https://github.com/pingcap/pd/pull/1596)の gRPC ゲートウェイ機能を有効にします
-   `store-balance-rate` 、 `hot-region-schedule-limit` 、およびスケジューラ構成に関連するその他の統計を追加します[#1601](https://github.com/pingcap/pd/pull/1601)
-   ホットリージョンのスケジューリング戦略を最適化し、スケジューリング中にレプリカのないリージョンをスキップして、複数のレプリカが同じ IDC [#1609](https://github.com/pingcap/pd/pull/1609)にスケジュールされるのを防ぎます。
-   リージョンのマージ処理ロジックを最適化し、サイズの小さいリージョンのマージを優先してリージョンのマージを高速化することをサポートします[#1613](https://github.com/pingcap/pd/pull/1613)
-   1 回のホットリージョンスケジューリングのデフォルト制限を 64 に調整して、あまりにも多くのスケジューリング タスクがシステム リソースを占有し、パフォーマンスに影響を与えないようにします[#1616](https://github.com/pingcap/pd/pull/1616)
-   リージョンのスケジューリング戦略を最適化し、 `Pending`ステータス[#1617](https://github.com/pingcap/pd/pull/1617)のリージョンのスケジューリングを優先してサポートする
-   `random-merge`と`admin-merge-region`オペレーターを追加できない問題を修正[#1634](https://github.com/pingcap/pd/pull/1634)
-   ログのリージョンキーの形式を 16 進数表記に調整して、見やすくします[#1639](https://github.com/pingcap/pd/pull/1639)

## ツール {#tools}

TiDBBinlog

-   Pump GC 戦略を最適化し、消費されていないbinlog を消去できないという制限を削除して、リソースが長時間占有されないようにします[#646](https://github.com/pingcap/tidb-binlog/pull/646)

TiDB Lightning

-   SQL ダンプで指定された列名が小文字[#210](https://github.com/pingcap/tidb-lightning/pull/210)でない場合に発生するインポート エラーを修正します。

## TiDB アンシブル {#tidb-ansible}

-   ansible コマンドとその`jmespath`および`jinja2`依存パッケージの事前チェック機能を追加します[#803](https://github.com/pingcap/tidb-ansible/pull/803) 、 [#813](https://github.com/pingcap/tidb-ansible/pull/813)
-   Pumpに`stop-write-at-available-space`パラメータ (デフォルトでは 10 GiB) を追加して、使用可能なディスク容量がパラメータ値[#806](https://github.com/pingcap/tidb-ansible/pull/806)未満の場合にPumpでbinlogファイルの書き込みを停止します。
-   TiKV監視情報のI/O監視項目を更新し、新バージョン[#820](https://github.com/pingcap/tidb-ansible/pull/820)の監視コンポーネントに対応
-   PD 監視情報を更新し、ディスク パフォーマンス ダッシュボード[#817](https://github.com/pingcap/tidb-ansible/pull/817)でディスク レイテンシが空になる異常を修正します。
-   TiKV 詳細ダッシュボードに Titan の監視項目を追加[#824](https://github.com/pingcap/tidb-ansible/pull/824)
