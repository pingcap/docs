---
title: TiSpark Deployment Topology
summary: Learn the deployment topology of TiSpark using TiUP based on the minimal TiDB topology.
---

# TiSpark 導入トポロジ {#tispark-deployment-topology}

> **警告：**
>
> TiUPクラスターでの TiSpark のサポートは廃止されました。使用することは**お**勧めしません。

このドキュメントでは、TiSpark の展開トポロジと、最小クラスター トポロジに基づいて TiSpark を展開する方法について説明します。

TiSpark は、TiDB/TiKV 上で Apache Spark を実行して複雑な OLAP クエリに応答するために構築されたコンポーネントです。これにより、Spark プラットフォームと分散型 TiKV クラスターの両方の利点が TiDB にもたらされ、TiDB はオンライン トランザクションと分析の両方のワンストップ ソリューションになります。

TiSparkアーキテクチャとその使用方法の詳細については、 [TiSpark ユーザーガイド](/tispark-overview.md)を参照してください。

## トポロジ情報 {#topology-information}

| 実例         | カウント | 物理マシン構成                         | 知財                                                           | コンフィグレーション                    |
| :--------- | :--- | :------------------------------ | :----------------------------------------------------------- | :---------------------------- |
| TiDB       | 3    | 16 仮想コア 32GB * 1                | 10.0.1.1<br/> 10.0.1.2<br/> 10.0.1.3                         | デフォルトのポート<br/>グローバル ディレクトリの構成 |
| PD         | 3    | 4 Vコア 8GB * 1                   | 10.0.1.4<br/> 10.0.1.5<br/> 10.0.1.6                         | デフォルトのポート<br/>グローバル ディレクトリの構成 |
| TiKV       | 3    | 16 仮想コア 32GB 2TB (nvme ssd) * 1 | 10.0.1.7<br/> 10.0.1.8<br/> 10.0.1.9                         | デフォルトのポート<br/>グローバル ディレクトリの構成 |
| ティスパーク     | 3    | 8 Vコア 16GB * 1                  | 10.0.1.21 (マスター)<br/> 10.0.1.22 (ワーカー)<br/> 10.0.1.23 (ワーカー) | デフォルトのポート<br/>グローバル ディレクトリの構成 |
| 監視とGrafana | 1    | 4 仮想コア 8GB * 1 500GB (ssd)      | 10.0.1.11                                                    | デフォルトのポート<br/>グローバル ディレクトリの構成 |

## トポロジ テンプレート {#topology-templates}

-   [シンプルな TiSpark トポロジ テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-tispark.yaml)
-   [複雑な TiSpark トポロジ テンプレート](https://github.com/pingcap/docs/blob/master/config-templates/complex-tispark.yaml)

上記の TiDB クラスター トポロジ ファイルの構成項目の詳細な説明については、 [TiUPを使用して TiDB をデプロイするためのトポロジコンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)を参照してください。

> **ノート：**
>
> -   構成ファイルで`tidb`ユーザーを手動で作成する必要はありません。 TiUPクラスターコンポーネントは、ターゲット マシンに`tidb`ユーザーを自動的に作成します。ユーザーをカスタマイズしたり、ユーザーと制御マシンとの一貫性を保つことができます。
> -   展開ディレクトリを相対パスとして構成すると、クラスターはユーザーのホーム ディレクトリに展開されます。

## 前提条件 {#prerequisites}

TiSpark は Apache Spark クラスターに基づいているため、TiSpark を含む TiDB クラスターを開始する前に、TiSpark をデプロイするサーバーにJavaランタイム環境 (JRE) 8 がインストールされていることを確認する必要があります。そうしないと、TiSpark を開始できません。

TiUP はJRE の自動インストールをサポートしていません。自分でインストールする必要があります。詳細なインストール手順については、 [ビルド済みの OpenJDK パッケージをダウンロードしてインストールする方法](https://openjdk.java.net/install/)を参照してください。

JRE 8 がデプロイメント・サーバーに既にインストールされているが、システムのデフォルトのパッケージ管理ツールのパスにない場合、トポロジー構成で`java_home`パラメーターを設定することにより、使用する JRE 環境のパスを指定できます。このパラメーターは、 `JAVA_HOME`システム環境変数に対応します。
