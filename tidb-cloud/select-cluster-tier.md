---
title: Select Your Cluster Tier
summary: Learn how to select your cluster tier on TiDB Cloud.
aliases: ['/tidbcloud/public-preview/developer-tier-cluster']
---

# Cluster Tierを選択する {#select-your-cluster-tier}

クラスター層によって、クラスターのスループットとパフォーマンスが決まります。

TiDB Cloudは、クラスター層の次の 2 つのオプションを提供します。クラスターを作成する前に、どのオプションがニーズに適しているかを検討する必要があります。

-   [Serverless Tier](#serverless-tier-beta)
-   [Dedicated Tier](#dedicated-tier)

## Serverless Tier(ベータ) {#serverless-tier-beta}

TiDB Cloud Serverless Tier (以前はDeveloper Tierと呼ばれていた) は、TiDB のフル マネージド サービスです。これはまだベータ版であり、本番環境では使用しないでください。ただし、Serverless Tierクラスターは、プロトタイプ アプリケーション、ハッカソン、アカデミック コースなどの非運用ワークロードに使用したり、データセットに一時的なデータ サービスを提供したりするために使用できます。

TiDB Cloudアカウントごとに、ベータ段階で使用する無料のServerless Tierクラスターを最大 5 つ作成できます。

### ユーザー名のプレフィックス {#user-name-prefix}

<!--Important: Do not update the section name "User name prefix" because this section is referenced by TiDB backend error messages.-->

Serverless Tierクラスターごとに、 TiDB Cloudは一意のプレフィックスを生成して、他のクラスターと区別します。

データベース ユーザー名を使用または設定するときは常に、ユーザー名にプレフィックスを含める必要があります。たとえば、クラスターのプレフィックスが`3pTAoNNegb47Uc8`であるとします。

-   クラスターに接続するには:

    ```shell
    mysql -u '3pTAoNNegb47Uc8.root' -h <host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_root_path> -p
    ```

    > **ノート：**
    >
    > Serverless Tierには TLS 接続が必要です。システムの CA ルート パスを見つけるには、 [ルート証明書のデフォルト パス](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md#root-certificate-default-path)を参照してください。

-   データベース ユーザーを作成するには:

    ```sql
    CREATE USER '3pTAoNNegb47Uc8.jeffrey';
    ```

クラスターのプレフィックスを取得するには、次の手順を実行します。

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。
2.  ターゲット クラスターの名前をクリックして概要ページに移動し、右上隅にある [**接続**] をクリックします。接続ダイアログが表示されます。
3.  ダイアログで、接続文字列からプレフィックスを取得します。

### Serverless Tierの特別利用規約 {#serverless-tier-special-terms-and-conditions}

-   Serverless Tierは現在ベータ版であり、ベータ フェーズ中のアップタイム SLA 保証はありません。 Serverless Tierベータ版を使用して商用または本番データセットを保存する場合、使用に伴う潜在的なリスクはご自身で負う必要があり、PingCAP はいかなる損害についても責任を負わないものとします。
-   一部のTiDB Cloud機能は、Serverless Tierで部分的にサポートされているか、サポートされていません。詳細は[Serverless Tierの制限](/tidb-cloud/serverless-tier-limitations.md)を参照してください。

## Dedicated Tier {#dedicated-tier}

TiDB Cloud Dedicated Tierは、クロスゾーンの高可用性、水平スケーリング、および[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)の利点を備えた、本番使用専用です。

Dedicated Tierクラスターの場合、ビジネス ニーズに応じて、TiDB、TiKV、およびTiFlashのクラスター サイズを簡単にカスタマイズできます。 TiKV ノードとTiFlashノードごとに、ノード上のデータが複製され、異なるアベイラビリティ ゾーンに分散され[高可用性](/tidb-cloud/high-availability-with-multi-az.md) 。

Dedicated Tierクラスターを作成するには、 [支払い方法を追加する](/tidb-cloud/tidb-cloud-billing.md#payment-method)または[概念実証 (PoC) トライアルに申し込む](/tidb-cloud/tidb-cloud-poc.md)が必要です。

> **ノート：**
>
> クラスターの作成後にノード ストレージを減らすことはできません。
