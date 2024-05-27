---
title: TiDB 5.0 RC Release Notes
summary: TiDB v5.0.0-rc は、TiDB v5.0 の前バージョンです。クラスター化インデックス、非同期コミット、ジッターの削減、 Raft Joint Consensus アルゴリズム、最適化された `EXPLAIN` 機能、非表示インデックス、エンタープライズ データの信頼性の向上などの新機能が含まれています。また、セキュリティのためにエラー メッセージとログ ファイルの感度を下げる機能もサポートしています。パフォーマンスの向上には、非同期コミット、オプティマイザーの安定性、パフォーマンス ジッターの削減などがあります。また、リージョンメンバーシップの変更中のシステム可用性も向上しています。さらに、AWS S3 および Google Cloud GCS へのバックアップと復元、データのインポート/エクスポート、SQL パフォーマンスの問題のトラブルシューティング用に最適化された `EXPLAIN` 機能もサポートしています。展開とメンテナンスの改善には、強化された `mirror` コマンドとより簡単なインストール プロセスが含まれます。
---

# TiDB 5.0 RC リリースノート {#tidb-5-0-rc-release-notes}

発売日: 2021年1月12日

TiDB バージョン: 5.0.0-rc

TiDB v5.0.0-rc は、TiDB v5.0 の前バージョンです。v5.0 では、PingCAP は、企業がデータベース パフォーマンス、パフォーマンス ジッター、セキュリティ、高可用性、災害復旧、SQL パフォーマンスのトラブルシューティングなどについて心配することなく、TiDB に基づくアプリケーションを迅速に構築できるようにすることに専念します。

v5.0 の主な新機能または改善点は次のとおりです。

-   クラスター化インデックス。この機能を有効にすると、データベースのパフォーマンスが向上します。たとえば、TPC-C tpmC テストでは、クラスター化インデックスを有効にすると TiDB のパフォーマンスが 39% 向上します。
-   非同期コミット。この機能を有効にすると、書き込みレイテンシーが短縮されます。たとえば、Sysbench olpt-insert テストでは、非同期コミットが有効になっている TiDB の書き込みレイテンシーは37.3% 短縮されます。
-   ジッターの削減。これは、オプティマイザーの安定性を向上させ、システム タスクによる I/O、ネットワーク、CPU、メモリリソースの使用を制限することで実現されます。たとえば、72 時間のパフォーマンス テストでは、Sysbench TPS ジッターの標準偏差が 11.09% から 3.36% に削減されます。
-   リージョンメンバーシップの変更中にシステムの可用性を確保するRaftジョイント コンセンサス アルゴリズム。
-   最適化された`EXPLAIN`機能と非表示のインデックスにより、データベース管理者 (DBA) は SQL ステートメントをより効率的にデバッグできるようになります。
-   エンタープライズ データの信頼性を保証します。TiDB から AWS S3storageや Google Cloud GCS にデータをバックアップしたり、これらのクラウドstorageプラットフォームからデータを復元したりできます。
-   AWS S3storageまたは TiDB/MySQL からのデータ インポートまたはデータ エクスポートのパフォーマンスが向上し、企業がクラウド上でアプリケーションを迅速に構築できるようになります。たとえば、TPC-C テストでは、1 TiB データのインポートのパフォーマンスが 254 GiB/h から 366 GiB/h に 40% 向上します。

## 構文 {#sql}

### クラスター化インデックスのサポート (実験的) {#support-clustered-index-experimental}

クラスター化インデックス機能を有効にすると、次の場合に TiDB のパフォーマンスが大幅に向上します (たとえば、TPC-C tpmC テストでは、クラスター化インデックスが有効になっている TiDB のパフォーマンスが 39% 向上します)。

-   データが挿入されると、クラスター化インデックスにより、ネットワークからのインデックス データの書き込みが 1 回削減されます。
-   同等の条件を持つクエリに主キーのみが関係する場合、クラスター化インデックスにより、ネットワークからのインデックス データの読み取りが 1 回削減されます。
-   範囲条件を持つクエリに主キーのみが関係する場合、クラスター化インデックスにより、ネットワークからのインデックス データの複数回の読み取りが削減されます。
-   同等条件または範囲条件を持つクエリに主キー プレフィックスが含まれる場合、クラスター化インデックスによって、ネットワークからのインデックス データの複数回の読み取りが削減されます。

クラスター化インデックスは、テーブル内のデータの物理的なstorage順序を定義します。テーブル内のデータは、クラスター化インデックスの定義に従ってのみ並べ替えられます。各テーブルには、クラスター化インデックスが 1 つだけあります。

ユーザーは、 `tidb_enable_clustered_index`変数を変更することでクラスター化インデックス機能を有効にできます。この機能を有効にすると、新しく作成されたテーブルにのみ適用され、複数の列があるか、1 つの列に整数以外の型がある主キーに適用されます。主キーが 1 つの列に整数型である場合、またはテーブルに主キーがない場合は、クラスター化インデックスの影響を受けずに、データは以前と同じ方法で並べ替えられます。

たとえば、テーブル（ `tbl_name` ）にクラスター化インデックスがあるかどうかを確認するには、 `select tidb_pk_type from information_schema.tables where table_name = '{tbl_name}'`実行します。

-   [ユーザードキュメント](/system-variables.md#tidb_enable_clustered_index-new-in-v50)
-   関連号: [＃4841](https://github.com/pingcap/tidb/issues/4841)

### 非表示のインデックスをサポート {#support-invisible-indexes}

ユーザーがパフォーマンスを調整したり、最適なインデックスを選択したりする場合、SQL ステートメントを使用してインデックスを`Visible`または`Invisible`に設定できます。この設定により、 `DROP INDEX`や`ADD INDEX`などのリソースを消費する操作の実行を回避できます。

インデックスの可視性を変更するには、 `ALTER INDEX`ステートメントを使用します。変更後、オプティマイザーはインデックスの可視性に基づいて、このインデックスをインデックス リストに追加するかどうかを決定します。

-   [ユーザードキュメント](/sql-statements/sql-statement-alter-index.md)
-   関連号: [＃9246](https://github.com/pingcap/tidb/issues/9246)

### <code>EXCEPT</code>および<code>INTERSECT</code>演算子をサポート {#support-code-except-code-and-code-intersect-code-operators}

`INTERSECT`演算子はセット演算子であり、2 つ以上のクエリの結果セットの積集合を返します。ある程度、これは`InnerJoin`演算子の代替となります。

`EXCEPT`演算子はセット演算子であり、2 つのクエリの結果セットを結合し、最初のクエリ結果にはあるが 2 番目のクエリ結果にはない要素を返します。

-   [ユーザードキュメント](/functions-and-operators/set-operators.md)
-   関連号: [＃18031](https://github.com/pingcap/tidb/issues/18031)

## トランザクション {#transaction}

### 悲観的トランザクションの実行成功率を高める {#increase-the-success-rate-of-executing-pessimistic-transactions}

悲観的トランザクション モードでは、トランザクションに関係するテーブルに同時 DDL 操作または`SCHEMA VERSION`変更が含まれている場合、システムはトランザクションの`SCHEMA VERSION`を最新のものに自動的に更新して、トランザクションが DDL 操作によって中断されるのを防ぎ、トランザクションのコミットが成功するようにします。トランザクションが中断された場合、クライアントは`Information schema is changed`エラー メッセージを受け取ります。

-   関連号: [＃18005](https://github.com/pingcap/tidb/issues/18005)

## 文字セットと照合順序 {#character-set-and-collation}

文字セットの大文字と小文字を区別しない比較ソートをサポートします。

-   [ユーザードキュメント](/character-set-and-collation.md#new-framework-for-collations)
-   関連号: [＃17596](https://github.com/pingcap/tidb/issues/17596)

## Security {#security}

### エラーメッセージとログファイルの感度低下をサポート {#support-desensitizing-error-messages-and-log-files}

TiDB では、ID 情報やクレジットカード番号などの機密情報の漏洩を防ぐために、エラー メッセージとログ ファイルの非機密化をサポートするようになりました。

ユーザーは、さまざまなコンポーネントに対して感度低下機能を有効にすることができます。

-   TiDB 側では、tidb-server で SQL ステートメントを使用して`tidb_redact_log=1`変数を設定します。
-   TiKV 側では、tikv-server で`security.redact-info-log = true`構成を設定します。
-   PD側では[＃2852](https://github.com/tikv/pd/issues/2852) -serverで`security.redact-info-log = true`設定をします。3 [＃3011](https://github.com/tikv/pd/pull/3011)
-   TiFlash側では、tiflash-server に`security.redact_info_log = true`設定を設定し、tiflash-learner に`security.redact-info-log = true`設定します。

[ユーザードキュメント](/log-redaction.md)

関連号: [＃18566](https://github.com/pingcap/tidb/issues/18566)

## パフォーマンスの改善 {#performance-improvements}

### 非同期コミットをサポート（実験的） {#support-async-commit-experimental}

非同期コミット機能を有効にすると、トランザクションのレイテンシーを大幅に削減できます。たとえば、この機能を有効にすると、Sysbench oltp-insert テストでのトランザクションのレイテンシーは、この機能が無効になっている場合よりも 37.3% 低くなります。

以前は非同期コミット機能がなかったため、書き込まれたステートメントは 2 フェーズ トランザクション コミットが完了した後にのみクライアントに返されました。現在、非同期コミット機能では、2 フェーズ コミットの最初のフェーズが完了した後に結果をクライアントに返すことがサポートされています。その後、2 番目のフェーズはバックグラウンドで非同期に実行されるため、トランザクション コミットのレイテンシーが短縮されます。

ただし、非同期コミットが有効になっている場合、トランザクションの外部一貫性は`tidb_guarantee_external_consistency = ON`が設定されている場合に**のみ**保証されます。非同期コミットを有効にすると、パフォーマンスが低下する可能性があります。

ユーザーは、グローバル変数`tidb_enable_async_commit = ON`を設定することでこの機能を有効にできます。

-   [ユーザードキュメント](/system-variables.md#tidb_enable_async_commit-new-in-v50)
-   関連号: [＃8316](https://github.com/tikv/tikv/issues/8316)

### インデックス選択におけるオプティマイザの安定性を向上（実験的） {#improve-the-optimizer-s-stability-in-index-selection-experimental}

オプティマイザが常に比較的適切なインデックスを選択できるかどうかは、クエリのレイテンシーが安定しているかどうかに大きく影響します。統計モジュールを改善およびリファクタリングして、同じ SQL ステートメントに対して、統計が欠落しているか不正確であるためにオプティマイザが複数の候補インデックスから毎回異なるインデックスを選択しないようにしました。オプティマイザが比較的適切なインデックスを選択できるようにするための主な改善点は次のとおりです。

-   複数列 NDV、複数列順序依存関係、複数列関数依存関係などの詳細情報を統計モジュールに追加します。
-   統計モジュールをリファクタリングします。
    -   `CMSKetch`から`TopN`値を削除します。
    -   `TopN`の検索ロジックをリファクタリングします。
    -   ヒストグラムから`TopN`情報を削除し、バケット NDV のメンテナンスを容易にするためにヒストグラムのインデックスを作成します。

関連号: [＃18065](https://github.com/pingcap/tidb/issues/18065)

### 不完全なスケジューリングや不完全なI/Oフロー制御によって発生するパフォーマンスジッタを最適化します。 {#optimize-performance-jitter-caused-by-imperfect-scheduling-or-imperfect-i-o-flow-control}

TiDB のスケジューリング プロセスは、I/O、ネットワーク、CPU、メモリなどのリソースを占有します。TiDB がスケジュールされたタスクを制御しない場合、リソースのプリエンプションにより QPS と遅延によってパフォーマンス ジッターが発生する可能性があります。次の最適化を行った後、72 時間のテストでは、Sysbench TPS ジッターの標準偏差が 11.09% から 3.36% に減少しました。

-   ノード容量の変動（常にウォーターライン付近）や PD の`store-limit`構成値が大きすぎるために発生する冗長なスケジューリングの問題を軽減します。これは、 `region-score-formula-version = v2`構成項目を介して有効になる新しいスケジューリング計算式のセットを導入することで実現されます[＃3269](https://github.com/tikv/pd/pull/3269)
-   `enable-cross-table-merge = true`を変更して空のリージョンの数を減らし、リージョン間のマージ機能を有効にします[＃3129](https://github.com/tikv/pd/pull/3129)
-   TiKV バックグラウンドでのデータ圧縮は、多くの I/O リソースを占有します。システムは、バックグラウンド タスクとフォアグラウンドの読み取りおよび書き込み間の I/O リソース`rate-limiter-auto-tuned`競合のバランスをとるために、圧縮率を自動的に調整します。1 構成項目でこの機能を有効にすると、遅延ジッターが大幅に削減されます[＃18011](https://github.com/pingcap/tidb/issues/18011)
-   TiKV がガベージコレクション(GC) とデータ圧縮を実行すると、パーティションが CPU と I/O リソースを占有します。これらの 2 つのタスクの実行中に重複データが存在します。I/O 使用量を削減するために、GC 圧縮フィルター機能はこれらの 2 つのタスクを 1 つに結合し、同じタスクで実行します。この機能はまだ実験的であり、 `gc.enable-compaction-filter = true`で有効にできます[＃18009](https://github.com/pingcap/tidb/issues/18009)
-   TiFlash がデータを圧縮またはソートすると、大量の I/O リソースが消費されます。システムは、圧縮とデータ ソートによる I/O リソースの使用を制限することで、リソースの競合を軽減します。この機能はまだ実験的であり、 `bg_task_io_rate_limit`で有効にできます。

関連号: [＃18005](https://github.com/pingcap/tidb/issues/18005)

### リアルタイム BI / データ ウェアハウス シナリオにおけるTiFlashの安定性を向上 {#improve-the-stability-of-tiflash-in-real-time-bi-data-warehousing-scenarios}

-   膨大なデータ量のシナリオで過剰なメモリ使用によって発生するシステムのメモリメモリ(OOM) を回避するために、DeltaIndex のメモリ使用量を制限します。
-   バックグラウンド データ ソート タスクで使用される I/O 書き込みトラフィックを制限して、フォアグラウンド タスクへの影響を軽減します。
-   コプロセッサ タスクをキューに入れるための新しいスレッド プールを追加します。これにより、コプロセッサを高同時処理するときに過剰なメモリ使用によって発生するシステム OOM を回避できます。

### その他のパフォーマンスの最適化 {#other-performance-optimizations}

-   `delete from table where id <?`文の実行パフォーマンスを向上。P99パフォーマンスが4倍向上[＃18028](https://github.com/pingcap/tidb/issues/18028)
-   TiFlash は、パフォーマンスを向上させるために、複数のローカル ディスクでのデータの同時読み取りと書き込みをサポートします。

## 高可用性と災害復旧 {#high-availability-and-disaster-recovery}

### リージョンメンバーシップの変更時のシステム可用性の向上 (実験的) {#improve-system-availability-during-region-membership-change-experimental}

リージョンのメンバーシップ変更のプロセスでは、「メンバーの追加」と「メンバーの削除」という 2 つの操作が 2 つのステップで実行されます。メンバーシップの変更が完了したときに障害が発生すると、リージョンは使用できなくなり、フォアグラウンド アプリケーションのエラーが返されます。導入されたRaft Joint Consensus アルゴリズムにより、リージョンのメンバーシップ変更中のシステムの可用性が向上します。メンバーシップ変更中の「メンバーの追加」と「メンバーの削除」の操作は 1 つの操作に結合され、すべてのメンバーに送信されます。変更プロセス中、リージョンは中間状態にあります。変更されたメンバーのいずれかが失敗しても、システムは引き続き使用できます。ユーザーは、 `pd-ctl config set enable-joint-consensus true`実行してメンバーシップ変数を変更することで、この機能を有効にすることができます[＃7587](https://github.com/tikv/tikv/issues/7587) [＃2860](https://github.com/tikv/pd/issues/2860)

-   [ユーザードキュメント](/pd-configuration-file.md#enable-joint-consensus-new-in-v50)
-   関連号: [＃18079](https://github.com/pingcap/tidb/issues/18079)

### メモリ管理モジュールを最適化してシステムOOMのリスクを軽減する {#optimize-the-memory-management-module-to-reduce-system-oom-risks}

-   キャッシュ統計のメモリ消費を削減します。
-   Dumplingツールを使用してデータのエクスポート時のメモリ消費を削減します。
-   データの暗号化された中間結果をディスクに保存することでメモリ消費を削減しました。

## バックアップと復元 {#backup-and-restore}

-   バックアップ＆復元ツール（BR）は、AWS S3とGoogle Cloud GCSへのデータのバックアップをサポートしています。（ [ユーザードキュメント](/br/backup-and-restore-storages.md) ）
-   バックアップ＆リストアツール（BR）は、AWS S3およびGoogle Cloud GCSからTiDBへのデータの復元をサポートしています。（ [ユーザードキュメント](/br/backup-and-restore-storages.md) ）
-   関連号: [＃89](https://github.com/pingcap/br/issues/89)

## データのインポートとエクスポート {#data-import-and-export}

-   TiDB Lightning は、 AWS S3storageから TiDB へのAuroraスナップショット データのインポートをサポートしています。(関連する問題: [＃266](https://github.com/pingcap/tidb-lightning/issues/266) )
-   1 TiB のデータを DBaaS T1.standard にインポートする TPC-C テストでは、パフォーマンスが 254 GiB/h から 366 GiB/h に 40% 向上しました。
-   Dumpling は、 TiDB/MySQL から AWS S3storageへのデータのエクスポートをサポートしています (実験的) (関連する問題: [＃8](https://github.com/pingcap/dumpling/issues/8) 、 [ユーザードキュメント](/dumpling-overview.md#export-data-to-amazon-s3-cloud-storage) )

## 診断 {#diagnostics}

### より多くの情報を収集して最適化された<code>EXPLAIN</code>機能により、ユーザーはパフォーマンスの問題をトラブルシューティングできるようになります。 {#optimized-code-explain-code-features-with-more-collected-information-help-users-troubleshoot-performance-issues}

ユーザーが SQL パフォーマンスの問題をトラブルシューティングする場合、パフォーマンスの問題の原因を特定するために詳細な診断情報が必要です。以前のバージョンの TiDB では、 `EXPLAIN`ステートメントによって収集された情報は十分に詳細ではありませんでした。DBA は、ログ情報、監視情報、または推測のみに基づいてトラブルシューティングを実行していましたが、これは非効率的でした。TiDB v5.0 では、ユーザーがパフォーマンスの問題をより効率的にトラブルシューティングできるように、次の改善が行われました。

-   `EXPLAIN ANALYZE`すべての DML ステートメントの分析をサポートし、実際のパフォーマンス プランと各演算子の実行情報を表示します[＃18056](https://github.com/pingcap/tidb/issues/18056)
-   ユーザーは`EXPLAIN FOR CONNECTION`使用して、実行中の SQL ステートメントのステータス情報を分析できます。この情報には、各演算子の実行時間や処理された行数などが含まれます[＃18233](https://github.com/pingcap/tidb/issues/18233)
-   `EXPLAIN ANALYZE`の出力には、オペレータによって送信された RPC 要求の数、ロック競合の解決にかかる時間、ネットワークレイテンシー、RocksDB でスキャンされた削除済みデータの量、RocksDB キャッシュのヒット率など、さらに詳しい情報が含まれています[＃18663](https://github.com/pingcap/tidb/issues/18663)
-   スローログには、SQL文の詳細な実行情報が記録されます。これは、 `EXPLAIN ANALYZE`の出力情報と一致しています。この情報には、各演算子に費やされた時間、処理された行数、送信されたRPC要求の数が含まれます[＃15009](https://github.com/pingcap/tidb/issues/15009)

[ユーザードキュメント](/sql-statements/sql-statement-explain.md)

## 導入とメンテナンス {#deployment-and-maintenance}

-   以前は、TiDB Ansible の設定情報がTiUPにインポートされると、 TiUP はユーザー設定を`ansible-imported-configs`ディレクトリに配置していました。後でユーザーが`tiup cluster edit-config`使用して設定を編集する必要がある場合、インポートされた設定はエディター インターフェイスに表示されず、ユーザーを混乱させる可能性がありました。TiDB v5.0 では、TiDB Ansible 設定がインポートされると、 TiUP は設定情報を`ansible-imported-configs`とエディター インターフェイスの両方に配置します。この改善により、ユーザーはクラスター設定を編集するときにインポートされた設定を確認できます。
-   複数のミラーを 1 つにマージし、ローカル ミラーにコンポーネントを公開し、ローカル ミラーにコンポーネント所有者を追加する機能をサポートする拡張`mirror`コマンド[＃814](https://github.com/pingcap/tiup/issues/814)
    -   大規模な企業、特に金融業界では、本番環境の変更は慎重に検討されます。バージョンごとに CD を使用してインストールする必要があると、面倒な場合があります。TiDB v5.0 では、 TiUPの`merge`コマンドで複数のインストール パッケージを 1 つにマージできるため、インストールが簡単になります。
    -   v4.0 では、ユーザーは自分で構築したミラーを公開するために tiup-server を起動する必要があり、これはあまり便利ではありませんでした。v5.0 では、ユーザーは`tiup mirror set`使用して現在のミラーをローカル ミラーに設定するだけで、自分で構築したミラーを公開できます。
