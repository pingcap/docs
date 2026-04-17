---
title: Integrate TiDB Cloud with n8n
summary: n8nにおけるTiDB Cloudノードの使い方を学びましょう。
---

# TiDB Cloudとn8nを統合する {#integrate-tidb-cloud-with-n8n}

[n8n](https://n8n.io/)は拡張可能なワークフロー自動化ツールです。[フェアコード](https://faircode.io/)配布モデルを採用しているため、n8nは常にソースコードが公開されており、セルフホストが可能で、独自の関数、ロジック、アプリケーションを追加できます。

このドキュメントでは、自動ワークフローの構築方法を紹介します。具体的には、 TiDB Cloud Starterインスタンスを作成し、Hacker NewsのRSSフィードを収集してTiDBに保存し、概要メールを送信します。

> **注記：**
>
> このドキュメントの手順は、 TiDB Cloud Starterインスタンスに加えて、 TiDB Cloud Essentialインスタンスでも適用できます。

## 前提条件： TiDB Cloud APIキーを取得する {#prerequisites-get-tidb-cloud-api-key}

1.  [TiDB Cloudコンソール](https://tidbcloud.com)では、左上隅のコンボボックスを使用して、対象の組織に切り替えてください。
2.  左側のナビゲーションペインで、 **[組織設定]** &gt; **[APIキー]**をクリックします。
3.  **APIキーの**ページで、 **「APIキーを作成」**をクリックします。
4.  APIキーの説明を入力し、 **「次へ」**をクリックしてください。
5.  作成したAPIキーをコピーしてn8nで後で使用するようにし、 **「完了」**をクリックしてください。

詳細については、 [TiDB Cloud APIの概要](https://docs.pingcap.com/api/tidb-cloud-api-overview)参照してください。

## ステップ1：n8nをインストールする {#step-1-install-n8n}

セルフホスティング型のn8nをインストールする方法は2つあります。ご自身に合った方法をお選びください。

<SimpleTab>
<div label="npm">

1.  作業スペースに[Node.js](https://nodejs.org/en/download/)をインストールしてください。
2.  `npx`から n8n をダウンロードして起動します。

    ```shell
    npx n8n
    ```

</div>
<div label="Docker">

1.  ワークスペースに[ドッカー](https://www.docker.com/products/docker-desktop)をインストールします。
2.  `docker`から n8n をダウンロードして起動します。

    ```shell
    docker run -it --rm --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n
    ```

</div>
</SimpleTab>

n8nを起動したら、 [localhost:5678](http://localhost:5678)にアクセスしてn8nを試してみてください。

## ステップ2：n8nにTiDB Cloudノードをインストールする {#step-2-install-tidb-cloud-node-in-n8n}

TiDB Cloudノードは、npmリポジトリでは`n8n-nodes-tidb-cloud`という名前です。n8nでTiDB Cloudを制御するには、このノードを手動でインストールする必要があります。

1.  [localhost:5678](http://localhost:5678)ページで、n8nをセルフホスティングするためのオーナーアカウントを作成します。
2.  **設定**&gt;**コミュニティノード**に移動してください。
3.  **「コミュニティノードをインストール」**をクリックしてください。
4.  **npmパッケージ名**フィールドに`n8n-nodes-tidb-cloud`と入力します。
5.  **「インストール」**をクリックしてください。

その後、**ワークフロー**の検索バーで**TiDB Cloud**ノードを検索し、ワークスペースにドラッグすることでTiDB Cloudノードを使用できます。

## ステップ3：ワークフローを構築する {#step-3-build-your-workflow}

このステップでは、 **「実行」**ボタンをクリックしたときに、TiDBにデータを挿入する新しいワークフローを作成します。

この使用例のワークフローでは、以下のノードを使用します。

-   [スケジュールトリガー](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.scheduletrigger/)
-   [RSSを読む](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.rssfeedread/)
-   [コード](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.code/)
-   [Gmail](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.gmail/)
-   [TiDB Cloudノード](https://www.npmjs.com/package/n8n-nodes-tidb-cloud)

最終的なワークフローは次の画像のようになります。

![img](/media/tidb-cloud/integration-n8n-workflow-rss.jpg)

### （オプション） TiDB Cloud Starterインスタンスを作成する {#optional-create-a-tidb-cloud-starter-instance}

TiDB Cloud Starterインスタンスをお持ちでない場合は、このノードを使用してインスタンスを作成できます。そうでない場合は、この操作をスキップしても構いません。

1.  **ワークフロー**パネルに移動し、 **「ワークフローの追加」**をクリックします。
2.  新しいワークフローワークスペースで、右上隅の**「+」**をクリックし、 **「すべての**フィールド」を選択します。
3.  `TiDB Cloud`を検索して、ワークスペースにドラッグします。
4.  TiDB Cloudノードの認証情報（TiDB Cloud APIキー）を入力してください。
5.  **プロジェクト**一覧から、プロジェクトを選択してください。
6.  **操作**リストで、 `Create Serverless Cluster`を選択します。
7.  **「クラスタ名」**ボックスに、 TiDB Cloud Starterインスタンスの名前を入力します。
8.  **リージョン**リストから地域を選択してください。
9.  **パスワード**欄に、 TiDB Cloud Starterインスタンスへのログインに使用するパスワードを入力してください。
10. ノードを実行するには、 **「ノードを実行」**をクリックしてください。

> **注記：**
>
> 新しいTiDB Cloud Starterインスタンスを作成するには、数秒かかります。

### ワークフローを作成する {#create-a-workflow}

#### ワークフローの開始点として手動トリガーを使用する {#use-a-manual-trigger-as-the-workflow-s-starter}

1.  ワークフローがまだ作成されていない場合は、**ワークフロー**パネルに移動して、 **「最初から作成」**をクリックしてください。既にワークフローを作成している場合は、この手順をスキップしてください。
2.  右上隅の**「+」**をクリックして、 `schedule trigger`を検索します。
3.  手動トリガーノードをワークスペースにドラッグし、ノードをダブルクリックします。**パラメーター**ダイアログが表示されます。
4.  ルールを以下のように設定してください。

    -   **トリガー間隔**： `Days`
    -   **トリガー間の日数**： `1`
    -   **時刻**： `8am`
    -   **トリガー時刻**: `0`

このトリガーは、毎朝午前8時にワークフローを実行します。

#### データ挿入に使用するテーブルを作成します。 {#create-a-table-used-to-insert-data}

1.  手動トリガーノードの右側にある**「+」**をクリックします。

2.  `TiDB Cloud`を検索してワークスペースに追加します。

3.  **パラメーター**ダイアログで、 TiDB Cloudノードの認証情報を入力します。認証情報は、 TiDB Cloud APIキーです。

4.  **プロジェクト**一覧から、プロジェクトを選択してください。

5.  **操作**リストで、 `Execute SQL`を選択します。

6.  TiDB Cloud Starterインスタンスを選択してください。リストに新しいインスタンスが表示されない場合は、インスタンスの作成が完了するまで数分お待ちください。

7.  **ユーザー**一覧からユーザーを選択してください。TiDB Cloudは常にデフォルトユーザーを作成するため、手動で作成する必要はありません。

8.  **データベース**ボックスに`test`と入力します。

9.  データベースのパスワードを入力してください。

10. **SQL**ボックスに、次のSQLを入力してください。

    ```sql
    CREATE TABLE IF NOT EXISTS hacker_news_briefing (creator VARCHAR (200), title TEXT,  link VARCHAR(200), pubdate VARCHAR(200), comments VARCHAR(200), content TEXT, guid VARCHAR (200), isodate VARCHAR(200));
    ```

11. テーブルを作成するには、 **「実行ノード」**をクリックしてください。

#### Hacker NewsのRSSフィードを入手する {#get-the-hacker-news-rss}

1.  TiDB Cloudノードの右側にある**「+」**をクリックします。
2.  `RSS Read`を検索してワークスペースに追加します。
3.  **URL**ボックスに`https://hnrss.org/frontpage`と入力します。

#### TiDBにデータを挿入する {#insert-data-to-tidb}

1.  RSS Readノードの右側にある**「+」**をクリックしてください。
2.  `TiDB Cloud`を検索してワークスペースに追加します。
3.  以前のTiDB Cloudノードで入力した認証情報を選択してください。
4.  **プロジェクト**一覧から、プロジェクトを選択してください。
5.  **操作**リストで、 `Insert`を選択します。
6.  **「クラスタ」** 、 **「ユーザー」** 、 **「データベース」** 、 **「パスワード」**の各ボックスに、それぞれ対応する値を入力してください。
7.  **表**ボックスに、 `hacker_news_briefing`表を入力します。
8.  **「列」**ボックスに`creator, title, link, pubdate, comments, content, guid, isodate`と入力します。

#### メッセージを作成する {#build-message}

1.  RSSフィードの「読む」ノードの右側にある**「+」**をクリックします。
2.  `code`を検索してワークスペースに追加します。
3.  `Run Once for All Items`モードを選択してください。
4.  **JavaScript**ボックスに、以下のコードをコピー＆ペーストしてください。

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

1.  コードノードの右側にある**「+」**をクリックします。
2.  `gmail`を検索してワークスペースに追加します。
3.  Gmail ノードの認証情報を入力します。詳細な手順については、 [n8nドキュメント](https://docs.n8n.io/integrations/builtin/credentials/google/oauth-single-service/)ドキュメントを参照してください。
4.  **リソース**リストで、 `Message`を選択します。
5.  **操作**リストで、 `Send`を選択します。
6.  **「宛先」**欄にメールアドレスを入力してください。
7.  **件名**欄に`Hacker News Briefing`と入力します。
8.  **「メールの種類」**ボックスで、 `HTML`を選択します。
9.  **メッセージ**ボックスで、 `Expression`をクリックし、 `{{ $json["response"] }}`と入力します。

    > **注記：**
    >
    > **メッセージ**ボックスにカーソルを合わせ、**式**パターンを選択する必要があります。

## ステップ4：ワークフローを実行する {#step-4-run-your-workflow}

ワークフローを作成したら、 **「ワークフローの実行」**をクリックしてテスト実行できます。

ワークフローが想定どおりに実行されれば、Hacker Newsの速報メールが届きます。これらのニュースコンテンツはTiDB Cloud Starterインスタンスにログとして記録されるため、紛失の心配はありません。

これで、**ワークフロー**パネルからこのワークフローを有効化できます。このワークフローを使用すると、Hacker Newsのトップページ記事を毎日取得できます。

## TiDB Cloudノードコア {#tidb-cloud-node-core}

### サポート対象のオペレーション {#supported-operations}

TiDB Cloudノードは[通常のノード](https://docs.n8n.io/workflows/nodes/#regular-nodes)として機能し、次の 5 つの操作のみをサポートします。

-   **サーバーレスクラスタの作成**: TiDB Cloud Starterインスタンスを作成します。
-   **SQLの実行**：TiDBでSQL文を実行します。
-   **削除**：TiDB内の行を削除します。
-   **Insert** ：TiDBに行を挿入します。
-   **更新**: TiDB の行を更新します。

### フィールズ {#fields}

各種操作を実行するには、それぞれの必須項目を入力する必要があります。以下に、各操作に対応する項目の説明を示します。

<SimpleTab>
<div label="Create Serverless Cluster">

-   **TiDB CloudAPI の認証情報**: TiDB CloudAPI キーのみをサポートします。 APIキーの作成方法については、 [TiDB Cloud APIキーを取得する](#prerequisites-get-tidb-cloud-api-key)を参照してください。
-   **プロジェクト**： TiDB Cloudプロジェクト名。
-   **操作**: このノードの操作。サポートされているすべての操作については、[サポート対象のオペレーション](#supported-operations)を参照してください。
-   **クラスタ**： TiDB Cloud Starterインスタンスの名前を入力してください。
-   **リージョン**：リージョン名。TiDB Cloud Starterインスタンスをデプロイするリージョンを選択してください。通常は、アプリケーションのデプロイ先に最も近いリージョンを選択してください。
-   **パスワード**：rootパスワード。新しいTiDB Cloud Starterインスタンスのパスワードを設定してください。

</div>
<div label="Execute SQL">

-   **TiDB CloudAPI の認証情報**: TiDB CloudAPI キーのみをサポートします。 APIキーの作成方法については、 [TiDB Cloud APIキーを取得する](#prerequisites-get-tidb-cloud-api-key)を参照してください。
-   **プロジェクト**： TiDB Cloudプロジェクト名。
-   **操作**: このノードの操作。サポートされているすべての操作については、[サポート対象のオペレーション](#supported-operations)を参照してください。
-   **クラスタ**： TiDB Cloud Starterインスタンスの名前。既存のインスタンスを1つ選択してください。
-   **パスワード**： TiDB Cloud Starterインスタンスのパスワード。
-   **ユーザー**： TiDB Cloud Starterインスタンスのユーザー名。
-   **データベース**：データベース名。
-   **SQL** ：実行するSQL文。

</div>
<div label="Delete">

-   **TiDB CloudAPI の認証情報**: TiDB CloudAPI キーのみをサポートします。 APIキーの作成方法については、 [TiDB Cloud APIキーを取得する](#prerequisites-get-tidb-cloud-api-key)を参照してください。
-   **プロジェクト**： TiDB Cloudプロジェクト名。
-   **操作**: このノードの操作。サポートされているすべての操作については、[支援活動](#supported-operations)を参照してください。
-   **クラスタ**： TiDB Cloud Starterインスタンスの名前。既存のインスタンスを1つ選択してください。
-   **パスワード**： TiDB Cloud Starterインスタンスのパスワード。
-   **ユーザー**： TiDB Cloud Starterインスタンスのユーザー名。
-   **データベース**：データベース名。
-   **テーブル**：テーブル名。 `From list`モードを使用してテーブル名を選択するか、 `Name`モードを使用してテーブル名を手動で入力できます。
-   **削除キー**：データベース内のどの行を削除するかを決定するアイテムのプロパティ名。アイテムとは、あるノードから別のノードに送信されるデータのことです。ノードは、受信データの各アイテムに対してアクションを実行します。n8n のアイテムの詳細については、 [n8nドキュメント](https://docs.n8n.io/workflows/items/)を参照してください。

</div>
<div label="Insert">

-   **TiDB CloudAPI の認証情報**: TiDB CloudAPI キーのみをサポートします。 APIキーの作成方法については、 [TiDB Cloud APIキーを取得する](#prerequisites-get-tidb-cloud-api-key)を参照してください。
-   **プロジェクト**： TiDB Cloudプロジェクト名。
-   **操作**: このノードの操作。サポートされているすべての操作については、[支援活動](#supported-operations)を参照してください。
-   **クラスタ**： TiDB Cloud Starterインスタンスの名前。既存のインスタンスを1つ選択してください。
-   **パスワード**： TiDB Cloud Starterインスタンスのパスワード。
-   **ユーザー**： TiDB Cloud Starterインスタンスのユーザー名。
-   **データベース**：データベース名。
-   **テーブル**：テーブル名。 `From list`モードを使用してテーブル名を選択するか、 `Name`モードを使用してテーブル名を手動で入力できます。
-   **列**：入力項目のプロパティをカンマで区切ったリストで、新しい行の列として使用されます。項目とは、あるノードから別のノードに送信されるデータのことです。ノードは、受信データの各項目に対してアクションを実行します。n8n の項目に関する詳細は、 [n8nドキュメント](https://docs.n8n.io/workflows/items/)を参照してください。

</div>
<div label="Update">

-   **TiDB CloudAPI の認証情報**: TiDB CloudAPI キーのみをサポートします。 APIキーの作成方法については、 [TiDB Cloud APIキーを取得する](#prerequisites-get-tidb-cloud-api-key)を参照してください。
-   **プロジェクト**： TiDB Cloudプロジェクト名。
-   **操作**: このノードの操作。サポートされているすべての操作については、[支援活動](#supported-operations)を参照してください。
-   **クラスタ**： TiDB Cloud Starterインスタンスの名前。既存のインスタンスを1つ選択してください。
-   **パスワード**： TiDB Cloud Starterインスタンスのパスワード。
-   **ユーザー**： TiDB Cloud Starterインスタンスのユーザー名。
-   **データベース**：データベース名。
-   **テーブル**：テーブル名。 `From list`モードを使用してテーブル名を選択するか、 `Name`モードを使用してテーブル名を手動で入力できます。
-   **更新キー**：データベース内のどの行を更新するかを決定するアイテムのプロパティ名。アイテムとは、あるノードから別のノードに送信されるデータのことです。ノードは、受信データの各アイテムに対してアクションを実行します。n8n のアイテムの詳細については、 [n8nドキュメント](https://docs.n8n.io/workflows/items/)を参照してください。
-   **列**：入力項目のプロパティをカンマで区切ったリスト。更新対象の行の列として使用されます。

</div>
</SimpleTab>

### 制限事項 {#limitations}

-   通常、 **SQL実行**操作では1つのSQLステートメントしか実行できません。1つの操作で複数のステートメントを実行する場合は、 [`tidb_multi_statement_mode`](https://docs.pingcap.com/tidbcloud/system-variables#tidb_multi_statement_mode-new-in-v4011)手動で有効にする必要があります。
-   **削除**および**更新**操作では、キーとして1つのフィールドを指定する必要があります。たとえば、 `Delete Key`を`id`に設定すると、 `DELETE FROM table WHERE id = ${item.id}`を実行するのと同等になります。現在、**削除**および**更新**操作では、キーを1つだけ指定できます。
-   **挿入**および**更新**操作の場合、**列**フィールドにカンマ区切りのリストを指定する必要があり、フィールド名は入力項目のプロパティ名と同じでなければなりません。
