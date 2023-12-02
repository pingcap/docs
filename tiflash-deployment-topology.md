---
title: TiFlash Deployment Topology
summary: Learn the deployment topology of TiFlash based on the minimal TiDB topology.
---

# TiFlash導入トポロジ {#tiflash-deployment-topology}

このドキュメントでは、最小の TiDB トポロジに基づいた[TiFlash](/tiflash/tiflash-overview.md)の展開トポロジについて説明します。

TiFlashはカラム型storageエンジンであり、徐々に標準のクラスター トポロジになりつつあります。リアルタイム HTAP アプリケーションに適しています。

## トポロジ情報 {#topology-information}

| 実例           | カウント | 物理マシンの構成                          | IP                                   | コンフィグレーション                  |
| :----------- | :--- | :-------------------------------- | :----------------------------------- | :-------------------------- |
| TiDB         | 3    | 16Vコア 32GB*1                      | 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9 | デフォルトのポート<br/>グローバルディレクトリ構成 |
| PD           | 3    | 4Vコア8GB*1                         | 10.0.1.4<br/> 10.0.1.5<br/> 10.0.1.6 | デフォルトのポート<br/>グローバルディレクトリ構成 |
| TiKV         | 3    | 16 VCore 32GB 2TB (nvme ssd) * 1  | 10.0.1.1<br/> 10.0.1.2<br/> 10.0.1.3 | デフォルトのポート<br/>グローバルディレクトリ構成 |
| TiFlash      | 1    | 32 VCore 64 GB 2TB (nvme ssd) * 1 | 10.0.1.11                            | デフォルトのポート<br/>グローバルディレクトリ構成 |
| モニタリングとグラファナ | 1    | 4 VCore 8GB * 1 500GB (SSD)       | 10.0.1.10                            | デフォルトのポート<br/>グローバルディレクトリ構成 |

### トポロジテンプレート {#topology-templates}

-   [TiFlashトポロジのシンプルなテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-tiflash.yaml)
-   [TiFlashトポロジの複雑なテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-tiflash.yaml)

上記の TiDB クラスター トポロジー ファイルの構成項目の詳細な説明については、 [TiUPを使用して TiDB を展開するためのトポロジコンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)を参照してください。

### 主要パラメータ {#key-parameters}

-   PD の[配置ルール](/configure-placement-rules.md)機能を有効にするには、構成テンプレートの`replication.enable-placement-rules`の値を`true`に設定します。
-   `tiflash_servers`のインスタンス レベル`"-host"`構成は IP のみをサポートし、ドメイン名はサポートしません。
-   TiFlashパラメータの詳細な説明については、 [TiFlashコンフィグレーション](/tiflash/tiflash-configuration.md)を参照してください。

> **注記：**
>
> -   構成ファイルに`tidb`ユーザーを手動で作成する必要はありません。 TiUPクラスターコンポーネントは、ターゲット マシン上に`tidb`のユーザーを自動的に作成します。ユーザーをカスタマイズしたり、ユーザーと制御マシンの一貫性を保つことができます。
> -   デプロイメント ディレクトリを相対パスとして構成すると、クラスターはユーザーのホーム ディレクトリにデプロイされます。
