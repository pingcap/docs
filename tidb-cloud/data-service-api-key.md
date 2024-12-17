---
title: API Keys in Data Service
summary: データ アプリの API キーを作成、編集、削除する方法を学びます。
---

# データサービスの API キー {#api-keys-in-data-service}

TiDB Cloud Data API は[基本認証](https://en.wikipedia.org/wiki/Basic_access_authentication)と[ダイジェスト認証](https://en.wikipedia.org/wiki/Digest_access_authentication)両方をサポートします。

-   [基本認証](https://en.wikipedia.org/wiki/Basic_access_authentication)暗号化されていない base64 エンコードを使用して公開鍵と秘密鍵を送信します。HTTPS により、送信のセキュリティが確保されます。詳細については、 [RFC 7617 - 「基本」HTTP 認証スキーム](https://datatracker.ietf.org/doc/html/rfc7617)参照してください。
-   [ダイジェスト認証](https://en.wikipedia.org/wiki/Digest_access_authentication) 、ネットワーク送信前に公開鍵、秘密鍵、サーバーから提供された nonce 値、HTTP メソッド、および要求された URI をハッシュすることにより、追加のセキュリティレイヤーを提供します。これにより、秘密鍵が暗号化され、プレーン テキストで送信されることが防止されます。詳細については、 [RFC 7616 - HTTP ダイジェスト アクセス認証](https://datatracker.ietf.org/doc/html/rfc7616)参照してください。

> **注記：**
>
> Data Service の Data API キーは、 [TiDB CloudAPI](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication)で使用されるキーとは異なります。Data API キーはTiDB Cloudクラスターのデータにアクセスするために使用されますが、 TiDB Cloud API キーはプロジェクト、クラスター、バックアップ、復元、インポートなどのリソースを管理するために使用されます。

## API キーの概要 {#api-key-overview}

-   API キーには、認証に必要なユーザー名とパスワードとして機能する公開キーと秘密キーが含まれています。秘密キーは、キーの作成時にのみ表示されます。
-   各 API キーは 1 つのデータ アプリにのみ属し、 TiDB Cloudクラスター内のデータにアクセスするために使用されます。
-   すべてのリクエストで正しい API キーを指定する必要があります。そうしないと、 TiDB Cloud は`401`エラーで応答します。

## レート制限 {#rate-limiting}

リクエストクォータには、次のレート制限が適用されます。

-   TiDB Cloudデータ サービスでは、デフォルトで API キーごとに 1 分あたり最大 100 件のリクエスト (rpm) が許可されます。

    API キーのレート制限は、キーを[作成する](#create-an-api-key)するときに編集できます。サポートされる値の範囲は`1` ～ [編集](#edit-an-api-key)です。1 分あたりのリクエスト数がレート制限を超えると、API は`429`を返します。API キーごとに 1000 rpm を超えるクォータ`1000`取得するには、サポート チームに[リクエストを送信する](https://tidb.support.pingcap.com/)連絡ください。

    各 API リクエストは、制限に関する次のヘッダーを返します。

    -   `X-Ratelimit-Limit-Minute` : 1 分あたりに許可されるリクエストの数。
    -   `X-Ratelimit-Remaining-Minute` : 現在の 1 分間の残りのリクエスト数。 `0`に達すると、API は`429`エラーを返し、レート制限を超えたことを示します。
    -   `X-Ratelimit-Reset` : 現在のレート制限がリセットされる時間（秒）。

    レート制限を超えると、次のようなエラー応答が返されます。

    ```bash
    HTTP/2 429
    date: Mon, 05 Sep 2023 02:50:52 GMT
    content-type: application/json
    content-length: 420
    x-debug-trace-id: 202309040250529dcdf2055e7b2ae5e9
    x-ratelimit-reset: 8
    x-ratelimit-remaining-minute: 0
    x-ratelimit-limit-minute: 10
    x-kong-response-latency: 1
    server: kong/2.8.1

    {"type":"","data":{"columns":[],"rows":[],"result":{"latency":"","row_affect":0,"code":49900007,"row_count":0,"end_ms":0,"limit":0,"message":"API key rate limit exceeded. The limit can be increased up to 1000 requests per minute per API key in TiDB Cloud console. For an increase in quota beyond 1000 rpm, please contact us: https://tidb.support.pingcap.com/","start_ms":0}}}
    ```

-   TiDB Cloudデータ サービスでは、Chat2Query データ アプリごとに 1 日あたり最大 100 件のリクエストが許可されます。

## API キーの有効期限 {#api-key-expiration}

デフォルトでは、API キーに有効期限はありません。ただし、セキュリティを考慮して、キーを[作成する](#create-an-api-key)または[編集](#edit-an-api-key)アップグレードするときに API キーの有効期限を指定できます。

-   API キーは有効期限前のみ有効です。有効期限が切れると、そのキーを使用するすべてのリクエストは`401`エラーで失敗し、応答は次のようになります。

    ```bash
    HTTP/2 401
    date: Mon, 05 Sep 2023 02:50:52 GMT
    content-type: application/json
    content-length: 420
    x-debug-trace-id: 202309040250529dcdf2055e7b2ae5e9
    x-kong-response-latency: 1
    server: kong/2.8.1

    {"data":{"result":{"start_ms":0,"end_ms":0,"latency":"","row_affect":0,"limit":0,"code":49900002,"message":"API Key is no longer valid","row_count":0},"columns":[],"rows":[]},"type":""}
    ```

-   API キーを手動で期限切れにすることもできます。詳細な手順については、 [APIキーの有効期限切れ](#expire-an-api-key)と[すべてのAPIキーの有効期限が切れる](#expire-all-api-keys)参照してください。API キーを手動で期限切れにすると、有効期限は直ちに有効になります。

-   対象のデータ アプリの**認証**領域で、API キーのステータスと有効期限を確認できます。

-   有効期限が切れると、API キーを再度有効化したり編集したりすることはできません。

## APIキーを管理する {#manage-api-keys}

次のセクションでは、データ アプリの API キーを作成、編集、削除、期限切れにする方法について説明します。

### APIキーを作成する {#create-an-api-key}

データ アプリの API キーを作成するには、次の手順を実行します。

1.  プロジェクトの[**データサービス**](https://tidbcloud.com/console/data-service)ページに移動します。

2.  左側のペインで、対象のデータ アプリの名前をクリックして詳細を表示します。

3.  **認証**領域で、 **「API キーの作成」を**クリックします。

4.  **[API キーの作成]**ダイアログ ボックスで、次の操作を行います。

    1.  (オプション) API キーの説明を入力します。

    2.  API キーのロールを選択します。

        このロールは、API キーがデータ アプリにリンクされたクラスターにデータを読み書きできるかどうかを制御するために使用されます`ReadOnly`または`ReadAndWrite`ロールを選択できます。

        -   `ReadOnly` : API キーは`SELECT` 、 `SHOW` 、 `USE` 、 `DESC` 、 `EXPLAIN`ステートメントなどのデータのみを読み取ることができます。
        -   `ReadAndWrite` : API キーによるデータの読み取りと書き込みを許可します。この API キーを使用して、DML ステートメントや DDL ステートメントなどのすべての SQL ステートメントを実行できます。

    3.  (オプション) API キーに必要なレート制限を設定します。

        1 分あたりのリクエスト数がレート制限を超えると、API は`429`エラーを返します。API キーごとに 1 分あたり 1000 リクエスト (rpm) を超えるクォータを取得するには、サポート チームに[リクエストを送信する](https://tidb.support.pingcap.com/)連絡してください。

    4.  (オプション) API キーの有効期限を設定します。

        デフォルトでは、API キーの有効期限はありません。API キーの有効期限`Days`指定する場合は、 **[有効期限]**をクリックし、時間単位 ( `Minutes` 、または`Months` ) を選択して、時間単位に必要な数値を入力します。

5.  **「次へ」**をクリックします。公開鍵と秘密鍵が表示されます。

    秘密鍵をコピーして安全な場所に保存したことを確認してください。このページを離れると、完全な秘密鍵を再度取得できなくなります。

6.  **「完了」**をクリックします。

### APIキーを編集する {#edit-an-api-key}

> **注記**：
>
> 期限切れのキーは編集できません。

API キーの説明またはレート制限を編集するには、次の手順を実行します。

1.  プロジェクトの[**データサービス**](https://tidbcloud.com/console/data-service)ページに移動します。
2.  左側のペインで、対象のデータ アプリの名前をクリックして詳細を表示します。
3.  **[認証]**領域で、 **[アクション**] 列を見つけて、変更する API キー行で**[...]** &gt; **[編集]**をクリックします。
4.  API キーの説明、ロール、レート制限、または有効期限を更新します。
5.  **[更新]**をクリックします。

### APIキーを削除する {#delete-an-api-key}

> **注記：**
>
> API キーを削除する前に、その API キーがどのデータ アプリでも使用されていないことを確認してください。

データ アプリの API キーを削除するには、次の手順を実行します。

1.  プロジェクトの[**データサービス**](https://tidbcloud.com/console/data-service)ページに移動します。
2.  左側のペインで、対象のデータ アプリの名前をクリックして詳細を表示します。
3.  **API キー**領域で、**アクション**列を見つけて、削除する API キー行で**...** &gt;**削除を**クリックします。
4.  表示されたダイアログボックスで削除を確認します。

### APIキーの有効期限切れ {#expire-an-api-key}

> **注記**：
>
> 期限切れのキーを期限切れにすることはできません。

データ アプリの API キーを期限切れにするには、次の手順を実行します。

1.  プロジェクトの[**データサービス**](https://tidbcloud.com/console/data-service)ページに移動します。
2.  左側のペインで、対象のデータ アプリの名前をクリックして詳細を表示します。
3.  **[認証]**領域で、 **[アクション**] 列を見つけて、期限切れにする API キーの行で**[...]** &gt; **[今すぐ期限切れ]**をクリックします。
4.  表示されたダイアログボックスで有効期限を確認します。

### すべてのAPIキーの有効期限が切れる {#expire-all-api-keys}

データ アプリのすべての API キーを期限切れにするには、次の手順を実行します。

1.  プロジェクトの[**データサービス**](https://tidbcloud.com/console/data-service)ページに移動します。
2.  左側のペインで、対象のデータ アプリの名前をクリックして詳細を表示します。
3.  **認証**領域で、 **「すべて期限切れ」**をクリックします。
4.  表示されたダイアログボックスで有効期限を確認します。
