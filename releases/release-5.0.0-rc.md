---
title: TiDB 5.0 RC Release Notes
---

# TiDB 5.0 RC リリース ノート {#tidb-5-0-rc-release-notes}

発売日：2021年1月12日

TiDB バージョン: 5.0.0-rc

TiDB v5.0.0-rc は、TiDB v5.0 の前のバージョンです。 v5.0 では、PingCAP は、企業が TiDB に基づいてアプリケーションを迅速に構築できるように支援し、データベースのパフォーマンス、パフォーマンスのジッター、セキュリティ、高可用性、災害復旧、SQL パフォーマンスのトラブルシューティングなどに関する心配から企業を解放することに専念します。

v5.0 の主な新機能または改善点は次のとおりです。

-   クラスター化インデックス。この機能を有効にすると、データベースのパフォーマンスが向上します。たとえば、TPC-C tpmC テストでは、クラスター化インデックスを有効にした TiDB のパフォーマンスが 39% 向上しました。
-   非同期コミット。この機能を有効にすると、書き込みレイテンシーが短縮されます。たとえば、Sysbench の olpt-insert テストでは、非同期コミットを有効にすると、TiDB の書き込みレイテンシーが37.3% 短縮されました。
-   ジッターの軽減。これは、オプティマイザの安定性を向上させ、システム タスクによる I/O、ネットワーク、CPU、メモリリソースの使用量を制限することによって実現されます。たとえば、72 時間のパフォーマンス テストでは、Sysbench TPS ジッターの標準偏差が 11.09% から 3.36% に減少しました。
-   Raft Joint Consensus アルゴリズム。リージョンのメンバーシップ変更中にシステムの可用性を確保します。
-   最適化された`EXPLAIN`機能と非表示のインデックスにより、データベース管理者 (DBA) が SQL ステートメントをより効率的にデバッグできるようになります。
-   企業データの信頼性を保証します。 TiDB から AWS S3storageおよび Google Cloud GCS にデータをバックアップしたり、これらのクラウドstorageプラットフォームからデータを復元したりできます。
-   AWS S3storageまたは TiDB/MySQL との間のデータのインポートまたはエクスポートのパフォーマンスが向上し、企業がクラウド上でアプリケーションを迅速に構築できるようになります。たとえば、TPC-C テストでは、1 TiB データをインポートするパフォーマンスが 254 GiB/h から 366 GiB/h に 40% 向上しました。

## SQL {#sql}

### クラスター化インデックスのサポート (実験的) {#support-clustered-index-experimental}

クラスター化インデックス機能を有効にすると、次の場合に TiDB のパフォーマンスが大幅に向上します (たとえば、TPC-C tpmC テストでは、クラスター化インデックスが有効になっている TiDB のパフォーマンスは 39% 向上しました)。

-   データが挿入されると、クラスター化インデックスにより、ネットワークからのインデックス データの書き込みが 1 回削減されます。
-   同等の条件を持つクエリに主キーのみが含まれる場合、クラスター化インデックスにより、ネットワークからのインデックス データの読み取りが 1 回削減されます。
-   範囲条件を含むクエリに主キーのみが含まれる場合、クラスター化インデックスにより、ネットワークからのインデックス データの複数回の読み取りが削減されます。
-   同等条件または範囲条件を含むクエリに主キー プレフィックスが含まれる場合、クラスター化インデックスにより、ネットワークからのインデックス データの複数回の読み取りが削減されます。

クラスター化インデックスは、テーブル内のデータの物理的なstorage順序を定義します。テーブル内のデータは、クラスター化インデックスの定義に従ってのみ並べ替えられます。各テーブルにはクラスター化インデックスが 1 つだけあります。

ユーザーは`tidb_enable_clustered_index`変数を変更することで、クラスター化インデックス機能を有効にすることができます。有効にすると、この機能は新しく作成されたテーブルにのみ有効になり、複数の列を持つ主キー、または 1 つの列に非整数型の主キーに適用されます。主キーが単一列の整数型である場合、またはテーブルに主キーがない場合、データはクラスター化インデックスの影響を受けることなく、以前と同じ方法で並べ替えられます。

たとえば、テーブル ( `tbl_name` ) にクラスター化インデックスがあるかどうかを確認するには、 `select tidb_pk_type from information_schema.tables where table_name = '{tbl_name}'`を実行します。

-   [ユーザードキュメント](/system-variables.md#tidb_enable_clustered_index-new-in-v50)
-   関連問題: [#4841](https://github.com/pingcap/tidb/issues/4841)

### 非表示のインデックスをサポートする {#support-invisible-indexes}

ユーザーは、パフォーマンスを調整したり、最適なインデックスを選択したりするときに、SQL ステートメントを使用してインデックスを`Visible`または`Invisible`に設定できます。この設定により、 `DROP INDEX`や`ADD INDEX`などのリソースを消費する操作の実行を回避できます。

インデックスの可視性を変更するには、 `ALTER INDEX`ステートメントを使用します。変更後、オプティマイザはインデックスの可視性に基づいて、このインデックスをインデックス リストに追加するかどうかを決定します。

-   [ユーザードキュメント](/sql-statements/sql-statement-alter-index.md)
-   関連問題: [#9246](https://github.com/pingcap/tidb/issues/9246)

### <code>EXCEPT</code>演算子と<code>INTERSECT</code>演算子のサポート {#support-code-except-code-and-code-intersect-code-operators}

`INTERSECT`演算子は集合演算子で、2 つ以上のクエリの結果セットの共通部分を返します。ある程度、これは`InnerJoin`演算子の代替となります。

`EXCEPT`演算子は集合演算子で、2 つのクエリの結果セットを結合し、最初のクエリ結果には含まれるが 2 番目のクエリ結果には含まれない要素を返します。

-   [ユーザードキュメント](/functions-and-operators/set-operators.md)
-   関連問題: [#18031](https://github.com/pingcap/tidb/issues/18031)

## トランザクション {#transaction}

### 悲観的トランザクションの実行の成功率を高める {#increase-the-success-rate-of-executing-pessimistic-transactions}

悲観的トランザクション モードでは、トランザクションに関係するテーブルに同時 DDL 操作または`SCHEMA VERSION`の変更が含まれている場合、システムはトランザクションの`SCHEMA VERSION`を最新のものに自動的に更新して、DDL 操作によるトランザクションの中断を回避し、トランザクションのコミットが成功することを保証します。トランザクションが中断されると、クライアントは`Information schema is changed`エラー メッセージを受け取ります。

-   関連問題: [#18005](https://github.com/pingcap/tidb/issues/18005)

## 文字セットと照合順序 {#character-set-and-collation}

文字セットの大文字と小文字を区別しない比較ソートをサポートします。

-   [ユーザードキュメント](/character-set-and-collation.md#new-framework-for-collations)
-   関連問題: [#17596](https://github.com/pingcap/tidb/issues/17596)

## Security {#security}

### エラーメッセージとログファイルの感度を下げるサポート {#support-desensitizing-error-messages-and-log-files}

TiDB は、ID 情報やクレジット カード番号などの機密情報の漏洩を防ぐために、エラー メッセージとログ ファイルの感度を解除することをサポートするようになりました。

ユーザーは、さまざまなコンポーネントの感度解除機能を有効にすることができます。

-   TiDB 側では、tidb-server の SQL ステートメントを使用して`tidb_redact_log=1`変数を設定します。
-   TiKV側では、tikv-serverに`security.redact-info-log = true`設定を行います。
-   PD 側の場合は、pd-server に`security.redact-info-log = true`構成を設定します。 [#2852](https://github.com/tikv/pd/issues/2852) [#3011](https://github.com/tikv/pd/pull/3011)
-   TiFlash側では、tflash-server で`security.redact_info_log = true`設定を設定し、tflash-learner で`security.redact-info-log = true`設定を設定します。

[ユーザードキュメント](/log-redaction.md)

関連問題: [#18566](https://github.com/pingcap/tidb/issues/18566)

## パフォーマンスの向上 {#performance-improvements}

### 非同期コミットをサポート (実験的) {#support-async-commit-experimental}

非同期コミット機能を有効にすると、トランザクションのレイテンシーを大幅に短縮できます。たとえば、この機能を有効にすると、Sysbench oltp-insert テストでのトランザクションのレイテンシーは、この機能が無効の場合より 37.3% 低くなります。

以前は、非同期コミット機能がなかったので、書き込まれているステートメントは、2 フェーズ トランザクションのコミットが終了した後にのみクライアントに返されました。非同期コミット機能は、2 フェーズ コミットの最初のフェーズが終了した後にクライアントに結果を返すことをサポートするようになりました。次に、2 番目のフェーズがバックグラウンドで非同期的に実行されるため、トランザクションのコミットのレイテンシーが短縮されます。

ただし、非同期コミットが有効な場合、トランザクションの外部整合性は`tidb_guarantee_external_consistency = ON`設定した場合に**のみ**保証されます。非同期コミットを有効にすると、パフォーマンスが低下する可能性があります。

ユーザーはグローバル変数`tidb_enable_async_commit = ON`を設定することでこの機能を有効にできます。

-   [ユーザードキュメント](/system-variables.md#tidb_enable_async_commit-new-in-v50)
-   関連問題: [#8316](https://github.com/tikv/tikv/issues/8316)

### インデックス選択におけるオプティマイザの安定性を改善しました (実験的) {#improve-the-optimizer-s-stability-in-index-selection-experimental}

比較的適切なインデックスを常に選択するオプティマイザの機能は、クエリのレイテンシーが安定しているかどうかを大きく左右します。統計モジュールを改善およびリファクタリングし、同じ SQL ステートメントに対して、統計の欠落または不正確さが原因でオプティマイザーが毎回複数の候補インデックスから異なるインデックスを選択しないようにしました。オプティマイザが比較的適切なインデックスを選択できるようにするための主な改善点は次のとおりです。

-   複数列の NDV、複数列の順序の依存関係、複数列の関数の依存関係などの情報を統計モジュールに追加します。
-   統計モジュールをリファクタリングします。
    -   `CMSKetch`から`TopN`値を削除します。
    -   `TopN`の検索ロジックをリファクタリングします。
    -   Bucket NDV のメンテナンスを容易にするために、ヒストグラムから`TopN`情報を削除し、ヒストグラムのインデックスを作成します。

関連問題: [#18065](https://github.com/pingcap/tidb/issues/18065)

### 不完全なスケジューリングまたは不完全な I/O フロー制御によって引き起こされるパフォーマンスのジッターを最適化します。 {#optimize-performance-jitter-caused-by-imperfect-scheduling-or-imperfect-i-o-flow-control}

TiDB スケジューリング プロセスは、I/O、ネットワーク、CPU、メモリなどのリソースを占有します。 TiDB がスケジュールされたタスクを制御しない場合、QPS と遅延により、リソースのプリエンプションによるパフォーマンスのジッターが発生する可能性があります。次の最適化の後、72 時間のテストで、Sysbench TPS ジッターの標準偏差は 11.09% から 3.36% に減少しました。

-   ノード容量の変動 (常に喫水線付近) や、PD `store-limit`構成値の設定が大きすぎることによって引き起こされる冗長なスケジューリングの問題を軽減します。これは、 `region-score-formula-version = v2`の構成項目によって有効になる新しいスケジューリング計算式のセットを導入することによって実現されます。 [#3269](https://github.com/tikv/pd/pull/3269)
-   `enable-cross-table-merge = true`を変更して空のリージョンの数を減らし、クロスリージョンのマージ機能を有効にします。 [#3129](https://github.com/tikv/pd/pull/3129)
-   TiKV バックグラウンドでのデータ圧縮は、多くの I/O リソースを占有します。システムは圧縮率を自動的に調整して、バックグラウンド タスクとフォアグラウンドの読み取りおよび書き込みの間の I/O リソースの競合のバランスをとります。 `rate-limiter-auto-tuned`設定項目でこの機能を有効にすると、遅延ジッターが大幅に減少します。 [#18011](https://github.com/pingcap/tidb/issues/18011)
-   TiKV がガベージコレクション(GC) とデータ圧縮を実行すると、パーティションが CPU と I/O リソースを占有します。これら 2 つのタスクの実行中に、重複するデータが存在します。 I/O 使用量を削減するために、GC 圧縮フィルター機能はこれら 2 つのタスクを 1 つに結合し、同じタスク内で実行します。この機能はまだ実験的であり、 `gc.enable-compaction-filter = true`で有効にできます。 [#18009](https://github.com/pingcap/tidb/issues/18009)
-   TiFlash がデータを圧縮または並べ替えると、大量の I/O リソースが占有されます。システムは、圧縮とデータの並べ替えによる I/O リソースの使用を制限することで、リソースの競合を軽減します。この機能はまだ実験的であり、 `bg_task_io_rate_limit`で有効にできます。

関連問題: [#18005](https://github.com/pingcap/tidb/issues/18005)

### リアルタイム BI / データ ウェアハウジング シナリオにおけるTiFlashの安定性を向上させる {#improve-the-stability-of-tiflash-in-real-time-bi-data-warehousing-scenarios}

-   DeltaIndex のメモリ使用量を制限して、膨大なデータ量のシナリオで過剰なメモリ使用量によって引き起こされるシステムのメモリ不足 (OOM) を回避します。
-   バックグラウンドのデータ並べ替えタスクで使用される I/O 書き込みトラフィックを制限して、フォアグラウンド タスクへの影響を軽減します。
-   新しいスレッド プールをコプロセッサ タスクのキューに追加します。これにより、コプロセッサを高い同時実行で処理するときに過剰なメモリ使用量によって引き起こされるシステム OOM が回避されます。

### その他のパフォーマンスの最適化 {#other-performance-optimizations}

-   `delete from table where id <?`ステートメントの実行パフォーマンスを向上させます。 P99 のパフォーマンスは 4 倍向上します。 [#18028](https://github.com/pingcap/tidb/issues/18028)
-   TiFlash は、パフォーマンスを向上させるために、複数のローカル ディスクでのデータの同時読み取りと書き込みをサポートしています。

## 高可用性と災害復旧 {#high-availability-and-disaster-recovery}

### リージョンのメンバーシップ変更時のシステム可用性の向上 (実験的) {#improve-system-availability-during-region-membership-change-experimental}

リージョンのメンバーシップ変更のプロセスでは、「メンバーの追加」と「メンバーの削除」の 2 つの操作が 2 つのステップで実行されます。メンバーシップの変更が完了するときに障害が発生すると、リージョンは使用できなくなり、フォアグラウンド アプリケーションのエラーが返されます。導入されたRaft Joint Consensus アルゴリズムにより、リージョンのメンバーシップ変更時のシステムの可用性が向上します。会員変更時の「会員追加」と「会員削除」の操作を一つにまとめて全会員に送信します。変更プロセス中、リージョンは中間状態になります。変更されたメンバーのいずれかが失敗した場合でも、システムは引き続き使用できます。ユーザーは、 `pd-ctl config set enable-joint-consensus true`を実行してメンバーシップ変数を変更することで、この機能を有効にできます。 [#7587](https://github.com/tikv/tikv/issues/7587) [#2860](https://github.com/tikv/pd/issues/2860)

-   [ユーザードキュメント](/pd-configuration-file.md#enable-joint-consensus-new-in-v50)
-   関連問題: [#18079](https://github.com/pingcap/tidb/issues/18079)

### メモリ管理モジュールを最適化してシステム OOM リスクを軽減する {#optimize-the-memory-management-module-to-reduce-system-oom-risks}

-   キャッシュ統計のメモリ消費量を削減します。
-   Dumplingツールを使用してデータをエクスポートする際のメモリ消費を削減します。
-   データの暗号化された中間結果をディスクに保存することでメモリ消費量を削減しました。

## バックアップと復元 {#backup-and-restore}

-   バックアップと復元ツール (BR) は、AWS S3 および Google Cloud GCS へのデータのバックアップをサポートしています。 ( [ユーザードキュメント](/br/backup-and-restore-storages.md) )
-   バックアップと復元ツール (BR) は、AWS S3 および Google Cloud GCS から TiDB へのデータの復元をサポートしています。 ( [ユーザードキュメント](/br/backup-and-restore-storages.md) )
-   関連問題: [#89](https://github.com/pingcap/br/issues/89)

## データのインポートとエクスポート {#data-import-and-export}

-   TiDB Lightning は、 AWS S3storageから TiDB へのAuroraスナップショット データのインポートをサポートしています。 (関連問題: [#266](https://github.com/pingcap/tidb-lightning/issues/266) )
-   1 TiB のデータを DBaaS T1.standard にインポートする TPC-C テストでは、パフォーマンスが 254 GiB/h から 366 GiB/h に 40% 向上しました。
-   Dumpling は、 TiDB/MySQL から AWS S3storageへのデータのエクスポートをサポートしています (実験的) (関連問題: [#8](https://github.com/pingcap/dumpling/issues/8) 、 [ユーザードキュメント](/dumpling-overview.md#export-data-to-amazon-s3-cloud-storage) )

## 診断 {#diagnostics}

### より多くの情報が収集され、最適化された<code>EXPLAIN</code>機能は、ユーザーがパフォーマンスの問題をトラブルシューティングするのに役立ちます {#optimized-code-explain-code-features-with-more-collected-information-help-users-troubleshoot-performance-issues}

ユーザーが SQL パフォーマンスの問題をトラブルシューティングする場合、パフォーマンスの問題の原因を特定するための詳細な診断情報が必要です。以前の TiDB バージョンでは、 `EXPLAIN`ステートメントによって収集される情報の詳細が十分ではありませんでした。 DBA は、ログ情報、監視情報、または推測に基づいてのみトラブルシューティングを実行していたため、非効率的である可能性がありました。 TiDB v5.0 では、ユーザーがパフォーマンスの問題をより効率的にトラブルシューティングできるように、次の改良が加えられています。

-   `EXPLAIN ANALYZE`はすべての DML ステートメントの分析をサポートし、実際のパフォーマンス プランと各オペレーターの実行情報を表示します。 [#18056](https://github.com/pingcap/tidb/issues/18056)
-   ユーザーは`EXPLAIN FOR CONNECTION`を使用して、実行中の SQL ステートメントのステータス情報を分析できます。この情報には、各演算子の実行時間と処理された行の数が含まれます。 [#18233](https://github.com/pingcap/tidb/issues/18233)
-   `EXPLAIN ANALYZE`の出力には、オペレーターによって送信された RPC リクエストの数、ロック競合の解決にかかる時間、ネットワークレイテンシー、RocksDB 内の削除されたデータのスキャン量、RocksDB キャッシュのヒット率などの詳細情報が含まれています。 [#18663](https://github.com/pingcap/tidb/issues/18663)
-   SQL ステートメントの詳細な実行情報はスロー ログに記録され、これは`EXPLAIN ANALYZE`の出力情報と一致します。この情報には、各オペレーターが費やした時間、処理された行数、送信された RPC リクエストの数が含まれます。 [#15009](https://github.com/pingcap/tidb/issues/15009)

[ユーザードキュメント](/sql-statements/sql-statement-explain.md)

## 導入とメンテナンス {#deployment-and-maintenance}

-   以前は、TiDB Ansible の構成情報がTiUPにインポートされると、 TiUP はユーザー構成を`ansible-imported-configs`ディレクトリに置きました。後でユーザーが`tiup cluster edit-config`使用して構成を編集する必要がある場合、インポートされた構成はエディター インターフェイスに表示されず、ユーザーが混乱する可能性がありました。 TiDB v5.0 では、TiDB Ansible 構成がインポートされると、 TiUP は構成情報を`ansible-imported-configs`とエディター インターフェイスの両方に置きます。この改善により、ユーザーはクラスター構成を編集するときに、インポートされた構成を確認できるようになります。
-   複数のミラーの 1 つへのマージ、ローカル ミラーでのコンポーネントの公開、およびローカル ミラーでのコンポーネント所有者の追加をサポートする強化された`mirror`コマンド。 [#814](https://github.com/pingcap/tiup/issues/814)
    -   大企業、特に金融業界の場合、本番環境の変化は慎重に考慮されます。各バージョンのインストールに CD を使用する必要がある場合は、面倒な場合があります。 TiDB v5.0 では、 TiUPの`merge`コマンドは複数のインストール パッケージを 1 つにマージすることをサポートしており、インストールが簡単になります。
    -   v4.0 では、ユーザーは自己構築ミラーを公開するために tiup-server を起動する必要がありましたが、これは十分に便利ではありませんでした。 v5.0 では、ユーザーは`tiup mirror set`を使用して現在のミラーをローカル ミラーに設定するだけで、自己構築ミラーを公開できます。
