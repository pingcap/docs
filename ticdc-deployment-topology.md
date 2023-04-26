---
title: TiCDC Deployment Topology
summary: Learn the deployment topology of TiCDC based on the minimal TiDB topology.
---

# TiCDC 導入トポロジ {#ticdc-deployment-topology}

> **ノート：**
>
> TiCDC は、v4.0.6 以降の一般提供 (GA) の機能です。本番環境で使用できます。

このドキュメントでは、最小限のクラスタ トポロジに基づく[TiCDC](/ticdc/ticdc-overview.md)の展開トポロジについて説明します。

TiCDC は、TiDB 4.0 で導入された、TiDB の増分データを複製するためのツールです。 TiDB、MySQL、MQ など、複数のダウンストリーム プラットフォームをサポートしています。 TiDB Binlogと比較して、TiCDC はレイテンシーが低く、ネイティブの高可用性を備えています。

## トポロジ情報 {#topology-information}

| 実例         | カウント | 物理マシン構成                         | 知財                                      | コンフィグレーション                    |
| :--------- | :--- | :------------------------------ | :-------------------------------------- | :---------------------------- |
| TiDB       | 3    | 16 仮想コア 32GB * 1                | 10.0.1.1<br/> 10.0.1.2<br/> 10.0.1.3    | デフォルトのポート<br/>グローバル ディレクトリの構成 |
| PD         | 3    | 4 Vコア 8GB * 1                   | 10.0.1.4<br/> 10.0.1.5<br/> 10.0.1.6    | デフォルトのポート<br/>グローバル ディレクトリの構成 |
| TiKV       | 3    | 16 仮想コア 32GB 2TB (nvme ssd) * 1 | 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9    | デフォルトのポート<br/>グローバル ディレクトリの構成 |
| CDC        | 3    | 8 Vコア 16GB * 1                  | 10.0.1.11<br/> 10.0.1.12<br/> 10.0.1.13 | デフォルトのポート<br/>グローバル ディレクトリの構成 |
| 監視とGrafana | 1    | 4 仮想コア 8GB * 1 500GB (ssd)      | 10.0.1.11                               | デフォルトのポート<br/>グローバル ディレクトリの構成 |

### トポロジ テンプレート {#topology-templates}

-   [TiCDC トポロジーの単純なテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-cdc.yaml)
-   [TiCDC トポロジの複雑なテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-cdc.yaml)

上記の TiDB クラスター トポロジ ファイルの構成項目の詳細な説明については、 [TiUPを使用して TiDB をデプロイするためのトポロジコンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)を参照してください。

> **ノート：**
>
> -   構成ファイルで`tidb`ユーザーを手動で作成する必要はありません。 TiUPクラスターコンポーネントは、ターゲット マシンに`tidb`ユーザーを自動的に作成します。ユーザーをカスタマイズしたり、ユーザーと制御マシンとの一貫性を保つことができます。
> -   展開ディレクトリを相対パスとして構成すると、クラスターはユーザーのホーム ディレクトリに展開されます。
