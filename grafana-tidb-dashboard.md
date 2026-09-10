---
title: TiDB Monitoring Metrics
summary: Grafana TiDB ダッシュボードに表示されるいくつかの主要なメトリックについて学習します。
---

# TiDB 監視メトリクス {#tidb-monitoring-metrics}

TiUPを使用してTiDBクラスターをデプロイする場合、監視システム（PrometheusとGrafana）も同時にデプロイされます。監視アーキテクチャについては、 [TiDB 監視フレームワークの概要](/tidb-monitoring-framework.md)を参照してください。

Grafanaダッシュボードは、概要、PD、TiDB、TiKV、Node_exporter、ディスクパフォーマンス、パフォーマンス概要を含む一連のサブダッシュボードに分かれています。TiDBダッシュボードは、TiDBパネルとTiDBサマリーパネルで構成されています。2つのパネルの違いは、以下のとおりです。

- TiDB パネル: クラスターの異常のトラブルシューティングのために可能な限り包括的な情報を提供します。
- TiDBサマリーパネル：TiDBパネル情報のうち、ユーザーが最も関心のある部分を抽出し、若干の修正を加えています。日々のデータベース運用においてユーザーが特に関心を持つデータ（QPS、TPS、応答遅延など）を提供し、表示またはレポートする監視情報として機能します。

このドキュメントでは、TiDB ダッシュボードに表示されるいくつかの主要な監視メトリックについて説明します。

## 主要な指標の説明 {#key-metrics-description}

TiDB ダッシュボードに表示される主要なメトリックを理解するには、次のセクションを確認してください。

### Query Summary {#query-summary}

- Duration: 実行時間
    - クライアントのネットワークリクエストがTiDBに送信されてから、TiDBがそれを実行した後にクライアントに返されるまでの時間。通常、クライアントリクエストはSQL文の形式で送信されますが、 `COM_PING`、`COM_SLEEP`、`COM_STMT_FETCH`、`COM_SEND_LONG_DATA`などのコマンドの実行時間も含まれる場合があります
    - TiDBはマルチクエリをサポートしているため、 `select 1; select 1; select 1;`ような複数のSQL文を一度に送信できます。この場合、このクエリの合計実行時間には、すべてのSQL文の実行時間が含まれます。
- Command Per Second: コマンド実行結果の成功または失敗に応じて分類される、TiDBによって1秒あたりに処理されるコマンドの数
- QPS: すべての TiDB インスタンスで秒あたりに実行される SQL文の数。`SELECT` 、 `INSERT` 、 `UPDATE`およびその他のタイプの文に従ってカウントされます
- CPS By Instance: コマンド実行結果の成功または失敗に応じて分類された各TiDBインスタンスのコマンド統計
- Failed Query OPM：各TiDBインスタンスで1分間にSQL文を実行した際に発生したエラー数に基づく、エラーの種類（構文エラーや主キーの競合など）の統計情報。エラーが発生したモジュールとエラーコードが含まれます。
- Slow query：スロークエリの処理時間の統計（スロークエリ全体の時間コスト、コプロセッサーの時間コスト、コプロセッサーのスケジューリングの待機時間）。スロークエリは、内部SQL文と一般SQL文に分類されます。
- Connection Idle Duration: アイドル接続の期間
- 999/99/95/80 Duration: 異なる種類のSQL文の実行時間の統計（異なるパーセンタイル）

### Query Detail {#query-detail}

- Duration 80/95/99/999 By Instance: 各 TiDB インスタンスでの SQL 文の実行時間の統計 (異なるパーセンタイル)
- Failed Query OPM Detail: 各 TiDB インスタンスで 1分あたりに SQL文を実行したときに発生したエラーに応じたエラーの種類 (構文エラーや主キーの競合など) の統計
- Internal SQL OPS: TiDBクラスタ全体で1秒あたりに実行された内部SQL文の数。内部SQL文は内部的に実行され、通常はユーザーのSQL文または内部的にスケジュールされたタスクによってトリガーされます。

### Server {#server}

- Uptime: 各 TiDB インスタンスの実行時間
- Memory Usage: 各 TiDB インスタンスのメモリ使用量の統計。プロセスが占有するメモリと、ヒープ上でGolangによって適用されるメモリに分かれています。
- CPU Usage: 各TiDBインスタンスのCPU使用率の統計
- Connection Count: 各 TiDB インスタンスに接続されているクライアントの数
- Open FD Count: 各TiDBインスタンスのオープンファイルディスクリプタの統計
- Disconnection Count: 各 TiDB インスタンスから切断されたクライアントの数
- Events OPM: "start"、"close"、"graceful-shutdown"、"kill"、"hang"などの主要なイベントの統計
- Goroutine Count: 各 TiDB インスタンス上の Goroutine の数
- Prepare Statement Count: 各 TiDB インスタンスで実行される`Prepare`のステートメントの数とその合計数
- Keep Alive OPM: 各TiDBインスタンスで毎分メトリクスが更新される回数。通常は注意する必要はありません。
- Panic And Critical Error: TiDB で発生したパニックと重大なエラーの数
- Time Jump Back OPS: 各 TiDB インスタンスでオペレーティングシステムの時刻が毎秒巻き戻る回数
- Get Token Duration: 各接続でトークンを取得するのにかかる時間コスト
- Skip Binlog Count: TiDB のbinlog書き込み失敗数。v8.4.0 以降では TiDB Binlogが削除され、このメトリックには値がありません。
- Client Data Traffic: TiDBとクライアントのデータトラフィック統計

### Transaction {#transaction}

- Transaction OPS: 1秒あたりに実行されるトランザクションの数
- Duration: トランザクションの実行期間
- Transaction Statement Num: トランザクション内のSQL文の数
- Transaction Retry Num: トランザクションが再試行される回数
- Session Retry Error OPS: トランザクション再試行中に発生したエラーの数（1秒あたり）。この指標には、再試行失敗と再試行回数の上限超過という2種類のエラーが含まれます。
- Commit Token Wait Duration: トランザクションのコミット中にフロー制御キューで待機する時間です。待機時間が長い場合、コミットするトランザクションが大きすぎてフローが制御されていることを意味します。システムにまだ利用可能なリソースがある場合は、システム変数`tidb_committer_concurrency`を増やすことでコミットプロセスを高速化できます。
- KV Transaction OPS: 各 TiDB インスタンス内で 1秒あたりに実行されるトランザクションの数
    - ユーザートランザクションは、内部メタデータの読み取りやユーザートランザクションのアトミック再試行など、TiDB内で複数のトランザクション実行をトリガーする可能性があります。
    - TiDBの内部的にスケジュールされたタスクもトランザクションを通じてデータベース上で動作し、このパネルにも含まれています。
- KV Transaction Duration: 各TiDB内でトランザクションを実行するのに費やされた時間
- Transaction Regions Num: トランザクションで操作されるリージョンの数
- Transaction Write KV Num Rate and Sum: トランザクション内でKVが書き込まれるレートと書き込まれたKVの合計
- Transaction Write KV Num: トランザクションで操作されたKVの数
- Statement Lock Keys: 1つのステートメントのロックの数
- Send HeartBeat Duration: トランザクションがハートビートを送信する期間
- Transaction Write Size Bytes Rate and sum: トランザクション内で書き込まれるバイト数と書き込まれたバイト数の合計
- Transaction Write Size Bytes: トランザクションで書き込まれたデータのサイズ
- Acquire Pessimistic Locks Duration: ロックの追加にかかる時間
- TTL Lifetime Reach Counter: TTL の上限に達したトランザクションの数。TTL 上限のデフォルト値は 1時間です。これは、悲観的トランザクションの最初のロック、または楽観的トランザクションの最初の事前書き込みから 1時間が経過したことを意味します。TTL 上限のデフォルト値は 1時間です。TTL 寿命の上限は、TiDB 設定ファイルで`max-txn-TTL`を変更することで変更できます。
- Load Safepoint OPS: `Safepoint`がロードされる回数。`Safepoint`は、トランザクションがデータを読み取る際に`Safepoint`より前のデータが読み込まれないようにすることで、データの安全性を確保するためのものです。`Safepoint`より前のデータはGCによってクリーンアップされる可能性があります。
- Pessimistic Statement Retry OPS：悲観的ステートメントの再試行回数。ステートメントがロックを追加しようとすると、書き込み競合が発生する可能性があります。この場合、ステートメントは新しいスナップショットを取得し、再度ロックを追加します。
- Transaction Types Per Seconds: 2フェーズコミット (2PC)、非同期コミット、および1フェーズコミット (1PC) メカニズムを使用して1秒あたりにコミットされたトランザクションの数 (成功トランザクションと失敗トランザクションの両方を含む)

### Executor {#executor}

- Parse Duration: SQL文の解析時間の統計
- Compile Duration: 解析されたSQL ASTを実行計画にコンパイルする時間の統計
- Execution Duration: SQL文の実行時間の統計
- Expensive Executor OPS: 1秒あたりに多くのシステムリソースを消費するオペレーター（`Merge Join`、`Hash Join`、`Index Look Up Join`、`Hash Agg`、`Stream Agg`、`Sort`、`TopN`を含む）の統計
- Queries Using Plan Cache OPS: プランキャッシュを使用したクエリの1秒あたりの統計
- Plan Cache Miss OPS: 1秒あたりにプランキャッシュがミスされた回数の統計
- Plan Cache Memory Usage: 各 TiDB インスタンスにキャッシュされた実行計画によって消費されるメモリの合計
- Plan Cache Plan Num: 各 TiDB インスタンスにキャッシュされた実行計画の総数

### Distsql {#distsql}

- Distsql Duration: Distsql ステートメントの処理時間
- Distsql QPS: Distsql ステートメントの統計
- Distsql Partial QPS: 1秒あたりの`Partial Result`の数
- Scan Keys Num: 各クエリがスキャンするキーの数
- Scan Keys Partial Num: 各`Partial Result`がスキャンするキーの数
- Partial Num: 各SQL文の`Partial Result`の数

### KV Errors {#kv-errors}

- KV Backoff Duration: KV再試行リクエストの合計継続時間。TiDBはTiKVへのリクエスト送信時にエラーが発生する可能性があります。TiDBはTiKVへのすべてのリクエストに対して再試行メカニズムを備えています。この`KV Backoff Duration`項目は、リクエストの再試行の合計時間を記録します。
- TiClient Region Error OPS: TiKV によって返されたリージョン関連のエラーメッセージの数
- KV Backoff OPS: TiKVによって返されたエラーメッセージの数
- Lock Resolve OPS: ロックを解決するためのTiDB操作の数。TiDBの読み取りまたは書き込みリクエストがロックに遭遇すると、ロックを解決しようとします。
- Other Errors OPS: ロックのクリアや`SafePoint`の更新など、その他の種類のエラーの数

### KV Request {#kv-request}

以下のメトリックは、TiKV に送信されたリクエストに関連します。再試行リクエストは複数回カウントされます。

- KV Request OPS: TiKVに応じて表示されるKVリクエストの実行時間
- KV Request Duration 99 by store: TiKVに応じて表示されるKVリクエストの実行時間
- KV Request Duration 99 by type: リクエストタイプに応じて表示される KV リクエストの実行時間
- Stale Read Hit/Miss Ops
    - **hit**: ステイル読み取りを正常に実行した 1秒あたりのリクエスト数
    - **miss**: ステイル読み取りを試みて失敗したリクエストの1秒あたりの数
- Stale Read Req Ops:
    - **cross-zone**: リモートゾーンでステイル読み取りを試みる 1秒あたりのリクエスト数
    - **local**: ローカルゾーンでステイル読み取りを試みる1秒あたりのリクエスト数
- Stale Read Req Traffic:
    - **cross-zone-in**: リモートゾーンでステイル読み取りを試みるリクエストに対する応答の着信トラフィック
    - **cross-zone-out**: リモートゾーンでステイル読み取りを試みるリクエストに対する応答の送信トラフィック
    - **local-in** : ローカルゾーンでステイル読み取りを試みるリクエストに対する応答の着信トラフィック
    - **local-out** : ローカルゾーンでステイル読み取りを試みるリクエストの送信トラフィック
- Read Req Traffic
    - **leader-local** : ローカルゾーンでのLeader読み取り処理の読み取りリクエストによって生成されたトラフィック
    - **leader-cross-zone** : リモートゾーンでのLeader読み取り処理の読み取りリクエストによって生成されるトラフィック
    - **follower-local** : ローカルゾーンでのFollower Read処理による読み取りリクエストによって生成されるトラフィック
    - **follower-cross-zone** : リモートゾーンでのFollower Read処理による読み取りリクエストによって生成されるトラフィック

### PD Client {#pd-client}

- PD Client CMD OPS: PD クライアントが 1秒あたりに実行したコマンドの統計
- PD Client CMD Duration:PDクライアントがコマンドを実行するのにかかる時間
- PD Client CMD Fail OPS: PD クライアントによって 1秒あたりに実行された失敗したコマンドの統計
- PD TSO OPS: TiDBがPDに送信する1秒あたりのgRPCリクエスト数（cmd）とTSOリクエスト数（request）。各gRPCリクエストには、TSOリクエストのバッチが含まれています。
- PD TSO Wait Duration: TiDB が PD から TSO が返されるまで待機する時間
- PD TSO RPC duration: TiDB が TSO を取得するために PD に gRPC リクエストを送信してから TiDB が PD から gRPC 応答を受信するまでの期間
- Async TSO Duration: TiDBがTSOを取得する準備をする時間から、TiDBが実際にPDがTSOを返すのを待ち始める時間までの期間

### Schema Load {#schema-load}

- Load Schema Duration: TiDBがTiKVからスキーマを取得するのにかかる時間
- Load Schema OPS: TiDBがTiKVから1秒あたりに取得するスキーマの統計
- Schema Lease Error OPM: スキーマ リース エラーには、 `change`と`outdate` 2つのタイプがあります。 `change`は、スキーマが変更されたことを意味し、 `outdate`は、スキーマを更新できないことを意味します。これはより重大なエラーであり、アラートをトリガーします。
- Load Privilege OPS: TiDBがTiKVから1秒あたりに取得した権限情報の件数の統計

### DDL {#ddl}

- DDL Duration 95: DDL文の処理時間の95パーセンタイル
- Batch Add Index Duration 100: 各バッチがインデックス作成に費やした最大時間の統計
- DDL Waiting Jobs Count: 待機中のDDLタスクの数
- DDL META OPM: DDLが1分間にMETAを取得する回数
- DDL Worker Duration 99: 各DDLワーカーの実行時間の99パーセンタイル
- Deploy Syncer Duration: Schema Version Syncer の初期化、再起動、およびクリア操作にかかる時間
- Owner Handle Syncer Duration: DDL所有者がスキーマバージョンを更新、取得、および確認するのにかかる時間
- Update Self Version Duration: Schema Version Syncerのバージョン情報の更新にかかる時間
- DDL OPM: 1秒あたりのDDL実行回数
- DDL backfill progress in percentage：DDL タスクのバックフィルの進行状況

### Statistics {#statistics}

- Auto Analyze Duration 95: 自動`ANALYZE`にかかる時間
- Auto Analyze QPS：自動`ANALYZE`の統計
- Stats Inaccuracy Rate: 統計不正確率の情報
- Pseudo Estimation OPS: 疑似統計を使用して最適化されたSQL文の数
- Dump Feedback OPS: 保存された統計フィードバックの数
- Store Query Feedback QPS: TiDBメモリで実行されるユニオンクエリのフィードバック情報を保存するための1秒あたりの操作数
- Significant Feedback: 統計情報を更新する重要なフィードバックの数
- Update Stats OPS: フィードバックによる統計更新操作の数

### Owner {#owner}

- New ETCD Session Duration 95: 新しいetcdセッションの作成にかかる時間。TiDBはetcdクライアントを介してPD内のetcdに接続し、メタデータ情報を保存/読み取ります。これはセッションの作成に要した時間を記録します。
- Owner Watcher OPS: DDLオーナーウォッチPDのetcdメタデータの1秒あたりのGoroutine操作の数

### Meta {#meta}

- AutoID QPS: 3つの操作 (グローバル ID 割り当て、単一テーブルの AutoID 割り当て、単一テーブルの AutoID リベース) を含む AutoID 関連の統計
- AutoID Duration: AutoID 関連の操作に費やされた時間
- Region Cache Error OPS: TiDBにキャッシュされたリージョン情報で1秒あたりに発生したエラーの数
- Meta Operations Duration 99: メタ操作のレイテンシー

### GC {#gc}

- Worker Action OPM: `run_job`、`resolve_lock`、`delete_range`を含むGC関連操作の数
- Duration 99: GC 関連操作に費やされた時間
- Config: GCデータの有効期間とGC実行間隔の設定
- GC Failure OPM: 失敗したGC関連操作の数
- Delete Range Failure OPM: `Delete Range`が失敗した回数
- Too Many Locks Error OPM: GCがロックをクリアしすぎたエラーの数
- Action Result OPM: GC関連操作の結果の数
- Delete Range Task Status: `Delete Range`のタスクステータス（完了、失敗を含む）
- Push Task Duration 95: GC サブタスクを GC ワーカーにプッシュするのにかかった時間

### Batch Client {#batch-client}

- Pending Request Count by TiKV: 処理が保留中のバッチメッセージの数
- Batch Client Unavailable Duration 95: バッチクライアントが利用できない時間
- No Available Connection Counter: バッチクライアントが利用可能なリンクを見つけられなかった回数

### TTL {#ttl}

- TiDB CPU Usage: 各 TiDB インスタンスの CPU 使用率。
- TiKV IO MBps: 各 TiKV インスタンスの I/O の合計バイト数。
- TiKV CPU: 各 TiKV インスタンスの CPU 使用率。
- TTL QPS By Type: TTL ジョブによって生成されたさまざまなタイプのステートメントの QPS 情報。
- TTL Insert Rows Per Second: 1秒あたりに TTL テーブルに挿入される行数。
- TTL Processed Rows Per Second: 1秒あたりに TTL ジョブによって処理された期限切れの行数。
- TTL Insert Rows Per Hour: 1時間ごとに TTL テーブルに挿入される行数。
- TTL Delete Rows Per Hour: TTL ジョブによって 1時間ごとに削除される期限切れの行数。
- TTL Scan/Delete Query Duration: TTL スキャン/削除ステートメントの実行時間。
- TTL Scan/Delete Worker Time By Phase: TTL 内部ワーカースレッドのさまざまなフェーズで消費された時間。
- TTL Job Count By Status: 現在実行中の TTL ジョブの数。
- TTL Task Count By Status: 現在実行中の TTL タスクの数。
