---
title: TiDB Cloud Quick Start
summary: すぐにサインアップしてTiDB Cloudを試し、TiDB クラスターを作成してください。
category: quick start
---

# TiDB Cloudクイックスタート {#tidb-cloud-quick-start}

*推定所要時間: 20 分*

このチュートリアルでは、 TiDB Cloudを使い始めるための簡単な方法を説明します。

さらに、 [TiDB プレイグラウンド](https://play.tidbcloud.com/?utm_source=docs&#x26;utm_medium=tidb_cloud_quick_start)で TiDB 機能を試すこともできます。

## ステップ1: TiDBクラスターを作成する {#step-1-create-a-tidb-cluster}

[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) TiDB Cloudを使い始めるのに最適な方法です。TiDB TiDB Cloud Serverlessクラスターを作成するには、以下の手順に従ってください。

1.  TiDB Cloudアカウントをお持ちでない場合は、 [ここ](https://tidbcloud.com/free-trial)クリックしてサインアップしてください。

    メールアドレスとパスワードでサインアップして、 TiDB Cloudを使用してパスワードを管理するか、Google、GitHub、または Microsoft アカウントでサインインして、 TiDB Cloudへのシングル サインオン (SSO) を選択することもできます。

2.  [ログイン](https://tidbcloud.com/) TiDB Cloudアカウントに追加します。

    デフォルトでは[**クラスター**](https://tidbcloud.com/project/clusters)ページ目が表示されます。

3.  新規サインアップ ユーザーの場合、 TiDB Cloud は`Cluster0`名前のデフォルトのTiDB Cloud Serverless クラスターを自動的に作成します。

    -   このデフォルトのクラスターでTiDB Cloud機能をすぐに試すには、 [ステップ2: AI支援SQLエディターを試す](#step-2-try-ai-assisted-sql-editor)に進みます。
    -   独自に新しいTiDB Cloud Serverless クラスターを作成するには、次の手順に従います。

        1.  **[クラスタの作成]を**クリックします。
        2.  **「クラスタの作成」**ページでは、デフォルトで**「Serverless」**が選択されています。クラスターのターゲットリージョンを選択し、必要に応じてデフォルトのクラスター名を更新し、 [クラスタープラン](/tidb-cloud/select-cluster-tier.md#cluster-plans)を選択して**「作成**」をクリックします。TiDB TiDB Cloud Serverless クラスターは約30秒で作成されます。

## ステップ2: AI支援SQLエディターを試す {#step-2-try-ai-assisted-sql-editor}

TiDB Cloudコンソールに搭載されたAI支援SQLエディタを使用することで、データの価値を最大限に引き出すことができます。これにより、ローカルSQLクライアントを必要とせずに、データベースに対してSQLクエリを実行できます。クエリ結果は表やグラフで直感的に表示され、クエリログも簡単に確認できます。

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページで、クラスター名をクリックして概要ページに移動し、左側のナビゲーション ペインで**[SQL エディター] を**クリックします。

2.  TiDB Cloudの AI 機能を試すには、画面上の指示に従って、PingCAP と AWS Bedrock がコードスニペットを研究とサービスの改善のために使用することを許可し、 **[保存して開始] を**クリックします。

3.  SQL エディターで、macOS の場合は<kbd>⌘</kbd> + <kbd>I</kbd> (Windows または Linux の場合は<kbd>Control</kbd> + <kbd>I</kbd> ) を押して、 [Chat2Query（ベータ版）](/tidb-cloud/tidb-cloud-glossary.md#chat2query) SQL クエリを自動的に生成するように指示します。

    たとえば、2 つの列 (列`id`と列`name` ) を持つ新しいテーブル`test.t`を作成するには、 `use test;`と入力してデータベースを指定し、 <kbd>⌘</kbd> + <kbd>I</kbd>を押して、指示として`create a new table t with id and name`入力し、 **Enter**を押すと、AI がそれに応じて SQL ステートメントを生成できます。

    生成されたステートメントについては、 **「承認」**をクリックして承認し、必要に応じてさらに編集するか、 **「破棄」を**クリックして拒否することができます。

    > **注記：**
    >
    > AI によって生成された SQL クエリは 100% 正確ではないため、さらに調整が必要になる場合があります。

4.  SQL クエリを実行します。

    <SimpleTab>
     <div label="macOS">

    macOSの場合:

    -   エディタにクエリが1つしかない場合は、 **⌘ + Enter**を押すか、 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>実行するには**実行してください**。

    -   エディターに複数のクエリがある場合は、カーソルで対象クエリの行を選択し、 **⌘ + Enter キー**を押すか、 **[実行]**をクリックして順番に実行します。

    -   エディター内のすべてのクエリを順番に実行するには、 **⇧ + ⌘ + Enter を**押すか、カーソルですべてのクエリの行を選択して**「実行」**をクリックします。

    </div>

    <div label="Windows/Linux">

    Windows または Linux の場合:

    -   エディタにクエリが1つしかない場合は、 **Ctrl + Enter**を押すか、 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>実行するには**実行してください**。

    -   エディターに複数のクエリがある場合は、カーソルで対象クエリの行を選択し、 **Ctrl + Enter キー**を押すか、 **[実行]**をクリックして順番に実行します。

    -   エディター内のすべてのクエリを順番に実行するには、 **Shift + Ctrl + Enter**を押すか、カーソルですべてのクエリの行を選択して**[実行]**をクリックします。

    </div>
     </SimpleTab>

クエリを実行すると、ページの下部にクエリのログと結果がすぐに表示されます。

AI にさらに多くの SQL ステートメントを生成させるには、次の例に示すように、さらに命令を入力します。

```sql
use test;

-- create a new table t with id and name 
CREATE TABLE
  `t` (`id` INT, `name` VARCHAR(255));

-- add 3 rows 
INSERT INTO
  `t` (`id`, `name`)
VALUES
  (1, 'row1'),
  (2, 'row2'),
  (3, 'row3');

-- query all
SELECT
  `id`,
  `name`
FROM
  `t`;
```

## ステップ3: インタラクティブなチュートリアルを試す {#step-3-try-interactive-tutorials}

TiDB Cloud は、 TiDB Cloudをすぐに使い始めることができるよう、丁寧に作成されたサンプルデータセットを使用したインタラクティブなチュートリアルを提供しています。これらのチュートリアルを試して、 TiDB Cloud を高性能なデータ分析に使用する方法を習得してください。

1.  コンソールの右下にある**[?]**アイコンをクリックし、 **[インタラクティブ チュートリアル]**を選択します。
2.  チュートリアル リストで、 **Steam ゲーム統計**などの開始するチュートリアル カードを選択します。
3.  チュートリアルで使用するTiDB Cloud Serverlessクラスターを選択し、 **「Import Dataset」**をクリックします。インポート処理には約1分かかる場合があります。
4.  サンプル データをインポートしたら、画面の指示に従ってチュートリアルを完了します。

## 次は何？ {#what-s-next}

-   さまざまな方法を使用してクラスターに接続する方法については、 [TiDB Cloud Serverless クラスターに接続する](/tidb-cloud/connect-to-tidb-cluster-serverless.md)参照してください。
-   SQL エディターと Chat2Query を使用してデータを探索する方法の詳細については、 [AI支援SQLエディターでデータを探索](/tidb-cloud/explore-data-with-chat2query.md)参照してください。
-   TiDB SQL の使用法については、 [TiDB で SQL を探索する](/basic-sql-operations.md)参照してください。
-   ゾーン間の高可用性、水平スケーリング、および[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)利点を備えた本番で使用する場合は、 [TiDB Cloud専用クラスタを作成する](/tidb-cloud/create-tidb-cluster.md)参照してください。
