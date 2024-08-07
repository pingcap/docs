---
title: Select Your Cluster Tier
summary: TiDB Cloudでクラスター層を選択する方法について説明します。
aliases: ['/tidbcloud/developer-tier-cluster']
---

# Cluster Tierを選択 {#select-your-cluster-tier}

クラスター層によって、クラスターのスループットとパフォーマンスが決まります。

TiDB Cloud、次の 2 つのクラスター層のオプションが提供されています。クラスターを作成する前に、どちらのオプションがニーズに適しているかを検討する必要があります。

-   [TiDB サーバーレス](#tidb-serverless)
-   [TiDB専用](#tidb-dedicated)

## TiDB サーバーレス {#tidb-serverless}

<!--To be confirmed-->

TiDB Serverless は、完全に管理されたマルチテナントの TiDB サービスです。瞬時に自動スケーリングされる MySQL 互換データベースを提供し、十分な無料利用枠と、無料制限を超えた場合の消費量に基づく課金を提供します。

### クラスタ計画 {#cluster-plans}

TiDB Serverless は、さまざまなユーザー要件を満たす 2 つのサービス プランを提供します。始めたばかりでも、増大するアプリケーション需要に対応するために拡張する場合でも、これらのサービス プランは必要な柔軟性と機能を提供します。

#### 無料クラスタープラン {#free-cluster-plan}

無料のクラスター プランは、TiDB Serverless を使い始める方に最適です。開発者や小規模チームに次の重要な機能を提供します。

-   **無料**: このプランは完全に無料で、開始するのにクレジットカードは必要ありません。
-   **ストレージ**: 初期 5 GiB の行ベースのstorageと 5 GiB の列ベースのstorageを提供します。
-   **リクエスト単位**: データベース操作用の 5000 万[リクエストユニット (RU)](/tidb-cloud/tidb-cloud-glossary.md#request-unit)が含まれます。
-   **簡単なアップグレード**: ニーズの拡大に応じて、 [スケーラブルなクラスタープラン](#scalable-cluster-plan)へのスムーズな移行を実現します。

#### スケーラブルなクラスタープラン {#scalable-cluster-plan}

ワークロードが増加し、リアルタイムのスケーラビリティを必要とするアプリケーションの場合、スケーラブル クラスター プランでは、次の機能により、ビジネスの成長に対応できる柔軟性とパフォーマンスが提供されます。

-   **強化された機能**: 無料のクラスター プランのすべての機能に加えて、より大規模で複雑なワークロードを処理する能力と高度なセキュリティ機能が含まれます。
-   **自動スケーリング**: 変化するワークロードの需要に効率的に対応するために、storageとコンピューティング リソースを自動的に調整します。
-   **予測可能な価格設定**: このプランではクレジットカードが必要ですが、使用したリソースに対してのみ課金されるため、コスト効率の高いスケーラビリティが保証されます。

### 使用量制限 {#usage-quota}

TiDB Cloudの各組織では、デフォルトで最大 5 [フリークラスター](#free-cluster-plan)のクラスターを作成できます。さらに TiDB Serverless クラスターを作成するには、クレジットカードを追加し、使用量に応じて[スケーラブルなクラスター](#scalable-cluster-plan)作成する必要があります。

組織内の最初の 5 つの TiDB Serverless クラスターについては、無料かスケーラブルかに関係なく、 TiDB Cloud はそれぞれに対して次のように無料使用量割り当てを提供します。

-   行ベースのstorage: 5 GiB
-   列型storage: 5 GiB
-   リクエスト ユニット (RU): 1 か月あたり 5,000 万 RU

リクエスト ユニット (RU) は、データベースへの単一のリクエストで消費されるリソースの量を表すために使用される測定単位です。リクエストで消費される RU の量は、操作の種類や取得または変更されるデータの量など、さまざまな要因によって異なります。

クラスターが使用量の割り当てに達すると、新しい月の開始時に使用量がリセットされるか、 [割り当てを増やす](/tidb-cloud/manage-serverless-spend-limit.md#update-spending-limit)なるまで、クラスターは新しい接続試行を直ちに拒否します。割り当てに達する前に確立された既存の接続はアクティブなままですが、スロットリングが発生します。たとえば、クラスターの行ベースのstorageが空きクラスターに対して 5 GiB を超えると、クラスターは新しい接続試行を自動的に制限します。

さまざまなリソース (読み取り、書き込み、SQL CPU、ネットワーク送信など) の RU 消費量、価格の詳細、スロットル情報の詳細については、 [TiDB サーバーレスの価格詳細](https://www.pingcap.com/tidb-cloud-serverless-pricing-details)を参照してください。

### ユーザー名プレフィックス {#user-name-prefix}

<!--Important: Do not update the section name "User name prefix" because this section is referenced by TiDB backend error messages.-->

TiDB Cloud は、TiDB Serverless クラスターごとに、他のクラスターと区別するための一意のプレフィックスを生成します。

データベース ユーザー名を使用または設定するときは、必ずユーザー名にプレフィックスを含める必要があります。たとえば、クラスターのプレフィックスが`3pTAoNNegb47Uc8`であるとします。

-   クラスターに接続するには:

    ```shell
    mysql -u '3pTAoNNegb47Uc8.root' -h <host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_root_path> -p
    ```

    > **注記：**
    >
    > TiDB Serverless には TLS 接続が必要です。システム上の CA ルート パスを見つけるには、 [ルート証明書のデフォルトパス](/tidb-cloud/secure-connections-to-serverless-clusters.md#root-certificate-default-path)参照してください。

-   データベース ユーザーを作成するには:

    ```sql
    CREATE USER '3pTAoNNegb47Uc8.jeffrey';
    ```

クラスターのプレフィックスを取得するには、次の手順を実行します。

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページ目に移動します。
2.  ターゲット クラスターの名前をクリックして概要ページに移動し、右上隅の**[接続]**をクリックします。接続ダイアログが表示されます。
3.  ダイアログで、接続文字列からプレフィックスを取得します。

### TiDB Serverless 特別利用規約 {#tidb-serverless-special-terms-and-conditions}

TiDB Cloud機能の一部は、TiDB Serverless では部分的にサポートされているか、サポートされていません。詳細については[TiDB サーバーレスの制限](/tidb-cloud/serverless-limitations.md)参照してください。

## TiDB専用 {#tidb-dedicated}

TiDB Dedicated は、クロスゾーンの高可用性、水平スケーリング、および[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)利点を備えた本番向けです。

TiDB 専用クラスターでは、ビジネス ニーズに応じて TiDB、TiKV、およびTiFlashのクラスター サイズを簡単にカスタマイズできます。各 TiKV ノードとTiFlashノードでは、ノード上のデータが複製され、 [高可用性](/tidb-cloud/high-availability-with-multi-az.md)間、異なるアベイラビリティ ゾーンに分散されます。

TiDB 専用クラスターを作成するには、 [支払い方法を追加する](/tidb-cloud/tidb-cloud-billing.md#payment-method)または[概念実証（PoC）トライアルを申請する](/tidb-cloud/tidb-cloud-poc.md)必要です。

> **注記：**
>
> クラスターの作成後にノードstorageを減らすことはできません。
