---
title: TiDB Cluster Management FAQs
summary: TiDB クラスター管理に関連する FAQ について説明します。
---

# TiDBクラスタ管理に関する FAQ {#tidb-cluster-management-faqs}

このドキュメントでは、TiDB クラスタ管理に関連する FAQ をまとめています。

## 日常管理 {#daily-management}

このセクションでは、日常的なクラスター管理中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### TiDBにログインするにはどうすればいいですか? {#how-to-log-into-tidb}

MySQL にログインするのと同じように、TiDB にログインできます。例:

```bash
mysql -h 127.0.0.1 -uroot -P4000
```

### TiDB のシステム変数を変更するにはどうすればよいですか? {#how-to-modify-the-system-variables-in-tidb}

MySQL と同様に、TiDB には静的パラメータとソリッドパラメータが含まれています。 `SET GLOBAL xxx = n`使用して静的パラメータを直接変更できますが、この場合、パラメータの新しい値はライフサイクル内でのみ有効です。

### TiDB (TiKV) のデータ ディレクトリはどこにあり、何ですか? {#where-and-what-are-the-data-directories-in-tidb-tikv}

TiKV データは[`--data-dir`](/command-line-flags-for-tikv-configuration.md#--data-dir)にあり、その中にはそれぞれバックアップ、データ、 Raftデータ、ミラー データを保存するために使用される、backup、db、raft、snap の 4 つのディレクトリが含まれています。

### TiDB のシステム テーブルとは何ですか? {#what-are-the-system-tables-in-tidb}

MySQL と同様に、TiDB にもシステム テーブルが含まれており、サーバーの実行時に必要な情報を保存するために使用されます。1 [TiDB システム テーブル](/mysql-schema.md)参照してください。

### TiDB/PD/TiKV ログはどこにありますか? {#where-are-the-tidb-pd-tikv-logs}

TiDB/PD/TiKV は、デフォルトではログに標準エラーを出力します。起動時にログファイルを`--log-file`で指定すると、指定されたファイルにログが出力され、毎日ローテーションが実行されます。

### TiDB を安全に停止するにはどうすればよいですか? {#how-to-safely-stop-tidb}

-   ロード バランサが実行中の場合 (推奨): ロード バランサを停止し、SQL ステートメント`SHUTDOWN`を実行します。その後、TiDB は[`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-new-in-v50)で指定された期間、すべてのセッションが終了するまで待機します。その後、TiDB は実行を停止します。

-   ロード バランサーが実行されていない場合: `SHUTDOWN`ステートメントを実行します。その後、TiDB コンポーネントは正常に停止されます。

### TiDB で<code>kill</code>を実行できますか? {#can-code-kill-code-be-executed-in-tidb}

-   DML ステートメントを強制終了します。

    まず`information_schema.cluster_processlist`使用して TiDB インスタンス アドレスとセッション ID を見つけ、次に kill コマンドを実行します。

    TiDB v6.1.0 では、Global Kill 機能が導入されています ( `enable-global-kill`構成によって制御され、デフォルトで有効になっています)。Global Kill が有効になっている場合は、 `kill session_id`実行するだけです。

    TiDB バージョンが v6.1.0 より前の場合、または Global Kill 機能が有効になっていない場合、 `kill session_id`デフォルトでは有効になりません。DML ステートメントを終了するには、DML ステートメントを実行している TiDB インスタンスにクライアントを直接接続してから、 `kill tidb session_id`ステートメントを実行する必要があります。クライアントが別の TiDB インスタンスに接続している場合、またはクライアントと TiDB クラスターの間にプロキシがある場合、 `kill tidb session_id`ステートメントが別の TiDB インスタンスにルーティングされ、別のセッションが誤って終了する可能性があります。詳細については、 [`KILL`](/sql-statements/sql-statement-kill.md)を参照してください。

-   DDL ステートメントを強制終了します。まず`admin show ddl jobs`使用して、終了する必要がある DDL ジョブの ID を見つけ、次に`admin cancel ddl jobs 'job_id' [, 'job_id'] ...`を実行します。詳細については、 [`ADMIN`ステートメント](/sql-statements/sql-statement-admin.md)を参照してください。

### TiDB はセッション タイムアウトをサポートしていますか? {#does-tidb-support-session-timeout}

TiDB は現在、 [`wait_timeout`](/system-variables.md#wait_timeout)と[`interactive_timeout`](/system-variables.md#interactive_timeout) 2 つのタイムアウトをサポートしています。

### TiDB バージョン管理戦略とは何ですか? {#what-is-the-tidb-version-management-strategy}

TiDBのバージョン管理の詳細については、 [TiDB のバージョン管理](/releases/versioning.md)参照してください。

### TiDB クラスターの導入と保守にかかる運用コストはどのくらいでしょうか? {#how-about-the-operating-cost-of-deploying-and-maintaining-a-tidb-cluster}

TiDB は、低コストで簡単にクラスターを管理できるいくつかの機能と[ツール](/ecosystem-tool-user-guide.md)提供します。

-   メンテナンス操作の場合、 [TiUP](/tiup/tiup-documentation-guide.md)パッケージ マネージャーとして機能し、展開、スケーリング、アップグレード、およびその他のメンテナンス タスクを簡素化します。
-   監視の場合、 [TiDB 監視フレームワーク](/tidb-monitoring-framework.md) [プロメテウス](https://prometheus.io/)を使用して監視およびパフォーマンス メトリックを保存し、 [グラファナ](https://grafana.com/grafana/)を使用してこれらのメトリックを視覚化します。数百のメトリックを備えた数十の組み込みパネルが利用可能です。
-   トラブルシューティングのために、 [TiDB トラブルシューティング マップ](/tidb-troubleshooting-map.md) TiDBサーバーとその他のコンポーネントの一般的な問題をまとめています。関連する問題が発生した場合、このマップを使用して問題を診断し、解決することができます。

### さまざまな TiDB マスター バージョンの違いは何ですか? {#what-s-the-difference-between-various-tidb-master-versions}

TiDB コミュニティは非常に活発です。エンジニアは機能の最適化とバグの修正を続けています。そのため、TiDB バージョンは非常に速く更新されます。最新バージョンの情報を常に把握したい場合は、 [TiDB リリース タイムライン](/releases/release-timeline.md)を参照してください。

TiDB [TiUPを使用する](/production-deployment-using-tiup.md)または[TiDB Operatorの使用](https://docs.pingcap.com/tidb-in-kubernetes/stable)を導入することをお勧めします。TiDB ではバージョン番号が一元管理されています。次のいずれかの方法でバージョン番号を表示できます。

-   `select tidb_version()`
-   `tidb-server -V`

### TiDB 用のグラフィカル デプロイメント ツールはありますか? {#is-there-a-graphical-deployment-tool-for-tidb}

現在はいいえ。

### TiDB クラスターをスケールアウトするにはどうすればよいですか? {#how-to-scale-out-a-tidb-cluster}

オンライン サービスを中断することなく、TiDB クラスターをスケールアウトできます。

-   クラスターが[TiUP](/production-deployment-using-tiup.md)使用してデプロイされている場合は、 [TiUPを使用して TiDBクラスタをスケールする](/scale-tidb-using-tiup.md)を参照してください。
-   クラスターが Kubernetes 上で[TiDB Operator](/tidb-operator-overview.md)使用してデプロイされている場合は、 [Kubernetes で TiDB を手動でスケールする](https://docs.pingcap.com/tidb-in-kubernetes/stable/scale-a-tidb-cluster)を参照してください。

### TiDB を水平方向にスケーリングするにはどうすればよいですか? {#how-to-scale-tidb-horizontally}

ビジネスが成長するにつれて、データベースは次の 3 つのボトルネックに直面する可能性があります。

-   ストレージ リソースが不足しているため、storage領域が十分ではありません。

-   CPU 占有率が高いなどのコンピューティング リソースの不足。

-   書き込みおよび読み取り容量が不十分です。

ビジネスの成長に合わせて TiDB を拡張できます。

-   ディスク容量が足りない場合は、TiKV ノードを追加するだけで容量を増やすことができます。新しいノードが起動すると、PD は他のノードから新しいノードにデータを自動的に移行します。

-   コンピューティング リソースが十分でない場合は、TiDB ノードまたは TiKV ノードを追加する前に、まず CPU の消費状況を確認してください。TiDB ノードを追加する場合は、ロード バランサーで設定できます。

-   容量が足りない場合は、TiDB ノードと TiKV ノードの両方を追加できます。

### Percolator が分散ロックを使用し、クラッシュ クライアントがロックを保持する場合、ロックは解放されませんか? {#if-percolator-uses-distributed-locks-and-the-crash-client-keeps-the-lock-will-the-lock-not-be-released}

詳細は中国語版[パーコレータと TiDBトランザクションアルゴリズム](https://pingcap.com/blog-cn/percolator-and-txn/)ご覧ください。

### TiDB が Thrift ではなく gRPC を使用するのはなぜですか? Google が使用しているからでしょうか? {#why-does-tidb-use-grpc-instead-of-thrift-is-it-because-google-uses-it}

そうではありません。フロー制御、暗号化、ストリーミングなど、gRPC の優れた機能が必要です。

### <code>like(bindo.customers.name, jason%, 92)</code>の 92 は何を示していますか? {#what-does-the-92-indicate-in-code-like-bindo-customers-name-jason-92-code}

92 はエスケープ文字を示し、デフォルトでは ASCII 92 です。

### <code>information_schema.tables.data_length</code>で表示されるデータ長が TiKV 監視パネルのストア サイズと異なるのはなぜですか? {#why-does-the-data-length-shown-by-code-information-schema-tables-data-length-code-differ-from-the-store-size-on-the-tikv-monitoring-panel}

理由は2つあります。

-   2 つの結果は異なる方法で計算されます。1 `information_schema.tables.data_length`各行の平均長を計算して推定した値ですが、TiKV 監視パネルのストア サイズは、単一の TiKV インスタンス内のデータ ファイル (RocksDB の SST ファイル) の長さを合計したものです。
-   `information_schema.tables.data_length`は論理値ですが、ストア サイズは物理値です。トランザクションの複数のバージョンによって生成された冗長データは論理値には含まれませんが、冗長データは物理値で TiKV によって圧縮されます。

### トランザクションが非同期コミットまたは 1 フェーズ コミット機能を使用しないのはなぜですか? {#why-does-the-transaction-not-use-the-async-commit-or-the-one-phase-commit-feature}

次の状況では、システム変数を使用して機能[非同期コミット](/system-variables.md#tidb_enable_async_commit-new-in-v50)と機能[1フェーズコミット](/system-variables.md#tidb_enable_1pc-new-in-v50)を有効にしても、TiDB はこれらの機能を使用しません。

-   TiDB Binlogを有効にしている場合、TiDB Binlogの実装によって制限され、TiDB は非同期コミットまたは 1 フェーズ コミット機能を使用しません。
-   TiDB は、トランザクションで書き込まれるキーと値のペアが 256 個以下で、キーの合計サイズが 4 KB 以下の場合にのみ、非同期コミットまたは 1 フェーズ コミット機能を使用します。これは、書き込むデータ量が多いトランザクションの場合、非同期コミットを使用してもパフォーマンスが大幅に向上しないためです。

## PD管理 {#pd-management}

このセクションでは、PD 管理中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### PDにアクセスすると、 <code>TiKV cluster is not bootstrapped</code>メッセージが表示されます {#the-code-tikv-cluster-is-not-bootstrapped-code-message-is-displayed-when-i-access-pd}

PD の API のほとんどは、TiKV クラスターが初期化されている場合にのみ使用できます。新しいクラスターがデプロイされたときに TiKV が起動されていない状態で PD が起動されているときに PD にアクセスすると、このメッセージが表示されます。このメッセージが表示された場合は、TiKV クラスターを起動してください。TiKV が初期化されると、PD にアクセスできるようになります。

### PD を起動すると、 <code>etcd cluster ID mismatch</code>メッセージが表示されます。 {#the-code-etcd-cluster-id-mismatch-code-message-is-displayed-when-starting-pd}

これは、PD 起動パラメータの`--initial-cluster`に、このクラスターに属していないメンバーが含まれているためです。この問題を解決するには、各メンバーの対応するクラスターを確認し、間違ったメンバーを削除してから、PD を再起動します。

### PD の保存時の暗号化を有効にすると<code>[PD:encryption:ErrEncryptionNewMasterKey]fail to get encryption key from file /root/path/file%!(EXTRA string=open /root/path/file: permission denied)</code>メッセージが表示されます。 {#the-code-pd-encryption-errencryptionnewmasterkey-fail-to-get-encryption-key-from-file-root-path-file-extra-string-open-root-path-file-permission-denied-code-message-is-displayed-when-enabling-encryption-at-rest-for-pd}

保存時の暗号化では、キー ファイルを`root`ディレクトリまたはそのサブディレクトリに保存することはできません。読み取り権限を付与しても、同じエラーが発生します。この問題を解決するには、キー ファイルを`root`ディレクトリ以外の場所に保存します。

### PD の時間同期エラーの最大許容範囲はどれくらいですか? {#what-s-the-maximum-tolerance-for-time-synchronization-error-of-pd}

PD はあらゆる同期エラーを許容できますが、エラー値が大きいほど、PD によって割り当てられたタイムスタンプと物理時間の間のギャップが大きくなり、履歴バージョンの読み取りなどの関数に影響します。

### クライアント接続はどのようにして PD を見つけるのでしょうか? {#how-does-the-client-connection-find-pd}

クライアント接続は TiDB を介してのみクラスターにアクセスできます。TiDB は PD と TiKV を接続します。PD と TiKV はクライアントに対して透過的です。TiDB がいずれかの PD に接続すると、PD は現在のリーダーが誰であるかを TiDB に伝えます。この PD がリーダーでない場合、TiDB はリーダー PD に再接続します。

### TiKV ストアの各ステータス (Up、Disconnect、Offline、Down、Tombstone) の関係は何ですか? {#what-is-the-relationship-between-each-status-up-disconnect-offline-down-tombstone-of-a-tikv-store}

各ステータスの関係については[TiKVストアの各ステータスの関係](/tidb-scheduling.md#information-collection)を参照してください。

PD Controlを使用して、TiKV ストアのステータス情報を確認できます。

### PD の<code>leader-schedule-limit</code>と<code>region-schedule-limit</code>スケジューリング パラメータの違いは何ですか? {#what-is-the-difference-between-the-code-leader-schedule-limit-code-and-code-region-schedule-limit-code-scheduling-parameters-in-pd}

-   `leader-schedule-limit`スケジューリング パラメータは、異なる TiKV サーバーのLeader数のバランスをとるために使用され、クエリ処理の負荷に影響します。
-   `region-schedule-limit`スケジューリング パラメータは、異なる TiKV サーバーのレプリカ数のバランスをとるために使用され、異なるノードのデータ量に影響します。

### 各リージョンのレプリカの数は設定可能ですか? 設定可能な場合、どのように設定しますか? {#is-the-number-of-replicas-in-each-region-configurable-if-yes-how-to-configure-it}

はい。現在、レプリカのグローバル数のみを更新できます。初めて起動すると、PD は構成ファイル (conf/pd.yml) を読み取り、その中の max-replicas 構成を使用します。後で数を更新する場合は、pd-ctl 構成コマンド`config set max-replicas $num`を使用し、 `config show all`使用して有効な構成を表示します。更新はアプリケーションに影響せず、バックグラウンドで構成されます。

TiKV インスタンスの合計数が、設定したレプリカの数以上であることを確認してください。たとえば、レプリカが 3 つある場合は、少なくとも 3 つの TiKV インスタンスが必要です。レプリカの数を増やす前に、追加のstorage要件を見積もる必要があります。pd-ctl の詳細については、 [PD Controlユーザー ガイド](/pd-control.md)を参照してください。

### コマンドラインのクラスター管理ツールがない場合に、クラスター全体のヘルス状態を確認するにはどうすればよいでしょうか? {#how-to-check-the-health-status-of-the-whole-cluster-when-lacking-command-line-cluster-management-tools}

pd-ctl ツールを使用して、クラスターの一般的なステータスを確認できます。詳細なクラスター ステータスを確認するには、モニターを使用して確認する必要があります。

### オフラインのクラスター ノードの監視データを削除するにはどうすればよいですか? {#how-to-delete-the-monitoring-data-of-a-cluster-node-that-is-offline}

オフライン ノードは通常、TiKV ノードを示します。オフライン プロセスが終了したかどうかは、pd-ctl またはモニターによって判断できます。ノードがオフラインになったら、次の手順を実行します。

1.  オフライン ノード上の関連サービスを手動で停止します。
2.  Prometheus 構成ファイルから対応するノードの`node_exporter`データを削除します。

## TiDBサーバー管理 {#tidb-server-management}

このセクションでは、TiDBサーバーの管理中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### TiDB で<code>lease</code>パラメータを設定するにはどうすればよいでしょうか? {#how-to-set-the-code-lease-code-parameter-in-tidb}

リースパラメータ（ `--lease=60` ）は、TiDBサーバーの起動時にコマンドラインから設定されます。リースパラメータの値は、現在のセッションのデータベーススキーマ変更（DDL）速度に影響します。テスト環境では、値を 1 秒に設定してテストサイクルを高速化できます。ただし、本番環境では、DDL の安全性を確保するために、値を分（たとえば 60）に設定することをお勧めします。

### DDL 操作の処理時間はどれくらいですか? {#what-is-the-processing-time-of-a-ddl-operation}

処理時間はシナリオによって異なります。一般的には、次の 3 つのシナリオが考えられます。

1.  対応するデータテーブル内の行数が比較的少ない`Add Index`の操作: 約3秒
2.  対応するデータ テーブル内の行数が比較的多い`Add Index`操作: 処理時間は、特定の行数とその時点の QPS によって異なります ( `Add Index`操作は通常の SQL 操作よりも優先度が低くなります)
3.  その他のDDL操作: 約1秒

DDL 要求を受信する TiDBサーバーインスタンスが、DDL 所有者が存在する TiDBサーバーインスタンスと同じである場合、上記の最初のシナリオと 3 番目のシナリオにかかる時間は、数十から数百ミリ秒に過ぎない可能性があります。

### DDL ステートメントの実行が非常に遅くなるのはなぜですか? {#why-it-is-very-slow-to-run-ddl-statements-sometimes}

考えられる理由:

-   複数の DDL ステートメントを同時に実行すると、最後のいくつかの DDL ステートメントの実行速度が遅くなる可能性があります。これは、DDL ステートメントが TiDB クラスター内で順番に実行されるためです。
-   クラスターを正常に起動した後、最初の DDL 操作の実行に通常 30 秒ほどかかることがあります。これは、TiDB クラスターが DDL ステートメントを処理するリーダーを選出しているためです。
-   以下の条件に該当する場合、TiDB 起動後の最初の 10 分間の DDL ステートメントの処理時間は通常の場合よりも大幅に長くなります。1) TiDB を停止しているとき (停電の場合を含む)、TiDB は通常どおり PD と通信できません。2) TiDB は`kill -9`コマンドによって停止されるため、PD から登録データを時間内にクリーンアップできません。この期間中に DDL ステートメントを実行すると、各 DDL の状態変更のために、2 * リース (リース = 45 秒) 待機する必要があります。
-   クラスター内の TiDBサーバーと PDサーバーの間で通信の問題が発生した場合、TiDBサーバーはPDサーバーからバージョン情報を時間内に取得または更新できません。この場合、各 DDL の状態処理に 2 * リースを待つ必要があります。

### TiDB のバックエンドstorageエンジンとして S3 を使用できますか? {#can-i-use-s3-as-the-backend-storage-engine-in-tidb}

いいえ。現在、TiDB は分散storageエンジンと Goleveldb/RocksDB/BoltDB エンジンのみをサポートしています。

### <code>Information_schema</code>より実際の情報をサポートできますか? {#can-the-code-information-schema-code-support-more-real-information}

MySQL 互換性の一環として、TiDB は多数の`INFORMATION_SCHEMA`テーブルをサポートしています。これらのテーブルの多くには、対応する SHOW コマンドもあります。詳細については、 [情報スキーマ](/information-schema/information-schema.md)を参照してください。

### TiDB バックオフ タイプのシナリオの説明は何ですか? {#what-s-the-explanation-of-the-tidb-backoff-type-scenario}

TiDBサーバーと TiKVサーバー間の通信プロセスで、大量のデータを処理しているときに、 `Server is busy`または`backoff.maxsleep 20000ms`ログメッセージが表示されます。これは、TiKVサーバーがデータを処理している間、システムがビジー状態になっているためです。このとき、通常、TiKV ホストのリソース使用率が高いことがわかります。このような場合は、リソースの使用状況に応じてサーバーの容量を増やすことができます。

### TiDB TiClient タイプの主な理由は何ですか? {#what-is-the-main-reason-of-tidb-ticlient-type}

TiClientリージョンエラー インジケータは、TiDBサーバーがクライアントとして KV インターフェイスを介して TiKVサーバーにアクセスしてデータ操作を実行するときに表示されるエラーの種類とメトリックを示します。エラーの種類には`not_leader`と`stale_epoch`含まれます。これらのエラーは、TiDBサーバーが独自のキャッシュ情報に従ってリージョンリーダー データを操作した場合、リージョンリーダーが移行した場合、または現在の TiKVリージョン情報と TiDB キャッシュのルーティング情報が一致しない場合に発生します。通常、この場合、TiDBサーバーはPD から最新のルーティング データを自動的に取得し、以前の操作をやり直します。

### TiDB がサポートする同時接続の最大数はいくつですか? {#what-s-the-maximum-number-of-concurrent-connections-that-tidb-supports}

デフォルトでは、TiDBサーバーあたりの最大接続数に制限はありません。必要に応じて、 `config.toml`ファイルに`instance.max_connections`設定するか、システム変数[`max_connections`](/system-variables.md#max_connections)の値を変更して、最大接続数を制限できます。同時接続数が多すぎると応答時間が長くなる場合は、TiDB ノードを追加して容量を増やすことをお勧めします。

### テーブルの作成時間を表示するにはどうすればいいですか? {#how-to-view-the-creation-time-of-a-table}

`information_schema`の表のうち`create_time`作成時刻です。

### TiDB ログの<code>EXPENSIVE_QUERY</code>の意味は何ですか? {#what-is-the-meaning-of-code-expensive-query-code-in-the-tidb-log}

TiDB が SQL ステートメントを実行しているときに、各演算子が 10,000 行以上を処理すると推定される場合、クエリは`EXPENSIVE_QUERY`なります。 `tidb-server`構成パラメータを変更してしきい値を調整し、 `tidb-server`を再起動できます。

### TiDB のテーブルのサイズを見積もるにはどうすればよいでしょうか? {#how-do-i-estimate-the-size-of-a-table-in-tidb}

TiDB 内のテーブルのサイズを見積もるには、次のクエリ ステートメントを使用できます。

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

上記のステートメントを使用する場合は、ステートメント内の次のフィールドを必要に応じて入力して置き換える必要があります。

-   `@dbname` : データベースの名前。
-   `@table_name` : ターゲット テーブルの名前。

さらに、上記の声明では、

-   `store_size_amplification`クラスター圧縮率の平均を示します。この情報を照会するために`SELECT * FROM METRICS_SCHEMA.store_size_amplification;`使用するだけでなく、 **Grafana Monitoring PD - 統計バランス**パネルで各ノードの**サイズ増幅**メトリックを確認することもできます。クラスター圧縮率の平均は、すべてのノードのサイズ増幅の平均です。
-   `Approximate_Size` 、圧縮前のレプリカ内のテーブルのサイズを示します。これはおおよその値であり、正確な値ではないことに注意してください。
-   `Disk_Size`圧縮後のテーブルのサイズを示します。これはおおよその値であり、 `Approximate_Size`と`store_size_amplification`に従って計算できます。

## TiKVサーバー管理 {#tikv-server-management}

このセクションでは、TiKVサーバーの管理中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### コンプライアンスまたはマルチテナント アプリケーションのデータの場所を指定するにはどうすればよいでしょうか? {#how-to-specify-the-location-of-data-for-compliance-or-multi-tenant-applications}

[配置ルール](/placement-rules-in-sql.md)使用して、コンプライアンスまたはマルチテナント アプリケーションのデータの場所を指定できます。

SQL の配置ルールは、レプリカの数、 Raftロール、配置場所、ルールが適用されるキー範囲など、連続したデータ範囲の属性を制御するように設計されています。

### TiKV クラスターのレプリカの推奨数はいくつですか? 高可用性のためには最小数を維持する方が良いですか? {#what-is-the-recommended-number-of-replicas-in-the-tikv-cluster-is-it-better-to-keep-the-minimum-number-for-high-availability}

テスト環境では、リージョンごとに 3 つのレプリカがあれば十分です。ただし、実本番シナリオでは、3 ノード未満の TiKV クラスターを運用しないでください。インフラストラクチャ、ワークロード、および回復力のニーズに応じて、この数を増やす必要がある場合があります。コピー数が多いほどパフォーマンスは低下しますが、セキュリティは高くなることに注意してください。

### TiKVを起動すると、 <code>cluster ID mismatch</code>メッセージが表示されます。 {#the-code-cluster-id-mismatch-code-message-is-displayed-when-starting-tikv}

これは、ローカル TiKV に保存されているクラスター ID が PD で指定されたクラスター ID と異なるためです。新しい PD クラスターがデプロイされると、PD はランダムなクラスター ID を生成します。TiKV は PD からクラスター ID を取得し、初期化時にクラスター ID をローカルに保存します。次に TiKV を起動すると、ローカル クラスター ID と PD のクラスター ID が照合されます。クラスター ID が一致しない場合は、 `cluster ID mismatch`メッセージが表示され、TiKV は終了します。

以前に PD クラスターをデプロイしたが、その後 PD データを削除して新しい PD クラスターをデプロイすると、TiKV が古いデータを使用して新しい PD クラスターに接続するため、このエラーが発生します。

### TiKVを起動すると<code>duplicated store address</code>メッセージが表示されます {#the-code-duplicated-store-address-code-message-is-displayed-when-starting-tikv}

これは、起動パラメータのアドレスが他の TiKV によって PD クラスターに登録されているためです。このエラーが発生する一般的な条件: TiKV `--data-dir`で指定されたパスにデータ フォルダーがありません (削除または移動後に --data-dir を更新していない)。以前のパラメータで TiKV を再起動します。pd-ctl の[ストア削除](https://github.com/pingcap/pd/tree/55db505e8f35e8ab4e00efd202beb27a8ecc40fb/tools/pd-ctl#store-delete--label--weight-store_id----jqquery-string)機能を試し、以前のストアを削除してから、TiKV を再起動してください。

### TiKV プライマリ ノードとセカンダリ ノードは同じ圧縮アルゴリズムを使用しますが、結果が異なるのはなぜですか? {#tikv-primary-node-and-secondary-node-use-the-same-compression-algorithm-why-the-results-are-different}

現在、TiKV プライマリ ノードの一部のファイルは圧縮率が高くなっています。これは、基盤となるデータ分布と RocksDB の実装に依存します。データ サイズが時々変動するのは正常です。基盤となるstorageエンジンは、必要に応じてデータを調整します。

### TiKVブロックキャッシュの機能は何ですか? {#what-are-the-features-of-tikv-block-cache}

TiKV は、RocksDB のカラムファミリ (CF) 機能を実装します。デフォルトでは、KV データは最終的に RocksDB 内の 3 つの CF (デフォルト、書き込み、ロック) に保存されます。

-   デフォルトの CF には実データが保存され、対応するパラメータは`[rocksdb.defaultcf]`にあります。
-   書き込み CF にはデータ バージョン情報 (MVCC) とインデックス関連データが格納され、対応するパラメータは`[rocksdb.writecf]`にあります。
-   ロック CF はロック情報を保存し、システムはデフォルトのパラメータを使用します。
-   Raft RocksDB インスタンスはRaftログを保存します。デフォルトの CF は主にRaftログを保存し、対応するパラメータは`[raftdb.defaultcf]`にあります。
-   すべての CF には、データ ブロックをキャッシュして RocksDB の読み取り速度を向上させる共有ブロック キャッシュがあります。ブロック キャッシュのサイズは、 `block-cache-size`パラメータによって制御されます。パラメータの値が大きいほど、より多くのホット データをキャッシュでき、読み取り操作に有利になります。同時に、システムメモリの消費量も増加します。
-   各 CF には個別の書き込みバッファがあり、そのサイズは`write-buffer-size`パラメータによって制御されます。

### TiKV チャンネルが満員なのはなぜですか? {#why-is-the-tikv-channel-full}

-   Raftstoreスレッドが遅すぎるか、I/O によってブロックされています。Raftstore の CPU 使用状況を表示できます。
-   TiKV がビジー状態 (CPU やディスク I/O など) のため、処理できません。

### TiKV がリージョンリーダーを頻繁に変更するのはなぜですか? {#why-does-tikv-frequently-switch-region-leader}

-   ネットワークの問題により、ノード間の通信が停止します。レポート障害の監視を確認できます。
-   元のメインLeaderのノードがスタックし、Followerに時間内に到達できなくなります。
-   Raftstore のスレッドがスタックしました。

### ノードがダウンした場合、サービスは影響を受けますか? 影響を受ける場合、どのくらいの期間ですか? {#if-a-node-is-down-will-the-service-be-affected-if-yes-how-long}

TiKV はRaftを使用して、複数のレプリカ間でデータを複製します (デフォルトでは、リージョンごとに 3 つのレプリカ)。1 つのレプリカに障害が発生した場合、他のレプリカがデータの安全性を保証します。Raft プロトコルに基づいて、ノードがダウンして単一のリーダーに障害が発生した場合、最大 2 倍のリース時間 (リース時間は 10 秒) 後に、別のノードのフォロワーがすぐにリージョンリーダーとして選出されます。

### I/O、メモリ、CPU を大量に消費し、パラメータ構成を超える TiKV シナリオは何ですか? {#what-are-the-tikv-scenarios-that-take-up-high-i-o-memory-cpu-and-exceed-the-parameter-configuration}

TiKV で大量のデータを書き込んだり読み取ったりすると、大量の I/O、メモリ、CPU が消費されます。大規模な中間結果セットを生成するシナリオなど、非常に複雑なクエリを実行すると、大量のメモリと CPU リソースが消費されます。

### TiKV は SAS/SATA ディスクまたは SSD/SAS ディスクの混合展開をサポートしていますか? {#does-tikv-support-sas-sata-disks-or-mixed-deployment-of-ssd-sas-disks}

いいえ。OLTP シナリオの場合、TiDB はデータ アクセスと操作のために高 I/O ディスクを必要とします。強力な一貫性を備えた分散データベースである TiDB には、レプリカ レプリケーションや最レイヤーのstorageコンパクションなどの書き込み増幅機能があります。したがって、TiDB のベスト プラクティスでは、storageディスクとして NVMe SSD を使用することをお勧めします。TiKV と PD の混合展開はサポートされていません。

### データアクセスの前に、キーデータテーブルの範囲が分割されていますか? {#is-the-range-of-the-key-data-table-divided-before-data-access}

いいえ。MySQL のテーブル分割ルールとは異なります。TiKV では、テーブル Range はリージョンのサイズに基づいて動的に分割されます。

### リージョンはどのように分割されますか? {#how-does-region-split}

リージョンは事前に分割されませんが、リージョン分割メカニズムに従います。リージョンのサイズが`region-max-size`または`region-max-keys`のパラメータの値を超えると、分割がトリガーされます。分割後、その情報は PD に報告されます。

### TiKV には、データのセキュリティを保証するために、MySQL のような<code>innodb_flush_log_trx_commit</code>パラメータがありますか? {#does-tikv-have-the-code-innodb-flush-log-trx-commit-code-parameter-like-mysql-to-guarantee-the-security-of-data}

はい。現在、スタンドアロンstorageエンジンは 2 つの RocksDB インスタンスを使用しています。1 つのインスタンスは raft-log の保存に使用されます。TiKV の`sync-log`パラメータが true に設定されている場合、各コミットは強制的に raft-log にフラッシュされます。クラッシュが発生した場合は、raft-log を使用して KV データを復元できます。

### SSD、RAID レベル、RAID カードのキャッシュ戦略、NUMA 構成、ファイル システム、オペレーティング システムの I/O スケジューリング戦略など、WALstorageに推奨されるサーバー構成は何ですか? {#what-is-the-recommended-server-configuration-for-wal-storage-such-as-ssd-raid-level-cache-strategy-of-raid-card-numa-configuration-file-system-i-o-scheduling-strategy-of-the-operating-system}

WAL は順序付き書き込みに属しており、現在、固有の構成は適用されていません。推奨される構成は次のとおりです。

-   ソリッドステートドライブ
-   RAID 10を推奨
-   RAID カードのキャッシュ戦略とオペレーティング システムの I/O スケジューリング戦略: 現在、特定のベスト プラクティスはありません。Linux 7 以降では、デフォルト構成を使用できます。
-   NUMA: 具体的な提案はありません。メモリ割り当て戦略としては、 `interleave = all`使用できます。
-   ファイルシステム: ext4

### 最も厳密なデータ利用可能モード ( <code>sync-log = true</code> ) での書き込みパフォーマンスはどうですか? {#how-is-the-write-performance-in-the-most-strict-data-available-mode-code-sync-log-true-code}

通常、 `sync-log`有効にするとパフォーマンスが約 30% 低下します。 `sync-log`を`false`に設定した場合の書き込みパフォーマンスについては、 [Sysbench を使用した TiDB のパフォーマンス テスト結果](/benchmark/v3.0-performance-benchmarking-with-sysbench.md)を参照してください。

### TiKVアーキテクチャのRaft + 複数のレプリカは絶対的なデータ安全性を実現できますか? スタンドアロンstorageに最も厳格なモード ( <code>sync-log = true</code> ) を適用する必要がありますか? {#can-raft-multiple-replicas-in-the-tikv-architecture-achieve-absolute-data-safety-is-it-necessary-to-apply-the-most-strict-mode-code-sync-log-true-code-to-a-standalone-storage}

データは、ノード障害が発生した場合の回復可能性を確保するために、 [Raftコンセンサスアルゴリズム](https://raft.github.io/)使用して TiKV ノード間で冗長的に複製されます。データがレプリカの 50% 以上に書き込まれた場合にのみ、アプリケーションは ACK を返します (3 つのノードのうち 2 つ)。ただし、理論的には 2 つのノードがクラッシュする可能性があります。したがって、データの安全性に対する要件がそれほど厳しくなく、パフォーマンスに対する要件が厳しいシナリオを除き、 `sync-log`モードを有効にすることを強くお勧めします。

`sync-log`を使用する代わりに、 Raftグループに 3 つのレプリカではなく 5 つのレプリカを持つことも検討できます。これにより、2 つのレプリカに障害が発生してもデータの安全性が確保されます。

スタンドアロンの TiKV ノードの場合、 `sync-log`モードを有効にすることをお勧めします。そうしないと、ノード障害が発生した場合に最後の書き込みが失われる可能性があります。

### TiKV はRaftプロトコルを使用するため、データの書き込み中に複数のネットワーク ラウンドトリップが発生します。実際の書き込み遅延はどのくらいですか? {#since-tikv-uses-the-raft-protocol-multiple-network-roundtrips-occur-during-data-writing-what-is-the-actual-write-delay}

理論上、TiDB の書き込み遅延は、スタンドアロン データベースよりもネットワーク ラウンドトリップが 4 回多くなります。

### TiDB には、MySQL のように、KV インターフェイスを直接使用でき、独立したキャッシュを必要としない InnoDB memcached プラグインがありますか? {#does-tidb-have-an-innodb-memcached-plugin-like-mysql-which-can-directly-use-the-kv-interface-and-does-not-need-the-independent-cache}

TiKV は、インターフェイスを個別に呼び出すことをサポートしています。理論的には、インスタンスをキャッシュとして取得できます。TiDB は分散リレーショナル データベースであるため、TiKV を個別にサポートしていません。

### コプロセッサーコンポーネントは何に使用されますか? {#what-is-the-coprocessor-component-used-for}

-   TiDBとTiKV間のデータ転送を削減
-   TiKV の分散コンピューティング リソースを最大限に活用して、コンピューティング プッシュダウンを実行します。

### エラーメッセージ<code>IO error: No space left on device While appending to file</code>が表示されます {#the-error-message-code-io-error-no-space-left-on-device-while-appending-to-file-code-is-displayed}

これはディスク容量が不足しているためです。ノードを追加するか、ディスク容量を拡大する必要があります。

### TiKV で OOM (メモリ不足) エラーが頻繁に発生するのはなぜですか? {#why-does-the-oom-out-of-memory-error-occur-frequently-in-tikv}

TiKV のメモリ使用量は主に RocksDB のブロック キャッシュから発生し、デフォルトではシステムメモリサイズの 40% を占めます。TiKV で OOM エラーが頻繁に発生する場合は、値`block-cache-size`の設定が高すぎないか確認する必要があります。また、1 台のマシンに複数の TiKV インスタンスを展開する場合は、複数のインスタンスがシステムメモリを大量に使用して OOM エラーが発生しないように、パラメータを明示的に構成する必要があります。

### TiDB データと RawKV データの両方を同じ TiKV クラスターに保存できますか? {#can-both-tidb-data-and-rawkv-data-be-stored-in-the-same-tikv-cluster}

これは、TiDBのバージョンとTiKV API V2が有効になっているかどうかによって異なります（ [`storage.api-version = 2`](/tikv-configuration-file.md#api-version-new-in-v610) ）。

-   TiDB バージョンが v6.1.0 以降で、TiKV API V2 が有効になっている場合は、TiDB データと RawKV データを同じ TiKV クラスターに保存できます。
-   それ以外の場合、TiDB データ (またはトランザクション API を使用して作成されたデータ) のキー形式は RawKV API を使用して作成されたデータ (または他の RawKV ベースのサービスからのデータ) と互換性がないため、答えは「いいえ」です。

## TiDB テスト {#tidb-testing}

このセクションでは、TiDB テスト中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### Sysbench を使用した TiDB のパフォーマンス テスト結果は何ですか? {#what-is-the-performance-test-result-for-tidb-using-sysbench}

最初は、多くのユーザーが TiDB と MySQL のベンチマーク テストや比較テストを行う傾向があります。私たちも同様の公式テストを実施しましたが、テスト データには多少の偏りはあるものの、テスト結果は概ね一貫していることがわかりました。TiDB のアーキテクチャはMySQL と大きく異なるため、ベンチマーク ポイントを見つけるのは困難です。提案は次のとおりです。

-   ベンチマーク テストに時間をかけすぎないでください。TiDB を使用するシナリオの違いにもっと注意を払ってください。
-   [Sysbench を使用した TiDB のパフォーマンス テスト結果](/benchmark/v3.0-performance-benchmarking-with-sysbench.md)参照。

### TiDB クラスター容量 (QPS) とノード数の関係は何ですか? TiDB と MySQL を比較するとどうなりますか? {#what-s-the-relationship-between-the-tidb-cluster-capacity-qps-and-the-number-of-nodes-how-does-tidb-compare-to-mysql}

-   10 ノード内では、TiDB 書き込み容量 (挿入 TPS) とノード数の関係は、およそ 40% の線形増加です。MySQL は単一ノード書き込みを使用するため、書き込み容量を拡張することはできません。
-   MySQL では、セカンダリ データベースを追加することで読み取り容量を増やすことができますが、書き込み容量はシャーディングを使用する以外では増やすことができず、多くの問題があります。
-   TiDB では、ノードを追加することで読み取り容量と書き込み容量の両方を簡単に増やすことができます。

### DBAによるMySQLとTiDBのパフォーマンステストでは、スタンドアロンのTiDBのパフォーマンスはMySQLほど良くないことがわかりました。 {#the-performance-test-of-mysql-and-tidb-by-our-dba-shows-that-the-performance-of-a-standalone-tidb-is-not-as-good-as-mysql}

TiDB は、MySQL スタンドアロンの容量が限られているためにシャーディングが使用され、強力な一貫性と完全な分散トランザクションが求められるシナリオ向けに設計されています。TiDB の利点の 1 つは、コンピューティングをstorageノードにプッシュダウンして同時コンピューティングを実行することです。

TiDB は、小さなデータサイズと限られたリージョンでは同時実行の強さを発揮できないため、小さいサイズ (1,000 万レベル未満など) のテーブルには適していません。典型的な例は、数行のレコードが頻繁に更新されるカウンター テーブルです。TiDB では、これらの行はstorageエンジンで複数のキーと値のペアになり、単一のノードにあるリージョンに落ち着きます。強力な一貫性を保証するためのバックグラウンド レプリケーションと TiDB から TiKV への操作のオーバーヘッドにより、MySQL スタンドアロンよりもパフォーマンスが低下します。

## バックアップと復元 {#backup-and-restoration}

このセクションでは、バックアップおよび復元中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### TiDB でデータをバックアップするにはどうすればよいですか? {#how-to-back-up-data-in-tidb}

現在、大容量データ (1 TB 以上) のバックアップには、 [バックアップと復元 (BR)](/br/backup-and-restore-overview.md)使用する方法が推奨されています。それ以外の場合は、 [Dumpling](/dumpling-overview.md)というツールが推奨されます。公式の MySQL ツール`mysqldump`も TiDB でデータのバックアップと復元にサポートされていますが、そのパフォーマンスはBRほど優れておらず、大容量データのバックアップと復元にはさらに多くの時間が必要です。

BRに関するその他の FAQ については、 [BRよくある質問](/faq/backup-and-restore-faq.md)参照してください。

### バックアップと復元の速度はどのくらいですか? {#how-is-the-speed-of-backup-and-restore}

[BR](/br/backup-and-restore-overview.md)使用してバックアップおよび復元タスクを実行すると、バックアップは TiKV インスタンスあたり約 40 MB/秒で処理され、復元は TiKV インスタンスあたり約 100 MB/秒で処理されます。
