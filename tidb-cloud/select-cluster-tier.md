---
title: Select Your Cluster Tier
summary: Learn how to select your cluster tier on TiDB Cloud.
---

# Cluster Tierを選択してください {#select-your-cluster-tier}

クラスター層によって、クラスターのスループットとパフォーマンスが決まります。

TiDB Cloud、次の 2 つのクラスター層のオプションが提供されます。クラスターを作成する前に、どちらのオプションがニーズに適しているかを検討する必要があります。

-   [TiDB サーバーレス](#tidb-serverless)
-   [TiDB専用](#tidb-dedicated)

## TiDB サーバーレス {#tidb-serverless}

<!--To be confirmed-->

TiDB Serverless は、フルマネージドのマルチテナント TiDB 製品です。即時自動スケーリングの MySQL 互換データベースを提供し、豊富な無料枠と、無料制限を超えた場合の従量制課金を提供します。

### 使用量割り当て {#usage-quota}

TiDB Cloudの組織ごとに、デフォルトで最大 5 つの TiDB サーバーレス クラスターを作成できます。さらに TiDB サーバーレス クラスターを作成するには、クレジット カードを追加し、使用量を[支出制限](/tidb-cloud/tidb-cloud-glossary.md#spending-limit)に設定する必要があります。

組織内の最初の 5 つの TiDB サーバーレス クラスターに対して、 TiDB Cloud は各クラスターに次のように無料の使用量クォータを提供します。

-   行ベースのstorage: 5 GiB
-   [リクエストユニット (RU)](/tidb-cloud/tidb-cloud-glossary.md#request-unit) : 月あたり 5,000 万 RU

リクエスト ユニット (RU) は、データベースへの 1 回のリクエストによって消費されるリソースの量を表すために使用される測定単位です。要求によって消費される RU の量は、操作の種類や取得または変更されるデータの量などのさまざまな要因によって異なります。

クラスターの無料クォータに達すると、このクラスターでの読み取りおよび書き込み操作は、新しい月の初めに使用量が[割り当てを増やす](/tidb-cloud/manage-serverless-spend-limit.md#update-spending-limit)されるまでスロットルされます。たとえば、クラスターのstorageが 5 GiB を超えると、単一トランザクションの最大サイズ制限が 10 MiB から 1 MiB に減ります。

さまざまなリソース (読み取り、書き込み、SQL CPU、ネットワーク下りなど) の RU 消費量、料金の詳細、および調整された情報の詳細については、 [TiDB サーバーレスの料金詳細](https://www.pingcap.com/tidb-cloud-serverless-pricing-details)を参照してください。

### ユーザー名のプレフィックス {#user-name-prefix}

<!--Important: Do not update the section name "User name prefix" because this section is referenced by TiDB backend error messages.-->

TiDB サーバーレス クラスターごとに、 TiDB Cloudは他のクラスターと区別するための一意のプレフィックスを生成します。

データベース ユーザー名を使用または設定するときは、ユーザー名に接頭辞を含める必要があります。たとえば、クラスターのプレフィックスが`3pTAoNNegb47Uc8`であると仮定します。

-   クラスターに接続するには:

    ```shell
    mysql -u '3pTAoNNegb47Uc8.root' -h <host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_root_path> -p
    ```

    > **注記：**
    >
    > TiDB サーバーレスには TLS 接続が必要です。システム上の CA ルート パスを見つけるには、 [ルート証明書のデフォルトのパス](/tidb-cloud/secure-connections-to-serverless-clusters.md#root-certificate-default-path)を参照してください。

-   データベース ユーザーを作成するには:

    ```sql
    CREATE USER '3pTAoNNegb47Uc8.jeffrey';
    ```

クラスターのプレフィックスを取得するには、次の手順を実行します。

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。
2.  ターゲット クラスターの名前をクリックして概要ページに移動し、右上隅の**[接続]**をクリックします。接続ダイアログが表示されます。
3.  ダイアログで、接続文字列からプレフィックスを取得します。

### TiDB サーバーレス特別利用規約 {#tidb-serverless-special-terms-and-conditions}

TiDB Cloud機能の一部は、TiDB サーバーレスで部分的にサポートされているか、サポートされていません。詳細については[TiDB サーバーレスの制限事項](/tidb-cloud/serverless-limitations.md)を参照してください。

## TiDB専用 {#tidb-dedicated}

TiDB D dedicated は、クロスゾーンの高可用性、水平スケーリング、および[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)利点を備えた本番環境向けです。

TiDB 専用クラスターの場合、ビジネス ニーズに応じて TiDB、TiKV、およびTiFlashのクラスター サイズを簡単にカスタマイズできます。 TiKV ノードとTiFlashノードごとに、ノード上のデータが複製され、 [高可用性](/tidb-cloud/high-availability-with-multi-az.md)アベイラビリティ ゾーンに分散されます。

TiDB 専用クラスターを作成するには、 [支払い方法を追加する](/tidb-cloud/tidb-cloud-billing.md#payment-method)または[概念実証 (PoC) トライアルに申し込む](/tidb-cloud/tidb-cloud-poc.md)を行う必要があります。

> **注記：**
>
> クラスターの作成後にノードstorageを減らすことはできません。
