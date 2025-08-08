---
title: OAuth 2.0
summary: TiDB Cloudで OAuth 2.0 を使用する方法について説明します。
---

# OAuth 2.0 {#oauth-2-0}

このドキュメントでは、OAuth 2.0 を使用してTiDB Cloud にアクセスする方法について説明します。

OAuth（Open Authorization）は、ユーザーに代わってリソースへの安全なアクセスを可能にするオープンスタンダードの認証プロトコルです。サードパーティアプリケーションがユーザーの資格情報を公開することなく、ユーザーのリソースにアクセスできるようにします。

OAuthの最新バージョンである[OAuth 2.0](https://oauth.net/2/)は、認証における業界標準プロトコルとなりました。OAuth 2.0の主な利点は次のとおりです。

-   Security: トークンベースの認証を使用することで、OAuth 2.0 はパスワードの盗難や不正アクセスのリスクを最小限に抑えます。
-   利便性: 複数の資格情報を管理することなく、データへのアクセスを許可および取り消すことができます。
-   アクセス制御: サードパーティ アプリケーションに付与するアクセス レベルを正確に指定して、必要な権限のみが付与されるようにすることができます。

## OAuth 付与タイプ {#oauth-grant-types}

OAuthフレームワークは、さまざまなユースケースに合わせて複数の権限付与タイプを指定します。TiDB TiDB Cloudは、デバイスコードと認証コードという2つの最も一般的なOAuth権限付与タイプをサポートしています。

### デバイスコード付与タイプ {#device-code-grant-type}

これは通常、デバイス フロー内のブラウザーレス デバイスまたは入力が制限されたデバイスによって、以前に取得したデバイス コードをアクセス トークンと交換するために使用されます。

### 認可コード付与タイプ {#authorization-code-grant-type}

これは最も一般的な OAuth 2.0 付与タイプであり、ユーザーがアプリを承認した後、Web アプリとネイティブ アプリの両方がアクセス トークンを取得できるようになります。

## OAuth を使用してTiDB Cloudにアクセスする {#use-oauth-to-access-tidb-cloud}

OAuth 2.0 デバイスコード付与タイプを使用して、 TiDB Cloud CLI にアクセスできます。

-   [ticloud認証ログイン](/tidb-cloud/ticloud-auth-login.md) : TiDB Cloudで認証する
-   [ticloud 認証ログアウト](/tidb-cloud/ticloud-auth-logout.md) : TiDB Cloudからログアウト

アプリがOAuthを使用してTiDB Cloudにアクセスする必要がある場合は、 [クラウド＆テクノロジーパートナーになる](https://www.pingcap.com/partners/become-a-partner/) （**パートナープログラム**で**クラウド＆テクノロジーパートナー**を選択）にリクエストを送信してください。担当者からご連絡いたします。

## 承認された OAuth アプリのビューと取り消し {#view-and-revoke-authorized-oauth-apps}

次のように、 TiDB Cloudコンソールで承認された OAuth アプリケーションのレコードを表示できます。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、<mdsvgicon name="icon-top-account-settings">左下隅にあります。</mdsvgicon>
2.  **[アカウント設定]**をクリックします。
3.  **「承認済みOAuthアプリ」**タブをクリックします。承認済みのOAuthアプリケーションが表示されます。

**「取り消し」**をクリックすると、いつでも承認を取り消すことができます。
