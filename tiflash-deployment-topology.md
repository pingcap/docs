---
title: TiFlash Deployment Topology
summary: Learn the deployment topology of TiFlash based on the minimal TiDB topology.
---

# TiFlash導入トポロジ {#tiflash-deployment-topology}

このドキュメントでは、最小限の TiDB トポロジに基づく[TiFlash](/tiflash/tiflash-overview.md)の展開トポロジについて説明します。

TiFlashは柱状storageエンジンであり、徐々に標準のクラスタ トポロジになります。リアルタイム HTAP アプリケーションに適しています。

## トポロジ情報 {#topology-information}

| 実例         | カウント | 物理マシン構成                          | 知財                                   | コンフィグレーション                    |
| :--------- | :--- | :------------------------------- | :----------------------------------- | :---------------------------- |
| TiDB       | 3    | 16 仮想コア 32GB * 1                 | 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9 | デフォルトのポート<br/>グローバル ディレクトリの構成 |
| PD         | 3    | 4 Vコア 8GB * 1                    | 10.0.1.4<br/> 10.0.1.5<br/> 10.0.1.6 | デフォルトのポート<br/>グローバル ディレクトリの構成 |
| TiKV       | 3    | 16 仮想コア 32GB 2TB (nvme ssd) * 1  | 10.0.1.1<br/> 10.0.1.2<br/> 10.0.1.3 | デフォルトのポート<br/>グローバル ディレクトリの構成 |
| TiFlash    | 1    | 32 仮想コア 64 GB 2TB (nvme ssd) * 1 | 10.0.1.11                            | デフォルトのポート<br/>グローバル ディレクトリの構成 |
| 監視とGrafana | 1    | 4 仮想コア 8GB * 1 500GB (ssd)       | 10.0.1.10                            | デフォルトのポート<br/>グローバル ディレクトリの構成 |

### トポロジ テンプレート {#topology-templates}

-   [TiFlashトポロジのシンプルなテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-tiflash.yaml)
-   [TiFlashトポロジの複雑なテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-tiflash.yaml)

上記の TiDB クラスター トポロジ ファイルの構成項目の詳細な説明については、 [TiUPを使用して TiDB をデプロイするためのトポロジコンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)を参照してください。

### 主なパラメータ {#key-parameters}

-   PD の[配置ルール](/configure-placement-rules.md)機能を有効にするには、構成テンプレートで`replication.enable-placement-rules`の値を`true`に設定します。
-   `tiflash_servers`のインスタンス レベル`"-host"`構成は、IP のみをサポートし、ドメイン名はサポートしません。
-   詳細なTiFlashパラメータの説明については、 [TiFlashのコンフィグレーション](/tiflash/tiflash-configuration.md)を参照してください。

> **ノート：**
>
> -   構成ファイルで`tidb`ユーザーを手動で作成する必要はありません。 TiUPクラスターコンポーネントは、ターゲット マシンに`tidb`ユーザーを自動的に作成します。ユーザーをカスタマイズしたり、ユーザーと制御マシンとの一貫性を保つことができます。
> -   展開ディレクトリを相対パスとして構成すると、クラスターはユーザーのホーム ディレクトリに展開されます。
