---
title: TiDB Cloud Quick Start
summary: Sign up quickly to try TiDB Cloud and create your TiDB cluster.
category: quick start
---

# TiDB Cloudクイック スタート {#tidb-cloud-quick-start}

*推定完了時間: 20 分*

このチュートリアルでは、 TiDB Cloudを使い始める簡単な方法について説明します。 TiDB Cloudコンソールの[**入門**](https://tidbcloud.com/console/getting-started)ページに移動して、チュートリアルを順を追って実行することもできます。

## ステップ 1. TiDB クラスターを作成する {#step-1-create-a-tidb-cluster}

TiDB Cloud [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) (ベータ) は、 TiDB Cloudを使い始めるための最良の方法です。Serverless Tierクラスターを作成するには、次の手順を実行します。

1.  TiDB Cloudアカウントを持っていない場合は、 [ここ](https://tidbcloud.com/free-trial)クリックしてアカウントにサインアップします。

    TiDB Cloud を使用してパスワードを管理できるように電子メールとパスワードでサインアップするか、 TiDB Cloudへのシングル サインオン (SSO) 用に Google、GitHub、または Microsoft アカウントを選択できます。

2.  [ログイン](https://tidbcloud.com/)をTiDB Cloudアカウントに追加します。

    デフォルトでは[**クラスター**](https://tidbcloud.com/console/clusters)ページが表示されます。

3.  新しいサインアップ ユーザーの場合、 TiDB Cloud はデフォルトのServerless Tierクラスター`Cluster0`を自動的に作成します。

    -   このデフォルトのクラスターでTiDB Cloud の機能をすぐに試すには、 [ステップ 2. AI を活用した Chat2Query (ベータ版) を試す](#step-2-try-ai-powered-chat2query-beta)に進みます。
    -   自分で新しいServerless Tierクラスターを作成するには、次の操作を行います。

        1.  **[クラスタの作成]**をクリックします。
        2.  **[クラスタの作成]**ページでは、<strong>サーバーレスが</strong>デフォルトで選択されています。クラスターのターゲット リージョンを選択し、必要に応じて既定のクラスター名を更新して、 <strong>[作成]</strong>をクリックします。 Serverless Tierクラスタは約 30 秒で作成されます。

## ステップ 2. AI を活用した Chat2Query (ベータ版) を試す {#step-2-try-ai-powered-chat2query-beta}

TiDB Cloud はAI によって強化されています。 TiDB Cloudコンソールで AI を利用した SQL エディターである Chat2Query (ベータ版) を使用して、データの価値を最大化できます。

Chat2Query では、単に`--`を入力してから命令を入力し、AI に SQL クエリを自動的に生成させるか、SQL クエリを手動で記述してから、ターミナルを使用せずにデータベースに対して SQL クエリを実行することができます。

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページでクラスター名をクリックしてその概要ページに移動し、左側のナビゲーション ペインで**[Chat2Query]**をクリックします。

2.  TiDB Cloud AI 容量を試すには、画面上の指示に従って、PingCAP と OpenAI がコード スニペットを使用してサービスを調査および改善できるようにし、 **[保存して開始]**をクリックします。

3.  エディターでは、単に`--`入力してから命令を入力し、AI に SQL クエリを自動的に生成させるか、SQL クエリを手動で作成することができます。

    > **ノート：**
    >
    > AI によって生成された SQL クエリは 100% 正確ではなく、さらに調整が必要になる場合があります。

4.  SQL クエリを実行します。

    <SimpleTab>
     <div label="macOS">

    macOS の場合:

    -   エディターにクエリが 1 つしかない場合、それを実行するには、 **⌘ + Enter**を押すか、 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg><strong>実行します</strong>。

    -   エディターに複数のクエリがある場合、そのうちの 1 つまたは複数を順番に実行するには、カーソルでターゲット クエリの行を選択し、 **⌘ + Enter**を押すか、 <strong>[実行]</strong>をクリックします。

    -   エディターですべてのクエリを順番に実行するには、 **⇧ + ⌘ + Enter を**押すか、カーソルですべてのクエリの行を選択して<strong>[実行]</strong>をクリックします。

    </div>

    <div label="Windows/Linux">

    Windows または Linux の場合:

    -   エディターにクエリが 1 つしかない場合、それを実行するには、 **Ctrl + Enter を**押すか、 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg><strong>実行します</strong>。

    -   エディターに複数のクエリがある場合、それらの 1 つまたは複数を順番に実行するには、カーソルでターゲット クエリの行を選択し、 **Ctrl + Enter**を押すか、 [<strong>実行]</strong>をクリックします。

    -   エディターですべてのクエリを順番に実行するには、 **Shift + Ctrl + Enter を**押すか、カーソルですべてのクエリの行を選択して<strong>[実行]</strong>をクリックします。

    </div>
     </SimpleTab>

クエリを実行すると、ページの下部にクエリ ログと結果がすぐに表示されます。

## ステップ 3. Playground を試す {#step-3-try-playground}

TiDB Cloudクラスターが作成されたら、 TiDB Cloud Playground に事前にロードされたサンプル データを使用して、TiDB の実験をすぐに開始することもできます。

[**クラスター**](https://tidbcloud.com/console/clusters)ページで、新しく作成したクラスターの名前をクリックしてその概要ページに移動し、左側のナビゲーション ペインで**[Playground]**をクリックします。

## 手順 4. サンプル データを読み込む {#step-4-load-sample-data}

**Plaground**を試した後、サンプル データをTiDB Cloudクラスターにロードできます。データを簡単にインポートしてサンプル クエリを実行できるように、Capital Bikeshare のサンプル データを提供しています。

1.  クラスターの概要ページで、左側のナビゲーション ペインにある**[インポート]**をクリックします。

2.  **[インポート]**ページで、右上隅にある<strong>[データのインポート]</strong>をクリックし、 <strong>[S3 から]</strong>を選択します。

3.  インポート パラメータを入力します。

    -   **データ形式**： <strong>SQLファイル</strong>を選択
    -   **バケット URI** : `s3://tidbcloud-sample-data/data-ingestion/`
    -   **ロールARN** ： `arn:aws:iam::801626783489:role/import-sample-access`

    バケットのリージョンがクラスターと異なる場合は、クロス リージョンのコンプライアンスを確認します。 **[次へ]**をクリックします。

4.  必要に応じてテーブル フィルター ルールを追加します。サンプル データの場合は、この手順を省略できます。 **[次へ]**をクリックします。

5.  **[プレビュー]**ページでインポートするデータを確認し、 <strong>[インポートの開始]</strong>をクリックします。

データのインポート プロセスには数分かかります。データ インポートの進行状況が**Finished**と表示されたら、サンプル データとデータベース スキーマがTiDB Cloudのデータベースに正常にインポートされました。

## 次は何ですか {#what-s-next}

-   さまざまな方法でクラスターに接続する方法については、 [TiDB クラスターに接続する](/tidb-cloud/connect-to-tidb-cluster.md)を参照してください。
-   Chat2Query を使用してデータを探索する方法の詳細については、 [Chat2Query](/tidb-cloud/explore-data-with-chat2query.md)を参照してください。
-   TiDB SQLの使用法については、 [TiDB で SQL を調べる](/basic-sql-operations.md)を参照してください。
-   クロスゾーンの高可用性、水平スケーリング、および[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)利点を備えた本番環境での本番については、 [TiDB クラスターを作成する](/tidb-cloud/create-tidb-cluster.md)を参照してDedicated Tierクラスターを作成してください。
