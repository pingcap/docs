---
title: Run Data App in Postman
summary: Learn how to run your Data App in Postman.
---

# Postman でデータ アプリを実行する {#run-data-app-in-postman}

[郵便屋さん](https://www.postman.com/)は、API ライフサイクルを簡素化し、コラボレーションを強化して、より迅速で優れた API 開発を実現する API プラットフォームです。

TiDB Cloud [データサービス](https://tidbcloud.com/console/data-service)では、データ アプリを Postman に簡単にインポートし、Postman の広範なツールを活用して API 開発エクスペリエンスを強化できます。

このドキュメントでは、データ アプリを Postman にインポートする方法と、データ アプリを Postman で実行する方法について説明します。

## あなたが始める前に {#before-you-begin}

Data App を Postman にインポートする前に、次のことを確認してください。

-   [郵便屋さん](https://www.postman.com/)アカウント

-   A [ポストマンデスクトップアプリ](https://www.postman.com/downloads) (オプション)。あるいは、アプリをダウンロードせずに Postman Web バージョンを使用することもできます。

-   明確に定義された[終点](/tidb-cloud/data-service-manage-endpoint.md)が少なくとも 1 つある[データアプリ](/tidb-cloud/data-service-manage-data-app.md) 。次の要件を満たすエンドポイントのみを Postman にインポートできます。

    -   ターゲットクラスターが選択されます。
    -   エンドポイントのパスとリクエスト方法が構成されます。
    -   SQL ステートメントが書き込まれます。

-   データ アプリの場合は[APIキー](/tidb-cloud/data-service-api-key.md#create-an-api-key) 。

## ステップ 1. データ アプリを Postman にインポートする {#step-1-import-your-data-app-to-postman}

Data App を Postman にインポートするには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、プロジェクトの[**データサービス**](https://tidbcloud.com/console/data-service)ページに移動します。

2.  左側のペインで、ターゲット データ アプリの名前をクリックして詳細を表示します。

3.  ページの右上隅にある**[Postman で実行]**をクリックします。インポート手順を示すダイアログが表示されます。

    > **注記：**
    >
    > -   データ アプリに明確に定義されたエンドポイントがない場合 (ターゲット クラスター、パス、リクエスト メソッド、および SQL ステートメントが構成されている場合)、データ アプリに対して**Postman での実行は**無効のままになります。
    > -   Chat2Query データ アプリの場合、 **Postman で実行は**利用できません。

4.  データ アプリのインポートのダイアログに表示される手順に従います。

    1.  好みに応じて、 **「Postman for Web で実行」**または**「Postman デスクトップで実行」**を選択して Postman ワークスペースを開き、ターゲット ワークスペースを選択します。

        -   Postman にログインしていない場合は、まず画面上の指示に従って Postman にログインします。
        -   **[Postman デスクトップで実行]**をクリックした場合は、画面上の指示に従って Postman デスクトップ アプリを起動します。

    2.  Postman のターゲット ワークスペースのページで、左側のナビゲーション メニューの**[インポート]**をクリックします。

    3.  TiDB Cloudダイアログから Data App URL をコピーし、インポートのためにその URL を Postman に貼り付けます。

5.  URL を貼り付けると、Postman はデータ アプリを新しい[コレクション](https://learning.postman.com/docs/collections/collections-overview)として自動的にインポートします。コレクションの名前は`TiDB Data Service - <Your App Name>`形式です。

    コレクションでは、デプロイされたエンドポイントは**Deployed**フォルダーの下にグループ化され、デプロイされていないエンドポイントは**Draft**フォルダーの下にグループ化されます。

## ステップ 2. Postman で Data App API キーを構成する {#step-2-configure-your-data-app-api-key-in-postman}

インポートされたデータ アプリを Postman で実行する前に、Postman でデータ アプリの API キーを次のように構成する必要があります。

1.  Postman の左側のナビゲーション メニューで、 `TiDB Data Service - <Your App Name>`をクリックして右側にそのタブを開きます。
2.  `TiDB Data Service - <Your App Name>`タブの下で**「変数」**タブをクリックします。
3.  変数テーブルの**[現在の値]**列にデータ アプリの公開キーと秘密キーを入力します。
4.  `TiDB Data Service - <Your App Name>`タブの右上隅にある**[保存]**をクリックします。

## ステップ 3. Postman でデータ アプリを実行する {#step-3-run-data-app-in-postman}

Postman でデータ アプリを実行するには、次の手順を実行します。

1.  Postman の左側のナビゲーション ウィンドウで、 **[Deployed]**フォルダーまたは**[Draft]**フォルダーを展開し、エンドポイント名をクリックして右側にそのタブを開きます。

2.  `<Your Endpoint Name>`タブで、次のようにエンドポイントを呼び出すことができます。

    -   パラメーターのないエンドポイントの場合は、 **「送信」**をクリックしてエンドポイントを直接呼び出すことができます。
    -   パラメーターを含むエンドポイントの場合は、最初にパラメーター値を入力してから、 **[送信]**をクリックする必要があります。

        -   `GET`または`DELETE`リクエストの場合、 **Query Params**テーブルにパラメータ値を入力します。
        -   `POST`または`PUT`リクエストの場合は、 **「本文」**タブをクリックし、パラメータ値を JSON オブジェクトとして入力します。 TiDB Cloud Data Service のエンドポイントに対して**バッチ操作が**有効になっている場合は、パラメーター値を JSON オブジェクトの配列として入力します。

3.  下部ペインで応答を確認します。

4.  異なるパラメーター値を使用してエンドポイントを再度呼び出す場合は、パラメーター値を編集して、再度**[送信]**をクリックします。

Postman の使用法の詳細については、 [郵便配達員のドキュメント](https://learning.postman.com/docs)を参照してください。

## Data App の新しい変更に対処する {#deal-with-new-changes-in-data-app}

データ アプリが Postman にインポートされた後、 TiDB Cloudデータ サービスはデータ アプリの新しい変更を Postman に自動的に同期しません。

新しい変更を Postman に反映させたい場合は、もう一度[インポートプロセスに従ってください](#step-1-import-your-data-app-to-postman)実行する必要があります。コレクション名は Postman ワークスペース内で一意であるため、最新のデータ アプリを使用して以前にインポートしたデータ アプリを置き換えるか、最新のデータ アプリを新しいコレクションとしてインポートできます。

また、Data App を再インポートした後は、Postman で再度[新しくインポートされたアプリの API キーを構成する](#step-2-configure-your-data-app-api-key-in-postman)を行う必要があります。
