---
title: Integrate TiDB Cloud with n8n
summary: Learn the use of TiDB Cloud node in n8n.
---

# TiDB Cloudと n8n を統合する {#integrate-tidb-cloud-with-n8n}

[n8n](https://n8n.io/)は、拡張可能なワークフロー自動化ツールです。 [フェアコード](https://faircode.io/)ディストリビューション モデルを使用すると、n8n には常にソース コードが表示され、セルフホストが可能になり、カスタム関数、ロジック、アプリを追加できるようになります。

このドキュメントでは、自動ワークフローの構築方法を紹介します。つまり、TiDB サーバーレス クラスターを作成し、Hacker News RSS を収集し、それを TiDB に保存し、ブリーフィング電子メールを送信します。

## 前提条件: TiDB CloudAPI キーを取得する {#prerequisites-get-tidb-cloud-api-key}

1.  TiDB Cloudダッシュボードにアクセスします。
2.  クリック<mdsvgicon name="icon-top-organization">をクリックし、左下隅にある**「組織の設定」**をクリックします。</mdsvgicon>
3.  **「API キー」**タブをクリックします。
4.  **「API キーの作成」**ボタンをクリックして、新しい API キーを作成します。
5.  作成した API キーを保存して、後で n8n で使用できるようにします。

詳細については、 [TiDB CloudAPI の概要](/tidb-cloud/api-overview.md)を参照してください。

## ステップ 1: n8n をインストールする {#step-1-install-n8n}

セルフホスティング n8n をインストールするには 2 つの方法があります。自分に合ったものを選択してください。

<SimpleTab>
<div label="npm">

1.  [ノード.js](https://nodejs.org/en/download/)ワークスペースにインストールします。
2.  `npx`で n8n をダウンロードして起動します。

    ```shell
    npx n8n
    ```

</div>
<div label="Docker">

1.  [ドッカー](https://www.docker.com/products/docker-desktop)ワークスペースにインストールします。
2.  `docker`で n8n をダウンロードして起動します。

    ```shell
    docker run -it --rm --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n
    ```

</div>
</SimpleTab>

n8n を起動した後、 [ローカルホスト:5678](http://localhost:5678)にアクセスして n8n を試すことができます。

## ステップ 2: TiDB Cloudノードを n8n にインストールする {#step-2-install-tidb-cloud-node-in-n8n}

TiDB Cloudノードは、npm リポジトリでは`n8n-nodes-tidb-cloud`という名前が付けられます。 n8n でTiDB Cloudを制御するには、このノードを手動でインストールする必要があります。

1.  [ローカルホスト:5678](http://localhost:5678)ページで、セルフホスティング n8n の所有者アカウントを作成します。
2.  **[設定]** &gt; **[コミュニティ ノード]**に移動します。
3.  **[コミュニティ ノードのインストール]**をクリックします。
4.  **[npm パッケージ名]**フィールドに`n8n-nodes-tidb-cloud`と入力します。
5.  **「インストール」**をクリックします。

次に、 **[ワークフロー]** &gt; 検索バーで**TiDB Cloud**ノードを検索し、 TiDB Cloudノードをワークスペースにドラッグして使用できます。

## ステップ 3: ワークフローを構築する {#step-3-build-your-workflow}

このステップでは、 **「実行」**ボタンをクリックしたときにデータを TiDB に挿入する新しいワークフローを作成します。

この使用例ワークフローでは、次のノードが使用されます。

-   [スケジュールトリガー](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.scheduletrigger/)
-   [RSSを読む](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.rssfeedread/)
-   [コード](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.code/)
-   [Gメール](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.gmail/)
-   [TiDB Cloudノード](https://www.npmjs.com/package/n8n-nodes-tidb-cloud)

最終的なワークフローは次の図のようになります。

![img](/media/tidb-cloud/integration-n8n-workflow-rss.jpg)

### (オプション) TiDB サーバーレスクラスターを作成する {#optional-create-a-tidb-serverless-cluster}

TiDB サーバーレス クラスターがない場合は、このノードを使用してクラスターを作成できます。それ以外の場合は、この操作をスキップしてください。

1.  **「ワークフロー」**パネルに移動し、 **「ワークフローの追加」**をクリックします。
2.  新しいワークフロー ワークスペースで、右上隅の**[+]**をクリックし、 **[すべての**フィールド] を選択します。
3.  `TiDB Cloud`検索してワークスペースにドラッグします。
4.  TiDB Cloudノードの資格情報 ( TiDB CloudAPI キー) を入力します。
5.  **「プロジェクト」**リストでプロジェクトを選択します。
6.  **「操作」**リストで`Create Serverless Cluster`を選択します。
7.  **[クラスタ名]**ボックスにクラスター名を入力します。
8.  **「リージョン」**リストで地域を選択します。
9.  **「パスワード」**ボックスに、TiDB クラスターへのログインに使用するパスワードを入力します。
10. **「ノードの実行」**をクリックしてノードを実行します。

> **注記：**
>
> 新しい TiDB サーバーレス クラスターを作成するには数秒かかります。

### ワークフローを作成する {#create-a-workflow}

#### ワークフローのスターターとして手動トリガーを使用する {#use-a-manual-trigger-as-the-workflow-s-starter}

1.  ワークフローがまだない場合は、 **「ワークフロー」**パネルに移動し、 **「最初から開始」**をクリックします。それ以外の場合は、この手順をスキップしてください。
2.  右上隅の**+**をクリックして検索します`schedule trigger` 。
3.  手動トリガー ノードをワークスペースにドラッグし、ノードをダブルクリックします。 **「パラメータ」**ダイアログが表示されます。
4.  ルールを次のように構成します。

    -   **トリガー間隔**: `Days`
    -   **トリガー間の日数**: `1`
    -   **時のトリガー**: `8am`
    -   **分単位でトリガー**: `0`

このトリガーはワークフローを毎朝午前 8 時に実行します。

#### データの挿入に使用するテーブルを作成する {#create-a-table-used-to-insert-data}

1.  手動トリガー ノードの右側にある**+**をクリックします。

2.  `TiDB Cloud`検索してワークスペースに追加します。

3.  **[パラメーター]**ダイアログで、 TiDB Cloudノードの認証情報を入力します。資格情報はTiDB CloudAPI キーです。

4.  **「プロジェクト」**リストでプロジェクトを選択します。

5.  **「操作」**リストで`Execute SQL`を選択します。

6.  クラスターを選択します。リストに新しいクラスターが表示されない場合は、クラスターの作成が完了するまで数分間待つ必要があります。

7.  **「ユーザー」**リストでユーザーを選択します。 TiDB Cloud は常にデフォルト ユーザーを作成するため、手動でユーザーを作成する必要はありません。

8.  **[データベース]**ボックスに`test`と入力します。

9.  データベースのパスワードを入力します。

10. **[SQL]**ボックスに次の SQL を入力します。

    ```sql
    CREATE TABLE IF NOT EXISTS hacker_news_briefing (creator VARCHAR (200), title TEXT,  link VARCHAR(200), pubdate VARCHAR(200), comments VARCHAR(200), content TEXT, guid VARCHAR (200), isodate VARCHAR(200));
    ```

11. **「ノードの実行」**をクリックしてテーブルを作成します。

#### ハッカー ニュース RSS を入手する {#get-the-hacker-news-rss}

1.  TiDB Cloudノードの右側にある**+**をクリックします。
2.  `RSS Read`検索してワークスペースに追加します。
3.  **[URL]**ボックスに`https://hnrss.org/frontpage`と入力します。

#### TiDB へのデータの挿入 {#insert-data-to-tidb}

1.  「RSS 読み取り」ノードの右側にある**「+」**をクリックします。
2.  `TiDB Cloud`検索してワークスペースに追加します。
3.  前のTiDB Cloudノードで入力した認証情報を選択します。
4.  **「プロジェクト」**リストでプロジェクトを選択します。
5.  **「操作」**リストで`Insert`を選択します。
6.  **[クラスタ]** 、 **[ユーザー**] 、 **[データベース]** 、および**[パスワード]**ボックスに、対応する値を入力します。
7.  **「テーブル」**ボックスに、 `hacker_news_briefing`テーブルを入力します。
8.  **[列]**ボックスに`creator, title, link, pubdate, comments, content, guid, isodate`と入力します。

#### ビルドメッセージ {#build-message}

1.  「RSS フィード読み取り」ノードの右側にある**「+」**をクリックします。
2.  `code`検索してワークスペースに追加します。
3.  `Run Once for All Items`モードを選択します。
4.  **[JavaScript]**ボックスに、次のコードをコピーして貼り付けます。

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

#### Gmailでメッセージを送信する {#send-message-by-gmail}

1.  コード ノードの右側にある**+**をクリックします。
2.  `gmail`検索してワークスペースに追加します。
3.  Gmail ノードの認証情報を入力します。詳細な手順については、 [n8n ドキュメント](https://docs.n8n.io/integrations/builtin/credentials/google/oauth-single-service/)を参照してください。
4.  **「リソース」**リストで`Message`を選択します。
5.  **「操作」**リストで`Send`を選択します。
6.  **[宛先]**ボックスに電子メールを入力します。
7.  **[件名]**ボックスに`Hacker News Briefing`と入力します。
8.  **[電子メールの種類]**ボックスで、 `HTML`を選択します。
9.  **「メッセージ」**ボックスで`Expression`をクリックし、 `{{ $json["response"] }}`と入力します。

    > **注記：**
    >
    > **メッセージ**ボックスの上にマウスを移動し、**式**パターンを選択する必要があります。

## ステップ 4: ワークフローを実行する {#step-4-run-your-workflow}

ワークフローを構築した後、 **「ワークフローの実行」を**クリックしてテスト実行できます。

ワークフローが期待どおりに実行されると、Hacker News の概要メールが届きます。これらのニュース コンテンツは TiDB サーバーレス クラスターに記録されるため、紛失することを心配する必要はありません。

これで、 **「ワークフロー」**パネルでこのワークフローをアクティブ化できるようになりました。このワークフローは、Hacker News のトップページの記事を毎日取得するのに役立ちます。

## TiDB Cloudノード コア {#tidb-cloud-node-core}

### サポートされている操作 {#supported-operations}

TiDB Cloudノードは[通常のノード](https://docs.n8n.io/workflows/nodes/#regular-nodes)として機能し、次の 5 つの操作のみをサポートします。

-   **サーバーレスクラスタの作成**: TiDB サーバーレスクラスターを作成します。
-   **SQL の実行**: TiDB で SQL ステートメントを実行します。
-   **削除**: TiDB 内の行を削除します。
-   **Insert** : TiDB に行を挿入します。
-   **Update** : TiDB 内の行を更新します。

### 田畑 {#fields}

さまざまな操作を使用するには、さまざまな必須フィールドに入力する必要があります。以下に、対応する操作の各フィールドの説明を示します。

<SimpleTab>
<div label="Create Serverless Cluster">

-   **TiDB CloudAPI の認証情報**: TiDB CloudAPI キーのみをサポートします。 APIキーの作成方法については、 [TiDB CloudAPI キーを取得する](#prerequisites-get-tidb-cloud-api-key)を参照してください。
-   **プロジェクト**: TiDB Cloudプロジェクト名。
-   **操作**: このノードの操作。サポートされているすべての操作については、 [サポートされている操作](#supported-operations)を参照してください。
-   **クラスタ**: TiDB Cloudクラスター名。新しいクラスターの名前を入力します。
-   **リージョン**: 地域名。クラスターをデプロイするリージョンを選択します。通常は、アプリケーションのデプロイメントに最も近いリージョンを選択します。
-   **パスワード**: root のパスワード。新しいクラスターのパスワードを設定します。

</div>
<div label="Execute SQL">

-   **TiDB CloudAPI の認証情報**: TiDB CloudAPI キーのみをサポートします。 APIキーの作成方法については、 [TiDB CloudAPI キーを取得する](#prerequisites-get-tidb-cloud-api-key)を参照してください。
-   **プロジェクト**: TiDB Cloudプロジェクト名。
-   **操作**: このノードの操作。サポートされているすべての操作については、 [サポートされている操作](#supported-operations)を参照してください。
-   **クラスタ**: TiDB Cloudクラスター名。既存のクラスターを 1 つ選択する必要があります。
-   **パスワード**: TiDB Cloudクラスターのパスワード。
-   **ユーザー**: TiDB Cloudクラスターのユーザー名。
-   **データベース**: データベース名。
-   **SQL** : 実行される SQL ステートメント。

</div>
<div label="Delete">

-   **TiDB CloudAPI の認証情報**: TiDB CloudAPI キーのみをサポートします。 APIキーの作成方法については、 [TiDB CloudAPI キーを取得する](#prerequisites-get-tidb-cloud-api-key)を参照してください。
-   **プロジェクト**: TiDB Cloudプロジェクト名。
-   **操作**: このノードの操作。サポートされているすべての操作については、 [サポートオペレーション](#supported-operations)を参照してください。
-   **クラスタ**: TiDB Cloudクラスター名。既存のクラスターを 1 つ選択する必要があります。
-   **パスワード**: TiDB Cloudクラスターのパスワード。
-   **ユーザー**: TiDB Cloudクラスターのユーザー名。
-   **データベース**: データベース名。
-   **テーブル**: テーブル名。 `From list`モードを使用して 1 つを選択することも、 `Name`モードを使用してテーブル名を手動で入力することもできます。
-   **削除キー**: データベース内のどの行を削除するかを決定する項目のプロパティの名前。アイテムとは、あるノードから別のノードに送信されるデータです。ノードは、受信データの各項目に対してアクションを実行します。 n8n の項目の詳細については、 [n8n ドキュメント](https://docs.n8n.io/workflows/items/)を参照してください。

</div>
<div label="Insert">

-   **TiDB CloudAPI の認証情報**: TiDB CloudAPI キーのみをサポートします。 APIキーの作成方法については、 [TiDB CloudAPI キーを取得する](#prerequisites-get-tidb-cloud-api-key)を参照してください。
-   **プロジェクト**: TiDB Cloudプロジェクト名。
-   **操作**: このノードの操作。サポートされているすべての操作については、 [サポートオペレーション](#supported-operations)を参照してください。
-   **クラスタ**: TiDB Cloudクラスター名。既存のクラスターを 1 つ選択する必要があります。
-   **パスワード**: TiDB Cloudクラスターのパスワード。
-   **ユーザー**: TiDB Cloudクラスターのユーザー名。
-   **データベース**: データベース名。
-   **テーブル**: テーブル名。 `From list`モードを使用して 1 つを選択することも、 `Name`モードを使用してテーブル名を手動で入力することもできます。
-   **列**: 入力項目のプロパティのカンマ区切りのリスト。新しい行の列として使用されます。アイテムとは、あるノードから別のノードに送信されるデータです。ノードは、受信データの各項目に対してアクションを実行します。 n8n の項目の詳細については、 [n8n ドキュメント](https://docs.n8n.io/workflows/items/)を参照してください。

</div>
<div label="Update">

-   **TiDB CloudAPI の認証情報**: TiDB CloudAPI キーのみをサポートします。 APIキーの作成方法については、 [TiDB CloudAPI キーを取得する](#prerequisites-get-tidb-cloud-api-key)を参照してください。
-   **プロジェクト**: TiDB Cloudプロジェクト名。
-   **操作**: このノードの操作。サポートされているすべての操作については、 [サポートオペレーション](#supported-operations)を参照してください。
-   **クラスタ**: TiDB Cloudクラスター名。既存のクラスターを 1 つ選択する必要があります。
-   **パスワード**: TiDB Cloudクラスターのパスワード。
-   **ユーザー**: TiDB Cloudクラスターのユーザー名。
-   **データベース**: データベース名。
-   **テーブル**: テーブル名。 `From list`モードを使用して 1 つを選択することも、 `Name`モードを使用してテーブル名を手動で入力することもできます。
-   **更新キー**: データベース内のどの行を更新するかを決定するアイテムのプロパティの名前。アイテムとは、あるノードから別のノードに送信されるデータです。ノードは、受信データの各項目に対してアクションを実行します。 n8n の項目の詳細については、 [n8n ドキュメント](https://docs.n8n.io/workflows/items/)を参照してください。
-   **列**: 入力項目のプロパティのカンマ区切りのリスト。更新される行の列として使用されます。

</div>
</SimpleTab>

### 制限事項 {#limitations}

-   通常、 **SQL 実行**操作では 1 つの SQL ステートメントのみが許可されます。 1 回の操作で複数のステートメントを実行する場合は、手動で[`tidb_multi_statement_mode`](https://docs.pingcap.com/tidbcloud/system-variables#tidb_multi_statement_mode-new-in-v4011)有効にする必要があります。
-   **削除**および**更新**操作では、1 つのフィールドをキーとして指定する必要があります。たとえば、 `Delete Key` `id`に設定されます。これは`DELETE FROM table WHERE id = ${item.id}`を実行するのと同じです。現在、**削除操作**と**更新**操作では 1 つのキーの指定のみがサポートされています。
-   **挿入**および**更新**操作の場合、[**列**] フィールドにカンマ区切りのリストを指定する必要があり、フィールド名は入力項目のプロパティと同じである必要があります。
