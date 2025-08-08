---
title: Glossary
summary: TiDB に関する用語集。
---

# 用語集 {#glossary}

この用語集では、TiDB プラットフォームに関連する主要な用語の定義を示します。

その他の利用可能な用語集:

-   [TiDB データ移行用語集](/dm/dm-glossary.md)
-   [TiCDC用語集](/ticdc/ticdc-glossary.md)
-   [TiDB Lightning用語集](/tidb-lightning/tidb-lightning-glossary.md)

## あ {#a}

### ACID {#acid}

ACIDとは、トランザクションの4つの主要な特性、すなわち原子性、一貫性、独立性、そして永続性を指します。これらの特性についてそれぞれ以下で説明します。

-   **原子性**とは、操作のすべての変更が実行されるか、まったく実行されないかのいずれかを意味します。TiDBは、トランザクションの原子性を実現するために、主キーを格納する[リージョン](#regionpeerraft-group)の要素の原子性を保証します。

-   **一貫性と**は、トランザクションがデータベースを常にある一貫性のある状態から別の一貫性のある状態へと移行させることを意味します。TiDBでは、データをメモリに書き込む前にデータの一貫性が確保されます。

-   **分離と**は、処理中のトランザクションが完了するまで他のトランザクションから参照できないことを意味します。これにより、同時実行中のトランザクションは一貫性を損なうことなくデータの読み書きを行うことができます。詳細については、 [TiDB トランザクション分離レベル](/transaction-isolation-levels.md#tidb-transaction-isolation-levels)参照してください。

-   **耐久性と**は、トランザクションが一度コミットされると、システム障害が発生してもコミットされた状態が維持されることを意味します。TiKVは永続storageを使用して耐久性を確保します。

## B {#b}

### バックアップと復元 (BR) {#backup-x26-restore-br}

BRはTiDBのバックアップおよびリストアツールです。詳細については[BRの概要](/br/backup-and-restore-overview.md)参照してください。

`br`は、TiDB でのバックアップまたは復元に使用される[br コマンドラインツール](/br/use-br-command-line-tool.md)です。

### ベースラインキャプチャ {#baseline-capturing}

ベースラインキャプチャは、キャプチャ条件を満たすクエリをキャプチャし、それらのバインディングを作成します。これは[アップグレード中の実行計画の回帰を防ぐ](/sql-plan-management.md#prevent-regression-of-execution-plans-during-an-upgrade)に使用されます。

### バッチテーブル作成 {#batch-create-table}

バッチテーブル作成機能は、複数のテーブルを一括作成することで、一度に複数のテーブルを作成する作業を大幅に高速化します。例えば、 [バックアップと復元 (BR)](/br/backup-and-restore-overview.md)ツールを使用して数千のテーブルを復元する場合、この機能は全体的な復旧時間を短縮するのに役立ちます。詳細については、 [バッチテーブル作成](/br/br-batch-create-table.md)ご覧ください。

### バケツ {#bucket}

[リージョン](#regionpeerraft-group)論理的にバケットと呼ばれる複数の小さな範囲に分割されます。TiKVはバケットごとにクエリ統計情報を収集し、バケットのステータスをPDに報告します。詳細については、 [バケット設計ドキュメント](https://github.com/tikv/rfcs/blob/master/text/0082-dynamic-size-region.md#bucket)参照してください。

## C {#c}

### キャッシュされたテーブル {#cached-table}

キャッシュ テーブル機能を使用すると、TiDB はテーブル全体のデータを TiDBサーバーのメモリにロードし、TiDB は TiKV にアクセスせずにメモリからテーブルデータを直接取得するため、読み取りパフォーマンスが向上します。

### クラスタ {#cluster}

クラスターとは、サービスを提供するために連携して動作するノードのグループです。分散システムでクラスターを使用することで、TiDBは単一ノード構成と比較して、より高い可用性と優れたスケーラビリティを実現します。

TiDB データベースの分散アーキテクチャでは、次のようになります。

-   TiDB ノードは、クライアントとのやり取りにスケーラブルな SQLレイヤーを提供します。
-   PD ノードは、TiDB に回復力のあるメタデータレイヤーを提供します。
-   TiKV ノードは、 Raftプロトコルを使用して、TiDB に可用性が高く、スケーラブルで、復元力のあるstorageを提供します。

詳細については[TiDBアーキテクチャ](/tidb-architecture.md)参照してください。

### パーティションの結合 {#coalesce-partition}

パーティション結合は、ハッシュまたはキーでパーティションテーブル内のパーティション数を減らす方法です。詳細については、 [ハッシュとキーのパーティションを管理する](/partitioned-table.md#manage-hash-and-key-partitions)参照してください。

### カラムファミリー（CF） {#column-family-cf}

RocksDB および TiKV では、カラムファミリ (CF) は、データベース内のキーと値のペアの論理グループを表します。

### 共通テーブル式（CTE） {#common-table-expression-cte}

共通テーブル式（CTE）を使用すると、 [`WITH`](/sql-statements/sql-statement-with.md)句を使用してSQL文内で複数回参照できる一時的な結果セットを定義できます。これにより、文の可読性と実行効率が向上します。詳細については、 [共通テーブル式](/develop/dev-guide-use-common-table-expression.md)参照してください。

### 継続的なプロファイリング {#continuous-profiling}

継続的プロファイリングは、システムコールレベルでリソースのオーバーヘッドを観測する方法です。継続的プロファイリングにより、TiDBはパフォーマンスの問題をきめ細かく観測し、運用チームがフレームグラフを用いて根本原因を特定するのに役立ちます。詳細については、 [TiDBダッシュボードインスタンスプロファイリング - 継続的なプロファイリング](/dashboard/continuous-profiling.md)ご覧ください。

### コプロセッサー {#coprocessor}

コプロセッサーは、TiDBと計算ワークロードを共有するコプロセッシング機構です。storageレイヤー（TiKVまたはTiFlash）に配置され、TiDBからの計算[押し下げられた](/functions-and-operators/expressions-pushed-down.md)リージョンごとに協調的に処理します。

## D {#d}

### Dumpling {#dumpling}

Dumplingは、TiDB、MySQL、またはMariaDBに保存されているデータをSQLまたはCSVデータファイルとしてエクスポートするためのデータエクスポートツールです。論理的なフルバックアップやエクスポートにも使用できます。さらに、 DumplingはAmazon S3へのデータエクスポートもサポートしています。

詳細については[Dumplingを使用してデータをエクスポートする](/dumpling-overview.md)参照してください。

### データ定義言語（DDL） {#data-definition-language-ddl}

データ定義言語（DDL）は、SQL標準の一部であり、テーブルやその他のオブジェクトの作成、変更、削除を扱います。詳細については、 [DDLの紹介](/ddl-introduction.md)参照してください。

### データ移行（DM） {#data-migration-dm}

データ移行（DM）は、MySQL互換データベースからTiDBにデータを移行するためのツールです。DMはMySQL互換データベースインスタンスからデータを読み取り、TiDBのターゲットインスタンスに適用します。詳細については、 [DMの概要](/dm/dm-overview.md)参照してください。

### データ変更言語 (DML) {#data-modification-language-dml}

データ変更言語 (DML) は、テーブル内の行の挿入、更新、および削除を処理する SQL 標準の一部です。

### 開発マイルストーンリリース（DMR） {#development-milestone-release-dmr}

開発マイルストーンリリース（DMR）は、最新機能を導入するTiDBリリースですが、長期サポートは提供されません。詳細については、 [TiDB のバージョン管理](/releases/versioning.md)ご覧ください。

### 災害復旧（DR） {#disaster-recovery-dr}

ディザスタリカバリ（DR）には、将来の災害からデータとサービスを復旧するためのソリューションが含まれます。TiDBは、バックアップやスタンバイクラスタへのレプリケーションなど、様々なディザスタリカバリソリューションを提供しています。詳細については、 [TiDB 災害復旧ソリューションの概要](/dr-solution-introduction.md)ご覧ください。

### 分散実行フレームワーク (DXF) {#distributed-execution-framework-dxf}

Distributed eXecution Framework（DXF）は、TiDBが特定のタスク（インデックスの作成やデータのインポートなど）を集中的にスケジュールし、分散的に実行するために使用するフレームワークです。DXFは、クラスタリソースを効率的に使用しながら、リソース使用量を制御し、コアビジネストランザクションへの影響を軽減するように設計されています。詳細については、 [DXFの紹介](/tidb-distributed-execution-framework.md)参照してください。

### 動的剪定 {#dynamic-pruning}

動的プルーニングモードは、TiDBがパーティションテーブルにアクセスするモードの一つです。動的プルーニングモードでは、各演算子は複数のパーティションへの直接アクセスをサポートします。そのため、TiDBはUnion演算を使用しません。Union演算を省略することで実行効率が向上し、Union演算の同時実行の問題を回避できます。

## E {#e}

### 表現インデックス {#expression-index}

式インデックスは、式に基づいて作成される特殊なタイプのインデックスです。式インデックスを作成すると、TiDBはこのインデックスを式ベースのクエリに使用できるようになり、クエリパフォーマンスが大幅に向上します。

詳細については[CREATE INDEX - 式インデックス](/sql-statements/sql-statement-create-index.md#expression-index)参照してください。

## G {#g}

### ガベージコレクション（GC） {#garbage-collection-gc}

ガベージコレクション（GC）は、不要になったデータを消去してリソースを解放するプロセスです。TiKV GCプロセスの詳細については、 [GCの概要](/garbage-collection-overview.md)参照してください。

### 一般提供（GA） {#general-availability-ga}

機能の一般提供（GA）とは、その機能が完全にテストされ、本番環境で使用できる状態になっていることを意味します。TiDB の機能は、リリース[DMR](#development-milestone-release-dmr)と[LTS](#long-term-support-lts)両方で GA としてリリースされる可能性があります。ただし、TiDB は DMR 用のパッチリリースを提供しないため、本番本番での使用には LTS リリースの使用が推奨されます。

### グローバルトランザクション識別子（GTID） {#global-transaction-identifiers-gtids}

グローバルトランザクションID (GTID) は、MySQL バイナリ ログでどのトランザクションが複製されたかを追跡するために使用される一意のトランザクション ID です。1 [データ移行（DM）](/dm/dm-overview.md) 、これらの ID を使用して一貫したレプリケーションを保証します。

## H {#h}

### ホットスポット {#hotspot}

ホットスポットとは、TiKVの読み取りおよび書き込みワークロードが1つまたは少数のリージョンまたはノードに集中している状況を指します。これはパフォーマンスのボトルネックにつながり、最適なシステムパフォーマンスを妨げる可能性があります。ホットスポットの問題を解決するには、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)参照してください。

### ハイブリッドトランザクションおよび分析処理 (HTAP) {#hybrid-transactional-and-analytical-processing-htap}

ハイブリッド・トランザクション・アンド・アナリティカル・プロセッシング（HTAP）は、同一データベース内でOLTP（オンライン・トランザクション処理）とOLAP（オンライン・アナリティカル・プロセッシング）の両方のワークロードを可能にするデータベース機能です。TiDBでは、行storageにTiKV、列storageにTiFlashを使用することでHTAP機能が提供されます。詳細については、 [TiDB HTAPのクイックスタート](/quick-start-with-htap.md)と[HTAPを探索する](/explore-htap.md)参照してください。

## 私 {#i}

### インメモリ悲観ロック {#in-memory-pessimistic-lock}

インメモリ悲観的ロックは、TiDB v6.0.0で導入された新機能です。この機能を有効にすると、悲観的ロックは通常、リージョンリーダーのメモリにのみ保存され、ディスクへの永続化やRaft経由の他のレプリカへの複製は行われません。この機能により、悲観的ロックの取得にかかるオーバーヘッドが大幅に削減され、悲観的トランザクションのスループットが向上します。

### インデックスの結合 {#index-merge}

インデックスマージは、TiDB v4.0で導入されたテーブルアクセス手法です。この手法により、TiDBオプティマイザはテーブルごとに複数のインデックスを使用し、各インデックスから返される結果をマージできます。場合によっては、この手法によってテーブル全体のスキャンが回避され、クエリの効率が向上します。v5.4以降、インデックスマージはGA機能となりました。

## K {#k}

### キー管理サービス (KMS) {#key-management-service-kms}

キー管理サービス（KMS）は、秘密鍵の安全なstorageと取得を可能にします。例としては、AWS KMS、Google Cloud KMS、HashiCorp Vaultなどが挙げられます。TiDBの様々なコンポーネントは、KMSを使用してstorage暗号化や関連サービスの鍵を管理できます。

### キーバリュー（KV） {#key-value-kv}

キーバリュー（KV）は、値を一意のキーに関連付けることで情報を保存する方法であり、これにより迅速なデータ取得が可能になります。TiDBはTiKVを使用してテーブルとインデックスをキーバリューのペアにマッピングし、データベース全体で効率的なデータstorageとアクセスを実現します。

## L {#l}

### Leader/Follower/Learner {#leader-follower-learner}

Leader/Follower/Learnerはそれぞれ、 [仲間](#regionpeerraft-group)のRaftグループ内の役割に対応します。リーダーはすべてのクライアントリクエストを処理し、フォロワーにデータを複製します。グループリーダーが失敗した場合、フォロワーの1人が新しいリーダーに選出されます。学習者は、レプリカの追加プロセスでのみ機能する、投票権を持たないフォロワーです。

### 軽量ディレクトリアクセスプロトコル（LDAP） {#lightweight-directory-access-protocol-ldap}

軽量ディレクトリアクセスプロトコル（LDAP）は、情報を持つディレクトリにアクセスするための標準化された方法です。アカウントやユーザーデータの管理によく使用されます。TiDBは[LDAP認証プラグイン](/security-compatibility-with-mysql.md#authentication-plugin-status)を介してLDAPをサポートしています。

### ビューをロック {#lock-view}

ロックビュー機能は、悲観的ロックにおけるロックの競合やロック待機に関する詳細情報を提供するため、DBA がトランザクションのロック状況を観察し、デッドロックの問題をトラブルシューティングするのに便利です。

詳細については、システム テーブルのドキュメント[`TIDB_TRX`](/information-schema/information-schema-tidb-trx.md) 、 [`DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md) 、および[`DEADLOCKS`](/information-schema/information-schema-deadlocks.md)参照してください。

### 長期サポート（LTS） {#long-term-support-lts}

長期サポート（LTS）とは、長期間にわたって徹底的にテストされ、メンテナンスされているソフトウェアバージョンを指します。詳細については、 [TiDB のバージョン管理](/releases/versioning.md)ご覧ください。

## M {#m}

### 超並列処理（MPP） {#massively-parallel-processing-mpp}

TiDB v5.0以降、 TiFlashノードを介した大規模並列処理（MPP）アーキテクチャが導入され、大規模な結合クエリの実行ワークロードがTiFlashノード間で共有されます。MPPモードが有効になっている場合、TiDBはコストに基づいて、MPPフレームワークを使用して計算を実行するかどうかを判断します。MPPモードでは、計算中に結合キーがExchange操作を通じて再分配されるため、各TiFlashノードへの計算負荷が分散され、計算速度が向上します。詳細については、 [TiFlash MPPモードを使用する](/tiflash/use-tiflash-mpp-mode.md)参照してください。

### マルチバージョン同時実行制御 (MVCC) {#multi-version-concurrency-control-mvcc}

[MVCC](https://en.wikipedia.org/wiki/Multiversion_concurrency_control) 、TiDBをはじめとするデータベースにおける同時実行制御メカニズムです。トランザクションによるメモリ読み取りを処理することで、TiDBへの同時アクセスを実現し、同時読み取りと書き込みの競合によるブロッキングを回避します。

## お {#o}

### 古い値 {#old-value}

TiCDC が出力する増分変更ログ内の「元の値」。TiCDC が出力する増分変更ログに「元の値」を含めるかどうかを指定できます。

### オンライン分析処理 (OLAP) {#online-analytical-processing-olap}

オンライン分析処理（OLAP）とは、データレポートや複雑なクエリなどの分析タスクに重点を置いたデータベースワークロードを指します。OLAPは、多数の行にわたる大量のデータを処理する、読み取り中心のクエリを特徴としています。

### オンライントランザクション処理 (OLTP) {#online-transaction-processing-oltp}

オンライントランザクション処理 (OLTP) とは、少量のレコードの選択、挿入、更新、削除などのトランザクション タスクに重点を置いたデータベース ワークロードを指します。

### メモリ不足（OOM） {#out-of-memory-oom}

メモリ不足（OOM）とは、メモリ不足によりシステムに障害が発生する状況です。詳細については、 [TiDB OOM の問題のトラブルシューティング](/troubleshoot-tidb-oom.md)参照してください。

### オペレーター {#operator}

オペレーターは、スケジュール設定のためにリージョンに適用されるアクションの集合です。オペレーターは、「リージョン2 のリーダーをストア 5 に移行する」や「リージョン2 のレプリカをストア 1、4、5 に移行する」といったスケジュール設定タスクを実行します。

演算子は[スケジューラ](#scheduler)によって計算および生成することも、外部 API によって作成することもできます。

### オペレータステップ {#operator-step}

オペレータステップは、オペレータの実行におけるステップです。オペレータには通常、複数のオペレータステップが含まれます。

現在、PD によって生成される利用可能なステップは次のとおりです。

-   `TransferLeader` : 指定されたメンバーにリーダーシップを委譲する
-   `AddPeer` : 指定されたストアにピアを追加する
-   `RemovePeer` :リージョンのピアを削除します
-   `AddLearner` : 指定されたストアに学習者を追加する
-   `PromoteLearner` : 指定された学習者を投票メンバーに昇格させる
-   `SplitRegion` : 指定されたリージョンを2つに分割します

### 楽観的な取引 {#optimistic-transaction}

楽観的トランザクションとは、楽観的同時実行制御を使用するトランザクションであり、通常、同時実行環境において競合が発生しません。楽観的トランザクションを有効にすると、TiDBはトランザクションが最終的にコミットされた時点でのみ競合をチェックします。楽観的トランザクションモードは、読み取りが多く書き込みが少ない同時実行シナリオに適しており、TiDBのパフォーマンスを向上させることができます。

詳細については[TiDB 楽観的トランザクションモデル](/optimistic-transaction.md)参照してください。

## P {#p}

### パーティショニング {#partitioning}

[パーティショニング](/partitioned-table.md) 、テーブルを物理的に小さなテーブル パーティションに分割することを指します。これは、RANGE、LIST、HASH、KEY パーティション分割などのパーティション方法によって実行できます。

### PD Control(pd-ctl) {#pd-control-pd-ctl}

PD Control （pd-ctl）は、TiDBクラスタ内のPlacement Driver （PD）と対話するためのコマンドラインツールです。クラスタのステータス情報を取得したり、クラスタ設定を変更したりできます。詳細については、 [PD Controlユーザー ガイド](/pd-control.md)参照してください。

### 保留中/ダウン {#pending-down}

「保留中」と「ダウン」は、ピアの2つの特別な状態です。保留中は、フォロワーまたは学習者のRaftログがリーダーのログと大きく異なることを示します。保留中のフォロワーはリーダーに選出されません。「ダウン」は、ピアがリーダーへの応答を長時間停止している状態を指し、通常は対応するノードがダウンしているか、ネットワークから分離されていることを意味します。

### 配置Driver（PD） {#placement-driver-pd}

配置Driver（PD）は、 [TiDBアーキテクチャ](/tidb-architecture.md#placement-driver-pd-server)の中核コンポーネントであり、メタデータの保存、トランザクションタイムスタンプの割り当て[タイムスタンプ オラクル (TSO)](/tso.md) 、TiKVへのデータ配置の調整、および[TiDBダッシュボード](/dashboard/dashboard-overview.md)実行を担います。詳細については、 [TiDB スケジューリング](/tidb-scheduling.md)参照してください。

### 配置ルール {#placement-rules}

配置ルールは、TiKVクラスター内のデータの配置を構成するために使用されます。この機能を使用すると、テーブルとパーティションを異なるリージョン、データセンター、キャビネット、またはホストに配置するように指定できます。ユースケースとしては、低コストでデータ可用性戦略を最適化したり、ローカルデータレプリカをローカルの古いデータ読み取りに確実に使用できるようにしたり、ローカルデータのコンプライアンス要件に準拠したりすることが挙げられます。

詳細については[SQLの配置ルール](/placement-rules-in-sql.md)参照してください。

### ポイントゲット {#point-get}

ポイント取得とは、一意のインデックスまたはプライマリ インデックスによって 1 行のデータを読み取ることを意味し、返される結果セットは最大 1 行になります。

### ポイントインタイムリカバリ（PITR） {#point-in-time-recovery-pitr}

ポイントインタイムリカバリ（PITR）を使用すると、データを特定の時点（例えば、意図しない`DELETE`ステートメントの直前）に復元できます。詳細については、 [TiDB ログバックアップと PITRアーキテクチャ](/br/br-log-architecture.md)参照してください。

### 述語列 {#predicate-columns}

ほとんどの場合、SQL文を実行する際、オプティマイザは一部の列（例えば、文`WHERE` 、 `JOIN` 、 `ORDER BY` 、 `GROUP BY`列）の統計情報のみを使用します。これらの使用される列は述語列と呼ばれます。詳細については、 [いくつかの列の統計を収集する](/statistics.md#collect-statistics-on-some-columns)参照してください。

## 質問 {#q}

### 1秒あたりのクエリ数（QPS） {#queries-per-second-qps}

1 秒あたりのクエリ数 (QPS) は、データベース サービスが 1 秒あたりに処理するクエリの数であり、データベース スループットの主要なパフォーマンス メトリックとして機能します。

### クォータリミッター {#quota-limiter}

クォータリミッターは、TiDB v6.0.0で導入された実験的機能です。TiKVがデプロイされているマシンのリソースが限られている場合（例えば、CPUが4Vでメモリが16GBしかない場合）、TiKVのフォアグラウンドで過剰な読み取りおよび書き込み要求を処理すると、バックグラウンドで使用されているCPUリソースがそれらの要求の処理に占有され、TiKVのパフォーマンス安定性に影響を与えます。このような状況を回避するために、 [クォータ関連の設定項目](/tikv-configuration-file.md#quota)設定することで、フォアグラウンドで使用されるCPUリソースを制限できます。

## R {#r}

### Raft Engine {#raft-engine}

Raft Engineは、ログ構造設計を備えた組み込みの永続storageエンジンです。TiKVが複数のRaftログを保存するために構築されています。TiDBはv5.4以降、ログstorageエンジンとしてRaft Engineの使用をサポートしています。詳細については、 [Raft Engine](/tikv-configuration-file.md#raft-engine)参照してください。

### リージョン分割 {#region-split}

TiKVクラスター内のリージョンは最初から分割されるのではなく、データが書き込まれるにつれて徐々に分割されます。このプロセスはリージョン分割と呼ばれます。

リージョン分割のメカニズムは、キー空間全体をカバーするために 1 つの初期リージョンを使用し、リージョンのサイズまたはキーの数がしきい値に達するたびに既存の領域を分割して新しい領域を生成することです。

### リージョン/ピア/Raftグループ {#region-peer-raft-group}

リージョンはTiKVにおけるデータstorageの最小単位であり、それぞれがデータ範囲（デフォルトでは256MiB）を表します。各リージョンにはデフォルトで3つのレプリカが存在します。リージョンのレプリカはピアと呼ばれます。同じリージョンに属する複数のピアは、 Raftコンセンサスアルゴリズムを介してデータを複製するため、ピアはRaftインスタンスのメンバーでもあります。TiKVはMulti-Raftを使用してデータを管理します。つまり、各リージョンには、対応する独立したRaftグループが存在します。

### リモート プロシージャ コール (RPC) {#remote-procedure-call-rpc}

リモートプロシージャコール（RPC）は、ソフトウェアコンポーネント間の通信方法です。TiDBクラスタでは、TiDB、TiKV、 TiFlashなどの異なるコンポーネント間の通信にgRPC標準が使用されます。

### リクエストユニット（RU） {#request-unit-ru}

リクエストユニット（RU）は、TiDBにおけるリソース使用量の統一された抽象化単位です。1と[リソース管理](/tidb-resource-control-ru-groups.md)てリソース使用量を管理します。

### 復元する {#restore}

リストアはバックアップ操作の逆の操作です。準備されたバックアップからデータを取得して、システムを以前の状態に戻すプロセスです。

### ロックスDB {#rocksdb}

[ロックスDB](https://rocksdb.org/) 、キーバリューstorageと読み書き機能を提供するLSMツリー構造のエンジンです。Facebookによって開発され、LevelDBをベースにしています。RocksDBはTiKVの中核storageエンジンです。

## S {#s}

### スケジューラ {#scheduler}

スケジューラはPD内のコンポーネントであり、スケジューリングタスクを生成します。PD内の各スケジューラは独立して動作し、それぞれ異なる目的を果たします。一般的に使用されるスケジューラは以下のとおりです。

-   `balance-leader-scheduler` : リーダーの分布を均衡させる
-   `balance-region-scheduler` : ピアの分散をバランスさせる
-   `hot-region-scheduler` : ホットリージョンの分布をバランスさせる
-   `evict-leader-{store-id}` : ノードのすべてのリーダーを排除します (ローリングアップグレードでよく使用されます)

### Security強化モード（SEM） {#security-enhanced-mode-sem}

Security拡張モード（SEM）は、TiDB管理者の権限をよりきめ細かく制御するために使用されます。1 [セキュリティ強化Linux](https://en.wikipedia.org/wiki/Security-Enhanced_Linux)のシステムに着想を得たSEMは、 `SUPER`権限を持つユーザーの権限を制限し、代わりに`RESTRICTED`きめ細かい権限を必要とします。これらの権限は、特定の管理アクションを制御するために明示的に付与する必要があります。

詳細については[System Variables documentation - `tidb_enable_enhanced_security`](/system-variables.md#tidb_enable_enhanced_security)参照してください。

### ステイル読み取り {#stale-read}

ステイル読み取りは、TiDBがTiDBに保存されているデータの履歴バージョンを読み取るために適用するメカニズムです。このメカニズムを使用すると、特定の時点または指定された時間範囲内の対応する履歴データを読み取ることができ、storageノード間のデータレプリケーションによって生じるレイテンシーを削減できます。Stale ステイル読み取りを使用すると、TiDBはデータ読み取り用のレプリカをランダムに選択します。つまり、すべてのレプリカがデータ読み取りに利用可能になります。

詳細については[ステイル読み取り](/stale-read.md)参照してください。

### 静的ソートテーブル / ソート文字列テーブル (SST) {#static-sorted-table-sorted-string-table-sst}

静的ソート テーブルまたはソート文字列テーブルは、RocksDB ( [TiKV](/storage-engine/rocksdb-overview.md)で使用されるstorageエンジン) で使用されるファイルstorage形式です。

### 店 {#store}

ストアとは、TiKVクラスター内のstorageノード（インスタンス数`tikv-server` ）を指します。各ストアには対応するTiKVインスタンスが存在します。

## T {#t}

### 一時テーブル {#temporary-table}

一時テーブルを使用すると、計算の途中結果を一時的に保存できるため、テーブルの作成と削除を繰り返す必要がなくなります。データが不要になると、TiDBは一時テーブルを自動的にクリーンアップして再利用します。この機能により、アプリケーションロジックが簡素化され、テーブル管理のオーバーヘッドが削減され、パフォーマンスが向上します。

詳細については[一時テーブル](/temporary-tables.md)参照してください。

### TiCDC {#ticdc}

[TiCDC](/ticdc/ticdc-overview.md) 、TiDBから様々な下流ターゲットへの増分データレプリケーションを可能にするツールです。これらの下流ターゲットには、他のTiDBインスタンス、MySQL互換データベース、storageサービス、ストリーミングプロセッサ（KafkaやPulsarなど）が含まれます。TiCDCは上流のTiKVからデータ変更ログを取得し、それを順序付けされた行レベルの変更データに解析し、下流に出力します。TiCDCの概念と用語の詳細については、 [TiCDC用語集](/ticdc/ticdc-glossary.md)参照してください。

### TiDB Lightning {#tidb-lightning}

[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)は、静的ファイルからテラバイトレベルのデータをTiDBクラスタにインポートするためのツールです。TiDBクラスタへの初期データインポートによく使用されます。

TiDB Lightningの概念と用語の詳細については、 [TiDB Lightning用語集](/tidb-lightning/tidb-lightning-glossary.md)参照してください。

### TiFlash {#tiflash}

[TiFlash](/tiflash/tiflash-overview.md) 、TiDBのHTAPアーキテクチャの主要コンポーネントです。これはTiKVの列指向拡張であり、強力な一貫性と優れた分離性の両方を提供します。TiFlashは、 **Raft Learnerプロトコル**を使用してTiKVからデータを非同期的に複製することで、列指向レプリカを維持します。読み取り時には、 **Raftコンセンサスインデックス**と**MVCC（多版型同時実行制御）**を活用して、**スナップショット分離の**一貫性を実現します。このアーキテクチャは、HTAPワークロードにおける分離と同期の課題に効果的に対処し、リアルタイムのデータ一貫性を維持しながら効率的な分析クエリを可能にします。

### TiKV MVCC インメモリエンジン (IME) {#tikv-mvcc-in-memory-engine-ime}

[TiKV MVCC インメモリエンジン](/tikv-in-memory-engine.md) (IME) は、書き込まれた最新の MVCC バージョンをメモリにキャッシュし、TiDB から独立した MVCC GC メカニズムを実装して、多数の MVCC 履歴バージョンを含むクエリを高速化します。

### タイムスタンプ オラクル (TSO) {#timestamp-oracle-tso}

TiKVは分散storageシステムであるため、単調増加するタイムスタンプを割り当てるために、グローバルタイミングサービスであるTimestamp Oracle（TSO）が必要です。TiKVでは、この機能はPDによって提供され、Google [スパナ](http://static.googleusercontent.com/media/research.google.com/en//archive/spanner-osdi2012.pdf)では、複数のアトミック時計とGPSによって提供されます。詳細については、 [TSO](/tso.md)参照してください。

### TiUP {#tiup}

[TiUP](/tiup/tiup-overview.md) 、TiDBクラスタのデプロイ、アップグレード、管理、およびTiDB、PD、TiKVを含むTiDBクラスタ内の様々なコンポーネントの管理に使用される管理ツールです。TiUPを使用すると、1つのコマンドを実行するだけでTiDB内の任意のコンポーネントを簡単に実行できるため、管理プロセスが大幅に簡素化されます。

### Top SQL {#top-sql}

Top SQLは、指定された時間範囲におけるTiDBまたはTiKVノードの高負荷の原因となったSQLクエリを特定するのに役立ちます。詳細については、 [Top SQLユーザードキュメント](/dashboard/top-sql.md)ご覧ください。

### 1秒あたりのトランザクション数（TPS） {#transactions-per-second-tps}

1 秒あたりのトランザクション数 (TPS) は、データベースが 1 秒あたりに処理するトランザクションの数であり、データベースのパフォーマンスとスループットを測定するための重要な指標として機能します。

## あなた {#u}

### ユニフォームリソース識別子 (URI) {#uniform-resource-identifier-uri}

URI（Uniform Resource Identifier）は、リソースを識別するための標準化された形式です。詳細については、Wikipediaの[統一資源識別子](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier)ご覧ください。

### ユニバーサルユニーク識別子 (UUID) {#universally-unique-identifier-uuid}

UUID（Universally Unique Identifier）は、データベース内のレコードを一意に識別するために使用される、128ビット（16バイト）のIDです。詳細については、 [UUID](/best-practices/uuid.md)参照してください。

## V {#v}

### ベクトル検索 {#vector-search}

[ベクトル検索](/vector-search/vector-search-overview.md) 、データの意味を優先して関連性の高い結果を提供する検索手法です。キーワードの完全一致や単語の出現頻度に依存する従来の全文検索とは異なり、ベクター検索は、テキスト、画像、音声など様々なデータタイプを高次元ベクトルに変換し、それらのベクトル間の類似性に基づいてクエリを実行します。この検索手法は、データの意味と文脈情報を捉えることで、ユーザーの検索意図をより正確に理解します。検索語がデータベース内のコンテンツと完全に一致しない場合でも、ベクター検索はデータのセマンティクスを分析することで、ユーザーの検索意図に沿った結果を提供できます。
