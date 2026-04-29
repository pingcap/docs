---
title: Select a Plan
summary: TiDB Cloudでプランを選択する方法を学びましょう。
aliases: ['/ja/tidbcloud/developer-tier-cluster']
---

# プランを選択してください {#select-your-plan}

プランによって、TiDBリソースのスループットとパフォーマンスが決まります。

TiDB Cloud、以下のプランをご用意しています。新規導入の場合でも、アプリケーションの需要増加に合わせて拡張していく場合でも、これらのサービスプランは必要な柔軟性と機能を提供します。TiDBリソースを作成する前に、どのプランがお客様のニーズに最適かを検討する必要があります。

-   [TiDB Cloud Starter](#starter)
-   [TiDB Cloud Essential](#essential)
-   [TiDB Cloud Premium](#premium)
-   [TiDB Cloud Dedicated](#tidb-cloud-dedicated)

> **注記：**
>
> TiDB Cloudの一部の機能は、 TiDB Cloud StarterおよびTiDB Cloud Essentialでは部分的にサポートされているか、サポートされていません。詳細については[TiDB Cloud StarterとEssential制限事項](/tidb-cloud/serverless-limitations.md)を参照してください。

## TiDB Cloud Starter {#starter} {#starter}

TiDB Cloud Starterは、フルマネージド型のマルチテナント対応TiDBサービスです。MySQL互換の自動スケーリング対応データベースを即座に提供し、十分な無料クォータと、無料制限を超えた場合の従量課金制を採用しています。

無料プランは、 TiDB Cloud Starter を初めて利用する方に最適です。開発者や小規模チーム向けに、以下の必須機能を提供します。

-   **無料**：このプランは完全に無料で、利用開始にクレジットカードは必要ありません。
-   **ストレージ**：初期容量として、行ベースのstorageが5 GiB、列ベースのstorageが5 GiB提供されます。
-   **要求単位**: データベース操作の 5,000 万[要求単位（RU）](/tidb-cloud/tidb-cloud-glossary.md#request-unit-ru)が含まれます。

### 使用クォータ {#usage-quota}

TiDB Cloudでは、組織ごとにデフォルトで最大5つのTiDB Cloud Starterインスタンスを無料で作成できます。それ以上のTiDB Cloud Starterインスタンスを作成するには、クレジットカードを追加して利用限度額を指定する必要があります。

組織内の最初の 5 つのTiDB Cloud Starterインスタンス（無料版かスケーラブル版かを問わず）については、 TiDB Cloud はそれぞれに以下の無料使用クォ​​ータを提供します。

-   行ベースstorage：5 GiB
-   カラム型storage：5 GiB
-   要求単位（RU）：月間5,000万RU

リクエストユニット（RU）とは、データベースへの単一のリクエストによって消費されるリソース量を表す単位です。リクエストによって消費されるRUの量は、操作の種類や取得または変更されるデータの量など、さまざまな要因によって異なります。

TiDB Cloud Starterインスタンスが使用クォータに達すると、ユーザーが または新しい月の開始時に使用がリセットさ[割り当てを増やす](/tidb-cloud/manage-serverless-spend-limit.md#update-spending-limit)まで、新しい接続試行は即座に拒否されます。クォータに達する前に確立された既存の接続はアクティブなままですが、スロットリングが発生します。たとえば、無料のTiDB Cloud Starter TiDB Cloud Starterインスタンスの行ベースのstorageが5 GiB を超えると、インスタンスは自動的に新しい接続試行を制限します。

さまざまなリソース（読み取り、書き込み、SQL CPU、ネットワーク出力など）のRU消費量、価格の詳細、およびスロットリング情報の詳細については、 [TiDB Cloud Starterの料金詳細](https://www.pingcap.com/tidb-cloud-starter-pricing-details/)参照してください。

## TiDB Cloud Essential {#essential} {#essential}

ワークロードが増加し、リアルタイムでの拡張性を必要とするアプリケーション向けに、 Essentialプランは以下の機能を備え、ビジネスの成長に合わせて柔軟かつ高性能なソリューションを提供します。

-   **機能強化**：Starterプランのすべての機能に加え、より大規模で複雑なワークロードを処理できる能力、および高度なセキュリティ機能が含まれています。
-   **自動スケーリング**：変化するワークロードの需要に効率的に対応するために、storageとコンピューティングリソースを自動的に調整します。
-   **高可用性**：組み込みの耐障害性と冗長性により、インフラストラクチャの障害発生時でも、アプリケーションの可用性と回復力が維持されます。
-   **予測可能な料金体系**：コンピューティングリソースのstorageとリクエストキャパシティユニット（RCU）に基づいて課金されるため、ニーズに合わせて拡張可能な透明性の高い使用量ベースの料金体系が提供され、予期せぬ追加料金なしで使用した分だけを支払うことができます。

## ユーザー名の接頭辞 {#user-name-prefix}

<!--Important: Do not update the section name "User name prefix" because this section is referenced by TiDB backend error messages.-->

TiDB TiDB Cloudは、 TiDB Cloud StarterまたはTiDB Cloud Essentialの各インスタンスに対して、他のインスタンスと区別するための固有のプレフィックスを生成します。

データベースユーザー名を使用または設定する際は、必ずプレフィックスをユーザー名に含める必要があります。たとえば、 TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスのプレフィックスが`3pTAoNNegb47Uc8`であるとします。

-   TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスに接続するには：

    ```shell
    mysql -u '3pTAoNNegb47Uc8.root' -h <host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_root_path> -p
    ```

    > **注記：**
    >
    > TiDB Cloud StarterおよびTiDB Cloud Essential には TLS 接続が必要です。システム上の CA ルート パスを見つけるには、 [ルート証明書のデフォルトパス](/tidb-cloud/secure-connections-to-serverless-clusters.md#root-certificate-default-path)を参照してください。

-   データベースユーザーを作成するには：

    ```sql
    CREATE USER '3pTAoNNegb47Uc8.jeffrey';
    ```

TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスのプレフィックスを取得するには、以下の手順を実行してください。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。
2.  対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして概要ページに移動し、右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。
3.  ダイアログで、接続文字列からプレフィックスを取得します。

## TiDB Cloud Premium {#premium} {#premium}

大規模な容量と一貫した高いパフォーマンスを必要とするミッションクリティカルなエンタープライズワークロード向けに、プレミアムプランは以下の機能を備えたクラウドネイティブなエクスペリエンスを提供します。

-   **即時的な拡張性**：トラフィックの急増に対応し、ピーク需要時にも安定したパフォーマンスを維持するために、コンピューティングリソースを自動的に拡張します。
-   **無制限の拡張性**：物理的なインフラストラクチャの制約を受けることなく、ビジネスの成長に合わせてstorageとスループットを拡張できます。
-   **ゼロインフラストラクチャ管理**：手動によるスケーリング、パッチ適用、キャパシティプランニングを排除する、完全マネージドサービスを提供します。
-   **予測可能な料金体系**：storageとリクエスト容量ユニット（RCU）に基づいて課金されるため、ニーズに合わせて拡張可能な透明性の高い使用量ベースの料金体系が実現し、予期せぬ追加料金なしで使用した分だけを支払うことができます。
-   **高度なセキュリティとコンプライアンス**：高度な暗号化、顧客管理型暗号化キー（CMEK）、プライベートネットワーク、およびコンプライアンス認証をサポートし、機密データを保護します。

## TiDB Cloud Dedicated {#tidb-cloud-dedicated}

TiDB Cloud Dedicatedは、ゾーン間高可用性、水平スケーリング、 [HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)といったメリットを備えた、本番での利用を想定したサービスです。

TiDB Cloud Dedicatedクラスターでは、ビジネスニーズに応じて TiDB、TiKV、 TiFlashのクラスターサイズを簡単にカスタマイズできます。各 TiKV ノードおよびTiFlashノードでは、ノード上のデータが複製され、 [高可用性](/tidb-cloud/high-availability-with-multi-az.md)実現するために異なる可用性ゾーンに分散されます。

TiDB Cloud Dedicatedクラスターを作成するには、 [支払い方法を追加する](/tidb-cloud/tidb-cloud-billing.md#payment-method)か、[概念実証（PoC）トライアルに申し込む](/tidb-cloud/tidb-cloud-poc.md)必要があります。

> **注記：**
>
> TiDB Cloud Dedicatedクラスタの作成後は、ノードのstorageを減らすことはできません。
