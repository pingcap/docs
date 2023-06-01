---
title: Select Your Cluster Tier
summary: Learn how to select your cluster tier on TiDB Cloud.
---

# Cluster Tierを選択してください {#select-your-cluster-tier}

クラスター層によって、クラスターのスループットとパフォーマンスが決まります。

TiDB Cloud、次の 2 つのクラスター層のオプションが提供されます。クラスターを作成する前に、どちらのオプションがニーズに適しているかを検討する必要があります。

-   [<a href="#serverless-tier-beta">Serverless Tier</a>](#serverless-tier-beta)
-   [<a href="#dedicated-tier">Dedicated Tier</a>](#dedicated-tier)

## Serverless Tier(ベータ版) {#serverless-tier-beta}

TiDB CloudServerless Tier(以前はDeveloper Tierと呼ばれていました) は、TiDB のフルマネージド サービスです。これはまだベータ版であるため、本番では使用しないでください。ただし、Serverless Tierクラスターは、プロトタイプ アプリケーション、ハッカソン、学術コースなどの非運用ワークロードに使用したり、データセットに一時的なデータ サービスを提供したりするために使用できます。

TiDB Cloudアカウントごとに、ベータ段階で使用する無料のServerless Tierクラスターを最大 5 つ作成できます。

### ユーザー名のプレフィックス {#user-name-prefix}

<!--Important: Do not update the section name "User name prefix" because this section is referenced by TiDB backend error messages.-->

TiDB Cloudは、Serverless Tierクラスターごとに、他のクラスターと区別するための一意のプレフィックスを生成します。

データベース ユーザー名を使用または設定するときは、ユーザー名に接頭辞を含める必要があります。たとえば、クラスターのプレフィックスが`3pTAoNNegb47Uc8`であると仮定します。

-   クラスターに接続するには:

    ```shell
    mysql -u '3pTAoNNegb47Uc8.root' -h <host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_root_path> -p
    ```

    > **ノート：**
    >
    > Serverless TierにはTLS接続が必要です。システム上の CA ルート パスを見つけるには、 [<a href="/tidb-cloud/secure-connections-to-serverless-tier-clusters.md#where-is-the-ca-root-path-on-my-system">CA ルート パス リスト</a>](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md#where-is-the-ca-root-path-on-my-system)を参照してください。

-   データベース ユーザーを作成するには:

    ```sql
    CREATE USER '3pTAoNNegb47Uc8.jeffrey';
    ```

クラスターのプレフィックスを取得するには、次の手順を実行します。

1.  [<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動します。
2.  ターゲット クラスターの名前をクリックして概要ページに移動し、右上隅の**[接続]**をクリックします。接続ダイアログが表示されます。
3.  ダイアログで、接続文字列からプレフィックスを取得します。

### Serverless Tierの特別利用規約 {#serverless-tier-special-terms-and-conditions}

-   Serverless Tierは現在ベータ版であり、ベータ段階中の稼働時間 SLA 保証はありません。商用または本番データセットを保存するためにServerless Tierベータ版を使用する場合、その使用に関連する潜在的なリスクはすべて自分で負う必要があり、PingCAP は損害に対して責任を負いません。
-   TiDB Cloud機能の一部は、Serverless Tierで部分的にサポートされているか、サポートされていません。詳細については[<a href="/tidb-cloud/serverless-tier-limitations.md">Serverless Tierの制限</a>](/tidb-cloud/serverless-tier-limitations.md)を参照してください。

## Dedicated Tier {#dedicated-tier}

TiDB CloudDedicated Tierは、クロスゾーンの高可用性、水平スケーリング、および[<a href="https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing">HTAP</a>](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)利点を備えた本番稼働専用です。

Dedicated Tierクラスターの場合、ビジネス ニーズに応じて TiDB、TiKV、およびTiFlashのクラスター サイズを簡単にカスタマイズできます。 TiKV ノードとTiFlashノードごとに、ノード上のデータが複製され、 [<a href="/tidb-cloud/high-availability-with-multi-az.md">高可用性</a>](/tidb-cloud/high-availability-with-multi-az.md)アベイラビリティ ゾーンに分散されます。

Dedicated Tierクラスターを作成するには、 [<a href="/tidb-cloud/tidb-cloud-billing.md#payment-method">支払い方法を追加する</a>](/tidb-cloud/tidb-cloud-billing.md#payment-method)または[<a href="/tidb-cloud/tidb-cloud-poc.md">概念実証 (PoC) トライアルに申し込む</a>](/tidb-cloud/tidb-cloud-poc.md)を行う必要があります。

> **ノート：**
>
> クラスターの作成後にノードstorageを減らすことはできません。
