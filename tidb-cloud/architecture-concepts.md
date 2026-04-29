---
title: Architecture
summary: TiDB Cloudのアーキテクチャ概念について学びましょう。
---

# アーキテクチャ {#architecture}

<CustomContent language="en,zh">

TiDB Cloudは、フルマネージド型のデータベース・アズ・ア・サービス（DBaaS）であり、オープンソースのHTAP（ハイブリッド・トランザクション・アンド・アナリティカル・プロセッシング）データベースである[TiDB](https://docs.pingcap.com/tidb/stable/overview)の柔軟性とパワーを、Amazon Web Services（AWS）、Google Cloud、Microsoft Azure、およびAlibaba Cloudに提供します。

</CustomContent>

<CustomContent language="ja">

TiDB Cloudは、フルマネージド型のデータベース・アズ・ア・サービス（DBaaS）であり、オープンソースのHTAP（ハイブリッド・トランザクション・アンド・アナリティカル・プロセッシング）データベースである[TiDB](https://docs.pingcap.com/tidb/stable/overview)の柔軟性とパワーを、Amazon Web Services（AWS）、Google Cloud、およびMicrosoft Azureに提供します。

</CustomContent>

TiDBはMySQLと互換性があるため、既存のアプリケーションとの移行や連携が容易です。また、小規模なワークロードから大規模な高性能システムまで、あらゆる規模のワークロードに対応できるシームレスな拡張性を提供します。トランザクション処理（OLTP）と分析処理（OLAP）の両方のワークロードを1つのシステムでサポートすることで、運用を簡素化し、リアルタイムのインサイトを実現します。

TiDB Cloudを使えば、データベースのスケーリング、複雑な管理タスクの処理が容易になり、信頼性が高く高性能なアプリケーションの開発に集中できます。

<CustomContent language="en,zh">

-   AWS向けに、 TiDB Cloudは、自動スケーリングとコスト効率の高いワークロード向けの**TiDB Cloud Starter** 、プロビジョニングされた容量を備えた本番環境対応ワークロード向けの**TiDB Cloud Essential** 、高いパフォーマンスと強化されたセキュリティを必要とするミッションクリティカルなワークロード向け**のTiDB Cloud Premium** 、専用リソースと高度な機能を備えたエンタープライズグレードのアプリケーション向けの**TiDB Cloud Dedicatedを**提供します。
-   Google CloudおよびAzure向けに、 TiDB Cloudは、専用リソースと高度な機能を備えたエンタープライズグレードのアプリケーション向けに、 **TiDB Cloud Dedicatedを**提供します。
-   Alibaba Cloud向けに、 TiDB Cloudは、自動スケーリングとコスト効率の高いワークロード向けの**TiDB Cloud Starter** 、プロビジョニングされた容量を備えた本番環境対応ワークロード向けの**TiDB Cloud Essential** 、そして高いパフォーマンスと強化されたセキュリティを必要とするミッションクリティカルなワークロード向けの**TiDB Cloud Premiumを**提供しています。

</CustomContent>

<CustomContent language="ja">

-   AWS向けに、 TiDB Cloudは、自動スケーリングとコスト効率の高いワークロード向けの**TiDB Cloud Starter** 、プロビジョニングされた容量を備えた本番環境対応ワークロード向けの**TiDB Cloud Essential** 、高いパフォーマンスと強化されたセキュリティを必要とするミッションクリティカルなワークロード向け**のTiDB Cloud Premium** 、専用リソースと高度な機能を備えたエンタープライズグレードのアプリケーション向けの**TiDB Cloud Dedicatedを**提供します。
-   Google CloudおよびAzure向けに、 TiDB Cloudは、専用リソースと高度な機能を備えたエンタープライズグレードのアプリケーション向けに、 **TiDB Cloud Dedicatedを**提供します。

</CustomContent>

## TiDB Cloud Starter {#tidb-cloud-starter}

TiDB Cloud Starterは、フルマネージド型のマルチテナントTiDBサービスです。MySQL互換の、自動スケーリング機能を備えた即時利用可能なデータベースを提供します。

Starterプランは、 TiDB Cloudを初めて利用する方に最適です。開発者や小規模チーム向けに、以下の機能を提供します。

-   **無料**：このプランは完全に無料で、利用開始にクレジットカードは必要ありません。
-   **ストレージ**：初期容量として、行ベースのstorageが5 GiB、列ベースのstorageが5 GiB提供されます。
-   **要求単位**: データベース操作の 5,000 万[要求単位（RU）](/tidb-cloud/tidb-cloud-glossary.md#request-unit-ru)が含まれます。

## TiDB Cloud Essential {#tidb-cloud-essential}

ワークロードが増加し、リアルタイムでの拡張性を必要とするアプリケーション向けに、 Essentialプランは以下の機能を備え、ビジネスの成長に合わせて柔軟かつ高性能なソリューションを提供します。

-   **機能強化**：Starterプランのすべての機能に加え、より大規模で複雑なワークロードを処理できる能力、および高度なセキュリティ機能が含まれています。
-   **自動スケーリング**：変化するワークロードの需要に効率的に対応するために、storageとコンピューティングリソースを自動的に調整します。
-   **高可用性**：組み込みの耐障害性と冗長性により、インフラストラクチャの障害発生時でも、アプリケーションの可用性と回復力が維持されます。
-   **予測可能な料金体系**：コンピューティングリソースのstorageとリクエストキャパシティユニット（RCU）に基づいて課金されるため、ニーズに合わせて拡張可能な透明性の高い使用量ベースの料金体系が提供され、予期せぬ追加料金なしで使用した分だけを支払うことができます。

TiDB Cloud Essentialは、さまざまな運用要件に対応するため、2種類の高可用性機能を提供します。

-   ゾーン高可用性：すべてのコンポーネントを同じ可用性ゾーン内に配置することで、ネットワークレイテンシーを低減します。
-   地域別高可用性：ノードを複数の可用性ゾーンに分散させることで、インフラストラクチャの最大限の分離性と冗長性を実現します。

詳細については、[TiDB Cloudにおける高可用性](/tidb-cloud/serverless-high-availability.md)参照してください。

## TiDB Cloudプレミアム {#tidb-cloud-premium}

管理された環境で高いパフォーマンスと強化されたセキュリティを必要とするミッションクリティカルなアプリケーション向けに、プレミアムプランは、以下の機能を備えた堅牢なインフラストラクチャと高度な制御を提供します。

-   **無制限の成長と自動スケーリング**：変化するワークロードに対応するためのシームレスなスケーリングを提供し、ビジネスに不可欠な業務の継続的な信頼性を確保します。
-   **パフォーマンス最適化**：高スループットかつ低遅延のワークロード向けに調整されており、より大きなリソース上限と、よりきめ細かなスケーリング制御を提供します。
-   **従量課金制**：実際の[要求容量単位（RCU）](/tidb-cloud/tidb-cloud-glossary.md#request-capacity-unit-rcu)消費量とstorage使用量に基づいて課金されます。この柔軟なモデルにより、バックエンドでの手動による過剰プロビジョニングが不要になります。
-   **高度なセキュリティ**：大規模企業や規制対象業界が必要とする、より高度なセキュリティ設定とコンプライアンス機能を提供します。

ミッション クリティカルなワークロードの稼働時間と回復力を最大化するために、 TiDB Cloud Premium は[地域的な高可用性](/tidb-cloud/serverless-high-availability.md#regional-high-availability-architecture)を提供し、複数のアベイラビリティ ゾーンにノードを分散して、ゾーン展開よりも高い冗長性を実現します。

## TiDB Cloud Dedicated {#tidb-cloud-dedicated}

TiDB Cloud Dedicatedは、ミッションクリティカルなビジネス向けに設計されており、複数のアベイラビリティゾーンにわたる高可用性、水平スケーリング、および完全なHTAP機能を提供します。

VPC、VM、マネージドKubernetesサービス、クラウドstorageなどの独立したクラウドリソース上に構築されたTiDB Cloud Dedicatedクラスターは、TiDBの全機能セットをサポートし、迅速なスケーリング、信頼性の高いバックアップ、特定のVPC内でのデプロイ、および地理的レベルのディザスタリカバリ。

![TiDB Cloud Dedicated Architecture](/media/tidb-cloud/tidb-cloud-dedicated-architecture.png)

## TiDB Cloudコンソール {#tidb-cloud-console}

[TiDB Cloudコンソール](https://tidbcloud.com/)TiDB CloudリソースのWebベースの管理インターフェースです。単一の使いやすいプラットフォームから、 TiDB Cloudリソースの管理、データのインポートまたは移行、パフォーマンス指標の監視、バックアップの設定、セキュリティ制御の設定、および他のクラウドサービスとの統合を行うためのツールを提供します。

## TiDB Cloud CLI（ベータ版） {#tidb-cloud-cli-beta}

TiDB Cloud CLI `ticloud`と、簡単なコマンドでターミナルから直接TiDB Cloud StarterおよびEssentialインスタンスを管理できます。次のようなタスクを実行できます。

-   TiDB Cloud StarterおよびEssentialインスタンスの作成、削除、一覧表示。
-   TiDB Cloud StarterおよびEssentialインスタンスへのデータインポート。
-   TiDB Cloud StarterおよびEssentialインスタンスからデータをエクスポートします。

詳細については、 [TiDB Cloud CLI リファレンス](/tidb-cloud/cli-reference.md)を参照してください。

## TiDB CloudAPI（ベータ版） {#tidb-cloud-api-beta}

TiDB Cloud APIは、RESTベースのインターフェースであり、 TiDB Cloud Starter、 TiDB Cloud Essential、 TiDB Cloud Premium、およびTiDB Cloud Dedicatedの各プランにわたるリソースをプログラムから管理するためのアクセスを提供します。これにより、 [TiDB Cloudデータサービス](/tidb-cloud/data-service-overview.md)におけるプロジェクト、クラスタ、バックアップ、リストア、データインポート、課金、その他のリソースの管理といったタスクを自動化し、効率的に処理することが可能になります。

詳細については、 [TiDB Cloud APIの概要](https://docs.pingcap.com/api/tidb-cloud-api-overview)参照してください。

## ノード {#nodes}

ノードはTiDBアーキテクチャの中核となるコンポーネントです。TiDBノード、TiKVノード、およびTiFlashノードは連携して、SQLクエリの処理、データの保存、および分析ワークロードの高速化を行います。

-   TiDB Cloud Dedicatedクラスターでは、パフォーマンス要件に応じて、専用の TiDB、TiKV、およびTiFlashノードの数とサイズを完全に管理できます。詳細については、[拡張性](/tidb-cloud/scalability-concepts.md)参照してください。
-   TiDB Cloud Starter、 TiDB Cloud Essential、またはTiDB Cloud Premiumインスタンスでは、TiDB、TiKV、およびTiFlashノードの数とサイズは自動的に管理されます。これにより、シームレスなスケーリングが実現され、ユーザーがノードの設定や管理を行う必要がなくなります。

### TiDBノード {#tidb-node}

[TiDBノード](/tidb-computing.md)MySQL互換エンドポイントを使用してアプリケーションに接続するステートレスなSQLレイヤーです。SQLクエリの解析、最適化、分散実行プランの作成などのタスクを処理します。

TiDBノードを複数デプロイすることで、水平方向に拡張し、より高いワークロードに対応できます。これらのノードは、TiProxyやHAProxyなどのロードバランサーと連携して、シームレスなインターフェースを提供します。TiDBノード自体はデータを保存せず、データ要求を行ベースstorageの場合はTiKVノードに、列ベースstorageの場合はTiFlashノードに転送します。

### TiKVノード {#tikv-node}

[TiKVノード](/tikv-overview.md)、TiDBアーキテクチャにおけるデータstorageの基盤であり、信頼性、拡張性、高可用性を提供する分散型トランザクションキーバリューstorageエンジンとして機能します。

**主な特徴：**

-   **地域ベースのデータstorage**

    -   データは[地域](https://docs.pingcap.com/tidb/dev/glossary#regionpeerraft-group)ごとに分割され、それぞれが特定のキー範囲（左端が閉じ、右端が開いた区間： `StartKey`から`EndKey` ）をカバーします。
    -   効率的なデータ配信を確保するため、各TiKVノード内には複数のリージョンが共存している。

-   **トランザクションサポート**

    -   TiKVノードは、キーバリューレベルでネイティブな分散トランザクションをサポートし、スナップショット分離をデフォルトの分離レベルとして保証します。
    -   TiDBノードは、SQL実行プランをTiKVノードAPIへの呼び出しに変換することで、シームレスなSQLレベルのトランザクションサポートを実現します。

-   **高可用性**

    -   TiKVノード内のすべてのデータは、耐久性を確保するために複製されます（デフォルト：3つのレプリカ）。
    -   TiKVはネイティブな高可用性を保証し、自動フェイルオーバーをサポートすることで、ノード障害からシステムを保護します。

-   **拡張性と信頼性**

    -   TiKVノードは、分散の一貫性と耐障害性を維持しながら、拡大するデータセットを処理できるように設計されています。

### TiFlashノード {#tiflash-node}

[TiFlashノード](/tiflash/tiflash-overview.md)TiDBアーキテクチャ内の特殊なstorageノードです。通常のTiKVノードとは異なり、 TiFlashはカラム型storageモデルによる分析高速化のために設計されています。

**主な特徴：**

-   **柱状storage**

    TiFlashノードはデータを列形式で保存するため、分析クエリに最適化されており、読み取り負荷の高いワークロードのパフォーマンスを大幅に向上させます。

-   **ベクトル検索インデックスのサポート**

    ベクトル検索インデックス機能は、テーブルにTiFlashレプリカを使用することで、高度な検索機能を実現し、複雑な分析シナリオにおける効率性を向上させます。

<CustomContent plan="premium">

## TiDB Cloud Premium でユニットと容量をリクエストする {#request-units-and-capacity-in-premium} {#request-units-and-capacity-in-premium}

### 要求容量単位（RCU） {#request-capacity-unit-rcu}

[要求容量単位（RCU）](/tidb-cloud/tidb-cloud-glossary.md#request-capacity-unit-rcu)は、 TiDB Cloud Premium インスタンスにプロビジョニングされたコンピューティング容量を表す単位です。1 RCU は、1 秒あたり一定数の RU を処理できる固定量のコンピューティング リソースを提供します。プロビジョニングする RCU の数によって、TiDB Cloud Premium インスタンスのベースライン パフォーマンスとスループット容量が決まります。

1 RCUは、毎秒RUの持続的な処理能力を表します。例えば、ベースラインとして*X* RCUを設定すると、1分間（またはインスタンスに設定された最小計算時間）で測定した平均で、毎秒*X* RUの処理能力が保証されます。

### RCUの自動スケーリング {#rcu-auto-scaling}

TiDB Cloud Premium インスタンスを構成する際に、ワークロードに必要な最大 RCU 数 ( `RCU_max` ) を指定します。TiDB TiDB Cloud は`0.25 * RCU_max`から`RCU_max` 。

例えば、最大容量を20,000 RCUに設定した場合、 TiDB Cloudはリアルタイムの需要に基づいて、容量を5,000 RCUから20,000 RCUの間で動的にスケーリングします。このスケーリングは自動的かつ瞬時に行われるため、手動操作や遅延なしに、いつでも最大数のRCUを消費できます。

### RCUの請求 {#rcu-billing}

TiDB Cloud Premiumは、実際の要求容量ユニット（RCU）の消費量とstorage使用量に基づいて課金される、使用量ベースの課金モデルを採用しています。

#### 1分あたりの計算 {#per-minute-calculation}

TiDB Cloudは、1分ごとに使用量を計算します。60秒間のウィンドウ内で消費されたリクエストユニット（RU）の総数を測定し、1秒あたりの平均RU数を算出し、この平均値をその分のRCU消費量として使用します。この計算により、請求額がリアルタイムのトラフィック変動を正確に反映することが保証されます。

#### 最低使用要件 {#minimum-usage-requirement}

TiDB Cloudは、ベースライン容量を維持し、インスタンスに必要なリソースが常に利用可能であることを保証するため、最大RCU設定に基づいて最小課金RCUを自動的に設定します。この値は、インスタンスのベースライン予約容量を定義します。

特定の1分間の実際の使用量がこのしきい値を下回る場合、課金は最小課金RCUに自動的に設定されます。この仕組みにより、インスタンスはパフォーマンスの低下や遅延を起こすことなく、指定された最大値までの急激なトラフィック増加に即座に対応できます。

### リクエストユニット（RU） {#request-unit-ru}

[リクエストユニット（RU）](/tidb-cloud/tidb-cloud-glossary.md#request-unit-ru)は、データベースへの単一のリクエストによって消費されるリソースを表す単位です。リクエストによって消費されるRUの数は、操作の種類や取得または変更されるデータの量などの要因によって異なります。

TiDB Cloud Premiumは、リクエストユニット（RU）を使用してすべてのデータベース操作のコストを標準化し、スループット（1秒あたりのリクエストユニット数、RU/s）に基づいてこのコストを測定します。この統一された指標により、スループットコストを予測しやすくなり、アプリケーションコストをより効果的に管理できるようになります。

#### ベースラインパフォーマンスの例 {#baseline-performance-examples}

以下の表は、一般的な操作における基本的なパフォーマンス例を示しており、作業負荷を推定するのに役立ちます。

| 操作タイプ    | 説明                         | 概算費用   |
| -------- | -------------------------- | ------ |
| 要点をまとめる  | 1 KiBのアイテムをその固有IDで読み込む     | 1.5 RU |
| OLTP書き込み | 標準Sysbenchモデル（アイテムサイズ1KiB） | 2.5 RU |

> **注記：**
>
> ポイントリードは、一意のIDを使用してデータを取得する最も効率的な方法です。書き込み操作の場合、RUコストは、データを永続化するために必要なI/Oとインデックス作成の作業量を表します。RU消費量は、データサイズと操作の複雑さに比例して増加します。

### ユニットの検討事項をリクエストする {#request-unit-considerations}

TiDB Cloudは、あらゆる操作の実行に必要なデータベース処理量に基づいて、その操作の総RU料金を計算します。

-   **データアクセスとサイズ**

    -   **読み書きボリューム**：RU（リソースユニット）はデータペイロードのサイズに比例して増加します。100 KiBのレコードを処理する場合、1 KiBのレコードを処理する場合よりも多くのRUを消費します。
    -   **行の読み書き**：操作に関わる行数は、コストを左右する主要因です。ペイロードが小さくても、複数の行を照会または更新すると、各行の処理、ロック、検証が必要となるため、RUの総消費量が増加します。
    -   **インデックスへの影響**：

        -   **書き込み**: テーブル上の影響を受ける各インデックスは、書き込み操作中に更新する必要があります。インデックスが多いテーブルでは、 `INSERT` 、 `UPDATE` 、および`DELETE`操作でRUコストが高くなります。
        -   **読み取り**：適切に設計されたインデックスは、エンジンが効率的に行を検索し、フルテーブルスキャンを回避できるようにすることで、クエリRUを大幅に削減します。

-   **クエリの複雑さ**

    -   **スキャン効率**：RU消費量は、エンジンがスキャンする必要のある行数に大きく影響されます。

        -   **読み取りメトリック（推定行数）** ：主キーまたは一意インデックスを使用するポイント読み取りが最も効率的な操作です。数百万行をスキャンするクエリは、最適化されたインデックスを使用するクエリよりもはるかに多くのRUを消費します。

        -   **書き込みメトリック（影響を受ける行数）** ：データ変更にかかるRUコストは、影響を受ける行数に依存します。1つのステートメントで10,000行を変更すると、1行だけを変更する場合よりもはるかに高い料金が発生します。

    -   **計算ロジック**：複数のテーブル結合、深いサブクエリ、集計などを含む複雑なSQL操作は、実行パスを計算してデータを処理するために、より多くのCPUサイクルを必要とします。

</CustomContent>
