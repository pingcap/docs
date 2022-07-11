---
title: TiSpark Deployment Topology
summary: Learn the deployment topology of TiSpark using TiUP based on the minimal TiDB topology.
---

# TiSpark展開トポロジ {#tispark-deployment-topology}

> **警告：**
>
> TiUPクラスタでのTiSparkのサポートは、まだ実験的機能です。実稼働環境での使用はお勧めし**ません**。

このドキュメントでは、TiSparkの展開トポロジと、最小クラスタトポロジに基づいてTiSparkを展開する方法を紹介します。

TiSparkは、TiDB /TiKV上でApacheSparkを実行して、複雑なOLAPクエリに応答するために構築されたコンポーネントです。 Sparkプラットフォームと分散TiKVクラスタの両方のメリットをTiDBにもたらし、TiDBをオンライントランザクションと分析の両方のワンストップソリューションにします。

TiSparkアーキテクチャとその使用方法の詳細については、 [TiSparkユーザーガイド](/tispark-overview.md)を参照してください。

## トポロジー情報 {#topology-information}

| 実例             | カウント | 物理マシン構成                        | IP                                                      | Configuration / コンフィグレーション |
| :------------- | :--- | :----------------------------- | :------------------------------------------------------ | :------------------------- |
| TiDB           | 3    | 16 VCore 32GB * 1              | 10.0.1.1<br/> 10.0.1.2<br/> 10.0.1.3                    | デフォルトポート<br/>グローバルディレクトリ構成 |
| PD             | 3    | 4 VCore 8GB * 1                | 10.0.1.4<br/> 10.0.1.5<br/> 10.0.1.6                    | デフォルトポート<br/>グローバルディレクトリ構成 |
| TiKV           | 3    | 16 VCore 32GB 2TB（nvme ssd）* 1 | 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9                    | デフォルトポート<br/>グローバルディレクトリ構成 |
| TiSpark        | 3    | 8 VCore 16GB * 1               | 10.0.1.21（マスター）<br/> 10.0.1.22（労働者）<br/> 10.0.1.23（労働者） | デフォルトポート<br/>グローバルディレクトリ構成 |
| モニタリングとGrafana | 1    | 4 VCore 8GB * 1 500GB（ssd）     | 10.0.1.11                                               | デフォルトポート<br/>グローバルディレクトリ構成 |

## トポロジテンプレート {#topology-templates}

-   [シンプルなTiSparkトポロジテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-tispark.yaml)
-   [複雑なTiSparkトポロジテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-tispark.yaml)

上記のTiDBクラスタトポロジファイルの構成項目の詳細については、 [TiUPを使用してTiDBを展開するためのトポロジConfiguration / コンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)を参照してください。

> **ノート：**
>
> -   構成ファイルに`tidb`人のユーザーを手動で作成する必要はありません。 TiUPクラスタコンポーネントは、ターゲットマシン上に`tidb`のユーザーを自動的に作成します。ユーザーをカスタマイズすることも、ユーザーを制御マシンと一貫性のある状態に保つこともできます。
> -   展開ディレクトリを相対パスとして構成すると、クラスタはユーザーのホームディレクトリに展開されます。

## 前提条件 {#prerequisites}

TiSparkはApacheSparkクラスタに基づいているため、TiSparkを含むTiDBクラスタを起動する前に、TiSparkをデプロイするサーバーにJavaランタイム環境（JRE）8がインストールされていることを確認する必要があります。そうしないと、TiSparkを開始できません。

TiUPは、JREの自動インストールをサポートしていません。自分でインストールする必要があります。インストール手順の詳細については、 [ビルド済みのOpenJDKパッケージをダウンロードしてインストールする方法](https://openjdk.java.net/install/)を参照してください。

JRE 8がすでにデプロイメント・サーバーにインストールされているが、システムのデフォルトのパッケージ管理ツールのパスにない場合は、トポロジー構成で`java_home`パラメーターを設定することにより、使用するJRE環境のパスを指定できます。このパラメーターは、 `JAVA_HOME`のシステム環境変数に対応します。
