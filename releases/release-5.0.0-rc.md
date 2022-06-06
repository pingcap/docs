---
title: TiDB 5.0 RC Release Notes
---

# TiDB5.0RCリリースノート {#tidb-5-0-rc-release-notes}

発売日：2021年1月12日

TiDBバージョン：5.0.0-rc

TiDB v5.0.0-rcは、TiDBv5.0の先行バージョンです。 v5.0では、PingCAPは、企業がTiDBに基づいてアプリケーションを迅速に構築し、データベースパフォーマンス、パフォーマンスジッター、セキュリティ、高可用性、ディザスタリカバリ、SQLパフォーマンスのトラブルシューティングなどの心配から解放するのを支援することに専念します。

v5.0では、主な新機能または改善点は次のとおりです。

-   クラスター化されたインデックス。この機能を有効にすると、データベースのパフォーマンスが向上します。たとえば、TPC-C tpmCテストでは、クラスター化インデックスを有効にした場合のTiDBのパフォーマンスが39％向上します。
-   非同期コミット。この機能を有効にすると、書き込みレイテンシが短縮されます。たとえば、Sysbench olpt-insertテストでは、非同期コミットが有効になっている場合のTiDBの書き込みレイテンシが37.3％減少します。
-   ジッタの低減。これは、オプティマイザの安定性を改善し、システムタスクによるI / O、ネットワーク、CPU、およびメモリリソースの使用を制限することによって実現されます。たとえば、72時間のパフォーマンステストでは、Sysbench TPSジッターの標準偏差が11.09％から3.36％に減少します。
-   Raft Joint Consensusアルゴリズム。これにより、リージョンメンバーシップの変更中にシステムの可用性が保証されます。
-   最適化された`EXPLAIN`機能と非表示のインデックス。データベース管理者（DBA）がSQLステートメントをより効率的にデバッグするのに役立ちます。
-   エンタープライズデータの信頼性が保証されています。 TiDBからAWSS3ストレージとGoogleCloudGCSにデータをバックアップしたり、これらのクラウドストレージプラットフォームからデータを復元したりできます。
-   AWSS3ストレージまたはTiDB/MySQLからのデータインポートまたはデータエクスポートのパフォーマンスが向上し、企業がクラウド上でアプリケーションを迅速に構築できるようになります。たとえば、TPC-Cテストでは、1TiBデータのインポートのパフォーマンスが254GiB/hから366GiB/ hに40％向上します。

## SQL {#sql}

### クラスタ化インデックスのサポート（実験的） {#support-clustered-index-experimental}

クラスタ化インデックス機能を有効にすると、次の場合にTiDBのパフォーマンスが大幅に向上します（たとえば、TPC-C tpmCテストでは、クラスタ化インデックスを有効にした場合のTiDBのパフォーマンスが39％向上します）。

-   データが挿入されると、クラスター化されたインデックスにより、ネットワークからのインデックスデータの書き込みが1回減ります。
-   同等の条件を持つクエリに主キーのみが含まれる場合、クラスター化されたインデックスは、ネットワークからのインデックスデータの読み取りを1回減らします。
-   範囲条件を含むクエリに主キーのみが含まれる場合、クラスター化されたインデックスにより、ネットワークからのインデックスデータの複数の読み取りが削減されます。
-   同等または範囲の条件を持つクエリに主キープレフィックスが含まれる場合、クラスター化されたインデックスにより、ネットワークからのインデックスデータの複数の読み取りが削減されます。

クラスタ化インデックスは、テーブル内のデータの物理的な格納順序を定義します。テーブル内のデータは、クラスター化インデックスの定義に従ってのみソートされます。各テーブルには、クラスター化されたインデックスが1つだけあります。

ユーザーは、 `tidb_enable_clustered_index`の変数を変更することにより、クラスター化インデックス機能を有効にできます。有効にすると、この機能は新しく作成されたテーブルでのみ有効になり、複数の列を持つか、単一の列に非整数型である主キーに適用されます。主キーが単一列の整数型である場合、またはテーブルに主キーがない場合、データはクラスター化されたインデックスの影響を受けることなく、以前と同じ方法でソートされます。

たとえば、テーブル（ `tbl_name` ）にクラスター化されたインデックスがあるかどうかを確認するには、 `select tidb_pk_type from information_schema.tables where table_name = '{tbl_name}'`を実行します。

-   [ユーザードキュメント](/system-variables.md#tidb_enable_clustered_index-new-in-v50)
-   関連する問題： [＃4841](https://github.com/pingcap/tidb/issues/4841)

### 非表示のインデックスをサポートする {#support-invisible-indexes}

ユーザーがパフォーマンスを調整したり、最適なインデックスを選択したりする場合、SQLステートメントを使用してインデックスを`Visible`または`Invisible`に設定できます。この設定により、 `DROP INDEX`や`ADD INDEX`などのリソースを消費する操作の実行を回避できます。

インデックスの表示を変更するには、 `ALTER INDEX`ステートメントを使用します。変更後、オプティマイザは、インデックスの可視性に基づいて、このインデックスをインデックスリストに追加するかどうかを決定します。

-   [ユーザードキュメント](/sql-statements/sql-statement-alter-index.md)
-   関連する問題： [＃9246](https://github.com/pingcap/tidb/issues/9246)

### <code>EXCEPT</code>および<code>INTERSECT</code>演算子をサポート {#support-code-except-code-and-code-intersect-code-operators}

`INTERSECT`演算子は集合演算子であり、2つ以上のクエリの結果セットの共通部分を返します。ある程度、それは`InnerJoin`演算子の代替です。

`EXCEPT`演算子は集合演算子であり、2つのクエリの結果セットを組み合わせて、最初のクエリ結果には含まれているが2番目のクエリ結果には含まれていない要素を返します。

-   [ユーザードキュメント](/functions-and-operators/set-operators.md)
-   関連する問題： [＃18031](https://github.com/pingcap/tidb/issues/18031)

## 取引 {#transaction}

### 悲観的なトランザクションの実行の成功率を高める {#increase-the-success-rate-of-executing-pessimistic-transactions}

ペシミスティックトランザクションモードでは、トランザクションに関係するテーブルに同時DDL操作または`SCHEMA VERSION`の変更が含まれている場合、システムはトランザクションの`SCHEMA VERSION`を最新に自動的に更新して、トランザクションがDDL操作によって中断されないようにし、トランザクションのコミットが成功するようにします。トランザクションが中断された場合、クライアントは`Information schema is changed`エラーメッセージを受け取ります。

-   [ユーザードキュメント](/system-variables.md#tidb_enable_amend_pessimistic_txn-new-in-v407)
-   関連する問題： [＃18005](https://github.com/pingcap/tidb/issues/18005)

## キャラクターセットと照合順序 {#character-set-and-collation}

文字セットの大文字と小文字を区別しない比較ソートをサポートします。

-   [ユーザードキュメント](/character-set-and-collation.md#new-framework-for-collations)
-   関連する問題： [＃17596](https://github.com/pingcap/tidb/issues/17596)

## 安全 {#security}

### エラーメッセージとログファイルの感度低下をサポート {#support-desensitizing-error-messages-and-log-files}

TiDBは、ID情報やクレジットカード番号などの機密情報の漏洩を防ぐために、エラーメッセージとログファイルの機密解除をサポートするようになりました。

ユーザーは、さまざまなコンポーネントの感度低下機能を有効にできます。

-   TiDB側では、tidb-serverのSQLステートメントを使用して`tidb_redact_log=1`変数を設定します。
-   TiKV側の場合は、tikv-serverで`security.redact-info-log = true`構成を設定します。
-   PD側は、pd-serverで`security.redact-info-log = true`構成を設定します。 [＃2852](https://github.com/tikv/pd/issues/2852) [＃3011](https://github.com/tikv/pd/pull/3011)
-   TiFlash側の場合、tiflash-serverで`security.redact_info_log = true`構成を設定し、tiflash-learnerで`security.redact-info-log = true`を設定します。

[ユーザードキュメント](/log-redaction.md)

関連する問題： [＃18566](https://github.com/pingcap/tidb/issues/18566)

## パフォーマンスの向上 {#performance-improvements}

### 非同期コミットのサポート（実験的） {#support-async-commit-experimental}

非同期コミット機能を有効にすると、トランザクションの待ち時間を大幅に短縮できます。たとえば、この機能を有効にすると、Sysbench oltp-insertテストのトランザクションの待機時間は、この機能を無効にした場合よりも37.3％低くなります。

以前は非同期コミット機能がなかったため、書き込まれるステートメントは、2フェーズのトランザクションコミットが終了した後にのみクライアントに返されていました。現在、非同期コミット機能は、2フェーズコミットの最初のフェーズが終了した後の結果をクライアントに返すことをサポートしています。次に、2番目のフェーズがバックグラウンドで非同期に実行されるため、トランザクションコミットの待機時間が短縮されます。

ただし、非同期コミットが有効になっている場合、トランザクションの外部整合性は、 `tidb_guarantee_external_consistency = ON`が設定されている場合に**のみ**保証されます。非同期コミットを有効にすると、パフォーマンスが低下する可能性があります。

ユーザーは、グローバル変数`tidb_enable_async_commit = ON`を設定することにより、この機能を有効にできます。

-   [ユーザードキュメント](/system-variables.md#tidb_enable_async_commit-new-in-v50)
-   関連する問題： [＃8316](https://github.com/tikv/tikv/issues/8316)

### インデックス選択におけるオプティマイザの安定性を向上させる（実験的） {#improve-the-optimizer-s-stability-in-index-selection-experimental}

常に比較的適切なインデックスを選択するオプティマイザーの機能は、クエリのレイテンシーが安定しているかどうかを大きく左右します。統計モジュールを改善およびリファクタリングして、同じSQLステートメントに対して、統計が欠落しているか不正確であるためにオプティマイザーが毎回複数の候補インデックスから異なるインデックスを選択しないようにしました。オプティマイザが比較的適切なインデックスを選択するのに役立つ主な改善点は次のとおりです。

-   複数列のNDV、複数列の順序の依存関係、複数列の関数の依存関係など、統計モジュールにさらに情報を追加します。
-   統計モジュールをリファクタリングします。
    -   `CMSKetch`から`TopN`の値を削除します。
    -   `TopN`の検索ロジックをリファクタリングします。
    -   ヒストグラムから`TopN`の情報を削除し、バケットNDVの保守を容易にするためにヒストグラムのインデックスを作成します。

関連する問題： [＃18065](https://github.com/pingcap/tidb/issues/18065)

### 不完全なスケジューリングまたは不完全なI/Oフロー制御によって引き起こされるパフォーマンスジッターを最適化する {#optimize-performance-jitter-caused-by-imperfect-scheduling-or-imperfect-i-o-flow-control}

TiDBスケジューリングプロセスは、I / O、ネットワーク、CPU、メモリなどのリソースを占有します。 TiDBがスケジュールされたタスクを制御しない場合、QPSと遅延により、リソースのプリエンプションが原因でパフォーマンスジッターが発生する可能性があります。次の最適化の後、72時間のテストで、Sysbench TPSジッターの標準偏差が11.09％から3.36％に減少しました。

-   ノード容量の変動（常に喫水線の近く）およびPDの`store-limit`構成値の設定が大きすぎることによって引き起こされる冗長なスケジューリングの問題を減らします。これは、 `region-score-formula-version = v2`の構成項目を介して有効化された新しいスケジューリング計算式のセットを導入することによって実現されます。 [＃3269](https://github.com/tikv/pd/pull/3269)
-   空のリージョンの数を減らすために`enable-cross-table-merge = true`を変更して、リージョン間のマージ機能を有効にします。 [＃3129](https://github.com/tikv/pd/pull/3129)
-   TiKVバックグラウンドでのデータ圧縮は、多くのI/Oリソースを占有します。システムは、圧縮率を自動的に調整して、バックグラウンドタスクとフォアグラウンド読み取りおよび書き込みの間のI/Oリソースの競合のバランスを取ります。 `rate-limiter-auto-tuned`の構成項目でこの機能を有効にすると、遅延ジッターが大幅に減少します。 [＃18011](https://github.com/pingcap/tidb/issues/18011)
-   TiKVがガベージコレクション（GC）とデータ圧縮を実行する場合、パーティションはCPUとI/Oリソースを占有します。これら2つのタスクの実行中に、重複するデータが存在します。 I / Oの使用量を減らすために、GC圧縮フィルター機能はこれら2つのタスクを1つに結合し、同じタスクで実行します。この機能はまだ実験的段階であり、 `gc.enable-compaction-filter = ture`を介して有効にすることができます。 [＃18009](https://github.com/pingcap/tidb/issues/18009)
-   TiFlashがデータを圧縮またはソートするとき、それは多くのI/Oリソースを占有します。システムは、圧縮とデータの並べ替えによるI / Oリソースの使用を制限することにより、リソースの競合を軽減します。この機能はまだ実験的段階であり、 `bg_task_io_rate_limit`を介して有効にすることができます。

関連する問題： [＃18005](https://github.com/pingcap/tidb/issues/18005)

### リアルタイムBI/データウェアハウジングシナリオでのTiFlashの安定性を向上させる {#improve-the-stability-of-tiflash-in-real-time-bi-data-warehousing-scenarios}

-   DeltaIndexのメモリ使用量を制限して、大量のデータ量のシナリオでの過度のメモリ使用量によって引き起こされるシステムのメモリ不足（OOM）を回避します。
-   フォアグラウンドタスクへの影響を減らすために、バックグラウンドデータソートタスクによって使用されるI/O書き込みトラフィックを制限します。
-   キューコプロセッサータスクに新しいスレッドプールを追加します。これにより、高い同時実行性でコプロセッサーを処理するときに過剰なメモリ使用量によって引き起こされるシステムOOMが回避されます。

### その他のパフォーマンスの最適化 {#other-performance-optimizations}

-   `delete from table where id <?`ステートメントの実行パフォーマンスを向上させます。そのP99のパフォーマンスは4倍向上します。 [＃18028](https://github.com/pingcap/tidb/issues/18028)
-   TiFlashは、パフォーマンスを向上させるために、複数のローカルディスクでのデータの同時読み取りと書き込みをサポートしています。

## 高可用性とディザスタリカバリ {#high-availability-and-disaster-recovery}

### リージョンメンバーシップの変更中のシステムの可用性を向上させる（実験的） {#improve-system-availability-during-region-membership-change-experimental}

リージョンメンバーシップの変更プロセスでは、「メンバーの追加」と「メンバーの削除」は、2つのステップで実行される2つの操作です。メンバーシップの変更が終了したときに障害が発生した場合、リージョンは使用できなくなり、フォアグラウンドアプリケーションのエラーが返されます。導入されたRaftJointConsensusアルゴリズムは、リージョンメンバーシップの変更中のシステムの可用性を向上させることができます。メンバーシップ変更時の「メンバーの追加」と「メンバーの削除」の操作を1つの操作にまとめて、すべてのメンバーに送信します。変更プロセス中、リージョンは中間状態になります。変更されたメンバーに障害が発生した場合でも、システムは引き続き使用できます。ユーザーは、 `pd-ctl config set enable-joint-consensus true`を実行してメンバーシップ変数を変更することにより、この機能を有効にできます。 [＃7587](https://github.com/tikv/tikv/issues/7587) [＃2860](https://github.com/tikv/pd/issues/2860)

-   [ユーザードキュメント](/pd-configuration-file.md#enable-joint-consensus-new-in-v50)
-   関連する問題： [＃18079](https://github.com/pingcap/tidb/issues/18079)

### メモリ管理モジュールを最適化して、システムOOMのリスクを軽減します {#optimize-the-memory-management-module-to-reduce-system-oom-risks}

-   キャッシュ統計のメモリ消費を削減します。
-   Dumplingツールを使用してデータをエクスポートする際のメモリ消費を削減します。
-   データの暗号化された中間結果をディスクに保存することにより、メモリ消費を削減しました。

## バックアップと復元 {#backup-and-restore}

-   Backup＆Restoreツール（BR）は、AWSS3およびGoogleCloudGCSへのデータのバックアップをサポートしています。 （ [ユーザードキュメント](/br/use-br-command-line-tool.md#back-up-data-to-amazon-s3-backend) ）
-   Backup＆Restoreツール（BR）は、AWSS3およびGoogleCloudGCSからTiDBへのデータの復元をサポートしています。 （ [ユーザードキュメント](/br/use-br-command-line-tool.md#restore-data-from-amazon-s3-backend) ）
-   関連する問題： [＃89](https://github.com/pingcap/br/issues/89)

## データのインポートとエクスポート {#data-import-and-export}

-   TiDB Lightningは、AWSS3ストレージからTiDBへのAuroraスナップショットデータのインポートをサポートしています。 （関連する問題： [＃266](https://github.com/pingcap/tidb-lightning/issues/266) ）
-   1TiBのデータをDBaaST1.standardにインポートするTPC-Cテストでは、パフォーマンスが254 GiB/hから366GiB/ hに40％向上します。
-   Dumplingは、TiDB /MySQLからAWSS3ストレージへのデータのエクスポートをサポートし[ユーザードキュメント](/dumpling-overview.md#export-data-to-amazon-s3-cloud-storage) （実験的）（関連する問題： [＃8](https://github.com/pingcap/dumpling/issues/8) ）

## 診断 {#diagnostics}

### より多くの情報が収集された最適化された<code>EXPLAIN</code>機能は、ユーザーがパフォーマンスの問題をトラブルシューティングするのに役立ちます {#optimized-code-explain-code-features-with-more-collected-information-help-users-troubleshoot-performance-issues}

ユーザーがSQLパフォーマンスの問題をトラブルシューティングする場合、パフォーマンスの問題の原因を特定するための詳細な診断情報が必要です。以前のTiDBバージョンでは、 `EXPLAIN`ステートメントによって収集された情報は十分に詳細ではありませんでした。 DBAは、ログ情報、監視情報、または推測に基づいてのみトラブルシューティングを実行しましたが、これは非効率的である可能性があります。 TiDB v5.0では、ユーザーがパフォーマンスの問題をより効率的にトラブルシューティングできるように、次の改善が行われました。

-   `EXPLAIN ANALYZE`は、すべてのDMLステートメントの分析をサポートし、各オペレーターの実際のパフォーマンス計画と実行情報を示します。 [＃18056](https://github.com/pingcap/tidb/issues/18056)
-   ユーザーは`EXPLAIN FOR CONNECTION`を使用して、実行中のSQLステートメントの状況情報を分析できます。この情報には、各オペレーターの実行期間と処理された行数が含まれます。 [＃18233](https://github.com/pingcap/tidb/issues/18233)
-   `EXPLAIN ANALYZE`の出力には、オペレーターによって送信されたRPC要求の数、ロックの競合を解決する期間、ネットワークレイテンシー、RocksDBでスキャンされた削除データの量、RocksDBキャッシュのヒット率などの詳細情報があります。 [＃18663](https://github.com/pingcap/tidb/issues/18663)
-   SQLステートメントの詳細な実行情報は、 `EXPLAIN ANALYZE`の出力情報と一致する低速ログに記録されます。この情報には、各オペレーターが消費した時間、処理された行の数、および送信されたRPC要求の数が含まれます。 [＃15009](https://github.com/pingcap/tidb/issues/15009)

[ユーザードキュメント](/sql-statements/sql-statement-explain.md)

## 展開とメンテナンス {#deployment-and-maintenance}

-   以前は、TiDB Ansibleの構成情報がTiUPにインポートされると、TiUPはユーザー構成を`ansible-imported-configs`ディレクトリに配置していました。ユーザーが後で`tiup cluster edit-config`を使用して構成を編集する必要がある場合、インポートされた構成はエディターインターフェイスに表示されないため、ユーザーを混乱させる可能性があります。 TiDB v5.0では、TiDB Ansible構成がインポートされると、TiUPは構成情報を`ansible-imported-configs`とエディターインターフェイスの両方に配置します。この改善により、ユーザーはクラスタ構成を編集しているときに、インポートされた構成を確認できます。
-   複数のミラーを1つにマージし、コンポーネントをローカルミラーに公開し、コンポーネントの所有者をローカルミラーに追加することをサポートする拡張`mirror`コマンド。 [＃814](https://github.com/pingcap/tiup/issues/814)
    -   大企業、特に金融業界では、本番環境の変更は慎重に検討されます。各バージョンでユーザーがインストールにCDを使用する必要がある場合は、問題が発生する可能性があります。 TiDB v5.0では、TiUPの`merge`コマンドは、複数のインストールパッケージを1つにマージすることをサポートしているため、インストールが簡単になります。
    -   v4.0では、ユーザーは自作ミラーを公開するためにtiup-serverを起動する必要がありましたが、これは十分に便利ではありませんでした。 v5.0では、ユーザーは`tiup mirror set`を使用して現在のミラーをローカルミラーに設定するだけで、自作ミラーを公開できます。
