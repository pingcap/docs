---
title: TiDB 5.0 RC Release Notes
summary: TiDB v5.0.0-rcはTiDB v5.0の前身バージョンです。クラスター化インデックス、非同期コミット、ジッターの低減、 Raft Joint Consensusアルゴリズム、最適化された「EXPLAIN」機能、非表示インデックス、エンタープライズデータの信頼性向上などの新機能が含まれています。また、セキュリティ対策として、エラーメッセージとログファイルの感度低下もサポートしています。パフォーマンス向上には、非同期コミット、オプティマイザーの安定性、パフォーマンスジッターの低減が含まれます。また、リージョンメンバーシップ変更時のシステム可用性も向上します。さらに、AWS S3およびGoogle Cloud GCSへのバックアップとリストア、データのインポート/エクスポート、SQLパフォーマンスの問題のトラブルシューティングのための最適化された「EXPLAIN」機能もサポートしています。導入とメンテナンスの改善には、強化された「mirror」コマンドとより簡単なインストールプロセスが含まれます。
---

# TiDB 5.0 RC リリースノート {#tidb-5-0-rc-release-notes}

発売日：2021年1月12日

TiDB バージョン: 5.0.0-rc

TiDB v5.0.0-rcはTiDB v5.0の前身バージョンです。v5.0では、PingCAPは企業がTiDBベースのアプリケーションを迅速に構築できるよう支援し、データベースのパフォーマンス、パフォーマンスジッター、セキュリティ、高可用性、災害復旧、SQLパフォーマンスのトラブルシューティングなどに関する懸念から解放します。

v5.0 の主な新機能または改善点は次のとおりです。

-   クラスター化インデックス。この機能を有効にすると、データベースのパフォーマンスが向上します。例えば、TPC-C tpmCテストでは、クラスター化インデックスを有効にしたTiDBのパフォーマンスは39%向上しました。
-   非同期コミット。この機能を有効にすると、書き込みレイテンシーが短縮されます。例えば、Sysbench olpt-insert テストでは、非同期コミットを有効にした TiDB の書き込みレイテンシーが 37.3% 短縮されます。
-   ジッターの低減。これは、オプティマイザーの安定性を向上させ、システムタスクによるI/O、ネットワーク、CPU、メモリリソースの使用を制限することで実現されます。例えば、72時間のパフォーマンステストでは、Sysbench TPSジッターの標準偏差が11.09%から3.36%に低減しました。
-   リージョンメンバーシップの変更中にシステムの可用性を確保するRaftジョイント コンセンサス アルゴリズム。
-   最適化された`EXPLAIN`機能と非表示のインデックスにより、データベース管理者 (DBA) は SQL ステートメントをより効率的にデバッグできるようになります。
-   エンタープライズデータの信頼性を保証します。TiDBからAWS S3storageやGoogle Cloud GCSにデータをバックアップしたり、これらのクラウドstorageプラットフォームからデータを復元したりできます。
-   AWS S3storageまたはTiDB/MySQLとの間でのデータインポート/エクスポートのパフォーマンスが向上し、企業がクラウド上でアプリケーションを迅速に構築できるようになります。例えば、TPC-Cテストでは、1TiBデータのインポートパフォーマンスが254GiB/時間から366GiB/時間へと40%向上しました。

## SQL {#sql}

### クラスター化インデックスのサポート（実験的） {#support-clustered-index-experimental}

クラスター化インデックス機能を有効にすると、次の場合に TiDB のパフォーマンスが大幅に向上します (たとえば、TPC-C tpmC テストでは、クラスター化インデックスを有効にすると TiDB のパフォーマンスが 39% 向上します)。

-   データが挿入されると、クラスター化インデックスにより、ネットワークからのインデックス データの書き込みが 1 回削減されます。
-   同等の条件を持つクエリに主キーのみが関係する場合、クラスター化インデックスにより、ネットワークからのインデックス データの読み取りが 1 回削減されます。
-   範囲条件を持つクエリに主キーのみが関係する場合、クラスター化インデックスにより、ネットワークからのインデックス データの複数回の読み取りが削減されます。
-   同等条件または範囲条件を持つクエリに主キー プレフィックスが含まれる場合、クラスター化インデックスによって、ネットワークからのインデックス データの複数回の読み取りが削減されます。

クラスター化インデックスは、テーブル内のデータの物理的なstorage順序を定義します。テーブル内のデータは、クラスター化インデックスの定義に従ってのみソートされます。各テーブルには、クラスター化インデックスが1つだけ存在します。

ユーザーは、 `tidb_enable_clustered_index`変数を変更することでクラスター化インデックス機能を有効にできます。この機能を有効にすると、新規作成されたテーブルにのみ適用され、複数の列を持つ主キー、または単一の列に整数型以外の型を持つ主キーに適用されます。主キーが単一の列に整数型を持つ場合、またはテーブルに主キーがない場合、データはクラスター化インデックスの影響を受けず、以前と同じ方法で並べ替えられます。

たとえば、テーブル（ `tbl_name` ）にクラスター化インデックスがあるかどうかを確認するには、 `select tidb_pk_type from information_schema.tables where table_name = '{tbl_name}'`実行します。

-   [ユーザードキュメント](/system-variables.md#tidb_enable_clustered_index-new-in-v50)
-   関連号: [＃4841](https://github.com/pingcap/tidb/issues/4841)

### 非表示のインデックスをサポート {#support-invisible-indexes}

ユーザーはパフォーマンスを調整したり、最適なインデックスを選択したりする際に、SQL文を使用してインデックスを`Visible`または`Invisible`に設定できます。この設定により、 `DROP INDEX`や`ADD INDEX`といったリソースを消費する操作の実行を回避できます。

インデックスの可視性を変更するには、 `ALTER INDEX`文を使用します。変更後、オプティマイザはインデックスの可視性に基づいて、このインデックスをインデックスリストに追加するかどうかを決定します。

-   [ユーザードキュメント](/sql-statements/sql-statement-alter-index.md)
-   関連号: [＃9246](https://github.com/pingcap/tidb/issues/9246)

### <code>EXCEPT</code>および<code>INTERSECT</code>演算子をサポート {#support-code-except-code-and-code-intersect-code-operators}

`INTERSECT`演算子は集合演算子であり、2つ以上のクエリの結果セットの積集合を返します。ある意味では、 `InnerJoin`演算子の代替として機能します。

`EXCEPT`演算子はセット演算子であり、2 つのクエリの結果セットを結合し、最初のクエリ結果にはあるが 2 番目のクエリ結果にはない要素を返します。

-   [ユーザードキュメント](/functions-and-operators/set-operators.md)
-   関連号: [＃18031](https://github.com/pingcap/tidb/issues/18031)

## トランザクション {#transaction}

### 悲観的トランザクションの実行成功率を高める {#increase-the-success-rate-of-executing-pessimistic-transactions}

悲観的トランザクションモードでは、トランザクションに関係するテーブルに同時DDL操作または`SCHEMA VERSION`変更が含まれている場合、システムはトランザクションの`SCHEMA VERSION`最新のものに自動的に更新し、DDL操作によるトランザクションの中断を回避し、トランザクションのコミットを確実に成功させます。トランザクションが中断された場合、クライアントは`Information schema is changed`エラーメッセージを受け取ります。

-   関連号: [＃18005](https://github.com/pingcap/tidb/issues/18005)

## 文字セットと照合順序 {#character-set-and-collation}

文字セットの大文字と小文字を区別しない比較ソートをサポートします。

-   [ユーザードキュメント](/character-set-and-collation.md#new-framework-for-collations)
-   関連号: [＃17596](https://github.com/pingcap/tidb/issues/17596)

## Security {#security}

### エラーメッセージとログファイルのわかりやすさをサポート {#support-desensitizing-error-messages-and-log-files}

TiDB では、ID 情報やクレジットカード番号などの機密情報の漏洩を防ぐために、エラー メッセージとログ ファイルの非機密化をサポートするようになりました。

ユーザーは、さまざまなコンポーネントに対して感度低下機能を有効にすることができます。

-   TiDB 側では、tidb-server で SQL ステートメントを使用して`tidb_redact_log=1`変数を設定します。
-   TiKV 側では、tikv-server で`security.redact-info-log = true`構成を設定します。
-   PD側ではpd-serverに`security.redact-info-log = true`設定をします[＃2852](https://github.com/tikv/pd/issues/2852) [＃3011](https://github.com/tikv/pd/pull/3011)
-   TiFlash側では、tiflash-server に`security.redact_info_log = true`設定を設定し、tiflash-learner に`security.redact-info-log = true`設定します。

[ユーザードキュメント](/log-redaction.md)

関連号: [＃18566](https://github.com/pingcap/tidb/issues/18566)

## パフォーマンスの改善 {#performance-improvements}

### 非同期コミットをサポート（実験的） {#support-async-commit-experimental}

非同期コミット機能を有効にすると、トランザクションのレイテンシーを大幅に削減できます。例えば、この機能を有効にすると、Sysbench oltp-insert テストにおけるトランザクションのレイテンシーは、この機能を無効にした場合よりも 37.3% 低くなります。

以前は非同期コミット機能がなかったため、書き込まれたステートメントは2フェーズトランザクションのコミットが完了した後にのみクライアントに返されていました。今回の非同期コミット機能では、2フェーズコミットの第1フェーズが完了した後に結果をクライアントに返すようになりました。第2フェーズはバックグラウンドで非同期的に実行されるため、トランザクションコミットのレイテンシーが短縮されます。

ただし、非同期コミットが有効になっている場合、トランザクションの外部一貫性は`tidb_guarantee_external_consistency = ON`設定されている場合**のみ**保証されます。非同期コミットを有効にすると、パフォーマンスが低下する可能性があります。

ユーザーは、グローバル変数`tidb_enable_async_commit = ON`設定することでこの機能を有効にできます。

-   [ユーザードキュメント](/system-variables.md#tidb_enable_async_commit-new-in-v50)
-   関連号: [＃8316](https://github.com/tikv/tikv/issues/8316)

### インデックス選択におけるオプティマイザの安定性を向上（実験的） {#improve-the-optimizer-s-stability-in-index-selection-experimental}

オプティマイザが常に比較的適切なインデックスを選択できるかどうかは、クエリのレイテンシーが安定しているかどうかを大きく左右します。統計モジュールを改良およびリファクタリングし、同じSQL文に対して、統計情報の欠落や不正確さが原因で、オプティマイザが複数の候補インデックスから毎回異なるインデックスを選択してしまうことがないようにしました。オプティマイザが比較的適切なインデックスを選択できるようにするための主な改良点は次のとおりです。

-   複数列の NDV、複数列の順序の依存関係、複数列の関数の依存関係など、統計モジュールにさらに情報を追加します。
-   統計モジュールをリファクタリングします。
    -   `CMSKetch`から`TopN`値を削除します。
    -   `TopN`の検索ロジックをリファクタリングします。
    -   ヒストグラムから`TopN`情報を削除し、ヒストグラムのインデックスを作成して、バケット NDV のメンテナンスを容易にします。

関連号: [＃18065](https://github.com/pingcap/tidb/issues/18065)

### 不完全なスケジューリングや不完全なI/Oフロー制御によって発生するパフォーマンスジッタを最適化します。 {#optimize-performance-jitter-caused-by-imperfect-scheduling-or-imperfect-i-o-flow-control}

TiDBのスケジューリングプロセスは、I/O、ネットワーク、CPU、メモリなどのリソースを占有します。TiDBがスケジュールされたタスクを制御しない場合、リソースのプリエンプションによりQPSと遅延がパフォーマンスジッターを引き起こす可能性があります。以下の最適化を行った後、72時間テストにおいて、Sysbench TPSジッターの標準偏差は11.09%から3.36%に減少しました。

-   ノード容量の変動（常にウォーターライン付近）やPDの`store-limit`設定値が大きすぎることによって引き起こされる冗長なスケジューリングの問題を軽減します。これは、 `region-score-formula-version = v2`設定項目で有効化できる新しいスケジューリング計算式を導入することで実現します[＃3269](https://github.com/tikv/pd/pull/3269)
-   `enable-cross-table-merge = true`変更して、空のリージョンの数を減らし、リージョン間のマージ機能を有効にします[＃3129](https://github.com/tikv/pd/pull/3129)
-   TiKVバックグラウンドでのデータ圧縮は、多くのI/Oリソースを消費します。システムは、バックグラウンドタスクとフォアグラウンドの読み取り・書き込み間のI/Oリソースの競合をバランスさせるために、圧縮率を自動的に調整します。この機能を`rate-limiter-auto-tuned`設定項目で有効にすると、遅延ジッターが大幅に減少します[＃18011](https://github.com/pingcap/tidb/issues/18011)
-   TiKVがガベージコレクション（GC）とデータ圧縮を実行する際、パーティションはCPUとI/Oリソースを占有します。これらの2つのタスクの実行中は、データが重複する状態になります。I/O使用量を削減するため、GC圧縮フィルタ機能はこれらの2つのタスクを1つに統合し、同じタスク内で実行します。この機能はまだ実験的であり、 `gc.enable-compaction-filter = true` . [＃18009](https://github.com/pingcap/tidb/issues/18009)から有効化できます。
-   TiFlash がデータを圧縮またはソートすると、大量の I/O リソースが消費されます。システムは、圧縮とデータソートによる I/O リソースの使用を制限することで、リソースの競合を軽減します。この機能はまだ実験的であり、 `bg_task_io_rate_limit`で有効化できます。

関連号: [＃18005](https://github.com/pingcap/tidb/issues/18005)

### リアルタイム BI / データ ウェアハウス シナリオにおけるTiFlashの安定性を向上 {#improve-the-stability-of-tiflash-in-real-time-bi-data-warehousing-scenarios}

-   膨大なデータ量のシナリオで過剰なメモリ使用によって発生するシステムのメモリ不足 (OOM) を回避するために、DeltaIndex のメモリ使用量を制限します。
-   バックグラウンド データ ソート タスクで使用される I/O 書き込みトラフィックを制限して、フォアグラウンド タスクへの影響を軽減します。
-   コプロセッサ タスクをキューに入れるための新しいスレッド プールを追加します。これにより、コプロセッサを高い同時実行性で処理するときに過剰なメモリ使用によって発生するシステム OOM を回避します。

### その他のパフォーマンス最適化 {#other-performance-optimizations}

-   `delete from table where id <?`文の実行パフォーマンスを向上します。P99パフォーマンスは4倍向上します[＃18028](https://github.com/pingcap/tidb/issues/18028)
-   TiFlash は、パフォーマンスを向上させるために、複数のローカル ディスクでのデータの同時読み取りと書き込みをサポートします。

## 高可用性と災害復旧 {#high-availability-and-disaster-recovery}

### リージョンメンバーシップの変更時のシステム可用性の向上（実験的） {#improve-system-availability-during-region-membership-change-experimental}

リージョンメンバーシップの変更プロセスでは、「メンバーの追加」と「メンバーの削除」という2つの操作が2つのステップで実行されます。メンバーシップの変更完了時に障害が発生した場合、リージョンは利用できなくなり、フォアグラウンドアプリケーションのエラーが返されます。導入されたRaft Joint Consensusアルゴリズムは、リージョンメンバーシップの変更中のシステム可用性を向上させることができます。メンバーシップ変更中の「メンバーの追加」と「メンバーの削除」操作は1つの操作に統合され、すべてのメンバーに送信されます。変更プロセス中、リージョンは中間状態にあります。変更されたメンバーのいずれかに障害が発生した場合でも、システムは引き続き利用可能です。ユーザーは、 `pd-ctl config set enable-joint-consensus true` . [＃7587](https://github.com/tikv/tikv/issues/7587) [＃2860](https://github.com/tikv/pd/issues/2860)を実行してメンバーシップ変数を変更することで、この機能を有効にすることができます。

-   [ユーザードキュメント](/pd-configuration-file.md#enable-joint-consensus-new-in-v50)
-   関連号: [＃18079](https://github.com/pingcap/tidb/issues/18079)

### メモリ管理モジュールを最適化してシステムのOOMリスクを軽減します {#optimize-the-memory-management-module-to-reduce-system-oom-risks}

-   キャッシュ統計のメモリ消費を削減します。
-   Dumplingツールを使用してデータのエクスポート時のメモリ消費を削減します。
-   データの暗号化された中間結果をディスクに保存することでメモリ消費を削減しました。

## バックアップと復元 {#backup-and-restore}

-   バックアップ＆リストアツール（BR）は、AWS S3とGoogle Cloud GCSへのデータのバックアップをサポートしています。（ [ユーザードキュメント](/br/backup-and-restore-storages.md) ）
-   バックアップ＆リストアツール(BR)は、AWS S3およびGoogle Cloud GCSからTiDBへのデータの復元をサポートしています。( [ユーザードキュメント](/br/backup-and-restore-storages.md) )
-   関連号: [＃89](https://github.com/pingcap/br/issues/89)

## データのインポートとエクスポート {#data-import-and-export}

-   TiDB Lightning は、 AWS S3storageから TiDB へのAuroraスナップショットデータのインポートをサポートしています。(関連問題: [＃266](https://github.com/pingcap/tidb-lightning/issues/266) )
-   1 TiB のデータを DBaaS T1.standard にインポートする TPC-C テストでは、パフォーマンスが 254 GiB/時間から 366 GiB/時間へと 40% 向上しました。
-   Dumpling は、TiDB/MySQL から AWS S3storageへのデータのエクスポートをサポートしています (実験的) (関連する問題: [＃8](https://github.com/pingcap/dumpling/issues/8) 、 [ユーザードキュメント](/dumpling-overview.md#export-data-to-amazon-s3-cloud-storage) )

## 診断 {#diagnostics}

### より多くの情報を収集する最適化された<code>EXPLAIN</code>機能により、ユーザーはパフォーマンスの問題をトラブルシューティングできるようになります。 {#optimized-code-explain-code-features-with-more-collected-information-help-users-troubleshoot-performance-issues}

SQLパフォーマンスの問題をトラブルシューティングする際には、原因を特定するための詳細な診断情報が必要です。以前のTiDBバージョンでは、 `EXPLAIN`ステートメントで収集される情報は十分に詳細ではありませんでした。DBAはログ情報、監視情報、あるいは推測のみに基づいてトラブルシューティングを行っていましたが、これは非効率的でした。TiDB v5.0では、ユーザーがパフォーマンスの問題をより効率的にトラブルシューティングできるよう、以下の改善が行われました。

-   `EXPLAIN ANALYZE`すべてのDML文の分析をサポートし、実際のパフォーマンスプランと各演算子の実行情報を表示します[＃18056](https://github.com/pingcap/tidb/issues/18056)
-   ユーザーは`EXPLAIN FOR CONNECTION`使用して、実行中のSQL文のステータス情報を分析できます。この情報には、各演算子の実行時間と処理された行数が含まれます[＃18233](https://github.com/pingcap/tidb/issues/18233)
-   `EXPLAIN ANALYZE`の出力には、オペレータによって送信された RPC 要求の数、ロック競合の解決にかかる時間、ネットワークレイテンシー、RocksDB でスキャンされた削除済みデータの量、RocksDB キャッシュのヒット率など、さらに詳しい情報が含まれています[＃18663](https://github.com/pingcap/tidb/issues/18663)
-   SQL文の詳細な実行情報はスローログに記録されます。これは`EXPLAIN ANALYZE`の出力情報と一致しています。この情報には、各演算子の実行時間、処理された行数、送信されたRPC要求の数などが含まれます[＃15009](https://github.com/pingcap/tidb/issues/15009)

[ユーザードキュメント](/sql-statements/sql-statement-explain.md)

## 展開と保守 {#deployment-and-maintenance}

-   以前は、TiDB Ansibleの設定情報がTiUPにインポートされると、 TiUPはユーザー設定を`ansible-imported-configs`ディレクトリに保存していました。その後、ユーザーが`tiup cluster edit-config`使用して設定を編集する必要がある場合、インポートされた設定はエディターインターフェースに表示されず、ユーザーの混乱を招く可能性がありました。TiDB v5.0では、TiDB Ansibleの設定がインポートされると、 TiUPは設定情報を`ansible-imported-configs`とエディターインターフェースの両方に保存します。この改善により、ユーザーはクラスター設定を編集する際に、インポートされた設定を確認できます。
-   複数のミラーを 1 つにマージし、ローカル ミラーにコンポーネントを公開し、ローカル ミラーにコンポーネント所有者を追加する機能をサポートする拡張`mirror`コマンド[＃814](https://github.com/pingcap/tiup/issues/814)
    -   大規模企業、特に金融業界では、本番環境の変更は慎重に検討されます。バージョンごとにCDを使用してインストールする必要があると、面倒な作業になる可能性があります。TiDB v5.0では、 TiUPの`merge`コマンドで複数のインストールパッケージを1つにマージできるため、インストール作業が簡素化されます。
    -   v4.0では、自分で構築したミラーを公開するにはtiup-serverを起動する必要があり、使い勝手が悪かったです。v5.0では、 `tiup mirror set`使用して現在のミラーをローカルミラーに設定するだけで、自分で構築したミラーを公開できます。
