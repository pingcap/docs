---
title: TiDB Cluster Management FAQs
summary: TiDBクラスタ管理に関するよくある質問（FAQ）をご覧ください。
---

# TiDBクラスタ管理に関するよくある質問 {#tidb-cluster-management-faqs}

このドキュメントは、TiDBクラスタ管理に関するよくある質問（FAQ）をまとめたものです。

## 日常管理 {#daily-management}

このセクションでは、日常的なクラスタ管理中に遭遇する可能性のある一般的な問題、その原因、および解決策について説明します。

### TiDBにログインするにはどうすればいいですか？ {#how-to-log-into-tidb}

TiDBへのログインは、MySQLへのログインと同様の方法で行えます。例えば：

```bash
mysql -h 127.0.0.1 -uroot -P4000
```

### TiDBのシステム変数を変更するにはどうすればよいですか？ {#how-to-modify-the-system-variables-in-tidb}

MySQLと同様に、TiDBには静的パラメータと固定パラメータがあります。 `SET GLOBAL xxx = n`を使用して静的パラメータを直接変更できますが、この場合、パラメータの新しい値はライフサイクル内でのみ有効です。

### TiDB（TiKV）におけるデータディレクトリはどこにあり、どのようなものですか？ {#where-and-what-are-the-data-directories-in-tidb-tikv}

TiKVデータは[`--data-dir`](/command-line-flags-for-tikv-configuration.md#--data-dir)に格納されており、バックアップ、データ、 Raftデータ、ミラーデータをそれぞれ保存するために使用されるbackup、db、raft、snapの4つのディレクトリが含まれています。

### TiDBのシステムテーブルとは何ですか？ {#what-are-the-system-tables-in-tidb}

MySQL と同様に、TiDB にはシステム テーブルも含まれており、サーバーの実行時に必要な情報を保存するために使用されます。 [TiDBシステムテーブル](/mysql-schema/mysql-schema.md)を参照してください。

### TiDB/PD/TiKVのログはどこにありますか？ {#where-are-the-tidb-pd-tikv-logs}

デフォルトでは、TiDB/PD/TiKV は標準エラーをログに出力します。起動時に`--log-file`でログファイルが指定されている場合、ログは指定されたファイルに出力され、毎日ローテーションが実行されます。

### TiDBを安全に停止するにはどうすればよいですか？ {#how-to-safely-stop-tidb}

-   ロードバランサーが稼働している場合（推奨）：ロードバランサーを停止し、SQL文`SHUTDOWN`を実行します。その後、TiDBは[`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-new-in-v50)で指定された期間、すべてのセッションが終了するまで待機します。その後、TiDBは停止します。

-   ロードバランサーが実行されていない場合： `SHUTDOWN`ステートメントを実行します。その後、TiDB コンポーネントは正常に停止されます。

### TiDBで<code>kill</code>は実行できますか？ {#can-code-kill-code-be-executed-in-tidb}

-   DMLステートメントを無効化する：

    まず`information_schema.cluster_processlist`を使用して TiDB インスタンスのアドレスとセッション ID を見つけ、次に kill コマンドを実行します。

    TiDB v6.1.0 では、グローバルキル機能が導入されました (デフォルトで有効になっている`enable-global-kill`設定によって制御されます)。グローバルキルが有効になっている場合は、 `kill session_id`を実行するだけです。

    TiDB のバージョンが v6.1.0 より前、またはグローバル キル機能が有効になっていない場合、 `kill session_id`デフォルトでは有効になりません。DML ステートメントを終了するには、クライアントを DML ステートメントを実行している TiDB インスタンスに直接接続してから、 `kill tidb session_id`ステートメントを実行する必要があります。クライアントが別の TiDB インスタンスに接続している場合、またはクライアントと TiDB クラスタの間にプロキシがある場合、 `kill tidb session_id`ステートメントが別の TiDB インスタンスにルーティングされ、別のセッションが誤って終了する可能性があります。詳細については、[`KILL`](/sql-statements/sql-statement-kill.md)参照してください。

-   DDL ステートメントを強制終了するには、まず`admin show ddl jobs`を使用して終了する必要のある DDL ジョブの ID を見つけ、次に`admin cancel ddl jobs 'job_id' [, 'job_id'] ...`を実行します。詳細については、 [`ADMIN`声明](/sql-statements/sql-statement-admin.md)参照してください。

### TiDBはセッションタイムアウトをサポートしていますか？ {#does-tidb-support-session-timeout}

TiDB は現在、 [`wait_timeout`](/system-variables.md#wait_timeout) 、 [`interactive_timeout`](/system-variables.md#interactive_timeout) 、および[`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760)というタイムアウトをサポートしています。

### TiDBのバージョン管理戦略とは何ですか？ {#what-is-the-tidb-version-management-strategy}

TiDB のバージョン管理の詳細については、 [TiDB のバージョン管理](/releases/versioning.md)を参照してください。

### TiDBクラスタの導入と維持にかかる運用コストはどうでしょうか？ {#how-about-the-operating-cost-of-deploying-and-maintaining-a-tidb-cluster}

TiDBは、低コストで簡単にクラスタを管理できるいくつかの機能と[ツール](/ecosystem-tool-user-guide.md)を提供しています。

-   保守作業においては、 [TiUP](/tiup/tiup-documentation-guide.md)パッケージマネージャーとして機能し、デプロイ、スケーリング、アップグレード、その他の保守作業を簡素化します。
-   モニタリングのために、 [TiDB監視フレームワーク](/tidb-monitoring-framework.md)[プロメテウス](https://prometheus.io/)を使用してモニタリングとパフォーマンスのメトリクスを保存し、[グラファナ](https://grafana.com/grafana/)を使用してこれらのメトリクスを視覚化します。数百のメトリクスを備えた数十の組み込みパネルが利用可能です。
-   トラブルシューティングについては、 [TiDBトラブルシューティングマップ](/tidb-troubleshooting-map.md)TiDBサーバーとその他のコンポーネントの一般的な問題がまとめられています。関連する問題が発生した場合は、このマップを使用して問題を診断し、解決できます。

### TiDBのマスターバージョンには、どのような違いがありますか？ {#what-s-the-difference-between-various-tidb-master-versions}

TiDB コミュニティは非常に活発です。エンジニアは機能の最適化とバグの修正を続けてきました。したがって、TiDB のバージョンは非常に速く更新されます。最新バージョンの情報を入手したい場合は、 [TiDBのリリーススケジュール](/releases/release-timeline.md)をご覧ください。

TiDB [TiUPを使用する](/production-deployment-using-tiup.md)、または[TiDB Operatorを使用する](https://docs.pingcap.com/tidb-in-kubernetes/stable)使用するを導入することをお勧めします。 TiDBではバージョン番号を一元管理しています。次のいずれかの方法を使用してバージョン番号を表示できます。

-   `select tidb_version()`
-   `tidb-server -V`

### TiDB用のグラフィカルなデプロイメントツールはありますか？ {#is-there-a-graphical-deployment-tool-for-tidb}

現時点ではいいえ。

### TiDBクラスタをスケールアウトするにはどうすればよいですか？ {#how-to-scale-out-a-tidb-cluster}

TiDBクラスタは、オンラインサービスを中断することなくスケールアウトできます。

-   クラスターが[TiUP](/production-deployment-using-tiup.md)を使用してデプロイされている場合は、 [TiUPを使用してTiDBクラスタをスケーリングする](/scale-tidb-using-tiup.md)を参照してください。
-   Kubernetes 上の[TiDB Operator](/tidb-operator-overview.md)を使用してクラスターがデプロイされている場合は、 [Kubernetes上でTiDBを手動でスケーリングする](https://docs.pingcap.com/tidb-in-kubernetes/stable/scale-a-tidb-cluster)を参照してください。

### TiDBを水平方向にスケールするにはどうすればよいですか？ {#how-to-scale-tidb-horizontally}

ビジネスの成長に伴い、データベースは以下の3つのボトルネックに直面する可能性があります。

-   storageリソースが不足している、つまりディスク容量が足りないということです。

-   CPU使用率が高いなど、コンピューティングリソースの不足。

-   書き込みおよび読み込み容量が不足しています。

TiDBは、ビジネスの成長に合わせて拡張できます。

-   ディスク容量が不足している場合は、TiKVノードを追加するだけで簡単に容量を増やすことができます。新しいノードが起動すると、PDは他のノードから新しいノードへデータを自動的に移行します。

-   コンピューティングリソースが不足している場合は、TiDBノードまたはTiKVノードを追加する前に、まずCPU使用率を確認してください。TiDBノードを追加したら、ロードバランサーで設定できます。

-   容量が不足する場合は、TiDBノードとTiKVノードの両方を追加できます。

### Percolatorが分散ロックを使用し、クラッシュクライアントがロックを保持している場合、ロックは解放されないのでしょうか？ {#if-percolator-uses-distributed-locks-and-the-crash-client-keeps-the-lock-will-the-lock-not-be-released}

詳細については、中国語の[パーコレーターとTiDBトランザクションアルゴリズム](https://pingkai.cn/tidbcommunity/blog/f537be2c)を参照してください。

### TiDBはなぜThriftではなくgRPCを使用しているのですか？Googleが使用しているからでしょうか？ {#why-does-tidb-use-grpc-instead-of-thrift-is-it-because-google-uses-it}

そうではありません。フロー制御、暗号化、ストリーミングなど、gRPCの優れた機能が必要です。

### <code>like(bindo.customers.name, jason%, 92)</code>の 92 は何を示していますか？ {#what-does-the-92-indicate-in-code-like-bindo-customers-name-jason-92-code}

92はエスケープ文字を示しており、デフォルトではASCIIコード92です。

### <code>information_schema.tables.data_length</code>で表示されるデータ長が、TiKV監視パネルのストアサイズと異なるのはなぜですか？ {#why-does-the-data-length-shown-by-code-information-schema-tables-data-length-code-differ-from-the-store-size-on-the-tikv-monitoring-panel}

理由は2つあります。

-   この2つの結果は異なる方法で計算されます。 `information_schema.tables.data_length`は各行の平均長を計算して推定した値ですが、TiKV監視パネルのストアサイズは単一のTiKVインスタンス内のデータファイル（RocksDBのSSTファイル）の長さを合計したものです。
-   `information_schema.tables.data_length`は論理値であり、ストアサイズは物理値です。トランザクションの複数のバージョンによって生成された冗長データは論理値には含まれませんが、物理値ではTiKVによって圧縮されます。

### なぜトランザクションは非同期コミットまたはワンフェーズコミット機能を使用しないのですか？ {#why-does-the-transaction-not-use-the-async-commit-or-the-one-phase-commit-feature}

TiDB は、トランザクションで書き込まれるキーと値のペアが 256 個以下で、キーの合計サイズが 4 KB 以下の場合にのみ、非同期コミットまたはワンフェーズコミット機能を使用します。それ以外の場合は、システム変数を使用して 機能と[非同期コミット](/system-variables.md#tidb_enable_async_commit-new-in-v50)機能を有効にしても、TiDB はこれらの機能を使用しません。これは、大量のデータを書き込むトランザクションでは、非同期コミットを使用して[ワンフェーズコミット](/system-variables.md#tidb_enable_1pc-new-in-v50)パフォーマンスが大幅に向上しないためです。

## PD管理 {#pd-management}

このセクションでは、PD（パーキンソン病）の管理中に遭遇する可能性のある一般的な問題、その原因、および解決策について説明します。

### PDにアクセスすると、 <code>TiKV cluster is not bootstrapped</code>メッセージが表示されます。 {#the-code-tikv-cluster-is-not-bootstrapped-code-message-is-displayed-when-i-access-pd}

PD の API のほとんどは、TiKV クラスタが初期化されたときにのみ利用可能です。このメッセージは、新しいクラスタがデプロイされた際に TiKV が起動していない状態で PD にアクセスした場合に表示されます。このメッセージが表示された場合は、TiKV クラスタを起動してください。TiKV が初期化されると、PD にアクセスできるようになります。

### PD の起動時に<code>etcd cluster ID mismatch</code>メッセージが表示されます {#the-code-etcd-cluster-id-mismatch-code-message-is-displayed-when-starting-pd}

これは、PD起動パラメータの`--initial-cluster`に、このクラスタに属さないメンバーが含まれているためです。この問題を解決するには、各メンバーに対応するクラスタを確認し、間違ったメンバーを削除してからPDを再起動してください。

### PD の保存時の暗号化を有効にすると<code>[PD:encryption:ErrEncryptionNewMasterKey]fail to get encryption key from file /root/path/file%!(EXTRA string=open /root/path/file: permission denied)</code>というメッセージが表示されます。 {#the-code-pd-encryption-errencryptionnewmasterkey-fail-to-get-encryption-key-from-file-root-path-file-extra-string-open-root-path-file-permission-denied-code-message-is-displayed-when-enabling-encryption-at-rest-for-pd}

保存時の暗号化では、キー ファイルを`root`ディレクトリまたはそのサブディレクトリに保存することはサポートされていません。読み取り権限を付与しても、同じエラーが発生します。この問題を解決するには、キー ファイルを`root`ディレクトリ以外の場所に保存してください。

### PDの時刻同期誤差に対する最大許容値はどれくらいですか？ {#what-s-the-maximum-tolerance-for-time-synchronization-error-of-pd}

PDはあらゆる同期エラーを許容できますが、エラー値が大きいほど、PDによって割り当てられたタイムスタンプと物理時刻との間のずれが大きくなり、履歴バージョンの読み取りなどの関数に影響が出ます。

### クライアント接続はどのようにしてPDを検出するのですか？ {#how-does-the-client-connection-find-pd}

クライアント接続は、TiDB を介してのみクラスタにアクセスできます。TiDB は PD と TiKV を接続します。PD と TiKV はクライアントからは透過的です。TiDB がいずれかの PD に接続すると、PD は現在のリーダーが誰であるかを TiDB に通知します。この PD がリーダーでない場合、TiDB はリーダー PD に再接続します。

### TiKVストアの各ステータス（稼働中、切断、オフライン、停止、削除済み）間の関係は何ですか？ {#what-is-the-relationship-between-each-status-up-disconnect-offline-down-tombstone-of-a-tikv-store}

各ステータスの関係については、 [TiKVストアの各ステータス間の関係](/tidb-scheduling.md#information-collection)を参照してください。

PD Controlを使用すると、TiKVストアの状態情報を確認できます。

### PDにおける<code>leader-schedule-limit</code>と<code>region-schedule-limit</code>というスケジューリングパラメータの違いは何ですか？ {#what-is-the-difference-between-the-code-leader-schedule-limit-code-and-code-region-schedule-limit-code-scheduling-parameters-in-pd}

-   `leader-schedule-limit`スケジューリング パラメータは、さまざまな TiKV サーバーのLeader数をバランスさせるために使用され、クエリ処理の負荷に影響します。
-   `region-schedule-limit`スケジューリング パラメータは、異なる TiKV サーバーのレプリカ数をバランスさせるために使用され、異なるノードのデータ量に影響を与えます。

### 各リージョンにおけるレプリカの数は設定可能ですか？設定可能な場合、どのように設定すればよいですか？ {#is-the-number-of-replicas-in-each-region-configurable-if-yes-how-to-configure-it}

はい。現在、グローバルレプリカ数のみ更新可能です。PD は初回起動時に設定ファイル (conf/pd.yml) を読み込み、そこに記載されている max-replicas 設定を使用します。後でレプリカ数を更新する場合は、設定コマンド`config set max-replicas $num`を使用して pd-ctl を実行し、 `config show all`を使用して有効な設定を確認してください。更新はアプリケーションに影響を与えず、バックグラウンドで実行されます。

TiKVインスタンスの総数は、設定したレプリカ数以上であることを確認してください。たとえば、レプリカ数を3にする場合は、少なくとも3つのTiKVインスタンスが必要です。レプリカ数を増やす前に、追加のstorage要件を見積もる必要があります。pd-ctlの詳細については、 [PD Controlユーザーガイド](/pd-control.md)を参照してください。

### コマンドラインによるクラスタ管理ツールがない場合、クラスタ全体の健全性状態を確認するにはどうすればよいでしょうか？ {#how-to-check-the-health-status-of-the-whole-cluster-when-lacking-command-line-cluster-management-tools}

pd-ctlツールを使用すると、クラスターの一般的な状態を確認できます。詳細なクラスターの状態を確認するには、モニターを使用する必要があります。

### オフライン状態のクラスタノードの監視データを削除するにはどうすればよいですか？ {#how-to-delete-the-monitoring-data-of-a-cluster-node-that-is-offline}

オフラインノードは通常、TiKVノードを指します。オフライン処理が完了したかどうかは、pd-ctlまたはモニターで確認できます。ノードがオフラインになったら、以下の手順を実行してください。

1.  オフラインノード上で、関連するサービスを手動で停止してください。
2.  Prometheus設定ファイルから、対応するノードの`node_exporter`データを削除します。

## TiDBサーバー管理 {#tidb-server-management}

このセクションでは、TiDBサーバーの管理中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### TiDBで<code>lease</code>パラメータを設定する方法は？ {#how-to-set-the-code-lease-code-parameter-in-tidb}

リースパラメータ（ `--lease=60` ）は、TiDBサーバーの起動時にコマンドラインから設定します。リースパラメータの値は、現在のセッションのデータベーススキーマ変更（DDL）の速度に影響します。テスト環境では、テストサイクルを高速化するために値を1秒に設定できます。しかし、本番環境では、DDLの安全性を確保するために、値を分（例えば60）に設定することをお勧めします。

### DDL操作の処理時間はどれくらいですか？ {#what-is-the-processing-time-of-a-ddl-operation}

処理時間は状況によって異なります。一般的には、以下の3つのシナリオが考えられます。

1.  対応するデータテーブルの行数が比較的少ない場合の`Add Index`操作：約3秒
2.  対応するデータテーブルの行数が比較的多い場合の`Add Index`操作: 処理時間は、特定の行数と当時の QPS によって異なります ( `Add Index`操作は、通常の SQL 操作よりも優先度が低くなります)。
3.  その他のDDL操作：約1秒

DDLリクエストを受信するTiDBサーバーインスタンスが、DDLオーナーがいるTiDBサーバーインスタンスと同じ場合、上記の1番目と3番目のシナリオでは、数十ミリ秒から数百ミリ秒しかかからない可能性があります。

### DDLステートメントの実行が非常に遅くなることがあるのはなぜですか？ {#why-it-is-very-slow-to-run-ddl-statements-sometimes}

考えられる理由：

-   複数のDDLステートメントを同時に実行する場合、最後の数個のDDLステートメントの実行速度が遅くなる可能性があります。これは、TiDBクラスタではDDLステートメントが直列に実行されるためです。
-   クラスターが正常に起動した後、最初のDDL操作の実行には通常30秒程度かかる場合があります。これは、TiDBクラスターがDDLステートメントを処理するリーダーを選出しているためです。
-   TiDB の起動後最初の 10 分間の DDL ステートメントの処理時間は、以下の条件を満たす場合、通常よりもはるかに長くなります。1) TiDB を停止する際に、TiDB が通常のように PD と通信できない場合 (停電の場合を含む)。2) TiDB が`kill -9`コマンドで停止されたため、TiDB が PD から登録データを適時にクリーンアップできない場合。この期間中に DDL ステートメントを実行すると、各 DDL の状態変更に対して、2 * リース (リース = 45 秒) の待機時間が必要になります。
-   クラスタ内のTiDBサーバーとPDサーバー間で通信障害が発生した場合、TiDBサーバーはPDサーバーからバージョン情報をタイムリーに取得または更新できません。この場合、各DDLの状態処理にはリース期間の2倍の時間待機する必要があります。

### TiDBのバックエンドstorageエンジンとしてS3を使用できますか？ {#can-i-use-s3-as-the-backend-storage-engine-in-tidb}

いいえ。現在、TiDBは分散storageエンジンとGoleveldb/RocksDB/BoltDBエンジンのみをサポートしています。

### <code>Information_schema</code>は、より多くの実際の情報をサポートできますか？ {#can-the-code-information-schema-code-support-more-real-information}

MySQLとの互換性の一環として、TiDBは多数の`INFORMATION_SCHEMA`テーブルをサポートしています。これらのテーブルの多くには、対応するSHOWコマンドもあります。詳細については、 [情報スキーマ](/information-schema/information-schema.md)を参照してください。

### TiDBバックオフタイプのシナリオの説明は何ですか？ {#what-s-the-explanation-of-the-tidb-backoff-type-scenario}

TiDBサーバーとTiKVサーバー間の通信プロセスにおいて、大量のデータを処理する際に`Server is busy`または`backoff.maxsleep 20000ms`ログメッセージが表示されることがあります。これは、TiKVサーバーがデータを処理している間、システムがビジー状態になっているためです。通常、このときTiKVホストのリソース使用率が高くなっていることが確認できます。このような場合は、リソース使用状況に応じてサーバー容量を増やすことができます。

### TiDB TiClientタイプの主な理由は何ですか？ {#what-is-the-main-reason-of-tidb-ticlient-type}

TiClientリージョンエラーインジケータは、TiDBサーバーがクライアントとしてKVインターフェイスを介してTiKVサーバーにアクセスし、データ操作を実行する際に表示されるエラーの種類とメトリックを示します。エラーの種類には`not_leader`と`stale_epoch`が含まれます。これらのエラーは、TiDBサーバーが自身のキャッシュ情報に基づいてリージョンリーダーデータを操作している場合、リージョンリーダーが移行した場合、または現在のTiKVリージョン情報とTiDBキャッシュのルーティング情報が一致しない場合に発生します。通常、この場合、TiDBサーバーはPDから最新のルーティングデータを自動的に取得し、以前の操作をやり直します。

### TiDBがサポートする同時接続の最大数はいくつですか？ {#what-s-the-maximum-number-of-concurrent-connections-that-tidb-supports}

デフォルトでは、TiDBサーバーあたりの最大接続数に制限はありません。必要に応じて、 `instance.max_connections`ファイルで`config.toml` }を設定するか、システム変数[`max_connections`](/system-variables.md#max_connections)の値を変更することで、最大接続数を制限できます。同時接続数が多すぎると応答時間が長くなる場合は、TiDBノードを追加して容量を増やすことをお勧めします。

### テーブルの作成時間を確認するにはどうすればよいですか？ {#how-to-view-the-creation-time-of-a-table}

`create_time`内のテーブルの`information_schema`は作成時刻です。

### TiDBログにおける<code>EXPENSIVE_QUERY</code>の意味は何ですか？ {#what-is-the-meaning-of-code-expensive-query-code-in-the-tidb-log}

TiDB が SQL ステートメントを実行する際、各オペレータが 10,000 行を超える行を処理すると推定される場合、クエリは`EXPENSIVE_QUERY`になります。 `tidb-server`構成パラメータを変更してしきい値を調整し、 `tidb-server`を再起動できます。

### TiDBでテーブルのサイズを推定するにはどうすればよいですか？ {#how-do-i-estimate-the-size-of-a-table-in-tidb}

TiDB のテーブルのサイズを推定するには、次のクエリ ステートメントを使用できます。

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

上記のステートメントを使用する際は、ステートメント内の以下のフィールドを適切に入力および置換する必要があります。

-   `@dbname` : データベースの名前。
-   `@table_name` : 対象テーブルの名前。

さらに、上記の声明では、

-   `store_size_amplification`クラスタ圧縮率の平均値を示します。 `SELECT * FROM METRICS_SCHEMA.store_size_amplification;`を使用してこの情報を照会する以外にも、 **Grafana Monitoring PD - 統計バランス**パネルで各ノードの**サイズ増幅**メトリックを確認することもできます。クラスタ圧縮率の平均値は、すべてのノードのサイズ増幅の平均値です。
-   `Approximate_Size`圧縮前のレプリカ内のテーブルのサイズを示します。これは概算値であり、正確な値ではないことに注意してください。
-   `Disk_Size`圧縮後のテーブルのサイズを示します。これは概算値であり、 `Approximate_Size`および`store_size_amplification`に基づいて計算できます。

## TiKVサーバー管理 {#tikv-server-management}

このセクションでは、TiKVサーバーの管理中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### コンプライアンス遵守やマルチテナントアプリケーションにおいて、データの保存場所を指定するにはどうすればよいですか？ {#how-to-specify-the-location-of-data-for-compliance-or-multi-tenant-applications}

[配置ルール](/placement-rules-in-sql.md)を使用して、コンプライアンスまたはマルチテナント アプリケーションのデータの場所を指定できます。

SQL の配置ルールは、レプリカ数、 Raftの役割、配置場所、ルールが適用されるキー範囲など、連続データ範囲の属性を制御するように設計されています。

### TiKVクラスターにおける推奨レプリカ数はいくつですか？高可用性を確保するためには、最小限の数に抑えるのが良いのでしょうか？ {#what-is-the-recommended-number-of-replicas-in-the-tikv-cluster-is-it-better-to-keep-the-minimum-number-for-high-availability}

テスト環境であれば、リージョンごとに3つのレプリカで十分です。ただし、本番環境では、3ノード未満のTiKVクラスタを運用することは絶対に避けてください。インフラストラクチャ、ワークロード、および耐障害性のニーズに応じて、この数を増やす必要があるかもしれません。コピー数が多いほどパフォーマンスは低下しますが、セキュリティは向上することに注意してください。

### TiKVの起動時に<code>cluster ID mismatch</code>メッセージが表示されます {#the-code-cluster-id-mismatch-code-message-is-displayed-when-starting-tikv}

これは、ローカルの TiKV に保存されているクラスタ ID が、PD で指定されているクラスタ ID と異なるためです。新しい PD クラスタがデプロイされると、PD はランダムなクラスタ ID を生成します。TiKV は初期化時に PD からクラスタ ID を取得し、ローカルに保存します。次に TiKV が起動されると、ローカルのクラスタ ID と PD のクラスタ ID が照合されます。クラスタ ID が一致しない場合、 `cluster ID mismatch`メッセージが表示され、TiKV は終了します。

以前にPDクラスタをデプロイした後、PDデータを削除して新しいPDクラスタをデプロイした場合、TiKVが古いデータを使用して新しいPDクラスタに接続しようとするため、このエラーが発生します。

### TiKVの起動時に<code>duplicated store address</code>メッセージが表示されます {#the-code-duplicated-store-address-code-message-is-displayed-when-starting-tikv}

これは、起動パラメータのアドレスが他の TiKV によって PD クラスタに登録されているためです。このエラーが発生する一般的な条件: TiKV `--data-dir`で指定されたパスにデータフォルダがありません (削除または移動後に --data-dir を更新しません)。以前のパラメータを使用して TiKV を再起動してください。pd-ctl の[ストア削除](https://github.com/pingcap/pd/tree/55db505e8f35e8ab4e00efd202beb27a8ecc40fb/tools/pd-ctl#store-delete--label--weight-store_id----jqquery-string)機能を使用して以前のストアを削除し、TiKV を再起動してください。

### TiKVのプライマリノードとセカンダリノードは同じ圧縮アルゴリズムを使用しているのに、なぜ結果が異なるのでしょうか？ {#tikv-primary-node-and-secondary-node-use-the-same-compression-algorithm-why-the-results-are-different}

現在、TiKVプライマリノードの一部のファイルは圧縮率が高くなっていますが、これは基盤となるデータ分布とRocksDBの実装に依存します。データサイズが時折変動するのは正常な動作です。基盤となるstorageエンジンが必要に応じてデータを調整します。

### TiKVブロックキャッシュの特徴は何ですか？ {#what-are-the-features-of-tikv-block-cache}

TiKVはRocksDBのカラムファミリー（CF）機能を実装しています。デフォルトでは、KVデータはRocksDB内の3つのCF（デフォルト、書き込み、ロック）に格納されます。

-   デフォルトのCFには実際のデータが保存され、対応するパラメータは`[rocksdb.defaultcf]`にあります。
-   書き込みCFにはデータバージョン情報（MVCC）とインデックス関連データが格納され、対応するパラメータは`[rocksdb.writecf]`にあります。
-   ロックCFにはロック情報が保存され、システムはデフォルトのパラメータを使用します。
-   Raft RocksDB インスタンスはRaftログを保存します。デフォルトの CF は主にRaftログを保存し、対応するパラメータは`[raftdb.defaultcf]`にあります。
-   すべてのCFには、データブロックをキャッシュしてRocksDBの読み取り速度を向上させるための共有ブロックキャッシュがあります。ブロックキャッシュのサイズは`block-cache-size`パラメータで制御されます。このパラメータの値が大きいほど、より多くのホットデータをキャッシュでき、読み取り操作に有利になります。同時に、システムメモリの消費量も増加します。
-   各CFには個別の書き込みバッファがあり、そのサイズは`write-buffer-size`パラメータによって制御されます。

### TiKVチャンネルが満員なのはなぜですか？ {#why-is-the-tikv-channel-full}

-   Raftstoreスレッドの処理速度が遅すぎるか、I/O によってブロックされています。RaftstoreのCPU 使用状況を確認できます。
-   TiKVは（CPUやディスクI/Oなど）ビジー状態であり、処理しきれません。

### TiKVはなぜ頻繁にリージョンリーダーを切り替えるのか？ {#why-does-tikv-frequently-switch-region-leader}

-   ネットワークの問題により、ノード間の通信が停止します。障害レポートの監視状況を確認できます。
-   元のメインLeaderのノードが停止したため、Followerへの接続が時間内に完了しませんでした。
-   Raftstoreのスレッドが詰まってしまった。

### ノードがダウンした場合、サービスに影響はありますか？影響がある場合、どのくらいの期間影響しますか？ {#if-a-node-is-down-will-the-service-be-affected-if-yes-how-long}

TiKVはRaftを使用して、複数のレプリカ間でデータを複製します（デフォルトでは、各リージョンにつき3つのレプリカ）。1つのレプリカに障害が発生した場合でも、他のレプリカがデータのRaft性を保証します。Raftプロトコルに基づき、ノードのダウンにより単一のリーダーが故障した場合、別のノードのフォロワーがリース時間（10秒）の2倍の時間が経過すると、リージョンのリーダーとして選出されます。

### TiKVにおいて、I/O、メモリ、CPUを大量に消費し、パラメータ設定を超えるシナリオとはどのようなものですか？ {#what-are-the-tikv-scenarios-that-take-up-high-i-o-memory-cpu-and-exceed-the-parameter-configuration}

TiKVで大量のデータを書き込んだり読み込んだりすると、I/O、メモリ、CPUリソースを大量に消費します。非常に複雑なクエリを実行すると、大量のメモリとCPUリソースが必要になります。例えば、大量の中間結果セットを生成するようなシナリオがこれに該当します。

### TiKVはSAS/SATAディスク、またはSSD/SASディスクの混在構成をサポートしていますか？ {#does-tikv-support-sas-sata-disks-or-mixed-deployment-of-ssd-sas-disks}

いいえ。OLTPシナリオでは、TiDBはデータアクセスと操作に高I/Oディスクを必要とします。TiDBは強力な一貫性を備えた分散データベースであり、レプリカレプリケーションやボトムレイヤーstorageの圧縮など、書き込み増幅機能を備えています。そのため、TiDBのベストプラクティスでは、storageディスクとしてNVMe SSDの使用を推奨しています。TiKVとPDの混在展開はサポートされていません。

### キーデータテーブルの範囲は、データアクセス前に分割されますか？ {#is-the-range-of-the-key-data-table-divided-before-data-access}

いいえ。これはMySQLのテーブル分割ルールとは異なります。TiKVでは、テーブルRangeはリージョンのサイズに基づいて動的に分割されます。

### リージョンはどのように分割されますか？ {#how-does-region-split}

リージョンは事前に分割されるのではなく、リージョン分割メカニズムに従って分割されます。リージョンサイズが`region-max-size`または`region-max-keys`パラメータの値を超えると、分割がトリガーされます。分割後、その情報がPDに報告されます。

### TiKVには、MySQLのようにデータのセキュリティを保証するための<code>innodb_flush_log_trx_commit</code>パラメータはありますか？ {#does-tikv-have-the-code-innodb-flush-log-trx-commit-code-parameter-like-mysql-to-guarantee-the-security-of-data}

TiKVには同様のパラメータはありませんが、TiKVではコミットごとにRaftログへの書き込みが強制されます（TiKVは[Raft Engine](/glossary.md#raft-engine)を使用してRaftログを保存し、コミット時に強制的に書き込みを行います）。TiKVがクラッシュした場合、KVデータはRaftログに基づいて自動的に復旧されます。

### WALstorageに推奨されるサーバー構成（SSD、RAIDレベル、RAIDカードのキャッシュ戦略、NUMA構成、ファイルシステム、オペレーティングシステムのI/Oスケジューリング戦略など）は何ですか？ {#what-is-the-recommended-server-configuration-for-wal-storage-such-as-ssd-raid-level-cache-strategy-of-raid-card-numa-configuration-file-system-i-o-scheduling-strategy-of-the-operating-system}

WALは順序付き書き込みに属し、現在、固有の構成は適用されていません。推奨される構成は以下のとおりです。

-   SSD
-   RAID 10を推奨
-   RAIDカードのキャッシュ戦略とオペレーティングシステムのI/Oスケジューリング戦略：現時点では特定のベストプラクティスはありません。Linux 7以降ではデフォルト設定を使用できます。
-   NUMA: 特に推奨はありません。メモリ割り当て戦略には`interleave = all`を使用できます。
-   ファイルシステム: ext4

### TiKVアーキテクチャにおけるRaftと複数のレプリカの組み合わせは、絶対的なデータ安全性を実現できるのか？ {#can-raft-multiple-replicas-in-the-tikv-architecture-achieve-absolute-data-safety}

データは[Raftコンセンサスアルゴリズム](https://raft.github.io/)を使用して TiKV ノード間で冗長的に複製され、ノード障害が発生した場合の回復可能性を確保します。データがレプリカの 50% を超えて書き込まれた場合にのみ、アプリケーションは ACK を返します (3 ノードのうち 2 ノード)。

理論上2つのノードがクラッシュする可能性があるため、v5.0以降、TiKVに書き込まれたデータはデフォルトでディスクに書き込まれるようになっています。つまり、コミットごとに強制的にRaftログに書き込まれることになります。TiKVがクラッシュした場合、KVデータはRaftログに基づいて自動的に復旧されます。

さらに、 Raftグループでレプリカを3つではなく5つ使用することを検討してみてください。この方法であれば、2つのレプリカが故障してもデータの安全性が確保されます。

### TiKVはRaftプロトコルを使用しているため、データ書き込み中に複数のネットワーク往復が発生します。実際の書き込み遅延時間はどれくらいですか？ {#since-tikv-uses-the-raft-protocol-multiple-network-roundtrips-occur-during-data-writing-what-is-the-actual-write-delay}

理論上、TiDBはスタンドアロンデータベースよりもネットワークの往復回数が4回多く、書き込み遅延が発生します。

### TiDBには、MySQLのようにKVインターフェースを直接使用でき、独立したキャッシュを必要としないInnoDB memcachedプラグインはありますか？ {#does-tidb-have-an-innodb-memcached-plugin-like-mysql-which-can-directly-use-the-kv-interface-and-does-not-need-the-independent-cache}

TiKVはインターフェースを個別に呼び出すことをサポートしています。理論的には、インスタンスをキャッシュとして使用できます。TiDBは分散リレーショナルデータベースであるため、TiKVを個別にサポートしていません。

### コプロセッサーコンポーネントは何のために使用されるのですか？ {#what-is-the-coprocessor-component-used-for}

-   TiDBとTiKV間のデータ伝送を削減する
-   TiKVの分散コンピューティングリソースを最大限に活用して、コンピューティングプッシュダウンを実行します。

### エラーメッセージ<code>IO error: No space left on device While appending to file</code>が表示されます。 {#the-error-message-code-io-error-no-space-left-on-device-while-appending-to-file-code-is-displayed}

これはディスク容量が不足しているためです。ノードを追加するか、ディスク容量を拡張する必要があります。

### TiKVでOOM（メモリ不足）エラーが頻繁に発生するのはなぜですか？ {#why-does-the-oom-out-of-memory-error-occur-frequently-in-tikv}

TiKVのメモリ使用量は主にRocksDBのブロックキャッシュによるもので、デフォルトではシステムメモリの40%を占めます。TiKVでOOMエラーが頻繁に発生する場合は、 `block-cache-size`の値が高すぎないか確認してください。また、1台のマシンに複数のTiKVインスタンスをデプロイする場合は、複数のインスタンスがシステムメモリを過剰に使用してOOMエラーが発生しないように、パラメータを明示的に設定する必要があります。

### TiDBデータとRawKVデータの両方を同じTiKVクラスタに保存することは可能ですか？ {#can-both-tidb-data-and-rawkv-data-be-stored-in-the-same-tikv-cluster}

TiDBのバージョンとTiKV API V2が有効になっているかどうか（ [`storage.api-version = 2`](/tikv-configuration-file.md#api-version-new-in-v610) ）によって異なります。

-   TiDBのバージョンがv6.1.0以降で、TiKV API V2が有効になっている場合、TiDBデータとRawKVデータを同じTiKVクラスタに保存できます。
-   それ以外の場合は、TiDBデータ（またはトランザクションAPIを使用して作成されたデータ）のキー形式がRawKV APIを使用して作成されたデータ（または他のRawKVベースのサービスからのデータ）と互換性がないため、答えは「いいえ」となります。

## TiDBテスト {#tidb-testing}

このセクションでは、TiDBのテスト中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### TiDBのSysbenchベンチマークテストを実施するにはどうすればよいですか？ {#how-to-conduct-a-sysbench-benchmark-test-for-tidb}

[Sysbenchを使用してTiDBをテストする方法](/benchmark/benchmark-tidb-using-sysbench.md)参照してください。

### Sysbenchを使用したTiDBのパフォーマンステスト結果はどうなっていますか？ {#what-is-the-performance-test-result-for-tidb-using-sysbench}

最初は、多くのユーザーがTiDBとMySQLのベンチマークテストや比較テストを実施する傾向があります。弊社でも同様のテストを実施しましたが、テストデータに多少の偏りはあるものの、テスト結果は概ね一貫していることがわかりました。TiDBのアーキテクチャはMySQLとは大きく異なるため、多くの点で完全に同等のベンチマークを見つけるのは困難です。

したがって、これらのベンチマークテストに過度にこだわる必要はありません。むしろ、TiDBを使用したシナリオの違いに注目することをお勧めします。

TiDB v8.5.0 のパフォーマンスについて知るには、 TiDB Cloud Dedicatedクラスターの[性能テストレポート](https://docs.pingcap.com/tidbcloud/v8.5-performance-highlights)を参照してください。

### TiDBのクラスタ容量（QPS）とノード数の関係はどうなっていますか？TiDBはMySQLと比べてどうですか？ {#what-s-the-relationship-between-the-tidb-cluster-capacity-qps-and-the-number-of-nodes-how-does-tidb-compare-to-mysql}

-   ノード数が10個以内の場合、TiDBの書き込み容量（挿入TPS）とノード数の関係は、おおよそ40%の線形増加を示します。MySQLはシングルノード書き込み方式を採用しているため、書き込み容量を拡張することはできません。
-   MySQLでは、セカンダリデータベースを追加することで読み取り容量を増やすことができますが、書き込み容量はシャーディングを使用しない限り増やすことはできません。しかし、シャーディングには多くの問題があります。
-   TiDBでは、ノードを追加することで、読み取り容量と書き込み容量の両方を容易に増やすことができます。

### 当社のDBAによるMySQLとTiDBのパフォーマンステストの結果、スタンドアロンのTiDBのパフォーマンスはMySQLほど良くないことが分かりました。 {#the-performance-test-of-mysql-and-tidb-by-our-dba-shows-that-the-performance-of-a-standalone-tidb-is-not-as-good-as-mysql}

TiDBは、MySQLスタンドアロンの容量が限られているためシャーディングが使用されるシナリオ、および強力な一貫性と完全な分散トランザクションが必要とされるシナリオ向けに設計されています。TiDBの利点の1つは、並列処理を実行するためにコンピューティング処理をstorageノードにプッシュダウンできることです。

TiDBは、小規模なテーブル（例えば1,000万件未満）には適していません。データサイズが小さく、リージョン数が限られている場合、TiDBの並行処理能力を十分に発揮できないためです。典型的な例として、数行のレコードが頻繁に更新されるカウンターテーブルが挙げられます。TiDBでは、これらの行はstorageエンジン内で複数のキーバリューペアに変換され、単一ノード上のリージョンに格納されます。強力な一貫性を保証するためのバックグラウンドレプリケーションや、TiDBからTiKVへの操作によるオーバーヘッドのため、MySQLスタンドアロンよりもパフォーマンスが低下します。

## バックアップと復元 {#backup-and-restoration}

このセクションでは、バックアップと復元中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### TiDBでデータをバックアップする方法は？ {#how-to-back-up-data-in-tidb}

現在、大容量データ（1 TB 以上）のバックアップには、[バックアップと復元 (BR)](/br/backup-and-restore-overview.md)を使用する方法が推奨されています。それ以外の場合は、 [Dumpling](/dumpling-overview.md)が推奨ツールです。公式の MySQL ツール`mysqldump`も TiDB でデータのバックアップと復元にサポートされていますが、そのパフォーマンスはBRと変わらず、大容量データのバックアップと復元にははるかに時間がかかります。

BRに関するその他のよくある質問については、 [BRよくある質問](/faq/backup-and-restore-faq.md)参照してください。

### バックアップと復元の速度はどうですか？ {#how-is-the-speed-of-backup-and-restore}

[BR](/br/backup-and-restore-overview.md)を使用してバックアップおよびリストアタスクを実行する場合、バックアップはTiKVインスタンスあたり約40MB/秒で処理され、リストアはTiKVインスタンスあたり約100MB/秒で処理されます。
