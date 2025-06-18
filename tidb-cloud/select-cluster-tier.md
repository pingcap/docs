---
title: Select Your Cluster Tier
summary: TiDB Cloudでクラスター層を選択する方法について説明します。
aliases: ['/tidbcloud/developer-tier-cluster']
---

# Cluster Tierを選択 {#select-your-cluster-tier}

クラスター層によって、クラスターのスループットとパフォーマンスが決まります。

TiDB Cloud は、以下の 2 つのクラスター層オプションを提供します。クラスターを作成する前に、どちらのオプションがニーズに適しているかを検討する必要があります。

-   [TiDB Cloudサーバーレス](#tidb-cloud-serverless)
-   [TiDB Cloud専用](#tidb-cloud-dedicated)

## TiDB Cloudサーバーレス {#tidb-cloud-serverless}

<!--To be confirmed-->

TiDB Cloud Serverlessは、フルマネージドのマルチテナント型TiDBサービスです。MySQL互換データベースを瞬時に自動スケーリングし、豊富な無料プランをご用意しています。無料プランの上限を超えた場合は、使用量に応じた課金体系でご利用いただけます。

### クラスタプラン {#cluster-plans}

TiDB Cloud Serverlessは、さまざまなユーザー要件に対応する2つのサービスプランを提供しています。導入直後から、あるいは増大するアプリケーション需要に合わせて拡張する場合でも、これらのサービスプランは必要な柔軟性と機能を提供します。

#### 無料クラスタープラン {#free-cluster-plan}

無料のクラスタープランは、 TiDB Cloud Serverless を初めてご利用になる方に最適です。開発者や小規模チームに、以下の重要な機能を提供します。

-   **無料**: このプランは完全に無料で、開始するのにクレジットカードは必要ありません。
-   **ストレージ**: 初期 5 GiB の行ベースのstorageと 5 GiB の列ベースのstorageを提供します。
-   **リクエスト単位**: データベース操作用の 5,000 万[リクエストユニット（RU）](/tidb-cloud/tidb-cloud-glossary.md#request-unit)が含まれます。
-   **簡単なアップグレード**: ニーズの拡大に応じて、 [スケーラブルなクラスタープラン](#scalable-cluster-plan)へのスムーズな移行を実現します。

#### スケーラブルなクラスタープラン {#scalable-cluster-plan}

ワークロードが増加し、リアルタイムのスケーラビリティを必要とするアプリケーションの場合、スケーラブル クラスター プランは、次の機能により、ビジネスの成長に対応できる柔軟性とパフォーマンスを提供します。

-   **拡張機能**: 無料のクラスター プランのすべての機能に加えて、より大規模で複雑なワークロードを処理する能力と高度なセキュリティ機能が含まれています。
-   **自動スケーリング**: 変化するワークロードの需要に効率的に対応するために、storageとコンピューティング リソースを自動的に調整します。
-   **予測可能な価格設定**: このプランではクレジットカードが必要ですが、使用したリソースに対してのみ課金されるため、コスト効率の高いスケーラビリティが保証されます。

### 使用量制限 {#usage-quota}

TiDB Cloudでは、組織ごとに最大5つのクラスター（デフォルトでは[フリークラスター](#free-cluster-plan)を作成できます。TiDB TiDB Cloud Serverlessクラスターをさらに作成するには、クレジットカードを追加し、使用量に応じて[スケーラブルなクラスター](#scalable-cluster-plan)クラスターを作成する必要があります。

組織内の最初の 5 つのTiDB Cloud Serverless クラスターについては、無料かスケーラブルかに関係なく、 TiDB Cloud は次のようにクラスターごとに無料使用量割り当てを提供します。

-   行ベースのstorage: 5 GiB
-   列指向storage: 5 GiB
-   リクエストユニット（RU）：月間5,000万RU

リクエストユニット（RU）は、データベースへの単一のリクエストで消費されるリソースの量を表す測定単位です。リクエストで消費されるRUの量は、操作の種類や取得または変更されるデータの量など、さまざまな要因によって異なります。

クラスターが使用量クォータに達すると、新しい月[割り当てを増やす](/tidb-cloud/manage-serverless-spend-limit.md#update-spending-limit)始まるまで、または使用量がリセットされるまで、新規接続の試行は直ちに拒否されます。クォータに達する前に確立された既存の接続はアクティブなままですが、スロットリングが発生します。例えば、クラスターの行ベースstorageが空きクラスターで5GiBを超えると、クラスターは自動的に新規接続の試行を制限します。

さまざまなリソース (読み取り、書き込み、SQL CPU、ネットワーク送信など) の RU 消費量、価格の詳細、スロットル情報の詳細については、 [TiDB Cloud Serverless の価格詳細](https://www.pingcap.com/tidb-cloud-serverless-pricing-details)参照してください。

### ユーザー名のプレフィックス {#user-name-prefix}

<!--Important: Do not update the section name "User name prefix" because this section is referenced by TiDB backend error messages.-->

TiDB Cloud は、各TiDB Cloud Serverless クラスターに対して、他のクラスターと区別するための一意のプレフィックスを生成します。

データベースユーザー名を使用または設定する際は、必ずユーザー名にプレフィックスを含める必要があります。例えば、クラスターのプレフィックスが`3pTAoNNegb47Uc8`であるとします。

-   クラスターに接続するには:

    ```shell
    mysql -u '3pTAoNNegb47Uc8.root' -h <host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_root_path> -p
    ```

    > **注記：**
    >
    > TiDB Cloud Serverless にはTLS接続が必要です。システム上のCAルートパスを確認するには、 [ルート証明書のデフォルトパス](/tidb-cloud/secure-connections-to-serverless-clusters.md#root-certificate-default-path)参照してください。

-   データベース ユーザーを作成するには:

    ```sql
    CREATE USER '3pTAoNNegb47Uc8.jeffrey';
    ```

クラスターのプレフィックスを取得するには、次の手順を実行します。

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。
2.  ターゲットクラスターの名前をクリックして概要ページに移動し、右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。
3.  ダイアログで、接続文字列からプレフィックスを取得します。

### TiDB Cloud Serverless の特別利用規約 {#tidb-cloud-serverless-special-terms-and-conditions}

TiDB Cloudの一部の機能は、 TiDB Cloud Serverlessでは部分的にサポートされるか、サポートされません。詳細は[TiDB Cloudサーバーレスの制限](/tidb-cloud/serverless-limitations.md)ご覧ください。

## TiDB Cloud専用 {#tidb-cloud-dedicated}

TiDB Cloud Dedicated は、クロスゾーンの高可用性、水平スケーリング、および[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)利点を備えた本番での使用を目的としています。

TiDB Cloud Dedicated クラスターでは、ビジネスニーズに合わせて TiDB、TiKV、 TiFlashのクラスターサイズを簡単にカスタマイズできます。各 TiKV ノードとTiFlashノードでは、ノード上のデータが複製され、異なるアベイラビリティゾーンに[高可用性](/tidb-cloud/high-availability-with-multi-az.md)日間分散されます。

TiDB Cloud Dedicated クラスターを作成するには、 [支払い方法を追加する](/tidb-cloud/tidb-cloud-billing.md#payment-method)または[概念実証（PoC）トライアルに申し込む](/tidb-cloud/tidb-cloud-poc.md)が必要です。

> **注記：**
>
> クラスターの作成後にノードstorageを減らすことはできません。
