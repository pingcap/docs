---
title: TiDB Monitoring Metrics
summary: Learn some key metrics displayed on the Grafana TiDB dashboard.
---

# TiDB 監視指標 {#tidb-monitoring-metrics}

TiUPを使用して TiDB クラスターをデプロイすると、監視システム (Prometheus &amp; Grafana) が同時にデプロイされます。監視アーキテクチャについては、 [TiDB 監視フレームワークの概要](/tidb-monitoring-framework.md)を参照してください。

Grafana ダッシュボードは、Overview、PD、TiDB、TiKV、Node_exporter、Disk Performance、および Performance_overview を含む一連のサブ ダッシュボードに分かれています。 TiDB ダッシュボードは、TiDB パネルと TiDB 概要パネルで構成されています。 2 つのパネルの違いは、次の点で異なります。

-   TiDB パネル: クラスターの異常をトラブルシューティングするための可能な限り包括的な情報を提供します。
-   TiDB 概要パネル: TiDB パネルの情報のうち、ユーザーが最も関心を持っている部分をいくつかの変更を加えて抽出します。ユーザーが日々のデータベース運用で気になるデータ（QPS、TPS、応答遅延など）を提供し、表示・報告する監視情報とします。

このドキュメントでは、TiDB ダッシュボードに表示される主要なモニタリング メトリックについて説明します。

## 主要指標の説明 {#key-metrics-description}

TiDB ダッシュボードに表示される主要なメトリックを理解するには、次のセクションを確認してください。

### クエリの概要 {#query-summary}

-   期間: 実行時間
    -   クライアントのネットワーク要求が TiDB に送信されてから、TiDB が要求を実行した後に要求がクライアントに返されるまでの時間。一般に、クライアント要求は SQL ステートメントの形式で送信されますが、 `COM_PING` 、および`COM_SEND_LONG_DATA`などのコマンドの実行時間を含める`COM_STMT_FETCH`もできます`COM_SLEEP`
    -   TiDB は Multi-Query をサポートしているため、 `select 1; select 1; select 1;`などの複数の SQL ステートメントを一度に送信できます。この場合、このクエリの合計実行時間には、すべての SQL ステートメントの実行時間が含まれます。
-   Command Per Second: TiDB が 1 秒間に処理したコマンドの数で、コマンド実行結果の成否に応じて分類されます。
-   QPS: すべての TiDB インスタンスで 1 秒あたりに実行される SQL ステートメントの数。これは、 `SELECT` 、 `INSERT` 、 `UPDATE` 、およびその他のタイプのステートメントに従ってカウントされます
-   CPS By Instance: コマンド実行結果の成功または失敗に従って分類された、各 TiDB インスタンスのコマンド統計
-   Failed Query OPM: 各 TiDB インスタンスで 1 分あたりに SQL ステートメントを実行したときに発生したエラーに応じた、エラーの種類 (構文エラーや主キーの競合など) の統計。エラーが発生したモジュールとエラーコードが含まれています
-   スロー クエリ: スロー クエリの処理時間の統計 (スロー クエリ全体の時間コスト、 コプロセッサーの時間コスト、およびコプロセッサースケジューリングの待機時間)。遅いクエリは、内部 SQL ステートメントと一般的な SQL ステートメントに分類されます
-   Connection Idle Duration: アイドル接続の期間
-   999/99/95/80 Duration: さまざまなタイプの SQL ステートメント (さまざまなパーセンタイル) の実行時間の統計

### クエリの詳細 {#query-detail}

-   期間 80/95/99/999 インスタンス別: 各 TiDB インスタンスでの SQL ステートメントの実行時間の統計 (異なるパーセンタイル)
-   失敗したクエリ OPM の詳細: 各 TiDB インスタンスで 1 分あたりに SQL ステートメントを実行したときに発生したエラーに応じたエラーの種類 (構文エラーや主キーの競合など) の統計
-   内部 SQL OPS: TiDB クラスター全体で 1 秒あたりに実行された内部 SQL ステートメント。内部 SQL ステートメントは内部で実行され、通常はユーザー SQL ステートメントまたは内部でスケジュールされたタスクによってトリガーされます。

### サーバ {#server}

-   Uptime: 各 TiDB インスタンスの実行時間
-   メモリ使用量: 各 TiDB インスタンスのメモリ使用量統計。プロセスが占有するメモリとGolangがヒープに適用するメモリに分けられます。
-   CPU 使用率: 各 TiDB インスタンスの CPU 使用率の統計
-   接続数: 各 TiDB インスタンスに接続されているクライアントの数
-   Open FD Count: 各 TiDB インスタンスの開かれたファイル記述子の統計
-   切断数: 各 TiDB インスタンスに切断されたクライアントの数
-   イベント OPM: 「開始」、「クローズ」、「グレースフル シャットダウン」、「強制終了」、「ハング」などの重要なイベントの統計
-   ゴルーチン カウント: 各 TiDB インスタンスのゴルーチンの数
-   Prepare Statement Count: 各 TiDB インスタンスで実行された`Prepare`ステートメントの数とそれらの合計数
-   Keep Alive OPM: 各 TiDB インスタンスで毎分メトリクスが更新される回数。通常は注意する必要はありません。
-   Panic And Critical Error: TiDB で発生したパニックと重大なエラーの数
-   Time Jump Back OPS: オペレーティング システムが各 TiDB インスタンスで 1 秒ごとに巻き戻す回数
-   Get Token Duration: 各接続でトークンを取得するための時間コスト
-   Skip Binlog Count: TiDB でのbinlog書き込み失敗の数
-   クライアント データ トラフィック: TiDB とクライアントのデータ トラフィック統計

### トランザクション {#transaction}

-   トランザクションOPS: 1 秒あたりに実行されたトランザクションの数
-   期間: トランザクションの実行期間
-   トランザクション Statement Num: トランザクション内の SQL ステートメントの数
-   トランザクション Retry Num: トランザクションが再試行される回数
-   セッション再試行エラー OPS: トランザクション再試行中に発生した 1 秒あたりのエラー数。このメトリックには、再試行の失敗と最大再試行回数の超過の 2 つのエラー タイプが含まれます。
-   コミット トークン待機時間: トランザクション コミット中のフロー制御キューでの待機時間。待機時間が長い場合は、コミットするトランザクションが大きすぎて、フローが制御されていることを意味します。システムに使用可能なリソースがまだある場合は、システム変数`tidb_committer_concurrency`を増やすことでコミット プロセスを高速化できます。
-   KVトランザクションOPS: 各 TiDB インスタンス内で 1 秒あたりに実行されるトランザクションの数
    -   ユーザー トランザクションは、内部メタデータの読み取りやユーザー トランザクションのアトミック再試行など、TiDB で複数のトランザクション実行をトリガーする可能性があります。
    -   TiDB の内部でスケジュールされたタスクも、このパネルに含まれているトランザクションを通じてデータベース上で動作します。
-   KVトランザクション期間: 各 TiDB 内でのトランザクションの実行に費やされた時間
-   トランザクション Regions Num: トランザクションで運営されているリージョンの数
-   トランザクション Write KV Num Rate and Sum: KV が書き込まれる速度と、トランザクションで書き込まれたこれらの KV の合計
-   トランザクション Write KV Num: トランザクションで操作された KV の数
-   ステートメント ロック キー: 1 つのステートメントのロック数
-   Send HeartBeat Duration: トランザクションがハートビートを送信する期間
-   トランザクション書き込みサイズ バイト レートと合計: バイトが書き込まれるレートと、トランザクションで書き込まれたこれらのバイトの合計
-   トランザクション書き込みサイズ バイト: トランザクションで書き込まれたデータのサイズ
-   Acquire Pessimistic Locks Duration: ロックの追加にかかった時間
-   TTL Lifetime Reach Counter: TTL の上限に達したトランザクションの数。 TTL 上限のデフォルト値は 1 時間です。これは、悲観的楽観的トランザクションの最初のロックまたは楽観的トランザクションの最初のプリライトから 1 時間が経過したことを意味します。 TTL の上限のデフォルト値は 1 時間です。 TiDB 設定ファイルの`max-txn-TTL`を変更することで TTL 寿命の上限を変更できます
-   Load Safepoint OPS: `Safepoint`がロードされた回数。 `Safepoint`は、トランザクションがデータを読み取るときに`Safepoint`より前のデータが読み取られないようにすることで、データの安全性を確保します。 `Safepoint`より前のデータは GC によってクリーンアップされる可能性があります
-   悲観的ステートメントの再試行 OPS:悲観的ステートメントの再試行回数。ステートメントがロックを追加しようとすると、書き込み競合が発生する可能性があります。この時点で、ステートメントは新しいスナップショットを取得し、ロックを再度追加します
-   1 秒あたりのトランザクションタイプ: 2 フェーズ コミット (2PC)、非同期コミット、および 1 フェーズ コミット (1PC) メカニズムを使用してコミットされた 1 秒あたりのトランザクション数 (成功および失敗の両方のトランザクションを含む)

### 実行者 {#executor}

-   解析時間: SQL ステートメントの解析時間の統計
-   コンパイル時間: 解析された SQL AST を実行計画にコンパイルする時間の統計
-   実行時間: SQL ステートメントの実行時間の統計
-   Expensive Executor OPS: `Merge Join` 、 `Hash Join` 、 `Index Look Up Join` 、 `Hash Agg` 、 `Stream Agg` 、 `Sort` 、および`TopN`を含む、1 秒あたりに多くのシステム リソースを消費するオペレーターの統計
-   プラン キャッシュを使用したクエリ OPS: 1 秒あたりのプラン キャッシュを使用したクエリの統計
-   Plan Cache Miss OPS: Plan Cache が失われた 1 秒あたりの回数の統計
-   Plan Cache Memory Usage: 各 TiDB インスタンスにキャッシュされた実行プランによって消費される合計メモリ
-   Plan Cache Plan Num: 各 TiDB インスタンスにキャッシュされた実行プランの総数

### Distsql {#distsql}

-   Distsql Duration: Distsql ステートメントの処理時間
-   Distsql QPS: Distsql ステートメントの統計
-   Distsql 部分 QPS: 1 秒ごとの部分結果の数
-   Scan Keys Num: 各クエリがスキャンするキーの数
-   Scan Keys Partial Num: 各部分結果がスキャンするキーの数
-   Partial Num: 各 SQL ステートメントの部分結果の数

### KV エラー {#kv-errors}

-   KV バックオフ期間: KV 再試行要求が続く合計期間。 TiDB が TiKV にリクエストを送信するときにエラーが発生する場合があります。 TiDB には、TiKV へのすべてのリクエストに対して再試行メカニズムがあります。この`KV Backoff Duration`項目は、リクエストの再試行の合計時間を記録します。
-   TiClientリージョンエラー OPS: TiKV によって返されたリージョン関連のエラー メッセージの数
-   KV Backoff OPS: TiKV から返されたエラー メッセージの数
-   ロック解決 OPS: ロックを解決するための TiDB 操作の数。 TiDB の読み取りまたは書き込み要求がロックに遭遇すると、ロックを解決しようとします。
-   その他のエラー OPS: ロックのクリアや更新を含む、その他の種類のエラーの数`SafePoint`

### KV リクエスト {#kv-request}

-   KV リクエスト OPS: TiKV に従って表示される KV リクエストの実行時間
-   KV Request Duration 99 by store: KV リクエストの実行時間。TiKV に従って表示されます。
-   KV Request Duration 99 by type: KV リクエストの実行時間。リクエスト タイプに応じて表示されます。

### PD クライアント {#pd-client}

-   PD クライアント CMD OPS: PD クライアントによって 1 秒間に実行されたコマンドの統計
-   PD クライアント CMD 期間: PD クライアントがコマンドを実行するのにかかる時間
-   PD クライアント CMD 失敗 OPS: PD クライアントによって実行された失敗したコマンドの 1 秒あたりの統計
-   PD TSO OPS: TiDB が 1 秒あたりに PD から取得する TSO の数
-   PD TSO Wait Duration: PD が TSO を返すのを TiDB が待機する時間
-   PD TSO RPC 期間: TiDB が (TSO を取得するために) PD に要求を送信してから、TiDB が TSO を受信するまでの期間
-   Start TSO Wait Duration: TiDB が要求を PD に送信してから ( `start TSO`を取得するため)、TiDB が`start TSO`受信するまでの期間

### スキーマのロード {#schema-load}

-   Load Schema Duration: TiDB が TiKV からスキーマを取得するのにかかる時間
-   Load Schema OPS: TiDB が TiKV から毎秒取得するスキーマの統計
-   スキーマ リース エラー OPM: スキーマ リース エラーには、 `change`と`outdate` 2 つのタイプがあります。 `change`スキーマが変更されたことを意味し、 `outdate`スキーマを更新できないことを意味します。これはより重大なエラーであり、アラートをトリガーします。
-   Load Privilege OPS: TiDB が TiKV から取得した 1 秒あたりの権限情報の数の統計

### DDL {#ddl}

-   DDL 期間 95: DDL ステートメント処理時間の 95% 分位数
-   Batch Add Index Duration 100: 各バッチがインデックスの作成に費やした最大時間の統計
-   DDL Waiting Jobs Count: 待機中の DDL タスクの数
-   DDL META OPM: DDL が毎分 META を取得する回数
-   DDL ワーカー期間 99: 各 DDL ワーカーの実行時間の 99% 分位数
-   デプロイ Syncer Duration: Schema Version Syncer の初期化、再起動、および操作のクリアに費やされた時間
-   Owner Handle Syncer Duration: DDL 所有者がスキーマ バージョンを更新、取得、およびチェックするのにかかる時間
-   Update Self Version Duration: Schema Version Syncer のバージョン情報の更新にかかった時間
-   DDL OPM: 1 秒あたりの DDL 実行数
-   DDL バックフィルの進行状況 (パーセンテージ): DDL タスクのバックフィルの進行状況

### 統計 {#statistics}

-   自動分析時間 95: 自動`ANALYZE`で消費される時間
-   自動分析 QPS: 自動`ANALYZE`の統計
-   統計の不正確率: 統計の不正確率の情報
-   疑似推定 OPS: 疑似統計を使用して最適化された SQL ステートメントの数
-   Dump Feedback OPS: 保存された統計フィードバックの数
-   Store Query Feedback QPS: TiDBメモリで実行されるユニオン クエリのフィードバック情報を格納するための 1 秒あたりの操作数
-   重要なフィードバック: 統計情報を更新する重要なフィードバックの数
-   Update Stats OPS: フィードバックによる統計の更新操作の数
-   Fast Analyze Status 100: 統計情報を迅速に収集するためのステータス

### オーナー {#owner}

-   New ETCD Session Duration 95: 新しい etcd セッションの作成にかかる時間。 TiDB は、etcd クライアントを介して PD の etcd に接続し、一部のメタデータ情報を保存/読み取ります。これは、セッションの作成に費やされた時間を記録します
-   オーナー ウォッチャー OPS: DDL オーナー ウォッチ PD の etcd メタデータの 1 秒あたりのゴルーチン操作の数

### メタ {#meta}

-   AutoID QPS: 3 つの操作 (グローバル ID の割り当て、単一テーブルの AutoID 割り当て、単一テーブルの AutoID Rebase) を含む AutoID 関連の統計
-   AutoID Duration: AutoID 関連の操作にかかった時間
-   リージョン Cache Error OPS: TiDB にキャッシュされたリージョン情報で 1 秒あたりに発生したエラーの数
-   メタ操作期間 99: メタ操作のレイテンシー

### GC {#gc}

-   ワーカー アクション OPM: `run_job` 、 `resolve_lock` 、および`delete_range`を含む GC 関連の操作の数
-   Duration 99: GC 関連の操作に費やされた時間
-   構成: GC データの有効期間と GC の実行間隔の構成
-   GC Failure OPM: 失敗した GC 関連操作の数
-   Delete Range Failure OPM: `Delete Range`が失敗した回数
-   Too Many Locks Error OPM: GC があまりにも多くのロックをクリアするエラーの数
-   Action Result OPM: GC 関連の操作の結果の数
-   削除範囲タスク ステータス: `Delete Range`のタスク ステータス (完了と失敗を含む)
-   Push Task Duration 95: GC サブタスクを GC ワーカーにプッシュするのに費やされた時間

### バッチ クライアント {#batch-client}

-   TiKV による保留中の要求数: 処理が保留中のバッチ メッセージの数
-   Batch Client Unavailable Duration 95: Batch クライアントの使用不可時間
-   No Available Connection Counter: Batch クライアントが利用可能なリンクを見つけられなかった回数

### TTL {#ttl}

-   タイプ別の TTL QPS: TTL ジョブによって生成されたさまざまなタイプのステートメントの QPS 情報。
-   1 秒あたりの TTL 処理行: 1 秒あたりの TTL ジョブによって処理された期限切れの行の数。
-   TTL スキャン/削除クエリ期間: TTL スキャン/削除ステートメントの実行時間。
-   フェーズごとの TTL スキャン/削除ワーカー時間: TTL 内部ワーカー スレッドのさまざまなフェーズで費やされた時間。
-   ステータス別の TTL ジョブ数: 現在実行中の TTL ジョブの数。
