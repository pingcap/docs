---
title: TiProxy Deployment Topology
summary: 最小限の TiDB トポロジに基づく TiProxy の展開トポロジについて学習します。
---

# TiProxy 展開トポロジ {#tiproxy-deployment-topology}

このドキュメントでは、最小限の TiDB トポロジに基づく[TiProxy](/tiproxy/tiproxy-overview.md)のデプロイメント トポロジについて説明します。

その他の展開方法については、次のドキュメントを参照してください。

-   TiDB Operatorを使用して TiProxy をデプロイするには、 [TiDB Operator](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/deploy-tiproxy)ドキュメントを参照してください。
-   TiUPを使用して TiProxy をローカルに素早く展開するには、 [TiProxyをデプロイ](/tiup/tiup-playground.md#deploy-tiproxy)参照してください。
-   TiUPを使用して TiProxy を展開するには、 [インストールと使用方法](/tiproxy/tiproxy-overview.md#installation-and-usage)参照してください。

TiProxy は TiDB の L7 プロキシサーバーであり、接続のバランスを取り、可能な場合はセッションを移行できます。

## トポロジ情報 {#topology-information}

| 実例             | カウント | 物理マシン構成                        | IP                                   | コンフィグレーション                 |
| :------------- | :--- | :----------------------------- | :----------------------------------- | :------------------------- |
| TiDB           | 3    | 16 VCore 32GB * 3              | 10.0.1.4<br/> 10.0.1.5<br/> 10.0.1.6 | デフォルトポート<br/>グローバルディレクトリ構成 |
| PD             | 3    | 4 VCore 8GB * 3                | 10.0.1.1<br/> 10.0.1.2<br/> 10.0.1.3 | デフォルトポート<br/>グローバルディレクトリ構成 |
| TiKV           | 3    | 16 VCore 32GB 2TB（NVMe SSD）* 3 | 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9 | デフォルトポート<br/>グローバルディレクトリ構成 |
| TiProxy        | 2    | 4 VCore 8 GB * 1               | 10.0.1.11<br/> 10.0.1.12             | デフォルトポート<br/>グローバルディレクトリ構成 |
| モニタリングとGrafana | 1    | 4 VCore 8GB * 1 500GB (SSD)    | 10.0.1.13                            | デフォルトポート<br/>グローバルディレクトリ構成 |

> **注記：**
>
> インスタンスのIPアドレスは例としてのみ示されています。実際の導入では、IPアドレスを実際のIPアドレスに置き換えてください。

### トポロジテンプレート {#topology-templates}

TiProxy のテンプレートの詳細については、 [TiProxyトポロジのシンプルなテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-tiproxy.yaml)参照してください。

前述の TiDB クラスター トポロジ ファイルの構成項目の詳細については、 [TiUPを使用して TiDB をデプロイするためのトポロジコンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)参照してください。

### 主なパラメータ {#key-parameters}

-   `tiproxy_servers`のインスタンス レベル`"-host"`構成では、ドメイン名ではなく IP のみがサポートされます。
-   TiProxy パラメータの詳細な説明については、 [TiProxy のコンフィグレーション](/tiproxy/tiproxy-configuration.md)参照してください。

> **注記：**
>
> -   設定ファイルに`tidb`ユーザーを手動で作成する必要はありません。TiUPTiUPコンポーネントは、ターゲットマシンに`tidb`ユーザーを自動的に作成します。ユーザーをカスタマイズすることも、コントロールマシンと同じユーザーを維持することもできます。
> -   デプロイメント ディレクトリを相対パスとして構成すると、クラスターはユーザーのホーム ディレクトリにデプロイされます。
