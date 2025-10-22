---
title: Select Your Cluster Plan
summary: TiDB Cloudでクラスター プランを選択する方法について説明します。
aliases: ['/tidbcloud/developer-tier-cluster']
---

# クラスタプランを選択 {#select-your-cluster-plan}

クラスター プランによって、クラスターのスループットとパフォーマンスが決まります。

TiDB Cloudは、以下のクラスタープランをご用意しています。導入直後でも、増大するアプリケーション需要に対応するための拡張でも、これらのサービスプランは必要な柔軟性と機能を提供します。クラスターを作成する前に、どのオプションがニーズに適しているかを検討してください。

-   [TiDB Cloudスターター](#starter)
-   [TiDB Cloudエッセンシャル](#essential)
-   [TiDB Cloud専用](#tidb-cloud-dedicated)

> **注記：**
>
> TiDB Cloudの一部機能は、 TiDB Cloud StarterおよびTiDB Cloud Essentialでは部分的にサポートされるか、サポートされません。詳細は[TiDB Cloud Starter と基本的な制限事項](/tidb-cloud/serverless-limitations.md)ご覧ください。

## TiDB Cloudスターター {#starter} {#starter}

TiDB Cloud Starterは、フルマネージドのマルチテナント型TiDBサービスです。MySQL互換データベースを瞬時に自動スケーリングし、十分な無料クォータと、無料クォータを超えた場合の使用量に応じた課金体系を提供します。

無料のクラスタープランは、 TiDB Cloud Starterを初めてご利用になる方に最適です。開発者や小規模チームに以下の重要な機能を提供します。

-   **無料**: このプランは完全に無料で、開始するのにクレジットカードは必要ありません。
-   **ストレージ**: 初期 5 GiB の行ベースのstorageと 5 GiB の列ベースのstorageを提供します。
-   **リクエスト単位**: データベース操作用に 5000 万[リクエストユニット（RU）](/tidb-cloud/tidb-cloud-glossary.md#request-unit)が含まれます。

### 使用量制限 {#usage-quota}

TiDB Cloudでは、組織ごとにデフォルトで最大5つのTiDB Cloud Starterクラスターを無料で作成できます。さらにTiDB Cloud Starterクラスターを作成するには、クレジットカードを追加し、利用限度額を指定する必要があります。

組織内の最初の 5 つのTiDB Cloud Starter クラスターについては、無料かスケーラブルかに関係なく、 TiDB Cloud は次のようにクラスターごとに無料使用量の割り当てを提供します。

-   行ベースのstorage: 5 GiB
-   列指向storage: 5 GiB
-   リクエストユニット（RU）：月間5,000万RU

リクエストユニット（RU）は、データベースへの単一のリクエストで消費されるリソースの量を表す測定単位です。リクエストで消費されるRUの量は、操作の種類や取得または変更されるデータの量など、さまざまな要因によって異なります。

クラスターが使用量クォータに達すると、新しい月の開始時に使用[割り当てを増やす](/tidb-cloud/manage-serverless-spend-limit.md#update-spending-limit)がリセットされるまで、新規接続の試行は直ちに拒否されます。クォータに達する前に確立された既存の接続はアクティブのままですが、スロットリングが発生します。例えば、クラスターの行ベースstorageが空きクラスターで5GiBを超えると、クラスターは自動的に新規接続の試行を制限します。

さまざまなリソース (読み取り、書き込み、SQL CPU、ネットワーク送信など) の RU 消費量、価格の詳細、スロットル情報の詳細については、 [TiDB Cloud Starter の価格詳細](https://www.pingcap.com/tidb-cloud-starter-pricing-details/)参照してください。

## TiDB Cloudエッセンシャル {#essential} {#essential}

ワークロードが増加し、リアルタイムの拡張性を必要とするアプリケーションの場合、Essential クラスター プランは次の機能により、ビジネスの成長に対応できる柔軟性とパフォーマンスを提供します。

-   **拡張機能**: スターター プランのすべての機能に加えて、より大規模で複雑なワークロードを処理する能力と高度なセキュリティ機能が含まれます。
-   **自動スケーリング**: 変化するワークロードの需要に効率的に対応するために、storageとコンピューティング リソースを自動的に調整します。
-   **高可用性**: フォールト トレランスと冗長性が組み込まれているため、インフラストラクチャに障害が発生した場合でも、アプリケーションの可用性と回復力を維持できます。
-   **予測可能な価格設定**: コンピューティング リソースのstorageとリクエスト容量単位 (RCU) に基づいて課金され、ニーズに合わせて拡張できる透明性の高い使用量ベースの価格設定が提供されるため、予期せぬ出費なく、使用した分だけを支払うことになります。

## ユーザー名のプレフィックス {#user-name-prefix}

<!--Important: Do not update the section name "User name prefix" because this section is referenced by TiDB backend error messages.-->

TiDB Cloud Starter またはTiDB Cloud Essential クラスターごとに、 TiDB Cloud は他のクラスターと区別するために一意のプレフィックスを生成します。

データベースユーザー名を使用または設定する際は、必ずユーザー名にプレフィックスを含める必要があります。例えば、クラスターのプレフィックスが`3pTAoNNegb47Uc8`であるとします。

-   クラスターに接続するには:

    ```shell
    mysql -u '3pTAoNNegb47Uc8.root' -h <host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_root_path> -p
    ```

    > **注記：**
    >
    > TiDB Cloud StarterおよびTiDB Cloud EssentialはTLS接続が必要です。システム上のCAルートパスを確認するには、 [ルート証明書のデフォルトパス](/tidb-cloud/secure-connections-to-serverless-clusters.md#root-certificate-default-path)参照してください。

-   データベース ユーザーを作成するには:

    ```sql
    CREATE USER '3pTAoNNegb47Uc8.jeffrey';
    ```

クラスターのプレフィックスを取得するには、次の手順を実行します。

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。
2.  ターゲットクラスターの名前をクリックして概要ページに移動し、右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。
3.  ダイアログで、接続文字列からプレフィックスを取得します。

## TiDB Cloud専用 {#tidb-cloud-dedicated}

TiDB Cloud Dedicated は、クロスゾーンの高可用性、水平スケーリング、 [HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)利点を備えた本番環境向けです。

TiDB Cloud Dedicated クラスターでは、ビジネスニーズに合わせて TiDB、TiKV、 TiFlashのクラスターサイズを簡単にカスタマイズできます。各 TiKV ノードとTiFlashノードでは、ノード上のデータが[高可用性](/tidb-cloud/high-availability-with-multi-az.md)間、異なるアベイラビリティゾーンに複製され、分散されます。

TiDB Cloud Dedicated クラスターを作成するには、 [支払い方法を追加する](/tidb-cloud/tidb-cloud-billing.md#payment-method)または[概念実証（PoC）トライアルに申し込む](/tidb-cloud/tidb-cloud-poc.md)が必要です。

> **注記：**
>
> クラスターの作成後にノードstorageを減らすことはできません。
