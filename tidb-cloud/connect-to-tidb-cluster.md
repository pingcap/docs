---
title: Connect to Your TiDB Cloud Dedicated Cluster
summary: さまざまな方法でTiDB Cloud Dedicated クラスターに接続する方法を学習します。
---

# TiDB Cloud専用クラスタに接続する {#connect-to-your-tidb-cloud-dedicated-cluster}

このドキュメントでは、TiDB Cloud Dedicated クラスターに接続する方法について説明します。

> **ヒント：**
>
> TiDB Cloud Serverless クラスターに接続する方法については、 [TiDB Cloudサーバーレスクラスタに接続する](/tidb-cloud/connect-to-tidb-cluster-serverless.md)参照してください。

TiDB Cloud上にTiDB Cloud Dedicated クラスターが作成されたら、次のいずれかの方法でそのクラスターに接続できます。

-   直接接続

    直接接続では、 [MySQL コマンドラインクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)経由の MySQL ネイティブ接続システムが使用されます。1 などの MySQL 接続をサポートする任意のツールを使用して、TiDB Cloud Dedicated クラスターに接続できます。TiDB TiDB Cloud[SQL シェル](/tidb-cloud/connect-via-sql-shell.md)も提供されており、これを使用すると、 TiDB SQL を試したり、TiDB と MySQL の互換性をすばやくテストしたり、ユーザー権限を管理したりできます。

    TiDB Cloud Dedicated は、次の 3 種類のネットワーク接続を提供します。

    -   [パブリック接続](/tidb-cloud/connect-via-standard-connection.md)

        パブリック接続では、トラフィック フィルター付きのパブリック エンドポイントが公開されるため、ノート PC から SQL クライアントを介して TiDB クラスターに接続できます。TLS を使用して TiDB クラスターに接続できるため、アプリケーションから TiDB クラスターへのデータ転送のセキュリティが確保されます。詳細については、 [パブリック接続経由​​でTiDB Cloud Dedicatedに接続する](/tidb-cloud/connect-via-standard-connection.md)を参照してください。

    -   プライベートエンドポイント（推奨）

        プライベート エンドポイント接続は、VPC 内の SQL クライアントがTiDB Cloud Dedicated クラスターに安全にアクセスできるようにするプライベート エンドポイントを提供します。これは、さまざまなクラウド プロバイダーによって提供されるプライベート リンク サービスを使用し、簡素化されたネットワーク管理でデータベース サービスへの非常に安全な一方向アクセスを提供します。

        -   AWS でホストされているTiDB Cloud Dedicated クラスターの場合、プライベートエンドポイント接続には AWS PrivateLink が使用されます。詳細については、 [AWS のプライベートエンドポイント経由でTiDB Cloud専用クラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections.md)参照してください。
        -   Google Cloud でホストされているTiDB Cloud Dedicated クラスタの場合、プライベート エンドポイント接続には Google Cloud Private Service Connect が使用されます。詳細については、 [Google Cloud Private Service Connect 経由でTiDB Cloud専用クラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)ご覧ください。

    -   [VPC ピアリング](/tidb-cloud/set-up-vpc-peering-connections.md)

        レイテンシーを低くしてセキュリティを強化したい場合は、VPC ピアリングを設定し、クラウド アカウント内の対応するクラウド プロバイダーの VM インスタンスを使用してプライベート エンドポイント経由で接続します。詳細については、 [VPC ピアリング経由でTiDB Cloud Dedicated に接続する](/tidb-cloud/set-up-vpc-peering-connections.md)を参照してください。

-   [組み込みSQLエディタ](/tidb-cloud/explore-data-with-chat2query.md)

    > **注記：**
    >
    > [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターで SQL エディターを使用するには、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

    クラスターが AWS でホストされており、クラスターの TiDB バージョンが v6.5.0 以降である場合は、 [TiDB Cloudコンソール](https://tidbcloud.com/)の AI 支援 SQL エディターを使用してデータの価値を最大化できます。

    SQL エディターでは、SQL クエリを手動で記述するか、macOS では<kbd>⌘</kbd> + <kbd>I</kbd> (Windows または Linux では<kbd>Control</kbd> + <kbd>I</kbd> ) を押して[Chat2Query (ベータ版)](/tidb-cloud/tidb-cloud-glossary.md#chat2query) SQL クエリを自動的に生成するように指示することができます。これにより、ローカル SQL クライアントを使用せずにデータベースに対して SQL クエリを実行できます。クエリ結果をテーブルやグラフで直感的に表示し、クエリ ログを簡単に確認できます。

## 次は何か {#what-s-next}

TiDB クラスターに正常に接続されたら、 [TiDBでSQL文を調べる](/basic-sql-operations.md)実行できます。
