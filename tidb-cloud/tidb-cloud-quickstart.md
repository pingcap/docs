---
title: TiDB Cloud Quick Start
summary: Sign up quickly to try TiDB Cloud and create your TiDB cluster.
category: quick start
---

# TiDB Cloudクイック スタート {#tidb-cloud-quick-start}

*推定完了時間: 20 分*

このチュートリアルでは、 TiDB Cloudを使い始める簡単な方法を説明します。 TiDB Cloudコンソールの[<a href="https://tidbcloud.com/console/getting-started">**入門**</a>](https://tidbcloud.com/console/getting-started)ページに移動して、チュートリアルをステップバイステップで実行することもできます。

さらに、[TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&utm_medium=tidb_quick_start)で TiDB の機能を試すことができます。

## ステップ 1. TiDB クラスターを作成する {#step-1-create-a-tidb-cluster}

[<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">TiDB Serverless</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta) (ベータ) は、 TiDB Cloudを開始するための最良の方法です。 TiDB Serverless クラスタを作成するには、次の手順を実行します。

1.  TiDB Cloudアカウントをお持ちでない場合は、 [<a href="https://tidbcloud.com/free-trial">ここ</a>](https://tidbcloud.com/free-trial)をクリックしてアカウントにサインアップしてください。

    TiDB Cloud を使用してパスワードを管理できるように電子メールとパスワードでサインアップすることも、 TiDB Cloudへのシングル サインオン (SSO) 用に Google、GitHub、または Microsoft アカウントを選択することもできます。

2.  TiDB Cloudアカウントに[<a href="https://tidbcloud.com/">ログイン</a>](https://tidbcloud.com/) 。

    デフォルトでは[<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページが表示されます。

3.  新規サインアップ ユーザーの場合、 TiDB Cloud はデフォルトの TiDB Serverless クラスタ`Cluster0`を自動的に作成します。

    -   このデフォルトのクラスターを使用してTiDB Cloud機能をすぐに試すには、 [<a href="#step-2-try-ai-powered-chat2query-beta">ステップ 2. AI を活用した Chat2Query (ベータ版) を試す</a>](#step-2-try-ai-powered-chat2query-beta)に進みます。
    -   新しい TiDB Serverless クラスタを独自に作成してみるには、次の操作を実行します。

        1.  **「クラスタの作成」**をクリックします。
        2.  **「クラスタの作成」**ページでは、デフォルトで**サーバーレス**が選択されています。クラスターのターゲット リージョンを選択し、必要に応じてデフォルトのクラスター名を更新して、 **[作成]**をクリックします。 TiDB Serverless クラスタは約 30 秒で作成されます。

## ステップ 2. AI を活用した Chat2Query (ベータ版) を試す {#step-2-try-ai-powered-chat2query-beta}

TiDB CloudはAI を活用しています。 TiDB Cloudコンソールの AI を活用した SQL エディターである Chat2Query (ベータ版) を使用して、データの価値を最大化できます。

Chat2Query では、 `--`入力してから AI に SQL クエリを自動的に生成させる指示を入力するか、SQL クエリを手動で作成して、ターミナルを使用せずにデータベースに対して SQL クエリを実行することができます。

1.  [<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページで、クラスター名をクリックしてその概要ページに移動し、左側のナビゲーション ペインで**[Chat2Query]**をクリックします。

2.  TiDB Cloud AI の容量を試すには、画面上の指示に従って、PingCAP と OpenAI がコード スニペットを使用してサービスを調査および改善できるようにし、 **[保存して開始する]**をクリックします。

3.  エディターでは、 `--`を入力してから AI に SQL クエリを自動的に生成させる指示を入力するか、SQL クエリを手動で作成することができます。

    > **ノート：**
    >
    > AI によって生成された SQL クエリは 100% 正確ではないため、さらに調整が必要な場合があります。

4.  SQL クエリを実行します。

    <SimpleTab>
     <div label="macOS">

    macOS の場合:

    -   エディターにクエリが 1 つしかない場合、それを実行するには、 **⌘ + Enter キー**を押すか、 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>**実行します**。

    -   エディターに複数のクエリがある場合、1 つまたは複数のクエリを順番に実行するには、カーソルでターゲット クエリの行を選択し、 **⌘ + Enter**を押すか、 **[実行]**をクリックします。

    -   エディターですべてのクエリを順番に実行するには、 **⇧ + ⌘ + Enter を**押すか、カーソルですべてのクエリの行を選択し、 **Run**をクリックします。

    </div>

    <div label="Windows/Linux">

    Windows または Linux の場合:

    -   エディターにクエリが 1 つしかない場合、それを実行するには、 **Ctrl + Enter を**押すか、 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>**実行します**。

    -   エディターに複数のクエリがある場合、1 つまたは複数のクエリを順番に実行するには、カーソルでターゲット クエリの行を選択し、 **Ctrl + Enter**を押すか、 [**実行]**をクリックします。

    -   エディターですべてのクエリを順番に実行するには、 **Shift + Ctrl + Enter を**押すか、カーソルですべてのクエリの行を選択し、 **[実行]**をクリックします。

    </div>
     </SimpleTab>

クエリを実行すると、ページの下部にクエリのログと結果がすぐに表示されます。

## ステップ 3. インタラクティブなチュートリアルを試す {#step-3-try-interactive-tutorials}

TiDB Cloud は、 TiDB Cloud をすぐに使い始めるのに役立つ、作成されたサンプル データセットを含むインタラクティブなチュートリアルを提供します。チュートリアルを試して、 TiDB Cloudを使用して高パフォーマンスのデータ分析を実行する方法を学ぶことができます。

1.  **「？」**をクリックします。コンソールの右下隅にある をクリックし、 **[対話型チュートリアル]**をクリックします。
2.  チュートリアル リストで、開始するチュートリアル カードを選択します。たとえば、 **Steam ゲーム統計**。
3.  チュートリアルに使用する TiDB Serverless クラスタを選択し、 **[データセットのインポート]**をクリックします。インポート プロセスには約 1 分かかる場合があります。
4.  サンプル データがインポートされたら、画面上の指示に従ってチュートリアルを完了します。

## 次は何ですか {#what-s-next}

-   さまざまな方法でクラスターに接続する方法については、 [<a href="/tidb-cloud/connect-to-tidb-cluster.md">TiDB クラスターに接続する</a>](/tidb-cloud/connect-to-tidb-cluster.md)を参照してください。
-   Chat2Query を使用してデータを探索する方法の詳細については、 [<a href="/tidb-cloud/explore-data-with-chat2query.md">チャット2クエリ</a>](/tidb-cloud/explore-data-with-chat2query.md)を参照してください。
-   TiDB SQLの使用法については、 [<a href="/basic-sql-operations.md">TiDB で SQL を探索する</a>](/basic-sql-operations.md)を参照してください。
-   クロスゾーン高可用性、水平スケーリング、および[<a href="https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing">HTAP</a>](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)利点を備えた本番での使用については、TiDB Dedicatedクラスターの作成方法については[<a href="/tidb-cloud/create-tidb-cluster.md">TiDB クラスターを作成する</a>](/tidb-cloud/create-tidb-cluster.md)を参照してください。
