---
title: TiSpark Deployment Topology
summary: Learn the deployment topology of TiSpark using TiUP based on the minimal TiDB topology.
---

# TiSpark 導入トポロジー {#tispark-deployment-topology}

> **警告：**
>
> TiUPクラスターでの TiSpark サポートは非​​推奨になりました。使用はお勧めし**ません**。

このドキュメントでは、TiSpark 導入トポロジと、最小クラスター トポロジに基づいて TiSpark を導入する方法を紹介します。

TiSpark は、TiDB/TiKV 上で Apache Spark を実行し、複雑な OLAP クエリに答えるために構築されたコンポーネントです。これにより、Spark プラットフォームと分散 TiKV クラスターの両方の利点が TiDB に導入され、TiDB はオンライン トランザクションと分析の両方に対するワンストップ ソリューションになります。

TiSparkアーキテクチャとその使用方法の詳細については、 [TiSpark ユーザーガイド](/tispark-overview.md)を参照してください。

## トポロジ情報 {#topology-information}

| 実例           | カウント | 物理マシンの構成                         | IP                                                           | コンフィグレーション                  |
| :----------- | :--- | :------------------------------- | :----------------------------------------------------------- | :-------------------------- |
| TiDB         | 3    | 16Vコア 32GB*1                     | 10.0.1.1<br/> 10.0.1.2<br/> 10.0.1.3                         | デフォルトのポート<br/>グローバルディレクトリ構成 |
| PD           | 3    | 4Vコア8GB*1                        | 10.0.1.4<br/> 10.0.1.5<br/> 10.0.1.6                         | デフォルトのポート<br/>グローバルディレクトリ構成 |
| TiKV         | 3    | 16 VCore 32GB 2TB (nvme ssd) * 1 | 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9                         | デフォルトのポート<br/>グローバルディレクトリ構成 |
| ティスパーク       | 3    | 8Vコア16GB*1                       | 10.0.1.21 (マスター)<br/> 10.0.1.22 (ワーカー)<br/> 10.0.1.23 (ワーカー) | デフォルトのポート<br/>グローバルディレクトリ構成 |
| モニタリングとグラファナ | 1    | 4 VCore 8GB * 1 500GB (SSD)      | 10.0.1.11                                                    | デフォルトのポート<br/>グローバルディレクトリ構成 |

## トポロジテンプレート {#topology-templates}

-   [シンプルな TiSpark トポロジ テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-tispark.yaml)
-   [複雑な TiSpark トポロジ テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-tispark.yaml)

上記の TiDB クラスター トポロジー ファイルの構成項目の詳細な説明については、 [TiUPを使用して TiDB を展開するためのトポロジコンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)を参照してください。

> **注記：**
>
> -   構成ファイルに`tidb`ユーザーを手動で作成する必要はありません。 TiUPクラスターコンポーネントは、ターゲット マシン上に`tidb`のユーザーを自動的に作成します。ユーザーをカスタマイズしたり、ユーザーと制御マシンの一貫性を保つことができます。
> -   デプロイメント ディレクトリを相対パスとして構成すると、クラスターはユーザーのホーム ディレクトリにデプロイされます。

## 前提条件 {#prerequisites}

TiSpark は Apache Spark クラスターに基づいているため、TiSpark を含む TiDB クラスターを開始する前に、TiSpark をデプロイするサーバーにJavaランタイム環境 (JRE) 8 がインストールされていることを確認する必要があります。そうしないと、TiSpark を起動できません。

TiUP は、 JRE の自動インストールをサポートしていません。自分でインストールする必要があります。詳しいインストール手順については、 [事前に構築された OpenJDK パッケージをダウンロードしてインストールする方法](https://openjdk.java.net/install/)を参照してください。

JRE 8 が展開サーバーにすでにインストールされているが、システムのデフォルトのパッケージ管理ツールのパスにない場合は、トポロジ構成で`java_home`パラメータを設定することで、使用する JRE 環境のパスを指定できます。このパラメータは`JAVA_HOME`システム環境変数に対応します。
