---
title: Password Authentication
summary: Learn how to manage passwords and enable multi-factor authentication (MFA) in the TiDB Cloud console.
---

# パスワード認証 {#password-authentication}

このドキュメントでは、TiDB Cloudコンソールでパスワードを管理し、多要素認証 (MFA) を有効にする方法について説明します。このドキュメントは、メールとパスワードを使用してTiDB Cloudを[サインアップ](https://tidbcloud.com/free-trial)しているユーザーにのみ適用されます。

## サインアップ {#sign-up}

電子メールとパスワードを使用してTiDB Cloud を[サインアップ](https://tidbcloud.com/free-trial)にするか、 TiDB Cloudへのシングル サインオン (SSO) 用に Google、GitHub、または Microsoft アカウントを選択できます。

-   電子メールとパスワードでTiDB Cloudにサインアップすると、このドキュメントに従ってパスワードを管理できます。
-   Google、GitHub、または Microsoft SSO to TiDB Cloudを選択した場合、パスワードは選択したプラットフォームによって管理され、 TiDB Cloudコンソールを使用してパスワードを変更することはできません。

電子メールとパスワードを使用してTiDB Cloudアカウントにサインアップするには、次の手順を実行します。

1.  TiDB Cloud [サインアップ](https://tidbcloud.com/free-trial)ページに移動し、登録情報を入力します。

2.  プライバシー ポリシーとサービス契約を読み、 **[プライバシー ポリシーとサービス契約に同意します]**を選択します。

3.  **[サインアップ]**をクリックします。

TiDB Cloudの確認メールが届きます。登録プロセス全体を完了するには、メールボックスをチェックして登録を確認します。

## サインインまたはサインアウト {#sign-in-or-sign-out}

### ログイン {#sign-in}

電子メールとパスワードを使用してTiDB Cloudにログインするには、次の手順を実行します。

1.  TiDB Cloud[ログイン](https://tidbcloud.com/)ページに移動します。

2.  メールアドレスとパスワードを入力します。

3.  **[サインイン]**をクリックします。

ログインに成功すると、 TiDB Cloudコンソールに移動します。

### サインアウト {#sign-out}

TiDB Cloudコンソールの右上隅にある<mdsvgicon name="icon-top-account-settings">**アカウントを**開き、 <strong>[ログアウト]</strong>を選択します。</mdsvgicon>

## パスワード ポリシー {#password-policy}

TiDB Cloud は、登録ユーザーのデフォルトのパスワード ポリシーを設定します。パスワードがポリシーを満たしていない場合は、パスワードを設定するときにプロンプトが表示されます。

デフォルトのパスワード ポリシーは次のとおりです。

-   長さは 8 文字以上。
-   少なくとも 1 つの大文字 (AZ)。
-   少なくとも 1 つの小文字 (az)。
-   少なくとも 1 つの数字 (0 ～ 9)。
-   新しいパスワードは、以前の 4 つのパスワードのいずれとも同じであってはなりません。

## パスワードをリセットする {#reset-a-password}

> **ノート：**
>
> このセクションは、電子メールとパスワードを使用したTiDB Cloud登録にのみ適用されます。 Google SSO または GitHub SSO を使用してTiDB Cloudにサインアップする場合、パスワードは Google または GitHub によって管理され、 TiDB Cloudコンソールを使用して変更することはできません。

パスワードを忘れた場合は、次のように電子メールでリセットできます。

1.  TiDB Cloud[ログイン](https://tidbcloud.com/)ページに移動します。

2.  **[パスワードを忘れた場合]**をクリックし、電子メールでパスワードをリセットするためのリンクを確認します。

## パスワードを変更する {#change-a-password}

> **ノート：**
>
> 電子メールとパスワードでTiDB Cloudにサインアップする場合は、90 日ごとにパスワードをリセットすることをお勧めします。それ以外の場合は、 TiDB Cloudにログインするときに、パスワードを変更するように求めるパスワードの有効期限のリマインダーが表示されます。

1.  クリック<mdsvgicon name="icon-top-account-settings">TiDB Cloudコンソールの右上隅に**あるアカウント**。</mdsvgicon>

2.  **[アカウント設定]**をクリックします。

3.  **[パスワードの変更]**タブをクリックし、 <strong>[パスワードの変更]</strong>をクリックしてから、 TiDB Cloudの電子メールを確認してパスワードをリセットします。

## MFA の有効化または無効化 (オプション) {#enable-or-disable-mfa-optional}

> **ノート：**
>
> このセクションは、電子メールとパスワードを使用し[サインアップ](https://tidbcloud.com/free-trial) TiDB Cloudを使用する場合にのみ適用されます。 Google、GitHub、または Microsoft SSO を使用してTiDB Cloudにサインアップすると、選択した ID 管理プラットフォームで MFA を有効にできます。

TiDB Cloudにログインした後、法規制に従って MFA を有効にすることができます。

2 要素認証は、Authenticator アプリにログイン用のワンタイム パスワードの生成を要求することで、セキュリティを強化します。 iOS または Android App Store の任意の Authenticator アプリ (Google Authenticator や Authy など) を使用して、このパスワードを生成できます。

### MFA を有効にする {#enable-mfa}

1.  クリック<mdsvgicon name="icon-top-account-settings">TiDB Cloudコンソールの右上隅に**あるアカウント**。</mdsvgicon>

2.  **[アカウント設定]**をクリックします。

3.  **[2 要素認証]**タブをクリックします。

4.  **[有効にする]**をクリックします。

### MFA を無効にする {#disable-mfa}

1.  クリック<mdsvgicon name="icon-top-account-settings">TiDB Cloudコンソールの右上隅に**あるアカウント**。</mdsvgicon>

2.  **[アカウント設定]**をクリックします。

3.  **[2 要素認証]**タブをクリックします。

4.  **[無効にする]**をクリックします。
