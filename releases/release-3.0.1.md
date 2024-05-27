---
title: TiDB 3.0.1 Release Notes
summary: 「TiDB 3.0.1 リリース ノート 2019 年 7 月 16 日。TiDB バージョン 3.0.1。MAX_EXECUTION_TIME 機能のサポートを追加。自動増分 ID の増分ギャップの自動調整をサポート。ADMIN PLUGINS ENABLE/DISABLE SQL ステートメントを追加。計画準備キャッシュでウィンドウ関数がキャッシュされるのを禁止。さまざまなバグと問題を修正。
---

# TiDB 3.0.1 リリースノート {#tidb-3-0-1-release-notes}

発売日: 2019年7月16日

TiDB バージョン: 3.0.1

TiDB Ansible バージョン: 3.0.1

## ティビ {#tidb}

-   `MAX_EXECUTION_TIME`機能[＃11026](https://github.com/pingcap/tidb/pull/11026)のサポートを追加
-   リージョン[＃11166](https://github.com/pingcap/tidb/pull/11166)を分割する際のバックオフ時間を制御するために`tidb_wait_split_region_finish_backoff`セッション変数を追加します。
-   負荷に応じて自動増分IDで割り当てられた増分ギャップの自動調整をサポートし、増分ギャップの自動調整範囲は1000〜2000000 [＃11006](https://github.com/pingcap/tidb/pull/11006)です。
-   プラグイン`ADMIN PLUGINS DISABLE`動的に有効または無効にする`ADMIN PLUGINS ENABLE` SQL ステートメントを追加します[＃11157](https://github.com/pingcap/tidb/pull/11157)
-   監査プラグイン[＃11013](https://github.com/pingcap/tidb/pull/11013)にセッション接続情報を追加する
-   リージョンを分割する期間中のデフォルトの動作を変更し、PD がスケジュール[＃11166](https://github.com/pingcap/tidb/pull/11166)を完了するまで待機します。
-   一部のケースで誤った結果を回避するために、ウィンドウ関数が Prepare Plan Cache にキャッシュされることを禁止します[＃11048](https://github.com/pingcap/tidb/pull/11048)
-   保存された生成列の定義を変更するステートメントを`ALTER`禁止する[＃11068](https://github.com/pingcap/tidb/pull/11068)
-   仮想生成列を保存生成列に変更することを禁止する[＃11068](https://github.com/pingcap/tidb/pull/11068)
-   インデックス[＃11068](https://github.com/pingcap/tidb/pull/11068)で生成された列式の変更を禁止する
-   ARM64アーキテクチャ上でのTiDBのコンパイルをサポート[＃11150](https://github.com/pingcap/tidb/pull/11150)
-   データベースまたはテーブルの照合順序順序の変更をサポートしますが、データベース/テーブルの文字セットは UTF-8 または utf8mb4 である必要があります[＃11086](https://github.com/pingcap/tidb/pull/11086)
-   `UPDATE … SELECT`文の`SELECT`サブクエリが`UPDATE`式の列を解析できず、列が誤ってプルーニングされた場合にエラーが報告される問題を修正しました[＃11252](https://github.com/pingcap/tidb/pull/11252)
-   ポイントクエリ中に列が複数回クエリされ、返された結果が NULL である場合に発生するpanic問題を修正しました[＃11226](https://github.com/pingcap/tidb/pull/11226)
-   `RAND`関数[＃11169](https://github.com/pingcap/tidb/pull/11169)を使用するときに非スレッドセーフ`rand.Rand`によって発生するデータ競合の問題を修正しました
-   `oom-action="cancel"`設定されている場合、SQL 文のメモリ使用量がしきい値を超えても、この文の実行がキャンセルされず、返される結果が不正確になることがあるというバグを修正しました[＃11004](https://github.com/pingcap/tidb/pull/11004)
-   MemTracker のメモリ使用量が`SHOW PROCESSLIST`消去されなかったため、メモリ使用量が`0`はないと表示される問題を修正しました[＃10970](https://github.com/pingcap/tidb/pull/10970)
-   整数と非整数の比較結果が場合によっては正しくないバグを修正[＃11194](https://github.com/pingcap/tidb/pull/11194)
-   テーブルパーティションのクエリに明示的なトランザクションの述語が含まれている場合にクエリ結果が正しくないというバグを修正[＃11196](https://github.com/pingcap/tidb/pull/11196)
-   `infoHandle` `NULL` [＃11022](https://github.com/pingcap/tidb/pull/11022)になる可能性があるため、DDL ジョブのpanic問題を修正しました。
-   クエリされた列がサブクエリで参照されず、ネストされた集計クエリを実行するときに誤ってプルーニングされるため、クエリ結果が正しくない問題を修正しました[＃11020](https://github.com/pingcap/tidb/pull/11020)
-   `Sleep`関数が[＃11028](https://github.com/pingcap/tidb/pull/11028)時点で`KILL`ステートメントに応答しない問題を修正
-   `SHOW PROCESSLIST`コマンドで表示される`DB`列目と`INFO`列目がMySQL [＃11003](https://github.com/pingcap/tidb/pull/11003)と互換性がない問題を修正
-   `skip-grant-table=true`が構成されている場合に`FLUSH PRIVILEGES`ステートメントによって発生するシステムpanicの問題を修正[＃11027](https://github.com/pingcap/tidb/pull/11027)
-   テーブルの主キーが`UNSIGNED`整数[＃11099](https://github.com/pingcap/tidb/pull/11099)場合、 `FAST ANALYZE`で収集された主キー統計が正しくない問題を修正しました。
-   `FAST ANALYZE`文で「無効なキー」エラーが報告される場合がある問題を修正[＃11098](https://github.com/pingcap/tidb/pull/11098)
-   列のデフォルト値として`CURRENT_TIMESTAMP`が使用され、浮動小数点精度が[＃11088](https://github.com/pingcap/tidb/pull/11088)指定されている場合、 `SHOW CREATE TABLE`ステートメントで表示される精度が不完全になる問題を修正しました。
-   ウィンドウ関数がエラーを報告するときに関数名が小文字にならない問題を修正し、MySQL [＃11118](https://github.com/pingcap/tidb/pull/11118)と互換性を持たせました。
-   TiKV クライアント バッチ gRPC のバックグラウンド スレッドがパニックになった後、TiDB が TiKV に接続できず、サービスを提供できなくなる問題を修正しました[＃11101](https://github.com/pingcap/tidb/pull/11101)
-   文字列[＃11044](https://github.com/pingcap/tidb/pull/11044)の浅いコピーにより変数が誤って`SetVar`に設定される問題を修正
-   `INSERT … ON DUPLICATE`ステートメントがテーブルパーティション[＃11231](https://github.com/pingcap/tidb/pull/11231)に適用されると実行が失敗し、エラーが報告される問題を修正しました。
-   悲観的ロック（実験的機能）
    -   悲観的ロックを使用してポイントクエリを実行し、返されたデータが空の場合、行の無効なロックのために誤った結果が返される問題を修正しました[＃10976](https://github.com/pingcap/tidb/pull/10976)
    -   クエリ[＃11015](https://github.com/pingcap/tidb/pull/11015)で悲観的ロックを使用する際に正しいTSOが使用されて`SELECT … FOR UPDATE`ないため、クエリ結果が正しくない問題を修正しました。
    -   ロック競合の悪化を避けるために、楽観的トランザクションが悲観的ロックに遭遇したときの検出動作を即時競合検出から待機に変更する[＃11051](https://github.com/pingcap/tidb/pull/11051)

## ティクヴ {#tikv}

-   統計情報[＃5060](https://github.com/tikv/tikv/pull/5060)にBLOBファイルのサイズの統計を追加します
-   プロセス終了時にメモリリソースが誤って消去されることで発生するコアダンプの問題を修正[＃5053](https://github.com/tikv/tikv/pull/5053)
-   Titanエンジン[＃4772](https://github.com/tikv/tikv/pull/4772)に関連するすべての監視メトリック[＃4836](https://github.com/tikv/tikv/pull/4836)追加します
-   ファイル ハンドルの統計が不正確であるためにファイル ハンドルが利用できないという問題を回避するために、開いているファイル ハンドルの数をカウントするときに Titan の開いているファイル ハンドルの数を追加します[＃5026](https://github.com/tikv/tikv/pull/5026)
-   特定のCF [＃4991](https://github.com/tikv/tikv/pull/4991)でTitanエンジンを有効にするかどうかを決定するには`blob_run_mode`設定します。
-   読み取り操作で悲観的トランザクションのコミット情報を取得できない問題を修正[＃5067](https://github.com/tikv/tikv/pull/5067)
-   Titanエンジンの実行モードを制御するための`blob-run-mode`構成パラメータを追加します。その値は`normal` 、または`fallback` [＃4865](https://github.com/tikv/tikv/pull/4865)になります`read-only`
-   デッドロック検出のパフォーマンスを向上[＃5089](https://github.com/tikv/tikv/pull/5089)

## PD {#pd}

-   PDがホットリージョン[＃1552](https://github.com/pingcap/pd/pull/1552)をスケジュールするときに、スケジュール制限が自動的に0に調整される問題を修正しました。
-   etcd [＃1596](https://github.com/pingcap/pd/pull/1596)のgRPCゲートウェイ機能を有効にするには、 `enable-grpc-gateway`設定オプションを追加します。
-   `store-balance-rate` `hot-region-schedule-limit`およびスケジューラ構成[＃1601](https://github.com/pingcap/pd/pull/1601)に関連するその他の統計情報を追加します。
-   ホットリージョンのスケジューリング戦略を最適化し、スケジューリング中にレプリカがないリージョンをスキップして、複数のレプリカが同じ IDC [＃1609](https://github.com/pingcap/pd/pull/1609)にスケジュールされるのを防ぎます。
-   リージョンのマージ処理ロジックを最適化し、サイズの小さいリージョンのマージを優先してリージョンのマージを高速化します[＃1613](https://github.com/pingcap/pd/pull/1613)
-   一度に実行できるホットリージョンのスケジューリング数のデフォルト制限を 64 に調整し、スケジューリングタスクが多すぎてシステムリソースが占有され、パフォーマンスに影響が出ないようにします[＃1616](https://github.com/pingcap/pd/pull/1616)
-   リージョンのスケジュール戦略を最適化し、 `Pending`ステータス[＃1617](https://github.com/pingcap/pd/pull/1617)のリージョンのスケジュールを優先することをサポートします。
-   `random-merge`と`admin-merge-region`演算子を追加できない問題を修正[＃1634](https://github.com/pingcap/pd/pull/1634)
-   ログ内のリージョンキーの形式を16進表記に調整して、見やすくします[＃1639](https://github.com/pingcap/pd/pull/1639)

## ツール {#tools}

TiDBBinlog

-   Pump GC戦略を最適化し、未使用のbinlogをクリーンアップできないという制限を削除して、リソースが長時間占有されないようにします[＃646](https://github.com/pingcap/tidb-binlog/pull/646)

TiDB Lightning

-   SQLダンプで指定された列名が小文字でない場合に発生するインポートエラーを修正[＃210](https://github.com/pingcap/tidb-lightning/pull/210)

## TiDB アンシブル {#tidb-ansible}

-   ansibleコマンドとその`jmespath`および`jinja2`依存パッケージ[＃803](https://github.com/pingcap/tidb-ansible/pull/803) [＃813](https://github.com/pingcap/tidb-ansible/pull/813)事前チェック機能を追加します。
-   Pumpに`stop-write-at-available-space`パラメータ (デフォルトでは 10 GiB) を追加して、使用可能なディスク容量がパラメータ値[＃806](https://github.com/pingcap/tidb-ansible/pull/806)より少ない場合にPumpでのbinlogファイルの書き込みを停止します。
-   TiKV監視情報のI/O監視項目を更新し、新しいバージョン[＃820](https://github.com/pingcap/tidb-ansible/pull/820)の監視コンポーネントと互換性を持たせます。
-   PD 監視情報を更新し、ディスク パフォーマンス ダッシュボード[＃817](https://github.com/pingcap/tidb-ansible/pull/817)でディスク レイテンシが空になる異常を修正しました。
-   TiKV詳細ダッシュボード[＃824](https://github.com/pingcap/tidb-ansible/pull/824)にTitanの監視項目を追加する
