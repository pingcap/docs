---
title: Minimal Deployment Topology
summary: Learn the minimal deployment topology of TiDB clusters.
---

# 最小限の展開トポロジ {#minimal-deployment-topology}

このドキュメントでは、TiDBクラスタの最小限の展開トポロジについて説明します。

## トポロジー情報 {#topology-information}

| 実例             | カウント | 物理マシン構成                        | IP                                   | Configuration / コンフィグレーション  |
| :------------- | :--- | :----------------------------- | :----------------------------------- | :-------------------------- |
| TiDB           | 3    | 16 VCore 32GB * 1              | 10.0.1.1<br/> 10.0.1.2<br/> 10.0.1.3 | デフォルトのポート<br/>グローバルディレクトリ構成 |
| PD             | 3    | 4 VCore 8GB * 1                | 10.0.1.4<br/> 10.0.1.5<br/> 10.0.1.6 | デフォルトのポート<br/>グローバルディレクトリ構成 |
| TiKV           | 3    | 16 VCore 32GB 2TB（nvme ssd）* 1 | 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9 | デフォルトのポート<br/>グローバルディレクトリ構成 |
| モニタリングとGrafana | 1    | 4 VCore 8GB * 1 500GB（ssd）     | 10.0.1.10                            | デフォルトのポート<br/>グローバルディレクトリ構成 |

### トポロジテンプレート {#topology-templates}

-   [最小限のトポロジーのための単純なテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-mini.yaml)
-   [最小限のトポロジーのための複雑なテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-mini.yaml)

上記のTiDBクラスタトポロジファイルの構成項目の詳細については、 [TiUPを使用してTiDBを展開するためのトポロジConfiguration / コンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)を参照してください。

> **ノート：**
>
> -   構成ファイルに`tidb`人のユーザーを手動で作成する必要はありません。 TiUPクラスタコンポーネントは、ターゲットマシン上に`tidb`のユーザーを自動的に作成します。ユーザーをカスタマイズすることも、ユーザーを制御マシンとの一貫性を保つこともできます。
> -   展開ディレクトリを相対パスとして構成すると、クラスタはユーザーのホームディレクトリに展開されます。
