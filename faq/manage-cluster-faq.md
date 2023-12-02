---
title: TiDB Cluster Management FAQs
summary: Learn about the FAQs related to TiDB cluster management.
---

# TiDBクラスタ管理に関するよくある質問 {#tidb-cluster-management-faqs}

このドキュメントには、TiDB クラスター管理に関連する FAQ がまとめられています。

## 日常管理 {#daily-management}

このセクションでは、日常のクラスター管理中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### TiDB にログインするにはどうすればよいですか? {#how-to-log-into-tidb}

MySQL にログインするのと同じように、TiDB にログインできます。例えば：

```bash
mysql -h 127.0.0.1 -uroot -P4000
```

### TiDB でシステム変数を変更するにはどうすればよいですか? {#how-to-modify-the-system-variables-in-tidb}

MySQL と同様に、TiDB には静的パラメーターとソリッド パラメーターが含まれています。 `SET GLOBAL xxx = n`を使用して静的パラメータを直接変更できますが、パラメータの新しい値は、このインスタンスのライフサイクル内でのみ有効です。

### TiDB (TiKV) のデータ ディレクトリはどこにありますか? {#where-and-what-are-the-data-directories-in-tidb-tikv}

TiKV データは[`--data-dir`](/command-line-flags-for-tikv-configuration.md#--data-dir)にあり、バックアップ、db、raft、snap の 4 つのディレクトリが含まれており、それぞれバックアップ、データ、 Raftデータ、ミラー データの保存に使用されます。

### TiDB のシステム テーブルとは何ですか? {#what-are-the-system-tables-in-tidb}

MySQL と同様に、TiDB にはシステム テーブルも含まれており、サーバーの実行時に必要な情報を保存するために使用されます。 [TiDBシステムテーブル](/mysql-schema.md)を参照してください。

### TiDB/PD/TiKV ログはどこにありますか? {#where-are-the-tidb-pd-tikv-logs}

デフォルトでは、TiDB/PD/TiKV は標準エラーをログに出力します。起動時にログファイルを`--log-file`で指定すると、指定したファイルにログが出力され、毎日ローテーションが実行されます。

### TiDB を安全に停止するにはどうすればよいですか? {#how-to-safely-stop-tidb}

-   ロード バランサーが実行中の場合 (推奨): ロード バランサーを停止し、SQL ステートメント`SHUTDOWN`を実行します。その後、TiDB は、すべてのセッションが終了するまで、 [`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-new-in-v50)で指定された期間待機します。その後、TiDB の実行が停止します。

-   ロードバランサが実行されていない場合: `SHUTDOWN`ステートメントを実行します。その後、TiDB コンポーネントが正常に停止されます。

### TiDB で<code>kill</code>を実行できますか? {#can-code-kill-code-be-executed-in-tidb}

-   DML ステートメントを強制終了します。

    まず`information_schema.cluster_processlist`を使用して TiDB インスタンスのアドレスとセッション ID を検索し、次に kill コマンドを実行します。

    TiDB v6.1.0 では、Global Kill 機能が導入されています (デフォルトで有効になっている`enable-global-kill`構成によって制御されます)。 Global Kill が有効な場合は、 `kill session_id`を実行するだけです。

    TiDB バージョンが v6.1.0 より前の場合、または Global Kill 機能が有効になっていない場合、デフォルトでは`kill session_id`は有効になりません。 DML ステートメントを終了するには、DML ステートメントを実行している TiDB インスタンスにクライアントを直接接続し、 `kill tidb session_id`ステートメントを実行する必要があります。クライアントが別の TiDB インスタンスに接続している場合、またはクライアントと TiDB クラスターの間にプロキシがある場合、 `kill tidb session_id`ステートメントが別の TiDB インスタンスにルーティングされる可能性があり、別のセッションが誤って終了する可能性があります。詳細は[`KILL`](/sql-statements/sql-statement-kill.md)を参照してください。

-   DDL ステートメントを強制終了する: まず`admin show ddl jobs`を使用して、終了する必要がある DDL ジョブの ID を見つけてから、 `admin cancel ddl jobs 'job_id' [, 'job_id'] ...`実行します。詳細については、 [`ADMIN`ステートメント](/sql-statements/sql-statement-admin.md)参照してください。

### TiDB はセッション タイムアウトをサポートしていますか? {#does-tidb-support-session-timeout}

TiDB は現在 2 つのタイムアウト、 [`wait_timeout`](/system-variables.md#wait_timeout)と[`interactive_timeout`](/system-variables.md#interactive_timeout)をサポートしています。

### TiDB のバージョン管理戦略とは何ですか? {#what-is-the-tidb-version-management-strategy}

TiDB のバージョン管理の詳細については、 [TiDB のバージョン管理](/releases/versioning.md)を参照してください。

### TiDB クラスターの導入と維持にかかる運用コストはどうでしょうか? {#how-about-the-operating-cost-of-deploying-and-maintaining-a-tidb-cluster}

TiDB は、クラスターを低コストで簡単に管理できるいくつかの機能と[ツール](/ecosystem-tool-user-guide.md)を提供します。

-   メンテナンス操作の場合、 [TiUP](/tiup/tiup-documentation-guide.md)パッケージ マネージャーとして機能し、展開、スケーリング、アップグレード、およびその他のメンテナンス タスクを簡素化します。
-   監視の場合、 [TiDB監視フレームワーク](/tidb-monitoring-framework.md) [プロメテウス](https://prometheus.io/)を使用して監視とパフォーマンスのメトリクスを保存し、 [グラファナ](https://grafana.com/grafana/)を使用してこれらのメトリクスを視覚化します。数百のメトリクスを備えた数十の組み込みパネルが利用可能です。
-   トラブルシューティングのために、TiDBサーバーとその他のコンポーネントの一般的な問題が[TiDB トラブルシューティング マップ](/tidb-troubleshooting-map.md)にまとめられています。関連する問題が発生した場合は、このマップを使用して問題を診断し、解決できます。

### さまざまな TiDB マスター バージョンの違いは何ですか? {#what-s-the-difference-between-various-tidb-master-versions}

TiDB コミュニティは非常に活発です。エンジニアは機能の最適化とバグの修正を続けてきました。したがって、TiDB のバージョンは非常に速く更新されます。最新バージョンの情報を常に知りたい場合は、 [TiDB リリース タイムライン](/releases/release-timeline.md)を参照してください。

TiDB [TiUPを使用する](/production-deployment-using-tiup.md)または[TiDB Operatorを使用する](https://docs.pingcap.com/tidb-in-kubernetes/stable)を導入することをお勧めします。 TiDBではバージョン番号を一元管理しています。次のいずれかの方法を使用してバージョン番号を表示できます。

-   `select tidb_version()`
-   `tidb-server -V`

### TiDB 用のグラフィカル導入ツールはありますか? {#is-there-a-graphical-deployment-tool-for-tidb}

現在のところ、いいえ。

### TiDB クラスターをスケールアウトするにはどうすればよいですか? {#how-to-scale-out-a-tidb-cluster}

オンライン サービスを中断することなく TiDB クラスターをスケールアウトできます。

-   クラスターが[TiUP](/production-deployment-using-tiup.md)使用してデプロイされている場合は、 [TiUPを使用して TiDBクラスタをスケールする](/scale-tidb-using-tiup.md)を参照してください。
-   クラスターが Kubernetes 上の[TiDB Operator](/tidb-operator-overview.md)使用してデプロイされている場合は、 [Kubernetes 上で TiDB を手動でスケールする](https://docs.pingcap.com/tidb-in-kubernetes/stable/scale-a-tidb-cluster)を参照してください。

### TiDB を水平方向にスケーリングするにはどうすればよいですか? {#how-to-scale-tidb-horizontally}

ビジネスが成長するにつれて、データベースは次の 3 つのボトルネックに直面する可能性があります。

-   storageリソースが不足しているため、ディスク領域が十分ではありません。

-   CPU 占有率が高いなど、コンピューティング リソースの不足。

-   十分な書き込みおよび読み取り容量がありません。

ビジネスの成長に合わせて TiDB を拡張できます。

-   ディスク容量が十分でない場合は、TiKV ノードを追加するだけで容量を増やすことができます。新しいノードが起動すると、PD は他のノードから新しいノードにデータを自動的に移行します。

-   コンピューティング リソースが十分でない場合は、TiDB ノードまたは TiKV ノードを追加する前に、まず CPU の消費状況を確認してください。 TiDB ノードが追加されると、ロード バランサーでそれを構成できます。

-   容量が十分でない場合は、TiDB ノードと TiKV ノードの両方を追加できます。

### Percolator が分散ロックを使用し、クラッシュ クライアントがロックを保持している場合、ロックは解放されませんか? {#if-percolator-uses-distributed-locks-and-the-crash-client-keeps-the-lock-will-the-lock-not-be-released}

詳細については、中国語の[パーコレーターと TiDBトランザクションアルゴリズム](https://pingcap.com/blog-cn/percolator-and-txn/)を参照してください。

### TiDB が Thrift ではなく gRPC を使用するのはなぜですか? Googleが使っているからでしょうか？ {#why-does-tidb-use-grpc-instead-of-thrift-is-it-because-google-uses-it}

あまり。フロー制御、暗号化、ストリーミングなど、gRPC のいくつかの優れた機能が必要です。

### <code>like(bindo.customers.name, jason%, 92)</code>の 92 は何を示していますか? {#what-does-the-92-indicate-in-code-like-bindo-customers-name-jason-92-code}

92 はエスケープ文字を示し、デフォルトでは ASCII 92 です。

### <code>information_schema.tables.data_length</code>で表示されるデータ長が、TiKV 監視パネルのストア サイズと異なるのはなぜですか? {#why-does-the-data-length-shown-by-code-information-schema-tables-data-length-code-differ-from-the-store-size-on-the-tikv-monitoring-panel}

2 つの理由:

-   2 つの結果は異なる方法で計算されます。 `information_schema.tables.data_length`は各行の平均長を計算した推定値であり、TiKV 監視パネルのストア サイズは 1 つの TiKV インスタンス内のデータ ファイル (RocksDB の SST ファイル) の長さを合計したものです。
-   `information_schema.tables.data_length`は論理値ですが、ストア サイズは物理値です。複数のバージョンのトランザクションによって生成された冗長データは論理値には含まれませんが、物理値では冗長データが TiKV によって圧縮されます。

### トランザクションが非同期コミットまたは 1 フェーズ コミット機能を使用しないのはなぜですか? {#why-does-the-transaction-not-use-the-async-commit-or-the-one-phase-commit-feature}

次の状況では、システム変数を使用して機能[非同期コミット](/system-variables.md#tidb_enable_async_commit-new-in-v50)と機能[1フェーズコミット](/system-variables.md#tidb_enable_1pc-new-in-v50)を有効にしても、TiDB はこれらの機能を使用しません。

-   TiDB Binlogの実装によって制限されている TiDB Binlogを有効にしている場合、TiDB は非同期コミットまたは 1 フェーズ コミット機能を使用しません。
-   TiDB は、トランザクションに書き込まれるキーと値のペアが 256 個以下で、キーの合計サイズが 4 KB 以下の場合にのみ、非同期コミットまたは 1 フェーズ コミット機能を使用します。これは、大量のデータを書き込むトランザクションの場合、非同期コミットを使用してもパフォーマンスを大幅に改善できないためです。

## PD管理 {#pd-management}

このセクションでは、PD 管理中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### PD にアクセスすると、 <code>TiKV cluster is not bootstrapped</code>メッセージが表示される {#the-code-tikv-cluster-is-not-bootstrapped-code-message-is-displayed-when-i-access-pd}

PD の API のほとんどは、TiKV クラスターが初期化されている場合にのみ使用できます。このメッセージは、新しいクラスターのデプロイ時に TiKV が起動していないときに PD の起動時に PD にアクセスした場合に表示されます。このメッセージが表示された場合は、TiKV クラスターを起動してください。 TiKV が初期化されると、PD にアクセスできるようになります。

### PD の起動時に<code>etcd cluster ID mismatch</code>メッセージが表示される {#the-code-etcd-cluster-id-mismatch-code-message-is-displayed-when-starting-pd}

これは、PD 起動パラメーターの`--initial-cluster`に、このクラスターに属さないメンバーが含まれているためです。この問題を解決するには、各メンバーの対応するクラスターを確認し、間違ったメンバーを削除してから PD を再起動します。

### PDの時刻同期誤差の最大許容範囲はどのくらいですか? {#what-s-the-maximum-tolerance-for-time-synchronization-error-of-pd}

PD はあらゆる同期エラーを許容できますが、エラー値が大きいほど、PD によって割り当てられたタイムスタンプと物理時間の間のギャップが大きくなることを意味し、履歴バージョンの読み取りなどの関数に影響します。

### クライアント接続はどのようにして PD を見つけますか? {#how-does-the-client-connection-find-pd}

クライアント接続は、TiDB 経由でのみクラスターにアクセスできます。 TiDB は PD と TiKV を接続します。 PD と TiKV はクライアントに対して透過的です。 TiDB が任意の PD に接続すると、PD は TiDB に現在のリーダーが誰であるかを通知します。この PD がリーダーでない場合、TiDB はリーダー PD に再接続します。

### TiKV ストアの各ステータス (稼働中、切断、オフライン、ダウン、廃棄) 間の関係は何ですか? {#what-is-the-relationship-between-each-status-up-disconnect-offline-down-tombstone-of-a-tikv-store}

各ステータスの関係については[TiKVストアの各ステータスの関係](/tidb-scheduling.md#information-collection)を参照してください。

PD Control を使用して、TiKV ストアのステータス情報を確認できます。

### PD の<code>leader-schedule-limit</code>パラメーターと<code>region-schedule-limit</code>スケジューリング パラメーターの違いは何ですか? {#what-is-the-difference-between-the-code-leader-schedule-limit-code-and-code-region-schedule-limit-code-scheduling-parameters-in-pd}

-   `leader-schedule-limit`スケジューリング パラメーターは、さまざまな TiKV サーバーのLeader数のバランスをとるために使用され、クエリ処理の負荷に影響します。
-   `region-schedule-limit`スケジューリング パラメーターは、さまざまな TiKV サーバーのレプリカ数のバランスをとるために使用され、さまざまなノードのデータ量に影響します。

### 各リージョンのレプリカの数は構成可能ですか? 「はい」の場合、どのように設定すればよいですか? {#is-the-number-of-replicas-in-each-region-configurable-if-yes-how-to-configure-it}

はい。現在、更新できるのはレプリカのグローバル数のみです。初めて起動すると、PD は構成ファイル (conf/pd.yml) を読み取り、その中の max-replicas 構成を使用します。後で番号を更新する場合は、pd-ctl コンフィグレーション コマンド`config set max-replicas $num`を使用し、有効な設定を`config show all`で表示します。更新はアプリケーションには影響せず、バックグラウンドで設定されます。

TiKV インスタンスの合計数が常に、設定したレプリカの数以上であることを確認してください。たとえば、3 つのレプリカには少なくとも 3 つの TiKV インスタンスが必要です。レプリカの数を増やす前に、追加のstorage要件を見積もる必要があります。 pd-ctl の詳細については、 [PD Controlユーザーガイド](/pd-control.md)を参照してください。

### コマンドラインクラスター管理ツールがない場合にクラスター全体の健全性状態を確認するにはどうすればよいですか? {#how-to-check-the-health-status-of-the-whole-cluster-when-lacking-command-line-cluster-management-tools}

pd-ctl ツールを使用して、クラスターの一般的なステータスを確認できます。クラスターの詳細なステータスについては、モニターを使用して判断する必要があります。

### オフラインのクラスターノードの監視データを削除するにはどうすればよいですか? {#how-to-delete-the-monitoring-data-of-a-cluster-node-that-is-offline}

オフライン ノードは通常、TiKV ノードを指します。オフライン処理が終了したかどうかは、pd-ctl またはモニタで判断できます。ノードがオフラインになったら、次の手順を実行します。

1.  オフライン ノード上の関連サービスを手動で停止します。
2.  Prometheus設定ファイルから該当ノードの`node_exporter`データを削除します。

## TiDBサーバー管理 {#tidb-server-management}

このセクションでは、TiDBサーバーの管理中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### TiDB で<code>lease</code>パラメータを設定するにはどうすればよいですか? {#how-to-set-the-code-lease-code-parameter-in-tidb}

リース パラメータ ( `--lease=60` ) は、TiDBサーバーの起動時にコマンド ラインから設定されます。リース パラメーターの値は、現在のセッションのデータベース スキーマ変更 (DDL) 速度に影響します。テスト環境では、値を 1 秒に設定して、テスト サイクルを高速化できます。ただし、本番環境では、DDL の安全性を確保するために、値を分 (たとえば、60) に設定することをお勧めします。

### DDL 操作の処理時間はどれくらいですか? {#what-is-the-processing-time-of-a-ddl-operation}

処理時間はシナリオによって異なります。一般に、次の 3 つのシナリオが考えられます。

1.  対応するデータテーブルの行数が比較的少ない`Add Index`操作: 約 3 秒
2.  対応するデータテーブル内の行数が比較的多い`Add Index`操作: 処理時間は、特定の行数とその時点の QPS によって異なります ( `Add Index`操作は通常の SQL 操作より優先順位が低くなります)
3.  その他の DDL 操作: 約 1 秒

DDL リクエストを受信する TiDBサーバーインスタンスが、DDL 所有者がいる TiDBサーバーインスタンスと同じである場合、上記の 1 番目と 3 番目のシナリオのコストは数十から数百ミリ秒だけである可能性があります。

### DDL ステートメントの実行が時々非常に遅くなるのはなぜですか? {#why-it-is-very-slow-to-run-ddl-statements-sometimes}

考えられる理由:

-   複数の DDL ステートメントを一緒に実行すると、最後のいくつかの DDL ステートメントの実行が遅くなる可能性があります。これは、DDL ステートメントが TiDB クラスター内でシリアルに実行されるためです。
-   クラスターが正常に起動した後、最初の DDL 操作の実行には時間がかかることがあります (通常は約 30 秒)。これは、TiDB クラスターが DDL ステートメントを処理するリーダーを選択しているためです。
-   以下の条件を満たす場合、TiDB 起動後の最初の 10 分間の DDL ステートメントの処理時間が通常よりも大幅に長くなることがあります。 1) TiDB 停止中は通常どおり TiDB が PD と通信できない (停電の場合も含む) ); 2) TiDB は`kill -9`コマンドによって停止されるため、時間内に PD から登録データをクリーンアップできません。この期間中に DDL ステートメントを実行すると、各 DDL の状態が変化するまで、2 * リース (リース = 45 秒) 待つ必要があります。
-   クラスター内の TiDBサーバーと PDサーバーの間で通信の問題が発生した場合、TiDBサーバーはPDサーバーからバージョン情報を時間内に取得または更新できません。この場合、各 DDL の状態処理のために 2 * リースを待つ必要があります。

### S3 を TiDB のバックエンドstorageエンジンとして使用できますか? {#can-i-use-s3-as-the-backend-storage-engine-in-tidb}

いいえ。現在、TiDB は分散storageエンジンと Goleveldb/RocksDB/BoltDB エンジンのみをサポートしています。

### <code>Information_schema</code>より実際の情報をサポートできますか? {#can-the-code-information-schema-code-support-more-real-information}

MySQL 互換性の一環として、TiDB は多数の`INFORMATION_SCHEMA`テーブルをサポートします。これらのテーブルの多くには、対応する SHOW コマンドもあります。詳細については、 [情報スキーマ](/information-schema/information-schema.md)を参照してください。

### TiDB バックオフ タイプのシナリオの説明は何ですか? {#what-s-the-explanation-of-the-tidb-backoff-type-scenario}

TiDBサーバーと TiKVサーバー間の通信プロセスにおいて、大量のデータを処理するときに`Server is busy`または`backoff.maxsleep 20000ms`ログ メッセージが表示されます。これは、TiKVサーバーがデータを処理している間、システムがビジー状態になるためです。このとき、通常、TiKV ホストのリソース使用率が高いことがわかります。この問題が発生した場合は、リソースの使用状況に応じてサーバーの容量を増やすことができます。

### TiDB TiClient タイプの主な理由は何ですか? {#what-is-the-main-reason-of-tidb-ticlient-type}

TiClientリージョンエラー インジケーターは、TiDBサーバーがクライアントとして KV インターフェースを介して TiKVサーバーにアクセスし、データ操作を実行するときに表示されるエラーのタイプとメトリクスを示します。エラーの種類には`not_leader`と`stale_epoch`があります。これらのエラーは、TiDBサーバーが独自のキャッシュ情報に従ってリージョンリーダー データを操作する場合、リージョンリーダーが移行された場合、または現在の TiKVリージョン情報と TiDB キャッシュのルーティング情報が矛盾している場合に発生します。通常、この場合、TiDBサーバーはPD から最新のルーティング データを自動的に取得し、前の操作をやり直します。

### TiDB がサポートする同時接続の最大数はどれくらいですか? {#what-s-the-maximum-number-of-concurrent-connections-that-tidb-supports}

デフォルトでは、TiDBサーバーごとの最大接続数に制限はありません。必要に応じて、 `config.toml`ファイルで`instance.max_connections`を設定するか、システム変数[`max_connections`](/system-variables.md#max_connections)の値を変更することで、最大接続数を制限できます。同時実行数が大きすぎると応答時間が長くなる場合は、TiDB ノードを追加して容量を増やすことをお勧めします。

### テーブルの作成時間を確認するにはどうすればよいですか? {#how-to-view-the-creation-time-of-a-table}

`information_schema`のテーブルの`create_time`作成時刻です。

### TiDB ログ内の<code>EXPENSIVE_QUERY</code>の意味は何ですか? {#what-is-the-meaning-of-code-expensive-query-code-in-the-tidb-log}

TiDB が SQL ステートメントを実行しているとき、各オペレーターが 10,000 行を超える行を処理すると推定される場合、クエリは`EXPENSIVE_QUERY`になります。 `tidb-server`設定パラメータを変更してしきい値を調整し、 `tidb-server`を再起動できます。

### TiDB のテーブルのサイズを見積もるにはどうすればよいですか? {#how-do-i-estimate-the-size-of-a-table-in-tidb}

TiDB のテーブルのサイズを見積もるには、次のクエリ ステートメントを使用できます。

```sql
SELECT
  db_name,
  table_name,
  ROUND(SUM(total_size / cnt), 2) Approximate_Size,
  ROUND(
    SUM(
      total_size / cnt / (
        SELECT
          ROUND(AVG(value), 2)
        FROM
          METRICS_SCHEMA.store_size_amplification
        WHERE
          value > 0
      )
    ),
    2
  ) Disk_Size
FROM
  (
    SELECT
      db_name,
      table_name,
      region_id,
      SUM(Approximate_Size) total_size,
      COUNT(*) cnt
    FROM
      information_schema.TIKV_REGION_STATUS
    WHERE
      db_name = @dbname
      AND table_name IN (@table_name)
    GROUP BY
      db_name,
      table_name,
      region_id
  ) tabinfo
GROUP BY
  db_name,
  table_name;
```

上記のステートメントを使用する場合は、ステートメント内の次のフィールドに必要に応じて入力し、置き換える必要があります。

-   `@dbname` : データベースの名前。
-   `@table_name` : ターゲットテーブルの名前。

さらに、上記のステートメントでは次のようになります。

-   `store_size_amplification`クラスター圧縮率の平均を示します。 `SELECT * FROM METRICS_SCHEMA.store_size_amplification;`を使用してこの情報をクエリすることに加えて、 **Grafana Monitoring PD - 統計バランス**パネルで各ノードの**サイズ増幅**メトリックを確認することもできます。クラスター圧縮率の平均は、すべてのノードのサイズ増幅の平均です。
-   `Approximate_Size`圧縮前のレプリカ内のテーブルのサイズを示します。これはおおよその値であり、正確な値ではないことに注意してください。
-   `Disk_Size`圧縮後のテーブルのサイズを示します。これは近似値であり、 `Approximate_Size`と`store_size_amplification`に従って計算できます。

## TiKVサーバー管理 {#tikv-server-management}

このセクションでは、TiKVサーバーの管理中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### コンプライアンスまたはマルチテナント アプリケーションのデータの場所を指定するにはどうすればよいですか? {#how-to-specify-the-location-of-data-for-compliance-or-multi-tenant-applications}

[配置ルール](/placement-rules-in-sql.md)を使用して、コンプライアンス アプリケーションまたはマルチテナント アプリケーションのデータの場所を指定できます。

SQL の配置ルールは、レプリカの数、 Raftロール、配置場所、ルールが有効になるキー範囲などの連続データ範囲の属性を制御するように設計されています。

### TiKV クラスター内のレプリカの推奨数はどれくらいですか?高可用性を実現するには、最小数を維持する方がよいでしょうか? {#what-is-the-recommended-number-of-replicas-in-the-tikv-cluster-is-it-better-to-keep-the-minimum-number-for-high-availability}

テスト環境には、各リージョンに 3 つのレプリカがあれば十分です。ただし、本番シナリオでは 3 ノード未満の TiKV クラスターを運用しないでください。インフラストラクチャ、ワークロード、復元力のニーズに応じて、この数値を増やすことが必要な場合があります。コピー数が多いほどパフォーマンスは低下しますが、セキュリティは高くなることに注意してください。

### TiKV の起動時に<code>cluster ID mismatch</code>メッセージが表示される {#the-code-cluster-id-mismatch-code-message-is-displayed-when-starting-tikv}

これは、ローカル TiKV に格納されているクラスター ID が PD で指定されたクラスター ID と異なるためです。新しい PD クラスターが展開されると、PD はランダムなクラスター ID を生成します。 TiKV は、初期化時に PD からクラスター ID を取得し、クラスター ID をローカルに保存します。次回、TiKV が起動されると、ローカル クラスター ID が PD 内のクラスター ID と照合されます。クラスター ID が一致しない場合は、 `cluster ID mismatch`メッセージが表示され、TiKV が終了します。

以前に PD クラスターをデプロイしていて、その後 PD データを削除して新しい PD クラスターをデプロイすると、TiKV が古いデータを使用して新しい PD クラスターに接続するため、このエラーが発生します。

### TiKV起動時に<code>duplicated store address</code>メッセージが表示される {#the-code-duplicated-store-address-code-message-is-displayed-when-starting-tikv}

これは、起動パラメータのアドレスが他の TiKV によって PD クラスタに登録されているためです。このエラーが発生する一般的な条件: TiKV `--data-dir`で指定されたパスにデータ フォルダーがありません (削除または移動後に --data-dir が更新されません)。以前のパラメーターで TiKV を再起動します。pd-ctl の[ストア削除](https://github.com/pingcap/pd/tree/55db505e8f35e8ab4e00efd202beb27a8ecc40fb/tools/pd-ctl#store-delete--label--weight-store_id----jqquery-string)機能を試してください。以前のストアを削除してから、TiKV を再起動します。

### TiKV プライマリ ノードとセカンダリ ノードは同じ圧縮アルゴリズムを使用していますが、結果が異なるのはなぜですか? {#tikv-primary-node-and-secondary-node-use-the-same-compression-algorithm-why-the-results-are-different}

現在、TiKV プライマリ ノードの一部のファイルはより高い圧縮率を持っていますが、これは基盤となるデータ分散と RocksDB の実装に依存します。データ サイズが時々変動するのは正常です。基盤となるstorageエンジンは、必要に応じてデータを調整します。

### TiKVブロックキャッシュの特徴は何ですか? {#what-are-the-features-of-tikv-block-cache}

TiKV は、RocksDB のカラムファミリー (CF) 機能を実装します。デフォルトでは、KV データは最終的に RocksDB 内の 3 つの CF (デフォルト、書き込み、ロック) に保存されます。

-   デフォルトの CF は実データを格納し、対応するパラメータは`[rocksdb.defaultcf]`にあります。
-   ライト CF にはデータ バージョン情報 (MVCC) とインデックス関連データが格納され、対応するパラメーターは`[rocksdb.writecf]`になります。
-   ロック CF にはロック情報が格納され、システムはデフォルトのパラメータを使用します。
-   Raft RocksDB インスタンスはRaftログを保存します。デフォルトの CF は主にRaftログを保存し、対応するパラメータは`[raftdb.defaultcf]`にあります。
-   すべての CF には、データ ブロックをキャッシュし、RocksDB の読み取り速度を向上させるための共有ブロック キャッシュがあります。ブロック キャッシュのサイズは`block-cache-size`パラメータによって制御されます。パラメータの値が大きいほど、より多くのホット データをキャッシュでき、読み取り操作に有利になることを意味します。同時に、より多くのシステムメモリを消費します。
-   各 CF には個別の書き込みバッファがあり、サイズは`write-buffer-size`パラメータによって制御されます。

### TiKV チャンネルがいっぱいなのはなぜですか? {#why-is-the-tikv-channel-full}

-   Raftstoreスレッドが遅すぎるか、I/O によってブロックされています。 RaftstoreのCPU使用状況を確認できます。
-   TiKV はビジー状態 (CPU やディスク I/O など) のため、処理できません。

### TiKV が頻繁にリージョンリーダーを交代するのはなぜですか? {#why-does-tikv-frequently-switch-region-leader}

-   ネットワークの問題により、ノード間の通信が停止します。レポート障害監視を確認できます。
-   元のメインLeaderのノードがスタックし、時間内にFollowerに連絡できなくなります。
-   Raftstoreスレッドがスタックしました。

### ノードがダウンした場合、サービスは影響を受けますか? 「はい」の場合、どのくらいの期間ですか? {#if-a-node-is-down-will-the-service-be-affected-if-yes-how-long}

TiKV は、 Raftを使用して複数のレプリカ間でデータを複製します (デフォルトでは、リージョンごとに 3 つのレプリカ)。 1 つのレプリカに障害が発生しても、他のレプリカがデータの安全性を保証できます。 Raftプロトコルに基づいて、ノードがダウンして単一のリーダーに障害が発生した場合、最大 2 * リース時間 (リース時間は 10 秒) の後に、別のノードのフォロワーがすぐにリージョンリーダーとして選出されます。

### I/O、メモリ、CPU を大量に消費し、パラメータ構成を超える TiKV シナリオは何ですか? {#what-are-the-tikv-scenarios-that-take-up-high-i-o-memory-cpu-and-exceed-the-parameter-configuration}

TiKV で大量のデータの書き込みまたは読み取りを行うと、大量の I/O、メモリ、CPU が消費されます。非常に複雑なクエリを実行すると、大規模な中間結果セットを生成するシナリオなど、大量のメモリと CPU リソースが消費されます。

### TiKV は SAS/SATA ディスク、または SSD/SAS ディスクの混合展開をサポートしていますか? {#does-tikv-support-sas-sata-disks-or-mixed-deployment-of-ssd-sas-disks}

いいえ。OLTP シナリオの場合、TiDB はデータ アクセスと操作に高 I/O ディスクを必要とします。 TiDB は、強整合性を備えた分散データベースとして、レプリカのレプリケーションや最レイヤーのstorage圧縮などの書き込み増幅機能を備えています。したがって、TiDB のベスト プラクティスでは、storageディスクとして NVMe SSD を使用することをお勧めします。 TiKV と PD の混合展開はサポートされていません。

### Keyデータテーブルの範囲はデータアクセス前に分割されていますか？ {#is-the-range-of-the-key-data-table-divided-before-data-access}

いいえ、MySQL のテーブル分割ルールとは異なります。 TiKV では、テーブル Range はリージョンのサイズに基づいて動的に分割されます。

### リージョンはどのように分割されますか? {#how-does-region-split}

リージョンは事前に分割されていませんが、リージョン分割メカニズムに従います。リージョンサイズが`region-max-size`または`region-max-keys`パラメータの値を超えると、分割がトリガーされます。解散後、その情報はPDに報告されます。

### データのセキュリティを保証するために、TiKV には MySQL のような<code>innodb_flush_log_trx_commit</code>パラメータがありますか? {#does-tikv-have-the-code-innodb-flush-log-trx-commit-code-parameter-like-mysql-to-guarantee-the-security-of-data}

はい。現在、スタンドアロンstorageエンジンは 2 つの RocksDB インスタンスを使用しています。 1 つのインスタンスは raft ログの保存に使用されます。 TiKV の`sync-log`パラメータが true に設定されている場合、各コミットは強制的に raft ログにフラッシュされます。クラッシュが発生した場合は、raft-log を使用して KV データを復元できます。

### WALstorageの推奨サーバー構成 (SSD、RAID レベル、RAID カードのキャッシュ戦略、NUMA 構成、ファイル システム、オペレーティング システムの I/O スケジューリング戦略など) は何ですか? {#what-is-the-recommended-server-configuration-for-wal-storage-such-as-ssd-raid-level-cache-strategy-of-raid-card-numa-configuration-file-system-i-o-scheduling-strategy-of-the-operating-system}

WAL は順序付けされた書き込みに属しており、現時点では独自の構成は適用されていません。推奨される構成は次のとおりです。

-   SSD
-   RAID 10 を推奨
-   RAID カードのキャッシュ戦略とオペレーティング システムの I/O スケジューリング戦略: 現在、具体的なベスト プラクティスはありません。 Linux 7 以降ではデフォルト構成を使用できます
-   NUMA: 具体的な提案はありません。メモリ割り当て戦略には`interleave = all`を使用できます。
-   ファイルシステム: ext4

### 最も厳密なデータ利用可能モード ( <code>sync-log = true</code> ) での書き込みパフォーマンスはどうですか? {#how-is-the-write-performance-in-the-most-strict-data-available-mode-code-sync-log-true-code}

一般に、 `sync-log`有効にすると、パフォーマンスが約 30% 低下します。 `sync-log`を`false`に設定した場合の書き込みパフォーマンスについては、 [Sysbenchを使用したTiDBのパフォーマンステスト結果](/benchmark/v3.0-performance-benchmarking-with-sysbench.md)参照してください。

### Raft + TiKVアーキテクチャの複数のレプリカは絶対的なデータ安全性を実現できますか?スタンドアロンstorageに最も厳密なモード ( <code>sync-log = true</code> ) を適用する必要がありますか? {#can-raft-multiple-replicas-in-the-tikv-architecture-achieve-absolute-data-safety-is-it-necessary-to-apply-the-most-strict-mode-code-sync-log-true-code-to-a-standalone-storage}

データは[Raftコンセンサス アルゴリズム](https://raft.github.io/)使用して TiKV ノード間で冗長的に複製され、ノード障害が発生した場合の回復可能性を確保します。データがレプリカの 50% を超えて書き込まれた場合にのみ、アプリケーションは ACK を返します (3 ノードのうち 2 ノード)。ただし、理論的には 2 つのノードがクラッシュする可能性があります。したがって、データの安全性についてはそれほど厳密ではないが、パフォーマンスについては極端な要件があるシナリオを除き、 `sync-log`モードを有効にすることを強くお勧めします。

`sync-log`を使用する代わりに、 Raftグループに 3 つではなく 5 つのレプリカを含めることも検討できます。これにより、データの安全性を確保しながら、2 つのレプリカの障害が許容されます。

スタンドアロン TiKV ノードの場合も、 `sync-log`モードを有効にすることが推奨されます。そうしないと、ノード障害が発生した場合に最後の書き込みが失われる可能性があります。

### TiKV はRaftプロトコルを使用するため、データの書き込み中に複数のネットワーク ラウンドトリップが発生します。実際の書き込み遅延はどれくらいですか? {#since-tikv-uses-the-raft-protocol-multiple-network-roundtrips-occur-during-data-writing-what-is-the-actual-write-delay}

理論的には、TiDB の書き込み遅延は、スタンドアロン データベースよりもネットワーク ラウンドトリップ 4 回多くなります。

### TiDB には、KV インターフェイスを直接使用でき、独立したキャッシュを必要としない MySQL のような InnoDB memcached プラグインがありますか? {#does-tidb-have-an-innodb-memcached-plugin-like-mysql-which-can-directly-use-the-kv-interface-and-does-not-need-the-independent-cache}

TiKV はインターフェイスの個別呼び出しをサポートしています。理論的には、インスタンスをキャッシュとして使用できます。 TiDB は分散リレーショナル データベースであるため、TiKV を個別にサポートしていません。

### コプロセッサーコンポーネントは何に使用されますか? {#what-is-the-coprocessor-component-used-for}

-   TiDB と TiKV 間のデータ送信を削減する
-   TiKVの分散コンピューティングリソースを最大限に活用して、コンピューティングプッシュダウンを実行します。

### エラー メッセージ<code>IO error: No space left on device While appending to file</code>が表示される {#the-error-message-code-io-error-no-space-left-on-device-while-appending-to-file-code-is-displayed}

ディスク容量が足りないためです。ノードを追加するか、ディスク容量を増やす必要があります。

### TiKV で OOM (メモリ不足) エラーが頻繁に発生するのはなぜですか? {#why-does-the-oom-out-of-memory-error-occur-frequently-in-tikv}

TiKV のメモリ使用量は主に RocksDB のブロック キャッシュから発生し、デフォルトではシステムメモリサイズの 40% になります。 TiKV で OOM エラーが頻繁に発生する場合は、 `block-cache-size`の値が高すぎないか確認する必要があります。さらに、複数の TiKV インスタンスが 1 台のマシンにデプロイされている場合は、複数のインスタンスがシステムメモリを過剰に使用して OOM エラーが発生するのを防ぐために、パラメータを明示的に構成する必要があります。

### TiDB データと RawKV データの両方を同じ TiKV クラスターに保存できますか? {#can-both-tidb-data-and-rawkv-data-be-stored-in-the-same-tikv-cluster}

いいえ。TiDB (またはトランザクション API から作成されたデータ) は、特定のキー形式に依存しています。 RawKV API から作成されたデータ (または他の RawKV ベースのサービスからのデータ) とは互換性がありません。

## TiDB テスト {#tidb-testing}

このセクションでは、TiDB のテスト中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### Sysbench を使用した TiDB のパフォーマンス テストの結果は何ですか? {#what-is-the-performance-test-result-for-tidb-using-sysbench}

多くのユーザーは最初に、TiDB と MySQL の間のベンチマーク テストや比較テストを行う傾向があります。また、同様の公式テストを実施したところ、テストデータには多少の偏りがあるものの、テスト結果は全体的に一貫していることがわかりました。 TiDB のアーキテクチャはMySQL とは大きく異なるため、ベンチマーク ポイントを見つけるのは困難です。提案は次のとおりです。

-   ベンチマーク テストにあまり時間をかけすぎないでください。 TiDB を使用するシナリオの違いにさらに注目してください。
-   [Sysbenchを使用したTiDBのパフォーマンステスト結果](/benchmark/v3.0-performance-benchmarking-with-sysbench.md)を参照してください。

### TiDB クラスター容量 (QPS) とノード数の関係は何ですか? TiDB と MySQL を比較するとどうですか? {#what-s-the-relationship-between-the-tidb-cluster-capacity-qps-and-the-number-of-nodes-how-does-tidb-compare-to-mysql}

-   10 ノード以内では、TiDB 書き込み容量 (TPS の挿入) とノード数の関係は、およそ 40% 直線的に増加します。 MySQL は単一ノード書き込みを使用するため、その書き込み容量を拡張することはできません。
-   MySQLでは、セカンダリデータベースを追加することで読み取り容量を増やすことができますが、書き込み容量はシャーディングを使用する以外に増やすことができず、多くの問題があります。
-   TiDB では、ノードを追加することで読み取りと書き込みの両方の容量を簡単に増やすことができます。

### 当社の DBA による MySQL と TiDB のパフォーマンス テストでは、スタンドアロン TiDB のパフォーマンスが MySQL ほど良くないことが示されました。 {#the-performance-test-of-mysql-and-tidb-by-our-dba-shows-that-the-performance-of-a-standalone-tidb-is-not-as-good-as-mysql}

TiDB は、MySQL スタンドアロンの容量が制限されているためにシャーディングが使用され、強い一貫性と完全な分散トランザクションが必要なシナリオ向けに設計されています。 TiDB の利点の 1 つは、コンピューティングをstorageノードにプッシュダウンして同時コンピューティングを実行できることです。

TiDB は、小さなサイズのテーブル (1,000 万レベル未満など) には適していません。これは、データのサイズが小さく、リージョンが限られている場合には同時実行性の強さを発揮できないためです。典型的な例はカウンタ テーブルで、数行のレコードが頻繁に更新されます。 TiDB では、これらの行はstorageエンジン内で複数のキーと値のペアになり、単一ノード上にあるリージョンに落ち着きます。強力な一貫性と TiDB から TiKV への操作を保証するためのバックグラウンド レプリケーションのオーバーヘッドにより、MySQL スタンドアロンよりもパフォーマンスが低下します。

## バックアップと復元 {#backup-and-restoration}

このセクションでは、バックアップと復元中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### TiDB のデータをバックアップするにはどうすればよいですか? {#how-to-back-up-data-in-tidb}

現在、大容量データ (1 TB を超える) のバックアップには、 [バックアップと復元 (BR)](/br/backup-and-restore-overview.md)使用する方法が推奨されています。それ以外の場合、推奨されるツールは[Dumpling](/dumpling-overview.md)です。 TiDB では、データのバックアップと復元のために公式 MySQL ツール`mysqldump`もサポートされていますが、そのパフォーマンスはBRよりも優れているわけではなく、大量のデータのバックアップと復元にはさらに多くの時間が必要です。

BRに関するその他の FAQ については、 [BRよくある質問](/faq/backup-and-restore-faq.md)を参照してください。

### バックアップと復元の速度はどうですか? {#how-is-the-speed-of-backup-and-restore}

[BR](/br/backup-and-restore-overview.md)を使用してバックアップおよび復元タスクを実行する場合、バックアップは TiKV インスタンスあたり約 40 MB/秒で処理され、復元は TiKV インスタンスあたり約 100 MB/秒で処理されます。
