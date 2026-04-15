---
title: Run Data App in Postman
summary: Postmanでデータアプリを実行する方法を学びましょう。
---

# Postmanでデータアプリを実行する {#run-data-app-in-postman}

[郵便配達人](https://www.postman.com/)API ライフサイクルを簡素化し、コラボレーションを強化してより迅速で優れた API 開発を実現する API プラットフォームです。

TiDB Cloudデータ [データサービス](https://tidbcloud.com/project/data-service)では、データアプリをPostmanに簡単にインポートし、Postmanの豊富なツールを活用してAPI開発体験を向上させることができます。

このドキュメントでは、データアプリをPostmanにインポートする方法と、Postmanでデータアプリを実行する方法について説明します。

## 始める前に {#before-you-begin}

Postmanにデータアプリをインポートする前に、以下のものを用意してください。

-   [郵便配達人](https://www.postman.com/)アカウント

-   [Postmanデスクトップアプリ](https://www.postman.com/downloads)(オプション)。あるいは、アプリをダウンロードせずに Postman Web バージョンを使用することもできます。

-   明確に定義された[終点](/tidb-cloud/data-service-manage-endpoint.md)が少なくとも 1 つある[データアプリ](/tidb-cloud/data-service-manage-data-app.md)。次の要件を満たすエンドポイントのみを Postman にインポートできます。

    -   対象のTiDB Cloud Starterインスタンスが選択されました。
    -   エンドポイントパスとリクエストメソッドが設定されました。
    -   SQL文が記述されました。

-   データアプリ用の[APIキー](/tidb-cloud/data-service-api-key.md#create-an-api-key)。

## ステップ1. データアプリをPostmanにインポートする {#step-1-import-your-data-app-to-postman}

データアプリをPostmanにインポートするには、以下の手順に従ってください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、プロジェクトの[**データサービス**](https://tidbcloud.com/project/data-service)ページに移動します。

2.  左側のペインで、対象のデータアプリの名前をクリックすると、その詳細が表示されます。

3.  ページ右上隅にある**「Postmanで実行」**をクリックします。インポート手順が表示されたダイアログが表示されます。

    > **注記：**
    >
    > -   データアプリに明確なエンドポイント（ターゲットとなるTiDB Cloud Starterインスタンス、パス、リクエストメソッド、SQLステートメントが構成されていること）が設定されていない場合、データアプリの**Postmanでの実行は**無効のままになります。
    > -   Chat2Queryデータアプリの場合、 **Postmanでの実行は**利用できません。

4.  データアプリのインポートに関するダイアログに表示される手順に従ってください。

    1.  お好みに応じて、 **「Postman for Webで実行」**または**「Postman Desktopで実行」**を選択してPostmanワークスペースを開き、次に目的のワークスペースを選択してください。

        -   Postmanにログインしていない場合は、画面の指示に従ってまずPostmanにログインしてください。
        -   **「Postmanデスクトップで実行」を**クリックした場合は、画面の指示に従ってPostmanデスクトップアプリを起動してください。

    2.  Postmanで目的のワークスペースのページで、左側のナビゲーションメニューにある**「インポート」を**クリックします。

    3.  TiDB CloudダイアログからデータアプリのURLをコピーし、そのURLをPostmanに貼り付けてインポートします。

5.  URLを貼り付けると、Postmanはデータアプリを新しい[コレクション](https://learning.postman.com/docs/collections/collections-overview)として自動的にインポートします。コレクション名は`TiDB Data Service - <Your App Name>`形式です。

    コレクション内では、デプロイ済みのエンドポイントは**「Deployed」**フォルダーに、デプロイされていないエンドポイントは**「Draft」**フォルダーにグループ化されます。

## ステップ2. PostmanでデータアプリAPIキーを設定します {#step-2-configure-your-data-app-api-key-in-postman}

Postmanでインポートしたデータアプリを実行する前に、PostmanでデータアプリのAPIキーを次のように設定する必要があります。

1.  Postman の左側のナビゲーション メニューで`TiDB Data Service - <Your App Name>`をクリックすると、右側にタブが開きます。
2.  `TiDB Data Service - <Your App Name>`タブの下にある**[変数]**タブをクリックします。
3.  変数テーブルの**「現在の値」**列に、データアプリの公開鍵と秘密鍵を入力してください。
4.  `TiDB Data Service - <Your App Name>`タブの右上隅にある**[保存]**をクリックします。

## ステップ3. Postmanでデータアプリを実行する {#step-3-run-data-app-in-postman}

Postmanでデータアプリを実行するには、以下の手順に従ってください。

1.  Postmanの左側のナビゲーションペインで、 **「デプロイ済み」**または**「ドラフト」**フォルダーを展開し、エンドポイント名をクリックして右側にタブを開きます。

2.  `<Your Endpoint Name>`タブでは、次のようにエンドポイントを呼び出すことができます。

    -   パラメータのないエンドポイントの場合は、 **「送信」**をクリックして直接呼び出すことができます。
    -   パラメータ付きのエンドポイントの場合は、まずパラメータ値を入力してから**「送信」**をクリックする必要があります。

        -   `GET`または`DELETE`リクエストの場合は、**クエリパラメータ**テーブルのパラメータ値を入力してください。
        -   `POST`または`PUT`リクエストの場合は、 **[本文]**タブをクリックし、パラメーター値を JSON オブジェクトとして入力します。TiDB TiDB Cloud Data Service のエンドポイントで**バッチ操作が**有効になっている場合は、パラメーター値を JSON オブジェクトの配列として`items`フィールドに入力します。

3.  下部のペインで応答を確認してください。

4.  異なるパラメータ値でエンドポイントを再度呼び出したい場合は、パラメータ値を適切に編集してから、再度**「送信」**をクリックしてください。

Postman の使用法の詳細については、 [Postmanのドキュメント](https://learning.postman.com/docs)を参照してください。

## データアプリの新しい変更点に対応する {#deal-with-new-changes-in-data-app}

データアプリがPostmanにインポートされた後、 TiDB Cloud Data Serviceはデータアプリの新しい変更をPostmanに自動的に同期しません。

Postmanに新しい変更を反映させるには、 再度[輸入プロセスに従う](#step-1-import-your-data-app-to-postman)必要があります。Postmanワークスペースではコレクション名が一意であるため、最新のデータアプリを使用して以前にインポートしたものを置き換えるか、最新のデータアプリを新しいコレクションとしてインポートすることができます。

また、Data App を再インポートした後、Postman で[新しくインポートしたアプリのAPIキーを設定します。](#step-2-configure-your-data-app-api-key-in-postman)
