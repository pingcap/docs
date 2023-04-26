---
title: Integrate TiDB Cloud with n8n
summary: Learn the use of TiDB Cloud node in n8n.
---

# TiDB Cloudをn8n と統合する {#integrate-tidb-cloud-with-n8n}

[n8n](https://n8n.io/)は、拡張可能なワークフロー自動化ツールです。 [フェアコード](https://faircode.io/)配布モデルでは、n8n は常にソース コードを表示し、セルフホストに使用でき、カスタム関数、ロジック、およびアプリを追加できます。

このドキュメントでは、自動ワークフローを構築する方法を紹介します。TiDB TiDB Cloud Serverless Tierクラスターを作成し、Hacker News RSS を収集し、それを TiDB に保存して、ブリーフィング メールを送信します。

## 前提条件: TiDB Cloud API キーを取得する {#prerequisites-get-tidb-cloud-api-key}

1.  TiDB Cloudダッシュボードにアクセスします。
2.  クリック<mdsvgicon name="icon-top-organization">右上隅にある**[組織]** &gt; <strong>[組織の設定]</strong> 。</mdsvgicon>
3.  **[API キー]**タブをクリックします。
4.  **[API キーの作成]**ボタンをクリックして、新しい API キーを作成します。
5.  後で n8n で使用するために、作成した API キーを保存します。

詳細については、 [TiDB CloudAPI の概要](/tidb-cloud/api-overview.md)を参照してください。

## ステップ 1: n8n をインストールする {#step-1-install-n8n}

自己ホスティング n8n をインストールするには 2 つの方法があります。あなたに合ったものを選んでください。

<SimpleTab>
<div label="npm">

1.  ワークスペースに[node.js](https://nodejs.org/en/download/)をインストールします。
2.  n8n を`npx`でダウンロードして起動します。

    ```shell
    npx n8n
    ```

</div>
<div label="Docker">

1.  ワークスペースに[ドッカー](https://www.docker.com/products/docker-desktop)をインストールします。
2.  n8n を`docker`でダウンロードして起動します。

    ```shell
    docker run -it --rm --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n
    ```

</div>
</SimpleTab>

n8n を起動したら、 [ローカルホスト:5678](http://localhost:5678)にアクセスして n8n を試すことができます。

## ステップ 2: n8n にTiDB Cloudノードをインストールする {#step-2-install-tidb-cloud-node-in-n8n}

TiDB Cloudノードは、npm リポジトリで`n8n-nodes-tidb-cloud`という名前です。 n8n でTiDB Cloudを制御するには、このノードを手動でインストールする必要があります。

1.  [ローカルホスト:5678](http://localhost:5678)ページで、セルフホスティング n8n の所有者アカウントを作成します。
2.  **[設定]** &gt; <strong>[コミュニティ ノード]</strong>に移動します。
3.  **[コミュニティ ノードのインストール]**をクリックします。
4.  **npm パッケージ名**フィールドに`n8n-nodes-tidb-cloud`と入力します。
5.  **[インストール]**をクリックします。

その後、 **[ワークフロー]** &gt; [検索バー] で<strong>TiDB Cloud</strong>ノードを検索し、 TiDB Cloudノードをワークスペースにドラッグして使用できます。

## ステップ 3: ワークフローを構築する {#step-3-build-your-workflow}

このステップでは、 **[実行]**ボタンをクリックしたときに TiDB にデータを挿入するための新しいワークフローを作成します。

この使用ワークフローの例では、次のノードを使用します。

-   [トリガーのスケジュール](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.scheduletrigger/)
-   [RSS 読み取り](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.rssfeedread/)
-   [コード](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.code/)
-   [Gmail](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.gmail/)
-   [TiDB Cloudノード](https://www.npmjs.com/package/n8n-nodes-tidb-cloud)

最終的なワークフローは次の図のようになります。

![img](/media/tidb-cloud/integration-n8n-workflow-rss.jpg)

### (オプション) TiDB Cloud Serverless Tierクラスターを作成する {#optional-create-a-tidb-cloud-serverless-tier-cluster}

TiDB Cloud Serverless Tierクラスターがない場合は、このノードを使用して作成できます。それ以外の場合は、この操作をスキップしてかまいません。

1.  **[ワークフロー]**パネルに移動し、 <strong>[ワークフローを追加]</strong>をクリックします。
2.  新しいワークフロー ワークスペースで、右上隅の**[+]**をクリックし、 <strong>[すべての</strong>フィールド] を選択します。
3.  `TiDB Cloud`検索し、ワークスペースにドラッグします。
4.  TiDB Cloudノードの資格情報 ( TiDB Cloud API キー) を入力します。
5.  **[プロジェクト]**リストで、プロジェクトを選択します。
6.  **[操作]**リストで、 `Create Serverless Cluster`を選択します。
7.  **[クラスタ名]**ボックスに、クラスター名を入力します。
8.  **リージョン**リストで、リージョンを選択します。
9.  **[パスワード]**ボックスに、TiDB クラスターへのログインに使用するパスワードを入力します。
10. **[ノードの実行]**をクリックして、ノードを実行します。

> **ノート：**
>
> 新しい TiDB サーバーレス クラスターを作成するには、数秒かかります。

### ワークフローを作成する {#create-a-workflow}

#### ワークフローのスターターとして手動トリガーを使用する {#use-a-manual-trigger-as-the-workflow-s-starter}

1.  ワークフローがまだない場合は、 **[ワークフロー]**パネルに移動し、 <strong>[最初から開始]</strong>をクリックします。それ以外の場合は、この手順をスキップしてください。
2.  右上隅の**+**をクリックして検索します`schedule trigger` 。
3.  手動トリガー ノードをワークスペースにドラッグし、ノードをダブルクリックします。 **[パラメータ]**ダイアログが表示されます。
4.  ルールを次のように構成します。

    -   **トリガー間隔**: `Days`
    -   **トリガー間の日数**: `1`
    -   **トリガー時間**: `8am`
    -   **分でトリガー**: `0`

このトリガーは、毎朝午前 8 時にワークフローを実行します。

#### データの挿入に使用するテーブルを作成する {#create-a-table-used-to-insert-data}

1.  手動トリガー ノードの右側にある**+**をクリックします。

2.  `TiDB Cloud`検索してワークスペースに追加します。

3.  **[パラメーター]**ダイアログで、 TiDB Cloudノードの資格情報を入力します。資格情報は、 TiDB Cloud API キーです。

4.  **[プロジェクト]**リストで、プロジェクトを選択します。

5.  **[操作]**リストで、 `Execute SQL`を選択します。

6.  クラスターを選択します。リストに新しいクラスターが表示されていない場合は、クラスターの作成が完了するまで数分待つ必要があります。

7.  **[ユーザー]**リストで、ユーザーを選択します。 TiDB Cloud は常にデフォルト ユーザーを作成するため、手動で作成する必要はありません。

8.  **[データベース]**ボックスに`test`と入力します。

9.  データベースのパスワードを入力します。

10. **[SQL]**ボックスに、次の SQL を入力します。

    ```sql
    CREATE TABLE IF NOT EXISTS hacker_news_briefing (creator VARCHAR (200), title TEXT,  link VARCHAR(200), pubdate VARCHAR(200), comments VARCHAR(200), content TEXT, guid VARCHAR (200), isodate VARCHAR(200));
    ```

11. **[ノードの実行]**をクリックして、テーブルを作成します。

#### ハッカー ニュースの RSS を入手する {#get-the-hacker-news-rss}

1.  TiDB Cloudノードの右側にある**+**をクリックします。
2.  `RSS Read`検索してワークスペースに追加します。
3.  **URL**ボックスに`https://hnrss.org/frontpage`と入力します。

#### TiDB にデータを挿入する {#insert-data-to-tidb}

1.  RSS Read ノードの右側にある**+**をクリックします。
2.  `TiDB Cloud`検索してワークスペースに追加します。
3.  前のTiDB Cloudノードで入力した資格情報を選択します。
4.  **[プロジェクト]**リストで、プロジェクトを選択します。
5.  **[操作]**リストで、 `Insert`を選択します。
6.  **クラスタ** 、 <strong>User</strong> 、 <strong>Database</strong> 、および<strong>Password</strong>ボックスに、対応する値を入力します。
7.  **[テーブル]**ボックスに、 `hacker_news_briefing`テーブルを入力します。
8.  **[列]**ボックスに`creator, title, link, pubdate, comments, content, guid, isodate`と入力します。

#### ビルド メッセージ {#build-message}

1.  RSS Feed Read ノードの右にある**+**をクリックします。
2.  `code`検索してワークスペースに追加します。
3.  `Run Once for All Items`モードを選択します。
4.  **JavaScript**ボックスに、次のコードをコピーして貼り付けます。

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

#### Gmail でメッセージを送信する {#send-message-by-gmail}

1.  コード ノードの右側にある**[+]**をクリックします。
2.  `gmail`検索してワークスペースに追加します。
3.  Gmail ノードの資格情報を入力します。詳細な手順については、 [n8n ドキュメント](https://docs.n8n.io/integrations/builtin/credentials/google/oauth-single-service/)を参照してください。
4.  **[リソース]**リストで、 `Message`を選択します。
5.  **[操作]**リストで、 `Send`を選択します。
6.  **[宛先]**ボックスに、メールアドレスを入力します。
7.  **[件名]**ボックスに`Hacker News Briefing`と入力します。
8.  **[電子メールの種類]**ボックスで、 `HTML`を選択します。
9.  **[メッセージ]**ボックスで、 `Expression`をクリックして`{{ $json["response"] }}`と入力します。

    > **ノート：**
    >
    > **メッセージ**ボックスにカーソルを合わせて、<strong>式</strong>パターンを選択する必要があります。

## ステップ 4: ワークフローを実行する {#step-4-run-your-workflow}

ワークフローを構築したら、 **[ワークフローの実行] を**クリックしてテスト実行できます。

ワークフローが期待どおりに実行されると、Hacker News のブリーフィング メールが届きます。これらのニュース コンテンツはTiDB Cloud Serverless Tierクラスターに記録されるため、失われる心配はありません。

これで、**ワークフロー**パネルでこのワークフローをアクティブ化できます。このワークフローは、Hacker News のトップページの記事を毎日入手するのに役立ちます。

## TiDB Cloudノード コア {#tidb-cloud-node-core}

### サポートされている操作 {#supported-operations}

TiDB Cloudノードは[通常のノード](https://docs.n8n.io/workflows/nodes/#regular-nodes)として機能し、次の 5 つの操作のみをサポートします。

-   **Create Serverless クラスタ** : TiDB Cloud Serverless Tierクラスターを作成します。
-   **Execute SQL** : TiDB で SQL ステートメントを実行します。
-   **Delete** : TiDB の行を削除します。
-   **Insert** : TiDB に行を挿入します。
-   **Update** : TiDB の行を更新します。

### 田畑 {#fields}

さまざまな操作を使用するには、さまざまな必須フィールドに入力する必要があります。次に、対応する操作の各フィールドの説明を示します。

<SimpleTab>
<div label="Create Serverless Cluster">

-   **TiDB Cloud API の認証情報**: TiDB Cloud API キーのみをサポートします。 API キーの作成方法については、 [TiDB CloudAPI キーを取得する](#prerequisites-get-tidb-cloud-api-key)を参照してください。
-   **Project** : TiDB Cloudのプロジェクト名。
-   **Operation** : このノードの操作。サポートされているすべての操作については、 [サポートされている操作](#supported-operations)を参照してください。
-   **クラスタ** : TiDB Cloudのクラスター名。新しいクラスターの名前を入力します。
-   **リージョン**: 地域名。クラスターをデプロイするリージョンを選択します。通常は、アプリケーションのデプロイに最も近いリージョンを選択してください。
-   **パスワード**: ルート パスワード。新しいクラスターのパスワードを設定します。

</div>
<div label="Execute SQL">

-   **TiDB Cloud API の認証情報**: TiDB Cloud API キーのみをサポートします。 API キーの作成方法については、 [TiDB CloudAPI キーを取得する](#prerequisites-get-tidb-cloud-api-key)を参照してください。
-   **Project** : TiDB Cloudのプロジェクト名。
-   **Operation** : このノードの操作。サポートされているすべての操作については、 [サポートされている操作](#supported-operations)を参照してください。
-   **クラスタ** : TiDB Cloudのクラスター名。既存のクラスターを 1 つ選択する必要があります。
-   **Password** : TiDB Cloudクラスターのパスワード。
-   **User** : TiDB Cloudクラスターのユーザー名。
-   **データベース**: データベース名。
-   **SQL** : 実行する SQL ステートメント。

</div>
<div label="Delete">

-   **TiDB Cloud API の認証情報**: TiDB Cloud API キーのみをサポートします。 API キーの作成方法については、 [TiDB CloudAPI キーを取得する](#prerequisites-get-tidb-cloud-api-key)を参照してください。
-   **Project** : TiDB Cloudのプロジェクト名。
-   **Operation** : このノードの操作。サポートされているすべての操作については、 [サポート操作](#supported-operations)を参照してください。
-   **クラスタ** : TiDB Cloudのクラスター名。既存のクラスターを 1 つ選択する必要があります。
-   **Password** : TiDB Cloudクラスターのパスワード。
-   **User** : TiDB Cloudクラスターのユーザー名。
-   **データベース**: データベース名。
-   **Table** : テーブル名。 `From list`モードを使用していずれかを選択するか、 `Name`モードを使用してテーブル名を手動で入力できます。
-   **Delete Key** : データベース内のどの行を削除するかを決定する項目のプロパティの名前。アイテムは、あるノードから別のノードに送信されるデータです。ノードは、受信データの各項目に対してアクションを実行します。 n8n のアイテムの詳細については、 [n8n ドキュメント](https://docs.n8n.io/workflows/items/)を参照してください。

</div>
<div label="Insert">

-   **TiDB Cloud API の認証情報**: TiDB Cloud API キーのみをサポートします。 API キーの作成方法については、 [TiDB CloudAPI キーを取得する](#prerequisites-get-tidb-cloud-api-key)を参照してください。
-   **Project** : TiDB Cloudのプロジェクト名。
-   **Operation** : このノードの操作。サポートされているすべての操作については、 [サポートオペレーション](#supported-operations)を参照してください。
-   **クラスタ** : TiDB Cloudのクラスター名。既存のクラスターを 1 つ選択する必要があります。
-   **Password** : TiDB Cloudクラスターのパスワード。
-   **User** : TiDB Cloudクラスターのユーザー名。
-   **データベース**: データベース名。
-   **Table** : テーブル名。 `From list`モードを使用していずれかを選択するか、 `Name`モードを使用してテーブル名を手動で入力できます。
-   **Columns** : 新しい行の列として使用される、入力項目のプロパティのコンマ区切りリスト。アイテムは、あるノードから別のノードに送信されるデータです。ノードは、受信データの各項目に対してアクションを実行します。 n8n のアイテムの詳細については、 [n8n ドキュメント](https://docs.n8n.io/workflows/items/)を参照してください。

</div>
<div label="Update">

-   **TiDB Cloud API の認証情報**: TiDB Cloud API キーのみをサポートします。 API キーの作成方法については、 [TiDB CloudAPI キーを取得する](#prerequisites-get-tidb-cloud-api-key)を参照してください。
-   **Project** : TiDB Cloudのプロジェクト名。
-   **Operation** : このノードの操作。サポートされているすべての操作については、 [サポート操作](#supported-operations)を参照してください。
-   **クラスタ** : TiDB Cloudのクラスター名。既存のクラスターを 1 つ選択する必要があります。
-   **Password** : TiDB Cloudクラスターのパスワード。
-   **User** : TiDB Cloudクラスターのユーザー名。
-   **データベース**: データベース名。
-   **Table** : テーブル名。 `From list`モードを使用していずれかを選択するか、 `Name`モードを使用してテーブル名を手動で入力できます。
-   **Update Key** : データベース内のどの行を更新するかを決定する項目のプロパティの名前。アイテムは、あるノードから別のノードに送信されるデータです。ノードは、受信データの各項目に対してアクションを実行します。 n8n のアイテムの詳細については、 [n8n ドキュメント](https://docs.n8n.io/workflows/items/)を参照してください。
-   **Columns** : 入力項目のプロパティのコンマ区切りリスト。更新する行の列として使用されます。

</div>
</SimpleTab>

### 制限事項 {#limitations}

-   通常、 **SQL 実行**操作で使用できる SQL ステートメントは 1 つだけです。 1 回の操作で複数のステートメントを実行する場合は、手動で[`tidb_multi_statement_mode`](https://docs.pingcap.com/tidbcloud/system-variables#tidb_multi_statement_mode-new-in-v4011)有効にする必要があります。
-   **削除**操作と<strong>更新</strong>操作では、1 つのフィールドをキーとして指定する必要があります。たとえば、 `Delete Key`は`id`に設定され、これは`DELETE FROM table WHERE id = ${item.id}`を実行することと同じです。現在、<strong>削除操作</strong>と<strong>更新</strong>操作では、1 つのキーの指定のみがサポートされています。
-   **挿入**操作と<strong>更新</strong>操作では、 <strong>[列</strong>] フィールドにカンマ区切りのリストを指定する必要があり、フィールド名は入力項目のプロパティと同じである必要があります。
