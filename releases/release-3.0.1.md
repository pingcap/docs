---
title: TiDB 3.0.1 Release Notes
summary: "TiDB 3.0.1 リリースノート 2019年7月16日。TiDBバージョン3.0.1。MAX_EXECUTION_TIME機能のサポートを追加。AUTO_INCREMENT IDの増分ギャップの自動調整をサポート。ADMIN PLUGINS ENABLE/DISABLE SQL文を追加。Prepare Plan CacheでWindow Functionsがキャッシュされるのを禁止。さまざまなバグと問題を修正。TiKV: BLOBファイルサイズの統計を追加。コアダンプの問題を修正。PD: enable-grpc-gateway構成オプションを追加。ホットリージョンスケジューリング戦略を最適化。ツール: TiDB Binlog - Pump GC戦略を最適化。TiDB Lightning - インポートエラーを修正。TiDB Ansible - 事前チェック機能を追加、監視情報を更新。"
---

# TiDB 3.0.1 リリースノート {#tidb-3-0-1-release-notes}

発売日：2019年7月16日

TiDB バージョン: 3.0.1

TiDB Ansible バージョン: 3.0.1

## TiDB {#tidb}

-   `MAX_EXECUTION_TIME`機能のサポートを追加 [＃11026](https://github.com/pingcap/tidb/pull/11026)
-   リージョンを分割する際のバックオフ時間を制御するために、 `tidb_wait_split_region_finish_backoff`セッション変数を追加します。 [＃11166](https://github.com/pingcap/tidb/pull/11166)
-   負荷に応じてAUTO_INCREMENT IDで割り当てられた増分ギャップを自動的に調整することをサポートし、増分ギャップの自動調整範囲は1000〜2000000です[＃11006](https://github.com/pingcap/tidb/pull/11006)
-   プラグイン`ADMIN PLUGINS DISABLE` `ADMIN PLUGINS ENABLE`ステートメントを追加する[＃11157](https://github.com/pingcap/tidb/pull/11157)
-   監査プラグインにセッション接続情報を追加する [＃11013](https://github.com/pingcap/tidb/pull/11013)
-   リージョン分割期間中のデフォルトの動作を変更し、PD がスケジュールを完了するまで待機します。 [＃11166](https://github.com/pingcap/tidb/pull/11166)
-   一部のケースで誤った結果を回避するために、ウィンドウ関数がプリペアドプランキャッシュにキャッシュされることを禁止します[＃11048](https://github.com/pingcap/tidb/pull/11048)
-   `ALTER`文が保存された生成列の定義を変更することを禁止する[＃11068](https://github.com/pingcap/tidb/pull/11068)
-   仮想生成列を保存生成列に変更することを禁止する[＃11068](https://github.com/pingcap/tidb/pull/11068)
-   インデックスで生成された列式の変更を禁止する [＃11068](https://github.com/pingcap/tidb/pull/11068)
-   ARM64アーキテクチャ上でのTiDBのコンパイルをサポート[＃11150](https://github.com/pingcap/tidb/pull/11150)
-   データベースまたはテーブルの照合順序の変更をサポートしますが、データベース/テーブルの文字セットは UTF-8 または utf8mb4 である必要があります。 [＃11086](https://github.com/pingcap/tidb/pull/11086)
-   `UPDATE … SELECT`文の`SELECT`サブクエリが`UPDATE`の列の解析に失敗し、列が誤ってプルーニングされたときにエラーが報告される問題を修正しました[＃11252](https://github.com/pingcap/tidb/pull/11252)
-   ポイントクエリ中に列が複数回クエリされ、返された結果が NULL である場合に発生するpanic問題を修正しました[＃11226](https://github.com/pingcap/tidb/pull/11226)
-   `RAND`関数使用する際に非スレッドセーフ`rand.Rand`によって発生するデータ競合問題を修正 [＃11169](https://github.com/pingcap/tidb/pull/11169)
-   `oom-action="cancel"`が設定されている場合、SQL 文のメモリ使用量がしきい値を超えているにもかかわらず、この文の実行がキャンセルされず、返される結果が正しくないというバグを修正しました[＃11004](https://github.com/pingcap/tidb/pull/11004)
-   MemTracker `SHOW PROCESSLIST`メモリ使用量が正しく消去されなかったため、メモリ使用量が`0`ではないと表示される問題を修正しました[＃10970](https://github.com/pingcap/tidb/pull/10970)
-   整数と非整数の比較結果が場合によっては正しくないというバグを修正[＃11194](https://github.com/pingcap/tidb/pull/11194)
-   テーブルパーティションのクエリに明示的なトランザクションの述語が含まれている場合にクエリ結果が正しくないというバグを修正しました[＃11196](https://github.com/pingcap/tidb/pull/11196)
-   `infoHandle` `NULL` になる可能性があるため、DDL ジョブのpanic問題を修正しました。 [＃11022](https://github.com/pingcap/tidb/pull/11022)
-   クエリされた列がサブクエリで参照されていないため、ネストされた集計クエリを実行するときに誤ってプルーニングされ、クエリ結果が正しくない問題を修正しました[＃11020](https://github.com/pingcap/tidb/pull/11020)
-   `Sleep`の関数が`KILL` のステートメントに応答しない問題を修正しました [＃11028](https://github.com/pingcap/tidb/pull/11028)
-   `SHOW PROCESSLIST`コマンドで表示される`DB`列と`INFO`列がMySQL と互換性がない問題を修正 [＃11003](https://github.com/pingcap/tidb/pull/11003)
-   `skip-grant-table=true`が設定されている場合に`FLUSH PRIVILEGES`ステートメントによって発生するシステムpanicの問題を修正[＃11027](https://github.com/pingcap/tidb/pull/11027)
-   テーブルの主キーが`UNSIGNED`整数の場合、 `FAST ANALYZE`で収集された主キー統計が正しくない問題を修正しました。 [＃11099](https://github.com/pingcap/tidb/pull/11099)
-   `FAST ANALYZE`文で「無効なキー」エラーが報告される場合がある問題を修正[＃11098](https://github.com/pingcap/tidb/pull/11098)
-   列のデフォルト値として`CURRENT_TIMESTAMP`が使用され、float精度が指定されている場合、 `SHOW CREATE TABLE`ステートメントで表示される精度が不完全になる問題を修正しました。 [＃11088](https://github.com/pingcap/tidb/pull/11088)
-   MySQL との互換性を保つために、ウィンドウ関数がエラーを報告するときに関数名が小文字にならない問題を修正しました。 [＃11118](https://github.com/pingcap/tidb/pull/11118)
-   TiKV クライアント バッチ gRPC のバックグラウンド スレッドがパニックを起こした後、TiDB が TiKV に接続できず、サービスを提供できなくなる問題を修正しました[＃11101](https://github.com/pingcap/tidb/pull/11101)
-   文字列の浅いコピーにより変数が誤って`SetVar`に設定される問題を修正しました [＃11044](https://github.com/pingcap/tidb/pull/11044)
-   `INSERT … ON DUPLICATE`ステートメントがテーブルパーティションに適用されると実行が失敗し、エラーが報告される問題を修正しました。 [＃11231](https://github.com/pingcap/tidb/pull/11231)
-   悲観的ロック（実験的機能）
    -   悲観的ロックを使用してポイントクエリを実行し、返されたデータが空の場合に、行の無効なロックのために誤った結果が返される問題を修正しました[＃10976](https://github.com/pingcap/tidb/pull/10976)
    -   クエリで悲観的ロックを使用する際に正しいTSO `SELECT … FOR UPDATE`が使用されていないため、クエリ結果が正しくない問題を修正しました。 [＃11015](https://github.com/pingcap/tidb/pull/11015)
    -   ロック競合の悪化を避けるために、楽観的トランザクションが悲観的ロックに遭遇したときの検出動作を即時競合検出から待機に変更します[＃11051](https://github.com/pingcap/tidb/pull/11051)

## TiKV {#tikv}

-   統計情報にBLOBファイルのサイズの統計を追加します [＃5060](https://github.com/tikv/tikv/pull/5060)
-   プロセス終了時にメモリリソースが誤って消去されることで発生するコアダンプの問題を修正[＃5053](https://github.com/tikv/tikv/pull/5053)
-   Titanエンジンに関連するすべての監視メトリック追加します [＃4772](https://github.com/tikv/tikv/pull/4772) [＃4836](https://github.com/tikv/tikv/pull/4836)
-   ファイルハンドルの統計が不正確であるためにファイルハンドルが利用できないという問題を回避するために、開いているファイルハンドルの数をカウントするときに Titan の開いているファイルハンドルの数を追加します[＃5026](https://github.com/tikv/tikv/pull/5026)
-   特定のCF でTitanエンジンを有効にするかどうかを決定するには`blob_run_mode`設定します。 [＃4991](https://github.com/tikv/tikv/pull/4991)
-   読み取り操作で悲観的トランザクションのコミット情報を取得できない問題を修正[＃5067](https://github.com/tikv/tikv/pull/5067)
-   Titanエンジンの実行モードを制御するための`blob-run-mode`構成パラメータを追加します。その値は`normal`、`fallback`、または`read-only`になります [＃4865](https://github.com/tikv/tikv/pull/4865)
-   デッドロック検出のパフォーマンスを向上[＃5089](https://github.com/tikv/tikv/pull/5089)

## PD {#pd}

-   PDがホットリージョンをスケジュールするときに、スケジュール制限が自動的に0に調整される問題を修正しました。 [＃1552](https://github.com/pingcap/pd/pull/1552)
-   etcd の gRPC ゲートウェイ機能を有効にするには、 `enable-grpc-gateway`構成オプションを追加します。 [＃1596](https://github.com/pingcap/pd/pull/1596)
-   `store-balance-rate` 、およびスケジューラ構成に関連するその他の統計情報を追加します`hot-region-schedule-limit` [＃1601](https://github.com/pingcap/pd/pull/1601)
-   ホットリージョンのスケジュール戦略を最適化し、スケジュール時にレプリカが不足しているリージョンをスキップして、同じIDC に複数のレプリカがスケジュールされるのを防ぎます。 [＃1609](https://github.com/pingcap/pd/pull/1609)
-   リージョンのマージ処理ロジックを最適化し、サイズの小さいリージョンのマージを優先してリージョンのマージを高速化します[＃1613](https://github.com/pingcap/pd/pull/1613)
-   一度に実行できるホットリージョンのスケジューリング数のデフォルト制限を64に調整し、スケジューリングタスクが多すぎるとシステムリソースが占有され、パフォーマンスに影響が出るのを防ぎます[＃1616](https://github.com/pingcap/pd/pull/1616)
-   リージョンスケジュール戦略を最適化し、 `Pending`ステータスのリージョンのスケジュールを優先することをサポートします。 [＃1617](https://github.com/pingcap/pd/pull/1617)
-   `random-merge`と`admin-merge-region`演算子を追加できない問題を修正[＃1634](https://github.com/pingcap/pd/pull/1634)
-   ログ内のリージョンキーの形式を16進表記に調整して、見やすくします[＃1639](https://github.com/pingcap/pd/pull/1639)

## ツール {#tools}

TiDB Binlog

-   Pump GC戦略を最適化し、未使用のbinlogをクリーンアップできないという制限を削除して、リソースが長時間占有されないようにします[＃646](https://github.com/pingcap/tidb-binlog/pull/646)

TiDB Lightning

-   SQLダンプで指定された列名が小文字でない場合に発生するインポートエラーを修正しました[＃210](https://github.com/pingcap/tidb-lightning/pull/210)

## TiDB Ansible {#tidb-ansible}

-   ansibleコマンドとその`jmespath`および`jinja2`依存パッケージの事前チェック機能を追加します[＃813](https://github.com/pingcap/tidb-ansible/pull/813) [＃803](https://github.com/pingcap/tidb-ansible/pull/803)
-   Pumpに`stop-write-at-available-space`パラメータ（デフォルトでは10 GiB）を追加して、使用可能なディスク容量がパラメータ値より少ない場合にPumpでbinlogファイルの書き込みを停止します。 [＃806](https://github.com/pingcap/tidb-ansible/pull/806)
-   TiKV監視情報のI/O監視項目を更新し、新しいバージョンの監視コンポーネントと互換性を持たせます。 [＃820](https://github.com/pingcap/tidb-ansible/pull/820)
-   PD 監視情報を更新し、ディスク パフォーマンス ダッシュボードでディスク レイテンシが空になる異常を修正しました。 [＃817](https://github.com/pingcap/tidb-ansible/pull/817)
-   TiKV詳細ダッシュボードにTitanの監視項目を追加する [＃824](https://github.com/pingcap/tidb-ansible/pull/824)
