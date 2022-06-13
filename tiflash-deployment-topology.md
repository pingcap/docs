---
title: TiFlash Deployment Topology
summary: Learn the deployment topology of TiFlash based on the minimal TiDB topology.
---

# TiFlash展開トポロジ {#tiflash-deployment-topology}

このドキュメントでは、最小のTiDBトポロジに基づく[TiFlash](/tiflash/tiflash-overview.md)の展開トポロジについて説明します。

TiFlashは列指向ストレージエンジンであり、徐々に標準のクラスタトポロジになります。リアルタイムHTAPアプリケーションに適しています。

## トポロジー情報 {#topology-information}

| 実例             | カウント | 物理マシン構成                         | IP                                   | Configuration / コンフィグレーション  |
| :------------- | :--- | :------------------------------ | :----------------------------------- | :-------------------------- |
| TiDB           | 3    | 16 VCore 32GB * 1               | 10.0.1.1<br/> 10.0.1.2<br/> 10.0.1.3 | デフォルトのポート<br/>グローバルディレクトリ構成 |
| PD             | 3    | 4 VCore 8GB * 1                 | 10.0.1.4<br/> 10.0.1.5<br/> 10.0.1.6 | デフォルトのポート<br/>グローバルディレクトリ構成 |
| TiKV           | 3    | 16 VCore 32GB 2TB（nvme ssd）* 1  | 10.0.1.1<br/> 10.0.1.2<br/> 10.0.1.3 | デフォルトのポート<br/>グローバルディレクトリ構成 |
| TiFlash        | 1    | 32 VCore 64 GB 2TB（nvme ssd）* 1 | 10.0.1.10                            | デフォルトのポート<br/>グローバルディレクトリ構成 |
| モニタリングとGrafana | 1    | 4 VCore 8GB * 1 500GB（ssd）      | 10.0.1.10                            | デフォルトのポート<br/>グローバルディレクトリ構成 |

### トポロジテンプレート {#topology-templates}

-   [TiFlashトポロジのシンプルなテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-tiflash.yaml)
-   [TiFlashトポロジの複雑なテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-tiflash.yaml)

上記のTiDBクラスタトポロジファイルの構成項目の詳細については、 [TiUPを使用してTiDBを展開するためのトポロジConfiguration / コンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)を参照してください。

### 重要なパラメータ {#key-parameters}

-   PDの[配置ルール](/configure-placement-rules.md)機能を有効にするには、構成テンプレートの値`replication.enable-placement-rules`を`true`に設定します。
-   `tiflash_servers`のインスタンスレベル`"-host"`構成は、ドメイン名ではなくIPのみをサポートします。
-   TiFlashパラメータの詳細については、 [TiFlashConfiguration / コンフィグレーション](/tiflash/tiflash-configuration.md)を参照してください。

> **ノート：**
>
> -   構成ファイルに`tidb`人のユーザーを手動で作成する必要はありません。 TiUPクラスタコンポーネントは、ターゲットマシン上に`tidb`のユーザーを自動的に作成します。ユーザーをカスタマイズすることも、ユーザーを制御マシンとの一貫性を保つこともできます。
> -   展開ディレクトリを相対パスとして構成すると、クラスタはユーザーのホームディレクトリに展開されます。
