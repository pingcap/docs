---
title: Connect to Your TiDB Cloud Dedicated Cluster
summary: さまざまな方法でTiDB Cloud Dedicatedクラスターに接続する方法を学びましょう。
---

# TiDB Cloud Dedicatedクラスタに接続します {#connect-to-your-tidb-cloud-dedicated-cluster}

このドキュメントでは、TiDB Cloud Dedicatedクラスタへの接続方法について説明します。

> **ヒント：**
>
> -   TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスに接続する方法については、 [TiDB Cloud StarterまたはEssentialインスタンスに接続します](/tidb-cloud/connect-to-tidb-cluster-serverless.md)参照してください。
> -   このドキュメントでは、 TiDB Cloud Dedicatedのネットワーク接続方法について説明します。特定のツール、ドライバ、または ORM を介して TiDB に接続する方法については、 [TiDBに接続する](/develop/dev-guide-connect-to-tidb.md)参照してください。

TiDB TiDB Cloud TiDB Cloud Dedicatedクラスタが作成されたら、以下のいずれかのネットワーク接続方法で接続できます。

-   直接接続

    直接接続では、TCP 上で MySQL のネイティブ接続システムを使用します。MySQL 接続をサポートするツールであれば、MySQL シェルなどを使用してTiDB Cloud Dedicated[MySQLコマンドラインクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)に接続できます。 TiDB Cloud は[SQLシェル](/tidb-cloud/connect-via-sql-shell.md)も提供しており、 TiDB SQL を試用したり、TiDB と MySQL の互換性を迅速にテストしたり、ユーザー権限を管理したりできます。

    TiDB Cloud Dedicatedは、3種類のネットワーク接続タイプを提供します。

    -   [パブリック接続](/tidb-cloud/connect-via-standard-connection.md)

        パブリック接続はトラフィック フィルターを備えたパブリック エンドポイントを公開するため、ラップトップから SQL クライアント経由で TiDB クラスターに接続できます。 TLS を使用して TiDB クラスターに接続できます。これにより、アプリケーションから TiDB クラスターへのデータ送信のセキュリティが確保されます。詳細については、 [パブリック接続経由​​でTiDB Cloud Dedicatedに接続します](/tidb-cloud/connect-via-standard-connection.md)参照してください。

    -   プライベートエンドポイント（推奨）

        プライベートエンドポイント接続は、VPC内のSQLクライアントがTiDB Cloud Dedicatedクラスターに安全にアクセスできるようにするためのプライベートエンドポイントを提供します。これは、さまざまなクラウドプロバイダーが提供するプライベートリンクサービスを利用しており、ネットワーク管理を簡素化しながら、データベースサービスへの高度に安全な一方向アクセスを実現します。

        -   AWS でホストされているTiDB Cloud Dedicatedクラスターの場合、プライベート エンドポイント接続は AWS PrivateLink を使用します。詳細については、 [AWS PrivateLink を介してTiDB Cloud Dedicatedクラスタに接続します。](/tidb-cloud/set-up-private-endpoint-connections.md)参照してください。
        -   Azure 上でホストされているTiDB Cloud Dedicatedクラスターの場合、プライベート エンドポイント接続は Azure Private Link を使用します。詳細については、 [Azureプライベートリンクを介してTiDB Cloud Dedicatedクラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md)参照してください。
        -   Google Cloud でホストされているTiDB Cloud Dedicatedクラスターの場合、プライベート エンドポイント接続は Google Cloud Private Service Connect を使用します。詳細については、 [Google Cloud Private Service Connect を介してTiDB Cloud Dedicatedクラスタに接続します。](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)参照してください。

    -   [VPCピアリング](/tidb-cloud/set-up-vpc-peering-connections.md)

        レイテンシーを短縮し、セキュリティを強化したい場合は、VPC ピアリングを設定し、クラウド アカウント内の対応するクラウド プロバイダー上の VM インスタンスを使用してプライベート エンドポイント経由で接続します。詳細については、 [VPCピアリング経由でTiDB Cloud Dedicatedに接続します](/tidb-cloud/set-up-vpc-peering-connections.md)参照してください。

-   [組み込みSQLエディタ](/tidb-cloud/explore-data-with-chat2query.md)

    > **注記：**
    >
    > [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスタでSQLエディタを使用するには、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

    クラスターがAWS上でホストされており、クラスターのTiDBバージョンがv6.5.0以降である場合、 [TiDB Cloudコンソール](https://tidbcloud.com/)のAI支援SQLエディタを使用して、データの価値を最大化できます。

    SQLエディタでは、SQLクエリを手動で記述することも、macOSでは<kbd>⌘</kbd> + <kbd>I</kbd> （WindowsまたはLinuxでは<kbd>Control</kbd> + <kbd>I</kbd> ）を押すだけで[Chat2Query（ベータ版）](/tidb-cloud/tidb-cloud-glossary.md#chat2query)にSQLクエリを自動生成させることもできます。これにより、ローカルSQLクライアントがなくてもデータベースに対してSQLクエリを実行できます。クエリ結果は表やグラフで直感的に表示でき、クエリログも簡単に確認できます。

## 次は？ {#what-s-next}

TiDB クラスターに正常に接続したら、 [TiDBを使用してSQLステートメントを探索する](/basic-sql-operations.md)ことができます。
