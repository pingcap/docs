---
title: Minimal Deployment Topology
summary: Learn the minimal deployment topology of TiDB clusters.
---

# 最小限の導入トポロジ {#minimal-deployment-topology}

このドキュメントでは、TiDB クラスターの最小限のデプロイ トポロジについて説明します。

## トポロジ情報 {#topology-information}

| 実例         | カウント | 物理マシン構成                                       | 知財                                   | コンフィグレーション                    |
| :--------- | :--- | :-------------------------------------------- | :----------------------------------- | :---------------------------- |
| TiDB       | 2    | 16 仮想コア 32 GiB<br/>storage用に 100 GiB          | 10.0.1.1<br/> 10.0.1.2               | デフォルトのポート<br/>グローバル ディレクトリの構成 |
| PD         | 3    | 4 仮想コア 8 GiB<br/>storage用に 100 GiB            | 10.0.1.4<br/> 10.0.1.5<br/> 10.0.1.6 | デフォルトのポート<br/>グローバル ディレクトリの構成 |
| TiKV       | 3    | 16 仮想コア 32 GiB<br/>storage用に 2 TiB (NVMe SSD) | 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9 | デフォルトのポート<br/>グローバル ディレクトリの構成 |
| 監視とGrafana | 1    | 4 仮想コア 8 GiB<br/>storage用に 500 GiB (SSD)      | 10.0.1.10                            | デフォルトのポート<br/>グローバル ディレクトリの構成 |

### トポロジ テンプレート {#topology-templates}

-   [最小限のトポロジの単純なテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-mini.yaml)
-   [最小限のトポロジの複雑なテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-mini.yaml)

上記の TiDB クラスター トポロジ ファイルの構成項目の詳細な説明については、 [TiUPを使用して TiDB をデプロイするためのトポロジコンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)を参照してください。

> **ノート：**
>
> -   構成ファイルで`tidb`ユーザーを手動で作成する必要はありません。 TiUPクラスターコンポーネントは、ターゲット マシンに`tidb`ユーザーを自動的に作成します。ユーザーをカスタマイズしたり、ユーザーと制御マシンとの一貫性を保つことができます。
> -   展開ディレクトリを相対パスとして構成すると、クラスターはユーザーのホーム ディレクトリに展開されます。
