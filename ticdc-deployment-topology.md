---
title: TiCDC Deployment Topology
summary: Learn the deployment topology of TiCDC based on the minimal TiDB topology.
---

# TiCDC展開トポロジ {#ticdc-deployment-topology}

> **ノート：**
>
> TiCDCは、v4.0.6以降の一般可用性（GA）の機能です。実稼働環境で使用できます。

このドキュメントでは、最小クラスタトポロジに基づく[TiCDC](/ticdc/ticdc-overview.md)の展開トポロジについて説明します。

TiCDCは、TiDB4.0で導入されたTiDBのインクリメンタルデータを複製するためのツールです。 TiDB、MySQL、MQなどの複数のダウンストリームプラットフォームをサポートします。 TiDB Binlogと比較して、TiCDCはレイテンシーが低く、ネイティブの高可用性を備えています。

## トポロジー情報 {#topology-information}

| 実例             | カウント | 物理マシン構成                        | 知財                                      | Configuration / コンフィグレーション  |
| :------------- | :--- | :----------------------------- | :-------------------------------------- | :-------------------------- |
| TiDB           | 3    | 16 VCore 32GB * 1              | 10.0.1.1<br/> 10.0.1.2<br/> 10.0.1.3    | デフォルトのポート<br/>グローバルディレクトリ構成 |
| PD             | 3    | 4 VCore 8GB * 1                | 10.0.1.4<br/> 10.0.1.5<br/> 10.0.1.6    | デフォルトのポート<br/>グローバルディレクトリ構成 |
| TiKV           | 3    | 16 VCore 32GB 2TB（nvme ssd）* 1 | 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9    | デフォルトのポート<br/>グローバルディレクトリ構成 |
| CDC            | 3    | 8 VCore 16GB * 1               | 10.0.1.11<br/> 10.0.1.12<br/> 10.0.1.13 | デフォルトのポート<br/>グローバルディレクトリ構成 |
| モニタリングとGrafana | 1    | 4 VCore 8GB * 1 500GB（ssd）     | 10.0.1.11                               | デフォルトのポート<br/>グローバルディレクトリ構成 |

### トポロジテンプレート {#topology-templates}

-   [TiCDCトポロジーの単純なテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-cdc.yaml)
-   [TiCDCトポロジの複雑なテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-cdc.yaml)

上記のTiDBクラスタトポロジファイルの構成項目の詳細については、 [TiUPを使用してTiDBを展開するためのトポロジConfiguration / コンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)を参照してください。

> **ノート：**
>
> -   構成ファイルに`tidb`人のユーザーを手動で作成する必要はありません。 TiUPクラスタコンポーネントは、ターゲットマシン上に`tidb`のユーザーを自動的に作成します。ユーザーをカスタマイズすることも、ユーザーと制御マシンの一貫性を保つこともできます。
> -   展開ディレクトリを相対パスとして構成すると、クラスタはユーザーのホームディレクトリに展開されます。
