---
title: API Keys in Data Service
summary: Learn how to create, edit, and delete an API key for a Data App.
---

# Data Service の API キー {#api-keys-in-data-service}

TiDB Cloud Data API は[HTTP ダイジェスト認証](https://en.wikipedia.org/wiki/Digest_access_authentication)を使用します。秘密鍵がネットワーク経由で送信されるのを防ぎます。 HTTP ダイジェスト認証の詳細については、 [IETF RFC](https://datatracker.ietf.org/doc/html/rfc7616)を参照してください。

> **ノート：**
>
> Data Service の Data API キーは、 [TiDB CloudAPI](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication)で使用されるキーとは異なります。 Data API キーはTiDB Cloudクラスター内のデータにアクセスするために使用されますが、 TiDB Cloud API キーはプロジェクト、クラスター、バックアップ、復元、インポートなどのリソースを管理するために使用されます。

## API キーの概要 {#api-key-overview}

-   API キーには公開鍵と秘密鍵が含まれており、HTTP ダイジェスト認証で必要なユーザー名とパスワードとして機能します。秘密鍵は、鍵の作成時にのみ表示されます。
-   各 API キーは 1 つの Data App のみに属し、 TiDB Cloudクラスター内のデータにアクセスするために使用されます。
-   すべてのリクエストで正しい API キーを提供する必要があります。それ以外の場合、 TiDB Cloud は`401`エラーで応答します。

## レート制限 {#rate-limiting}

各 Chat2Query データ アプリには、1 日あたり 100 リクエストのレート制限があります。他のデータ アプリには、API キーごとに 1 分あたり 100 リクエストのレート制限があります。レート制限を超えると、API は`429`エラーを返します。さらに割り当てが必要な場合は、サポート チームに[リクエストを提出する](https://support.pingcap.com/hc/en-us/requests/new?ticket_form_id=7800003722519)してください。

## API キーの管理 {#manage-api-keys}

次のセクションでは、データ アプリの API キーを作成、編集、および削除する方法について説明します。

### API キーを作成する {#create-an-api-key}

データ アプリの API キーを作成するには、次の手順を実行します。

1.  プロジェクトの[**データサービス**](https://tidbcloud.com/console/data-service)ページに移動します。

2.  左ペインで、ターゲット データ アプリの名前をクリックして詳細を表示します。

3.  **[API キー]**領域で、 <strong>[API キーの作成]</strong>をクリックします。

4.  **[API キーの作成]**ダイアログ ボックスで、説明を入力し、API キーのロールを選択します。

    ロールは、API キーが Data App にリンクされたクラスターにデータを読み書きできるかどうかを制御するために使用されます。 `ReadOnly`または`ReadAndWrite`役割を選択できます。

    -   `ReadOnly` : API キーが`SELECT` 、 `SHOW` 、 `USE` 、 `DESC` 、および`EXPLAIN`ステートメントなどのデータを読み取ることのみを許可します。
    -   `ReadAndWrite` : API キーによるデータの読み取りと書き込みを許可します。この API キーを使用して、DML ステートメントや DDL ステートメントなど、すべての SQL ステートメントを実行できます。

5.  **[次へ]**をクリックします。公開鍵と秘密鍵が表示されます。

    秘密鍵をコピーして安全な場所に保存したことを確認してください。このページを離れると、完全な秘密鍵を再度取得することはできなくなります。

6.  **[完了]**をクリックします。

### API キーを編集する {#edit-an-api-key}

API キーの説明を編集するには、次の手順を実行します。

1.  プロジェクトの[**データサービス**](https://tidbcloud.com/console/data-service)ページに移動します。
2.  左ペインで、ターゲット データ アプリの名前をクリックして詳細を表示します。
3.  **[API キー]**領域で、 <strong>[アクション]</strong>列を見つけて、変更する API キーの行で<strong>[...]</strong> &gt; <strong>[編集]</strong>をクリックします。
4.  API キーの説明または役割を更新します。
5.  **[更新]**をクリックします。

### API キーを削除する {#delete-an-api-key}

> **ノート：**
>
> API キーを削除する前に、その API キーがデータ アプリで使用されていないことを確認してください。

データ アプリの API キーを削除するには、次の手順を実行します。

1.  プロジェクトの[**データサービス**](https://tidbcloud.com/console/data-service)ページに移動します。
2.  左ペインで、ターゲット データ アプリの名前をクリックして詳細を表示します。
3.  **[API キー]**領域で、 <strong>[アクション]</strong>列を見つけて、削除する API キーの行で<strong>[...]</strong> &gt; <strong>[削除]</strong>をクリックします。
4.  表示されたダイアログボックスで、削除を確認します。
