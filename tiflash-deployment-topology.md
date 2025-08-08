---
title: TiFlash Deployment Topology
summary: 最小限の TiDB トポロジに基づくTiFlashの展開トポロジについて学習します。
---

# TiFlash展開トポロジ {#tiflash-deployment-topology}

このドキュメントでは、最小限の TiDB トポロジに基づく[TiFlash](/tiflash/tiflash-overview.md)のデプロイメント トポロジについて説明します。

TiFlashは列指向型storageエンジンであり、徐々に標準的なクラスタトポロジーになりつつあります。リアルタイムHTAPアプリケーションに適しています。

## トポロジ情報 {#topology-information}

| 実例             | カウント | 物理マシン構成                           | IP                                   | コンフィグレーション                 |
| :------------- | :--- | :-------------------------------- | :----------------------------------- | :------------------------- |
| TiDB           | 3    | 16 VCore 32GB * 1                 | 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9 | デフォルトポート<br/>グローバルディレクトリ構成 |
| PD             | 3    | 4 VCore 8GB * 1                   | 10.0.1.4<br/> 10.0.1.5<br/> 10.0.1.6 | デフォルトポート<br/>グローバルディレクトリ構成 |
| TiKV           | 3    | 16 VCore 32GB 2TB（NVMe SSD）* 1    | 10.0.1.1<br/> 10.0.1.2<br/> 10.0.1.3 | デフォルトポート<br/>グローバルディレクトリ構成 |
| TiFlash        | 1    | 32 VCore 64 GB 2TB (nvme ssd) * 1 | 10.0.1.11                            | デフォルトポート<br/>グローバルディレクトリ構成 |
| モニタリングとGrafana | 1    | 4 VCore 8GB * 1 500GB (SSD)       | 10.0.1.10                            | デフォルトポート<br/>グローバルディレクトリ構成 |

> **注記：**
>
> インスタンスのIPアドレスは例としてのみ示されています。実際の導入では、IPアドレスを実際のIPアドレスに置き換えてください。

### トポロジテンプレート {#topology-templates}

-   [TiFlashトポロジのシンプルなテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-tiflash.yaml)
-   [TiFlashトポロジの複雑なテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-tiflash.yaml)

上記の TiDB クラスター トポロジ ファイルの構成項目の詳細については、 [TiUPを使用して TiDB をデプロイするためのトポロジコンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)参照してください。

### 主なパラメータ {#key-parameters}

-   PD の[配置ルール](/configure-placement-rules.md)機能を有効にするには、構成テンプレートの`replication.enable-placement-rules`の値を`true`に設定します。
-   `tiflash_servers`のインスタンス レベル`"-host"`構成では、ドメイン名ではなく IP のみがサポートされます。
-   TiFlashパラメータの詳細な説明については、 [TiFlashコンフィグレーション](/tiflash/tiflash-configuration.md)参照してください。

> **注記：**
>
> -   設定ファイルに`tidb`ユーザーを手動で作成する必要はありません。TiUPTiUPコンポーネントは、ターゲットマシンに`tidb`ユーザーを自動的に作成します。ユーザーをカスタマイズすることも、制御マシンと同じユーザーを維持することもできます。
> -   デプロイメント ディレクトリを相対パスとして構成すると、クラスターはユーザーのホーム ディレクトリにデプロイされます。
