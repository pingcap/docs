---
title: TiDB Cluster Management FAQs
summary: Learn about the FAQs related to TiDB cluster management.
---

# TiDBクラスタ管理に関するよくある質問 {#tidb-cluster-management-faqs}

このドキュメントは、TiDB クラスター管理に関連する FAQ をまとめたものです。

## 日常管理 {#daily-management}

このセクションでは、日常のクラスター管理中に発生する可能性がある一般的な問題、その原因、および解決策について説明します。

### TiDB にログインするには？ {#how-to-log-into-tidb}

MySQL にログインするのと同じように、TiDB にログインできます。例えば：

```bash
mysql -h 127.0.0.1 -uroot -P4000
```

### TiDB でシステム変数を変更するには? {#how-to-modify-the-system-variables-in-tidb}

MySQL と同様に、TiDB には静的パラメーターと固体パラメーターが含まれています。 `SET GLOBAL xxx = n`を使用して静的パラメーターを直接変更できますが、パラメーターの新しい値は、このインスタンスのライフサイクル内でのみ有効です。

### TiDB (TiKV) のデータ ディレクトリはどこにあり、どのようなものですか? {#where-and-what-are-the-data-directories-in-tidb-tikv}

TiKV データは[`--data-dir`](/command-line-flags-for-tikv-configuration.md#--data-dir)にあり、そこには backup、db、raft、snap の 4 つのディレクトリがあり、それぞれバックアップ、データ、 Raftデータ、およびミラー データを格納するために使用されます。

### TiDB のシステム テーブルとは何ですか? {#what-are-the-system-tables-in-tidb}

MySQL と同様に、TiDB にはシステム テーブルも含まれており、サーバーの実行時に必要な情報を格納するために使用されます。 [TiDB システム テーブル](/mysql-schema.md)を参照してください。

### TiDB/PD/TiKV ログはどこにありますか? {#where-are-the-tidb-pd-tikv-logs}

デフォルトでは、TiDB/PD/TiKV は標準エラーをログに出力します。起動時にログファイルを`--log-file`で指定すると、指定したファイルにログを出力し、日次ローテーションを実行します。

### TiDB を安全に停止するには? {#how-to-safely-stop-tidb}

-   ロード バランサーが実行されている場合 (推奨): ロード バランサーを停止し、SQL ステートメント`SHUTDOWN`を実行します。次に、TiDB は、すべてのセッションが終了するまで、 [`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-new-in-v50)で指定された期間待機します。その後、TiDB は実行を停止します。

-   ロードバランサーが実行されていない場合: `SHUTDOWN`ステートメントを実行します。その後、TiDB コンポーネントは正常に停止します。

### <code>kill</code> TiDB で実行できますか? {#can-code-kill-code-be-executed-in-tidb}

-   DML ステートメントを強制終了します。

    最初に`information_schema.cluster_processlist`を使用して TiDB インスタンスのアドレスとセッション ID を検索し、次に kill コマンドを実行します。

    TiDB v6.1.0 では、Global Kill 機能が導入されています (デフォルトで有効になっている`enable-global-kill`構成によって制御されます)。 Global Kill が有効になっている場合は、 `kill session_id`を実行するだけです。

    TiDB のバージョンが v6.1.0 より前の場合、または Global Kill 機能が有効になっていない場合、デフォルトでは`kill session_id`は有効になりません。 DML ステートメントを終了するには、DML ステートメントを実行している TiDB インスタンスにクライアントを直接接続してから、 `kill tidb session_id`ステートメントを実行する必要があります。クライアントが別の TiDB インスタンスに接続するか、クライアントと TiDB クラスターの間にプロキシがある場合、 `kill tidb session_id`ステートメントが別の TiDB インスタンスにルーティングされ、別のセッションが誤って終了する可能性があります。詳細については、 [`KILL`](/sql-statements/sql-statement-kill.md)を参照してください。

-   DDL ステートメントを強制終了します。最初に`admin show ddl jobs`使用して、終了する必要がある DDL ジョブの ID を見つけ、次に`admin cancel ddl jobs 'job_id' [, 'job_id'] ...`実行します。詳細については、 [`ADMIN`ステートメント](/sql-statements/sql-statement-admin.md)参照してください。

### TiDB はセッションタイムアウトをサポートしていますか? {#does-tidb-support-session-timeout}

TiDB は現在、 [`wait_timeout`](/system-variables.md#wait_timeout)と[`interactive_timeout`](/system-variables.md#interactive_timeout) 2 つのタイムアウトをサポートしています。

### TiDB のバージョン管理戦略とは? {#what-is-the-tidb-version-management-strategy}

TiDB のバージョン管理の詳細については、 [TiDB のバージョン管理](/releases/versioning.md)を参照してください。

### TiDB クラスターをデプロイして維持するための運用コストはどうですか? {#how-about-the-operating-cost-of-deploying-and-maintaining-a-tidb-cluster}

TiDB は、低コストで簡単にクラスターを管理できるいくつかの機能と[ツール](/ecosystem-tool-user-guide.md)を提供します。

-   メンテナンス操作の場合、 [TiUP](/tiup/tiup-documentation-guide.md)パッケージ マネージャーとして機能し、デプロイ、スケーリング、アップグレード、およびその他のメンテナンス タスクを簡素化します。
-   モニタリングの場合、 [TiDB 監視フレームワーク](/tidb-monitoring-framework.md) [プロメテウス](https://prometheus.io/)使用してモニタリングおよびパフォーマンス メトリックを保存し、 [グラファナ](https://grafana.com/grafana/)を使用してこれらのメトリックを視覚化します。数百のメトリックを備えた数十の組み込みパネルが利用可能です。
-   トラブルシューティングのために、 [TiDB トラブルシューティング マップ](/tidb-troubleshooting-map.md) TiDBサーバーとその他のコンポーネントの一般的な問題をまとめます。このマップを使用して、関連する問題が発生したときに問題を診断して解決できます。

### さまざまな TiDB マスター バージョンの違いは何ですか? {#what-s-the-difference-between-various-tidb-master-versions}

TiDB コミュニティは非常に活発です。エンジニアは、機能の最適化とバグの修正を続けています。したがって、TiDB のバージョンは非常に高速に更新されます。最新バージョンの情報を入手したい場合は、 [TiDB リリースのタイムライン](/releases/release-timeline.md)を参照してください。

TiDB [TiUPの使用](/production-deployment-using-tiup.md)または[TiDB Operatorの使用](https://docs.pingcap.com/tidb-in-kubernetes/stable)をデプロイすることをお勧めします。 TiDB は、バージョン番号の管理が一元化されています。バージョン番号は、次のいずれかの方法で表示できます。

-   `select tidb_version()`
-   `tidb-server -V`

### TiDB 用のグラフィカルな展開ツールはありますか? {#is-there-a-graphical-deployment-tool-for-tidb}

現在No.

### TiDB クラスターをスケールアウトするには? {#how-to-scale-out-a-tidb-cluster}

オンライン サービスを中断することなく、TiDB クラスターをスケールアウトできます。

-   [TiUP](/production-deployment-using-tiup.md)を使用してクラスターをデプロイする場合は、 [TiUPを使用して TiDBクラスタをスケーリングする](/scale-tidb-using-tiup.md)を参照してください。
-   クラスターが[TiDB Operator](/tidb-operator-overview.md)使用して Kubernetes にデプロイされている場合は、 [Kubernetes で TiDB を手動でスケーリングする](https://docs.pingcap.com/tidb-in-kubernetes/stable/scale-a-tidb-cluster)を参照してください。

### TiDB を水平方向にスケーリングするには? {#how-to-scale-tidb-horizontally}

ビジネスが成長するにつれて、データベースは次の 3 つのボトルネックに直面する可能性があります。

-   ディスク容量が不足していることを意味するstorageリソースの不足。

-   CPU 占有率が高いなどのコンピューティング リソースの不足。

-   十分な書き込みおよび読み取り容量がありません。

ビジネスの成長に合わせて TiDB を拡張できます。

-   ディスク容量が足りない場合は、TiKV ノードを追加するだけで容量を増やすことができます。新しいノードが開始されると、PD はデータを他のノードから新しいノードに自動的に移行します。

-   コンピューティング リソースが十分でない場合は、TiDB ノードまたは TiKV ノードを追加する前に、まず CPU の消費状況を確認してください。 TiDB ノードが追加されると、ロード バランサーで構成できます。

-   容量が足りない場合は、TiDB ノードと TiKV ノードの両方を追加できます。

### Percolator が分散ロックを使用し、クラッシュしたクライアントがロックを保持している場合、ロックは解放されませんか? {#if-percolator-uses-distributed-locks-and-the-crash-client-keeps-the-lock-will-the-lock-not-be-released}

詳細については、中国語の[Percolator と TiDBトランザクションアルゴリズム](https://pingcap.com/blog-cn/percolator-and-txn/)を参照してください。

### TiDB が Thrift ではなく gRPC を使用するのはなぜですか? Googleが使用しているからですか？ {#why-does-tidb-use-grpc-instead-of-thrift-is-it-because-google-uses-it}

あまり。フロー制御、暗号化、ストリーミングなど、gRPC の優れた機能が必要です。

### <code>like(bindo.customers.name, jason%, 92)</code>の 92 は何を示していますか? {#what-does-the-92-indicate-in-code-like-bindo-customers-name-jason-92-code}

92 はエスケープ文字を示し、デフォルトでは ASCII 92 です。

### <code>information_schema.tables.data_length</code>で表示されるデータ長が、TiKV 監視パネルのストア サイズと異なるのはなぜですか? {#why-does-the-data-length-shown-by-code-information-schema-tables-data-length-code-differ-from-the-store-size-on-the-tikv-monitoring-panel}

2 つの理由:

-   2 つの結果は、異なる方法で計算されます。 `information_schema.tables.data_length`は、各行の平均の長さを計算することによる推定値ですが、TiKV 監視パネルのストア サイズは、1 つの TiKV インスタンス内のデータ ファイル (RocksDB の SST ファイル) の長さを合計したものです。
-   `information_schema.tables.data_length`は論理値で、ストア サイズは物理値です。複数のバージョンのトランザクションによって生成された冗長データは論理値には含まれませんが、物理値では冗長データが TiKV によって圧縮されます。

### トランザクションが非同期コミットまたは 1 フェーズ コミット機能を使用しないのはなぜですか? {#why-does-the-transaction-not-use-the-async-commit-or-the-one-phase-commit-feature}

次の状況では、システム変数を使用して[非同期コミット](/system-variables.md#tidb_enable_async_commit-new-in-v50)機能と[1 フェーズ コミット](/system-variables.md#tidb_enable_1pc-new-in-v50)機能を有効にしても、TiDB はこれらの機能を使用しません。

-   TiDB Binlogの実装によって制限されている TiDB Binlogを有効にしている場合、TiDB は非同期コミットまたは 1 フェーズ コミット機能を使用しません。
-   TiDB は、トランザクションに 256 を超えるキーと値のペアが書き込まれず、キーの合計サイズが 4 KB を超えない場合にのみ、非同期コミットまたは 1 フェーズ コミット機能を使用します。これは、大量のデータを書き込むトランザクションの場合、Async Commit を使用してもパフォーマンスが大幅に向上しないためです。

## PD管理 {#pd-management}

このセクションでは、PD の管理中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### PD にアクセスすると、「The <code>TiKV cluster is not bootstrapped</code>メッセージが表示される {#the-code-tikv-cluster-is-not-bootstrapped-code-message-is-displayed-when-i-access-pd}

PD のほとんどの API は、TiKV クラスターが初期化されている場合にのみ使用できます。 PD 起動時に PD にアクセスし、新規クラスタ配備時に TiKV を起動していない場合、このメッセージが表示されます。このメッセージが表示された場合は、TiKV クラスタを起動してください。 TiKV が初期化されると、PD がアクセス可能になります。

### PD の起動時に<code>etcd cluster ID mismatch</code>メッセージが表示される {#the-code-etcd-cluster-id-mismatch-code-message-is-displayed-when-starting-pd}

これは、PD 起動パラメーターの`--initial-cluster`に、このクラスターに属していないメンバーが含まれているためです。この問題を解決するには、各メンバーの対応するクラスターを確認し、間違ったメンバーを削除してから、PD を再起動します。

### PDの時刻同期誤差の最大許容値は? {#what-s-the-maximum-tolerance-for-time-synchronization-error-of-pd}

PD は同期エラーを許容できますが、エラー値が大きいほど、PD によって割り当てられたタイムスタンプと物理時間とのギャップが大きくなり、履歴バージョンの読み取りなどの関数に影響します。

### クライアント接続はどのように PD を見つけますか? {#how-does-the-client-connection-find-pd}

クライアント接続は、TiDB を介してのみクラスターにアクセスできます。 TiDB は PD と TiKV を接続します。 PD と TiKV は、クライアントに対して透過的です。 TiDB が任意の PD に接続すると、PD は現在のリーダーが誰であるかを TiDB に通知します。この PD がリーダーでない場合、TiDB はリーダー PD に再接続します。

### TiKV ストアの各ステータス (Up、Disconnect、Offline、Down、Tombstone) の関係は? {#what-is-the-relationship-between-each-status-up-disconnect-offline-down-tombstone-of-a-tikv-store}

各ステータスの関係については、 [TiKV店舗の各ステータスの関係](/tidb-scheduling.md#information-collection)を参照してください。

PD Control を使用して、TiKV ストアのステータス情報を確認できます。

### PD の<code>leader-schedule-limit</code>と<code>region-schedule-limit</code>スケジューリング パラメーターの違いは何ですか? {#what-is-the-difference-between-the-code-leader-schedule-limit-code-and-code-region-schedule-limit-code-scheduling-parameters-in-pd}

-   `leader-schedule-limit`スケジューリング パラメータは、異なる TiKV サーバーのLeader数のバランスをとるために使用され、クエリ処理の負荷に影響を与えます。
-   `region-schedule-limit`スケジューリング パラメータは、異なる TiKV サーバーのレプリカ数のバランスを取るために使用され、異なるノードのデータ量に影響を与えます。

### 各リージョンのレプリカの数は構成可能ですか?はいの場合、どのように構成しますか? {#is-the-number-of-replicas-in-each-region-configurable-if-yes-how-to-configure-it}

はい。現在、レプリカのグローバル数のみを更新できます。初めて起動すると、PD は構成ファイル (conf/pd.yml) を読み取り、その中で max-replicas 構成を使用します。後で番号を更新する場合は、 pd-ctl 構成コマンド`config set max-replicas $num`を使用し、 `config show all`使用して有効な構成を表示します。更新はアプリケーションに影響を与えず、バックグラウンドで構成されます。

TiKV インスタンスの総数が常に、設定したレプリカの数以上であることを確認してください。たとえば、3 つのレプリカには少なくとも 3 つの TiKV インスタンスが必要です。レプリカの数を増やす前に、追加のstorage要件を見積もる必要があります。 pd-ctl の詳細については、 [PD Controlユーザー ガイド](/pd-control.md)を参照してください。

### コマンド ライン クラスタ管理ツールがない場合に、クラスタ全体のヘルス ステータスを確認する方法を教えてください。 {#how-to-check-the-health-status-of-the-whole-cluster-when-lacking-command-line-cluster-management-tools}

pd-ctl ツールを使用して、クラスターの一般的なステータスを確認できます。詳細なクラスタ ステータスについては、モニタを使用して判断する必要があります。

### オフラインのクラスタ ノードの監視データを削除するにはどうすればよいですか? {#how-to-delete-the-monitoring-data-of-a-cluster-node-that-is-offline}

オフライン ノードは通常、TiKV ノードを示します。オフライン プロセスが終了したかどうかは、pd-ctl またはモニターによって判断できます。ノードがオフラインになったら、次の手順を実行します。

1.  オフライン ノードで関連するサービスを手動で停止します。
2.  Prometheus 設定ファイルから該当するノードの`node_exporter`データを削除します。

## TiDBサーバー管理 {#tidb-server-management}

このセクションでは、TiDBサーバーの管理中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### TiDB で<code>lease</code>パラメータを設定するには? {#how-to-set-the-code-lease-code-parameter-in-tidb}

リース パラメータ ( `--lease=60` ) は、TiDBサーバーの起動時にコマンド ラインから設定されます。リース パラメータの値は、現在のセッションのデータベース スキーマ変更 (DDL) 速度に影響を与えます。テスト環境では、値を 1 に設定して、テスト サイクルを高速化できます。ただし、本番環境では、DDL の安全性を確保するために、値を分 (60 など) に設定することをお勧めします。

### DDL操作の処理時間は? {#what-is-the-processing-time-of-a-ddl-operation}

処理時間はシナリオごとに異なります。一般に、次の 3 つのシナリオを考慮することができます。

1.  対応するデータ テーブルの行数が比較的少ない`Add Index`の操作: 約 3 秒
2.  `Add Index`対応するデータ テーブルの行数が比較的多い操作: 処理時間は特定の行数とその時の QPS によって異なります ( `Add Index`操作は通常の SQL 操作より優先度が低くなります)。
3.  その他の DDL 操作: 約 1 秒

DDL 要求を受け取る TiDBサーバーインスタンスが、DDL 所有者がいる TiDBサーバーインスタンスと同じである場合、上記の最初と 3 番目のシナリオでは、数十から数百ミリ秒しかかからない可能性があります。

### DDL ステートメントの実行が時々非常に遅いのはなぜですか? {#why-it-is-very-slow-to-run-ddl-statements-sometimes}

考えられる理由:

-   複数の DDL ステートメントを一緒に実行すると、最後のいくつかの DDL ステートメントの実行が遅くなる可能性があります。これは、DDL ステートメントが TiDB クラスターでシリアルに実行されるためです。
-   クラスターを正常に起動した後、最初の DDL 操作の実行に時間がかかる場合があります (通常は約 30 秒)。これは、TiDB クラスターが DDL ステートメントを処理するリーダーを選出しているためです。
-   TiDB を起動してから最初の 10 分間の DDL ステートメントの処理時間は、次の条件を満たしている場合、通常の場合よりも大幅に長くなります。 ); 2) TiDB が`kill -9`コマンドで停止されるため、TiDB は PD からの登録データのクリーンアップに間に合いません。この期間中に DDL ステートメントを実行すると、各 DDL の状態が変化するために、2 * リース (リース = 45 秒) 待つ必要があります。
-   クラスター内の TiDBサーバーと PDサーバーの間で通信の問題が発生した場合、TiDBサーバーはPDサーバーからバージョン情報を取得または更新することができません。この場合、各 DDL の状態処理のために 2 * リースを待つ必要があります。

### S3 を TiDB のバックエンドstorageエンジンとして使用できますか? {#can-i-use-s3-as-the-backend-storage-engine-in-tidb}

いいえ。現在、TiDB は分散storageエンジンと Goleveldb/RocksDB/BoltDB エンジンのみをサポートしています。

### <code>Information_schema</code>より現実的な情報をサポートできますか? {#can-the-code-information-schema-code-support-more-real-information}

MySQL との互換性の一部として、TiDB は多数の`INFORMATION_SCHEMA`テーブルをサポートしています。これらのテーブルの多くには、対応する SHOW コマンドもあります。詳細については、 [情報スキーマ](/information-schema/information-schema.md)を参照してください。

### TiDB Backoff タイプのシナリオの説明は? {#what-s-the-explanation-of-the-tidb-backoff-type-scenario}

TiDBサーバーとTiKVサーバー間の通信処理において、大量のデータを処理している場合、 `Server is busy`または`backoff.maxsleep 20000ms`ログメッセージが表示されます。これは、TiKVサーバーがデータを処理している間、システムがビジーであるためです。このとき、通常は TiKV ホストのリソース使用率が高いことがわかります。このような場合は、リソースの使用状況に応じてサーバーの容量を増やすことができます。

### TiDB TiClient タイプの主な理由は何ですか? {#what-is-the-main-reason-of-tidb-ticlient-type}

TiClientリージョンエラー インジケーターは、クライアントとしての TiDBサーバーがKV インターフェイスを介して TiKVサーバーにアクセスし、データ操作を実行するときに表示されるエラーの種類とメトリックを示します。エラーの種類には`not_leader`と`stale_epoch`があります。これらのエラーは、TiDBサーバーが独自のキャッシュ情報に従ってリージョンリーダー データを操作する場合、リージョンリーダーが移行された場合、または現在の TiKVリージョン情報と TiDB キャッシュのルーティング情報が一致しない場合に発生します。通常、この場合、TiDBサーバーはPD から最新のルーティング データを自動的に取得し、以前の操作をやり直します。

### TiDB がサポートする同時接続の最大数はいくつですか? {#what-s-the-maximum-number-of-concurrent-connections-that-tidb-supports}

デフォルトでは、TiDBサーバーごとの最大接続数に制限はありません。必要に応じて、 `config.toml`ファイルで`instance.max_connections`を設定するか、システム変数[`max_connections`](/system-variables.md#max_connections)の値を変更して、接続の最大数を制限できます。同時実行数が多すぎると応答時間が長くなる場合は、TiDB ノードを追加して容量を増やすことをお勧めします。

### テーブルの作成時間を表示するには? {#how-to-view-the-creation-time-of-a-table}

`information_schema`の表の`create_time`は作成時刻です。

### TiDB ログの<code>EXPENSIVE_QUERY</code>の意味は何ですか? {#what-is-the-meaning-of-code-expensive-query-code-in-the-tidb-log}

TiDB が SQL ステートメントを実行しているとき、各オペレーターが 10,000 行を処理すると推定される場合、クエリは`EXPENSIVE_QUERY`になります。 `tidb-server`設定パラメータを変更してしきい値を調整し、 `tidb-server`を再起動できます。

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

上記のステートメントを使用する場合、必要に応じてステートメントの次のフィールドに入力して置き換える必要があります。

-   `@dbname` : データベースの名前。
-   `@table_name` : ターゲット テーブルの名前。

さらに、上記のステートメントでは、次のようになります。

-   `store_size_amplification`クラスター圧縮率の平均を示します。 `SELECT * FROM METRICS_SCHEMA.store_size_amplification;`を使用してこの情報をクエリするだけでなく、 **Grafana Monitoring PD - statistics balance**パネルで各ノードの<strong>サイズ増幅</strong>メトリックを確認することもできます。クラスター圧縮率の平均は、すべてのノードのサイズ増幅の平均です。
-   `Approximate_Size`圧縮前のレプリカ内のテーブルのサイズを示します。これはおおよその値であり、正確な値ではないことに注意してください。
-   `Disk_Size`圧縮後のテーブルのサイズを示します。これは概算値であり、 `Approximate_Size`および`store_size_amplification`に従って計算できます。

## TiKVサーバー管理 {#tikv-server-management}

このセクションでは、TiKVサーバーの管理中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### コンプライアンスまたはマルチテナント アプリケーションのデータの場所を指定する方法は? {#how-to-specify-the-location-of-data-for-compliance-or-multi-tenant-applications}

[配置ルール](/placement-rules-in-sql.md)を使用して、コンプライアンスまたはマルチテナント アプリケーションのデータの場所を指定できます。

SQL の配置ルールは、レプリカの数、 Raftロール、配置場所、ルールが有効になるキー範囲など、連続するデータ範囲の属性を制御するように設計されています。

### TiKV クラスターで推奨されるレプリカの数はいくつですか?高可用性のために最小数を維持する方が良いですか? {#what-is-the-recommended-number-of-replicas-in-the-tikv-cluster-is-it-better-to-keep-the-minimum-number-for-high-availability}

テスト環境には、リージョンに 3 つのレプリカで十分です。ただし、本番シナリオでは 3 ノード未満の TiKV クラスターを操作しないでください。インフラストラクチャ、ワークロード、回復力のニーズによっては、この数を増やしたい場合があります。コピーが多いほどパフォーマンスは低下しますが、セキュリティは高くなります。

### TiKV の起動時に<code>cluster ID mismatch</code>メッセージが表示される {#the-code-cluster-id-mismatch-code-message-is-displayed-when-starting-tikv}

これは、ローカル TiKV に格納されているクラスター ID が、PD で指定されたクラスター ID と異なるためです。新しい PD クラスターがデプロイされると、PD はランダムなクラスター ID を生成します。 TiKV は PD からクラスター ID を取得し、初期化時にクラスター ID をローカルに保存します。次回 TiKV 起動時にローカルクラスタ ID と PD のクラスタ ID を照合します。クラスター ID が一致しない場合、 `cluster ID mismatch`メッセージが表示され、TiKV が終了します。

以前に PD クラスターをデプロイした後、PD データを削除して新しい PD クラスターをデプロイした場合、TiKV が古いデータを使用して新しい PD クラスターに接続するため、このエラーが発生します。

### TiKV起動時に<code>duplicated store address</code>メッセージが表示される {#the-code-duplicated-store-address-code-message-is-displayed-when-starting-tikv}

これは、起動パラメーターのアドレスが他の TiKV によって PD クラスターに登録されているためです。このエラーが発生する一般的な条件: TiKV で指定されたパスにデータ フォルダーがない`--data-dir` (削除または移動後に更新 --data-dir がない)、以前のパラメーターで TiKV を再起動します。pd-ctl の[ストア削除](https://github.com/pingcap/pd/tree/55db505e8f35e8ab4e00efd202beb27a8ecc40fb/tools/pd-ctl#store-delete--label--weight-store_id----jqquery-string)機能を試してください。以前のストアを削除してから、TiKV を再起動してください。

### TiKV プライマリ ノードとセカンダリ ノードは同じ圧縮アルゴリズムを使用していますが、結果が異なるのはなぜですか? {#tikv-primary-node-and-secondary-node-use-the-same-compression-algorithm-why-the-results-are-different}

現在、TiKV プライマリ ノードの一部のファイルは圧縮率が高く、これは基盤となるデータの分散と RocksDB の実装によって異なります。データサイズが時々変動するのは正常です。基盤となるstorageエンジンは、必要に応じてデータを調整します。

### TiKVブロックキャッシュの特徴は？ {#what-are-the-features-of-tikv-block-cache}

TiKV は、RocksDB のカラムファミリー (CF) 機能を実装します。デフォルトでは、KV データは最終的に RocksDB 内の 3 つの CF (デフォルト、書き込み、およびロック) に格納されます。

-   デフォルトの CF は実データを格納し、対応するパラメーターは`[rocksdb.defaultcf]`です。
-   書き込み CF は、データ バージョン情報 (MVCC) とインデックス関連のデータを格納し、対応するパラメーターは`[rocksdb.writecf]`です。
-   ロック CF はロック情報を保管し、システムはデフォルトのパラメーターを使用します。
-   Raft RocksDB インスタンスはRaftログを保存します。デフォルトの CF は主にRaftログを格納し、対応するパラメーターは`[raftdb.defaultcf]`です。
-   すべての CF には、データ ブロックをキャッシュし、RocksDB の読み取り速度を向上させるための共有ブロック キャッシュがあります。ブロック キャッシュのサイズは、 `block-cache-size`パラメータによって制御されます。パラメータの値が大きいほど、キャッシュできるホット データが多くなり、読み取り操作に適していることを意味します。同時に、より多くのシステムメモリを消費します。
-   各 CF には個別の書き込みバッファーがあり、サイズは`write-buffer-size`パラメーターによって制御されます。

### TiKV チャンネルがいっぱいなのはなぜですか? {#why-is-the-tikv-channel-full}

-   Raftstoreスレッドが遅すぎるか、I/O によってブロックされています。 Raftstoreの CPU 使用状況を表示できます。
-   TiKV はビジー状態 (CPU やディスク I/O など) であり、処理できません。

### TiKV がリージョンリーダーを頻繁に切り替えるのはなぜですか? {#why-does-tikv-frequently-switch-region-leader}

-   ネットワークの問題により、ノード間で通信が停止します。レポート障害監視を確認できます。
-   元のメインLeaderのノードがスタックしているため、時間内にFollowerに到達できません。
-   Raftstoreスレッドがスタックしました。

### ノードがダウンした場合、サービスは影響を受けますか?はいの場合、どのくらいの期間ですか？ {#if-a-node-is-down-will-the-service-be-affected-if-yes-how-long}

TiKV はRaftを使用して、複数のレプリカ間でデータを複製します (デフォルトでは、リージョンごとに 3 つのレプリカ)。 1 つのレプリカに問題が発生した場合、他のレプリカがデータの安全性を保証できます。 Raftプロトコルに基づいて、ノードがダウンしたときに 1 つのリーダーに障害が発生した場合、別のノードのフォロワーが、最大 2 * リース時間 (リース時間は 10 秒) 後にすぐにリージョンリーダーとして選出されます。

### 高い I/O、メモリ、CPU を使用し、パラメータ構成を超える TiKV シナリオは何ですか? {#what-are-the-tikv-scenarios-that-take-up-high-i-o-memory-cpu-and-exceed-the-parameter-configuration}

TiKV で大量のデータを読み書きすると、I/O、メモリ、および CPU が大量に消費されます。大規模な中間結果セットを生成するシナリオなど、非常に複雑なクエリを実行すると、大量のメモリと CPU リソースが消費されます。

### TiKV は SAS/SATA ディスクまたは SSD/SAS ディスクの混合展開をサポートしていますか? {#does-tikv-support-sas-sata-disks-or-mixed-deployment-of-ssd-sas-disks}

いいえ。OLTP シナリオの場合、TiDB はデータ アクセスと操作のために高 I/O ディスクを必要とします。強力な整合性を備えた分散データベースとして、TiDB にはレプリカの複製や最レイヤーのstorageの圧縮など、いくつかの書き込み増幅機能があります。したがって、TiDB のベスト プラクティスでは、storageディスクとして NVMe SSD を使用することをお勧めします。 TiKV と PD の混合展開はサポートされていません。

### KeyデータテーブルのRangeはデータアクセス前に分割されていますか? {#is-the-range-of-the-key-data-table-divided-before-data-access}

いいえ。MySQL のテーブル分割ルールとは異なります。 TiKV では、テーブル Range はリージョンのサイズに基づいて動的に分割されます。

### リージョンはどのように分割されますか? {#how-does-region-split}

リージョンは事前に分割されていませんが、リージョン分割メカニズムに従います。リージョンサイズが`region-max-size`または`region-max-keys`パラメータの値を超えると、分割がトリガーされます。分割後、その情報はPDに報告されます。

### TiKV には、データのセキュリティを保証するために、MySQL のような<code>innodb_flush_log_trx_commit</code>パラメータがありますか? {#does-tikv-have-the-code-innodb-flush-log-trx-commit-code-parameter-like-mysql-to-guarantee-the-security-of-data}

はい。現在、スタンドアロンstorageエンジンは 2 つの RocksDB インスタンスを使用しています。 raft-log を保存するために 1 つのインスタンスが使用されます。 TiKV の`sync-log`パラメータが true に設定されている場合、各コミットは強制的に raft-log にフラッシュされます。クラッシュが発生した場合、raft-log を使用して KV データを復元できます。

### SSD、RAID レベル、RAID カードのキャッシュ戦略、NUMA 構成、ファイル システム、オペレーティング システムの I/O スケジューリング戦略など、WALstorageの推奨サーバー構成は何ですか? {#what-is-the-recommended-server-configuration-for-wal-storage-such-as-ssd-raid-level-cache-strategy-of-raid-card-numa-configuration-file-system-i-o-scheduling-strategy-of-the-operating-system}

WAL は順序付けられた書き込みに属し、現在、独自の構成を適用していません。推奨構成は次のとおりです。

-   SSD
-   RAID 10 推奨
-   RAID カードのキャッシュ戦略とオペレーティング システムの I/O スケジューリング戦略: 現在、具体的なベスト プラクティスはありません。 Linux 7 以降ではデフォルト構成を使用できます
-   NUMA: 具体的な提案はありません。メモリ割り当て戦略の場合、 `interleave = all`を使用できます
-   ファイルシステム: ext4

### 最も厳密なデータ利用可能モード ( <code>sync-log = true</code> ) での書き込みパフォーマンスはどうですか? {#how-is-the-write-performance-in-the-most-strict-data-available-mode-code-sync-log-true-code}

通常、 `sync-log`を有効にすると、パフォーマンスが約 30% 低下します。 `sync-log`を`false`に設定した場合の書き込み性能については、 [Sysbenchを使ったTiDBの性能テスト結果](/benchmark/v3.0-performance-benchmarking-with-sysbench.md)参照してください。

### Raft + TiKVアーキテクチャの複数のレプリカは絶対的なデータの安全性を達成できますか?最も厳格なモード ( <code>sync-log = true</code> ) をスタンドアロンstorageに適用する必要はありますか? {#can-raft-multiple-replicas-in-the-tikv-architecture-achieve-absolute-data-safety-is-it-necessary-to-apply-the-most-strict-mode-code-sync-log-true-code-to-a-standalone-storage}

ノード障害が発生した場合の回復可能性を確保するために、データは[Raftコンセンサスアルゴリズム](https://raft.github.io/)を使用して TiKV ノード間で冗長的に複製されます。データがレプリカの 50% 以上に書き込まれた場合にのみ、アプリケーションは ACK を返します (3 つのノードのうち 2 つ)。ただし、理論的には、2 つのノードがクラッシュする可能性があります。したがって、データの安全性に関する要件はそれほど厳しくなく、パフォーマンスに関する要件が非常に厳しいシナリオを除き、 `sync-log`モードを有効にすることを強くお勧めします。

`sync-log`を使用する代わりに、 Raftグループに 3 つではなく 5 つのレプリカを持つことを検討することもできます。これにより、データの安全性を維持しながら、2 つのレプリカの障害が許容されます。

スタンドアロンの TiKV ノードの場合でも、 `sync-log`モードを有効にすることをお勧めします。そうしないと、ノード障害が発生した場合に最後の書き込みが失われる可能性があります。

### TiKV はRaftプロトコルを使用するため、データの書き込み中に複数のネットワーク ラウンドトリップが発生します。実際の書き込み遅延は? {#since-tikv-uses-the-raft-protocol-multiple-network-roundtrips-occur-during-data-writing-what-is-the-actual-write-delay}

理論的には、TiDB の書き込み遅延は、スタンドアロン データベースよりもネットワーク ラウンドトリップが 4 回多くなります。

### TiDB には、KV インターフェイスを直接使用でき、独立したキャッシュを必要としない MySQL のような InnoDB memcached プラグインがありますか? {#does-tidb-have-an-innodb-memcached-plugin-like-mysql-which-can-directly-use-the-kv-interface-and-does-not-need-the-independent-cache}

TiKV は、インターフェースの個別呼び出しをサポートしています。理論的には、インスタンスをキャッシュとして使用できます。 TiDB は分散リレーショナル データベースであるため、TiKV を個別にサポートしていません。

### コプロセッサーコンポーネントは何に使用されますか? {#what-is-the-coprocessor-component-used-for}

-   TiDB と TiKV 間のデータ転送を減らす
-   TiKV の分散コンピューティング リソースを最大限に活用して、コンピューティング プッシュダウンを実行します。

### エラー メッセージ<code>IO error: No space left on device While appending to file</code>が表示されます {#the-error-message-code-io-error-no-space-left-on-device-while-appending-to-file-code-is-displayed}

これは、ディスク容量が不足しているためです。ノードを追加するか、ディスク容量を拡大する必要があります。

### TiKVでOOM(Out of Memory)エラーが多発するのはなぜですか? {#why-does-the-oom-out-of-memory-error-occur-frequently-in-tikv}

TiKV のメモリ使用量は主に RocksDB のブロック キャッシュによるもので、デフォルトではシステムメモリサイズの 40% です。 TiKV で OOM エラーが多発する場合は、 `block-cache-size`の値を大きくしすぎていないか確認してください。さらに、複数の TiKV インスタンスが 1 台のマシンにデプロイされている場合は、複数のインスタンスがシステムメモリを使いすぎて OOM エラーが発生しないように、パラメーターを明示的に構成する必要があります。

### TiDB データと RawKV データの両方を同じ TiKV クラスターに保存できますか? {#can-both-tidb-data-and-rawkv-data-be-stored-in-the-same-tikv-cluster}

いいえ。TiDB (またはトランザクション API から作成されたデータ) は、特定のキー形式に依存しています。 RawKV API から作成されたデータ (または他の RawKV ベースのサービスからのデータ) とは互換性がありません。

## TiDB テスト {#tidb-testing}

このセクションでは、TiDB のテスト中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### Sysbenchを使ったTiDBの性能テスト結果は？ {#what-is-the-performance-test-result-for-tidb-using-sysbench}

多くのユーザーは、最初はベンチマーク テストや、TiDB と MySQL の比較テストを行う傾向にあります。同様の公式テストも実施しており、テスト データには多少の偏りがありますが、テスト結果は全体として一貫していることがわかりました。 TiDB のアーキテクチャはMySQL とは大きく異なるため、ベンチマーク ポイントを見つけるのは困難です。提案は次のとおりです。

-   ベンチマーク テストに時間をかけすぎないでください。 TiDB を使用するシナリオの違いに注意してください。
-   [Sysbenchを使ったTiDBの性能テスト結果](/benchmark/v3.0-performance-benchmarking-with-sysbench.md)を参照してください。

### TiDB クラスター容量 (QPS) とノード数の関係は? TiDB は MySQL と比べてどうですか? {#what-s-the-relationship-between-the-tidb-cluster-capacity-qps-and-the-number-of-nodes-how-does-tidb-compare-to-mysql}

-   10 ノード以内では、TiDB 書き込み容量 (Insert TPS) とノード数の関係は約 40% 直線的に増加します。 MySQL は単一ノードの書き込みを使用するため、その書き込み容量はスケーリングできません。
-   MySQL では、セカンダリ データベースを追加することで読み取り容量を増やすことができますが、書き込み容量はシャーディングを使用しない限り増やすことができず、多くの問題があります。
-   TiDB では、ノードを追加することで、読み取り容量と書き込み容量の両方を簡単に増やすことができます。

### DBA による MySQL と TiDB のパフォーマンス テストでは、スタンドアロンの TiDB のパフォーマンスは MySQL ほど良くないことが示されています。 {#the-performance-test-of-mysql-and-tidb-by-our-dba-shows-that-the-performance-of-a-standalone-tidb-is-not-as-good-as-mysql}

TiDB は、MySQL スタンドアロンの容量が限られているためにシャーディングが使用され、強力な整合性と完全な分散トランザクションが必要なシナリオ向けに設計されています。 TiDB の利点の 1 つは、コンピューティングをstorageノードにプッシュダウンして、コンカレント コンピューティングを実行できることです。

TiDB は、小さなサイズのテーブル (1,000 万レベル以下など) には適していません。これは、データのサイズが小さく、リージョンが限られていると、並行性の強さが発揮されないためです。典型的な例はカウンターテーブルで、数行のレコードが高頻度で更新されます。 TiDB では、これらの行はstorageエンジンでいくつかのキーと値のペアになり、単一のノードにあるリージョンに落ち着きます。 TiDB から TiKV への強力な整合性と操作を保証するためのバックグラウンド レプリケーションのオーバーヘッドは、MySQL スタンドアロンよりもパフォーマンスの低下につながります。

## バックアップと復元 {#backup-and-restoration}

このセクションでは、バックアップおよび復元中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### TiDB でデータをバックアップするには? {#how-to-back-up-data-in-tidb}

現在、大量のデータ (1 TB を超える) のバックアップの場合、推奨される方法は[バックアップと復元 (BR)](/br/backup-and-restore-overview.md)を使用することです。それ以外の場合、推奨されるツールは[Dumpling](/dumpling-overview.md)です。公式の MySQL ツール`mysqldump`も TiDB でデータのバックアップと復元のためにサポートされていますが、そのパフォーマンスはBRに劣らず、大量のデータのバックアップと復元にはさらに多くの時間を必要とします。

BRに関するその他の FAQ については、 [BRのよくある質問](/faq/backup-and-restore-faq.md)を参照してください。

### バックアップと復元の速度はどうですか? {#how-is-the-speed-of-backup-and-restore}

[BR](/br/backup-and-restore-overview.md)を使用してバックアップおよび復元タスクを実行すると、バックアップは TiKV インスタンスあたり約 40 MB/秒で処理され、復元は TiKV インスタンスあたり約 100 MB/秒で処理されます。
