---
title: Cluster Management FAQs
summary: Learn about the FAQs related to TiDB cluster management.
---

# クラスター管理に関するFAQ {#cluster-management-faqs}

このドキュメントは、TiDBクラスタ管理に関連するFAQをまとめたものです。

## 日常の管理 {#daily-management}

このセクションでは、日常のクラスタ管理中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### TiDBにログインする方法は？ {#how-to-log-into-tidb}

MySQLにログインするのと同じようにTiDBにログインできます。例えば：

```bash
mysql -h 127.0.0.1 -uroot -P4000
```

### TiDBでシステム変数を変更するにはどうすればよいですか？ {#how-to-modify-the-system-variables-in-tidb}

MySQLと同様に、TiDBには静的パラメーターとソリッドパラメーターが含まれています。 `set global xxx = n`を使用して静的パラメーターを直接変更できますが、パラメーターの新しい値は、この場合のライフサイクル内でのみ有効です。

### TiDB（TiKV）のデータディレクトリはどこにありますか？ {#where-and-what-are-the-data-directories-in-tidb-tikv}

TiKVデータは[`--data-dir`](/command-line-flags-for-tikv-configuration.md#--data-dir)にあり、バックアップ、db、raft、およびsnapの4つのディレクトリが含まれ、それぞれバックアップ、データ、Raftデータ、およびミラーデータを格納するために使用されます。

### TiDBのシステムテーブルは何ですか？ {#what-are-the-system-tables-in-tidb}

MySQLと同様に、TiDBにはシステムテーブルも含まれており、サーバーの実行時にサーバーに必要な情報を格納するために使用されます。 [TiDBシステムテーブル](/mysql-schema.md)を参照してください。

### TiDB / PD / TiKVログはどこにありますか？ {#where-are-the-tidb-pd-tikv-logs}

デフォルトでは、TiDB / PD/TiKVはログに標準エラーを出力します。起動時にログファイルを`--log-file`で指定すると、指定したファイルにログが出力され、毎日ローテーションが実行されます。

### TiDBを安全に停止する方法は？ {#how-to-safely-stop-tidb}

-   ロードバランサーが実行されている場合（推奨）：ロードバランサーを停止し、SQLステートメント`SHUTDOWN`を実行します。次に、TiDBは、すべてのセッションが終了するまで、 [`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-new-in-v50)で指定された期間待機します。その後、TiDBは実行を停止します。

-   ロードバランサーが実行されていない場合： `SHUTDOWN`ステートメントを実行します。その後、TiDBコンポーネントは正常に停止します。

### <code>kill</code>はTiDBで実行できますか？ {#can-code-kill-code-be-executed-in-tidb}

-   DMLステートメントを強制終了します。

    最初に`information_schema.cluster_processlist`を使用して、TiDBインスタンスアドレスとセッションIDを見つけます。 DMLステートメントを実行しているTiDBインスタンスにクライアントを直接接続します。次に、 `kill tidb session_id`ステートメントを実行します。

    クライアントが別のTiDBインスタンスに接続する場合、またはクライアントとTiDBクラスタの間にプロキシがある場合、 `kill tidb session_id`ステートメントが別のTiDBインスタンスにルーティングされ、別のセッションが誤って終了する可能性があります。詳細については、 [`KILL`](/sql-statements/sql-statement-kill.md)を参照してください。

-   DDLステートメントを強制終了する：最初に`admin show ddl jobs`を使用して終了する必要のあるDDLジョブのIDを見つけてから、 `admin cancel ddl jobs 'job_id' [, 'job_id'] ...`を実行します。詳細については、 [`ADMIN`ステートメント](/sql-statements/sql-statement-admin.md)を参照してください。

### TiDBはセッションタイムアウトをサポートしていますか？ {#does-tidb-support-session-timeout}

TiDBは現在、 [`wait_timeout`](/system-variables.md#wait_timeout)と[`interactive_timeout`](/system-variables.md#interactive_timeout)の2つのタイムアウトをサポートしています。

### 本番環境のTiDBバージョン管理戦略とは何ですか？頻繁なアップグレードを回避する方法は？ {#what-is-the-tidb-version-management-strategy-for-production-environment-how-to-avoid-frequent-upgrade}

現在、TiDBにはさまざまなバージョンの標準管理があります。各リリースには、詳細な変更ログと[リリースノート](/releases/release-notes.md)が含まれています。実稼働環境でアップグレードする必要があるかどうかは、アプリケーションシステムによって異なります。アップグレードする前に、以前のバージョンと新しいバージョンの機能の違いについて詳しく知ることをお勧めします。

バージョン番号の説明の例として`Release Version: v1.0.3-1-ga80e796`を取り上げます。

-   `v1.0.3`は標準GAバージョンを示します。
-   `-1`は、現在のバージョンに1つのコミットがあることを示します。
-   `ga80e796`はバージョン`git-hash`を示します。

### さまざまなTiDBマスターバージョンの違いは何ですか？ {#what-s-the-difference-between-various-tidb-master-versions}

TiDBコミュニティは非常に活発です。 1.0 GAのリリース後、エンジニアはバグの最適化と修正を続けています。したがって、TiDBバージョンは非常に高速に更新されます。最新バージョンの情報を常に入手したい場合は、 [TiDBウィークリーアップデート](https://pingcap.com/weekly/)を参照してください。

[TiUPを使用してTiDBをデプロイする](/production-deployment-using-tiup.md)に推奨されます。 TiDBは、1.0GAリリース以降のバージョン番号を統一的に管理しています。次の2つの方法を使用して、バージョン番号を表示できます。

-   `select tidb_version()`
-   `tidb-server -V`

### TiDB用のグラフィカルな展開ツールはありますか？ {#is-there-a-graphical-deployment-tool-for-tidb}

現在はありません。

### TiDBを水平方向にスケーリングする方法は？ {#how-to-scale-tidb-horizontally}

ビジネスが成長するにつれて、データベースは次の3つのボトルネックに直面する可能性があります。

-   ストレージリソースの不足。これは、ディスク容量が十分でないことを意味します。

-   CPU占有率が高いなどのコンピューティングリソースの不足。

-   書き込みと読み取りの容量が不足しています。

ビジネスの成長に合わせてTiDBを拡張できます。

-   ディスク容量が足りない場合は、TiKVノードを追加するだけで容量を増やすことができます。新しいノードが開始されると、PDはデータを他のノードから新しいノードに自動的に移行します。

-   コンピューティングリソースが十分でない場合は、TiDBノードまたはTiKVノードを追加する前に、まずCPU消費状況を確認してください。 TiDBノードが追加されると、ロードバランサーで構成できます。

-   容量が足りない場合は、TiDBノードとTiKVノードの両方を追加できます。

### Percolatorが分散ロックを使用し、クラッシュクライアントがロックを保持している場合、ロックは解放されませんか？ {#if-percolator-uses-distributed-locks-and-the-crash-client-keeps-the-lock-will-the-lock-not-be-released}

詳細については、中国語の[パーコレーターとTiDBトランザクションアルゴリズム](https://pingcap.com/blog-cn/percolator-and-txn/)を参照してください。

### TiDBがThriftの代わりにgRPCを使用するのはなぜですか？グーグルが使っているからですか？ {#why-does-tidb-use-grpc-instead-of-thrift-is-it-because-google-uses-it}

あまり。フロー制御、暗号化、ストリーミングなど、gRPCの優れた機能が必要です。

### 92は<code>like(bindo.customers.name, jason%, 92)</code>何を示していますか？ {#what-does-the-92-indicate-in-code-like-bindo-customers-name-jason-92-code}

92はエスケープ文字を示し、デフォルトではASCII92です。

### <code>information_schema.tables.data_length</code>で表示されるデータ長がTiKV監視パネルのストアサイズと異なるのはなぜですか？ {#why-does-the-data-length-shown-by-code-information-schema-tables-data-length-code-differ-from-the-store-size-on-the-tikv-monitoring-panel}

2つの理由：

-   2つの結果は異なる方法で計算されます。 `information_schema.tables.data_length`は、各行の平均の長さを計算することによる推定値です。一方、TiKV監視パネルのストアサイズは、単一のTiKVインスタンス内のデータファイル（RocksDBのSSTファイル）の長さを合計します。
-   `information_schema.tables.data_length`は論理値であり、ストアサイズは物理値です。トランザクションの複数のバージョンによって生成された冗長データは論理値に含まれませんが、冗長データは物理値のTiKVによって圧縮されます。

### トランザクションが非同期コミットまたは1フェーズコミット機能を使用しないのはなぜですか？ {#why-does-the-transaction-not-use-the-async-commit-or-the-one-phase-commit-feature}

次の状況では、システム変数を使用して[非同期コミット](/system-variables.md#tidb_enable_async_commit-new-in-v50)つの機能と[ワンフェーズコミット](/system-variables.md#tidb_enable_1pc-new-in-v50)の機能を有効にした場合でも、TiDBはこれらの機能を使用しません。

-   TiDB Binlogの実装によって制限されている、TiDB Binlogを有効にしている場合、TiDBは非同期コミットまたは1フェーズコミット機能を使用しません。
-   TiDBは、トランザクションに256以下のキーと値のペアが書き込まれ、キーの合計サイズが4 KB以下の場合にのみ、非同期コミットまたは1フェーズコミット機能を使用します。これは、書き込むデータが大量のトランザクションの場合、非同期コミットを使用してもパフォーマンスを大幅に向上させることができないためです。

## PD管理 {#pd-management}

このセクションでは、PD管理中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### PDにアクセスすると、 <code>TiKV cluster is not bootstrapped</code>というメッセージが表示されます {#the-code-tikv-cluster-is-not-bootstrapped-code-message-is-displayed-when-i-access-pd}

PDのほとんどのAPIは、TiKVクラスタが初期化されている場合にのみ使用できます。このメッセージは、新しいクラスタがデプロイされたときにTiKVが開始されていないときに、PDが開始されたときにPDにアクセスした場合に表示されます。このメッセージが表示された場合は、TiKVクラスタを起動してください。 TiKVが初期化されると、PDにアクセスできます。

### PDの開始時に<code>etcd cluster ID mismatch</code>メッセージが表示されます {#the-code-etcd-cluster-id-mismatch-code-message-is-displayed-when-starting-pd}

これは、PDスタートアップパラメータの`--initial-cluster`に、このクラスタに属していないメンバーが含まれているためです。この問題を解決するには、各メンバーの対応するクラスタを確認し、間違ったメンバーを削除してから、PDを再起動します。

### PDの時刻同期誤差の最大許容値はどれくらいですか？ {#what-s-the-maximum-tolerance-for-time-synchronization-error-of-pd}

PDは同期エラーを許容できますが、エラー値が大きいほど、PDによって割り当てられたタイムスタンプと物理時間の間のギャップが大きくなり、履歴バージョンの読み取りなどの機能に影響します。

### クライアント接続はどのようにしてPDを見つけますか？ {#how-does-the-client-connection-find-pd}

クライアント接続は、TiDBを介してのみクラスタにアクセスできます。 TiDBはPDとTiKVを接続します。 PDとTiKVはクライアントに対して透過的です。 TiDBがPDに接続すると、PDはTiDBに現在のリーダーを通知します。このPDがリーダーでない場合、TiDBはリーダーPDに再接続します。

### TiKVストアの各ステータス（アップ、切断、オフライン、ダウン、トゥームストーン）間の関係は何ですか？ {#what-is-the-relationship-between-each-status-up-disconnect-offline-down-tombstone-of-a-tikv-store}

各ステータスの関係については、 [TiKVストアの各ステータス間の関係](/tidb-scheduling.md#information-collection)を参照してください。

PD制御を使用して、TiKVストアのステータス情報を確認できます。

### PDの<code>leader-schedule-limit</code>と<code>region-schedule-limit</code>スケジューリングパラメータの違いは何ですか？ {#what-is-the-difference-between-the-code-leader-schedule-limit-code-and-code-region-schedule-limit-code-scheduling-parameters-in-pd}

-   `leader-schedule-limit`スケジューリングパラメータは、さまざまなTiKVサーバーのリーダー数のバランスを取るために使用され、クエリ処理の負荷に影響を与えます。
-   `region-schedule-limit`スケジューリングパラメータは、さまざまなTiKVサーバーのレプリカ数のバランスを取るために使用され、さまざまなノードのデータ量に影響を与えます。

### 各リージョンのレプリカの数は構成可能ですか？はいの場合、それを構成する方法は？ {#is-the-number-of-replicas-in-each-region-configurable-if-yes-how-to-configure-it}

はい。現在、更新できるのはグローバル数のレプリカのみです。初めて起動すると、PDは構成ファイル（conf / pd.yml）を読み取り、その中のmax-replicas構成を使用します。後で番号を更新する場合は、pd-ctl設定コマンド`config set max-replicas $num`を使用し、 `config show all`を使用して有効な設定を表示します。更新はアプリケーションに影響を与えず、バックグラウンドで構成されます。

TiKVインスタンスの総数が、設定したレプリカの数以上であることを常に確認してください。たとえば、3つのレプリカには少なくとも3つのTiKVインスタンスが必要です。レプリカの数を増やす前に、追加のストレージ要件を見積もる必要があります。 pd-ctlの詳細については、 [PD制御ユーザーガイド](/pd-control.md)を参照してください。

### コマンドラインクラスタ管理ツールがない場合にクラスタ全体のヘルスステータスを確認するにはどうすればよいですか？ {#how-to-check-the-health-status-of-the-whole-cluster-when-lacking-command-line-cluster-management-tools}

pd-ctlツールを使用して、クラスタの一般的なステータスを判別できます。クラスタのステータスの詳細については、モニターを使用して判別する必要があります。

### オフラインのクラスタノードの監視データを削除するにはどうすればよいですか？ {#how-to-delete-the-monitoring-data-of-a-cluster-node-that-is-offline}

オフラインノードは通常、TiKVノードを示します。オフラインプロセスがpd-ctlまたはモニターのどちらで終了したかを判別できます。ノードがオフラインになったら、次の手順を実行します。

1.  オフラインノードで関連するサービスを手動で停止します。
2.  Prometheus構成ファイルから対応するノードの`node_exporter`のデータを削除します。

## TiDBサーバー管理 {#tidb-server-management}

このセクションでは、TiDBサーバーの管理中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### TiDBで<code>lease</code>パラメータを設定するにはどうすればよいですか？ {#how-to-set-the-code-lease-code-parameter-in-tidb}

リースパラメータ（ `--lease=60` ）は、TiDBサーバーの起動時にコマンドラインから設定されます。リースパラメータの値は、現在のセッションのデータベーススキーマ変更（DDL）速度に影響を与えます。テスト環境では、テストサイクルを高速化するために値を1に設定できます。ただし、実稼働環境では、DDLの安全性を確保するために、値を分（たとえば、60）に設定することをお勧めします。

### DDL操作の処理時間はどのくらいですか？ {#what-is-the-processing-time-of-a-ddl-operation}

処理時間はシナリオによって異なります。一般に、次の3つのシナリオを検討できます。

1.  対応するデータテーブルの行数が比較的少ない`Add Index`の操作：約3秒
2.  対応するデータテーブルに比較的多数の行がある`Add Index`の操作：処理時間は、特定の行数とそのときのQPSによって異なります（ `Add Index`の操作の優先度は通常のSQL操作よりも低くなります）。
3.  その他のDDL操作：約1秒

DDL要求を受信するTiDBサーバーインスタンスが、DDL所有者がいるTiDBサーバーインスタンスと同じである場合、上記の最初と3番目のシナリオのコストは数十から数百ミリ秒にすぎない可能性があります。

### DDLステートメントの実行が非常に遅い場合があるのはなぜですか？ {#why-it-is-very-slow-to-run-ddl-statements-sometimes}

考えられる理由：

-   複数のDDLステートメントを一緒に実行すると、最後のいくつかのDDLステートメントの実行が遅くなる可能性があります。これは、DDLステートメントがTiDBクラスタでシリアルに実行されるためです。
-   クラスタを正常に開始した後、最初のDDL操作の実行に時間がかかる場合があります（通常は約30秒）。これは、TiDBクラスタがDDLステートメントを処理するリーダーを選択しているためです。
-   以下の条件を満たした場合、TiDB開始後の最初の10分間のDDLステートメントの処理時間は通常の場合よりもはるかに長くなります。1）TiDBを停止しているとき（停電の場合を含む）、TiDBは通常どおりPDと通信できません。 ）; 2）TiDBは`kill -9`コマンドで停止しているため、PDからの登録データのクリーンアップに間に合いません。この期間中にDDLステートメントを実行する場合、各DDLの状態変更のために、2 *リース（リース= 45秒）を待つ必要があります。
-   クラスタのTiDBサーバーとPDサーバーの間で通信の問題が発生した場合、TiDBサーバーはPDサーバーからバージョン情報を時間内に取得または更新できません。この場合、各DDLの状態処理のために2*リースを待つ必要があります。

### TiDBのバックエンドストレージエンジンとしてS3を使用できますか？ {#can-i-use-s3-as-the-backend-storage-engine-in-tidb}

いいえ。現在、TiDBは分散ストレージエンジンとGoleveldb / RocksDB/BoltDBエンジンのみをサポートしています。

### Information_schemaはより現実的な<code>Information_schema</code>をサポートできますか？ {#can-the-code-information-schema-code-support-more-real-information}

MySQL互換性の一部として、TiDBは多数の`INFORMATION_SCHEMA`テーブルをサポートしています。これらのテーブルの多くには、対応するSHOWコマンドもあります。詳細については、 [情報スキーマ](/information-schema/information-schema.md)を参照してください。

### TiDBバックオフタイプのシナリオの説明は何ですか？ {#what-s-the-explanation-of-the-tidb-backoff-type-scenario}

TiDBサーバーとTiKVサーバー間の通信処理では、大量のデータを処理するときに`Server is busy`または`backoff.maxsleep 20000ms`のログメッセージが表示されます。これは、TiKVサーバーがデータを処理している間、システムがビジーであるためです。このとき、通常、TiKVホストリソースの使用率が高いことがわかります。これが発生した場合は、リソースの使用量に応じてサーバーの容量を増やすことができます。

### TiDB TiClientタイプの主な理由は何ですか？ {#what-is-the-main-reason-of-tidb-ticlient-type}

TiClientリージョンエラーインジケータは、クライアントとしてのTiDBサーバーがKVインターフェイスを介してTiKVサーバーにアクセスしてデータ操作を実行するときに表示されるエラータイプとメトリックを示します。エラータイプには`not_leader`と`stale_epoch`が含まれます。これらのエラーは、TiDBサーバーが自身のキャッシュ情報に従ってリージョンリーダーデータを操作する場合、リージョンリーダーが移行した場合、または現在のTiKVリージョン情報とTiDBキャッシュのルーティング情報に一貫性がない場合に発生します。通常、この場合、TiDBサーバーはPDから最新のルーティングデータを自動的に取得し、前の操作をやり直します。

### TiDBがサポートする同時接続の最大数はいくつですか？ {#what-s-the-maximum-number-of-concurrent-connections-that-tidb-supports}

デフォルトでは、TiDBサーバーあたりの最大接続数に制限はありません。同時実行性が大きすぎると応答時間が長くなる場合は、TiDBノードを追加して容量を増やすことをお勧めします。

### テーブルの作成時間を表示するにはどうすればよいですか？ {#how-to-view-the-creation-time-of-a-table}

`information_schema`のテーブルの`create_time`つが作成時間です。

### TiDBログの<code>EXPENSIVE_QUERY</code>の意味は何ですか？ {#what-is-the-meaning-of-code-expensive-query-code-in-the-tidb-log}

TiDBがSQLステートメントを実行しているとき、各演算子が10,000を超える行を処理すると推定される場合、クエリは`EXPENSIVE_QUERY`になります。 `tidb-server`構成パラメーターを変更してしきい値を調整してから、 `tidb-server`を再起動できます。

### TiDBのテーブルのサイズを見積もるにはどうすればよいですか？ {#how-do-i-estimate-the-size-of-a-table-in-tidb}

TiDBのテーブルのサイズを見積もるには、次のクエリステートメントを使用できます。

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

上記のステートメントを使用する場合は、ステートメントの次のフィールドに必要に応じて入力して置き換える必要があります。

-   `@dbname` ：データベースの名前。
-   `@table_name` ：ターゲットテーブルの名前。

さらに、上記のステートメントでは：

-   `store_size_amplification`は、クラスタ圧縮率の平均を示します。 `SELECT * FROM METRICS_SCHEMA.store_size_amplification;`を使用してこの情報を照会することに加えて、 **GrafanaMonitoringPD-統計バランス**パネルで各ノードの<strong>サイズ増幅</strong>メトリックを確認することもできます。クラスタ圧縮率の平均は、すべてのノードのサイズ増幅の平均です。
-   `Approximate_Size`は、圧縮前のレプリカ内のテーブルのサイズを示します。これは概算値であり、正確な値ではないことに注意してください。
-   `Disk_Size`は、圧縮後のテーブルのサイズを示します。これは概算値であり、 `Approximate_Size`と`store_size_amplification`に従って計算できます。

## TiKVサーバー管理 {#tikv-server-management}

このセクションでは、TiKVサーバーの管理中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### TiKVクラスタのレプリカの推奨数はいくつですか？高可用性のために最小数を維持する方が良いですか？ {#what-is-the-recommended-number-of-replicas-in-the-tikv-cluster-is-it-better-to-keep-the-minimum-number-for-high-availability}

テスト環境には、リージョンごとに3つのレプリカで十分です。ただし、実稼働シナリオでは、3ノード未満のTiKVクラスタを操作しないでください。インフラストラクチャ、ワークロード、および復元力のニーズに応じて、この数を増やすことをお勧めします。コピーが高いほどパフォーマンスは低下しますが、セキュリティは高くなることに注意してください。

### TiKVの起動時に、 <code>cluster ID mismatch</code>メッセージが表示されます {#the-code-cluster-id-mismatch-code-message-is-displayed-when-starting-tikv}

これは、ローカルTiKVに格納されているクラスタIDがPDで指定されているクラスタIDと異なるためです。新しいPDクラスタが展開されると、PDはランダムなクラスタIDを生成します。 TiKVはPDからクラスタIDを取得し、初期化時にクラスタIDをローカルに保存します。次回TiKVが起動すると、ローカルクラスタIDとPDのクラスタIDがチェックされます。クラスタIDが一致しない場合は、 `cluster ID mismatch`メッセージが表示され、TiKVが終了します。

以前にPDクラスタをデプロイした後、PDデータを削除して新しいPDクラスタをデプロイした場合、TiKVが古いデータを使用して新しいPDクラスタに接続するため、このエラーが発生します。

### TiKVを起動すると、 <code>duplicated store address</code>メッセージが表示されます {#the-code-duplicated-store-address-code-message-is-displayed-when-starting-tikv}

これは、スタートアップパラメータのアドレスが他のTiKVによってPDクラスタに登録されているためです。このエラーの原因となる一般的な条件：TiKV `--data-dir`で指定されたパスにデータフォルダーがありません（削除または移動後に更新--data-dirがありません）、前のパラメーターでTiKVを再起動してください.pd-ctlの[ストア削除](https://github.com/pingcap/pd/tree/55db505e8f35e8ab4e00efd202beb27a8ecc40fb/tools/pd-ctl#store-delete--label--weight-store_id----jqquery-string)の機能を試してください。前のストアを削除してから、TiKVを再起動します。

### TiKVプライマリノードとセカンダリノードは同じ圧縮アルゴリズムを使用していますが、結果が異なるのはなぜですか？ {#tikv-primary-node-and-secondary-node-use-the-same-compression-algorithm-why-the-results-are-different}

現在、TiKVプライマリノードの一部のファイルの圧縮率は高く、これは基盤となるデータ分散とRocksDBの実装によって異なります。データサイズが時々変動するのは正常です。基盤となるストレージエンジンは、必要に応じてデータを調整します。

### TiKVブロックキャッシュの機能は何ですか？ {#what-are-the-features-of-tikv-block-cache}

TiKVは、RocksDBの列ファミリー（CF）機能を実装しています。デフォルトでは、KVデータは最終的にRocksDB内の3つのCF（デフォルト、書き込み、ロック）に保存されます。

-   デフォルトのCFは実際のデータを格納し、対応するパラメーターは`[rocksdb.defaultcf]`にあります。
-   書き込みCFは、データバージョン情報（MVCC）とインデックス関連データを格納し、対応するパラメータは`[rocksdb.writecf]`にあります。
-   ロックCFはロック情報を保存し、システムはデフォルトパラメータを使用します。
-   RaftRocksDBインスタンスはRaftログを保存します。デフォルトのCFは主にRaftログを格納し、対応するパラメーターは`[raftdb.defaultcf]`にあります。
-   すべてのCFには、データブロックをキャッシュし、RocksDBの読み取り速度を向上させるための共有ブロックキャッシュがあります。ブロックキャッシュのサイズは、 `block-cache-size`パラメーターによって制御されます。パラメータの値が大きいほど、より多くのホットデータをキャッシュでき、読み取り操作に適しています。同時に、より多くのシステムメモリを消費します。
-   各CFには個別の書き込みバッファーがあり、サイズは`write-buffer-size`パラメーターによって制御されます。

### TiKVチャネルがいっぱいになるのはなぜですか？ {#why-is-the-tikv-channel-full}

-   Raftstoreスレッドが遅すぎるか、I/Oによってブロックされています。 RaftstoreのCPU使用状況を確認できます。
-   TiKVはビジー状態（CPU、ディスクI / Oなど）であり、処理できません。

### TiKVがリージョンリーダーを頻繁に切り替えるのはなぜですか？ {#why-does-tikv-frequently-switch-region-leader}

-   ネットワークの問題により、ノード間の通信が停止します。レポート障害の監視を確認できます。
-   元のメインリーダーのノードがスタックしているため、時間内にフォロワーに連絡できません。
-   Raftstoreスレッドがスタックしました。

### ノードがダウンした場合、サービスは影響を受けますか？はいの場合、どのくらいですか？ {#if-a-node-is-down-will-the-service-be-affected-if-yes-how-long}

TiKVは、Raftを使用して、複数のレプリカ間でデータを複製します（デフォルトでは、リージョンごとに3つのレプリカ）。 1つのレプリカで問題が発生した場合、他のレプリカでデータの安全性を保証できます。 Raftプロトコルに基づいて、ノードがダウンしたときに1つのリーダーに障害が発生した場合、最大2 *のリース時間（リース時間は10秒）の後、別のノードのフォロワーがすぐにリージョンリーダーとして選出されます。

### 高いI/O、メモリ、CPUを使用し、パラメータ構成を超えるTiKVシナリオは何ですか？ {#what-are-the-tikv-scenarios-that-take-up-high-i-o-memory-cpu-and-exceed-the-parameter-configuration}

TiKVで大量のデータを読み書きすると、高いI / O、メモリ、およびCPUが消費されます。非常に複雑なクエリを実行すると、大きな中間結果セットを生成するシナリオなど、多くのメモリとCPUリソースが消費されます。

### TiKVはSAS/SATAディスクまたはSSD/SASディスクの混合展開をサポートしていますか？ {#does-tikv-support-sas-sata-disks-or-mixed-deployment-of-ssd-sas-disks}

いいえ。OLTPシナリオの場合、TiDBはデータアクセスと操作のために高I/Oディスクを必要とします。一貫性の高い分散データベースとして、TiDBには、レプリカレプリケーションや最下層ストレージの圧縮などの書き込み増幅機能があります。したがって、TiDBのベストプラクティスでは、ストレージディスクとしてNVMeSSDを使用することをお勧めします。 TiKVとPDの混合展開はサポートされていません。

### キーデータテーブルの範囲は、データアクセスの前に分割されていますか？ {#is-the-range-of-the-key-data-table-divided-before-data-access}

いいえ。MySQLのテーブル分割ルールとは異なります。 TiKVでは、テーブルRangeはRegionのサイズに基づいて動的に分割されます。

### リージョンはどのように分割されますか？ {#how-does-region-split}

リージョンは事前に分割されていませんが、リージョン分割メカニズムに従います。リージョンサイズが`region-max-size`つまたは`region-max-keys`のパラメーターの値を超えると、分割がトリガーされます。分割後、情報はPDに報告されます。

### TiKVには、データのセキュリティを保証するために、MySQLのような<code>innodb_flush_log_trx_commit</code>パラメーターがありますか？ {#does-tikv-have-the-code-innodb-flush-log-trx-commit-code-parameter-like-mysql-to-guarantee-the-security-of-data}

はい。現在、スタンドアロンストレージエンジンは2つのRocksDBインスタンスを使用しています。 1つのインスタンスは、raft-logを格納するために使用されます。 TiKVの`sync-log`パラメーターがtrueに設定されている場合、各コミットは強制的にraft-logにフラッシュされます。クラッシュが発生した場合は、raft-logを使用してKVデータを復元できます。

### SSD、RAIDレベル、RAIDカードのキャッシュ戦略、NUMA構成、ファイルシステム、オペレーティングシステムのI / Oスケジューリング戦略など、WALストレージに推奨されるサーバー構成は何ですか？ {#what-is-the-recommended-server-configuration-for-wal-storage-such-as-ssd-raid-level-cache-strategy-of-raid-card-numa-configuration-file-system-i-o-scheduling-strategy-of-the-operating-system}

WALは順序付き書き込みに属しており、現在、独自の構成を適用していません。推奨される構成は次のとおりです。

-   SSD
-   RAID10を推奨
-   RAIDカードのキャッシュ戦略とオペレーティングシステムのI/Oスケジューリング戦略：現在、特定のベストプラクティスはありません。 Linux7以降ではデフォルト構成を使用できます
-   NUMA：具体的な提案はありません。メモリ割り当て戦略には、 `interleave = all`を使用できます
-   ファイルシステム：ext4

### 最も厳密なデータ使用可能モード（ <code>sync-log = true</code> ）での書き込みパフォーマンスはどうですか？ {#how-is-the-write-performance-in-the-most-strict-data-available-mode-code-sync-log-true-code}

一般に、 `sync-log`を有効にすると、パフォーマンスが約30％低下します。 `sync-log`が`false`に設定されている場合の書き込みパフォーマンスについては、 [Sysbenchを使用したTiDBのパフォーマンステスト結果](/benchmark/v3.0-performance-benchmarking-with-sysbench.md)を参照してください。

### Raft + TiKVアーキテクチャの複数のレプリカは、絶対的なデータの安全性を実現できますか？最も厳密なモード（ <code>sync-log = true</code> ）をスタンドアロンストレージに適用する必要がありますか？ {#can-raft-multiple-replicas-in-the-tikv-architecture-achieve-absolute-data-safety-is-it-necessary-to-apply-the-most-strict-mode-code-sync-log-true-code-to-a-standalone-storage}

[いかだコンセンサスアルゴリズム](https://raft.github.io/)を使用してTiKVノード間でデータが冗長に複製され、ノード障害が発生した場合の回復可能性が確保されます。データがレプリカの50％以上に書き込まれた場合にのみ、アプリケーションはACK（3つのノードのうち2つ）を返します。ただし、理論的には、2つのノードがクラッシュする可能性があります。したがって、データの安全性に関する要件はそれほど厳しくなく、パフォーマンスに関する要件が極端なシナリオを除いて、 `sync-log`モードを有効にすることを強くお勧めします。

`sync-log`を使用する代わりに、Raftグループに3つではなく5つのレプリカを用意することを検討することもできます。これにより、データの安全性を維持しながら、2つのレプリカの障害が発生する可能性があります。

スタンドアロンのTiKVノードの場合でも、 `sync-log`モードを有効にすることをお勧めします。そうしないと、ノードに障害が発生した場合に最後の書き込みが失われる可能性があります。

### TiKVはRaftプロトコルを使用するため、データの書き込み中に複数のネットワークラウンドトリップが発生します。実際の書き込み遅延はどれくらいですか？ {#since-tikv-uses-the-raft-protocol-multiple-network-roundtrips-occur-during-data-writing-what-is-the-actual-write-delay}

理論的には、TiDBには、スタンドアロンデータベースよりも4回多いネットワークラウンドトリップの書き込み遅延があります。

### TiDBには、KVインターフェイスを直接使用でき、独立したキャッシュを必要としないMySQLのようなInnoDB memcachedプラグインがありますか？ {#does-tidb-have-an-innodb-memcached-plugin-like-mysql-which-can-directly-use-the-kv-interface-and-does-not-need-the-independent-cache}

TiKVは、インターフェイスの個別の呼び出しをサポートしています。理論的には、インスタンスをキャッシュとして使用できます。 TiDBは分散リレーショナルデータベースであるため、TiKVを個別にサポートすることはありません。

### コプロセッサーコンポーネントは何に使用されますか？ {#what-is-the-coprocessor-component-used-for}

-   TiDBとTiKV間のデータ伝送を削減します
-   TiKVの分散コンピューティングリソースを最大限に活用して、コンピューティングプッシュダウンを実行します。

### エラーメッセージ<code>IO error: No space left on device While appending to file</code>が表示されます {#the-error-message-code-io-error-no-space-left-on-device-while-appending-to-file-code-is-displayed}

これは、ディスク容量が不足しているためです。ノードを追加するか、ディスク容量を増やす必要があります。

### TiKVでOOM（メモリ不足）エラーが頻繁に発生するのはなぜですか？ {#why-does-the-oom-out-of-memory-error-occur-frequently-in-tikv}

TiKVのメモリ使用量は、主にRocksDBのブロックキャッシュから発生します。これは、デフォルトでシステムメモリサイズの40％です。 TiKVでOOMエラーが頻繁に発生する場合は、 `block-cache-size`の値が高すぎるかどうかを確認する必要があります。さらに、複数のTiKVインスタンスが単一のマシンにデプロイされている場合、複数のインスタンスがOOMエラーを引き起こすシステムメモリを使いすぎないように、パラメータを明示的に設定する必要があります。

### TiDBデータとRawKVデータの両方を同じTiKVクラスタに保存できますか？ {#can-both-tidb-data-and-rawkv-data-be-stored-in-the-same-tikv-cluster}

いいえ。TiDB（またはトランザクションAPIから作成されたデータ）は特定のキー形式に依存しています。 RawKV APIから作成されたデータ（または他のRawKVベースのサービスからのデータ）とは互換性がありません。

## TiDBテスト {#tidb-testing}

このセクションでは、TiDBテスト中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### Sysbenchを使用したTiDBのパフォーマンステストの結果は何ですか？ {#what-is-the-performance-test-result-for-tidb-using-sysbench}

最初は、多くのユーザーがベンチマークテストまたはTiDBとMySQLの比較テストを行う傾向があります。同様の公式テストを実施しましたが、テストデータには多少の偏りがありますが、テスト結果は全体的に一貫していることがわかりました。 TiDBのアーキテクチャはMySQLとは大きく異なるため、ベンチマークポイントを見つけるのは困難です。提案は次のとおりです。

-   ベンチマークテストに時間をかけすぎないでください。 TiDBを使用するシナリオの違いにもっと注意を払ってください。
-   [Sysbenchを使用したTiDBのパフォーマンステスト結果](/benchmark/v3.0-performance-benchmarking-with-sysbench.md)を参照してください。

### TiDBクラスタ容量（QPS）とノード数の関係は何ですか？ TiDBはMySQLとどのように比較されますか？ {#what-s-the-relationship-between-the-tidb-cluster-capacity-qps-and-the-number-of-nodes-how-does-tidb-compare-to-mysql}

-   10ノード内では、TiDB書き込み容量（TPSの挿入）とノード数の関係は約40％直線的に増加します。 MySQLはシングルノード書き込みを使用するため、その書き込み容量をスケーリングすることはできません。
-   MySQLでは、セカンダリデータベースを追加することで読み取り容量を増やすことができますが、多くの問題があるシャーディングを使用しない限り、書き込み容量を増やすことはできません。
-   TiDBでは、ノードを追加することで、読み取りと書き込みの両方の容量を簡単に増やすことができます。

### DBAによるMySQLとTiDBのパフォーマンステストは、スタンドアロンTiDBのパフォーマンスがMySQLほど良くないことを示しています {#the-performance-test-of-mysql-and-tidb-by-our-dba-shows-that-the-performance-of-a-standalone-tidb-is-not-as-good-as-mysql}

TiDBは、MySQLスタンドアロンの容量が制限されているためにシャーディングが使用され、強力な一貫性と完全な分散トランザクションが必要なシナリオ向けに設計されています。 TiDBの利点の1つは、同時コンピューティングを実行するためにコンピューティングをストレージノードにプッシュダウンすることです。

TiDBは、小さなサイズのデータと限られたリージョンでは同時実行性の強さを示すことができないため、小さなサイズ（1,000万レベル未満など）のテーブルには適していません。典型的な例は、数行のレコードが頻繁に更新されるカウンターテーブルです。 TiDBでは、これらの行はストレージエンジンでいくつかのキーと値のペアになり、単一のノードにあるリージョンに落ち着きます。 TiDBからTiKVへの強力な一貫性と操作を保証するためのバックグラウンドレプリケーションのオーバーヘッドにより、MySQLスタンドアロンよりもパフォーマンスが低下します。

## バックアップと復元 {#backup-and-restoration}

このセクションでは、バックアップと復元中に発生する可能性のある一般的な問題、その原因、および解決策について説明します。

### TiDBでデータをバックアップする方法は？ {#how-to-back-up-data-in-tidb}

現在、大量のデータ（1 TBを超える）のバックアップには、 [BR](/br/backup-and-restore-tool.md)を使用する方法が推奨されます。それ以外の場合、推奨されるツールは[Dumpling](/dumpling-overview.md)です。公式のMySQLツール`mysqldump`はデータのバックアップと復元のためにTiDBでもサポートされていますが、そのパフォーマンスは[BR](/br/backup-and-restore-tool.md)よりも悪く、大量のデータのバックアップと復元にははるかに長い時間が必要です。

BRに関するその他のFAQについては、 [BRのよくある質問](/br/backup-and-restore-faq.md)を参照してください。
