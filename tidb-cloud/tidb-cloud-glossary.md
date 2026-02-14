---
title: TiDB Cloud Glossary
summary: TiDB Cloudで使用される用語を学習します。
category: glossary
aliases: ['/ja/tidbcloud/glossary']
---

# TiDB Cloud用語集 {#tidb-cloud-glossary}

## あ {#a}

### ACID {#acid}

ACIDとは、トランザクションの4つの主要な特性、すなわち原子性、一貫性、独立性、そして永続性を指します。これらの特性については、以下でそれぞれ説明します。

-   **原子性**とは、操作のすべての変更が実行されるか、まったく実行されないかのいずれかを意味します。TiDBは、トランザクションの原子性を実現するために、主キーを格納する[TiDBリージョン](#region)のキーの原子性を保証します。

-   **一貫性と**は、トランザクションが常にデータベースをある一貫性のある状態から別の一貫性のある状態へと移行させることを意味します。TiDBでは、データをメモリに書き込む前にデータの一貫性が確保されます。

-   **分離と**は、処理中のトランザクションが完了するまで他のトランザクションから参照できないことを意味します。これにより、同時実行中のトランザクションは一貫性を損なうことなくデータの読み書きを行うことができます。TiDBは現在、分離レベル`REPEATABLE READ`をサポートしています。

-   **耐久性**とは、トランザクションが一度コミットされると、システム障害が発生してもコミットされた状態が維持されることを意味します。TiKVは永続storageを使用して耐久性を確保します。

## C {#c}

### チャット2クエリ {#chat2query}

Chat2Queryは、SQLエディタに統合されたAIを活用した機能で、自然言語による指示を用いてSQLクエリの生成、デバッグ、書き換えを支援します。詳細については、 [AI支援SQLエディターでデータを探索](/tidb-cloud/explore-data-with-chat2query.md)ご覧ください。

さらに、 TiDB CloudはAWSでホストされているTiDB Cloud Starterクラスター向けにChat2Query APIを提供しています。有効化すると、 TiDB Cloudは自動的に**Chat2Query**というシステムデータアプリと、データサービスにChat2Dataエンドポイントを作成します。このエンドポイントを呼び出すことで、AIが指示を与えることでSQL文を生成・実行できるようになります。詳細については、 [Chat2Query APIを使い始める](/tidb-cloud/use-chat2query-api.md)ご覧ください。

### クレジット {#credit}

TiDB Cloudは、概念実証（PoC）ユーザーに一定数のクレジットを提供しています。1クレジットは1米ドルに相当します。クレジットは、有効期限が切れる前にTiDBクラスタの料金をお支払いいただくためにご利用いただけます。

## D {#d}

### データアプリ {#data-app}

[データサービス（ベータ版）](#data-service)のデータアプリは、特定のアプリケーションのデータにアクセスするために使用できるエンドポイントのコレクションです。APIキーを使用して認証設定を構成し、データアプリ内のエンドポイントへのアクセスを制限できます。

詳細については[データアプリを管理する](/tidb-cloud/data-service-manage-data-app.md)参照してください。

### データサービス {#data-service}

データサービス（ベータ版）を使用すると、カスタムAPI [終点](#endpoint)を使用したHTTPSリクエストを介してTiDB Cloudデータにアクセスできます。この機能は、サーバーレスアーキテクチャを使用してコンピューティングリソースと柔軟なスケーリングを処理するため、インフラストラクチャやメンテナンスコストを気にすることなく、エンドポイントのクエリロジックに集中できます。

詳細については[データサービスの概要](/tidb-cloud/data-service-overview.md)参照してください。

### 直接顧客 {#direct-customer}

直接顧客とは、 TiDB Cloudを購入し、PingCAPから直接請求書を支払うエンドカスタマーです。これは[MSP顧客](#msp-customer)とは区別されます。

## E {#e}

### 終点 {#endpoint}

Data Service のエンドポイントは、SQL 文を実行するためにカスタマイズできる Web API です。SQL 文のパラメータ（ `WHERE`句で使用する値など）を指定できます。クライアントがエンドポイントを呼び出し、リクエスト URL でパラメータの値を指定すると、エンドポイントは指定されたパラメータを使用して対応する SQL 文を実行し、結果を HTTP レスポンスの一部として返します。

詳細については[エンドポイントを管理する](/tidb-cloud/data-service-manage-endpoint.md)参照してください。

## F {#f}

### 全文検索 {#full-text-search}

意味的類似性に重点を置く[ベクトル検索](/ai/concepts/vector-search-overview.md)は異なり、全文検索では正確なキーワードで文書を検索できます。検索拡張生成（RAG）シナリオでは、全文検索とベクトル検索を併用することで、検索品質を向上させることができます。

詳細については、 [SQLによる全文検索](https://docs.pingcap.com/developer/vector-search-full-text-search-sql)および[Pythonによる全文検索](https://docs.pingcap.com/developer/vector-search-full-text-search-python)を参照してください。

## M {#m}

### メンバー {#member}

組織に招待され、組織とこの組織のクラスターへのアクセス権を持つユーザー。

### MPP {#mpp}

TiDB v5.0以降、 TiFlashノードを介した大規模並列処理（MPP）アーキテクチャが導入され、大規模な結合クエリの実行ワークロードをTiFlashノード間で共有できるようになりました。MPPモードを有効にすると、TiDBはコストに基づいて、MPPフレームワークを使用して計算を実行するかどうかを判断します。MPPモードでは、計算中に結合キーがExchange操作を通じて再分配されるため、各TiFlashノードへの計算負荷が分散され、計算速度が向上します。詳細については、 [TiFlash MPPモードを使用する](/tiflash/use-tiflash-mpp-mode.md)参照してください。

### MSP顧客 {#msp-customer}

マネージドサービスプロバイダー（MSP）顧客とは、 TiDB Cloudを購入し、MSPチャネルを通じて請求書を支払うエンドカスタマーです。これは[直接顧客](#direct-customer)とは区別されます。

### マネージドサービスプロバイダー（MSP） {#managed-service-provider-msp}

マネージド サービス プロバイダー (MSP) は、 TiDB Cloudを再販し、 TiDB Cloud組織管理、課金サービス、技術サポートなどを含む付加価値サービスを提供するパートナーです。

## 北 {#n}

### ノード {#node}

データ インスタンス (TiKV)、コンピューティング インスタンス (TiDB)、または分析インスタンス (TiFlash) のいずれかを指します。

## お {#o}

### 組織 {#organization}

任意の数の複数のメンバー アカウントを持つ管理アカウントを含む、 TiDB Cloudアカウントを管理するために作成するエンティティ。

### 組織メンバー {#organization-members}

組織メンバーとは、組織のオーナーまたはプロジェクトオーナーから組織への参加を招待されたユーザーです。組織メンバーは、組織のメンバーを閲覧したり、組織内のプロジェクトに招待したりできます。

## P {#p}

### ポリシー {#policy}

特定のアクションやリソースへのアクセスなど、ロール、ユーザー、または組織に適用される権限を定義するドキュメント。

### プロジェクト {#project}

組織が作成したプロジェクトに基づいて、人員、インスタンス、ネットワークなどのリソースをプロジェクトごとに個別に管理することができ、プロジェクト間のリソースが互いに干渉することはありません。

### プロジェクトメンバー {#project-members}

プロジェクトメンバーとは、組織内の1つ以上のプロジェクトに参加するよう招待されたユーザーです。プロジェクトメンバーは、クラスタ、ネットワークアクセス、バックアップ、その他のリソースを管理できます。

## R {#r}

### ごみ箱 {#recycle-bin}

有効なバックアップがある削除されたクラスターのデータが保存される場所です。バックアップされたTiDB Cloud Dedicated クラスターが削除されると、クラスターの既存のバックアップ ファイルはごみ箱に移動されます。自動バックアップからのバックアップ ファイルの場合、ごみ箱には指定された期間保持されます。バックアップの保持期間は**バックアップ設定**で設定でき、デフォルトは 7 日間です。手動バックアップからのバックアップ ファイルの場合、有効期限はありません。データ損失を避けるため、データを新しいクラスターに時間内に復元することを忘れないでください。クラスターに**バックアップがない**場合、削除されたクラスターはここに表示されないことに注意してください。

### 地域 {#region}

-   TiDB Cloudリージョン

    TiDB Cloudクラスターがデプロイされる地理的領域。TiDB TiDB Cloudリージョンは少なくとも 3 つのアベイラビリティーゾーンで構成され、クラスターはこれらのゾーンにまたがってデプロイされます。

-   TiDBリージョン

    TiDBにおけるデータの基本単位。TiKVはキーバリュー空間を連続するキーセグメントに分割し、各セグメントはリージョンと呼ばれます。各リージョンのデフォルトのサイズ制限は96MBですが、変更可能です。

### レプリカ {#replica}

同じリージョンまたは別のリージョンに配置され、同じデータを含む独立したデータベース。レプリカは、災害復旧やパフォーマンス向上のためによく使用されます。

### レプリケーション容量ユニット (RCU) {#replication-capacity-unit-rcu}

TiDB Cloudは、 [チェンジフィード](/tidb-cloud/changefeed-overview.md)の容量をTiCDCレプリケーション容量ユニット（RCU）で測定します。クラスターの変更フィードを作成する際に、適切な仕様を選択できます。RCUが大きいほど、レプリケーションパフォーマンスが向上します。これらのTiCDC変更フィードRCUに対して料金が発生します。詳細については、 [チェンジフィードコスト](https://www.pingcap.com/tidb-dedicated-pricing-details/#changefeed-cost)ご覧ください。

### リクエスト容量単位 (RCU) {#request-capacity-unit-rcu}

リクエスト容量ユニット（RCU）は、 TiDB Cloud Essential クラスターにプロビジョニングされたコンピューティング容量を表す測定単位です。1 RCU は、1 秒あたり一定数の RU を処理できる固定量のコンピューティングリソースを提供します。プロビジョニングする RCU の数によって、クラスターのベースラインパフォーマンスとスループット容量が決まります。詳細については、 [TiDB Cloud Essential の価格詳細](https://www.pingcap.com/tidb-cloud-essential-pricing-details/)ご覧ください。

### リクエストユニット（RU） {#request-unit-ru}

TiDB Cloud StarterとEssentialでは、リクエストユニット（RU）は、データベースへの1回のリクエストで消費されるリソース量を表す測定単位です。リクエストで消費されるRUの量は、操作の種類や取得または変更されるデータの量など、さまざまな要因によって異なります。ただし、 TiDB Cloud StarterとEssentialの課金モデルは異なります。

-   TiDB Cloud Starterは、消費されたRUの合計数に基づいて課金されます。詳細については、 [TiDB Cloud Starter の価格詳細](https://www.pingcap.com/tidb-cloud-starter-pricing-details/)ご覧ください。
-   TiDB Cloud Essentialは、プロビジョニングされた[リクエスト容量単位（RCU）](#request-capacity-unit-rcu) RCUの数に基づいて課金されます。1 RCUは、1秒あたり一定数のRUを処理できる固定量のコンピューティングリソースを提供します。詳細については、 [TiDB Cloud Essential の価格詳細](https://www.pingcap.com/tidb-cloud-essential-pricing-details/)ご覧ください。

TiDB Cloud DedicatedおよびTiDB Self-Managedにおいて、リクエストユニット（RU）はシステムリソースの消費量を表すリソース抽象化単位であり、現在CPU、IOPS、IO帯域幅のメトリクスが含まれます。リクエストユニットは、**課金目的ではなく**、リソース制御機能によってデータベースリクエストで消費されるリソースを制限、分離、管理するために使用されます。詳細については、 [リソース制御を使用してリソースグループの制限とフロー制御を実現する](/tidb-resource-control-ru-groups.md)ご覧ください。

## S {#s}

### 支出限度額 {#spending-limit}

[支出限度額](/tidb-cloud/manage-serverless-spend-limit.md) 、特定のワークロードに対して1ヶ月あたりに支出可能な最大金額を表します。これは、TiDB Cloud Starterクラスターの予算を設定できるコスト管理メカニズムです。支出限度額が0に設定されている場合、クラスターは無料のままです。支出限度額が0より大きい場合は、クレジットカードを追加する必要があります。

## T {#t}

### TiDB クラスター {#tidb-cluster}

機能的な作業データベースを形成する[ティドブ](https://docs.pingcap.com/tidb/stable/tidb-computing) 、 [TiKV](https://docs.pingcap.com/tidb/stable/tidb-storage) 、 [配置Driver](https://docs.pingcap.com/tidb/stable/tidb-scheduling) (PD)、および[TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview)のノードの集合。

### TiDBノード {#tidb-node}

トランザクションストアまたは分析ストアから返されたクエリからデータを集約するコンピューティングノード。TiDBノードの数を増やすと、クラスターが処理できる同時クエリの数が増加します。

### TiDB X {#tidb-x}

クラウドネイティブなオブジェクトstorageをTiDBのバックボーンとする、新しい分散SQLアーキテクチャ。TiDB Xは、コンピューティングとstorageを分離することで、ワークロードパターン、ビジネスサイクル、データ特性にリアルタイムで適応し、TiDBをインテリジェントに拡張することを可能にします。

TiDB Xアーキテクチャは現在、<customcontent plan="starter,essential,dedicated"> TiDB Cloud StarterとEssential</customcontent><customcontent plan="premium"> TiDB Cloud Starter、Essential、および Premium</customcontent>詳細については、 [TiDB X のご紹介: AI 時代の分散 SQL の新たな基盤](https://www.pingcap.com/blog/introducing-tidb-x-a-new-foundation-distributed-sql-ai-era/)および[PingCAP、SCaiLE Summit 2025でTiDB Xと新しいAI機能を発表](https://www.pingcap.com/press-release/pingcap-launches-tidb-x-new-ai-capabilities/)を参照してください。

### TiFlashノード {#tiflash-node}

TiKV からデータをリアルタイムで複製し、リアルタイムの分析ワークロードをサポートする分析storageノード。

### TiKVノード {#tikv-node}

オンライントランザクション処理（OLTP）データを保存するstorageノードです。高可用性を実現するために、3ノードの倍数（例：3、6、9）で拡張され、2つのノードがレプリカとして機能します。TiKVノードの数を増やすと、全体のスループットが向上します。

### トラフィックフィルター {#traffic-filter}

SQLクライアント経由でTiDB Cloudクラスターへのアクセスが許可されるIPアドレスとクラスレス・インタードメイン・ルーティング（CIDR）アドレスのリスト。トラフィックフィルターはデフォルトで空です。

## V {#v}

### ベクトル検索 {#vector-search}

[ベクトル検索](/ai/concepts/vector-search-overview.md)は、データの意味を優先して関連性の高い結果を提供する検索手法です。キーワードの完全一致や単語の出現頻度に依存する従来の全文検索とは異なり、ベクター検索は、テキスト、画像、音声など様々なデータタイプを高次元ベクトルに変換し、それらのベクトル間の類似性に基づいてクエリを実行します。この検索手法は、データの意味と文脈情報を捉えることで、ユーザーの検索意図をより正確に理解します。検索語がデータベース内のコンテンツと完全に一致しない場合でも、ベクター検索はデータのセマンティクスを分析することで、ユーザーの検索意図に沿った結果を提供できます。

### 仮想プライベートクラウド {#virtual-private-cloud}

リソースに対して管理されたネットワーク サービスを提供する、論理的に分離された仮想ネットワーク パーティション。

### VPC {#vpc}

Virtual Private Cloud の略。

### VPCピアリング {#vpc-peering}

異なる VPC ネットワーク内のワークロードがプライベートに通信できるように、仮想プライベート クラウド ( [VPC](#vpc) ) ネットワークを接続できます。

### VPCピアリング接続 {#vpc-peering-connection}

2 つの仮想プライベート クラウド (VPC) 間のネットワーク接続。これにより、プライベート IP アドレスを使用して VPC 間のトラフィックをルーティングし、データ転送を容易にすることができます。
