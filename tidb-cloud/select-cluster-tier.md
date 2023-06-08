---
title: Select Your Cluster Tier
summary: Learn how to select your cluster tier on TiDB Cloud.
aliases: ['/tidbcloud/developer-tier-cluster']
---

# Cluster Tierを選択してください {#select-your-cluster-tier}

クラスター層によって、クラスターのスループットとパフォーマンスが決まります。

TiDB Cloud、次の 2 つのクラスター層のオプションが提供されます。クラスターを作成する前に、どちらのオプションがニーズに適しているかを検討する必要があります。

-   [<a href="#tidb-serverless-beta">TiDB Serverless</a>](#tidb-serverless-beta)
-   [<a href="#tidb-dedicated">TiDB Dedicated</a>](#tidb-dedicated)

## TiDB Serverless (ベータ版) {#tidb-serverless-beta}

TiDB Serverless (以前はDeveloper Tierと呼ばれていました) は、TiDB のフルマネージド サービスです。これはまだベータ版であるため、本番では使用しないでください。ただし、TiDB Serverless クラスターは、プロトタイプ アプリケーション、ハッカソン、学術コースなどの非運用ワークロードに使用したり、データセットに一時的なデータ サービスを提供したりするために使用できます。

### 使用量割り当て {#usage-quota}

TiDB Cloudの組織ごとに、デフォルトで最大 5 つの TiDB Serverless クラスターを作成できます。さらに TiDB Serverless クラスターを作成するには、クレジット カードを追加し、使用量を[<a href="/tidb-cloud/tidb-cloud-glossary.md#spend-limit">支出制限</a>](/tidb-cloud/tidb-cloud-glossary.md#spend-limit)に設定する必要があります。

組織内の最初の 5 つの TiDB Serverless クラスターに対して、 TiDB Cloud は各クラスターに次のように無料の使用量クォータを提供します。

-   行storage: 5 GiB
-   [<a href="/tidb-cloud/tidb-cloud-glossary.md#request-unit">リクエストユニット (RU)</a>](/tidb-cloud/tidb-cloud-glossary.md#request-unit) : 月あたり 5,000 万 RU

リクエスト ユニット (RU) は、データベースへの 1 回のリクエストによって消費されるリソースの量を表すために使用される測定単位です。要求によって消費される RU の量は、操作の種類や取得または変更されるデータの量などのさまざまな要因によって異なります。

クラスターの無料クォータに達すると、このクラスターでの読み取りおよび書き込み操作は、新しい月の初めに使用量が[<a href="/tidb-cloud/manage-serverless-spend-limit.md#update-spend-limit">割り当てを増やす</a>](/tidb-cloud/manage-serverless-spend-limit.md#update-spend-limit)されるまでスロットルされます。たとえば、クラスターのstorageが 5 GiB を超えると、単一トランザクションの最大サイズ制限が 10 MiB から 1 MiB に減ります。

さまざまなリソース (読み取り、書き込み、SQL CPU、ネットワーク下りなど) の RU 消費量、料金の詳細、および調整された情報の詳細については、 [<a href="https://www.pingcap.com/tidb-cloud-serverless-pricing-details">TiDB Serverlessの料金詳細</a>](https://www.pingcap.com/tidb-cloud-serverless-pricing-details)を参照してください。

### ユーザー名のプレフィックス {#user-name-prefix}

<!--Important: Do not update the section name "User name prefix" because this section is referenced by TiDB backend error messages.-->

TiDB Serverless クラスターごとに、 TiDB Cloudは他のクラスターと区別するための一意のプレフィックスを生成します。

データベース ユーザー名を使用または設定するときは、ユーザー名に接頭辞を含める必要があります。たとえば、クラスターのプレフィックスが`3pTAoNNegb47Uc8`であると仮定します。

-   クラスターに接続するには:

    ```shell
    mysql -u '3pTAoNNegb47Uc8.root' -h <host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_root_path> -p
    ```

    > **ノート：**
    >
    > TiDB Serverlessには TLS 接続が必要です。システム上の CA ルート パスを見つけるには、 [<a href="/tidb-cloud/secure-connections-to-serverless-tier-clusters.md#root-certificate-default-path">ルート証明書のデフォルトのパス</a>](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md#root-certificate-default-path)を参照してください。

-   データベース ユーザーを作成するには:

    ```sql
    CREATE USER '3pTAoNNegb47Uc8.jeffrey';
    ```

クラスターのプレフィックスを取得するには、次の手順を実行します。

1.  [<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動します。
2.  ターゲット クラスターの名前をクリックして概要ページに移動し、右上隅の**[接続]**をクリックします。接続ダイアログが表示されます。
3.  ダイアログで、接続文字列からプレフィックスを取得します。

### TiDB Serverless特別利用規約 {#tidb-serverless-special-terms-and-conditions}

-   TiDB Serverlessは現在ベータ版であり、ベータ段階中の稼働時間 SLA 保証はありません。 TiDB Serverless ベータ版を使用して商用または本番データセットを保存する場合、その使用に関連する潜在的なリスクはお客様ご自身で負う必要があり、PingCAP は損害に対して責任を負いません。
-   TiDB Cloud機能の一部は、TiDB Serverlessで部分的にサポートされているか、サポートされていません。詳細については[<a href="/tidb-cloud/serverless-tier-limitations.md">TiDB Serverlessの制限事項</a>](/tidb-cloud/serverless-tier-limitations.md)を参照してください。

## TiDB Dedicated {#tidb-dedicated}

TiDB D dedicated は、クロスゾーンの高可用性、水平スケーリング、および[<a href="https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing">HTAP</a>](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)利点を備えた本番環境向けです。

TiDB Dedicatedクラスターの場合、ビジネス ニーズに応じて TiDB、TiKV、およびTiFlashのクラスター サイズを簡単にカスタマイズできます。 TiKV ノードとTiFlashノードごとに、ノード上のデータが複製され、 [<a href="/tidb-cloud/high-availability-with-multi-az.md">高可用性</a>](/tidb-cloud/high-availability-with-multi-az.md)アベイラビリティ ゾーンに分散されます。

TiDB Dedicatedクラスターを作成するには、 [<a href="/tidb-cloud/tidb-cloud-billing.md#payment-method">支払い方法を追加する</a>](/tidb-cloud/tidb-cloud-billing.md#payment-method)または[<a href="/tidb-cloud/tidb-cloud-poc.md">概念実証 (PoC) トライアルに申し込む</a>](/tidb-cloud/tidb-cloud-poc.md)を行う必要があります。

> **ノート：**
>
> クラスターの作成後にノードstorageを減らすことはできません。
