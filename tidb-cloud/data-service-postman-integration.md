---
title: Run Data App in Postman
summary: Postman でデータ アプリを実行する方法を学びます。
---

# Postmanでデータアプリを実行する {#run-data-app-in-postman}

[郵便配達員](https://www.postman.com/)は、API ライフサイクルを簡素化し、コラボレーションを強化して、より迅速かつ優れた API 開発を実現する API プラットフォームです。

TiDB Cloud [データサービス](https://tidbcloud.com/console/data-service)では、データ アプリを Postman に簡単にインポートし、Postman の豊富なツールを活用して API 開発エクスペリエンスを強化できます。

このドキュメントでは、データ アプリを Postman にインポートする方法と、Postman でデータ アプリを実行する方法について説明します。

## あなたが始める前に {#before-you-begin}

データ アプリを Postman にインポートする前に、次のものがあることを確認してください。

-   [郵便配達員](https://www.postman.com/)アカウント

-   [Postmanデスクトップアプリ](https://www.postman.com/downloads) (オプション)。または、アプリをダウンロードせずに Postman Web バージョンを使用することもできます。

-   少なくとも 1 つの明確に定義された[終点](/tidb-cloud/data-service-manage-endpoint.md)を持つ[データアプリ](/tidb-cloud/data-service-manage-data-app.md)次の要件を満たすエンドポイントのみを Postman にインポートできます。

    -   ターゲット クラスターが選択されました。
    -   エンドポイント パスとリクエスト メソッドが構成されます。
    -   SQL ステートメントが記述されます。

-   データ アプリの場合は[APIキー](/tidb-cloud/data-service-api-key.md#create-an-api-key) 。

## ステップ1.データアプリをPostmanにインポートする {#step-1-import-your-data-app-to-postman}

データ アプリを Postman にインポートするには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、プロジェクトの[**データサービス**](https://tidbcloud.com/console/data-service)ページに移動します。

2.  左側のペインで、対象のデータ アプリの名前をクリックして詳細を表示します。

3.  ページの右上隅にある**「Postman で実行」を**クリックします。インポート手順を示すダイアログが表示されます。

    > **注記：**
    >
    > -   データ アプリに明確に定義されたエンドポイントがない場合 (ターゲット クラスター、パス、リクエスト メソッド、および SQL ステートメントが構成されている場合)、データ アプリに対して**Postman で実行は**無効のままになります。
    > -   Chat2Query データ アプリの場合、 **Postman で実行すること**はできません。

4.  データ アプリのインポートについては、ダイアログに表示される手順に従います。

    1.  好みに応じて、 **「Postman for Web で実行」**または**「Postman Desktop で実行」**のいずれかを選択して Postman ワークスペースを開き、ターゲットワークスペースを選択します。

        -   Postman にログインしていない場合は、画面の指示に従ってまず Postman にログインしてください。
        -   **Postman Desktop で「実行」を**クリックした場合は、画面の指示に従って Postman デスクトップ アプリを起動します。

    2.  Postman のターゲット ワークスペースのページで、左側のナビゲーション メニューの**[インポート] を**クリックします。

    3.  TiDB Cloudダイアログからデータ アプリの URL をコピーし、その URL を Postman に貼り付けてインポートします。

5.  URL を貼り付けると、Postman はデータ アプリを新しい[コレクション](https://learning.postman.com/docs/collections/collections-overview)として自動的にインポートします。コレクションの名前は`TiDB Data Service - <Your App Name>`形式になります。

    コレクションでは、展開されたエンドポイントは**[展開済み]**フォルダーの下にグループ化され、展開されていないエンドポイントは**[下書き]**フォルダーの下にグループ化されます。

## ステップ2. PostmanでデータアプリAPIキーを設定する {#step-2-configure-your-data-app-api-key-in-postman}

インポートしたデータ アプリを Postman で実行する前に、次のように Postman でデータ アプリの API キーを構成する必要があります。

1.  Postman の左側のナビゲーション メニューで`TiDB Data Service - <Your App Name>`クリックすると、右側にタブが開きます。
2.  `TiDB Data Service - <Your App Name>`タブの下にある**変数**タブをクリックします。
3.  変数テーブルの**「現在の値」**列に、データ アプリの公開キーと秘密キーを入力します。
4.  `TiDB Data Service - <Your App Name>`タブの右上隅にある**[保存]**をクリックします。

## ステップ3. Postmanでデータアプリを実行する {#step-3-run-data-app-in-postman}

Postman でデータ アプリを実行するには、次の手順を実行します。

1.  Postman の左側のナビゲーション ペインで、 **[デプロイ済み]**または**[下書き]**フォルダーを展開し、エンドポイント名をクリックして右側にタブを開きます。

2.  `<Your Endpoint Name>`タブでは、次のようにエンドポイントを呼び出すことができます。

    -   パラメータのないエンドポイントの場合は、 **[送信] を**クリックして直接呼び出すことができます。
    -   パラメータを持つエンドポイントの場合は、まずパラメータ値を入力してから、 **「送信」**をクリックする必要があります。

        -   `GET`または`DELETE`リクエストの場合は、**クエリ パラメータ**テーブルにパラメータ値を入力します。
        -   `POST`または`PUT`リクエストの場合は、 **[Body]**タブをクリックし、パラメータ値を JSON オブジェクトとして入力します。TiDB TiDB Cloud Data Service のエンドポイントで**バッチ操作**が有効になっている場合は、パラメータ値を JSON オブジェクトの配列として`items`フィールドに入力します。

3.  下のペインで応答を確認します。

4.  異なるパラメータ値でエンドポイントを再度呼び出す場合は、パラメータ値を適宜編集し、再度**「送信」**をクリックします。

Postman の使用方法の詳細については、 [Postman ドキュメント](https://learning.postman.com/docs)参照してください。

## データアプリの新たな変更に対応する {#deal-with-new-changes-in-data-app}

データ アプリが Postman にインポートされた後、 TiDB Cloudデータ サービスはデータ アプリの新しい変更を Postman に自動的に同期しません。

新しい変更を Postman に反映させたい場合は、もう一度[インポートプロセスに従う](#step-1-import-your-data-app-to-postman)実行する必要があります。コレクション名は Postman ワークスペース内で一意であるため、最新のデータ アプリを使用して以前にインポートしたものを置き換えるか、最新のデータ アプリを新しいコレクションとしてインポートすることができます。

また、データ アプリを再インポートした後は、Postman で再度[新しくインポートしたアプリのAPIキーを設定します](#step-2-configure-your-data-app-api-key-in-postman)実行する必要があります。
