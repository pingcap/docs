---
title: PD Microservice Deployment Topology
summary: 最小限の TiDB トポロジに基づく PD マイクロサービスのデプロイメント トポロジを学習します。
---

# PDマイクロサービスデプロイメントトポロジ {#pd-microservice-deployment-topology}

このドキュメントでは、最小限の TiDB トポロジに基づく[PDマイクロサービス](/pd-microservices.md)のデプロイメント トポロジについて説明します。

## トポロジ情報 {#topology-information}

| 実例             | カウント | 物理マシン構成                        | IP                                      | コンフィグレーション                 |
| :------------- | :--- | :----------------------------- | :-------------------------------------- | :------------------------- |
| TiDB           | 2    | 16 VCore 32GB * 1              | 10.0.1.1<br/> 10.0.1.2                  | デフォルトポート<br/>グローバルディレクトリ構成 |
| PD             | 3    | 4 VCore 8GB * 1                | 10.0.1.3<br/> 10.0.1.4<br/> 10.0.1.5    | デフォルトポート<br/>グローバルディレクトリ構成 |
| TSO            | 2    | 4 VCore 8GB * 1                | 10.0.1.6<br/> 10.0.1.7                  | デフォルトポート<br/>グローバルディレクトリ構成 |
| スケジュール         | 2    | 4 VCore 8GB * 1                | 10.0.1.8<br/> 10.0.1.9                  | デフォルトポート<br/>グローバルディレクトリ構成 |
| TiKV           | 3    | 16 VCore 32GB 2TB（NVMe SSD）* 1 | 10.0.1.10<br/> 10.0.1.11<br/> 10.0.1.12 | デフォルトポート<br/>グローバルディレクトリ構成 |
| モニタリングとGrafana | 1    | 4 VCore 8GB * 1 500GB (SSD)    | 10.0.1.13                               | デフォルトポート<br/>グローバルディレクトリ構成 |

> **注記：**
>
> インスタンスのIPアドレスは例としてのみ示されています。実際の導入では、IPアドレスを実際のIPアドレスに置き換えてください。

### トポロジテンプレート {#topology-template}

<details><summary>PDマイクロサービストポロジのシンプルなテンプレート</summary>

```yaml
# # Global variables are applied to all deployments and used as the default value of
# # the deployments if a specific deployment value is missing.
global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/tidb-deploy"
  data_dir: "/tidb-data"
  listen_host: 0.0.0.0
  arch: "amd64"
  pd_mode: "ms" # To enable PD microservices, you must specify this field as "ms".

monitored:
  node_exporter_port: 9200
  blackbox_exporter_port: 9215

# # Specifies the configuration of PD servers.
pd_servers:
  - host: 10.0.1.3
  - host: 10.0.1.4
  - host: 10.0.1.5

# # Specifies the configuration of TiDB servers.
tidb_servers:
  - host: 10.0.1.1
  - host: 10.0.1.2

# # Specifies the configuration of TiKV servers.
tikv_servers:
  - host: 10.0.1.10
  - host: 10.0.1.11
  - host: 10.0.1.12

# # Specifies the configuration of TSO servers.
tso_servers:
  - host: 10.0.1.6
  - host: 10.0.1.7

# # Specifies the configuration of Scheduling servers.
scheduling_servers:
  - host: 10.0.1.8
  - host: 10.0.1.9

# # Specifies the configuration of Prometheus servers.
monitoring_servers:
  - host: 10.0.1.13

# # Specifies the configuration of Grafana servers.
grafana_servers:
  - host: 10.0.1.13
```

</details>

前述の TiDB クラスター トポロジ ファイルの構成項目の詳細については、 [TiUPを使用して TiDB をデプロイするためのトポロジ構成ファイル](/tiup/tiup-cluster-topology-reference.md)参照してください。

### 主なパラメータ {#key-parameters}

-   `tso_servers`のインスタンスのレベル`host`構成では、ドメイン名ではなく IP アドレスのみがサポートされます。
-   TSO 構成項目の詳細については、 [TSO 構成ファイル](/tso-configuration-file.md)参照してください。
-   `scheduling_servers`のインスタンスのレベル`host`構成では、ドメイン名ではなく IP アドレスのみがサポートされます。
-   スケジュール設定項目の詳細については、 [スケジュール設定ファイル](/scheduling-configuration-file.md)参照してください。

> **注記：**
>
> -   設定ファイルに`tidb`ユーザーを手動で作成する必要はありません。TiUPTiUPコンポーネントは、ターゲットマシンに`tidb`ユーザーを自動的に作成します。ユーザーをカスタマイズすることも、制御マシンと同じユーザーを維持することもできます。
> -   デプロイメント ディレクトリを相対パスとして構成すると、クラスターはユーザーのホーム ディレクトリにデプロイされます。
