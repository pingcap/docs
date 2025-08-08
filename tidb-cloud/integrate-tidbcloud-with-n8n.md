---
title: Integrate TiDB Cloud with n8n
summary: n8n でのTiDB Cloudノードの使用方法を学習します。
---

# TiDB Cloudとn8nを統合する {#integrate-tidb-cloud-with-n8n}

[n8n](https://n8n.io/)は拡張可能なワークフロー自動化ツールです。2 [フェアコード](https://faircode.io/)配布モデルにより、n8nは常にソースコードを公開し、セルフホストが可能になり、カスタム関数、ロジック、アプリを追加できるようになります。

このドキュメントでは、 TiDB Cloud Serverless クラスターを作成し、Hacker News RSS を収集して TiDB に保存し、ブリーフィング メールを送信するという自動ワークフローの構築方法を紹介します。

## 前提条件: TiDB Cloud APIキーを取得する {#prerequisites-get-tidb-cloud-api-key}

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、左上隅のコンボ ボックスを使用して対象の組織に切り替えます。
2.  左側のナビゲーション ペインで、 **[組織設定]** &gt; **[API キー]**をクリックします。
3.  **「API キー」**ページで、 **「API キーの作成」を**クリックします。
4.  API キーの説明を入力し、 **「次へ」**をクリックします。
5.  作成した API キーを n8n で後で使用するためにコピーし、 **[完了]**をクリックします。

詳細については[TiDB CloudAPI の概要](/tidb-cloud/api-overview.md)参照してください。

## ステップ1：n8nをインストールする {#step-1-install-n8n}

セルフホスティングn8nをインストールするには2つの方法があります。ご都合の良い方をお選びください。

<SimpleTab>
<div label="npm">

1.  ワークスペースに[ノード.js](https://nodejs.org/en/download/)インストールします。
2.  `npx`で n8n をダウンロードして起動します。

    ```shell
    npx n8n
    ```

</div>
<div label="Docker">

1.  ワークスペースに[ドッカー](https://www.docker.com/products/docker-desktop)インストールします。
2.  `docker`で n8n をダウンロードして起動します。

    ```shell
    docker run -it --rm --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n
    ```

</div>
</SimpleTab>

n8nを起動したら、 [ローカルホスト:5678](http://localhost:5678)アクセスしてn8nを試すことができます。

## ステップ2: n8nにTiDB Cloudノードをインストールする {#step-2-install-tidb-cloud-node-in-n8n}

TiDB Cloudノードはnpmリポジトリで`n8n-nodes-tidb-cloud`名前です。n8nでTiDB Cloudを制御するには、このノードを手動でインストールする必要があります。

1.  [ローカルホスト:5678](http://localhost:5678)ページで、セルフホスティング n8n の所有者アカウントを作成します。
2.  **[設定]** &gt; **[コミュニティ ノード]**に移動します。
3.  **「コミュニティ ノードのインストール」を**クリックします。
4.  **npm パッケージ名**フィールドに`n8n-nodes-tidb-cloud`入力します。
5.  **[インストール]**をクリックします。

次に、**ワークフロー**&gt; 検索バーで**TiDB Cloud**ノードを検索し、ワークスペースにドラッグしてTiDB Cloudノードを使用できます。

## ステップ3: ワークフローを構築する {#step-3-build-your-workflow}

このステップでは、 **「実行」**ボタンをクリックしたときに TiDB にデータを挿入する新しいワークフローを作成します。

この使用例のワークフローでは、次のノードが使用されます。

-   [スケジュールトリガー](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.scheduletrigger/)
-   [RSSを読む](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.rssfeedread/)
-   [コード](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.code/)
-   [Gメール](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.gmail/)
-   [TiDB Cloudノード](https://www.npmjs.com/package/n8n-nodes-tidb-cloud)

最終的なワークフローは次の画像のようになります。

![img](/media/tidb-cloud/integration-n8n-workflow-rss.jpg)

### （オプション） TiDB Cloud Serverless クラスターを作成する {#optional-create-a-tidb-cloud-serverless-cluster}

TiDB Cloud Serverless クラスターをお持ちでない場合は、このノードを使用して作成できます。そうでない場合は、この操作をスキップしてください。

1.  **ワークフロー**パネルに移動し、**ワークフローの追加を**クリックします。
2.  新しいワークフロー ワークスペースで、右上隅の**+**をクリックし、 **[すべての**フィールド] を選択します。
3.  `TiDB Cloud`検索し、ワークスペースにドラッグします。
4.  TiDB TiDB Cloud TiDB Cloud API キー) を入力します。
5.  **プロジェクト**リストでプロジェクトを選択します。
6.  **操作**リストで`Create Serverless Cluster`選択します。
7.  **[クラスタ名]**ボックスにクラスター名を入力します。
8.  **「リージョン」**リストで地域を選択します。
9.  **[パスワード]**ボックスに、TiDB クラスターにログインするために使用するパスワードを入力します。
10. ノードを実行するには、 **「ノードの実行」を**クリックします。

> **注記：**
>
> 新しいTiDB Cloud Serverless クラスターを作成するには数秒かかります。

### ワークフローを作成する {#create-a-workflow}

#### ワークフローのスターターとして手動トリガーを使用する {#use-a-manual-trigger-as-the-workflow-s-starter}

1.  ワークフローがまだない場合は、 **「ワークフロー」**パネルに移動し、 **「最初から始める」**をクリックします。そうでない場合は、この手順をスキップしてください。
2.  右上の**+**をクリックして`schedule trigger`検索します。
3.  手動トリガーノードをワークスペースにドラッグし、ダブルクリックします。**パラメータ**ダイアログが表示されます。
4.  ルールを次のように設定します。

    -   **トリガー間隔**: `Days`
    -   **トリガー間の日数**： `1`
    -   **トリガー時刻**: `8am`
    -   **トリガー時間**： `0`

このトリガーは、毎朝午前 8 時にワークフローを実行します。

#### データを挿入するためのテーブルを作成する {#create-a-table-used-to-insert-data}

1.  手動トリガー ノードの右側にある**+**をクリックします。

2.  `TiDB Cloud`検索してワークスペースに追加します。

3.  **パラメータ**ダイアログで、 TiDB Cloudノードの認証情報を入力します。認証情報はTiDB Cloud APIキーです。

4.  **プロジェクト**リストでプロジェクトを選択します。

5.  **操作**リストで`Execute SQL`選択します。

6.  クラスターを選択します。リストに新しいクラスターが表示されない場合は、クラスターの作成が完了するまで数分お待ちください。

7.  **「ユーザー」**リストでユーザーを選択します。TiDB TiDB Cloud は常にデフォルトのユーザーを作成するため、手動で作成する必要はありません。

8.  **データベース**ボックスに`test`入力します。

9.  データベースのパスワードを入力してください。

10. **SQL**ボックスに次の SQL を入力します。

    ```sql
    CREATE TABLE IF NOT EXISTS hacker_news_briefing (creator VARCHAR (200), title TEXT,  link VARCHAR(200), pubdate VARCHAR(200), comments VARCHAR(200), content TEXT, guid VARCHAR (200), isodate VARCHAR(200));
    ```

11. **実行ノード**をクリックしてテーブルを作成します。

#### ハッカーニュースRSSを入手 {#get-the-hacker-news-rss}

1.  TiDB Cloudノードの右側にある**+ を**クリックします。
2.  `RSS Read`検索してワークスペースに追加します。
3.  **URL**ボックスに`https://hnrss.org/frontpage`入力します。

#### TiDBにデータを挿入する {#insert-data-to-tidb}

1.  RSS 読み取りノードの右側にある**+ を**クリックします。
2.  `TiDB Cloud`検索してワークスペースに追加します。
3.  以前のTiDB Cloudノードに入力した資格情報を選択します。
4.  **プロジェクト**リストでプロジェクトを選択します。
5.  **操作**リストで`Insert`選択します。
6.  **クラスタ**、**ユーザー**、**データベース**、および**パスワードの**各ボックスに、対応する値を入力します。
7.  **テーブル**ボックスにテーブル`hacker_news_briefing`入力します。
8.  **「列」**ボックスに`creator, title, link, pubdate, comments, content, guid, isodate`と入力します。

#### ビルドメッセージ {#build-message}

1.  RSS フィード読み取りノードの右側にある**+ を**クリックします。
2.  `code`検索してワークスペースに追加します。
3.  `Run Once for All Items`モードを選択します。
4.  **JavaScript**ボックスに次のコードをコピーして貼り付けます。

    ```javascript
    let message = "";

    // Loop the input items
    for (item of items) {
      message += `
          <h3>${item.json.title}</h3>
          <br>
          ${item.json.content}
          <br>
          `
    }

    let response =
        `
          <!DOCTYPE html>
          <html>
          <head>
          <title>Hacker News Briefing</title>
        </head>
        <body>
            ${message}
        </body>
        </html>
        `
    // Return our message
    return [{json: {response}}];
    ```

#### Gmailでメッセージを送信 {#send-message-by-gmail}

1.  コード ノードの右側にある**+ を**クリックします。
2.  `gmail`検索してワークスペースに追加します。
3.  Gmailノードの認証情報を入力してください。詳細な手順については、 [n8n ドキュメント](https://docs.n8n.io/integrations/builtin/credentials/google/oauth-single-service/)を参照してください。
4.  **リソース**リストで`Message`選択します。
5.  **操作**リストで`Send`選択します。
6.  **[宛先**] ボックスにメールアドレスを入力します。
7.  **[件名]**ボックスに`Hacker News Briefing`と入力します。
8.  [**電子メールの種類]**ボックスで、 `HTML`を選択します。
9.  **メッセージ**ボックスで、 `Expression`クリックし、 `{{ $json["response"] }}`入力します。

    > **注記：**
    >
    > **メッセージ**ボックスの上にマウスを移動して、**式**パターンを選択する必要があります。

## ステップ4: ワークフローを実行する {#step-4-run-your-workflow}

ワークフローを構築した後、 **「ワークフローの実行」**をクリックしてテスト実行できます。

ワークフローが期待通りに実行されると、Hacker Newsのブリーフィングメールが届きます。これらのニュースコンテンツはTiDB Cloud Serverlessクラスターに記録されるため、失われる心配はありません。

**ワークフロー**パネルでこのワークフローを有効化できるようになりました。このワークフローを使えば、Hacker Newsのトップページ記事を毎日取得できるようになります。

## TiDB Cloudノードコア {#tidb-cloud-node-core}

### サポートされている操作 {#supported-operations}

TiDB Cloudノードは[通常ノード](https://docs.n8n.io/workflows/nodes/#regular-nodes)として機能し、次の 5 つの操作のみをサポートします。

-   **サーバーレスクラスタの作成**: TiDB Cloud Serverless クラスターを作成します。
-   **SQL の実行**: TiDB で SQL ステートメントを実行します。
-   **削除**: TiDB 内の行を削除します。
-   **挿入**: TiDB に行を挿入します。
-   **更新**: TiDB 内の行を更新します。

### フィールド {#fields}

異なる操作を使用するには、それぞれの必須フィールドに入力する必要があります。以下に、対応する操作の各フィールドの説明を示します。

<SimpleTab>
<div label="Create Serverless Cluster">

-   **TiDB Cloud APIの認証情報**： TiDB Cloud APIキーのみをサポートします。APIキーの作成方法については、 [TiDB CloudAPIキーを取得する](#prerequisites-get-tidb-cloud-api-key)を参照してください。
-   **プロジェクト**: TiDB Cloudプロジェクト名。
-   **操作**: このノードの操作。サポートされているすべての操作については、 [サポートされている操作](#supported-operations)を参照してください。
-   **クラスタ**： TiDB Cloudクラスター名。新しいクラスターの名前を入力してください。
-   **リージョン**: リージョン名。クラスターをデプロイするリージョンを選択します。通常は、アプリケーションのデプロイメントに最も近いリージョンを選択します。
-   **パスワード**: ルートパスワード。新しいクラスターのパスワードを設定してください。

</div>
<div label="Execute SQL">

-   **TiDB Cloud APIの認証情報**： TiDB Cloud APIキーのみをサポートします。APIキーの作成方法については、 [TiDB CloudAPIキーを取得する](#prerequisites-get-tidb-cloud-api-key)を参照してください。
-   **プロジェクト**: TiDB Cloudプロジェクト名。
-   **操作**: このノードの操作。サポートされているすべての操作については、 [サポートされている操作](#supported-operations)を参照してください。
-   **クラスタ**: TiDB Cloudクラスター名。既存のクラスターを 1 つ選択してください。
-   **パスワード**: TiDB Cloudクラスターのパスワード。
-   **ユーザー**: TiDB Cloudクラスターのユーザー名。
-   **データベース**: データベース名。
-   **SQL** : 実行される SQL ステートメント。

</div>
<div label="Delete">

-   **TiDB Cloud APIの認証情報**： TiDB Cloud APIキーのみをサポートします。APIキーの作成方法については、 [TiDB CloudAPIキーを取得する](#prerequisites-get-tidb-cloud-api-key)を参照してください。
-   **プロジェクト**: TiDB Cloudプロジェクト名。
-   **操作**: このノードの操作。サポートされているすべての操作については、 [サポートオペレーション](#supported-operations)を参照してください。
-   **クラスタ**: TiDB Cloudクラスター名。既存のクラスターを 1 つ選択してください。
-   **パスワード**: TiDB Cloudクラスターのパスワード。
-   **ユーザー**: TiDB Cloudクラスターのユーザー名。
-   **データベース**: データベース名。
-   **テーブル**: テーブル名。2 `From list`でテーブル名を選択するか、 `Name`モードでテーブル名を手動で入力できます。
-   **削除キー**: データベース内のどの行を削除するかを決定するアイテムのプロパティ名。アイテムとは、あるノードから別のノードに送信されるデータです。ノードは、受信データの各アイテムに対してアクションを実行します。n8nにおけるアイテムの詳細については、 [n8n ドキュメント](https://docs.n8n.io/workflows/items/)参照してください。

</div>
<div label="Insert">

-   **TiDB Cloud APIの認証情報**： TiDB Cloud APIキーのみをサポートします。APIキーの作成方法については、 [TiDB CloudAPIキーを取得する](#prerequisites-get-tidb-cloud-api-key)を参照してください。
-   **プロジェクト**: TiDB Cloudプロジェクト名。
-   **操作**: このノードの操作。サポートされているすべての操作については、 [サポートオペレーション](#supported-operations)を参照してください。
-   **クラスタ**: TiDB Cloudクラスター名。既存のクラスターを 1 つ選択してください。
-   **パスワード**: TiDB Cloudクラスターのパスワード。
-   **ユーザー**: TiDB Cloudクラスターのユーザー名。
-   **データベース**: データベース名。
-   **テーブル**: テーブル名。2 `From list`でテーブル名を選択するか、 `Name`モードでテーブル名を手動で入力できます。
-   **列**: 入力アイテムのプロパティをカンマ区切りでリストしたもので、新しい行の列として使用されます。アイテムとは、あるノードから別のノードに送信されるデータです。ノードは、入力データの各アイテムに対してアクションを実行します。n8nにおけるアイテムの詳細については、 [n8n ドキュメント](https://docs.n8n.io/workflows/items/)参照してください。

</div>
<div label="Update">

-   **TiDB Cloud APIの認証情報**： TiDB Cloud APIキーのみをサポートします。APIキーの作成方法については、 [TiDB CloudAPIキーを取得する](#prerequisites-get-tidb-cloud-api-key)を参照してください。
-   **プロジェクト**: TiDB Cloudプロジェクト名。
-   **操作**: このノードの操作。サポートされているすべての操作については、 [サポートオペレーション](#supported-operations)を参照してください。
-   **クラスタ**: TiDB Cloudクラスター名。既存のクラスターを 1 つ選択してください。
-   **パスワード**: TiDB Cloudクラスターのパスワード。
-   **ユーザー**: TiDB Cloudクラスターのユーザー名。
-   **データベース**: データベース名。
-   **テーブル**: テーブル名。2 `From list`でテーブル名を選択するか、 `Name`モードでテーブル名を手動で入力できます。
-   **更新キー**: データベース内のどの行を更新するかを決定するアイテムのプロパティ名。アイテムとは、あるノードから別のノードに送信されるデータです。ノードは、受信データの各アイテムに対してアクションを実行します。n8nにおけるアイテムの詳細については、 [n8n ドキュメント](https://docs.n8n.io/workflows/items/)参照してください。
-   **列**: 更新する行の列として使用される、入力項目のプロパティのコンマ区切りリスト。

</div>
</SimpleTab>

### 制限事項 {#limitations}

-   通常、 **SQL実行**操作では1つのSQL文のみが許可されます。1回の操作で複数のSQL文を実行する場合は、 [`tidb_multi_statement_mode`](https://docs.pingcap.com/tidbcloud/system-variables#tidb_multi_statement_mode-new-in-v4011)手動で有効にする必要があります。
-   **削除**および**更新**操作では、キーとして1つのフィールドを指定する必要があります。例えば、 `Delete Key` `id`に設定され、これは`DELETE FROM table WHERE id = ${item.id}`実行するのと同じです。現在、**削除**および**更新**操作では、1つのキーの指定のみがサポートされています。
-   **挿入**および**更新**操作の場合、**列**フィールドにコンマ区切りのリストを指定する必要があり、フィールド名は入力項目のプロパティと同じである必要があります。
