---
title: TiDB Cluster Management FAQs
summary: TiDB クラスター管理に関する FAQ について説明します。
---

# TiDBクラスタ管理に関する FAQ {#tidb-cluster-management-faqs}

このドキュメントでは、TiDB クラスタ管理に関する FAQ をまとめています。

## 日常管理 {#daily-management}

このセクションでは、日常的なクラスター管理中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### TiDB にログインするにはどうすればいいですか? {#how-to-log-into-tidb}

MySQLにログインするのと同じように、TiDBにログインできます。例えば：

```bash
mysql -h 127.0.0.1 -uroot -P4000
```

### TiDB のシステム変数を変更するにはどうすればよいでしょうか? {#how-to-modify-the-system-variables-in-tidb}

MySQLと同様に、TiDBには静的パラメータとソリッドパラメータが含まれています。静的パラメータは`SET GLOBAL xxx = n`を使用して直接変更できますが、このインスタンスではパラメータの新しい値はライフサイクル内でのみ有効です。

### TiDB (TiKV) のデータ ディレクトリはどこにあり、何ですか? {#where-and-what-are-the-data-directories-in-tidb-tikv}

TiKV データは[`--data-dir`](/command-line-flags-for-tikv-configuration.md#--data-dir)にあり、その中にはそれぞれバックアップ、データ、 Raftデータ、ミラー データの保存に使用される、backup、db、raft、snap の 4 つのディレクトリが含まれます。

### TiDB のシステム テーブルとは何ですか? {#what-are-the-system-tables-in-tidb}

MySQLと同様に、TiDBにもシステムテーブルが含まれており、サーバーの実行時に必要な情報を格納するために使用されます。1 [TiDB システムテーブル](/mysql-schema/mysql-schema.md)参照してください。

### TiDB/PD/TiKV ログはどこにありますか? {#where-are-the-tidb-pd-tikv-logs}

TiDB/PD/TiKVはデフォルトで標準エラー出力をログに出力します。起動時にログファイルを`--log-file`で指定すると、指定されたファイルにログが出力され、日次ローテーションが実行されます。

### TiDB を安全に停止するにはどうすればよいですか? {#how-to-safely-stop-tidb}

-   ロードバランサが実行中の場合（推奨）：ロードバランサを停止し、SQL文`SHUTDOWN`を実行します。その後、TiDBは[`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-new-in-v50)で指定された期間、すべてのセッションが終了するまで待機します。その後、TiDBは実行を停止します。

-   ロードバランサが動作していない場合： `SHUTDOWN`ステートメントを実行します。その後、TiDBコンポーネントは正常に停止します。

### TiDB で<code>kill</code>実行できますか? {#can-code-kill-code-be-executed-in-tidb}

-   DML ステートメントを強制終了します。

    まず`information_schema.cluster_processlist`使用して TiDB インスタンス アドレスとセッション ID を見つけ、次に kill コマンドを実行します。

    TiDB v6.1.0 では、Global Kill 機能が導入されました（これは`enable-global-kill`設定で制御され、デフォルトで有効になっています）。Global Kill が有効になっている場合は、 `kill session_id`実行するだけです。

    TiDBのバージョンがv6.1.0より前の場合、またはGlobal Kill機能が有効になっていない場合、 `kill session_id`デフォルトでは有効になりません。DML文を終了するには、クライアントをDML文を実行しているTiDBインスタンスに直接接続し、 `kill tidb session_id`文を実行する必要があります。クライアントが別のTiDBインスタンスに接続している場合、またはクライアントとTiDBクラスタの間にプロキシが存在する場合、 `kill tidb session_id`文が別のTiDBインスタンスにルーティングされ、別のセッションが誤って終了する可能性があります。詳細については、 [`KILL`](/sql-statements/sql-statement-kill.md)参照してください。

-   DDL文の強制終了：まず`admin show ddl jobs`使用して、終了するDDLジョブのIDを確認し、 `admin cancel ddl jobs 'job_id' [, 'job_id'] ...`実行します。詳細については、 [`ADMIN`ステートメント](/sql-statements/sql-statement-admin.md)を参照してください。

### TiDB はセッション タイムアウトをサポートしていますか? {#does-tidb-support-session-timeout}

TiDB は現在、 [`wait_timeout`](/system-variables.md#wait_timeout) 、 [`interactive_timeout`](/system-variables.md#interactive_timeout) 、 [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760)のタイムアウトをサポートしています。

### TiDB バージョン管理戦略とは何ですか? {#what-is-the-tidb-version-management-strategy}

TiDB バージョン管理の詳細については、 [TiDBのバージョン管理](/releases/versioning.md)参照してください。

### TiDB クラスターの導入と保守にかかる運用コストはどのくらいでしょうか? {#how-about-the-operating-cost-of-deploying-and-maintaining-a-tidb-cluster}

TiDB は、低コストで簡単にクラスターを管理できるいくつかの機能と[ツール](/ecosystem-tool-user-guide.md)提供します。

-   メンテナンス操作の場合、 [TiUP](/tiup/tiup-documentation-guide.md)パッケージ マネージャーとして機能し、デプロイメント、スケーリング、アップグレード、およびその他のメンテナンス タスクを簡素化します。
-   監視に関しては、 [TiDB 監視フレームワーク](/tidb-monitoring-framework.md) [プロメテウス](https://prometheus.io/)使用して監視およびパフォーマンスメトリックを保存し、 [グラファナ](https://grafana.com/grafana/)使用してこれらのメトリックを視覚化します。数百のメトリックを備えた数十の組み込みパネルが利用可能です。
-   トラブルシューティングのために、 [TiDB トラブルシューティング マップ](/tidb-troubleshooting-map.md)では TiDBサーバーおよびその他のコンポーネントの一般的な問題をまとめています。関連する問題が発生した場合、このマップを使用して診断および解決できます。

### さまざまな TiDB マスター バージョンの違いは何ですか? {#what-s-the-difference-between-various-tidb-master-versions}

TiDBコミュニティは非常に活発です。エンジニアたちは機能の最適化とバグ修正に継続的に取り組んでいます。そのため、TiDBのバージョンは非常に頻繁に更新されています。最新バージョンの情報を常に把握したい場合は、 [TiDB リリース タイムライン](/releases/release-timeline.md)ご覧ください。

TiDB [TiUPを使用する](/production-deployment-using-tiup.md)または[TiDB Operatorを使用する](https://docs.pingcap.com/tidb-in-kubernetes/stable)の導入をお勧めします。TiDB はバージョン番号を一元管理しています。バージョン番号は、以下のいずれかの方法で確認できます。

-   `select tidb_version()`
-   `tidb-server -V`

### TiDB 用のグラフィカルデプロイメントツールはありますか? {#is-there-a-graphical-deployment-tool-for-tidb}

現在はいいえ。

### TiDB クラスターをスケールアウトするにはどうすればよいでしょうか? {#how-to-scale-out-a-tidb-cluster}

オンライン サービスを中断することなく、TiDB クラスターをスケール アウトできます。

-   クラスターが[TiUP](/production-deployment-using-tiup.md)を使用してデプロイされている場合は、 [TiUPを使用して TiDBクラスタをスケールする](/scale-tidb-using-tiup.md)を参照してください。
-   クラスターが Kubernetes 上で[TiDB Operator](/tidb-operator-overview.md)使用してデプロイされている場合は、 [Kubernetes 上で TiDB を手動でスケールする](https://docs.pingcap.com/tidb-in-kubernetes/stable/scale-a-tidb-cluster)を参照してください。

### TiDB を水平方向にスケーリングするにはどうすればよいですか? {#how-to-scale-tidb-horizontally}

ビジネスが成長するにつれて、データベースは次の 3 つのボトルネックに直面する可能性があります。

-   storageリソースが不足しており、ディスク領域が十分ではありません。

-   CPU 占有率が高いなどのコンピューティング リソースの不足。

-   書き込みおよび読み取り容量が不十分です。

ビジネスの成長に合わせて TiDB を拡張できます。

-   ディスク容量が不足している場合は、TiKVノードを追加するだけで容量を増やすことができます。新しいノードが起動すると、PDは他のノードから新しいノードにデータを自動的に移行します。

-   コンピューティングリソースが不足している場合は、TiDBノードまたはTiKVノードを追加する前に、CPUの使用状況を確認してください。TiDBノードを追加した場合は、ロードバランサーで設定できます。

-   容量が足りない場合は、TiDB ノードと TiKV ノードの両方を追加できます。

### Percolator が分散ロックを使用し、クラッシュ クライアントがロックを保持している場合、ロックは解放されないのでしょうか? {#if-percolator-uses-distributed-locks-and-the-crash-client-keeps-the-lock-will-the-lock-not-be-released}

詳細は中国語版[パーコレータとTiDBトランザクションアルゴリズム](https://tidb.net/blog/f537be2c)ご覧ください。

### TiDB が Thrift ではなく gRPC を使用するのはなぜですか? Google が使用しているからでしょうか? {#why-does-tidb-use-grpc-instead-of-thrift-is-it-because-google-uses-it}

あまりそうではありません。フロー制御、暗号化、ストリーミングなど、gRPC の優れた機能が必要です。

### <code>like(bindo.customers.name, jason%, 92)</code>の 92 は何を示していますか? {#what-does-the-92-indicate-in-code-like-bindo-customers-name-jason-92-code}

92 はエスケープ文字を示し、デフォルトでは ASCII 92 です。

### <code>information_schema.tables.data_length</code>で表示されるデータ長が、TiKV 監視パネルのストア サイズと異なるのはなぜですか? {#why-does-the-data-length-shown-by-code-information-schema-tables-data-length-code-differ-from-the-store-size-on-the-tikv-monitoring-panel}

理由は2つあります。

-   2 つの結果は異なる方法で計算されます。1 `information_schema.tables.data_length`各行の平均長さを計算して推定された値ですが、TiKV 監視パネルのストア サイズは単一の TiKV インスタンス内のデータ ファイル (RocksDB の SST ファイル) の長さを合計したものです。
-   `information_schema.tables.data_length`は論理値であり、ストアサイズは物理値です。トランザクションの複数のバージョンによって生成された冗長データは論理値には含まれませんが、冗長データはTiKVによって圧縮されて物理値に含まれます。

### トランザクションが非同期コミットまたは 1 フェーズ コミット機能を使用しないのはなぜですか? {#why-does-the-transaction-not-use-the-async-commit-or-the-one-phase-commit-feature}

TiDBは、トランザクションで書き込まれるキーと値のペアが256個以下で、キーの合計サイズが4KB以下の場合にのみ、非同期コミットまたは1フェーズコミット機能を使用します。それ以外の場合、システム変数を使用して機能[非同期コミット](/system-variables.md#tidb_enable_async_commit-new-in-v50)と機能[1フェーズコミット](/system-variables.md#tidb_enable_1pc-new-in-v50)を有効にしても、TiDBはこれらの機能を使用しません。これは、書き込みデータ量が多いトランザクションでは、非同期コミットを使用してもパフォーマンスが大幅に向上しないためです。

## PD管理 {#pd-management}

このセクションでは、PD 管理中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### PDにアクセスすると、 <code>TiKV cluster is not bootstrapped</code>メッセージが表示されます {#the-code-tikv-cluster-is-not-bootstrapped-code-message-is-displayed-when-i-access-pd}

PD の API のほとんどは、TiKV クラスターが初期化されている場合にのみ使用できます。このメッセージは、新しいクラスターをデプロイした際に TiKV が起動されていない状態で PD を起動した際に PD にアクセスした場合に表示されます。このメッセージが表示された場合は、TiKV クラスターを起動してください。TiKV が初期化されると、PD にアクセスできるようになります。

### PD を起動すると、 <code>etcd cluster ID mismatch</code>メッセージが表示されます。 {#the-code-etcd-cluster-id-mismatch-code-message-is-displayed-when-starting-pd}

これは、PD起動パラメータの`--initial-cluster`に、このクラスタに属していないメンバーが含まれているためです。この問題を解決するには、各メンバーに対応するクラスタを確認し、誤ったメンバーを削除してからPDを再起動してください。

### PDの保存時の暗号化を有効にすると<code>[PD:encryption:ErrEncryptionNewMasterKey]fail to get encryption key from file /root/path/file%!(EXTRA string=open /root/path/file: permission denied)</code>メッセージが表示されます。 {#the-code-pd-encryption-errencryptionnewmasterkey-fail-to-get-encryption-key-from-file-root-path-file-extra-string-open-root-path-file-permission-denied-code-message-is-displayed-when-enabling-encryption-at-rest-for-pd}

保存時の暗号化では、キーファイルを`root`ディレクトリまたはそのサブディレクトリに保存することはできません。読み取り権限を付与しても同じエラーが発生します。この問題を解決するには、キーファイルを`root`ディレクトリ以外の場所に保存してください。

### PD の時間同期エラーの最大許容範囲はどれくらいですか? {#what-s-the-maximum-tolerance-for-time-synchronization-error-of-pd}

PD はどのような同期エラーも許容しますが、エラー値が大きいほど、PD によって割り当てられたタイムスタンプと物理時間の間のギャップが大きくなり、履歴バージョンの読み取りなどの関数に影響します。

### クライアント接続はどのようにして PD を見つけるのでしょうか? {#how-does-the-client-connection-find-pd}

クライアント接続はTiDBを介してのみクラスタにアクセスできます。TiDBはPDとTiKVに接続します。PDとTiKVはクライアントに対して透過的です。TiDBがいずれかのPDに接続すると、PDはTiDBに現在のリーダーを通知します。このPDがリーダーでない場合、TiDBはリーダーPDに再接続します。

### TiKV ストアの各ステータス (Up、Disconnect、Offline、Down、Tombstone) 間の関係は何ですか? {#what-is-the-relationship-between-each-status-up-disconnect-offline-down-tombstone-of-a-tikv-store}

各ステータスの関係については[TiKVストアの各ステータスの関係](/tidb-scheduling.md#information-collection)を参照してください。

PD Controlを使用して、TiKV ストアのステータス情報を確認できます。

### PD の<code>leader-schedule-limit</code>と<code>region-schedule-limit</code>スケジューリング パラメータの違いは何ですか? {#what-is-the-difference-between-the-code-leader-schedule-limit-code-and-code-region-schedule-limit-code-scheduling-parameters-in-pd}

-   `leader-schedule-limit`スケジューリング パラメータは、異なる TiKV サーバーのLeader数のバランスをとるために使用され、クエリ処理の負荷に影響します。
-   `region-schedule-limit`スケジューリング パラメータは、異なる TiKV サーバーのレプリカ数のバランスをとるために使用され、異なるノードのデータ量に影響を与えます。

### 各リージョンのレプリカ数は設定可能ですか？設定可能な場合、どのように設定すればよいですか？ {#is-the-number-of-replicas-in-each-region-configurable-if-yes-how-to-configure-it}

はい。現在、レプリカのグローバル数のみを更新できます。PD は初回起動時に設定ファイル (conf/pd.yml) を読み取り、そこに含まれる max-replicas 設定を使用します。後でレプリカ数を更新する場合は、pd-ctl 設定コマンド`config set max-replicas $num`を使用し、有効な設定を`config show all`で表示してください。更新はアプリケーションに影響を与えず、バックグラウンドで実行されます。

TiKVインスタンスの総数は、必ず設定したレプリカ数以上になるようにしてください。例えば、レプリカが3つある場合は、少なくとも3つのTiKVインスタンスが必要です。レプリカ数を増やす前に、追加のstorage要件を見積もる必要があります。pd-ctlの詳細については、 [PD Controlユーザー ガイド](/pd-control.md)参照してください。

### コマンドラインのクラスター管理ツールがない場合に、クラスター全体のヘルス状態を確認するにはどうすればよいでしょうか? {#how-to-check-the-health-status-of-the-whole-cluster-when-lacking-command-line-cluster-management-tools}

pd-ctlツールを使用して、クラスターの全体的なステータスを確認できます。詳細なクラスターステータスを確認するには、モニターを使用する必要があります。

### オフラインになっているクラスター ノードの監視データを削除するにはどうすればよいですか? {#how-to-delete-the-monitoring-data-of-a-cluster-node-that-is-offline}

オフラインノードは通常、TiKVノードを指します。オフラインプロセスが完了したかどうかは、pd-ctlまたはモニターで確認できます。ノードがオフラインになったら、以下の手順を実行してください。

1.  オフライン ノード上の関連サービスを手動で停止します。
2.  Prometheus 構成ファイルから対応するノードの`node_exporter`データを削除します。

## TiDBサーバー管理 {#tidb-server-management}

このセクションでは、TiDBサーバーの管理中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### TiDB で<code>lease</code>パラメータを設定するにはどうすればよいでしょうか? {#how-to-set-the-code-lease-code-parameter-in-tidb}

リースパラメータ（ `--lease=60` ）は、TiDBサーバーの起動時にコマンドラインから設定されます。リースパラメータの値は、現在のセッションにおけるデータベーススキーマ変更（DDL）の速度に影響します。テスト環境では、テストサイクルを高速化するために、この値を1秒に設定できます。ただし、本番環境では、DDLの安全性を確保するために、この値を分単位（例：60）に設定することをお勧めします。

### DDL 操作の処理時間はどれくらいですか? {#what-is-the-processing-time-of-a-ddl-operation}

処理時間はシナリオによって異なります。一般的には、次の3つのシナリオが考えられます。

1.  対応するデータテーブル内の比較的少ない行数での`Add Index`の操作：約3秒
2.  対応するデータテーブル内の行数が比較的多い`Add Index`の操作：処理時間は、その時点の特定の行数とQPSに依存します（ `Add Index`操作は通常のSQL操作よりも優先度が低くなります）
3.  その他のDDL操作: 約1秒

DDL 要求を受信する TiDBサーバーインスタンスが、DDL 所有者が存在する TiDBサーバーインスタンスと同じ場合、上記の最初のシナリオと 3 番目のシナリオでは、数十から数百ミリ秒しかかからない可能性があります。

### DDL ステートメントの実行が非常に遅くなることが時々あるのはなぜですか? {#why-it-is-very-slow-to-run-ddl-statements-sometimes}

考えられる理由:

-   複数のDDL文を同時に実行する場合、最後のいくつかのDDL文の実行速度が遅くなる可能性があります。これは、DDL文がTiDBクラスタ内で順次実行されるためです。
-   クラスタを正常に起動した後、最初のDDL操作の実行に時間がかかる場合があります（通常30秒程度）。これは、TiDBクラスタがDDL文を処理するリーダーを選出しているためです。
-   TiDB 起動後の最初の 10 分間における DDL 文の処理時間は、以下の条件に該当する場合、通常よりも大幅に長くなります。1) TiDB の停止時（停電時を含む）に TiDB が通常どおり PD と通信できない。2) TiDB が`kill -9`コマンドで停止したため、PD から登録データを時間内にクリーンアップできない。この期間中に DDL 文を実行すると、各 DDL の状態変化に 2 * リース（リース = 45 秒）の待機時間が必要になります。
-   クラスタ内のTiDBサーバーとPDサーバー間で通信障害が発生した場合、TiDBサーバーはPDサーバーからバージョン情報を時間内に取得または更新できません。この場合、各DDLの状態処理にはリースの2倍の時間を待つ必要があります。

### TiDB のバックエンドstorageエンジンとして S3 を使用できますか? {#can-i-use-s3-as-the-backend-storage-engine-in-tidb}

いいえ。現在、TiDB は分散storageエンジンと Goleveldb/RocksDB/BoltDB エンジンのみをサポートしています。

### <code>Information_schema</code>はより実際の情報をサポートできますか? {#can-the-code-information-schema-code-support-more-real-information}

MySQLとの互換性の一環として、TiDBは多数の`INFORMATION_SCHEMA`テーブルをサポートしています。これらのテーブルの多くには、対応するSHOWコマンドも用意されています。詳細については、 [情報スキーマ](/information-schema/information-schema.md)参照してください。

### TiDB バックオフ タイプのシナリオの説明は何ですか? {#what-s-the-explanation-of-the-tidb-backoff-type-scenario}

TiDBサーバーとTiKVサーバー間の通信プロセスにおいて、大量のデータを処理している際に`Server is busy`または`backoff.maxsleep 20000ms`ログメッセージが表示されます。これは、TiKVサーバーがデータを処理している間、システムがビジー状態になっているためです。このとき、通常、TiKVホストのリソース使用率が高いことがわかります。このような場合は、リソースの使用状況に応じてサーバー容量を増やすことができます。

### TiDB TiClient タイプの主な理由は何ですか? {#what-is-the-main-reason-of-tidb-ticlient-type}

TiClientリージョンエラーインジケータは、TiDBサーバーがクライアントとしてKVインターフェースを介してTiKVサーバーにアクセスし、データ操作を実行した際に表示されるエラーの種類とメトリックを示します。エラーの種類には`not_leader`と`stale_epoch`含まれます。これらのエラーは、TiDBサーバーが自身のキャッシュ情報に基づいてリージョンリーダーデータを操作した場合、リージョンリーダーが移行した場合、または現在のTiKVリージョン情報とTiDBキャッシュのルーティング情報が一致しない場合に発生します。通常、この場合、TiDBサーバーはPDから最新のルーティングデータを自動的に取得し、以前の操作をやり直します。

### TiDB がサポートする同時接続の最大数はいくつですか? {#what-s-the-maximum-number-of-concurrent-connections-that-tidb-supports}

デフォルトでは、TiDBサーバーあたりの最大接続数に制限はありません。必要に応じて、 `config.toml`ファイルに`instance.max_connections`設定するか、システム変数[`max_connections`](/system-variables.md#max_connections)の値を変更することで、最大接続数を制限できます。同時接続数が多すぎると応答時間が長くなる場合は、TiDBノードを追加して容量を増やすことをお勧めします。

### テーブルの作成時間を表示するにはどうすればいいですか? {#how-to-view-the-creation-time-of-a-table}

`information_schema`の表のうち`create_time`は作成時刻です。

### TiDB ログの<code>EXPENSIVE_QUERY</code>の意味は何ですか? {#what-is-the-meaning-of-code-expensive-query-code-in-the-tidb-log}

TiDBがSQL文を実行する際、各演算子が10,000行以上を処理すると推定される場合、クエリは`EXPENSIVE_QUERY`になります。しきい値を調整するには、 `tidb-server`構成パラメータを変更し、 `tidb-server`を再起動できます。

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

上記のステートメントを使用する場合、ステートメント内の次のフィールドを必要に応じて入力して置き換える必要があります。

-   `@dbname` : データベースの名前。
-   `@table_name` : ターゲット テーブルの名前。

さらに、上記の声明では、

-   `store_size_amplification`クラスター圧縮率の平均を示します。この情報を取得するには`SELECT * FROM METRICS_SCHEMA.store_size_amplification;`使用するだけでなく、 **Grafana Monitoring PD - 統計バランス**パネルで各ノードの**サイズ増幅**メトリックを確認することもできます。クラスター圧縮率の平均は、全ノードのサイズ増幅の平均です。
-   `Approximate_Size`レプリカ内の圧縮前のテーブルサイズを示します。これは概算値であり、正確な値ではないことに注意してください。
-   `Disk_Size`圧縮後のテーブルのサイズを示します。これは概算値であり、 `Approximate_Size`と`store_size_amplification`に基づいて計算できます。

## TiKVサーバー管理 {#tikv-server-management}

このセクションでは、TiKVサーバーの管理中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### コンプライアンスまたはマルチテナント アプリケーションのデータの場所を指定するにはどうすればよいでしょうか? {#how-to-specify-the-location-of-data-for-compliance-or-multi-tenant-applications}

[配置ルール](/placement-rules-in-sql.md)使用して、コンプライアンスまたはマルチテナント アプリケーションのデータの場所を指定できます。

SQL の配置ルールは、レプリカの数、 Raftロール、配置場所、ルールが適用されるキー範囲など、連続したデータ範囲の属性を制御するように設計されています。

### TiKVクラスターのレプリカの推奨数はいくつですか？高可用性を確保するには、レプリカ数を最小限にしておく方が良いでしょうか？ {#what-is-the-recommended-number-of-replicas-in-the-tikv-cluster-is-it-better-to-keep-the-minimum-number-for-high-availability}

テスト環境では、リージョンごとに3つのレプリカがあれば十分です。ただし、本番環境では、TiKVクラスターを3ノード未満で運用することは避けてください。インフラストラクチャ、ワークロード、および回復力のニーズに応じて、この数を増やす必要がある場合があります。なお、コピー数が多いほどパフォーマンスは低下しますが、セキュリティは向上します。

### TiKVを起動すると<code>cluster ID mismatch</code>メッセージが表示されます {#the-code-cluster-id-mismatch-code-message-is-displayed-when-starting-tikv}

これは、ローカルTiKVに保存されているクラスタIDがPDで指定されたクラスタIDと異なるためです。新しいPDクラスタがデプロイされると、PDはランダムなクラスタIDを生成します。TiKVはPDからクラスタIDを取得し、初期化時にローカルに保存します。次回TiKVを起動すると、ローカルクラスタIDとPDのクラスタIDが照合されます。クラスタIDが一致しない場合は、 `cluster ID mismatch`メッセージが表示され、TiKVは終了します。

以前に PD クラスターをデプロイしたが、その後 PD データを削除して新しい PD クラスターをデプロイすると、TiKV が古いデータを使用して新しい PD クラスターに接続するため、このエラーが発生します。

### TiKVを起動すると、 <code>duplicated store address</code>メッセージが表示されます {#the-code-duplicated-store-address-code-message-is-displayed-when-starting-tikv}

これは、起動パラメータのアドレスが他のTiKVによってPDクラスタに登録されているためです。このエラーが発生する一般的な状況：TiKV `--data-dir`で指定されたパスにデータフォルダが存在しない（削除または移動後に--data-dirを更新していない）場合は、以前のパラメータでTiKVを再起動してください。pd-ctlの[ストア削除](https://github.com/pingcap/pd/tree/55db505e8f35e8ab4e00efd202beb27a8ecc40fb/tools/pd-ctl#store-delete--label--weight-store_id----jqquery-string)機能を試し、以前のストアを削除してから、TiKVを再起動してください。

### TiKV プライマリノードとセカンダリノードは同じ圧縮アルゴリズムを使用しますが、結果が異なるのはなぜですか? {#tikv-primary-node-and-secondary-node-use-the-same-compression-algorithm-why-the-results-are-different}

現在、TiKVプライマリノードの一部のファイルは圧縮率が高くなっています。これは、基盤となるデータ分散とRocksDBの実装に依存します。データサイズが時折変動するのは正常な動作です。基盤となるstorageエンジンは必要に応じてデータを調整します。

### TiKVブロックキャッシュの機能は何ですか? {#what-are-the-features-of-tikv-block-cache}

TiKVはRocksDBのカラムファミリ（CF）機能を実装しています。デフォルトでは、KVデータは最終的にRocksDB内の3つのCF（デフォルト、書き込み、ロック）に保存されます。

-   デフォルトの CF には実数データが保存され、対応するパラメータは`[rocksdb.defaultcf]`にあります。
-   書き込み CF にはデータ バージョン情報 (MVCC) とインデックス関連データが格納されており、対応するパラメータは`[rocksdb.writecf]`にあります。
-   ロック CF にはロック情報が保存され、システムはデフォルトのパラメータを使用します。
-   Raft RocksDBインスタンスはRaftログを保存します。デフォルトのCFは主にRaftログを保存し、対応するパラメータは`[raftdb.defaultcf]`です。
-   すべてのCFは、データブロックをキャッシュし、RocksDBの読み取り速度を向上させるための共有ブロックキャッシュを備えています。ブロックキャッシュのサイズはパラメータ`block-cache-size`によって制御されます。パラメータの値が大きいほど、より多くのホットデータをキャッシュできるため、読み取り操作に有利になります。ただし、システムメモリの消費量も増加します。
-   各 CF には個別の書き込みバッファがあり、そのサイズは`write-buffer-size`パラメータによって制御されます。

### TiKV チャンネルが満員なのはなぜですか? {#why-is-the-tikv-channel-full}

-   Raftstoreスレッドが遅すぎるか、I/O によってブロックされています。RaftstoreのCPU 使用状況を確認できます。
-   TiKV はビジー状態 (CPU やディスク I/O など) のため、処理できません。

### TiKV がリージョンリーダーを頻繁に切り替えるのはなぜですか? {#why-does-tikv-frequently-switch-region-leader}

-   ネットワークの問題により、ノード間の通信が停止します。レポート障害の監視を確認できます。
-   元のメインLeaderのノードがスタックし、Followerに時間内に到達できなくなります。
-   Raftstore のスレッドがスタックしました。

### ノードがダウンした場合、サービスに影響はありますか？もしそうなら、どのくらいの期間影響がありますか？ {#if-a-node-is-down-will-the-service-be-affected-if-yes-how-long}

TiKVはRaftを使用して複数のレプリカ（デフォルトでは各リージョンに3つのレプリカ）間でデータを複製します。1つのレプリカに障害が発生した場合でも、他のレプリカがデータの安全性を保証します。Raftプロトコルに基づき、ノードのダウンにより単一のリーダーノードに障害が発生した場合、最大2倍のリース時間（リース時間は10秒）後に、別のノードのフォロワーノードがリージョンリーダーとして選出されます。

### I/O、メモリ、CPU を大量に消費し、パラメータ構成を超える TiKV シナリオは何ですか? {#what-are-the-tikv-scenarios-that-take-up-high-i-o-memory-cpu-and-exceed-the-parameter-configuration}

TiKVへの大容量データの書き込みや読み取りは、I/O、メモリ、CPUを大量に消費します。大規模な中間結果セットを生成するシナリオなど、非常に複雑なクエリの実行には、大量のメモリとCPUリソースが消費されます。

### TiKV は SAS/SATA ディスクまたは SSD/SAS ディスクの混合展開をサポートしていますか? {#does-tikv-support-sas-sata-disks-or-mixed-deployment-of-ssd-sas-disks}

いいえ。OLTPシナリオでは、TiDBはデータアクセスと操作のために高I/Oディスクを必要とします。強力な整合性を備えた分散データベースであるTiDBは、レプリカレプリケーションや最レイヤーのstorageコンパクションといった書き込み増幅機能を備えています。そのため、TiDBのベストプラクティスでは、storageディスクとしてNVMe SSDの使用を推奨します。TiKVとPDの混在環境はサポートされていません。

### データアクセスの前に、キーデータテーブルの範囲が分割されていますか? {#is-the-range-of-the-key-data-table-divided-before-data-access}

いいえ。MySQLのテーブル分割ルールとは異なります。TiKVでは、テーブル Range はリージョンのサイズに基づいて動的に分割されます。

### リージョンはどのように分割されますか? {#how-does-region-split}

リージョンは事前に分割されませんが、リージョン分割メカニズムに従います。リージョンサイズが`region-max-size`または`region-max-keys`パラメータの値を超えると、分割がトリガーされます。分割後、その情報はPDに報告されます。

### TiKV には、データのセキュリティを保証するために、MySQL のような<code>innodb_flush_log_trx_commit</code>パラメータがありますか? {#does-tikv-have-the-code-innodb-flush-log-trx-commit-code-parameter-like-mysql-to-guarantee-the-security-of-data}

TiKVには同様のパラメータはありませんが、TiKVの各コミットはRaftログに強制的にフラッシュされます（TiKVは[Raft Engine](/glossary.md#raft-engine)使用してRaftログを保存し、コミット時に強制的にフラッシュします）。TiKVがクラッシュした場合、KVデータはRaftログに基づいて自動的に復元されます。

### SSD、RAID レベル、RAID カードのキャッシュ戦略、NUMA 構成、ファイル システム、オペレーティング システムの I/O スケジューリング戦略など、WALstorageに推奨されるサーバー構成は何ですか? {#what-is-the-recommended-server-configuration-for-wal-storage-such-as-ssd-raid-level-cache-strategy-of-raid-card-numa-configuration-file-system-i-o-scheduling-strategy-of-the-operating-system}

WALは順序付き書き込み方式に属しており、現時点では特別な設定は適用されていません。推奨される設定は以下のとおりです。

-   SSD
-   RAID 10を推奨
-   RAID カードのキャッシュ戦略とオペレーティング システムの I/O スケジュール戦略: 現在、特定のベスト プラクティスはありません。Linux 7 以降では、デフォルト構成を使用できます。
-   NUMA: 具体的な提案はありません。メモリ割り当て戦略としては、 `interleave = all`使用できます。
-   ファイルシステム: ext4

### TiKVアーキテクチャにおけるRaft + 複数のレプリカは絶対的なデータ安全性を実現できますか? {#can-raft-multiple-replicas-in-the-tikv-architecture-achieve-absolute-data-safety}

データは、ノード障害発生時の復旧可能性を確保するため、 [Raftコンセンサスアルゴリズム](https://raft.github.io/)を使用してTiKVノード間で冗長的に複製されます。データがレプリカの50%以上に書き込まれた場合にのみ、アプリケーションはACKを返します（3ノード中2ノード）。

理論上、2つのノードがクラッシュする可能性があるため、v5.0以降ではTiKVに書き込まれたデータはデフォルトでディスクに書き込まれます。つまり、各コミットはRaftログに強制的にフラッシュされます。TiKVがクラッシュした場合、KVデータはRaftログに従って自動的に回復されます。

さらに、 Raftグループでは3つのレプリカではなく5つのレプリカを使用することも検討できます。このアプローチでは、2つのレプリカに障害が発生してもデータの安全性が確保されます。

### TiKVはRaftプロトコルを使用しているため、データの書き込み中に複数のネットワークラウンドトリップが発生します。実際の書き込み遅延はどの程度ですか？ {#since-tikv-uses-the-raft-protocol-multiple-network-roundtrips-occur-during-data-writing-what-is-the-actual-write-delay}

理論上、TiDB では、スタンドアロン データベースよりもネットワーク ラウンドトリップが 4 回多く書き込み遅延が発生します。

### TiDB には、MySQL のように、KV インターフェイスを直接使用でき、独立したキャッシュを必要としない InnoDB memcached プラグインがありますか? {#does-tidb-have-an-innodb-memcached-plugin-like-mysql-which-can-directly-use-the-kv-interface-and-does-not-need-the-independent-cache}

TiKVはインターフェースの個別呼び出しをサポートしています。理論的には、インスタンスをキャッシュとして使用できます。TiDBは分散リレーショナルデータベースであるため、TiKVを個別にサポートしていません。

### コプロセッサーコンポーネントは何に使用されますか? {#what-is-the-coprocessor-component-used-for}

-   TiDBとTiKV間のデータ転送を削減
-   TiKV の分散コンピューティング リソースを最大限に活用して、コンピューティング プッシュダウンを実行します。

### エラーメッセージ<code>IO error: No space left on device While appending to file</code>が表示されます {#the-error-message-code-io-error-no-space-left-on-device-while-appending-to-file-code-is-displayed}

これはディスク容量が不足しているためです。ノードを追加するか、ディスク容量を拡張する必要があります。

### TiKV で OOM (メモリ不足) エラーが頻繁に発生するのはなぜですか? {#why-does-the-oom-out-of-memory-error-occur-frequently-in-tikv}

TiKVのメモリ使用量は主にRocksDBのブロックキャッシュによって発生し、デフォルトではシステムメモリの40%を占めます。TiKVでOOMエラーが頻繁に発生する場合は、値`block-cache-size`の設定が高すぎないか確認する必要があります。また、複数のTiKVインスタンスを1台のマシンにデプロイしている場合は、複数のインスタンスがシステムメモリを過剰に消費してOOMエラーが発生しないように、パラメータを明示的に設定する必要があります。

### TiDB データと RawKV データの両方を同じ TiKV クラスターに保存できますか? {#can-both-tidb-data-and-rawkv-data-be-stored-in-the-same-tikv-cluster}

これは、TiDBのバージョンとTiKV API V2が有効になっているかどうかによって異なります（ [`storage.api-version = 2`](/tikv-configuration-file.md#api-version-new-in-v610) ）。

-   TiDB バージョンが v6.1.0 以降で、TiKV API V2 が有効になっている場合は、TiDB データと RawKV データを同じ TiKV クラスターに保存できます。
-   それ以外の場合、TiDB データ (またはトランザクション API を使用して作成されたデータ) のキー形式は RawKV API (または他の RawKV ベースのサービスからのデータ) を使用して作成されたデータと互換性がないため、答えは「いいえ」です。

## TiDBテスト {#tidb-testing}

このセクションでは、TiDB テスト中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### TiDB の Sysbench ベンチマーク テストを実行するにはどうすればよいでしょうか? {#how-to-conduct-a-sysbench-benchmark-test-for-tidb}

[Sysbenchを使用してTiDBをテストする方法](/benchmark/benchmark-tidb-using-sysbench.md)参照。

### Sysbench を使用した TiDB のパフォーマンス テスト結果は何ですか? {#what-is-the-performance-test-result-for-tidb-using-sysbench}

多くのユーザーは、最初はTiDBとMySQLのベンチマークテストや比較テストを行う傾向があります。私たちも同様のテストを実施しており、テストデータには多少の偏りはあるものの、テスト結果は概ね一貫していることがわかりました。TiDBのアーキテクチャはMySQLとは大きく異なるため、多くの側面で完全に同等のベンチマークを見つけるのは困難です。

したがって、これらのベンチマークテストに過度に重点を置く必要はありません。むしろ、TiDB を使用したシナリオの違いに注目することをお勧めします。

TiDB v8.5.0 のパフォーマンスについて詳しくは、 TiDB Cloud Dedicated クラスターの[パフォーマンステストレポート](https://docs.pingcap.com/tidbcloud/v8.5-performance-highlights)を参照してください。

### TiDB クラスタの容量 (QPS) とノード数の関係は何ですか? TiDB と MySQL を比較するとどうなりますか? {#what-s-the-relationship-between-the-tidb-cluster-capacity-qps-and-the-number-of-nodes-how-does-tidb-compare-to-mysql}

-   10ノード以内では、TiDBの書き込み容量（挿入TPS）とノード数の関係は、約40%の線形増加となります。MySQLは単一ノード書き込みを採用しているため、書き込み容量をスケールすることはできません。
-   MySQL では、セカンダリ データベースを追加することで読み取り容量を増やすことができますが、書き込み容量はシャーディングを使用する以外では増やすことができず、多くの問題があります。
-   TiDB では、ノードを追加することで読み取り容量と書き込み容量の両方を簡単に増やすことができます。

### 当社のDBAによるMySQLとTiDBのパフォーマンステストでは、スタンドアロンのTiDBのパフォーマンスはMySQLほど良くないことがわかりました。 {#the-performance-test-of-mysql-and-tidb-by-our-dba-shows-that-the-performance-of-a-standalone-tidb-is-not-as-good-as-mysql}

TiDBは、MySQLスタンドアロンの容量が限られているためシャーディングが使用され、強力な一貫性と完全な分散トランザクションが求められるシナリオ向けに設計されています。TiDBの利点の一つは、コンピューティングをstorageノードにプッシュダウンして同時コンピューティングを実行できることです。

TiDBは、小規模なテーブル（例えば1000万件未満）には適していません。これは、データサイズが小さく、リージョンが限られている場合、その並列処理の強みを発揮できないためです。典型的な例としては、数行のレコードが頻繁に更新されるカウンターテーブルが挙げられます。TiDBでは、これらの行はstorageエンジン内で複数のキーと値のペアに変換され、単一ノード上のリージョンに格納されます。強力な一貫性を保証するためのバックグラウンドレプリケーションや、TiDBからTiKVへの操作のオーバーヘッドにより、MySQLスタンドアロンよりもパフォーマンスが低下します。

## バックアップと復元 {#backup-and-restoration}

このセクションでは、バックアップおよび復元中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### TiDB でデータをバックアップするにはどうすればいいですか? {#how-to-back-up-data-in-tidb}

現在、大容量データ（1TB以上）のバックアップには、 [バックアップと復元 (BR)](/br/backup-and-restore-overview.md)使用するのが推奨されます。それ以外の場合は、 [Dumpling](/dumpling-overview.md)推奨ツールです。MySQL公式ツール`mysqldump`もTiDBでデータのバックアップと復元にサポートされていますが、そのパフォーマンスはBRに劣り、大容量データのバックアップと復元にはBRよりもはるかに長い時間がかかります。

BRに関するその他の FAQ については、 [BRよくある質問](/faq/backup-and-restore-faq.md)参照してください。

### バックアップと復元の速度はどうですか? {#how-is-the-speed-of-backup-and-restore}

[BR](/br/backup-and-restore-overview.md)使用してバックアップおよび復元タスクを実行すると、バックアップは TiKV インスタンスごとに約 40 MB/秒で処理され、復元は TiKV インスタンスごとに約 100 MB/秒で処理されます。
