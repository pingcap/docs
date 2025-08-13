---
title: Connect to Your TiDB Cloud Dedicated Cluster
summary: さまざまな方法でTiDB Cloud Dedicated クラスターに接続する方法を学習します。
---

# TiDB Cloud専用クラスタに接続する {#connect-to-your-tidb-cloud-dedicated-cluster}

このドキュメントでは、 TiDB Cloud Dedicated クラスターに接続する方法について説明します。

> **ヒント：**
>
> TiDB Cloud Starter またはTiDB Cloud Essential クラスターに接続する方法については、 [TiDB Cloud StarterまたはEssential クラスタに接続する](/tidb-cloud/connect-to-tidb-cluster-serverless.md)参照してください。

TiDB Cloud上にTiDB Cloud Cloud Dedicated クラスターが作成されたら、次のいずれかの方法でそのクラスターに接続できます。

-   直接接続

    直接接続では、TCP経由のMySQLネイティブ接続システムを使用します。1 など、MySQL接続をサポートする任意のツールを使用して、 TiDB Cloud Dedicatedクラスタに接続できます。TiDB TiDB Cloudは[SQLシェル](/tidb-cloud/connect-via-sql-shell.md)も提供しており、これを使用するとTiDB SQLを試用したり、TiDBとMySQLの互換性を迅速[MySQL コマンドラインクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)テストしたり、ユーザー権限を管理したりできます。

    TiDB Cloud Dedicated は、次の 3 種類のネットワーク接続を提供します。

    -   [パブリック接続](/tidb-cloud/connect-via-standard-connection.md)

        パブリック接続はトラフィックフィルター付きのパブリックエンドポイントを公開するため、ノートパソコンからSQLクライアント経由でTiDBクラスタに接続できます。TiDBクラスタへの接続にはTLSを使用できるため、アプリケーションからTiDBクラスタへのデータ転送のセキュリティが確保されます。詳細については、 [パブリック接続経由でTiDB Cloud Dedicated に接続](/tidb-cloud/connect-via-standard-connection.md)ご覧ください。

    -   プライベートエンドポイント（推奨）

        プライベートエンドポイント接続は、VPC内のSQLクライアントがTiDB Cloud Dedicatedクラスターに安全にアクセスできるようにするプライベートエンドポイントを提供します。これは、複数のクラウドプロバイダーが提供するプライベートリンクサービスを使用することで、簡素化されたネットワーク管理で、データベースサービスへの高度に安全な一方向アクセスを実現します。

        -   AWS でホストされているTiDB Cloud Dedicated クラスターの場合、プライベートエンドポイント接続には AWS PrivateLink が使用されます。詳細については、 [AWS PrivateLink 経由でTiDB Cloud専用クラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections.md)参照してください。
        -   AzureでホストされているTiDB Cloud Dedicatedクラスターの場合、プライベートエンドポイント接続にはAzure Private Linkが使用されます。詳細については、 [Azure Private Link 経由でTiDB Cloud専用クラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md)ご覧ください。
        -   Google Cloud でホストされているTiDB Cloud Dedicated クラスタの場合、プライベートエンドポイント接続には Google Cloud Private Service Connect が使用されます。詳細については、 [Google Cloud Private Service Connect 経由でTiDB Cloud専用クラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)ご覧ください。

    -   [VPCピアリング](/tidb-cloud/set-up-vpc-peering-connections.md)

        レイテンシーの低減とセキュリティの強化をご希望の場合は、VPCピアリングを設定し、クラウドアカウント内の対応するクラウドプロバイダーのVMインスタンスを使用してプライベートエンドポイント経由で接続してください。詳細については、 [VPC ピアリング経由でTiDB Cloud Dedicated に接続する](/tidb-cloud/set-up-vpc-peering-connections.md)ご覧ください。

-   [組み込みSQLエディタ](/tidb-cloud/explore-data-with-chat2query.md)

    > **注記：**
    >
    > [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターで SQL エディターを使用するには、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

    クラスターが AWS でホストされており、クラスターの TiDB バージョンが v6.5.0 以降である場合は、 [TiDB Cloudコンソール](https://tidbcloud.com/)の AI 支援 SQL エディターを使用してデータの価値を最大化できます。

    SQLエディタでは、SQLクエリを手動で記述するか、macOSでは<kbd>⌘</kbd> + <kbd>I</kbd> （WindowsまたはLinuxでは<kbd>Control</kbd> + <kbd>I</kbd> ）を押して[Chat2Query（ベータ版）](/tidb-cloud/tidb-cloud-glossary.md#chat2query) SQLクエリを自動生成させることができます。これにより、ローカルSQLクライアントなしでデータベースに対してSQLクエリを実行できます。クエリ結果は表やグラフで直感的に表示でき、クエリログも簡単に確認できます。

## 次は何？ {#what-s-next}

TiDB クラスターに正常に接続すると、 [TiDBでSQL文を調べる](/basic-sql-operations.md) 。
