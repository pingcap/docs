---
title: Minimal Deployment Topology
summary: TiDB クラスターの最小限のデプロイメント トポロジについて学習します。
---

# 最小限の展開トポロジ {#minimal-deployment-topology}

このドキュメントでは、TiDB クラスターの最小限の展開トポロジについて説明します。

## トポロジ情報 {#topology-information}

| 実例             | カウント | 物理マシン構成                                      | IP                                   | コンフィグレーション                 |
| :------------- | :--- | :------------------------------------------- | :----------------------------------- | :------------------------- |
| TiDB           | 2    | 16 仮想コア 32 GiB<br/>storage用に100 GiB          | 10.0.1.1<br/> 10.0.1.2               | デフォルトポート<br/>グローバルディレクトリ構成 |
| PD             | 3    | 4 VCore 8 GiB<br/>storage用に100 GiB           | 10.0.1.4<br/> 10.0.1.5<br/> 10.0.1.6 | デフォルトポート<br/>グローバルディレクトリ構成 |
| TiKV           | 3    | 16 仮想コア 32 GiB<br/>storage用 2 TiB (NVMe SSD) | 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9 | デフォルトポート<br/>グローバルディレクトリ構成 |
| モニタリングとGrafana | 1    | 4 VCore 8 GiB<br/>storage用500 GiB（SSD）       | 10.0.1.10                            | デフォルトポート<br/>グローバルディレクトリ構成 |

> **注記：**
>
> インスタンスのIPアドレスは例としてのみ示されています。実際の導入では、IPアドレスを実際のIPアドレスに置き換えてください。

### トポロジテンプレート {#topology-templates}

-   [最小トポロジーのシンプルなテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-mini.yaml)
-   [最小位相の複雑なテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-mini.yaml)

上記の TiDB クラスター トポロジ ファイルの構成項目の詳細については、 [TiUPを使用して TiDB をデプロイするためのトポロジコンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)参照してください。

> **注記：**
>
> -   設定ファイルに`tidb`ユーザーを手動で作成する必要はありません。TiUPTiUPコンポーネントは、ターゲットマシンに`tidb`ユーザーを自動的に作成します。ユーザーをカスタマイズすることも、制御マシンと同じユーザーを維持することもできます。
> -   デプロイメント ディレクトリを相対パスとして構成すると、クラスターはユーザーのホーム ディレクトリにデプロイされます。
