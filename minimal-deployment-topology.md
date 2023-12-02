---
title: Minimal Deployment Topology
summary: Learn the minimal deployment topology of TiDB clusters.
---

# 最小限の導入トポロジ {#minimal-deployment-topology}

このドキュメントでは、TiDB クラスターの最小限の展開トポロジについて説明します。

## トポロジ情報 {#topology-information}

| 実例           | カウント | 物理マシンの構成                                      | IP                                   | コンフィグレーション                  |
| :----------- | :--- | :-------------------------------------------- | :----------------------------------- | :-------------------------- |
| TiDB         | 2    | 16 仮想コア 32 GiB<br/>storage用に 100 GiB          | 10.0.1.1<br/> 10.0.1.2               | デフォルトのポート<br/>グローバルディレクトリ構成 |
| PD           | 3    | 4 Vコア 8 GiB<br/>storage用に 100 GiB             | 10.0.1.4<br/> 10.0.1.5<br/> 10.0.1.6 | デフォルトのポート<br/>グローバルディレクトリ構成 |
| TiKV         | 3    | 16 仮想コア 32 GiB<br/>storage用に 2 TiB (NVMe SSD) | 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9 | デフォルトのポート<br/>グローバルディレクトリ構成 |
| モニタリングとグラファナ | 1    | 4 Vコア 8 GiB<br/>storage用に 500 GiB (SSD)       | 10.0.1.10                            | デフォルトのポート<br/>グローバルディレクトリ構成 |

### トポロジテンプレート {#topology-templates}

-   [最小限のトポロジのシンプルなテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-mini.yaml)
-   [最小トポロジの複雑なテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-mini.yaml)

上記の TiDB クラスター トポロジー ファイルの構成項目の詳細な説明については、 [TiUPを使用して TiDB を展開するためのトポロジコンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)を参照してください。

> **注記：**
>
> -   構成ファイルに`tidb`ユーザーを手動で作成する必要はありません。 TiUPクラスターコンポーネントは、ターゲット マシン上に`tidb`のユーザーを自動的に作成します。ユーザーをカスタマイズしたり、ユーザーと制御マシンの一貫性を保つことができます。
> -   デプロイメント ディレクトリを相対パスとして構成すると、クラスターはユーザーのホーム ディレクトリにデプロイされます。
