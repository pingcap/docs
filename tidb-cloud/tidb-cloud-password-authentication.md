---
title: Password Authentication
summary: Learn how to manage passwords and enable multi-factor authentication (MFA) in the TiDB Cloud console.
---

# パスワード認証 {#password-authentication}

このドキュメントでは、TiDB Cloudコンソールでパスワードを管理し、多要素認証 (MFA) を有効にする方法について説明します。このドキュメントは、電子メールとパスワードを使用してTiDB Cloudを[<a href="https://tidbcloud.com/free-trial">サインアップ</a>](https://tidbcloud.com/free-trial)するユーザーにのみ適用されます。

## サインアップ {#sign-up}

TiDB Cloudの場合はメールとパスワードを使用するか、 TiDB Cloudへのシングル サインオン (SSO [<a href="https://tidbcloud.com/free-trial">サインアップ</a>](https://tidbcloud.com/free-trial)用に Google Workspace または GitHub アカウントを選択できます。

-   電子メールとパスワードを使用してTiDB Cloudにサインアップすると、本書に従ってパスワードを管理できます。
-   TiDB Cloudへの Google SSO または GitHub SSO を選択した場合、パスワードは Google または GitHub によって管理され、 TiDB Cloudコンソールを使用して変更することはできません。

電子メールとパスワードを使用してTiDB Cloudアカウントにサインアップするには、次の手順を実行します。

1.  TiDB Cloud [<a href="https://tidbcloud.com/free-trial">サインアップ</a>](https://tidbcloud.com/free-trial)ページに移動し、登録情報を入力します。

2.  「プライバシー ポリシーとサービス契約」を読み、 **「プライバシー ポリシーとサービス契約に同意する」**を選択します。

3.  **「サインアップ」**をクリックします。

TiDB Cloudの確認メールが届きます。登録プロセス全体を完了するには、メールボックスをチェックして登録を確認してください。

## サインインまたはサインアウト {#sign-in-or-sign-out}

### ログイン {#sign-in}

電子メールとパスワードを使用してTiDB Cloudにログインするには、次の手順を実行します。

1.  TiDB Cloud[<a href="https://tidbcloud.com/">ログイン</a>](https://tidbcloud.com/)ページに移動します。

2.  メールアドレスとパスワードを入力します。

3.  **「サインイン」**をクリックします。

ログインが成功すると、 TiDB Cloudコンソールに移動します。

### サインアウト {#sign-out}

TiDB Cloudコンソールの右上隅にある をクリックします。<mdsvgicon name="icon-top-account-settings">**アカウントを**選択し、 **「ログアウト」**を選択します。</mdsvgicon>

## パスワードポリシー {#password-policy}

TiDB Cloudは、登録ユーザーに対してデフォルトのパスワード ポリシーを設定します。パスワードがポリシーを満たしていない場合は、パスワードを設定するときにプロンプトが表示されます。

デフォルトのパスワードポリシーは次のとおりです。

-   少なくとも 8 文字の長さ。
-   少なくとも 1 つの大文字 (AZ)。
-   少なくとも 1 つの小文字 (az)。
-   少なくとも 1 つの数字 (0 ～ 9)。
-   新しいパスワードは、以前の 4 つのパスワードと同じであってはなりません。

## パスワードをリセットする {#reset-a-password}

> **ノート：**
>
> このセクションは、電子メールとパスワードを使用したTiDB Cloud登録にのみ適用されます。 Google SSO または GitHub SSO を使用してTiDB Cloudにサインアップした場合、パスワードは Google または GitHub によって管理され、 TiDB Cloudコンソールを使用して変更することはできません。

パスワードを忘れた場合は、次のように電子メールでパスワードをリセットできます。

1.  TiDB Cloud[<a href="https://tidbcloud.com/">ログイン</a>](https://tidbcloud.com/)ページに移動します。

2.  **[パスワードを忘れた場合]**をクリックし、電子メールでパスワードをリセットするためのリンクを確認します。

## パスワードを変更する {#change-a-password}

> **ノート：**
>
> 電子メールとパスワードを使用してTiDB Cloudにサインアップする場合は、90 日ごとにパスワードをリセットすることをお勧めします。それ以外の場合は、 TiDB Cloudにログインするときにパスワードの有効期限を通知するメッセージが表示され、パスワードを変更する必要があります。

1.  クリック<mdsvgicon name="icon-top-account-settings">TiDB Cloudコンソールの右上隅にある**アカウント**。</mdsvgicon>

2.  **[アカウント設定]**をクリックします。

3.  **「パスワードの変更」**タブをクリックし、 **「パスワードの変更」**をクリックして、 TiDB Cloudの電子メールを確認してパスワードをリセットします。

## MFA を有効または無効にする (オプション) {#enable-or-disable-mfa-optional}

> **ノート：**
>
> このセクションは、電子メールとパスワードを使用し[<a href="https://tidbcloud.com/free-trial">サインアップ</a>](https://tidbcloud.com/free-trial) TiDB Cloudを利用する場合にのみ適用されます。 Google SSO または GitHub SSO を使用してTiDB Cloudにサインアップすると、GitHub や Google Workspace などの ID 管理プラットフォームで MFA を有効にすることができます。

TiDB Cloudにログインした後、法律や規制に従って MFA を有効にすることができます。

2 要素認証では、Authenticator アプリにログイン用のワンタイム パスワードの生成を要求することで、セキュリティが強化されます。 iOS または Android App Store の認証アプリ (Google Authenticator や Authy など) を使用してこのパスワードを生成できます。

### MFA を有効にする {#enable-mfa}

1.  クリック<mdsvgicon name="icon-top-account-settings">TiDB Cloudコンソールの右上隅に**あるアカウント**。</mdsvgicon>

2.  **[アカウント設定]**をクリックします。

3.  **[2 要素認証]**タブをクリックします。

4.  **「有効にする」**をクリックします。

### MFA を無効にする {#disable-mfa}

1.  クリック<mdsvgicon name="icon-top-account-settings">TiDB Cloudコンソールの右上隅に**あるアカウント**。</mdsvgicon>

2.  **[アカウント設定]**をクリックします。

3.  **[2 要素認証]**タブをクリックします。

4.  **「無効にする」**をクリックします。
