---
title: Integrate a Data App with Third-Party Tools
summary: TiDB Cloudコンソールで、 TiDB CloudデータアプリをGPTやDifyなどのサードパーティツールと統合する方法を学びましょう。
---

# データアプリをサードパーティツールと統合する {#integrate-a-data-app-with-third-party-tools}

データアプリにサードパーティ製ツールを統合することで、サードパーティ製ツールが提供する高度な自然言語処理機能と人工知能（AI）機能をアプリケーションに組み込むことができます。この統合により、アプリケーションはより複雑なタスクを実行し、インテリジェントなソリューションを提供できるようになります。

このドキュメントでは、TiDB CloudコンソールでデータアプリをGPTやDifyなどのサードパーティツールと統合する方法について説明します。

## データアプリをGPTと統合する {#integrate-your-data-app-with-gpts}

データアプリを[GPT](https://openai.com/blog/introducing-gpts)と統合することで、アプリケーションにインテリジェントな機能を追加できます。

データアプリをGPTと統合するには、以下の手順を実行してください。

1.  プロジェクトの[**Data Service**](https://tidbcloud.com/project/data-service)ページに移動します。

2.  左側のペインで、対象のデータアプリを見つけ、対象のデータアプリの名前をクリックし、次に**「統合」**タブをクリックします。

3.  **「GPTとの統合」**領域で、 **「コンフィグレーションを取得」**をクリックします。

    ![Get Configuration](/media/tidb-cloud/data-service/GPTs1.png)

4.  表示されたダイアログボックスには、以下の項目が表示されます。

    ａ． **API 仕様 URL** : データ アプリの OpenAPI 仕様の URL をコピーします。詳細については、 [OpenAPI仕様を使用する](/tidb-cloud/data-service-manage-data-app.md#use-the-openapi-specification)参照してください。

    b. **API キー**: データ アプリの API キーを入力します。 API キーをまだ持っていない場合は、 **「API キーの作成**」をクリックして作成します。詳細については、 [APIキーを作成する](/tidb-cloud/data-service-api-key.md#create-an-api-key)参照してください。

    c. **APIキーエンコード**：提供したAPIキーに相当するbase64エンコードされた文字列をコピーします。

    ![GPTs Dialog Box](/media/tidb-cloud/data-service/GPTs2.png)

5.  コピーしたAPI仕様のURLとエンコードされたAPIキーをGPT構成で使用してください。

## データアプリをDifyと連携させましょう {#integrate-your-data-app-with-dify}

データアプリを[Dify](https://dify.ai/)と統合することで、ベクトル距離計算、高度な類似性検索、ベクトル解析などのインテリジェントな機能を追加し、アプリケーションを強化できます。

データアプリをDifyと連携させるには、 [GPT統合](#integrate-your-data-app-with-gpts)の場合と同じ手順に従ってください。唯一の違いは、 **[連携]**タブの**[Difyとの連携]**エリアで**[コンフィグレーションを取得]を**クリックする必要がある点です。
