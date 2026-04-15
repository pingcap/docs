---
title: API Keys in Data Service
summary: データアプリのAPIキーの作成、編集、削除方法を学びましょう。
---

# データサービスのAPIキー {#api-keys-in-data-service}

TiDB Cloud Data API は[基本認証](https://en.wikipedia.org/wiki/Basic_access_authentication)と[ダイジェスト認証](https://en.wikipedia.org/wiki/Digest_access_authentication)の両方をサポートしています。

-   [基本認証](https://en.wikipedia.org/wiki/Basic_access_authentication)は、暗号化されていない Base64 エンコーディングを使用して、公開キーと秘密キーを送信します。 HTTPS により通信のセキュリティが確保されます。詳細については、 [RFC 7617 - 「基本」HTTP認証方式](https://datatracker.ietf.org/doc/html/rfc7617)を参照してください。
-   [ダイジェスト認証](https://en.wikipedia.org/wiki/Digest_access_authentication)ネットワーク送信前に公開キー、秘密キー、サーバー提供のノンス値、HTTP メソッド、および要求された URI をハッシュすることにより、追加のセキュリティレイヤーを提供します。これにより、秘密キーが暗号化され、秘密キーが平文で送信されるのを防ぎます。詳細については、 [RFC 7616 - HTTPダイジェストアクセス認証](https://datatracker.ietf.org/doc/html/rfc7616)を参照してください。

> **注記：**
>
> データサービスで使用されるデータAPIキーは、 [TiDB CloudAPI](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication)で使用されるキーとは異なります。データAPIキーはTiDB内のデータにアクセスするために使用されますが、 TiDB Cloud APIキーはプロジェクト、クラスタ、バックアップ、リストア、インポートなどのリソースを管理するために使用されます。

## APIキーの概要 {#api-key-overview}

-   APIキーには公開鍵と秘密鍵が含まれており、これらは認証に必要なユーザー名とパスワードとして機能します。秘密鍵はキー作成時にのみ表示されます。
-   各APIキーは1つのデータアプリにのみ属し、TiDB内のデータにアクセスするために使用されます。
-   すべてのリクエストで正しいAPIキーを指定する必要があります。そうでない場合、 TiDB Cloudは`401`エラーを返します。

## 律速段階 {#rate-limiting}

リクエストの割り当て量には、以下のレート制限が適用されます。

-   TiDB Cloud Data Serviceでは、デフォルトではAPIキーごとに1分あたり最大100件のリクエスト（rpm）が許可されています。

    API キーのレート制限は、キー[作成する](#create-an-api-key)または[編集](#edit-an-api-key)ときに編集できます。サポートされている値の範囲は、 `1`から`1000`です。 1 分あたりのリクエストがレート制限を超えると、API は`429`エラーを返します。 API キーごとに 1000 rpm を超える割り当てを取得するには、サポート チームに[リクエストを送信する](https://tidb.support.pingcap.com/)ができます。

    各APIリクエストは、制限に関する以下のヘッダーを返します。

    -   `X-Ratelimit-Limit-Minute` : 1 分あたりに許可されるリクエスト数。
    -   `X-Ratelimit-Remaining-Minute` : 現在の1分間に残っているリクエスト数。この数が`0`に達すると、APIは`429`エラーを返し、レート制限を超過したことを示します。
    -   `X-Ratelimit-Reset` : 現在のレート制限がリセットされるまでの時間（秒）。

    レート制限を超過した場合、次のようなエラー応答が返されます。

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

-   TiDB Cloudデータサービスでは、Chat2Queryデータアプリごとに1日あたり最大100件のリクエストが可能です。

## APIキーの有効期限 {#api-key-expiration}

デフォルトでは、API キーは期限切れになりません。ただし、セキュリティを考慮して、キー[作成する](#create-an-api-key)または[編集](#edit-an-api-key)ときに API キーの有効期限を指定できます。

-   APIキーは有効期限までのみ有効です。有効期限が切れると、そのキーを使用したすべてのリクエストは`401`エラーで失敗し、応答は次のようになります。

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

-   API キーを手動で期限切れにすることもできます。詳細な手順については、 [APIキーの有効期限を切る](#expire-an-api-key)[すべてのAPIキーを期限切れにする](#expire-all-api-keys)参照してください。 API キーを手動で期限切れにすると、期限切れはすぐに有効になります。

-   APIキーのステータスと有効期限は、対象のデータアプリの**認証**エリアで確認できます。

-   有効期限が切れたAPIキーは、再度有効化したり編集したりすることはできません。

## APIキーの管理 {#manage-api-keys}

以下のセクションでは、データアプリのAPIキーを作成、編集、削除、および期限切れにする方法について説明します。

### APIキーを作成する {#create-an-api-key}

データアプリのAPIキーを作成するには、以下の手順を実行してください。

1.  プロジェクトの[**データサービス**](https://tidbcloud.com/project/data-service)ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、目的のプロジェクトの**データ サービス**ページに移動するには、[**私のTiDB**](https://tidbcloud.com/tidbs)ページの**[プロジェクト ビュー]**タブをクリックし、目的のプロジェクトの [ **...** ] をクリックしてから、 **[データ サービス]**をクリックします。

2.  左側のペインで、対象のデータアプリの名前をクリックすると、その詳細が表示されます。

3.  **認証**エリアで、 **「APIキーの作成」を**クリックします。

4.  **「APIキーの作成」**ダイアログボックスで、以下の操作を行います。

    1.  （任意）APIキーの説明を入力してください。

    2.  APIキーの役割を選択してください。

        このロールは、APIキーがデータアプリにリンクされたデータソースに対してデータの読み取りまたは書き込みを行えるかどうかを制御するために使用されます。 `ReadOnly`または`ReadAndWrite`ロールを選択できます。

        -   `ReadOnly` : API キーで`SELECT` 、 {{B-PLACEHOLDER `SHOW` 、 `USE` `DESC` }} 、 `EXPLAIN`ステートメントなどのデータを読み取ることのみを許可します。
        -   `ReadAndWrite` : このAPIキーは、データの読み書きを可能にします。このAPIキーを使用して、DMLステートメントやDDLステートメントなど、すべてのSQLステートメントを実行できます。

    3.  （オプション）APIキーの希望するレート制限を設定します。

        1 分あたりのリクエストがレート制限を超えると、API は`429`エラーを返します。 API キーごとに 1 分あたり 1000 リクエスト (rpm) を超える割り当てを取得するには、サポート チームに[リクエストを送信する](https://tidb.support.pingcap.com/)ます。

    4.  （オプション）APIキーの有効期限を設定します。

        デフォルトでは、API キーの有効期限はありません。API キーの有効期限を指定する場合は、[**有効期限]**をクリックし、時間単位 ( `Minutes` 、 `Days` 、または`Months` ) を選択してから、時間単位に希望する数値を入力してください。

5.  **「次へ」**をクリックします。公開鍵と秘密鍵が表示されます。

    秘密鍵を安全な場所にコピーして保存したことを確認してください。このページを離れると、完全な秘密鍵を再度取得することはできません。

6.  **「完了」**をクリックしてください。

### APIキーを編集する {#edit-an-api-key}

> **注記**：
>
> 有効期限切れのキーは編集できません。

APIキーの説明またはレート制限を編集するには、以下の手順を実行してください。

1.  プロジェクトの[**データサービス**](https://tidbcloud.com/project/data-service)ページに移動します。
2.  左側のペインで、対象のデータアプリの名前をクリックすると、その詳細が表示されます。
3.  **認証**エリアで、 **「アクション」**列を探し、変更したいAPIキーの行で**「...」** &gt; **「編集」**をクリックします。
4.  APIキーの説明、役割、レート制限、または有効期限を更新します。
5.  **「更新」**をクリックしてください。

### APIキーを削除する {#delete-an-api-key}

> **注記：**
>
> APIキーを削除する前に、そのAPIキーがどのデータアプリでも使用されていないことを確認してください。

データアプリのAPIキーを削除するには、以下の手順を実行してください。

1.  プロジェクトの[**データサービス**](https://tidbcloud.com/project/data-service)ページに移動します。
2.  左側のペインで、対象のデータアプリの名前をクリックすると、その詳細が表示されます。
3.  **APIキーの**領域で、 **「アクション」**列を探し、削除したいAPIキーの行で**「...」** &gt; **「削除」を**クリックします。
4.  表示されたダイアログボックスで、削除を確認してください。

### APIキーの有効期限を切る {#expire-an-api-key}

> **注記**：
>
> 有効期限切れのキーを再度無効にすることはできません。

データアプリのAPIキーを期限切れにするには、以下の手順を実行してください。

1.  プロジェクトの[**データサービス**](https://tidbcloud.com/project/data-service)ページに移動します。
2.  左側のペインで、対象のデータアプリの名前をクリックすると、その詳細が表示されます。
3.  **認証**エリアで、 **「アクション」**列を探し、有効期限を切れるようにしたいAPIキーの行で**「...」** &gt; **「今すぐ期限切れ」を**クリックします。
4.  表示されたダイアログボックスで、有効期限を確認してください。

### すべてのAPIキーを期限切れにする {#expire-all-api-keys}

データアプリのすべてのAPIキーを期限切れにするには、以下の手順を実行してください。

1.  プロジェクトの[**データサービス**](https://tidbcloud.com/project/data-service)ページに移動します。
2.  左側のペインで、対象のデータアプリの名前をクリックすると、その詳細が表示されます。
3.  **認証**エリアで、 **「すべて期限切れ」**をクリックします。
4.  表示されたダイアログボックスで、有効期限を確認してください。
