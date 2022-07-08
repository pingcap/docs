---
title: TiDB 6.0.0 Release Notes
---

# TiDB6.0.0リリースノート {#tidb-6-0-0-release-notes}

発売日：2022年4月7日

TiDBバージョン：6.0.0-DMR

6.0.0-DMRでは、主な新機能または改善点は次のとおりです。

-   SQLで配置ルールをサポートして、データ配置のより柔軟な管理を提供します。
-   カーネルレベルでデータとインデックスの間に整合性チェックを追加します。これにより、システムの安定性と堅牢性が向上し、リソースのオーバーヘッドが非常に低くなります。
-   非専門家向けのセルフサービスのデータベースパフォーマンス監視および診断機能であるTop SQLを提供します。
-   クラスタのパフォーマンスデータを常に収集する継続的なプロファイリングをサポートし、技術専門家のMTTRを削減します。
-   ホットスポットの小さなテーブルをメモリにキャッシュします。これにより、アクセスパフォーマンスが大幅に向上し、スループットが向上し、アクセスの待ち時間が短縮されます。
-   インメモリの悲観的ロックを最適化します。ペシミスティックロックによって引き起こされるパフォーマンスのボトルネックの下で、ペシミスティックロックのメモリ最適化により、レイテンシを10％削減し、QPSを10％向上させることができます。
-   プリペアドステートメントを拡張して実行プランを共有します。これにより、CPUリソースの消費が減り、SQLの実行効率が向上します。
-   より多くの式のプッシュダウンとエラスティックスレッドプールの一般的な可用性（GA）をサポートすることにより、MPPエンジンのコンピューティングパフォーマンスを向上させます。
-   DM WebUIを追加して、多数の移行タスクの管理を容易にします。
-   大規模なクラスターでデータを複製する際のTiCDCの安定性と効率を向上させます。 TiCDCは、100,000テーブルの同時複製をサポートするようになりました。
-   TiKVノードを再起動した後、リーダーのバランシングを加速します。これにより、再起動後のビジネス回復の速度が向上します。
-   統計の自動更新のキャンセルをサポートします。これにより、リソースの競合が減少し、SQLパフォーマンスへの影響が制限されます。
-   TiDBクラスターの自動診断サービスであるPingCAPクリニックを提供します（テクニカルプレビューバージョン）。
-   エンタープライズレベルのデータベース管理プラットフォームであるTiDBEnterpriseManagerを提供します。

また、TiDBのHTAPソリューションのコアコンポーネントとして、 <sup>TiFlashTM</sup>はこのリリースで正式にオープンソースになっています。詳細については、 [TiFlashリポジトリ](https://github.com/pingcap/tiflash)を参照してください。

## リリース戦略の変更 {#release-strategy-changes}

TiDB v6.0.0以降、TiDBは次の2種類のリリースを提供します。

-   長期サポートリリース

    ロングタームサポート（LTS）リリースは、約6か月ごとにリリースされます。 LTSリリースでは、新機能と改善点が導入され、リリースライフサイクル内でパッチリリースが受け入れられます。たとえば、v6.1.0はLTSリリースになります。

-   開発マイルストーンリリース

    開発マイルストーンリリース（DMR）は、約2か月ごとにリリースされます。 DMRは新機能と改善点を導入しますが、パッチリリースは受け入れません。オンプレミスユーザーが実稼働環境でDMRを使用することはお勧めしません。たとえば、v6.0.0-DMRはDMRです。

TiDB v6.0.0はDMRであり、そのバージョンは6.0.0-DMRです。

## 新機能 {#new-features}

### SQL {#sql}

-   データのSQLベースの配置ルール

    TiDBは、優れたスケーラビリティを備えた分散データベースです。通常、データは複数のサーバーまたは複数のデータセンターに展開されます。したがって、データスケジューリング管理は、TiDBの最も重要な基本機能の1つです。ほとんどの場合、ユーザーはデータのスケジュールと管理の方法を気にする必要はありません。ただし、アプリケーションの複雑さが増すにつれて、分離とアクセス遅延によって引き起こされる展開の変更は、TiDBにとって新たな課題になっています。 v6.0.0以降、TiDBはSQLインターフェイスに基づくデータのスケジューリングおよび管理機能を公式に提供します。レプリカ数、役割の種類、データの配置場所などのディメンションでの柔軟なスケジューリングと管理をサポートします。 TiDBは、マルチサービス共有クラスターおよびクロスAZ展開でのデータ配置のより柔軟な管理もサポートします。

    [ユーザードキュメント](/placement-rules-in-sql.md)

-   データベースによるTiFlashレプリカの構築をサポートします。データベース内のすべてのテーブルにTiFlashレプリカを追加するには、単一のSQLステートメントを使用するだけで済み、運用と保守のコストを大幅に節約できます。

    [ユーザードキュメント](/tiflash/create-tiflash-replicas.md#create-tiflash-replicas-for-databases)

### 取引 {#transaction}

-   カーネルレベルでのデータインデックスの整合性のチェックを追加します

    トランザクションの実行時にデータインデックスの整合性のチェックを追加します。これにより、システムの安定性と堅牢性が向上し、リソースのオーバーヘッドが非常に低くなります。 `tidb_enable_mutation_checker`変数と`tidb_txn_assertion_level`変数を使用して、チェックの動作を制御できます。デフォルト構成では、ほとんどのシナリオでQPSドロップは2％以内に制御されます。整合性チェックのエラーの説明については、 [ユーザードキュメント](/troubleshoot-data-inconsistency-errors.md)を参照してください。

### 可観測性 {#observability}

-   Top SQL：非専門家向けのパフォーマンス診断

    Top SQLは、DBAおよびアプリ開発者向けのTiDBダッシュボードのセルフサービスデータベースパフォーマンス監視および診断機能であり、現在TiDBv6.0で一般的に利用可能です。

    専門家向けの既存の診断機能とは異なり、 Top SQLは非専門家向けに設計されています。相関関係を見つけたり、Raftスナップショット、RocksDB、MVCC、TSOなどのTiDB内部メカニズムを理解したりするために、何千もの監視チャートをトラバースする必要はありません。Top SQLを使用してデータベースの負荷をすばやく分析し、アプリのパフォーマンスを向上させるには、基本的なデータベースの知識（インデックス、ロックの競合、実行プランなど）のみが必要です。

    Top SQLはデフォルトでは有効になっていません。有効にすると、 Top SQLは各TiKVまたはTiDBノードのリアルタイムCPU負荷を提供します。したがって、CPU負荷の高いSQLステートメントを一目見ただけで、データベースのホットスポットや突然の負荷の増加などの問題をすばやく分析できます。たとえば、 Top SQLを使用して、単一のTiKVノードの90％のCPUを消費する異常なクエリを特定して診断できます。

    [ユーザードキュメント](/dashboard/top-sql.md)

-   継続的なプロファイリングをサポートする

    TiDBダッシュボードには、継続的プロファイリング機能が導入されています。この機能は、TiDBv6.0で一般的に利用可能になりました。連続プロファイリングはデフォルトでは有効になっていません。有効にすると、個々のTiDB、TiKV、およびPDインスタンスのパフォーマンスデータが常に収集され、オーバーヘッドはごくわずかです。履歴パフォーマンスデータを使用すると、技術専門家は、問題の再現が困難な場合でも、メモリ消費量が多いなどの問題の根本原因をさかのぼって特定できます。このようにして、平均修復時間（MTTR）を短縮できます。

    [ユーザードキュメント](/dashboard/continuous-profiling.md)

### パフォーマンス {#performance}

-   ホットスポットの小さなテーブルをキャッシュする

    ホットスポットの小さなテーブルにアクセスするシナリオのユーザーアプリケーションの場合、TiDBはホットスポットテーブルをメモリに明示的にキャッシュすることをサポートします。これにより、アクセスパフォーマンスが大幅に向上し、スループットが向上し、アクセスの待ち時間が短縮されます。このソリューションは、サードパーティのキャッシュミドルウェアの導入を効果的に回避し、アーキテクチャの複雑さを軽減し、運用と保守のコストを削減できます。このソリューションは、構成テーブルや為替レートテーブルなど、小さなテーブルが頻繁にアクセスされるが更新されることはめったにないシナリオに適しています。

    [ユーザードキュメント](/cached-tables.md) [＃25293](https://github.com/pingcap/tidb/issues/25293)

-   インメモリ悲観的ロック

    TiDB v6.0.0以降、メモリ内のペシミスティックロックはデフォルトで有効になっています。この機能を有効にすると、悲観的なトランザクションロックがメモリで管理されます。これにより、ペシミスティックロックの永続化とロック情報のRaftレプリケーションが回避され、ペシミスティックトランザクションロックの管理のオーバーヘッドが大幅に削減されます。ペシミスティックロックによって引き起こされるパフォーマンスのボトルネックの下で、ペシミスティックロックのメモリ最適化により、レイテンシを10％削減し、QPSを10％向上させることができます。

    [ユーザードキュメント](/pessimistic-transaction.md#in-memory-pessimistic-lock) [＃11452](https://github.com/tikv/tikv/issues/11452)

-   読み取りコミット分離レベルでTSOを取得するための最適化

    クエリの待ち時間を短縮するために、読み取りと書き込みの競合がまれな場合、TiDBは[コミットされた分離レベルを読み取る](/transaction-isolation-levels.md#read-committed-isolation-level)に`tidb_rc_read_check_ts`のシステム変数を追加して、不要なTSOを減らします。この変数はデフォルトで無効になっています。変数が有効になっている場合、この最適化によりTSOの重複が回避され、読み取りと書き込みの競合がないシナリオでの遅延が減少します。ただし、読み取りと書き込みの競合が頻繁に発生するシナリオでは、この変数を有効にするとパフォーマンスが低下する可能性があります。

    [ユーザードキュメント](/transaction-isolation-levels.md#read-committed-isolation-level) [＃33159](https://github.com/pingcap/tidb/issues/33159)

-   実行計画を共有するために準備されたステートメントを強化する

    SQL実行プランを再利用すると、SQLステートメントの解析時間を効果的に短縮し、CPUリソースの消費を減らし、SQLの実行効率を向上させることができます。 SQLチューニングの重要な方法の1つは、SQL実行プランを効果的に再利用することです。 TiDBは、プリペアドステートメントとの実行プランの共有をサポートしています。ただし、プリペアドステートメントが閉じられると、TiDBは対応するプランキャッシュを自動的にクリアします。その後、TiDBは繰り返されるSQLステートメントを不必要に解析し、実行効率に影響を与える可能性があります。 v6.0.0以降、TiDBは、 `tidb_ignore_prepared_cache_close_stmt`パラメーター（デフォルトでは無効）を介して`COM_STMT_CLOSE`コマンドを無視するかどうかの制御をサポートしています。パラメータが有効になっている場合、TiDBはプリペアドステートメントを閉じるコマンドを無視し、実行プランをキャッシュに保持して、実行プランの再利用率を向上させます。

    [ユーザードキュメント](/sql-prepared-plan-cache.md#ignore-the-com_stmt_close-command-and-the-deallocate-prepare-statement) [＃31056](https://github.com/pingcap/tidb/issues/31056)

-   クエリプッシュダウンを改善する

    コンピューティングをストレージから分離するネイティブアーキテクチャにより、TiDBは演算子をプッシュダウンすることで無効なデータを除外することをサポートします。これにより、TiDBとTiKV間のデータ転送が大幅に削減され、クエリの効率が向上します。 v6.0.0では、TiDBはより多くの式と`BIT`のデータ型をTiKVにプッシュダウンすることをサポートし、式とデータ型を計算する際のクエリ効率を向上させます。

    [ユーザードキュメント](/functions-and-operators/expressions-pushed-down.md#add-to-the-blocklist) [＃30738](https://github.com/pingcap/tidb/issues/30738)

-   ホットスポットインデックスの最適化

    単調に増加するデータをバッチでセカンダリインデックスに書き込むと、インデックスのホットスポットが発生し、全体的な書き込みスループットに影響します。 v6.0.0以降、TiDBは、書き込みパフォーマンスを向上させるために`tidb_shard`関数を使用したインデックスホットスポットの分散をサポートしています。現在、 `tidb_shard`は一意のセカンダリインデックスにのみ有効です。このアプリケーションフレンドリーなソリューションでは、元のクエリ条件を変更する必要はありません。このソリューションは、高い書き込みスループット、ポイントクエリ、およびバッチポイントクエリのシナリオで使用できます。アプリケーションで範囲クエリによって分散されたデータを使用すると、パフォーマンスが低下する可能性があることに注意してください。したがって、このような場合は確認せずにこの機能を使用しないでください。

    [ユーザードキュメント](/functions-and-operators/tidb-functions.md#tidb_shard) [＃31040](https://github.com/pingcap/tidb/issues/31040)

-   TiFlash MPPエンジンのパーティションテーブルの動的プルーニングモードをサポート（実験的）

    このモードでは、TiDBはTiFlashのMPPエンジンを使用してパーティションテーブルのデータを読み取り、計算できます。これにより、パーティションテーブルのクエリパフォーマンスが大幅に向上します。

    [ユーザードキュメント](/tiflash/use-tiflash-mpp-mode.md#access-partitioned-tables-in-the-mpp-mode)

-   MPPエンジンのコンピューティングパフォーマンスを向上させる

    -   より多くの関数と演算子をMPPエンジンにプッシュダウンすることをサポート

        -   `IS NOT`関数： `IS`
        -   文字列`NOT REGEXP()` ： `REGEXP()`
        -   数学`LEAST(int/real)` ： `GREATEST(int/real)`
        -   `DAYOFYEAR()` `LAST_DAY()` `MONTHNAME()` `DAYNAME()` `DAYOFMONTH()` `DAYOFWEEK()`
        -   演算子：反左外側半結合、左外側半結合

        [ユーザードキュメント](/tiflash/tiflash-supported-pushdown-calculations.md)

    -   エラスティックスレッドプール（デフォルトで有効）はGAになります。この機能は、CPU使用率を向上させることを目的としています。

        [ユーザードキュメント](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)

### 安定 {#stability}

-   実行計画のベースラインキャプチャを強化する

    テーブル名、頻度、ユーザー名などのディメンションを持つブロックリストを追加することにより、実行プランのベースラインキャプチャの使いやすさを向上させます。バインディングをキャッシュするためのメモリ管理を最適化するための新しいアルゴリズムを導入します。ベースラインキャプチャを有効にすると、システムはほとんどのOLTPクエリのバインディングを自動的に作成します。バインドされたステートメントの実行プランが修正され、実行プランの変更によるパフォーマンスの問題が回避されます。ベースラインキャプチャは、メジャーバージョンのアップグレードやクラスタの移行などのシナリオに適用でき、実行プランのリグレッションによって引き起こされるパフォーマンスの問題を軽減するのに役立ちます。

    [ユーザードキュメント](/sql-plan-management.md#baseline-capturing) [＃32466](https://github.com/pingcap/tidb/issues/32466)

-   TiKVクォータリミッターをサポート（実験的）

    TiKVを使用してデプロイされたマシンのリソースが限られており、フォアグラウンドに大量のリクエストが発生している場合、バックグラウンドCPUリソースがフォアグラウンドによって占有され、TiKVのパフォーマンスが不安定になります。 TiDB v6.0.0では、クォータ関連の構成アイテムを使用して、CPUや読み取り/書き込み帯域幅など、フォアグラウンドで使用されるリソースを制限できます。これにより、長期間の重いワークロードでのクラスターの安定性が大幅に向上します。

    [ユーザードキュメント](/tikv-configuration-file.md#quota) [＃12131](https://github.com/tikv/tikv/issues/12131)

-   TiFlashでzstd圧縮アルゴリズムをサポートする

    TiFlashには、 `profiles.default.dt_compression_method`と`profiles.default.dt_compression_level`の2つのパラメーターが導入されており、ユーザーはパフォーマンスと容量のバランスに基づいて最適な圧縮アルゴリズムを選択できます。

    [ユーザードキュメント](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)

-   デフォルトですべてのI/Oチェック（チェックサム）を有効にする

    この機能は、v5.4.0で実験的ものとして導入されました。ユーザーのビジネスに明らかな影響を与えることなく、データの精度とセキュリティを強化します。

    警告：新しいバージョンのデータ形式は、v5.4.0より前のバージョンにダウングレードすることはできません。このようなダウングレード中は、TiFlashレプリカを削除し、ダウングレード後にデータを複製する必要があります。または、 [dttoolの移行](/tiflash/tiflash-command-line-flags.md#dttool-migrate)を参照してダウングレードを実行することもできます。

    [ユーザードキュメント](/tiflash/tiflash-data-validation.md)

-   スレッドの使用率を向上させる

    TiFlashは、非同期gRPCおよびMin-TSOスケジューリングメカニズムを導入しています。このようなメカニズムは、スレッドのより効率的な使用を保証し、過剰なスレッドによって引き起こされるシステムクラッシュを回避します。

    [ユーザードキュメント](/tiflash/monitor-tiflash.md#coprocessor)

### データ移行 {#data-migration}

#### TiDBデータ移行（DM） {#tidb-data-migration-dm}

-   WebUIを追加する（実験的）

    WebUIを使用すると、多数の移行タスクを簡単に管理できます。 WebUIでは、次のことができます。

    -   ダッシュボードで移行タスクを表示する
    -   移行タスクを管理する
    -   アップストリーム設定を構成する
    -   レプリケーションステータスのクエリ
    -   マスターとワーカーの情報を表示する

    WebUIはまだ実験的段階であり、開発中です。したがって、試用のみをお勧めします。既知の問題は、WebUIとdmctlを使用して同じタスクを操作すると問題が発生する可能性があることです。この問題は、以降のバージョンで解決される予定です。

    [ユーザードキュメント](/dm/dm-webui-guide.md)

-   エラー処理メカニズムを追加する

    移行タスクを中断する問題に対処するために、より多くのコマンドが導入されています。例えば：

    -   スキーマエラーが発生した場合は、スキーマファイルを個別に編集する代わりに、 `binlog-schema update`コマンドの`--from-source/--from-target`パラメーターを使用してスキーマファイルを更新できます。
    -   binlogの位置を指定して、DDLステートメントを挿入、置換、スキップ、または元に戻すことができます。

    [ユーザードキュメント](/dm/dm-manage-schema.md)

-   AmazonS3への完全なデータストレージをサポートする

    DMがすべてまたは完全なデータ移行タスクを実行する場合、アップストリームからの完全なデータを格納するために十分なハードディスク容量が必要です。 EBSと比較して、AmazonS3は低コストでほぼ無限のストレージを備えています。現在、DMはAmazonS3をダンプディレクトリとして設定することをサポートしています。つまり、すべてまたは完全なデータ移行タスクを実行するときに、S3を使用して完全なデータを保存できます。

    [ユーザードキュメント](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)

-   指定された時間からの移行タスクの開始をサポート

    新しいパラメーター`--start-time`が移行タスクに追加されます。時刻は「2021-10-2100：01：00」または「2021-10-21T00：01：00」の形式で定義できます。

    この機能は、シャードmysqlインスタンスからインクリメンタルデータを移行およびマージするシナリオで特に役立ちます。具体的には、増分移行タスクで各ソースにbinlog開始点を設定する必要はありません。代わりに、 `safe-mode`の`--start-time`パラメーターを使用して、増分移行タスクをすばやく作成できます。

    [ユーザードキュメント](/dm/dm-create-task.md#flags-description)

#### TiDB Lightning {#tidb-lightning}

-   許容可能なエラーの最大数の構成をサポート

    構成アイテム`lightning.max-error`を追加しました。デフォルト値は0です。値が0より大きい場合、最大エラー機能が有効になります。エンコード中に行でエラーが発生した場合、この行を含むレコードがターゲットTiDBの`lightning_task_info.type_error_v1`に追加され、この行は無視されます。エラーのある行がしきい値を超えると、TiDBLightningはすぐに終了します。

    `lightning.max-error`の構成と一致して、 `lightning.task-info-schema-name`の構成項目は、データ保存エラーを報告するデータベースの名前を記録します。

    この機能は、すべてのタイプのエラーを網羅しているわけではありません。たとえば、構文エラーは適用されません。

    [ユーザードキュメント](/tidb-lightning/tidb-lightning-error-resolution.md#type-error)

### TiDBデータ共有サブスクリプション {#tidb-data-share-subscription}

-   100,000テーブルの同時複製をサポート

    TiCDCは、データ処理フローを最適化することにより、各テーブルの増分データを処理するためのリソース消費を削減します。これにより、大規模なクラスターでデータを複製する際の複製の安定性と効率が大幅に向上します。内部テストの結果は、TiCDCが100,000テーブルの同時複製を安定してサポートできることを示しています。

### 展開とメンテナンス {#deployment-and-maintenance}

-   デフォルトで新しい照合順序ルールを有効にする

    v4.0以降、TiDBは、大文字と小文字を区別しない、アクセントを区別しない、およびパディングルールでMySQLと同じように動作する新しい照合順序ルールをサポートしています。新しい照合順序ルールは、デフォルトで無効になっている`new_collations_enabled_on_first_bootstrap`パラメーターによって制御されます。 v6.0以降、TiDBはデフォルトで新しい照合順序ルールを有効にします。この構成は、TiDBクラスタの初期化時にのみ有効になることに注意してください。

    [ユーザードキュメント](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)

-   TiKVノードを再起動した後、リーダーのバランシングを加速します

    TiKVノードの再起動後、負荷分散のために、不均一に分散したリーダーを再分散する必要があります。大規模なクラスターでは、リーダーのバランシング時間はリージョンの数と正の相関があります。たとえば、100Kリージョンのリーダーバランシングには20〜30分かかる場合があります。これは、不均一な負荷によるパフォーマンスの問題や安定性のリスクが発生しやすい傾向があります。 TiDB v6.0.0は、バランシングの同時実行性を制御するパラメータを提供し、デフォルト値を元の値の4倍に拡大します。これにより、リーダーのリバランシング時間が大幅に短縮され、TiKVノードの再起動後のビジネス回復が加速されます。

    [ユーザードキュメント](/pd-control.md#scheduler-config-balance-leader-scheduler) [＃4610](https://github.com/tikv/pd/issues/4610)

-   統計の自動更新のキャンセルをサポート

    統計は、SQLのパフォーマンスに影響を与える最も重要な基本データの1つです。統計の完全性と適時性を確保するために、TiDBはバックグラウンドでオブジェクト統計を定期的に自動的に更新します。ただし、統計の自動更新によりリソースの競合が発生し、SQLのパフォーマンスに影響を与える可能性があります。この問題に対処するために、v6.0以降の統計の自動更新を手動でキャンセルできます。

    [ユーザードキュメント](/statistics.md#automatic-update)

-   PingCAPクリニック診断サービス（テクニカルプレビュー版）

    PingCAPクリニックはTiDBクラスターの診断サービスです。このサービスは、クラスタの問題をリモートでトラブルシューティングするのに役立ち、クラスタのステータスをローカルですばやく確認できます。 PingCAPクリニックを使用すると、TiDBクラスタのライフサイクル全体での安定した動作を保証し、潜在的な問題を予測し、問題の可能性を減らし、クラスタの問題を迅速にトラブルシューティングできます。

    クラスタの問題をトラブルシューティングするためのリモートアシスタンスについてPingCAPテクニカルサポートに連絡する場合、 PingCAPクリニックサービスを使用して診断データを収集およびアップロードできるため、トラブルシューティングの効率が向上します。

    [ユーザードキュメント](/clinic/clinic-introduction.md)

-   エンタープライズレベルのデータベース管理プラットフォーム、TiDB Enterprise Manager

    TiDB Enterprise Manager（TiEM）は、TiDBデータベースに基づくエンタープライズレベルのデータベース管理プラットフォームであり、ユーザーがオンプレミスまたはパブリッククラウド環境でTiDBクラスターを管理できるようにすることを目的としています。

    TiEMは、TiDBクラスターの完全なライフサイクルビジュアル管理を提供するだけでなく、パラメーター管理、バージョンアップグレード、クラスタクローン、アクティブスタンバイクラスタスイッチング、データのインポートとエクスポート、データレプリケーション、およびデータのバックアップと復元のサービスなどのワンストップサービスも提供します。 TiEMは、TiDB上のDevOpsの効率を改善し、企業のDevOpsコストを削減できます。

    現在、TiEMは[TiDBエンタープライズ](https://en.pingcap.com/tidb-enterprise/)エディションでのみ提供されています。 TiEMを入手するには、 [TiDBエンタープライズ](https://en.pingcap.com/tidb-enterprise/)ページからお問い合わせください。

-   監視コンポーネントの構成のカスタマイズをサポート

    TiUPを使用してTiDBクラスタをデプロイすると、TiUPはPrometheus、Grafana、Alertmanagerなどのモニタリングコンポーネントを自動的にデプロイし、スケールアウト後に新しいノードをモニタリングスコープに自動的に追加します。 `topology.yaml`のファイルに構成項目を追加することにより、監視コンポーネントの構成をカスタマイズできます。

    [ユーザードキュメント](/tiup/customized-montior-in-tiup-environment.md)

## 互換性の変更 {#compatibility-changes}

> **ノート：**
>
> 以前のTiDBバージョンからv6.0.0にアップグレードするときに、すべての中間バージョンの互換性変更に関する注意事項を知りたい場合は、対応するバージョンの[リリースノート](/releases/release-notes.md)を確認できます。

### システム変数 {#system-variables}

| 変数名                                                                                                                                                                                       | タイプを変更する   | 説明                                                                                                                                                                                                                                                                                                       |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `placement_checks`                                                                                                                                                                        | 削除         | DDLステートメントが[SQLの配置ルール](/placement-rules-in-sql.md)で指定された配置ルールを検証するかどうかを制御します。 `tidb_placement_mode`に置き換えられました。                                                                                                                                                                                           |
| `tidb_enable_alter_placement`                                                                                                                                                             | 削除         | [SQLの配置ルール](/placement-rules-in-sql.md)を有効にするかどうかを制御します。                                                                                                                                                                                                                                                 |
| `tidb_mem_quota_hashjoin`<br/>`tidb_mem_quota_indexlookupjoin`<br/>`tidb_mem_quota_indexlookupreader` <br/>`tidb_mem_quota_mergejoin`<br/>`tidb_mem_quota_sort`<br/>`tidb_mem_quota_topn` | 削除         | v5.0以降、これらの変数は`tidb_mem_quota_query`に置き換えられ、 [システム変数](/system-variables.md)ドキュメントから削除されました。互換性を確保するために、これらの変数はソースコードに保持されていました。 TiDB 6.0.0以降、これらの変数もコードから削除されています。                                                                                                                                       |
| [`tidb_enable_mutation_checker`](/system-variables.md#tidb_enable_mutation_checker-new-in-v600)                                                                                           | 新しく追加されました | ミューテーションチェッカーを有効にするかどうかを制御します。デフォルト値は`ON`です。 v6.0.0より前のバージョンからアップグレードする既存のクラスターの場合、ミューテーションチェッカーはデフォルトで無効になっています。                                                                                                                                                                                        |
| [`tidb_ignore_prepared_cache_close_stmt`](/system-variables.md#tidb_ignore_prepared_cache_close_stmt-new-in-v600)                                                                         | 新しく追加されました | プリペアドステートメントを閉じるコマンドを無視するかどうかを制御します。デフォルト値は`OFF`です。                                                                                                                                                                                                                                                      |
| [`tidb_mem_quota_binding_cache`](/system-variables.md#tidb_mem_quota_binding_cache-new-in-v600)                                                                                           | 新しく追加されました | `binding`を保持するキャッシュのメモリ使用量のしきい値を設定します。デフォルト値は`67108864` （64 MiB）です。                                                                                                                                                                                                                                      |
| [`tidb_placement_mode`](/system-variables.md#tidb_placement_mode-new-in-v600)                                                                                                             | 新しく追加されました | DDLステートメントが[SQLの配置ルール](/placement-rules-in-sql.md)で指定された配置ルールを無視するかどうかを制御します。デフォルト値は`strict`です。これは、DDLステートメントが配置規則を無視しないことを意味します。                                                                                                                                                                        |
| [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600)                                                                                                         | 新しく追加されました | <li>トランザクション内の読み取りステートメントの待機時間を最適化します。読み取り/書き込みの競合がより深刻な場合、この変数をオンにすると、オーバーヘッドと遅延が追加され、パフォーマンスが低下します。デフォルト値は`off`です。</li><li>この変数はまだ[レプリカ読み取り](/system-variables.md#tidb_replica_read-new-in-v40)と互換性がありません。読み取り要求で`tidb_rc_read_check_ts`がオンになっている場合、レプリカ読み取りを使用できない可能性があります。両方の変数を同時にオンにしないでください。</li> |
| [`tidb_sysdate_is_now`](/system-variables.md#tidb_sysdate_is_now-new-in-v600)                                                                                                             | 新しく追加されました | `SYSDATE`関数を`NOW`関数に置き換えることができるかどうかを制御します。この構成アイテムは、MySQLオプション[`sysdate-is-now`](https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_sysdate-is-now)と同じ効果があります。デフォルト値は`OFF`です。                                                                                                     |
| [`tidb_table_cache_lease`](/system-variables.md#tidb_table_cache_lease-new-in-v600)                                                                                                       | 新しく追加されました | [テーブルキャッシュ](/cached-tables.md)のリース時間を秒単位で制御します。デフォルト値は`3`です。                                                                                                                                                                                                                                             |
| [`tidb_top_sql_max_meta_count`](/system-variables.md#tidb_top_sql_max_meta_count-new-in-v600)                                                                                             | 新しく追加されました | 1分あたり[Top SQL](/dashboard/top-sql.md)ずつ収集されるSQLステートメントタイプの最大数を制御します。デフォルト値は`5000`です。                                                                                                                                                                                                                     |
| [`tidb_top_sql_max_time_series_count`](/system-variables.md#tidb_top_sql_max_time_series_count-new-in-v600)                                                                               | 新しく追加されました | 負荷に最も寄与するSQLステートメント（つまり、上位N）の数を1分あたり[Top SQL](/dashboard/top-sql.md)回記録できるかどうかを制御します。デフォルト値は`100`です。                                                                                                                                                                                                     |
| [`tidb_txn_assertion_level`](/system-variables.md#tidb_txn_assertion_level-new-in-v600)                                                                                                   | 新しく追加されました | アサーションレベルを制御します。アサーションは、データとインデックス間の整合性チェックであり、書き込まれているキーがトランザクションコミットプロセスに存在するかどうかをチェックします。デフォルトでは、チェックによりほとんどのチェック項目が有効になり、パフォーマンスにほとんど影響を与えません。 v6.0.0より前のバージョンからアップグレードする既存のクラスターの場合、チェックはデフォルトで無効になっています。                                                                                           |

### Configuration / コンフィグレーションファイルのパラメーター {#configuration-file-parameters}

| Configuration / コンフィグレーションファイル | Configuration / コンフィグレーション                                                                                                                                                                                       | タイプを変更する   | 説明                                                                                                                                                                                                                                                                                                         |
| :----------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB                           | `stmt-summary.enable` <br/> `stmt-summary.enable-internal-query` <br/> `stmt-summary.history-size` <br/> `stmt-summary.max-sql-length` <br/> `stmt-summary.max-stmt-count` <br/> `stmt-summary.refresh-interval` | 削除         | [ステートメント要約表](/statement-summary-tables.md)に関連するConfiguration / コンフィグレーション。これらの構成アイテムはすべて削除されます。ステートメントサマリーテーブルを制御するには、SQL変数を使用する必要があります。                                                                                                                                                                   |
| TiDB                           | [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)                                                                                             | 変更         | 新しい照合順序のサポートを有効にするかどうかを制御します。 v6.0以降、デフォルト値は`false`から`true`に変更されています。この構成項目は、クラスタが初めて初期化されたときにのみ有効になります。最初のブートストラップの後、この構成アイテムを使用して新しい照合順序フレームワークを有効または無効にすることはできません。                                                                                                                                      |
| TiKV                           | [`backup.num-threads`](/tikv-configuration-file.md#num-threads-1)                                                                                                                                                | 変更         | 値の範囲が`[1, CPU]`に変更されます。                                                                                                                                                                                                                                                                                    |
| TiKV                           | [`raftstore.apply-max-batch-size`](/tikv-configuration-file.md#apply-max-batch-size)                                                                                                                             | 変更         | 最大値が`10240`に変更されます。                                                                                                                                                                                                                                                                                        |
| TiKV                           | [`raftstore.raft-max-size-per-msg`](/tikv-configuration-file.md#raft-max-size-per-msg)                                                                                                                           | 変更         | <li>最小値が`0`から`0`より大きい値に変更されます。</li><li>最大値は`3GB`に設定されています。</li><li>単位が`MB`から`KB\|MB\|GB`に変更されます。</li>                                                                                                                                                                                                      |
| TiKV                           | [`raftstore.store-max-batch-size`](/tikv-configuration-file.md#store-max-batch-size)                                                                                                                             | 変更         | 最大値は`10240`に設定されます。                                                                                                                                                                                                                                                                                        |
| TiKV                           | [`readpool.unified.max-thread-count`](/tikv-configuration-file.md#max-thread-count)                                                                                                                              | 変更         | 調整可能範囲が`[min-thread-count, MAX(4, CPU)]`に変更されます。                                                                                                                                                                                                                                                           |
| TiKV                           | [`rocksdb.enable-pipelined-write`](/tikv-configuration-file.md#enable-pipelined-write)                                                                                                                           | 変更         | デフォルト値は`true`から`false`に変更されます。この構成を有効にすると、以前のパイプライン書き込みが使用されます。この構成を無効にすると、新しいパイプラインコミットメカニズムが使用されます。                                                                                                                                                                                                      |
| TiKV                           | [`rocksdb.max-background-flushes`](/tikv-configuration-file.md#max-background-flushes)                                                                                                                           | 変更         | <li>CPUコアの数が10の場合、デフォルト値は`3`です。</li><li> CPUコアの数が8の場合、デフォルト値は`2`です。</li>                                                                                                                                                                                                                                   |
| TiKV                           | [`rocksdb.max-background-jobs`](/tikv-configuration-file.md#max-background-jobs)                                                                                                                                 | 変更         | <li>CPUコアの数が10の場合、デフォルト値は`9`です。</li><li> CPUコアの数が8の場合、デフォルト値は`7`です。</li>                                                                                                                                                                                                                                   |
| TiFlash                        | [`profiles.default.dt_enable_logical_split`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                                                                                                   | 変更         | DeltaTreeStorageEngineのセグメントが論理分割を使用するかどうかを決定します。デフォルト値は`true`から`false`に変更されます。                                                                                                                                                                                                                            |
| TiFlash                        | [`profiles.default.enable_elastic_threadpool`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                                                                                                 | 変更         | エラスティックスレッドプールを有効にするかどうかを制御します。デフォルト値は`false`から`true`に変更されます。                                                                                                                                                                                                                                              |
| TiFlash                        | [`storage.format_version`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                                                                                                                     | 変更         | TiFlashのデータ検証機能を制御します。デフォルト値は`2`から`3`に変更されます。<br/> `format_version`が`3`に設定されている場合、ハードウェア障害による誤った読み取りを回避するために、すべてのTiFlashデータの読み取り操作で整合性チェックが実行されます。<br/>新しい形式のバージョンをv5.4より前のバージョンにダウングレードすることはできないことに注意してください。                                                                                              |
| TiDB                           | [`pessimistic-txn.pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600)                                                                                                     | 新しく追加されました | 悲観的トランザクションモードがグローバルに有効になっている場合に自動コミットトランザクションが使用するトランザクションモードを決定します（ `tidb_txn_mode='pessimistic'` ）。                                                                                                                                                                                                     |
| TiKV                           | [`pessimistic-txn.in-memory`](/tikv-configuration-file.md#in-memory-new-in-v600)                                                                                                                                 | 新しく追加されました | メモリ内のペシミスティックロックを有効にするかどうかを制御します。この機能を有効にすると、ペシミスティックトランザクションは、ペシミスティックロックをディスクに書き込んだり、他のレプリカに複製したりする代わりに、ペシミスティックロックを可能な限りTiKVメモリに保存します。これにより、悲観的なトランザクションのパフォーマンスが向上します。ただし、ペシミスティックロックが失われる可能性は低く、ペシミスティックトランザクションのコミットに失敗する可能性があります。デフォルト値は`true`です。                                                   |
| TiKV                           | [`quota`](/tikv-configuration-file.md#quota)                                                                                                                                                                     | 新しく追加されました | フロントエンドリクエストが占めるリソースを制限するクォータリミッターに関連する構成アイテムを追加します。クォータリミッターは実験的機能であり、デフォルトでは無効になっています。新しい`max-delay-duration`関連の構成アイテムは、 `foreground-cpu-time` 、および`foreground-read-bandwidth` `foreground-write-bandwidth` 。                                                                                            |
| TiFlash                        | [`profiles.default.dt_compression_method`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                                                                                                     | 新しく追加されました | TiFlashの圧縮アルゴリズムを指定します。オプションの値は`LZ4` 、および`zstd`で、すべて大文字と小文字は区別され`LZ4HC`ん。デフォルト値は`LZ4`です。                                                                                                                                                                                                                   |
| TiFlash                        | [`profiles.default.dt_compression_level`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                                                                                                      | 新しく追加されました | TiFlashの圧縮レベルを指定します。デフォルト値は`1`です。                                                                                                                                                                                                                                                                          |
| DM                             | [`loaders.&#x3C;name>.import-mode`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                                                                                               | 新しく追加されました | フルインポートフェーズ中のインポートモード。 v6.0以降、DMはTiDB LightningのTiDBバックエンドモードを使用して、完全なインポートフェーズ中にデータをインポートします。以前のローダーコンポーネントは使用されなくなりました。これは内部交換であり、日常業務に明らかな影響はありません。<br/>デフォルト値は`sql`に設定されています。これは、 `tidb-backend`モードを使用することを意味します。まれに、 `tidb-backend`が完全に互換性がない場合があります。このパラメーターを`loader`に構成することにより、ローダーモードにフォールバックできます。 |
| DM                             | [`loaders.&#x3C;name>.on-duplicate`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                                                                                              | 新しく追加されました | フルインポートフェーズ中に競合を解決する方法を指定します。デフォルト値は`replace`です。これは、新しいデータを使用して既存のデータを置き換えることを意味します。                                                                                                                                                                                                                       |
| TiCDC                          | [`dial-timeout`](/ticdc/manage-ticdc.md#configure-sink-uri-with-kafka)                                                                                                                                           | 新しく追加されました | ダウンストリームKafkaとの接続を確立する際のタイムアウト。デフォルト値は`10s`です。                                                                                                                                                                                                                                                             |
| TiCDC                          | [`read-timeout`](/ticdc/manage-ticdc.md#configure-sink-uri-with-kafka)                                                                                                                                           | 新しく追加されました | ダウンストリームのKafkaから返される応答を取得する際のタイムアウト。デフォルト値は`10s`です。                                                                                                                                                                                                                                                        |
| TiCDC                          | [`write-timeout`](/ticdc/manage-ticdc.md#configure-sink-uri-with-kafka)                                                                                                                                          | 新しく追加されました | ダウンストリームKafkaにリクエストを送信する際のタイムアウト。デフォルト値は`10s`です。                                                                                                                                                                                                                                                           |

### その他 {#others}

-   データ配置ポリシーには、次の互換性の変更があります。
    -   バインディングはサポートされていません。直接配置オプションは構文から削除されます。
    -   `CREATE PLACEMENT POLICY`および`ALTER PLACEMENT POLICY`ステートメントは、 `VOTERS`および`VOTER_CONSTRAINTS`配置オプションをサポートしなくなりました。
    -   TiDB移行ツール（TiDB Binlog、TiCDC、およびBR）は、配置ルールと互換性があります。配置オプションは、TiDBBinlogの特別なコメントに移動されます。
    -   `information_schema.placement_rules`システムテーブルの名前が`information_schema.placement_policies`に変更されます。このテーブルには、配置ポリシーに関する情報のみが表示されるようになりました。
    -   `placement_checks`システム変数は`tidb_placement_mode`に置き換えられます。
    -   TiFlashレプリカを持つテーブルに配置ルールのあるパーティションを追加することは禁止されています。
    -   `INFORMATION_SCHEMA`のテーブルから`TIDB_DIRECT_PLACEMENT`の列を削除します。
-   SQL計画管理（SPM）バインディングの`status`の値が変更されました。
    -   `using`を削除します。
    -   `enabled` （使用可能）を追加して`using`を置き換えます。
    -   `disabled`を追加します（使用不可）。
-   DMはOpenAPIインターフェースを変更します
    -   内部メカニズムの変更により、タスク管理に関連するインターフェースは以前の実験的バージョンと互換性がありません。適応のために新しい[DMOpenAPIドキュメント](/dm/dm-open-api.md)を参照する必要があります。
-   DMは、完全なインポートフェーズ中に競合を解決するためにメソッドを変更します
    -   `loader.<name>.on-duplicate`つのパラメータが追加されます。デフォルト値は`replace`です。これは、新しいデータを使用して既存のデータを置き換えることを意味します。以前の動作を維持したい場合は、値を`error`に設定できます。このパラメーターは、完全なインポートフェーズ中の動作のみを制御します。
-   DMを使用するには、対応するバージョンの`dmctl`を使用する必要があります
    -   内部メカニズムの変更により、DMをv6.0.0にアップグレードした後、 `dmctl`もv6.0.0にアップグレードする必要があります。
-   v5.4（v5.4のみ）では、TiDBは一部のnoopシステム変数に誤った値を許可します。 v6.0.0以降、TiDBはシステム変数に誤った値を設定することを許可していません。 [＃31538](https://github.com/pingcap/tidb/issues/31538)

## 改善 {#improvements}

-   TiDB

    -   `FLASHBACK`または`RECOVER`ステートメントを使用してテーブルを復元した後、テーブルの配置ルール設定を自動的にクリアします[＃31668](https://github.com/pingcap/tidb/issues/31668)
    -   パフォーマンス概要ダッシュボードを追加して、一般的なクリティカルパスのコアパフォーマンスメトリックを表示し、TiDBでのメトリック分析を容易にします[＃31676](https://github.com/pingcap/tidb/issues/31676)
    -   `LOAD DATA LOCAL INFILE`ステートメント[＃24515](https://github.com/pingcap/tidb/issues/24515)での`REPLACE`キーワードの使用のサポート
    -   Rangeパーティションテーブル[＃26739](https://github.com/pingcap/tidb/issues/26739)の組み込み`IN`式のパーティションプルーニングをサポートします。
    -   MPP集計クエリで冗長になる可能性のあるExchange操作を排除することにより、クエリの効率を向上させます[＃31762](https://github.com/pingcap/tidb/issues/31762)
    -   `TRUNCATE PARTITION`ステートメントと`DROP PARTITION`ステートメントで重複するパーティション名を許可することでMySQLとの互換性を向上させます[＃31681](https://github.com/pingcap/tidb/issues/31681)
    -   `ADMIN SHOW DDL JOBS`ステートメント[＃23494](https://github.com/pingcap/tidb/issues/23494)の結果に`CREATE_TIME`情報を表示することをサポートします。
    -   新しい組み込み関数をサポートする`CHARSET()` [＃3931](https://github.com/pingcap/tidb/issues/3931)
    -   ユーザー名によるベースラインキャプチャブロックリストのフィルタリングをサポート[＃32558](https://github.com/pingcap/tidb/issues/32558)
    -   ベースラインキャプチャブロックリストでのワイルドカードの使用のサポート[＃32714](https://github.com/pingcap/tidb/issues/32714)
    -   現在の[＃26642](https://github.com/pingcap/tidb/issues/26642)に従って時間を表示することにより、 `ADMIN SHOW DDL JOBS`および`SHOW TABLE STATUS`ステートメントの結果を最適化し`time_zone` 。
    -   `DAYNAME()`および`MONTHNAME()`機能の[＃32594](https://github.com/pingcap/tidb/issues/32594)へのプッシュダウンをサポート
    -   `REGEXP`機能を[＃32637](https://github.com/pingcap/tidb/issues/32637)にプッシュダウンすることをサポート
    -   `DAYOFMONTH()`および`LAST_DAY()`機能の[＃33012](https://github.com/pingcap/tidb/issues/33012)へのプッシュダウンをサポート
    -   `DAYOFWEEK()`および`DAYOFYEAR()`機能の[＃33130](https://github.com/pingcap/tidb/issues/33130)へのプッシュダウンをサポート
    -   `IS_TRUE` 、および`IS_FALSE`関数の`IS_TRUE_WITH_NULL`へのプッシュダウンを[＃33047](https://github.com/pingcap/tidb/issues/33047)
    -   `GREATEST`および`LEAST`機能の[＃32787](https://github.com/pingcap/tidb/issues/32787)へのプッシュダウンをサポート
    -   `UnionScan`オペレーター[＃32631](https://github.com/pingcap/tidb/issues/32631)の実行の追跡をサポート
    -   `_tidb_rowid`列[＃31543](https://github.com/pingcap/tidb/issues/31543)を読み取るクエリでのPointGetプランの使用をサポートする
    -   名前を小文字の[＃32719](https://github.com/pingcap/tidb/issues/32719)に変換せずに、 `EXPLAIN`ステートメントの出力に元のパーティション名を表示することをサポート
    -   IN条件および文字列型列でのRANGECOLUMNSパーティショニングのパーティションプルーニングを有効にする[＃32626](https://github.com/pingcap/tidb/issues/32626)
    -   システム変数がNULLに設定されている場合、エラーメッセージを返します[＃32850](https://github.com/pingcap/tidb/issues/32850)
    -   非MPPモードからブロードキャスト参加を削除する[＃31465](https://github.com/pingcap/tidb/issues/31465)
    -   動的プルーニング・モード[＃32347](https://github.com/pingcap/tidb/issues/32347)でのパーティション表でのMPPプランの実行をサポートします。
    -   Common Table Expression（CTE）の述部のプッシュダウンをサポート[＃28163](https://github.com/pingcap/tidb/issues/28163)
    -   `Statement Summary`と`Capture Plan Baselines`の構成を単純化して、グローバルベースでのみ利用できるようにします[＃30557](https://github.com/pingcap/tidb/issues/30557)
    -   gopsutilをv3.21.12に更新して、 [＃31607](https://github.com/pingcap/tidb/issues/31607)でバイナリをビルドするときに報告されるアラームに対処します。

-   TiKV

    -   多くのキー範囲を持つバッチのRaftstoreのサンプリング精度を向上させます[＃12327](https://github.com/tikv/tikv/issues/12327)
    -   プロファイルをより簡単に識別できるように、 `debug/pprof/profile`に正しい「Content-Type」を追加します[＃11521](https://github.com/tikv/tikv/issues/11521)
    -   Raftstoreにハートビートがある場合、または読み取り要求を処理する場合に、リーダーのリース時間を無限に更新します。これにより、遅延ジッターを減らすことができます[＃11579](https://github.com/tikv/tikv/issues/11579)
    -   リーダーを切り替える際のコストが最も少ないストアを選択してください。これにより、パフォーマンスの安定性が向上します[＃10602](https://github.com/tikv/tikv/issues/10602)
    -   Raftストアをブロックすることによって引き起こされるパフォーマンスジッターを減らすために、Raftログを非同期的にフェッチします[＃11320](https://github.com/tikv/tikv/issues/11320)
    -   ベクトル計算[＃5751](https://github.com/tikv/tikv/issues/5751)で`QUARTER`関数をサポートします
    -   `BIT`データ型の[＃30738](https://github.com/pingcap/tidb/issues/30738)へのプッシュダウンをサポート
    -   `MOD`機能と`SYSDATE`機能の[＃11916](https://github.com/tikv/tikv/issues/11916)へのプッシュダウンをサポート
    -   ロックの解決ステップ[＃11993](https://github.com/tikv/tikv/issues/11993)を必要とするリージョンの数を減らすことにより、TiCDCの回復時間を短縮します。
    -   動的変更の[＃11865](https://github.com/tikv/tikv/issues/11865) `raftstore.raft-max-inflight-msgs`
    -   動的プルーニングモード[＃11888](https://github.com/tikv/tikv/issues/11888)を有効にするためのサポート`EXTRA_PHYSICAL_TABLE_ID_COL_ID`
    -   バケット[＃11759](https://github.com/tikv/tikv/issues/11759)での計算をサポート
    -   [＃11965](https://github.com/tikv/tikv/issues/11965)のキーを`user-key` + `memcomparable-padding` +57としてエンコードし`timestamp`
    -   [＃11965](https://github.com/tikv/tikv/issues/11965)の値を`user-value` + `ttl` + `ValueMeta`としてエンコードし、911で`delete`をエンコードし`ValueMeta` 。
    -   動的変更の[＃12017](https://github.com/tikv/tikv/issues/12017) `raftstore.raft-max-size-per-msg`
    -   Grafana1でのマルチ[＃12014](https://github.com/tikv/tikv/issues/12014)のモニタリングをサポート
    -   リーダーシップをCDCオブザーバーに移して、レイテンシージッターを減らす[＃12111](https://github.com/tikv/tikv/issues/12111)
    -   `raftstore.apply_max_batch_size`および`raftstore.store_max_batch_size`の動的変更を[＃11982](https://github.com/tikv/tikv/issues/11982)
    -   RawKV V2は、 `raw_get`つまたは`raw_scan`のリクエストを受信すると最新バージョンを返します[＃11965](https://github.com/tikv/tikv/issues/11965)
    -   RCCheckTS整合性読み取り[＃12097](https://github.com/tikv/tikv/issues/12097)をサポートする
    -   動的変更のサポート`storage.scheduler-worker-pool-size` （スケジューラープールのスレッド数） [＃12067](https://github.com/tikv/tikv/issues/12067)
    -   グローバルフォアグラウンドフローコントローラーを使用してCPUと帯域幅の使用を制御し、TiKV1のパフォーマンスの安定性を向上させ[＃11855](https://github.com/tikv/tikv/issues/11855)
    -   動的変更のサポート`readpool.unified.max-thread-count` （UnifyReadPoolのスレッド数） [＃11781](https://github.com/tikv/tikv/issues/11781)
    -   TiKV内部パイプラインを使用してRocksDBパイプラインを置き換え、 `rocksdb.enable-multibatch-write`パラメーター[＃12059](https://github.com/tikv/tikv/issues/12059)を廃止します

-   PD

    -   リーダーを追い出すときに転送する最速のオブジェクトを自動的に選択することをサポートします。これにより、追い出しプロセスがスピードアップします[＃4229](https://github.com/tikv/pd/issues/4229)
    -   地域が利用できなくなった場合に備えて、2レプリカのいかだグループから投票者を削除することを禁止する[＃4564](https://github.com/tikv/pd/issues/4564)
    -   バランスリーダーのスケジューリングをスピードアップ[＃4652](https://github.com/tikv/pd/issues/4652)

-   TiFlash

    -   TiFlashファイルの論理分割を禁止し（デフォルト値の`profiles.default.dt_enable_logical_split`から`false`を調整します。詳細は[ユーザードキュメント](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters)を参照）、TiFlash列型ストレージのスペース使用効率を改善して、TiFlashに同期されたテーブルのスペース占有がスペースと同じになるようにします。 TiKVのテーブルの占有
    -   以前のクラスタ管理モジュールをTiDBに統合することにより、TiFlashのクラスタ管理とレプリカ複製メカニズムを最適化します。これにより、小さなテーブルのレプリカ作成が高速化されます[＃29924](https://github.com/pingcap/tidb/issues/29924) 。

-   ツール

    -   バックアップと復元（BR）

        -   バックアップデータの復元速度を向上させます。 BRが16TBのデータを15ノード（各ノードに16個のCPUコアがある）のTiKVクラスタに復元するシミュレーションテストでは、スループットは2.66 GiB/sに達します。 [＃27036](https://github.com/pingcap/tidb/issues/27036)

        -   配置ルールのインポートとエクスポートをサポートします。データをインポートするときに配置ルールを無視するかどうかを制御する`--with-tidb-placement-mode`つのパラメーターを追加します。 [＃32290](https://github.com/pingcap/tidb/issues/32290)

    -   TiCDC

        -   Grafana3に`Lag analyze`のパネルを追加し[＃4891](https://github.com/pingcap/tiflow/issues/4891)
        -   配置ルールのサポート[＃4846](https://github.com/pingcap/tiflow/issues/4846)
        -   HTTPAPI処理の同期[＃1710](https://github.com/pingcap/tiflow/issues/1710)
        -   チェンジフィードを再開するための指数バックオフメカニズムを追加する[＃3329](https://github.com/pingcap/tiflow/issues/3329)
        -   MySQLシンクのデフォルトの分離レベルを読み取りコミットに設定して、 [＃3589](https://github.com/pingcap/tiflow/issues/3589)のデッドロックを減らします。
        -   作成時にチェンジフィードパラメータを検証し、エラーメッセージを調整します[＃1716](https://github.com/pingcap/tiflow/issues/1716) [＃1718](https://github.com/pingcap/tiflow/issues/1718) [＃1719](https://github.com/pingcap/tiflow/issues/1719) [＃4472](https://github.com/pingcap/tiflow/issues/4472)
        -   Kafkaプロデューサーの構成パラメーターを公開して、 [＃4385](https://github.com/pingcap/tiflow/issues/4385)で構成可能にします。

    -   TiDBデータ移行（DM）

        -   アップストリームテーブルスキーマに一貫性がなく、オプティミスティックモードである場合のタスクの開始をサポートする[＃3629](https://github.com/pingcap/tiflow/issues/3629) [＃3708](https://github.com/pingcap/tiflow/issues/3708) [＃3786](https://github.com/pingcap/tiflow/issues/3786)
        -   `stopped`状態でのタスクの作成をサポート[＃4484](https://github.com/pingcap/tiflow/issues/4484)
        -   `/tmp`ではなくDM-workerの作業ディレクトリを使用して内部ファイルを書き込み、タスクの停止後にディレクトリをクリーンアップするSyncerをサポートします[＃4107](https://github.com/pingcap/tiflow/issues/4107)
        -   事前チェックが改善されました。一部の重要なチェックがスキップされなくなりました。 [＃3608](https://github.com/pingcap/tiflow/issues/3608)

    -   TiDB Lightning

        -   再試行可能なエラータイプをさらに追加する[＃31376](https://github.com/pingcap/tidb/issues/31376)
        -   base64形式のパスワード文字列[＃31194](https://github.com/pingcap/tidb/issues/31194)をサポートします
        -   エラーコードとエラー出力を標準化する[＃32239](https://github.com/pingcap/tidb/issues/32239)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `SCHEDULE = majority_in_primary` 、および`PrimaryRegion`の値が同じである場合に`Regions`が配置ルールを使用してテーブルを作成できないバグを修正します[＃31271](https://github.com/pingcap/tidb/issues/31271)
    -   インデックスルックアップ結合[＃30468](https://github.com/pingcap/tidb/issues/30468)を使用してクエリを実行するときの`invalid transaction`のエラーを修正しました
    -   2つ以上の特権が付与されたときに`show grants`が誤った結果を返すバグを修正します[＃30855](https://github.com/pingcap/tidb/issues/30855)
    -   `INSERT INTO t1 SET timestamp_col = DEFAULT`がデフォルトで[＃29926](https://github.com/pingcap/tidb/issues/29926)に設定されたフィールドのタイムスタンプをゼロタイムスタンプに設定するバグを修正し`CURRENT_TIMESTAMP` 。
    -   文字列タイプ[＃31721](https://github.com/pingcap/tidb/issues/31721)の最大値と最小の非null値のエンコードを回避することにより、結果の読み取りで報告されたエラーを修正します
    -   エスケープ文字[＃31589](https://github.com/pingcap/tidb/issues/31589)でデータが壊れた場合のデータのロードパニックを修正
    -   照合順序を伴う`greatest`または`least`関数が間違った結果を取得する問題を修正します[＃31789](https://github.com/pingcap/tidb/issues/31789)
    -   date_add関数とdate_sub関数が誤ったデータ型を返す可能性があるバグを修正します[＃31809](https://github.com/pingcap/tidb/issues/31809)
    -   挿入ステートメントを使用して仮想的に生成された列にデータを挿入するときに発生する可能性のあるパニックを修正[＃31735](https://github.com/pingcap/tidb/issues/31735)
    -   作成されたリストパーティションに重複する列が存在する場合にエラーが報告されないバグを修正します[＃31784](https://github.com/pingcap/tidb/issues/31784)
    -   `select for update union select`が誤ったスナップショットを使用したときに返される誤った結果を修正する[＃31530](https://github.com/pingcap/tidb/issues/31530)
    -   復元操作の終了後にリージョンが不均一に分散される可能性があるという潜在的な問題を修正します[＃31034](https://github.com/pingcap/tidb/issues/31034)
    -   `json`タイプ[＃31541](https://github.com/pingcap/tidb/issues/31541)のCOERCIBILITYが間違っているバグを修正します
    -   このタイプがbuiltin- [＃31320](https://github.com/pingcap/tidb/issues/31320)を使用して処理される場合の、 `json`タイプの誤った照合順序を修正します。
    -   TiFlashレプリカの数が[＃32190](https://github.com/pingcap/tidb/issues/32190)に設定されている場合にPDルールが削除されないバグを修正します
    -   `alter column set default`がテーブルスキーマ[＃31074](https://github.com/pingcap/tidb/issues/31074)を誤って更新する問題を修正します
    -   TiDBの`date_format`がMySQLと互換性のない方法で`'\n'`を処理する問題を修正します[＃32232](https://github.com/pingcap/tidb/issues/32232)
    -   結合[＃31629](https://github.com/pingcap/tidb/issues/31629)を使用してパーティションテーブルを更新するときにエラーが発生する可能性があるバグを修正します
    -   列挙値[＃32428](https://github.com/pingcap/tidb/issues/32428)のNulleq関数の誤った範囲計算結果を修正しました
    -   `upper()`および`lower()`の機能で発生する可能性のあるパニックを修正[＃32488](https://github.com/pingcap/tidb/issues/32488)
    -   他のタイプの列をタイムスタンプタイプの列に変更するときに発生するタイムゾーンの問題を修正します[＃29585](https://github.com/pingcap/tidb/issues/29585)
    -   ChunkRPCを使用してデータをエクスポートするときの[＃30880](https://github.com/pingcap/tidb/issues/30880)を修正[＃31981](https://github.com/pingcap/tidb/issues/31981)
    -   動的パーティションプルーニングモード[＃32516](https://github.com/pingcap/tidb/issues/32516)でサブSELECTLIMITが期待どおりに機能しないバグを修正します。
    -   `INFORMATION_SCHEMA.COLUMNS`テーブル[＃32655](https://github.com/pingcap/tidb/issues/32655)のビットデフォルト値の誤った形式または一貫性のない形式を修正します
    -   サーバーの再起動後にパーティションテーブルを一覧表示するためにパーティションテーブルのプルーニングが機能しない可能性があるバグを修正します[＃32416](https://github.com/pingcap/tidb/issues/32416)
    -   `SET timestamp`が実行された後に`add column`が間違ったデフォルトのタイムスタンプを使用する可能性があるバグを修正します[＃31968](https://github.com/pingcap/tidb/issues/31968)
    -   MySQL5.5または5.6クライアントからTiDBパスワードなしアカウントに接続すると失敗する可能性があるバグを修正します[＃32334](https://github.com/pingcap/tidb/issues/32334)
    -   トランザクション[＃29851](https://github.com/pingcap/tidb/issues/29851)で動的モードでパーティションテーブルを読み取るときの誤った結果を修正
    -   TiDBが重複タスクをTiFlash1にディスパッチする可能性があるバグを修正し[＃32814](https://github.com/pingcap/tidb/issues/32814)
    -   `timdiff`関数の入力にミリ秒[＃31680](https://github.com/pingcap/tidb/issues/31680)が含まれている場合に返される誤った結果を修正
    -   パーティションを明示的に読み取り、IndexJoinプランを使用するときの誤った結果を修正する[＃32007](https://github.com/pingcap/tidb/issues/32007)
    -   列タイプを同時に変更すると、列の名前変更が失敗するバグを修正します[＃31075](https://github.com/pingcap/tidb/issues/31075)
    -   TiFlashプランの正味コストを計算するための式がTiKVプランと一致しないというバグを修正します[＃30103](https://github.com/pingcap/tidb/issues/30103)
    -   `KILL TIDB`がアイドル状態の接続ですぐに有効にならないバグを修正します[＃24031](https://github.com/pingcap/tidb/issues/24031)
    -   生成された列を含むテーブルをクエリするときに発生する可能性のある誤った結果を修正する[＃33038](https://github.com/pingcap/tidb/issues/33038)
    -   `left join`を使用して複数のテーブルのデータを削除した誤った結果を[＃31321](https://github.com/pingcap/tidb/issues/31321)
    -   オーバーフロー[＃31868](https://github.com/pingcap/tidb/issues/31868)の場合に`SUBTIME`関数が間違った結果を返すバグを修正します
    -   集計クエリに`having`の条件が含まれている場合に`selection`演算子をプッシュダウンできないバグを修正します[＃33166](https://github.com/pingcap/tidb/issues/33166)
    -   クエリがエラーを報告したときにCTEがブロックされる可能性があるバグを修正します[＃31302](https://github.com/pingcap/tidb/issues/31302)
    -   非厳密モードでテーブルを作成するときにvarbinary列またはvarchar列の長さが長すぎると、エラーが発生する可能性があるバグを修正します[＃30328](https://github.com/pingcap/tidb/issues/30328)
    -   フォロワーが指定されていない場合の`information_schema.placement_policies`のフォロワー数の誤りを修正[＃31702](https://github.com/pingcap/tidb/issues/31702)
    -   インデックスが作成されるときにTiDBが列プレフィックスの長さを0として指定できる問題を修正します[＃31972](https://github.com/pingcap/tidb/issues/31972)
    -   TiDBがスペース[＃31535](https://github.com/pingcap/tidb/issues/31535)で終わるパーティション名を許可する問題を修正します
    -   `RENAME TABLE`ステートメント[＃29893](https://github.com/pingcap/tidb/issues/29893)のエラーメッセージを修正します。

-   TiKV

    -   ピアステータスが`Applying`のときにスナップショットファイルを削除することによって引き起こされるパニックの問題を修正し[＃11746](https://github.com/tikv/tikv/issues/11746)
    -   フロー制御が有効で、 `level0_slowdown_trigger`が明示的に設定されている場合のQPSドロップの問題を修正します[＃11424](https://github.com/tikv/tikv/issues/11424)
    -   ピアを破棄すると待ち時間が長くなる可能性があるという問題を修正します[＃10210](https://github.com/tikv/tikv/issues/10210)
    -   GCワーカーがビジー状態のときにTiKVがデータの範囲を削除できない（つまり、内部コマンド`unsafe_destroy_range`が実行される）バグを修正します[＃11903](https://github.com/tikv/tikv/issues/11903)
    -   一部のコーナーケース[＃11852](https://github.com/tikv/tikv/issues/11852)で、 `StoreMeta`のデータが誤って削除されたときにTiKVがパニックになるバグを修正します。
    -   ARMプラットフォームでプロファイリングを実行するときにTiKVがパニックになるバグを修正します[＃10658](https://github.com/tikv/tikv/issues/10658)
    -   TiKVが2年以上実行されている場合にパニックになる可能性があるバグを修正します[＃11940](https://github.com/tikv/tikv/issues/11940)
    -   SSE命令セット[＃12034](https://github.com/tikv/tikv/issues/12034)の欠落によって引き起こされるARM64アーキテクチャのコンパイルの問題を修正します
    -   初期化されていないレプリカを削除すると、古いレプリカが再作成される可能性がある問題を修正します[＃10533](https://github.com/tikv/tikv/issues/10533)
    -   古いメッセージが原因でTiKVがパニックになるバグを修正します[＃12023](https://github.com/tikv/tikv/issues/12023)
    -   TsSet変換で未定義動作（UB）が発生する可能性がある問題を修正します[＃12070](https://github.com/tikv/tikv/issues/12070)
    -   レプリカの読み取りが線形化可能性に違反する可能性があるバグを修正します[＃12109](https://github.com/tikv/tikv/issues/12109)
    -   TiKVが[＃9765](https://github.com/tikv/tikv/issues/9765)でプロファイリングを実行するときに発生する可能性のあるパニックの問題を修正します。
    -   文字列の一致が正しくないためにtikv-ctlが誤った結果を返す問題を修正します[＃12329](https://github.com/tikv/tikv/issues/12329)
    -   メモリメトリックのオーバーフローによって引き起こされる断続的なパケット損失とメモリ不足（OOM）の問題を修正します[＃12160](https://github.com/tikv/tikv/issues/12160)
    -   TiKV1を終了するときに誤ってTiKVパニックを報告する潜在的な問題を修正し[＃12231](https://github.com/tikv/tikv/issues/12231)

-   PD

    -   PDがジョイントコンセンサス[＃4362](https://github.com/tikv/pd/issues/4362)の無意味なステップで演算子を生成する問題を修正します
    -   PDクライアントを閉じるときにTSO取り消しプロセスがスタックする可能性があるバグを修正します[＃4549](https://github.com/tikv/pd/issues/4549)
    -   リージョンスキャッタースケジューリングが一部のピアを失った問題を修正します[＃4565](https://github.com/tikv/pd/issues/4565)
    -   `dr-autosync`の`Duration`のフィールドを動的に構成できない問題を修正します[＃4651](https://github.com/tikv/pd/issues/4651)

-   TiFlash

    -   メモリ制限が有効になっているときに発生するTiFlashパニックの問題を修正します[＃3902](https://github.com/pingcap/tiflash/issues/3902)
    -   期限切れのデータがゆっくりとリサイクルされる問題を修正します[＃4146](https://github.com/pingcap/tiflash/issues/4146)
    -   `Snapshot`が複数のDDL操作と同時に適用された場合のTiFlashパニックの潜在的な問題を修正します[＃4072](https://github.com/pingcap/tiflash/issues/4072)
    -   読み取りワークロードが重い場合に列を追加した後の潜在的なクエリエラーを修正する[＃3967](https://github.com/pingcap/tiflash/issues/3967)
    -   負の引数を持つ`SQRT`関数が[＃3598](https://github.com/pingcap/tiflash/issues/3598)ではなく`NaN`を返す問題を修正し`Null` 。
    -   `INT`から`DECIMAL`をキャストするとオーバーフロー[＃3920](https://github.com/pingcap/tiflash/issues/3920)が発生する可能性がある問題を修正します
    -   複数値式[＃4016](https://github.com/pingcap/tiflash/issues/4016)で`IN`の結果が正しくない問題を修正します
    -   日付形式が`'\n'`を無効な区切り文字[＃4036](https://github.com/pingcap/tiflash/issues/4036)として識別する問題を修正します
    -   同時実行性の高いシナリオでは、学習者の読み取りプロセスに時間がかかりすぎるという問題を修正します[＃3555](https://github.com/pingcap/tiflash/issues/3555)
    -   `DATETIME`から[＃4151](https://github.com/pingcap/tiflash/issues/4151)をキャストするときに発生する間違った結果を修正し`DECIMAL`
    -   クエリがキャンセルされたときに発生するメモリリークの問題を修正します[＃4098](https://github.com/pingcap/tiflash/issues/4098)
    -   エラスティックスレッドプールを有効にするとメモリリークが発生する可能性があるバグを修正します[＃4098](https://github.com/pingcap/tiflash/issues/4098)
    -   ローカルトンネルが有効になっている場合、MPPクエリをキャンセルすると、タスクが永久にハングする可能性があるバグを修正します[＃4229](https://github.com/pingcap/tiflash/issues/4229)
    -   HashJoinビルド側の失敗により、MPPクエリが永久にハングする可能性があるバグを修正します[＃4195](https://github.com/pingcap/tiflash/issues/4195)
    -   MPPタスクがスレッドを永久にリークする可能性があるバグを修正します[＃4238](https://github.com/pingcap/tiflash/issues/4238)

-   ツール

    -   バックアップと復元（BR）

        -   復元操作で回復不能なエラーが発生したときにBRがスタックするバグを修正します[＃33200](https://github.com/pingcap/tidb/issues/33200)
        -   バックアップの再試行中に暗号化情報が失われた場合に復元操作が失敗するバグを修正します[＃32423](https://github.com/pingcap/tidb/issues/32423)

    -   TiCDC

        -   `batch-replace-enable`が無効になっている場合にMySQLシンクが重複した`replace`のSQLステートメントを生成するバグを修正します[＃4501](https://github.com/pingcap/tiflow/issues/4501)
        -   PDリーダーが殺されたときにTiCDCノードが異常終了するバグを修正します[＃4248](https://github.com/pingcap/tiflow/issues/4248)
        -   一部のMySQLバージョン[＃4504](https://github.com/pingcap/tiflow/issues/4504)のエラー`Unknown system variable 'transaction_isolation'`を修正
        -   `Canal-JSON`が35を誤って処理したときに発生する可能性がある`string`パニックの問題を修正し[＃4635](https://github.com/pingcap/tiflow/issues/4635)
        -   シーケンスが誤って複製される場合があるバグを修正します[＃4563](https://github.com/pingcap/tiflow/issues/4552)
        -   `Canal-JSON`がnil3をサポートしていないために発生する可能性のあるTiCDCパニックの問題を修正し[＃4736](https://github.com/pingcap/tiflow/issues/4736)
        -   タイプ`Enum/Set`および`TinyText/MediumText/Text/LongText`のavroコーデックの誤ったデータマッピングを修正します[＃4454](https://github.com/pingcap/tiflow/issues/4454)
        -   Avroが`NOT NULL`列をnull許容フィールドに変換するバグを修正します[＃4818](https://github.com/pingcap/tiflow/issues/4818)
        -   TiCDCが[＃4699](https://github.com/pingcap/tiflow/issues/4699)を終了できない問題を修正します

    -   TiDBデータ移行（DM）

        -   シンカーメトリックがステータス[＃4281](https://github.com/pingcap/tiflow/issues/4281)をクエリするときにのみ更新される問題を修正します
        -   セーフモードでの更新ステートメントの実行エラーがDMワーカーのパニックを引き起こす可能性がある問題を修正します[＃4317](https://github.com/pingcap/tiflow/issues/4317)
        -   [＃4637](https://github.com/pingcap/tiflow/issues/4637)がエラーを報告するバグを修正します`Column length too big`
        -   複数のDMワーカーが同じアップストリームからデータを書き込むことによって引き起こされる競合の問題を修正します[＃3737](https://github.com/pingcap/tiflow/issues/3737)
        -   何百もの「チェックポイントに変更がない、同期フラッシュチェックポイントをスキップする」がログに出力され、レプリケーションが非常に遅いという問題を修正します[＃4619](https://github.com/pingcap/tiflow/issues/4619)
        -   シャードをマージし、ペシミスティックモードでアップストリームからインクリメンタルデータを複製するときのDML損失の問題を修正します[＃5002](https://github.com/pingcap/tiflow/issues/5002)

    -   TiDB Lightning

        -   一部のインポートタスクにソースファイルが含まれていない場合にTiDBLightningがメタデータスキーマを削除しない可能性があるバグを修正します[＃28144](https://github.com/pingcap/tidb/issues/28144)
        -   ソースファイルとターゲットクラスタのテーブル名が異なる場合に発生するパニックを修正します[＃31771](https://github.com/pingcap/tidb/issues/31771)
        -   チェックサムエラー「GCの有効期間がトランザクション期間より短い」を修正[＃32733](https://github.com/pingcap/tidb/issues/32733)
        -   空のテーブルのチェックに失敗したときにTiDBLightningがスタックする問題を修正します[＃31797](https://github.com/pingcap/tidb/issues/31797)

    -   Dumpling

        -   `dumpling --sql $query`を実行しているときに表示される進行状況が正確でない問題を修正し[＃30532](https://github.com/pingcap/tidb/issues/30532)
        -   AmazonS3が圧縮データのサイズを正しく計算できない問題を修正します[＃30534](https://github.com/pingcap/tidb/issues/30534)

    -   TiDB Binlog

        -   大規模なアップストリーム書き込みトランザクションがKafka1にレプリケートされるときにTiDBBinlogがスキップされる可能性がある問題を修正し[＃1136](https://github.com/pingcap/tidb-binlog/issues/1136)
