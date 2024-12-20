---
title: Glossary
summary: TiDB に関する用語集。
---

# 用語集 {#glossary}

この用語集では、TiDB プラットフォームに関連する重要な用語の定義を示します。

その他の利用可能な用語集:

-   [TiDB データ移行用語集](/dm/dm-glossary.md)
-   [TiCDC 用語集](/ticdc/ticdc-glossary.md)
-   [TiDB Lightning用語集](/tidb-lightning/tidb-lightning-glossary.md)

## あ {#a}

### ACID {#acid}

ACID は、トランザクションの 4 つの主要な特性、つまり原子性、一貫性、独立性、および永続性を指します。これらの各特性については、以下で説明します。

-   **アトミック性**とは、操作のすべての変更が実行されるか、まったく実行されないかのいずれかを意味します。TiDB は、トランザクションのアトミック性を実現するために、主キーを格納する[リージョン](#regionpeerraft-group)のアトミック性を保証します。

-   **一貫性**とは、トランザクションが常にデータベースをある一貫性のある状態から別の一貫性のある状態に移行することを意味します。TiDB では、データをメモリに書き込む前にデータの一貫性が確保されます。

-   **分離とは**、進行中のトランザクションが完了するまで他のトランザクションから見えないことを意味します。これにより、同時トランザクションは一貫性を犠牲にすることなくデータの読み取りと書き込みを行うことができます。詳細については、 [TiDB トランザクション分離レベル](/transaction-isolation-levels.md#tidb-transaction-isolation-levels)参照してください。

-   **耐久性**とは、トランザクションが一度コミットされると、システム障害が発生した場合でもコミットされたままになることを意味します。TiKV は永続storageを使用して耐久性を確保します。

## B {#b}

### バックアップと復元 (BR) {#backup-x26-restore-br}

BR はTiDB のバックアップおよび復元ツールです。詳細については、 [BRの概要](/br/backup-and-restore-overview.md)参照してください。

`br` TiDB でのバックアップまたは復元に使用される[br コマンドラインツール](/br/use-br-command-line-tool.md)です。

### ベースラインキャプチャ {#baseline-capturing}

ベースライン キャプチャは、キャプチャ条件を満たすクエリをキャプチャし、それらのバインディングを作成します。これは[アップグレード中の実行計画の回帰を防ぐ](/sql-plan-management.md#prevent-regression-of-execution-plans-during-an-upgrade)に使用されます。

### バッチテーブル作成 {#batch-create-table}

バッチテーブル作成は、TiDB v6.0.0 で導入された機能です。この機能はデフォルトで有効になっていますBR (バックアップと復元) を使用して多数のテーブル (約 50000) を含むデータを復元する場合、この機能を使用すると、バッチでテーブルを作成することで復元プロセスを大幅に高速化できます。詳細については、 [バッチテーブル作成](/br/br-batch-create-table.md)参照してください。

### バケツ {#bucket}

[リージョン](#regionpeerraft-group)論理的にバケットと呼ばれるいくつかの小さな範囲に分割されます。TiKV はバケットごとにクエリ統計を収集し、バケットのステータスを PD に報告します。詳細については、 [バケット設計ドキュメント](https://github.com/tikv/rfcs/blob/master/text/0082-dynamic-size-region.md#bucket)を参照してください。

## Ｃ {#c}

### キャッシュされたテーブル {#cached-table}

キャッシュテーブル機能を使用すると、TiDB はテーブル全体のデータを TiDBサーバーのメモリにロードし、TiKV にアクセスせずにメモリからテーブルデータを直接取得するため、読み取りパフォーマンスが向上します。

### パーティションの結合 {#coalesce-partition}

パーティション結合は、ハッシュまたはキーでパーティションテーブル内のパーティションの数を減らす方法です。詳細については、 [ハッシュとキーのパーティションを管理する](/partitioned-table.md#manage-hash-and-key-partitions)参照してください。

### カラムファミリー (CF) {#column-family-cf}

RocksDB および TiKV では、カラムファミリ (CF) は、データベース内のキーと値のペアの論理グループを表します。

### 共通テーブル式 (CTE) {#common-table-expression-cte}

共通テーブル式 (CTE) を使用すると、 [`WITH`](/sql-statements/sql-statement-with.md)句を使用して SQL ステートメント内で複数回参照できる一時的な結果セットを定義できます。詳細については、 [共通テーブル式](/develop/dev-guide-use-common-table-expression.md)参照してください。

### 継続的なプロファイリング {#continuous-profiling}

TiDB 5.3.0 で導入された継続的プロファイリングは、システム コール レベルでリソース オーバーヘッドを観察する方法です。継続的プロファイリングのサポートにより、TiDB はデータベース ソース コードを直接調べるのと同じくらい明確なパフォーマンス情報を提供し、R&amp;D および運用保守担当者がフレーム グラフを使用してパフォーマンスの問題の根本原因を特定するのに役立ちます。詳細については、 [TiDB ダッシュボード インスタンス プロファイリング - 継続的なプロファイリング](/dashboard/continuous-profiling.md)参照してください。

## だ {#d}

### データ定義言語 (DDL) {#data-definition-language-ddl}

データ定義言語 (DDL) は、テーブルやその他のオブジェクトの作成、変更、削除を扱う SQL 標準の一部です。詳細については、 [DDL の概要](/ddl-introduction.md)参照してください。

### データ移行 (DM) {#data-migration-dm}

データ移行 (DM) は、MySQL 互換データベースから TiDB にデータを移行するためのツールです。DM は、MySQL 互換データベース インスタンスからデータを読み取り、それを TiDB ターゲット インスタンスに適用します。詳細については、 [DMの概要](/dm/dm-overview.md)参照してください。

### データ変更言語 (DML) {#data-modification-language-dml}

データ変更言語 (DML) は、テーブル内の行の挿入、更新、削除を処理する SQL 標準の一部です。

### 開発マイルストーンリリース (DMR) {#development-milestone-release-dmr}

開発マイルストーン リリース (DMR) は、最新の機能を導入するが長期的なサポートは提供しない TiDB リリースです。詳細については、 [TiDB バージョン管理](/releases/versioning.md)参照してください。

### 災害復旧 (DR) {#disaster-recovery-dr}

災害復旧 (DR) には、将来の災害からデータとサービスを復旧するために使用できるソリューションが含まれます。TiDB は、バックアップやスタンバイ クラスターへのレプリケーションなど、さまざまな災害復旧ソリューションを提供します。詳細については、 [TiDB 災害復旧ソリューションの概要](/dr-solution-introduction.md)参照してください。

### 分散実行フレームワーク (DXF) {#distributed-execution-framework-dxf}

Distributed eXecution Framework (DXF) は、TiDB が特定のタスク (インデックスの作成やデータのインポートなど) を集中的にスケジュールし、分散方式で実行するために使用するフレームワークです。DXF は、リソースの使用を制御し、コア ビジネス トランザクションへの影響を軽減しながら、クラスター リソースを効率的に使用するように設計されています。詳細については、 [DXF の紹介](/tidb-distributed-execution-framework.md)参照してください。

### 動的剪定 {#dynamic-pruning}

動的プルーニングモードは、TiDB がパーティション テーブルにアクセスするモードの 1 つです。動的プルーニング モードでは、各演算子は複数のパーティションへの直接アクセスをサポートします。そのため、TiDB は Union を使用しなくなりました。Union 操作を省略すると、実行効率が向上し、Union の同時実行の問題を回避できます。

## グ {#g}

### ガベージコレクション (GC) {#garbage-collection-gc}

ガベージ コレクション (GC) は、古くなったデータを消去してリソースを解放するプロセスです。TiKV GC プロセスの詳細については、 [GC の概要](/garbage-collection-overview.md)参照してください。

### 一般提供 (GA) {#general-availability-ga}

機能の一般提供 (GA) とは、機能が完全にテストされ、実本番環境で使用できる一般提供であることを意味します。TiDB 機能は、リリース[DMMR の](#development-milestone-release-dmr)と[長期保証](#long-term-support-lts)両方で GA としてリリースできます。ただし、TiDB は DMR のパッチ リリースを提供しないため、実本番環境での使用には LTS リリースを使用することをお勧めします。

### グローバルトランザクション識別子 (GTID) {#global-transaction-identifiers-gtids}

グローバルトランザクションID (GTID) は、MySQL バイナリ ログでどのトランザクションが複製されたかを追跡するために使用される一意のトランザクション ID です。1 [データ移行 (DM)](/dm/dm-overview.md) 、これらの ID を使用して一貫したレプリケーションを保証します。

## H {#h}

### ハイブリッドトランザクションおよび分析処理 (HTAP) {#hybrid-transactional-and-analytical-processing-htap}

ハイブリッド トランザクションおよび分析処理 (HTAP) は、同じデータベース内で OLTP (オンライン トランザクション処理) と OLAP (オンライン分析処理) の両方のワークロードを可能にするデータベース機能です。TiDB の場合、行storageには TiKV、列storageにはTiFlash を使用して HTAP 機能が提供されます。詳細については、 [ガートナーのウェブサイトにおけるHTAPの定義](https://www.gartner.com/en/information-technology/glossary/htap-enabling-memory-computing-technologies)参照してください。

## 私 {#i}

### インメモリ悲観的ロック {#in-memory-pessimistic-lock}

インメモリ悲観的ロックは、TiDB v6.0.0 で導入された新機能です。この機能を有効にすると、悲観的ロックは通常、リージョンリーダーのメモリにのみ保存され、ディスクに永続化されず、 Raftを介して他のレプリカに複製されません。この機能により、悲観的ロックの取得にかかるオーバーヘッドが大幅に削減され、悲観的トランザクションのスループットが向上します。

### インデックスの結合 {#index-merge}

インデックス マージは、TiDB v4.0 で導入されたテーブルへのアクセス方法です。この方法を使用すると、TiDB オプティマイザーはテーブルごとに複数のインデックスを使用し、各インデックスによって返された結果をマージできます。シナリオによっては、この方法によりテーブル全体のスキャンが回避され、クエリの効率が向上します。v5.4 以降、インデックス マージは GA 機能になりました。

## け {#k}

### キー管理サービス (KMS) {#key-management-service-kms}

キー管理サービス (KMS) を使用すると、秘密キーを安全にstorageおよび取得できます。例としては、AWS KMS、Google Cloud KMS、HashiCorp Vault などがあります。さまざまな TiDB コンポーネントは、KMS を使用してstorage暗号化および関連サービスのキーを管理できます。

### キーバリュー (KV) {#key-value-kv}

キー値 (KV) は、値を一意のキーに関連付けることで情報を保存し、迅速なデータ取得を可能にする方法です。TiDB は TiKV を使用してテーブルとインデックスをキーと値のペアにマッピングし、データベース全体で効率的なデータstorageとアクセスを可能にします。

## ら {#l}

### Leader/Follower/Learner {#leader-follower-learner}

Leader/Follower/Learnerはそれぞれ、 [仲間](#regionpeerraft-group)のRaftグループ内の役割に対応します。リーダーはすべてのクライアント要求に応え、フォロワーにデータを複製します。グループ リーダーが失敗した場合、フォロワーの 1 人が新しいリーダーとして選出されます。学習者は、レプリカの追加プロセスでのみ機能する、投票権のないフォロワーです。

### 軽量ディレクトリ アクセス プロトコル (LDAP) {#lightweight-directory-access-protocol-ldap}

軽量ディレクトリ アクセス プロトコル (LDAP) は、情報を含むディレクトリにアクセスするための標準化された方法です。これは、アカウントとユーザー データの管理によく使用されます。TiDB は、 [LDAP認証プラグイン](/security-compatibility-with-mysql.md#authentication-plugin-status)介して LDAP をサポートします。

### 長期サポート (LTS) {#long-term-support-lts}

長期サポート (LTS) とは、長期間にわたって徹底的にテストされ、保守されるソフトウェア バージョンを指します。詳細については、 [TiDB バージョン管理](/releases/versioning.md)参照してください。

## ま {#m}

### 超並列処理 (MPP) {#massively-parallel-processing-mpp}

v5.0 以降、TiDB はTiFlashノードを介して大規模並列処理 (MPP)アーキテクチャを導入し、大規模な結合クエリの実行ワークロードをTiFlashノード間で共有します。MPP モードを有効にすると、TiDB はコストに基づいて、MPP フレームワークを使用して計算を実行するかどうかを決定します。MPP モードでは、計算中に結合キーが Exchange 操作を通じて再分配されるため、計算負荷が各TiFlashノードに分散され、計算が高速化されます。詳細については、 [TiFlash MPPモードを使用する](/tiflash/use-tiflash-mpp-mode.md)参照してください。

### マルチバージョン同時実行制御 (MVCC) {#multi-version-concurrency-control-mvcc}

[MVCC](https://en.wikipedia.org/wiki/Multiversion_concurrency_control) 、TiDB やその他のデータベースにおける同時実行制御メカニズムです。トランザクションによって読み取られたメモリを処理して TiDB への同時アクセスを実現し、同時読み取りと書き込みの競合によるブロッキングを回避します。

## お {#o}

### 古い値 {#old-value}

TiCDC が出力する増分変更ログ内の「元の値」。TiCDC が出力する増分変更ログに「元の値」を含めるかどうかを指定できます。

### オンライン分析処理 (OLAP) {#online-analytical-processing-olap}

オンライン分析処理 (OLAP) とは、データ レポートや複雑なクエリなどの分析タスクに重点を置いたデータベース ワークロードを指します。OLAP は、多数の行にわたる大量のデータを処理する読み取り中心のクエリを特徴としています。

### オンライントランザクション処理 (OLTP) {#online-transaction-processing-oltp}

オンライントランザクション処理 (OLTP) とは、少量のレコードの選択、挿入、更新、削除などのトランザクション タスクに重点を置いたデータベース ワークロードを指します。

### メモリ不足 (OOM) {#out-of-memory-oom}

メモリ不足 (OOM) は、メモリ不足によりシステムが障害を起こす状況です。詳細については、 [TiDB OOM の問題のトラブルシューティング](/troubleshoot-tidb-oom.md)参照してください。

### オペレーター {#operator}

オペレーターは、スケジュール設定の目的でリージョンに適用されるアクションの集合です。オペレーターは、「リージョン2 のリーダーをストア 5 に移行する」や「リージョン2 のレプリカをストア 1、4、5 に移行する」などのスケジュール設定タスクを実行します。

演算子は[スケジューラ](#scheduler)によって計算および生成することも、外部 API によって作成することもできます。

### オペレータステップ {#operator-step}

オペレータ ステップは、オペレータの実行におけるステップです。オペレータには通常、複数のオペレータ ステップが含まれます。

現在、PD によって生成される利用可能なステップは次のとおりです。

-   `TransferLeader` : 指定されたメンバーにリーダーシップを移譲する
-   `AddPeer` : 指定されたストアにピアを追加します
-   `RemovePeer` :リージョンのピアを削除します
-   `AddLearner` : 指定されたストアに学習者を追加する
-   `PromoteLearner` : 指定された学習者を投票メンバーに昇格させる
-   `SplitRegion` : 指定されたリージョンを2つに分割します

## ポ {#p}

### パーティショニング {#partitioning}

[パーティショニング](/partitioned-table.md) 、テーブルを物理的に小さなテーブル パーティションに分割することを指します。これは、RANGE、LIST、HASH、KEY パーティション分割などのパーティション メソッドによって実行できます。

### 保留中/ダウン {#pending-down}

「保留中」と「ダウン」は、ピアの 2 つの特別な状態です。保留中は、フォロワーまたは学習者のRaftログがリーダーのログと大きく異なることを示します。保留中のフォロワーはリーダーとして選出できません。「ダウン」は、ピアがリーダーに長時間応答しなくなった状態を指し、通常は対応するノードがダウンしているか、ネットワークから分離されていることを意味します。

### 配置Driver（PD） {#placement-driver-pd}

配置Driver(PD) は、メタデータの保存、トランザクション タイムスタンプの[タイムスタンプ オラクル (TSO)](/tso.md)割り当て、TiKV 上のデータ配置の調整、および[TiDBダッシュボード](/dashboard/dashboard-overview.md)実行を担当する[TiDBアーキテクチャ](/tidb-architecture.md#placement-driver-pd-server)のコアコンポーネントです。詳細については、 [TiDB スケジューリング](/tidb-scheduling.md)参照してください。

### ポイントゲット {#point-get}

ポイント取得とは、一意のインデックスまたはプライマリ インデックスによって 1 行のデータを読み取ることを意味し、返される結果セットは最大 1 行になります。

### ポイントインタイムリカバリ (PITR) {#point-in-time-recovery-pitr}

ポイントインタイムリカバリ (PITR) を使用すると、データを特定の時点 (たとえば、意図しない`DELETE`ステートメントの直前) に復元できます。詳細については、 [TiDB ログ バックアップと PITRアーキテクチャ](/br/br-log-architecture.md)参照してください。

### 述語列 {#predicate-columns}

ほとんどの場合、SQL 文を実行するときに、オプティマイザは一部の列 ( `WHERE` 、 `JOIN` 、 `ORDER BY` 、および`GROUP BY`文の列など) の統計情報のみを使用します。これらの使用される列は述語列と呼ばれます。詳細については、 [いくつかの列の統計を収集する](/statistics.md#collect-statistics-on-some-columns)参照してください。

## 質問 {#q}

### 1秒あたりのクエリ数 (QPS) {#queries-per-second-qps}

1 秒あたりのクエリ数 (QPS) は、データベース サービスが 1 秒あたりに処理するクエリの数であり、データベース スループットの主要なパフォーマンス メトリックとして機能します。

### クォータリミッター {#quota-limiter}

クォータ リミッターは、TiDB v6.0.0 で導入された実験的機能です。TiKV がデプロイされているマシンのリソースが限られている場合 (たとえば、4v CPU と 16 Gメモリのみ)、TiKV のフォアグラウンドが読み取りおよび書き込み要求を過度に処理すると、バックグラウンドで使用される CPU リソースがそのような要求の処理に占有され、TiKV のパフォーマンスの安定性に影響します。この状況を回避するには、 [クォータ関連の設定項目](/tikv-configuration-file.md#quota)設定して、フォアグラウンドで使用される CPU リソースを制限できます。

## R {#r}

### Raft Engine {#raft-engine}

Raft Engineは、ログ構造設計の組み込み永続storageエンジンです。TiKV が複数の Raft ログを保存できるように構築されています。v5.4 以降、TiDB はログstorageエンジンとしてRaft Engineの使用をサポートしています。詳細については、 [Raft Engine](/tikv-configuration-file.md#raft-engine)参照してください。

### リージョン分割 {#region-split}

TiKV クラスター内の領域は最初は分割されませんが、データが書き込まれるにつれて徐々に分割されます。このプロセスは、リージョン分割と呼ばれます。

リージョン分割のメカニズムは、1 つの初期リージョンを使用してキー空間全体をカバーし、リージョンのサイズまたはキーの数がしきい値に達するたびに既存の領域を分割して新しい領域を生成することです。

### リージョン/ ピア /Raftグループ {#region-peer-raft-group}

リージョンはTiKV のデータstorageの最小部分であり、それぞれがデータの範囲 (デフォルトでは 256 MiB) を表します。各リージョンには、デフォルトで 3 つのレプリカがあります。リージョンのレプリカはピアと呼ばれます。同じリージョンの複数のピアは、 Raftコンセンサス アルゴリズムを介してデータを複製するため、ピアもRaftインスタンスのメンバーになります。TiKV は、Multi-Raft を使用してデータを管理します。つまり、各リージョンには、対応する分離されたRaftグループが存在します。

### リモート プロシージャ コール (RPC) {#remote-procedure-call-rpc}

リモート プロシージャ コール (RPC) は、ソフトウェア コンポーネント間の通信方法です。TiDB クラスターでは、TiDB、TiKV、 TiFlashなどのさまざまなコンポーネント間の通信に gRPC 標準が使用されます。

### リクエストユニット (RU) {#request-unit-ru}

リクエスト ユニット (RU) は、TiDB のリソース使用に関する統一された抽象化ユニットです。1 [リソース管理](/tidb-resource-control.md)組み合わせて使用して、リソース使用を管理します。

### 復元する {#restore}

復元はバックアップ操作の逆です。準備されたバックアップからデータを取得して、システムを以前の状態に戻すプロセスです。

## S {#s}

### スケジューラ {#scheduler}

スケジューラは、PD 内のスケジュール タスクを生成するコンポーネントです。PD 内の各スケジューラは独立して実行され、異なる目的を果たします。よく使用されるスケジューラは次のとおりです。

-   `balance-leader-scheduler` : リーダーの分布を均等にする
-   `balance-region-scheduler` : ピアの分散をバランスさせる
-   `hot-region-scheduler` : ホットリージョンの分布をバランスさせる
-   `evict-leader-{store-id}` : ノードのすべてのリーダーを排除します (ローリング アップグレードでよく使用されます)

### 静的ソートテーブル / ソート文字列テーブル (SST) {#static-sorted-table-sorted-string-table-sst}

静的ソートテーブルまたはソート文字列テーブルは、RocksDB ( [ティクヴ](/storage-engine/rocksdb-overview.md)で使用されるstorageエンジン) で使用されるファイルstorage形式です。

### 店 {#store}

ストアとは、TiKV クラスター内のstorageノード ( `tikv-server`のインスタンス) を指します。各ストアには対応する TiKV インスタンスがあります。

## T {#t}

### タイムスタンプ オラクル (TSO) {#timestamp-oracle-tso}

TiKV は分散storageシステムであるため、単調に増加するタイムスタンプを割り当てるために、グローバルタイミングサービスである Timestamp Oracle (TSO) が必要です。TiKV では、このような機能は PD によって提供され、Google [スパナ](http://static.googleusercontent.com/media/research.google.com/en//archive/spanner-osdi2012.pdf)では、この機能は複数のアトミック時計と GPS によって提供されます。詳細については、 [TSO](/tso.md)参照してください。

### Top SQL {#top-sql}

Top SQL は、指定された時間範囲内で TiDB または TiKV ノードの高負荷の原因となっている SQL クエリを見つけるのに役立ちます。詳細については、 [Top SQLユーザードキュメント](/dashboard/top-sql.md)参照してください。

### 1秒あたりのトランザクション数 (TPS) {#transactions-per-second-tps}

1 秒あたりのトランザクション数 (TPS) は、データベースが 1 秒あたりに処理するトランザクションの数であり、データベースのパフォーマンスとスループットを測定するための主要な指標として機能します。

## あなた {#u}

### 統一リソース識別子 (URI) {#uniform-resource-identifier-uri}

Uniform Resource Identifier (URI) は、リソースを識別するための標準化された形式です。詳細については、Wikipedia の[統一リソース識別子](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier)参照してください。

### ユニバーサルユニーク識別子 (UUID) {#universally-unique-identifier-uuid}

ユニバーサルユニーク識別子 (UUID) は、データベース内のレコードを一意に識別するために使用される 128 ビット (16 バイト) の生成 ID です。詳細については、 [言語](/best-practices/uuid.md)参照してください。
