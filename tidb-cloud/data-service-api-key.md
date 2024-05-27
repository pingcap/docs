---
title: API Keys in Data Service
summary: データ アプリの API キーを作成、編集、削除する方法を学びます。
---

# データサービスの API キー {#api-keys-in-data-service}

TiDB Cloud Data API は[基本認証](https://en.wikipedia.org/wiki/Basic_access_authentication)と[ダイジェスト認証](https://en.wikipedia.org/wiki/Digest_access_authentication)両方をサポートします。

-   [基本認証](https://en.wikipedia.org/wiki/Basic_access_authentication) 、暗号化されていない base64 エンコードを使用して公開鍵と秘密鍵を送信します。HTTPS により、送信のセキュリティが確保されます。詳細については、 [RFC 7617 - 「基本」HTTP 認証スキーム](https://datatracker.ietf.org/doc/html/rfc7617)を参照してください。
-   [ダイジェスト認証](https://en.wikipedia.org/wiki/Digest_access_authentication) 、ネットワーク送信前に公開鍵、秘密鍵、サーバーから提供された nonce 値、HTTP メソッド、および要求された URI をハッシュすることにより、追加のセキュリティレイヤーを提供します。これにより、秘密鍵が暗号化され、プレーン テキストで送信されることが防止されます。詳細については、 [RFC 7616 - HTTP ダイジェスト アクセス認証](https://datatracker.ietf.org/doc/html/rfc7616)を参照してください。

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

    API キーのレート制限は`1`キーを[編集](#edit-an-api-key)ときに編集できます。サポートされる値の範囲は[作成する](#create-an-api-key) ～ `1000`です。1 分あたりのリクエスト数がレート制限を超えると、API は`429`を返します。API キーごとに 1000 rpm を超えるクォータを取得するには、サポート チームにご[リクエストを送信する](https://support.pingcap.com/hc/en-us/requests/new?ticket_form_id=7800003722519)ください。

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

    {"type":"","data":{"columns":[],"rows":[],"result":{"latency":"","row_affect":0,"code":49900007,"row_count":0,"end_ms":0,"limit":0,"message":"API key rate limit exceeded. The limit can be increased up to 1000 requests per minute per API key in TiDB Cloud console. For an increase in quota beyond 1000 rpm, please contact us: https://support.pingcap.com/hc/en-us/requests/new?ticket_form_id=7800003722519","start_ms":0}}}
    ```

-   TiDB Cloudデータ サービスでは、Chat2Query データ アプリごとに 1 日あたり最大 100 件のリクエストが許可されます。

## APIキーを管理する {#manage-api-keys}

次のセクションでは、データ アプリの API キーを作成、編集、削除する方法について説明します。

### APIキーを作成する {#create-an-api-key}

データ アプリの API キーを作成するには、次の手順を実行します。

1.  プロジェクトの[**データサービス**](https://tidbcloud.com/console/data-service)ページに移動します。

2.  左側のペインで、対象のデータ アプリの名前をクリックして詳細を表示します。

3.  **認証**領域で、 **「API キーの作成」を**クリックします。

4.  **[API キーの作成]**ダイアログ ボックスで、次の操作を行います。

    1.  (オプション) API キーの説明を入力します。

    2.  API キーのロールを選択します。

        このロールは、API キーがデータ アプリにリンクされたクラスターにデータを読み書きできるかどうかを制御するために使用されます。1 または`ReadOnly` `ReadAndWrite`ロールを選択できます。

        -   `ReadOnly` : API キーは`SELECT` 、 `SHOW` 、 `USE` 、 `DESC` 、 `EXPLAIN`ステートメントなどのデータのみを読み取ることができます。
        -   `ReadAndWrite` : API キーによるデータの読み取りと書き込みを許可します。この API キーを使用して、DML ステートメントや DDL ステートメントなどのすべての SQL ステートメントを実行できます。

    3.  (オプション) API キーに必要なレート制限を設定します。

        1 分あたりのリクエスト数がレート制限を超えると、API は`429`エラーを返します。API キーごとに 1 分あたり 1000 リクエスト (rpm) を超えるクォータを取得するには、サポート チームに[リクエストを送信する](https://support.pingcap.com/hc/en-us/requests/new?ticket_form_id=7800003722519)連絡してください。

5.  **「次へ」**をクリックします。公開鍵と秘密鍵が表示されます。

    秘密鍵をコピーして安全な場所に保存したことを確認してください。このページを離れると、完全な秘密鍵を再度取得できなくなります。

6.  **「完了」を**クリックします。

### APIキーを編集する {#edit-an-api-key}

API キーの説明またはレート制限を編集するには、次の手順を実行します。

1.  プロジェクトの[**データサービス**](https://tidbcloud.com/console/data-service)ページに移動します。
2.  左側のペインで、対象のデータ アプリの名前をクリックして詳細を表示します。
3.  **API キー**領域で、**アクション**列を見つけて、変更する API キー行で**...** &gt;**編集を**クリックします。
4.  API キーの説明、ロール、またはレート制限を更新します。
5.  **[更新]を**クリックします。

### APIキーを削除する {#delete-an-api-key}

> **注記：**
>
> API キーを削除する前に、その API キーがどのデータ アプリでも使用されていないことを確認してください。

データ アプリの API キーを削除するには、次の手順を実行します。

1.  プロジェクトの[**データサービス**](https://tidbcloud.com/console/data-service)ページに移動します。
2.  左側のペインで、対象のデータ アプリの名前をクリックして詳細を表示します。
3.  **API キー**領域で、**アクション**列を見つけて、削除する API キー行で**...** &gt;**削除を**クリックします。
4.  表示されたダイアログボックスで削除を確認します。
