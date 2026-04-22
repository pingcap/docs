---
title: TiDB Cloud Glossary
summary: TiDB Cloudで使用される用語を学びましょう。
category: glossary
aliases: ['/ja/tidbcloud/glossary']
---

# TiDB Cloud用語集 {#tidb-cloud-glossary}

## A {#a}

### ACID {#acid}

ACIDとは、トランザクションの4つの主要な特性、すなわち原子性、一貫性、分離性、および永続性を指します。これらの特性はそれぞれ以下で説明します。

-   **原子性**とは、操作のすべての変更が実行されるか、まったく実行されないかのどちらかであることを意味します。TiDB は[TiDBリージョン](#region)です。

-   **一貫性と**は、トランザクションによってデータベースが常に一貫性のある状態から別の一貫性のある状態へと移行することを意味します。TiDBでは、メモリにデータを書き込む前にデータの一貫性が確保されます。

-   **分離とは**、進行中のトランザクションが完了するまで他のトランザクションから見えないことを意味します。これにより、同時実行トランザクションは一貫性を損なうことなくデータの読み書きを行うことができます。TiDB は現在、 `REPEATABLE READ`の分離レベルをサポートしています。

-   **永続性**とは、一度トランザクションがコミットされると、システム障害が発生した場合でもコミットされた状態が維持されることを意味します。TiKVは永続storageを使用して永続性を確保しています。

## C {#c}

### Chat2Query {#chat2query}

Chat2Query は、SQL エディターに統合された AI を活用した機能で、ユーザーが自然言語命令を使用して SQL クエリを生成、デバッグ、または書き換えるのを支援します。詳細については、[AI支援型SQLエディタでデータを探索しよう](/tidb-cloud/explore-data-with-chat2query.md)参照してください。

さらに、 TiDB Cloud は、AWS でホストされているTiDB Cloud Starterインスタンス向けに Chat2Query API を提供しています。有効化すると、 TiDB Cloud は自動的に**Chat2Query**というシステムデータアプリと、データサービスに Chat2Data エンドポイントを作成します。このエンドポイントを呼び出すことで、指示を与えることにより AI に SQL ステートメントを生成および実行させることができます。詳細については、 [Chat2Query API を使い始めましょう](/tidb-cloud/use-chat2query-api.md)参照してください。.

### クラスタ {#cluster}

TiDB Cloudでは、クラスターとは、ノードトポロジー、インスタンスタイプ、storage構成、スケーリングモデルなどの明確なインフラストラクチャの詳細を含む、専用のクラウドデプロイメントのことです。

TiDB Cloudのプランの中で、このデプロイメントモデルを採用しているのはTiDB Cloud Dedicatedクラスタのみです。

### クレジット {#credit}

TiDB Cloudは、概念実証（PoC）ユーザー向けに一定数のクレジットを提供しています。1クレジットは1米ドルに相当します。クレジットは有効期限が切れる前に料金の支払いに使用できます。

## D {#d}

### データアプリ {#data-app}

データサービス[データサービス（ベータ版）](#data-service)のデータアプリは、特定のアプリケーションのデータにアクセスするために使用できるエンドポイントの集合です。APIキーを使用して認証設定を構成することで、データアプリ内のエンドポイントへのアクセスを制限できます。

詳細については、[データアプリを管理する](/tidb-cloud/data-service-manage-data-app.md)参照してください。

### データサービス {#data-service}

データサービス（ベータ版）を使用すると、カスタムAPI[終点](#endpoint)を使用してHTTPSリクエスト経由でTiDB Cloudデータにアクセスできます。この機能はサーバーレスアーキテクチャを採用し、コンピューティングリソースと柔軟なスケーリングを処理するため、インフラストラクチャやメンテナンスコストを気にすることなく、エンドポイントのクエリロジックに集中できます。

詳細については、[データサービス概要](/tidb-cloud/data-service-overview.md)ご覧ください。

### 直接顧客 {#direct-customer}

直接顧客とは、 TiDB Cloudを購入し、PingCAP から直接請求書を支払うエンド顧客です。 [MSPのお客様](#msp-customer)とは区別されます。

## E {#e}

### 終点 {#endpoint}

Data Service のエンドポイントは、SQL ステートメントを実行するようにカスタマイズできる Web API です。SQL ステートメントには、 `WHERE`句で使用される値などのパラメーターを指定できます。クライアントがエンドポイントを呼び出し、リクエスト URL のパラメーターに値を指定すると、エンドポイントは指定されたパラメーターを使用して対応する SQL ステートメントを実行し、結果を HTTP レスポンスの一部として返します。

詳細については、[エンドポイントを管理する](/tidb-cloud/data-service-manage-endpoint.md)参照してください。

## F {#f}

### 全文検索 {#full-text-search}

意味的な類似性に焦点を当てる[ベクトル検索](/ai/concepts/vector-search-overview.md)とは異なり、全文検索では正確なキーワードに基づいて文書を取得できます。検索拡張生成（RAG）シナリオでは、全文検索とベクトル検索を組み合わせて使用​​することで、検索品質を向上させることができます。

詳細については、 [SQLによる全文検索](/ai/guides/vector-search-full-text-search-sql.md)および[Pythonによる全文検索](/ai/guides/vector-search-full-text-search-python.md)参照してください。

## M {#m}

### メンバー {#member}

TiDB Cloudの[組織](#organization)に招待されたユーザー。

### MPP {#mpp}

バージョン5.0以降、TiDBはTiFlashノードを介した大規模並列処理（MPP）アーキテクチャを導入し、大規模な結合クエリの実行ワークロードをTiFlashノード間で共有します。MPPモードが有効になっている場合、TiDBはコストに基づいて、計算にMPPフレームワークを使用するかどうかを決定します。MPPモードでは、結合キーは計算中にExchange操作によって再分配され、計算負荷が各TiFlashノードに分散され、計算速度が向上します。詳細については、 [TiFlash MPPモードを使用する](/tiflash/use-tiflash-mpp-mode.md)参照してください。 .

### MSP顧客 {#msp-customer}

マネージドサービスプロバイダー（MSP）の顧客とは、 TiDB Cloudを購入し、MSPチャネルを通じて請求書を支払うエンドユーザーのことです。これは[直接の顧客](#direct-customer)とは異なります。

### マネージドサービスプロバイダー（MSP） {#managed-service-provider-msp}

マネージドサービスプロバイダー（MSP）とは、 TiDB Cloudを再販し、 TiDB Cloudの組織管理、請求サービス、技術サポートなどを含む（ただしこれらに限定されない）付加価値サービスを提供するパートナーです。

## N {#n}

### ノード {#node}

データインスタンス（TiKV）、コンピューティングインスタンス（TiDB）、または分析インスタンス（TiFlash）のいずれかを指します。

## O {#o}

### 組織 {#organization}

TiDB Cloudアカウント (任意の数の複数のメンバー アカウントを持つ管理アカウントを含む)、[プロジェクト](#project)、および[リソース](#tidb-cloud-resource)を管理するための最上位のコンテナー。

### 組織のメンバー {#organization-members}

組織メンバーとは、組織のオーナーまたはプロジェクトのオーナーから組織への参加を招待されたユーザーのことです。組織メンバーは組織のメンバーを閲覧したり、組織内のプロジェクトに招待されたりすることができます。

## P {#p}

### ポリシー {#policy}

役割、ユーザー、または組織に適用される権限（特定のアクションやリソースへのアクセスなど）を定義する文書。

### プロジェクト {#project}

TiDB Cloudでは、プロジェクトを使用してTiDBリソースをグループ化および管理できます。

-   <CustomContent plan="starter,essential,dedicated">TiDB Cloud StarterとEssential</CustomContent> <CustomContent plan="premium">TiDB Cloud Starter、 Essential、およびPremium</CustomContent>インスタンスの場合、プロジェクトはオプションです。つまり、これらのインスタンスをプロジェクトにグループ化するか、組織レベルでこれらのインスタンスを保持することができます。
-   TiDB Cloud Dedicatedクラスターの場合、プロジェクトが必要です。

プロジェクトの機能はプロジェクトの種類によって異なります。現在、プロジェクトには以下の3種類があります。

-   **TiDB Dedicatedプロジェクト**：このプロジェクトタイプは、 TiDB Cloud Dedicatedクラスタでのみ使用されます。RBAC、ネットワーク、メンテナンス、アラート購読、暗号化アクセスなど、 TiDB Cloud Dedicatedクラスタの設定をプロジェクトごとに個別に管理できます。
-   **TiDB X プロジェクト**: このプロジェクト タイプは、TiDB X インスタンス ( <CustomContent plan="starter,essential,dedicated">TiDB Cloud StarterとEssential</CustomContent> <CustomContent plan="premium">TiDB Cloud Starter、 Essential、およびPremium</CustomContent> ) でのみ使用されます。プロジェクトごとに TiDB X インスタンスの RBAC を管理できます。TiDB X プロジェクトは、[**私のTiDB**](https://tidbcloud.com/tidbs)ページでプロジェクトを作成する際のデフォルトのプロジェクト タイプです。
-   **TiDB X 仮想プロジェクト**: このプロジェクトは仮想であり、管理機能は提供しません。これは、どのプロジェクトにも属さない TiDB X インスタンス ( <CustomContent plan="starter,essential,dedicated">TiDB Cloud StarterとEssential</CustomContent> <CustomContent plan="premium">TiDB Cloud Starter、 Essential、およびPremium</CustomContent> ) の仮想コンテナとして機能し、プロジェクト ID を使用してTiDB Cloud API を介してこれらのインスタンスにアクセスできます。各組織には一意の仮想プロジェクト ID があります。この ID は[**私のTiDB**](https://tidbcloud.com/tidbs)ページのプロジェクト ビューから取得できます。

これらのプロジェクト タイプの違いの詳細については、 [プロジェクト](/tidb-cloud/manage-user-access.md#projects)を参照してください。

### プロジェクトメンバー {#project-members}

プロジェクトメンバーとは、組織の1つ以上のプロジェクトへの参加を招待されたユーザーのことです。

## R {#r}

### リサイクルボックス {#recycle-bin}

削除された[TiDB Cloudのリソース](#tidb-cloud-resource)のデータと有効なバックアップが保存される場所。

バックアップされたTiDB Cloudリソースが削除されると、その既存のバックアップ ファイルはごみ箱に移動されます。自動バックアップからのバックアップ ファイルについては、ごみ箱に指定された期間保持されます。バックアップの保持期間は**「バックアップ設定」**で設定でき、デフォルトは 7 日です。手動バックアップからのバックアップ ファイルには有効期限はありません。データ損失を防ぐため、新しいTiDB Cloudリソースにデータを速やかに復元してください。なお、 TiDB Cloudリソース**にバックアップがない**場合、削除されたリソースはごみ箱に表示されません。

<CustomContent plan="starter,essential,dedicated">

現在、ごみ箱機能はTiDB Cloud Dedicatedクラスタのみがサポートしています。

</CustomContent>

<CustomContent plan="premium">

現在、ごみ箱機能はTiDB Cloud PremiumインスタンスとTiDB Cloud Dedicatedクラスタのみをサポートしています。

</CustomContent>

### 地域 {#region}

-   TiDB Cloudリージョン

    TiDB Cloudリソースがデプロイされる地理的領域。TiDB TiDB Cloudリージョンは少なくとも3つのアベイラビリティゾーンで構成され、クラスターまたはインスタンスはこれらのゾーンにまたがってデプロイされます。

-   TiDBリージョン

    TiDBにおけるデータの基本単位。TiKVはキーバリュー空間を連続するキーセグメントに分割し、各セグメントをリージョンと呼びます。各リージョンのデフォルトのサイズ制限は96MBで、設定可能です。

### レプリカ {#replica}

同一または異なるリージョンに配置される、同じデータを含む独立したデータベース。レプリカは、ディザスタリカバリ目的やパフォーマンス向上のためによく使用される。

### レプリケーション容量ユニット（RCU） {#replication-capacity-unit-rcu}

TiDB Cloud は、TiCDC Replication Capacity Unit (RCU) の[変更フィード](/tidb-cloud/changefeed-overview.md)の容量を測定します。変更フィードを作成するときに、適切な仕様を選択できます。 RCU が高いほど、レプリケーションのパフォーマンスが向上します。これらの TiCDC 変更フィード RCU に対して料金が発生します。詳細については、 [変更フィードのコスト](https://www.pingcap.com/tidb-dedicated-pricing-details/#changefeed-cost)参照してください。

### 要求容量単位（RCU） {#request-capacity-unit-rcu}

リクエストキャパシティユニット（RCU）は、 TiDB Cloud Essentialインスタンスにプロビジョニングされたコンピューティング能力を表す単位です。1 RCUは、1秒あたり一定数のRUを処理できる固定量のコンピューティングリソースを提供します。プロビジョニングするRCUの数によって、TiDB Cloud Essentialインスタンスのベースラインパフォーマンスとスループット容量が決まります。詳細については、 [TiDB Cloud Essentialの料金詳細](https://www.pingcap.com/tidb-cloud-essential-pricing-details/)参照してください。

### リクエストユニット（RU） {#request-unit-ru}

TiDB Cloud StarterおよびEssentialでは、リクエストユニット（RU）は、データベースへの単一のリクエストによって消費されるリソース量を表す単位です。リクエストによって消費されるRUの量は、操作の種類や取得または変更されるデータの量など、さまざまな要因によって異なります。ただし、 TiDB Cloud StarterとEssentialの課金モデルは異なります。

-   TiDB Cloud Starter は、消費された RU の合計数に基づいて請求されます。詳細については、 [TiDB Cloud Starterの料金詳細](https://www.pingcap.com/tidb-cloud-starter-pricing-details/)を参照してください。
-   TiDB Cloud Essentialは、プロビジョニングされた[要求容量単位（RCU）](#request-capacity-unit-rcu)の数に基づいて請求されます。 1 つの RCU は、1 秒あたり特定の数の RU を処理できる固定量のコンピューティング リソースを提供します。詳細については、 [TiDB Cloud Essentialの料金詳細](https://www.pingcap.com/tidb-cloud-essential-pricing-details/)を参照してください。

TiDB Cloud Dedicatedおよび TiDB セルフマネージドの場合、リクエスト ユニット (RU) はシステム リソースの消費を表すリソース抽象化ユニットであり、これには現在 CPU、IOPS、および IO 帯域幅のメトリクスが含まれます。これは、**請求目的ではなく**、データベース要求によって消費されるリソースを制限、分離、管理するためにリソース制御機能によって使用されます。詳細については、[リソース制御を使用して、リソースグループの制限とフロー制御を実現します。](/tidb-resource-control-ru-groups.md)参照してください。

## S {#s}

### 支出限度額 {#spending-limit}

は、特定のワークロードに対して1か月あたりに費やすことができる最大金額を指します。これは、TiDB Cloud Starterインスタンスの予算を設定できるコスト管理メカニズムです。 [支出限度額](/tidb-cloud/manage-serverless-spend-limit.md)制限が0に設定されている場合、 TiDB Cloud Starterインスタンスは無料のままです。支出制限が0より大きい場合は、クレジットカードを追加する必要があります。

## T {#t}

### TiDBクラスター {#tidb-cluster}

TiDB Cloudでは、クラスターは TiDB の専用クラウド展開であり、ノードトポロジー ( [TiDB](/tidb-computing.md)ノード、[ティクヴ](/tidb-storage.md)、 [TiFlash](/tiflash/tiflash-overview.md)ノードの数を指定できます)、storage構成、スケーリングモデルなどのインフラストラクチャの詳細が明示的に含まれています。

### TiDBノード {#tidb-node}

トランザクションストアまたは分析ストアから返されたクエリのデータを集約するコンピューティングノード。TiDBノードの数を増やすと、TiDB Cloud Dedicatedクラスタが処理できる同時クエリの数が増加します。

### TiDB Cloudリソース {#tidb-cloud-resource}

TiDB Cloudリソースとは、管理可能なTiDB Cloudデプロイメント単位のことです。以下のいずれかになります。

-   TiDB X インスタンス ( [TiDB Xアーキテクチャ](/tidb-cloud/tidb-x-architecture.md)上に構築されたサービス指向のTiDB Cloudオファリング) ( <CustomContent plan="starter,essential,dedicated">TiDB Cloud StarterまたはEssential</CustomContent> <CustomContent plan="premium">TiDB Cloud Starter、 Essential、またはPremium</CustomContent>など)
-   TiDB Cloud Dedicatedクラスター

### TiDB X {#tidb-x}

TiDB Xは、クラウドネイティブなオブジェクトstorageをTiDBの基盤とする、新しい分散SQLアーキテクチャです。コンピューティングとstorageを分離することで、TiDBはワークロードパターン、ビジネスサイクル、データ特性にリアルタイムで適応し、インテリジェントなスケーリングを実現します。

TiDB Xアーキテクチャは、 <CustomContent plan="starter,essential,dedicated">TiDB Cloud StarterとEssential</CustomContent> <CustomContent plan="premium">TiDB Cloud Starter、 Essential、およびPremium</CustomContent>で利用できるようになりました。詳細については、 [TiDB Xのご紹介：AI時代の分散SQLのための新たな基盤](https://www.pingcap.com/blog/introducing-tidb-x-a-new-foundation-distributed-sql-ai-era/)および[PingCAPがSCaiLEサミット2025でTiDB Xと新たなAI機能を発表](https://www.pingcap.com/press-release/pingcap-launches-tidb-x-new-ai-capabilities/)参照してください。

### TiDB Xインスタンス {#tidb-x-instance}

TiDB Xインスタンスは、 [TiDB Xアーキテクチャ](/tidb-cloud/tidb-x-architecture.md)上に構築されたサービス指向のTiDB Cloudサービスです。基盤となるクラスタトポロジーの管理や理解は不要です。

TiDB Cloudプランのうち、 <CustomContent plan="starter,essential,dedicated">TiDB Cloud StarterとEssential</CustomContent> <CustomContent plan="premium">TiDB Cloud Starter、 Essential、およびPremium</CustomContent>は TiDB Xアーキテクチャを使用しています。したがって、「TiDB X インスタンス」という場合は、 <CustomContent plan="starter,essential,dedicated">TiDB Cloud StarterまたはEssential</CustomContent> <CustomContent plan="premium">TiDB Cloud Starter、 Essential、またはPremium</CustomContent>インスタンスを指します。

### TiFlashノード {#tiflash-node}

TiKVからリアルタイムでデータを複製し、リアルタイムの分析ワークロードをサポートする分析storageノード。

### TiKVノード {#tikv-node}

オンライントランザクション処理（OLTP）データを格納するstorageノード。高可用性を実現するため、3ノードの倍数（例えば、3、6、9）で拡張され、2つのノードがレプリカとして機能します。TiKVノードの数を増やすと、総スループットが向上します。

### トラフィックフィルター {#traffic-filter}

SQLクライアント経由でTiDB Cloudリソースへのアクセスが許可されているIPアドレスとクラスレスドメイン間ルーティング（CIDR）アドレスのリスト。トラフィックフィルタはデフォルトでは空です。

## V {#v}

### ベクトル検索 {#vector-search}

[ベクトル検索](/ai/concepts/vector-search-overview.md)、データの意味を優先して関連性の高い結果を提供する検索方法です。キーワードの完全一致や単語の出現頻度に依存する従来の全文検索とは異なり、ベクトル検索は、テキスト、画像、音声などのさまざまなデータタイプを高次元ベクトルに変換し、これらのベクトル間の類似性に基づいてクエリを実行します。この検索方法は、データの意味と文脈情報を捉え、ユーザーの意図をより正確に理解することを可能にします。検索語がデータベース内のコンテンツと完全に一致しない場合でも、ベクトル検索はデータの意味を分析することで、ユーザーの意図に沿った結果を提供できます。

### 仮想プライベートクラウド {#virtual-private-cloud}

論理的に分離された仮想ネットワークパーティションであり、お客様のリソースに対してマネージドネットワークサービスを提供します。

### VPC {#vpc}

仮想プライベートクラウドの略。

### VPCピアリング {#vpc-peering}

仮想プライベートクラウド（ [VPC](#vpc) ）ネットワークを接続し、異なるVPCネットワーク内のワークロードがプライベートに通信できるようにします。

### VPCピアリング接続 {#vpc-peering-connection}

2つの仮想プライベートクラウド（VPC）間のネットワーク接続であり、プライベートIPアドレスを使用してVPC間でトラフィックをルーティングし、データ転送を容易にします。
