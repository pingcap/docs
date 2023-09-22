---
title: API Keys in Data Service
summary: Learn how to create, edit, and delete an API key for a Data App.
---

# データサービスの API キー {#api-keys-in-data-service}

TiDB Cloud Data API は[基本認証](https://en.wikipedia.org/wiki/Basic_access_authentication)と[ダイジェスト認証](https://en.wikipedia.org/wiki/Digest_access_authentication)の両方をサポートします。

-   [基本認証](https://en.wikipedia.org/wiki/Basic_access_authentication)暗号化されていない Base64 エンコードを使用して、公開キーと秘密キーを送信します。 HTTPS により通信のセキュリティが確保されます。詳細については、 [RFC 7617 - 「基本」HTTP 認証スキーム](https://datatracker.ietf.org/doc/html/rfc7617)を参照してください。
-   [ダイジェスト認証](https://en.wikipedia.org/wiki/Digest_access_authentication)ネットワーク送信前に公開キー、秘密キー、サーバー提供の nonce 値、HTTP メソッド、および要求された URI をハッシュすることにより、追加のセキュリティレイヤーを提供します。これにより、秘密キーが暗号化され、平文で送信されるのを防ぎます。詳細については、 [RFC 7616 - HTTP ダイジェスト アクセス認証](https://datatracker.ietf.org/doc/html/rfc7616)を参照してください。

> **注記：**
>
> Data Service の Data API キーは、 [TiDB CloudAPI](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication)で使用されるキーとは異なります。 Data API キーはTiDB Cloudクラスター内のデータにアクセスするために使用され、 TiDB CloudAPI キーはプロジェクト、クラスター、バックアップ、復元、インポートなどのリソースを管理するために使用されます。

## APIキーの概要 {#api-key-overview}

-   API キーには公開キーと秘密キーが含まれており、認証に必要なユーザー名とパスワードとして機能します。秘密キーはキーの作成時にのみ表示されます。
-   各 API キーは 1 つのデータ アプリにのみ属し、 TiDB Cloudクラスター内のデータにアクセスするために使用されます。
-   すべてのリクエストで正しい API キーを指定する必要があります。それ以外の場合、 TiDB Cloud は`401`エラーで応答します。

## レート制限 {#rate-limiting}

リクエスト クォータには、次のようなレート制限が適用されます。

-   TiDB Cloudデータ サービスでは、デフォルトで API キーごとに 1 分あたり最大 100 リクエスト (rpm) が許可されます。

    API キーのレート制限は、キーを[作成する](#create-an-api-key)または[編集](#edit-an-api-key)にするときに編集できます。サポートされる値の範囲は`1` ～ `1000`です。 1 分あたりのリクエストがレート制限を超えると、API は`429`エラーを返します。 API キーごとに 1000 rpm を超える割り当てを取得するには、サポート チームにご[リクエストを送信する](https://support.pingcap.com/hc/en-us/requests/new?ticket_form_id=7800003722519)ください。

    各 API リクエストは、制限に関する次のヘッダーを返します。

    -   `X-Ratelimit-Limit-Minute` : 1 分あたりに許可されるリクエストの数。
    -   `X-Ratelimit-Remaining-Minute` : 現在の 1 分間に残っているリクエストの数。 `0`に達すると、API は`429`エラーを返し、レート制限を超えていることを示します。
    -   `X-Ratelimit-Reset` : 現在のレート制限がリセットされる時間 (秒)。

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

    {"type":"","data":{"columns":[],"rows":[],"result":{"latency":"","row_affect":0,"code":49900007,"row_count":0,"end_ms":0,"limit":0,"message":"API key rate limit exceeded. The limit can be increased up to 1000 requests per minute per API key in TiDB Cloud console. For an increase in quota beyond 1000 rpm, please contact us: https://support.pingcap.com/hc/en-us/requests/new?ticket_form_id=7800003722519","start_ms":0}}}
    ```

-   TiDB Cloudデータ サービスでは、Chat2Query データ アプリごとに 1 日あたり最大 100 件のリクエストが許可されます。

## APIキーを管理する {#manage-api-keys}

次のセクションでは、データ アプリの API キーを作成、編集、削除する方法について説明します。

### APIキーを作成する {#create-an-api-key}

データ アプリの API キーを作成するには、次の手順を実行します。

1.  プロジェクトの[**データサービス**](https://tidbcloud.com/console/data-service)ページに移動します。

2.  左側のペインで、ターゲット データ アプリの名前をクリックして詳細を表示します。

3.  **「認証」**領域で、 **「API キーの作成」を**クリックします。

4.  **[API キーの作成]**ダイアログ ボックスで、次の操作を実行します。

    1.  (オプション) API キーの説明を入力します。

    2.  API キーのロールを選択します。

        このロールは、API キーがデータ アプリにリンクされたクラスターに対してデータの読み取りまたは書き込みを行えるかどうかを制御するために使用されます。 `ReadOnly`または`ReadAndWrite`役割を選択できます。

        -   `ReadOnly` : API キーは`SELECT` 、 `SHOW` 、 `USE` 、 `DESC` 、 `EXPLAIN`ステートメントなどのデータの読み取りのみを許可します。
        -   `ReadAndWrite` : API キーによるデータの読み取りと書き込みを許可します。この API キーを使用して、DML ステートメントや DDL ステートメントなどのすべての SQL ステートメントを実行できます。

    3.  (オプション) API キーに必要なレート制限を設定します。

        1 分あたりのリクエストがレート制限を超えると、API は`429`エラーを返します。 API キーごとに 1 分あたり 1000 リクエスト (rpm) を超える割り当てを取得するには、サポート チームに[リクエストを送信する](https://support.pingcap.com/hc/en-us/requests/new?ticket_form_id=7800003722519)してください。

5.  **「次へ」**をクリックします。公開鍵と秘密鍵が表示されます。

    秘密キーをコピーして安全な場所に保存したことを確認してください。このページを離れると、完全な秘密キーを再度取得することはできなくなります。

6.  **「完了」**をクリックします。

### APIキーを編集する {#edit-an-api-key}

API キーの説明またはレート制限を編集するには、次の手順を実行します。

1.  プロジェクトの[**データサービス**](https://tidbcloud.com/console/data-service)ページに移動します。
2.  左側のペインで、ターゲット データ アプリの名前をクリックして詳細を表示します。
3.  **[API キー]**領域で [**アクション]**列を見つけ、変更する API キー行で**[...]** &gt; **[編集]**をクリックします。
4.  API キーの説明、役割、またはレート制限を更新します。
5.  **「更新」**をクリックします。

### APIキーを削除する {#delete-an-api-key}

> **注記：**
>
> API キーを削除する前に、その API キーがどのデータ アプリでも使用されていないことを確認してください。

データ アプリの API キーを削除するには、次の手順を実行します。

1.  プロジェクトの[**データサービス**](https://tidbcloud.com/console/data-service)ページに移動します。
2.  左側のペインで、ターゲット データ アプリの名前をクリックして詳細を表示します。
3.  **[API キー]**領域で、 **[アクション]**列を見つけて、削除する API キー行の**[...]** &gt; **[削除]**をクリックします。
4.  表示されるダイアログボックスで、削除を確認します。
