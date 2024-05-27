---
title: Minimal Deployment Topology
summary: TiDB クラスターの最小限のデプロイメント トポロジについて学習します。
---

# 最小限の展開トポロジ {#minimal-deployment-topology}

このドキュメントでは、TiDB クラスターの最小限のデプロイメント トポロジについて説明します。

## トポロジ情報 {#topology-information}

| 実例             | カウント | 物理マシン構成                                       | IP                                   | コンフィグレーション                 |
| :------------- | :--- | :-------------------------------------------- | :----------------------------------- | :------------------------- |
| ティビ            | 2    | 16 VCore 32 GiB<br/>storage用 100 GiB          | 10.0.1.1<br/> 10.0.1.2               | デフォルトポート<br/>グローバルディレクトリ構成 |
| PD             | 3    | 4 VCore 8 GiB<br/>storage用 100 GiB            | 10.0.1.4<br/> 10.0.1.5<br/> 10.0.1.6 | デフォルトポート<br/>グローバルディレクトリ構成 |
| ティクヴ           | 3    | 16 VCore 32 GiB<br/>storage用 2 TiB (NVMe SSD) | 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9 | デフォルトポート<br/>グローバルディレクトリ構成 |
| モニタリングとGrafana | 1    | 4 VCore 8 GiB<br/>storage用 500 GiB (SSD)      | 10.0.1.10                            | デフォルトポート<br/>グローバルディレクトリ構成 |

### トポロジーテンプレート {#topology-templates}

-   [最小トポロジーのシンプルなテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-mini.yaml)
-   [最小トポロジーの複雑なテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-mini.yaml)

上記の TiDB クラスタ トポロジ ファイルの構成項目の詳細については、 [TiUPを使用して TiDB をデプロイするためのトポロジコンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)を参照してください。

> **注記：**
>
> -   構成ファイルで`tidb`ユーザーを手動で作成する必要はありません。TiUP クラスターコンポーネントは、ターゲット マシンに`tidb`ユーザーを自動的に作成します。ユーザーをカスタマイズすることも、ユーザーをコントロール マシンと一致させることもできます。
> -   デプロイメント ディレクトリを相対パスとして構成すると、クラスターはユーザーのホーム ディレクトリにデプロイされます。
