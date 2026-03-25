---
title: Glossary
summary: TiDBに関する用語集。
---

# 用語集 {#glossary}

この用語集では、TiDBプラットフォームに関連する主要な用語の定義を提供します。

その他の利用可能な用語集：

-   [TiDBデータ移行用語集](/dm/dm-glossary.md)
-   [TiCDC用語集](/ticdc/ticdc-glossary.md)
-   [TiDB Lightning用語集](/tidb-lightning/tidb-lightning-glossary.md)

<TabsPanel letters="ABCDEGHIKLMOPQRSTUV" />

## <a id="A" class="letter" href="#A">A</a> {#a-id-a-class-letter-href-a-a-a}

### ACID {#acid}

ACIDとは、トランザクションの4つの主要な特性、すなわち原子性、一貫性、分離性、および永続性を指します。これらの特性はそれぞれ以下で説明します。

-   **原子性**とは、操作による変更がすべて実行されるか、あるいは全く実行されないかのどちらかであることを意味します。TiDBは、トランザクションの原子性を実現するために、プライマリキーを格納する[リージョン](#regionpeerraft-group)の要素の原子性を保証します。

-   **一貫性と**は、トランザクションによってデータベースが常に一貫性のある状態から別の一貫性のある状態へと移行することを意味します。TiDBでは、メモリにデータを書き込む前にデータの一貫性が確保されます。

-   **分離とは**、処理中のトランザクションが完了するまで他のトランザクションから見えないことを意味します。これにより、同時実行トランザクションは一貫性を損なうことなくデータの読み書きを行うことができます。詳細については、 [TiDBトランザクション分離レベル](/transaction-isolation-levels.md#tidb-transaction-isolation-levels)参照してください。

-   **永続性**とは、一度トランザクションがコミットされると、システム障害が発生した場合でもコミットされた状態が維持されることを意味します。TiKVは永続storageを使用して永続性を確保しています。

## <a id="B" class="letter" href="#B">B</a> {#a-id-b-class-letter-href-b-b-a}

### バックアップと復元 (BR) {#backup-x26-restore-br}

BRは TiDB のバックアップおよび復元ツールです。詳細については[BR概要](/br/backup-and-restore-overview.md)参照してください。

TiDBでは、 `br`はバックアップまたはリストアに使用される[br コマンドラインツール](/br/use-br-command-line-tool.md)です。

### ベースラインの取得 {#baseline-capturing}

ベースラインキャプチャは、キャプチャ条件を満たすクエリをキャプチャし、それらのバインディングを作成します。これは、 [アップグレード中に実行プランの退行を防ぐ](/sql-plan-management.md#prevent-regression-of-execution-plans-during-an-upgrade)に使用されます。

### バッチテーブル作成 {#batch-create-table}

バッチテーブル作成機能は、テーブルをバッチで作成することで、一度に複数のテーブルを作成する処理を大幅に高速化します。たとえば、 [バックアップと復元 (BR)](/br/backup-and-restore-overview.md)ツールを使用して数千のテーブルを復元する場合、この機能は全体のリカバリ時間を短縮するのに役立ちます。詳細については、 [バッチテーブル作成](/br/br-batch-create-table.md)参照してください。

### バケツ {#bucket}

[リージョン](#regionpeerraft-group)は論理的にバケットと呼ばれるいくつかの小さな範囲に分割されます。TiKV はバケットごとにクエリ統計を収集し、バケットの状態を PD に報告します。詳細については、 [バケット設計ドキュメント](https://github.com/tikv/rfcs/blob/master/text/0082-dynamic-size-region.md#bucket)を参照してください。

## <a id="C" class="letter" href="#C">C</a> {#a-id-c-class-letter-href-c-c-a}

### キャッシュされたテーブル {#cached-table}

キャッシュテーブル機能を使用すると、TiDBはテーブル全体のデータをTiDBサーバーのメモリにロードし、TiKVにアクセスすることなくメモリから直接テーブルデータを取得するため、読み取りパフォーマンスが向上します。

### クラスタ {#cluster}

クラスターとは、サービスを提供するために連携して動作するノードのグループです。分散システムにおいてクラスターを使用することで、TiDBは単一ノード構成と比較して、より高い可用性と優れた拡張性を実現します。

TiDBデータベースの分散アーキテクチャでは：

-   TiDBノードは、クライアントとのやり取りのためのスケーラブルなSQLレイヤーを提供します。
-   PDノードは、TiDBに対して堅牢なメタデータレイヤーを提供する。
-   TiKVノードは、 Raftプロトコルを使用することで、TiDB向けに高可用性、拡張性、および耐障害性に優れたstorageを提供します。

詳細については、 [TiDBアーキテクチャ](/tidb-architecture.md)参照してください。

### パーティションを合体させる {#coalesce-partition}

パーティションの結合は、ハッシュまたはキーでパーティションテーブルのパーティション数を減らす方法です。詳細については、 [ハッシュとキーのパーティションを管理する](/partitioned-table.md#manage-hash-and-key-partitions)参照してください。

### カラムファミリー（CF） {#column-family-cf}

RocksDBとTiKVでは、カラムファミリー（CF）は、データベース内のキーと値のペアの論理的なグループを表します。

### 共通テーブル式（CTE） {#common-table-expression-cte}

共通テーブル式 (CTE) を使用すると、 [`WITH`](/sql-statements/sql-statement-with.md)句を使用して SQL ステートメント内で複数回参照できる一時的な結果セットを定義できます。これにより、ステートメントの可読性と実行効率が向上します。詳細については、 [共通テーブル式](/develop/dev-guide-use-common-table-expression.md)参照してください。

### 継続的なプロファイリング {#continuous-profiling}

継続的プロファイリングは、システムコールレベルでのリソースオーバーヘッドを監視する方法です。継続的プロファイリングを使用すると、TiDB はパフォーマンスの問題をきめ細かく監視し、フレームグラフを使用して運用チームが根本原因を特定するのに役立ちます。詳細については、 [TiDBダッシュボードインスタンスプロファイリング - 継続的プロファイリング](/dashboard/continuous-profiling.md)参照してください。

### コプロセッサー {#coprocessor}

コプロセッサーは、TiDBと計算ワークロードを共有するコプロセッシングメカニズムです。storageレイヤー（TiKVまたはTiFlash）に配置され、リージョンごとにTiDBからの計算[押し下げる](/functions-and-operators/expressions-pushed-down.md)共同で処理します。

## <a id="D" class="letter" href="#D">D</a> {#a-id-d-class-letter-href-d-d-a}

### Dumpling {#dumpling}

Dumplingは、TiDB、MySQL、またはMariaDBに保存されているデータをSQLまたはCSVデータファイルとしてエクスポートするためのデータエクスポートツールです。論理的なフルバックアップやエクスポートにも使用できます。さらに、 DumplingはAmazon S3へのデータエクスポートもサポートしています。

詳細については、 [Dumplingを使用してデータをエクスポートする](/dumpling-overview.md)参照してください。

### データ定義言語（DDL） {#data-definition-language-ddl}

データ定義言語（DDL）は、テーブルやその他のオブジェクトの作成、変更、削除を扱うSQL標準の一部です。詳細については、 [DDL入門](/best-practices/ddl-introduction.md)参照してください。

### データ移行（DM） {#data-migration-dm}

データ移行 (DM) は、MySQL 互換データベースから TiDB へデータを移行するためのツールです。DM は、MySQL 互換データベースインスタンスからデータを読み込み、TiDB ターゲットインスタンスに適用します。詳細については、 [DMの概要](/dm/dm-overview.md)参照してください。

### データ変更言語（DML） {#data-modification-language-dml}

データ変更言語（DML）は、SQL標準の一部であり、テーブルへの行の挿入、更新、削除を扱うものです。

### 開発マイルストーンリリース（DMR） {#development-milestone-release-dmr}

開発マイルストーンリリース（DMR）は、最新の機能を導入するTiDBリリースですが、長期サポートは提供されません。詳細については、 [TiDB バージョン管理](/releases/versioning.md)参照してください。

### 災害復旧（DR） {#disaster-recovery-dr}

ディザスターリカバリー（DR）には、将来発生する災害からデータやサービスを復旧するために使用できるソリューションが含まれます。TiDB は、バックアップやスタンバイクラスタへのレプリケーションなど、さまざまなディザスターリカバリーソリューションを提供しています。詳細については、 [TiDB災害復旧ソリューションの概要](/dr-solution-introduction.md)参照してください。

### 分散実行フレームワーク（DXF） {#distributed-execution-framework-dxf}

分散実行フレームワーク (DXF) は、TiDB が特定のタスク (インデックスの作成やデータのインポートなど) を一元的にスケジュールし、分散的に実行するために使用するフレームワークです。DXF は、リソースの使用を制御し、コア業務トランザクションへの影響を軽減しながら、クラスタ リソースを効率的に使用するように設計されています。詳細については、 [DXFの概要](/tidb-distributed-execution-framework.md)参照してください。

### 動的剪定 {#dynamic-pruning}

動的プルーニングモードは、TiDBがパーティションテーブルにアクセスするモードの1つです。動的プルーニングモードでは、各演算子が複数のパーティションへの直接アクセスをサポートします。そのため、TiDBはUnionを使用しなくなります。Union操作を省略することで、実行効率が向上し、Unionの同時実行による問題を回避できます。

## <a id="E" class="letter" href="#E">E</a> {#a-id-e-class-letter-href-e-e-a}

### 式インデックス or 関数インデックス {#expression-index}

式インデックスは、式に基づいて作成される特殊なタイプのインデックスです。式インデックスが作成されると、TiDBはこのインデックスを式ベースのクエリに使用できるようになり、クエリのパフォーマンスが大幅に向上します。

詳細については、 [インデックスの作成 -式インデックス or 関数インデックス](/sql-statements/sql-statement-create-index.md#expression-index)参照してください。

## <a id="G" class="letter" href="#G">G</a> {#a-id-g-class-letter-href-g-g-a}

### ごみ収集（GC） {#garbage-collection-gc}

ガベージコレクション（GC）は、不要になったデータをクリアしてリソースを解放するプロセスです。TiKV GC プロセスについては、 [GCの概要](/garbage-collection-overview.md)参照してください。

### 一般提供開始（GA） {#general-availability-ga}

機能の一般提供開始（GA）とは、その機能が完全にテストされ、本番環境での使用が一般的に可能になったことを意味します。TiDBの機能は、バージョン[DMR](#development-milestone-release-dmr)とバージョン[LTS](#long-term-support-lts)の両方でGAとしてリリースされる可能性があります。ただし、TiDBはDMRのパッチリリースを提供していないため、本番本番での使用にはLTSリリースを使用することをお勧めします。

### グローバルトランザクション識別子（GTID） {#global-transaction-identifiers-gtids}

グローバルトランザクション識別子（GTID）は、MySQLバイナリログで使用される一意のトランザクションIDで、どのトランザクションが複製されたかを追跡するために使用されます。1 [データ移行（DM）](/dm/dm-overview.md) 、これらのIDを使用して一貫性のあるレプリケーションを保証します。

## <a id="H" class="letter" href="#H">H</a> {#a-id-h-class-letter-href-h-h-a}

### ホットスポット {#hotspot}

ホットスポットとは、TiKV の読み取りおよび書き込みワークロードが 1 つまたは少数のリージョンまたはノードに集中している状況を指します。これによりパフォーマンスのボトルネックが発生し、最適なシステムパフォーマンスが妨げられる可能性があります。ホットスポットの問題を解決するには、 [ホットスポットの問題をトラブルシューティングする](/troubleshoot-hot-spot-issues.md)参照してください。

### ハイブリッドトランザクション・分析処理（HTAP） {#hybrid-transactional-and-analytical-processing-htap}

ハイブリッドトランザクションおよび分析処理（HTAP）は、同一データベース内でOLTP（オンライントランザクション処理）とOLAP（オンライン分析処理）の両方のワークロードを可能にするデータベース機能です。TiDBでは、行storageにTiKV、列storageにTiFlashを使用することでHTAP機能が提供されます。詳細については、 [TiDB HTAPクイックスタート](/quick-start-with-htap.md)および[HTAPを探索する](/explore-htap.md)参照してください。

## <a id="I" class="letter" href="#I">私</a> {#a-id-i-class-letter-href-i-i-a}

### インメモリ悲観的ロック {#in-memory-pessimistic-lock}

インメモリ悲観的ロックは、TiDB v6.0.0 で導入された新機能です。この機能が有効になっている場合、悲観的ロックは通常、リージョンリーダーのメモリにのみ保存され、ディスクに永続化されたり、 Raftを介して他のレプリカに複製されたりすることはありません。この機能により、悲観的ロックの取得にかかるオーバーヘッドを大幅に削減し、悲観的トランザクションのスループットを向上させることができます。

### インデックスマージ {#index-merge}

インデックスマージは、TiDB v4.0で導入されたテーブルアクセス方法です。この方法を使用すると、TiDBオプティマイザはテーブルごとに複数のインデックスを使用し、各インデックスから返される結果をマージできます。場合によっては、この方法によってフルテーブルスキャンが回避され、クエリの効率が向上します。インデックスマージは、v5.4以降、一般提供（GA）機能となっています。

## <a id="K" class="letter" href="#K">K</a> {#a-id-k-class-letter-href-k-k-a}

### キー管理サービス（KMS） {#key-management-service-kms}

キー管理サービス（KMS）は、秘密鍵を安全な方法でstorageおよび取得することを可能にします。例としては、AWS KMS、Google Cloud KMS、HashiCorp Vaultなどがあります。TiDBのさまざまなコンポーネントは、KMSを使用してstorage暗号化および関連サービス用の鍵を管理できます。

### キーバリュー（KV） {#key-value-kv}

キーバリュー（KV）は、値を一意のキーに関連付けることで情報を保存する方法であり、迅速なデータ検索を可能にします。TiDBはTiKVを使用してテーブルとインデックスをキーバリューペアにマッピングし、データベース全体で効率的なデータstorageとアクセスを実現します。

## <a id="L" class="letter" href="#L">L</a> {#a-id-l-class-letter-href-l-l-a}

### Leader／Follower／Learner {#leader-follower-learner}

Raftグループ（ [仲間](#regionpeerraft-group)構成）では、Leader、Follower、Learnerがそれぞれ役割を担います。リーダーはすべてのクライアント要求を処理し、フォロワーにデータを複製します。グループリーダーが故障した場合、フォロワーの中から1人が新しいリーダーに選出されます。学習者は投票権を持たないフォロワーであり、複製データの追加処理のみに関与します。

### 軽量ディレクトリアクセスプロトコル（LDAP） {#lightweight-directory-access-protocol-ldap}

軽量ディレクトリアクセスプロトコル (LDAP) は、情報を含むディレクトリにアクセスするための標準化された方法です。アカウントおよびユーザーデータの管理によく使用されます。TiDB は[LDAP認証プラグイン](/security-compatibility-with-mysql.md#authentication-plugin-status)を介して LDAP をサポートしています。

### ロックビュー {#lock-view}

ロックビュー機能は、悲観的ロックにおけるロックの競合とロック待機に関する詳細情報を提供するため、DBAはトランザクションのロック状況を把握し、デッドロックの問題をトラブルシューティングするのに便利です。

詳細については、システムテーブルのドキュメント[`TIDB_TRX`](/information-schema/information-schema-tidb-trx.md) [`DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md)および[`DEADLOCKS`](/information-schema/information-schema-deadlocks.md)を参照してください。

### 長期サポート（LTS） {#long-term-support-lts}

長期サポート (LTS) とは、長期間にわたって徹底的にテストおよびメンテナンスされるソフトウェア バージョンを指します。詳細については、 [TiDB バージョン管理](/releases/versioning.md)参照してください。

## <a id="M" class="letter" href="#M">M</a> {#a-id-m-class-letter-href-m-m-a}

### 超並列処理（MPP） {#massively-parallel-processing-mpp}

TiDBはv5.0以降、 TiFlashノードを介して大規模並列処理（MPP）アーキテクチャを導入し、大規模な結合クエリの実行ワークロードをTiFlashノード間で共有します。MPPモードが有効になっている場合、TiDBはコストに基づいて、計算を実行するためにMPPフレームワークを使用するかどうかを決定します。MPPモードでは、結合キーは計算中にExchange操作によって再分配され、計算負荷が各TiFlashノードに分散され、計算が高速化されます。詳細については、 [TiFlash MPPモードを使用する](/tiflash/use-tiflash-mpp-mode.md)参照してください。

### マルチバージョン同時実行制御 (MVCC) {#multi-version-concurrency-control-mvcc}

[MVCC](https://en.wikipedia.org/wiki/Multiversion_concurrency_control)は、TiDBをはじめとするデータベースにおける並行性制御メカニズムです。トランザクションによって読み取られたメモリを処理することで、TiDBへの同時アクセスを実現し、同時読み取りと書き込みの競合によって発生するブロッキングを回避します。

## <a id="O" class="letter" href="#O">O</a> {#a-id-o-class-letter-href-o-o-a}

### 旧価格 {#old-value}

TiCDCが出力する増分変更ログにおける「元の値」。TiCDCが出力する増分変更ログに「元の値」を含めるかどうかを指定できます。

### オンライン分析処理（OLAP） {#online-analytical-processing-olap}

オンライン分析処理（OLAP）とは、データレポート作成や複雑なクエリなど、分析タスクに特化したデータベースワークロードを指します。OLAPの特徴は、多数の行にわたる大量のデータを処理する、読み取り負荷の高いクエリです。

### オンライントランザクション処理（OLTP） {#online-transaction-processing-oltp}

オンライン・トランザクション処理（OLTP）とは、レコードの選択、挿入、更新、削除といったトランザクション処理に特化したデータベースワークロードを指します。

### メモリ不足 (OOM) {#out-of-memory-oom}

メモリ不足 (OOM) は、メモリ不足によりシステムが故障する状況です。詳細については、 [TiDBのメモリ不足問題​​のトラブルシューティング](/troubleshoot-tidb-oom.md)参照してください。

### オペレーター {#operator}

オペレーターとは、スケジューリングの目的でリージョンに適用される一連のアクションのことです。オペレーターは、「リージョン2のリーダーをストア5に移行する」や「リージョン2のレプリカをストア1、4、5に移行する」といったスケジューリングタスクを実行します。

演算子は、 [スケジューラ](#scheduler)によって計算および生成されるか、外部 API によって作成されます。

### オペレーターステップ {#operator-step}

演算子ステップとは、演算子の実行における手順のことです。通常、1つの演算子は複数の演算子ステップで構成されます。

現在、PDによって生成される利用可能なステップは以下のとおりです。

-   `TransferLeader` ：指定されたメンバーにリーダーシップを移譲する
-   `AddPeer` : 指定されたストアにピアを追加します
-   `RemovePeer` :リージョンのピアを削除します
-   `AddLearner` : 指定されたストアに学習者を追加します
-   `PromoteLearner` ：指定された学習者を投票権を持つメンバーに昇格させる
-   `SplitRegion` ：指定されたリージョンを2つに分割します

### 楽観的な取引 {#optimistic-transaction}

楽観的トランザクションとは、楽観的並行性制御を使用するトランザクションであり、一般的に並行環境で競合を引き起こしません。楽観的トランザクションを有効にすると、TiDB はトランザクションが最終的にコミットされたときにのみ競合チェックを行います。楽観的トランザクションモードは、読み取りが多く書き込みが少ない並行シナリオに適しており、TiDB のパフォーマンスを向上させることができます。

詳細については、 [TiDBの楽観的トランザクションモデル](/optimistic-transaction.md)参照してください。

## <a id="P" class="letter" href="#P">P</a> {#a-id-p-class-letter-href-p-p-a}

### パーティショニング {#partitioning}

[パーティショニング](/partitioned-table.md) 、テーブルを物理的に小さなテーブルパーティションに分割することを指し、これはRANGE、LIST、HASH、KEYパーティショニングなどのパーティション方式によって実行できます。

### PD Control（pd-ctl） {#pd-control-pd-ctl}

PD Control (pd-ctl) は、TiDB クラスタ内の Placement Driver (PD) と対話するために使用されるコマンドライン ツールです。これを使用して、クラスタの状態情報を取得したり、クラスタ構成を変更したりできます。詳細については、 [PD Controlユーザーガイド](/pd-control.md)参照してください。

### 保留中／ダウン中 {#pending-down}

「保留中」と「ダウン」は、ピアの2つの特別な状態です。「保留中」とは、フォロワーまたは学習者のRaftログがリーダーのログと大きく異なる状態を指します。保留中のフォロワーはリーダーに選出されません。「ダウン」とは、ピアが長時間リーダーに応答しなくなった状態を指し、通常は対応するノードがダウンしているか、ネットワークから孤立していることを意味します。

### 配置Driver（PD） {#placement-driver-pd}

配置Driver(PD) は、メタデータの保存、トランザクション タイムスタンプの[タイムスタンプオラクル（TSO）](/tso.md) 、TiKV 上でのデータ配置の調整、および[TiDBダッシュボード](/dashboard/dashboard-overview.md)実行を担当する[TiDBアーキテクチャ](/tidb-architecture.md#placement-driver-pd-server)の中核コンポーネントです。詳細については、 [TiDBスケジューリング](/tidb-scheduling.md)参照してください。

### 配置ルール {#placement-rules}

配置ルールは、TiKVクラスタにおけるデータの配置を設定するために使用されます。この機能を使用すると、テーブルとパーティションを異なるリージョン、データセンター、キャビネット、またはホストに展開するように指定できます。使用例としては、低コストでデータ可用性戦略を最適化すること、ローカルの古いデータの読み取りのためにローカルデータレプリカが利用可能であることを保証すること、およびローカルのデータコンプライアンス要件に準拠することなどが挙げられます。

詳細については、 [SQLにおける配置ルール](/placement-rules-in-sql.md)参照してください。

### ポイント獲得 {#point-get}

ポイント取得とは、一意のインデックスまたは主インデックスによってデータの単一行を読み取ることを意味し、返される結果セットは最大で1行です。

### 特定時点復旧（PITR） {#point-in-time-recovery-pitr}

ポイントインタイムリカバリ（PITR）を使用すると、データを特定の時点（たとえば、意図しない`DELETE`の直前）に復元できます。詳細については、 [TiDBログバックアップとPITRアーキテクチャ](/br/br-log-architecture.md)参照してください。

### 述語列 {#predicate-columns}

ほとんどの場合、SQL ステートメントを実行する際、オプティマイザは一部の列 ( `WHERE` `GROUP BY`の列など) の統計情報のみを使用します。これらの使用される列`ORDER BY`述語列と呼ばれます。詳細については、 [いくつかの列の統計情報を収集する](/statistics.md#collect-statistics-on-some-columns) `JOIN`してください。

## <a id="Q" class="letter" href="#Q">Q</a> {#a-id-q-class-letter-href-q-q-a}

### 1秒あたりのクエリ数（QPS） {#queries-per-second-qps}

1秒あたりのクエリ数（QPS）とは、データベースサービスが1秒間に処理するクエリの数であり、データベースのスループットを示す重要なパフォーマンス指標です。

### クォータリミッター {#quota-limiter}

クォータリミッターは、TiDB v6.0.0 で導入された実験的機能です。TiKV がデプロイされているマシンにリソース制限がある場合（例えば、CPU が 4V、メモリが 16GB しかない場合）、TiKV のフォアグラウンドが読み書き要求を過剰に処理すると、バックグラウンドで使用される CPU リソースがこれらの要求の処理に使用され、TiKV のパフォーマンスの安定性に影響します。この状況を回避するために、クォータリミッターを[クォータ関連の設定項目](/tikv-configuration-file.md#quota)に設定して、フォアグラウンドで使用される CPU リソースを制限できます。

## <a id="R" class="letter" href="#R">R</a> {#a-id-r-class-letter-href-r-r-a}

### Raft Engine {#raft-engine}

Raft Engine は、ログ構造設計の組み込み型永続storageエンジンです。TiKV 用に構築されており、複数の Raft ログを保存します。v5.4 以降、TiDB はRaft Engine をログstorageエンジンとして使用することをサポートしています。詳細については、 [Raft Engine](/tikv-configuration-file.md#raft-engine)参照してください。

### リージョン分割 {#region-split}

TiKVクラスタ内の領域は、最初は分割されておらず、データが書き込まれるにつれて徐々に分割されていきます。このプロセスはリージョン分割と呼ばれます。

リージョン分割の仕組みは、まず1つの初期リージョンを使用して鍵空間全体をカバーし、リージョンのサイズまたは鍵の数が閾値に達するたびに、既存の領域を分割して新しい領域を生成するというものです。

### リージョン／仲間／Raftグループ {#region-peer-raft-group}

TiKV におけるデータstorageの最小単位はリージョンであり、それぞれがデータ範囲 (デフォルトでは 256 MiB) を表します。各リージョンには、デフォルトで 3 つのレプリカがあります。リージョンのレプリカはピアと呼ばれます。同じリージョンの複数のピアは、 Raftコンセンサスアルゴリズムを使用してデータを複製するため、ピアもRaftインスタンスのメンバーとなります。TiKV は、マルチ Raft を使用してデータを管理します。つまり、各リージョンには、対応する独立したRaftグループが存在します。

### リモートプロシージャコール（RPC） {#remote-procedure-call-rpc}

リモートプロシージャコール（RPC）は、ソフトウェアコンポーネント間の通信手段です。TiDBクラスタでは、TiDB、TiKV、 TiFlashなどの異なるコンポーネント間の通信にgRPC標準が使用されます。

### リクエストユニット（RU） {#request-unit-ru}

リクエストユニット（RU）は、TiDBにおけるリソース使用状況を統一的に抽象化した単位です。リソース使用状況を管理するために、 [リソース制御](/tidb-resource-control-ru-groups.md)と組み合わせて使用​​されます。

### 復元する {#restore}

リストアはバックアップ操作の逆の操作です。これは、事前に準備されたバックアップからデータを取得することで、システムを以前の状態に戻すプロセスです。

### RocksDB {#rocksdb}

[RocksDB](https://rocksdb.org/)は、キーバリューstorageと読み書き機能を提供するLSMツリー構造のエンジンです。Facebookによって開発され、LevelDBをベースとしています。RocksDBはTiKVの中核となるstorageエンジンです。

## <a id="S" class="letter" href="#S">S</a> {#a-id-s-class-letter-href-s-s-a}

### スケジューラ {#scheduler}

スケジューラはPDのコンポーネントであり、スケジューリングタスクを生成します。PDの各スケジューラは独立して動作し、それぞれ異なる目的を果たします。一般的に使用されるスケジューラは以下のとおりです。

-   `balance-leader-scheduler` ：リーダーの分布のバランスを取る
-   `balance-region-scheduler` ：ピアの分布のバランスを取る
-   `hot-region-scheduler` ：高温領域の分布のバランスをとる
-   `evict-leader-{store-id}` ：ノードのすべてのリーダーを追い出す（ローリングアップグレードによく使用される）

### Security強化モード（SEM） {#security-enhanced-mode-sem}

Security強化モード（SEM）は、TiDB管理者の権限をより細かく制御するために使用されます。1 [セキュリティ強化Linux](https://en.wikipedia.org/wiki/Security-Enhanced_Linux)のシステムに触発されたSEMは、 `SUPER`権限を持つユーザーの機能を制限し、代わりに`RESTRICTED`つのきめ細かい権限を必要とします。これらの権限は、特定の管理アクションを制御するために明示的に付与される必要があります。

詳細については、 [システム変数に関するドキュメント - `tidb_enable_enhanced_security`](/system-variables.md#tidb_enable_enhanced_security)参照してください。

### ステイル読み取り {#stale-read}

ステイル読み取りは、TiDBに保存されているデータの履歴バージョンを読み取るためにTiDBが適用するメカニズムです。このメカニズムを使用すると、特定の時点または指定された期間内の対応する履歴データを読み取ることができ、storageノード間のデータ複製によって発生するレイテンシーを削減できます。Stale ステイル読み取りを使用する場合、TiDBはデータ読み取り用にレプリカをランダムに選択するため、すべてのレプリカがデータ読み取りに使用可能になります。

詳細については、 [ステイル読み取り](/stale-read.md)参照してください。

### 静的ソート済みテーブル／ソート済み文字列テーブル（SST） {#static-sorted-table-sorted-string-table-sst}

静的ソートテーブルまたはソート文字列テーブルは、RocksDB（ [ティクヴ](/storage-engine/rocksdb-overview.md)で使用されているstorageエンジン）で使用されるファイルstorage形式です。

### 店 {#store}

ストアとは、TiKV クラスタ内のstorageノード (インスタンス`tikv-server` ) を指します。各ストアには、対応する TiKV インスタンスがあります。

## <a id="T" class="letter" href="#T">T</a> {#a-id-t-class-letter-href-t-t-a}

### 一時テーブル {#temporary-table}

一時テーブルを使用すると、中間計算結果を一時的に保存できるため、テーブルの作成と削除を繰り返す必要がなくなります。データが不要になると、TiDB は一時テーブルを自動的にクリーンアップして再利用します。この機能により、アプリケーションロジックが簡素化され、テーブル管理のオーバーヘッドが削減され、パフォーマンスが向上します。

詳細については、 [一時テーブル](/temporary-tables.md)参照してください。

### TiCDC {#ticdc}

TiCDC は、TiDB からさまざまなダウンストリーム ターゲットへの増分データ レプリケーションを可能にするツール[TiCDC](/ticdc/ticdc-overview.md) 。これらのダウンストリーム ターゲットには、他の TiDB インスタンス、MySQL 互換データベース、storageサービス、ストリーミング プロセッサ (Kafka や Pulsar など) が含まれます。TiCDC は、アップストリーム TiKV からデータ変更ログを取得し、それを順序付き行レベル変更データに解析し、ダウンストリームにデータを出力します。TiCDC の概念と用語の詳細については、 [TiCDC用語集](/ticdc/ticdc-glossary.md)参照してください。

### TiDB Lightning {#tidb-lightning}

[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)は、テラバイト規模のデータを静的ファイルからTiDBクラスタにインポートするためのツールです。TiDBクラスタへの初期データインポートによく使用されます。

TiDB Lightningの概念と用語の詳細については、 [TiDB Lightning用語集](/tidb-lightning/tidb-lightning-glossary.md)参照してください。

### TiFlash {#tiflash}

[TiFlash](/tiflash/tiflash-overview.md)は、TiDB の HTAPアーキテクチャの重要なコンポーネントです。これは、強力な一貫性と優れた分離性の両方を提供する TiKV のカラム型拡張です。TiFlashは、 **Raft Learnerプロトコル**を使用して TiKV からデータを非同期的に複製することで、カラム型レプリカを維持します。読み取りに関しては、 **Raftコンセンサス インデックス**と**MVCC (マルチ バージョン同時実行制御)**を活用して、**スナップショット分離の**一貫性を実現します。このアーキテクチャは、HTAP ワークロードにおける分離と同期の課題に効果的に対処し、リアルタイムのデータ一貫性を維持しながら、効率的な分析クエリを可能にします。

### TiKV MVCC インメモリエンジン (IME) {#tikv-mvcc-in-memory-engine-ime}

[TiKV MVCC インメモリエンジン](/tikv-in-memory-engine.md) (IME) は、最新の書き込み済み MVCC バージョンをメモリにキャッシュし、TiDB とは独立した MVCC GC メカニズムを実装して、多数の MVCC 履歴バージョンを含むクエリを高速化します。

### タイムスタンプオラクル（TSO） {#timestamp-oracle-tso}

TiKVは分散storageシステムであるため、単調増加するタイムスタンプを割り当てるためのグローバルタイミングサービスであるタイムスタンプオラクル（TSO）が必要です。TiKVでは、この機能はPDによって提供され、Google [スパナ](http://static.googleusercontent.com/media/research.google.com/en//archive/spanner-osdi2012.pdf)では、この機能は複数のアトミック時計とGPSによって提供されます。詳細については、 [TSO](/tso.md)参照してください。

### TiUP {#tiup}

TiUP[TiUP](/tiup/tiup-overview.md)は、TiDB クラスタのデプロイ、アップグレード、管理、および TiDB、PD、TiKV を含む TiDB クラスタ内のさまざまなコンポーネントの管理に使用される管理ツールです。TiUP を使用すると、単一のコマンドを実行するだけで TiDB 内の任意のコンポーネントを簡単に実行できるため、管理プロセスが大幅に簡素化されます。

### Top SQL {#top-sql}

Top SQLは、指定された時間範囲内でTiDBまたはTiKVノードの負荷を高める原因となっているSQLクエリを特定するのに役立ちます。詳細については、 [Top SQLドキュメント](/dashboard/top-sql.md)参照してください。

### 1秒あたりのトランザクション数（TPS） {#transactions-per-second-tps}

トランザクション/秒（TPS）とは、データベースが1秒間に処理するトランザクションの数であり、データベースのパフォーマンスとスループットを測定するための重要な指標です。

## <a id="U" class="letter" href="#U">U</a> {#a-id-u-class-letter-href-u-u-a}

### 統一リソース識別子（URI） {#uniform-resource-identifier-uri}

URI（Uniform Resource Identifier）は、リソースを識別するための標準化された形式です。詳細については、Wikipediaの[統一リソース識別子](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier)参照してください。

### ユニバーサル一意識別子（UUID） {#universally-unique-identifier-uuid}

UUID（Universally Unique Identifier）は、データベース内のレコードを一意に識別するために使用される128ビット（16バイト）の生成されたIDです。詳細については、 [UUID](/best-practices/uuid.md)参照してください。

## <a id="V" class="letter" href="#V">V</a> {#a-id-v-class-letter-href-v-v-a}

### ベクトル検索 {#vector-search}

[ベクトル検索](/ai/concepts/vector-search-overview.md)検索は、データの意味を優先して関連性の高い検索結果を提供する検索方法です。キーワードの完全一致や単語の出現頻度に依存する従来の全文検索とは異なり、ベクトル検索はテキスト、画像、音声などの様々なデータタイプを高次元ベクトルに変換し、これらのベクトルの類似性に基づいてクエリを実行します。この検索方法は、データの意味と文脈情報を捉え、ユーザーの意図をより正確に理解することを可能にします。検索語がデータベース内のコンテンツと完全に一致しない場合でも、ベクトル検索はデータの意味を分析することで、ユーザーの意図に沿った結果を提供できます。
