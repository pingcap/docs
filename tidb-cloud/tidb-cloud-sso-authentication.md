---
title: SSO Authentication
summary: Learn how to log in to the TiDB Cloud console via your Google account or GitHub account.
---

# SSO認証 {#sso-authentication}

このドキュメントでは、簡単で便利なシングル サインオン (SSO) 認証を介して[<a href="https://tidbcloud.com/">TiDB Cloudコンソール</a>](https://tidbcloud.com/)にログインする方法について説明します。

TiDB Cloud は、 Google および GitHub アカウントの SSO 認証をサポートしています。 SSO 認証経由でTiDB Cloudにログインする場合、ID と資格情報はサードパーティの Google および GitHub プラットフォームに保存されるため、アカウントのパスワードを変更したり、TiDB を使用して多要素認証 (MFA) を有効にしたりすることはできません。コンソール。

> **ノート：**
>
> ユーザー名とパスワードを使用してTiDB Cloudにログインする場合は、 [<a href="/tidb-cloud/tidb-cloud-password-authentication.md">パスワード認証</a>](/tidb-cloud/tidb-cloud-password-authentication.md)を参照してください。

## Google SSO でサインインする {#sign-in-with-google-sso}

Google アカウントでサインインするには、次の手順を実行します。

1.  TiDB Cloud[<a href="https://tidbcloud.com/">ログイン</a>](https://tidbcloud.com/)ページに移動します。

2.  **[Google でサインイン]**をクリックします。 Google ログインページに移動します。

3.  画面上の指示に従って、Google のユーザー名とパスワードを入力します。

    ログインが成功すると、 TiDB Cloudコンソールに移動します。

    > **ノート：**
    >
    > -   初めて Google にサインインする場合は、 TiDB Cloud の規約に同意するかどうかを尋ねられます。規約を読んで同意すると、 TiDB Cloudのようこそページが表示され、 TiDB Cloudコンソールに移動します。
    > -   Google アカウントの 2 段階認証プロセス (2 要素認証とも呼ばれます) を有効にしている場合は、ユーザー名とパスワードを入力した後、確認コードも入力する必要があります。

## GitHub SSO でサインインする {#sign-in-with-github-sso}

GitHub アカウントでサインインするには、次の手順を実行します。

1.  TiDB Cloud[<a href="https://tidbcloud.com/">ログイン</a>](https://tidbcloud.com/)ページに移動します。

2.  **「GitHub でサインイン」を**クリックします。 GitHub のログイン ページに移動します。

3.  画面上の指示に従って、GitHub のユーザー名とパスワードを入力します。

    ログインが成功すると、 TiDB Cloudコンソールに移動します。

    > **ノート：**
    >
    > -   初めて GitHub にサインインする場合は、 TiDB Cloud の規約に同意するかどうかを尋ねられます。規約を読んで同意すると、 TiDB Cloudのようこそページが表示され、 TiDB Cloudコンソールに移動します。
    > -   GitHub アカウントに 2 要素認証を構成している場合は、ユーザー名とパスワードを入力した後に確認コードも入力する必要があります。
