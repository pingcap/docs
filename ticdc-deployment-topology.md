---
title: TiCDC Deployment Topology
summary: Learn the deployment topology of TiCDC based on the minimal TiDB topology.
---

# TiCDC 導入トポロジ {#ticdc-deployment-topology}

> **注記：**
>
> TiCDC は、v4.0.6 以降の一般提供 (GA) の機能です。本番環境でも使用できます。

このドキュメントでは、最小クラスター トポロジに基づいた[TiCDC](/ticdc/ticdc-overview.md)の展開トポロジについて説明します。

TiCDC は、TiDB 4.0 で導入された、TiDB の増分データを複製するためのツールです。 TiDB、MySQL、Kafka、MQ、storageサービスなどの複数のダウンストリーム プラットフォームをサポートします。 TiDB Binlogと比較して、TiCDC はレイテンシーが低く、ネイティブの高可用性を備えています。

## トポロジ情報 {#topology-information}

| 実例           | カウント | 物理マシンの構成                         | IP                                      | コンフィグレーション                  |
| :----------- | :--- | :------------------------------- | :-------------------------------------- | :-------------------------- |
| TiDB         | 3    | 16Vコア 32GB*1                     | 10.0.1.1<br/> 10.0.1.2<br/> 10.0.1.3    | デフォルトのポート<br/>グローバルディレクトリ構成 |
| PD           | 3    | 4Vコア8GB*1                        | 10.0.1.4<br/> 10.0.1.5<br/> 10.0.1.6    | デフォルトのポート<br/>グローバルディレクトリ構成 |
| TiKV         | 3    | 16 VCore 32GB 2TB (nvme ssd) * 1 | 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9    | デフォルトのポート<br/>グローバルディレクトリ構成 |
| CDC          | 3    | 8Vコア16GB*1                       | 10.0.1.11<br/> 10.0.1.12<br/> 10.0.1.13 | デフォルトのポート<br/>グローバルディレクトリ構成 |
| モニタリングとグラファナ | 1    | 4 VCore 8GB * 1 500GB (SSD)      | 10.0.1.11                               | デフォルトのポート<br/>グローバルディレクトリ構成 |

### トポロジテンプレート {#topology-templates}

-   [TiCDC トポロジのシンプルなテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-cdc.yaml)
-   [TiCDC トポロジの複雑なテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-cdc.yaml)

上記の TiDB クラスター トポロジー ファイルの構成項目の詳細な説明については、 [TiUPを使用して TiDB を展開するためのトポロジコンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)を参照してください。

> **注記：**
>
> -   構成ファイルに`tidb`ユーザーを手動で作成する必要はありません。 TiUPクラスターコンポーネントは、ターゲット マシン上に`tidb`のユーザーを自動的に作成します。ユーザーをカスタマイズしたり、ユーザーと制御マシンの一貫性を保つことができます。
> -   デプロイメント ディレクトリを相対パスとして構成すると、クラスターはユーザーのホーム ディレクトリにデプロイされます。
