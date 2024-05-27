---
title: Password Authentication
summary: TiDB Cloudコンソールでパスワードを管理し、多要素認証 (MFA) を有効にする方法を学習します。
---

# パスワード認証 {#password-authentication}

このドキュメントでは、 TiDB Cloudコンソールでパスワードを管理し、多要素認証 (MFA) を有効にする方法について説明します。このドキュメントは、電子メールとパスワードを使用してTiDB Cloudに[サインアップ](https://tidbcloud.com/free-trial)ユーザーにのみ適用されます。

## サインアップ {#sign-up}

電子メールとパスワードを使用してTiDB Cloudに[サインアップ](https://tidbcloud.com/free-trial)か、Google、GitHub、または Microsoft アカウントを選択してTiDB Cloudへのシングル サインオン (SSO) を行うことができます。

-   メールアドレスとパスワードを使用してTiDB Cloudにサインアップすると、このドキュメントに従ってパスワードを管理できます。
-   TiDB Cloudへの Google、GitHub、または Microsoft SSO を選択した場合、パスワードは選択したプラットフォームによって管理され、 TiDB Cloudコンソールを使用して変更することはできません。

電子メールとパスワードを使用してTiDB Cloudアカウントにサインアップするには、次の手順を実行します。

1.  TiDB Cloud [サインアップ](https://tidbcloud.com/free-trial)ページに移動し、登録情報を入力します。

2.  プライバシー ポリシーとサービス契約を読み、 **[プライバシー ポリシーとサービス契約に同意する]**を選択します。

3.  **「サインアップ」を**クリックします。

TiDB Cloudの確認メールが届きます。登録プロセス全体を完了するには、メールボックスを確認して登録を確認してください。

## サインインまたはサインアウト {#sign-in-or-sign-out}

### サインイン {#sign-in}

電子メールとパスワードを使用してTiDB Cloudにログインするには、次の手順を実行します。

1.  TiDB Cloud [ログイン](https://tidbcloud.com/)ページに移動します。

2.  メールアドレスとパスワードを入力してください。

3.  **[サインイン]を**クリックします。

ログインが成功すると、 TiDB Cloudコンソールに移動します。

### サインアウト {#sign-out}

TiDB Cloudコンソールの左下隅で、<mdsvgicon name="icon-top-account-settings">**ログアウト**を選択します。</mdsvgicon>

## パスワードポリシー {#password-policy}

TiDB Cloud は、登録ユーザーに対してデフォルトのパスワード ポリシーを設定します。パスワードがポリシーを満たしていない場合は、パスワードを設定するときにプロンプ​​トが表示されます。

デフォルトのパスワード ポリシーは次のとおりです。

-   長さは 8 文字以上。
-   少なくとも 1 つの大文字 (A ～ Z)。
-   少なくとも 1 つの小文字 (az)。
-   少なくとも 1 つの数字 (0 ～ 9)。
-   新しいパスワードは、以前の 4 つのパスワードと同じにすることはできません。

## パスワードをリセットする {#reset-a-password}

> **注記：**
>
> このセクションは、電子メールとパスワードを使用したTiDB Cloud登録にのみ適用されます。Google SSO または GitHub SSO を使用してTiDB Cloudにサインアップする場合、パスワードは Google または GitHub によって管理され、 TiDB Cloudコンソールを使用して変更することはできません。

パスワードを忘れた場合は、次の手順に従ってメールでリセットできます。

1.  TiDB Cloud [ログイン](https://tidbcloud.com/)ページに移動します。

2.  **「パスワードを忘れた場合**」をクリックし、パスワードをリセットするためのリンクが記載されたメールを確認してください。

## パスワードを変更する {#change-a-password}

> **注記：**
>
> 電子メールとパスワードを使用してTiDB Cloudにサインアップする場合は、90 日ごとにパスワードをリセットすることをお勧めします。そうしないと、 TiDB Cloudにログインしたときに、パスワードを変更するように求めるパスワード有効期限のリマインダーが表示されます。

1.  クリック<mdsvgicon name="icon-top-account-settings">TiDB Cloudコンソールの左下隅にあります。</mdsvgicon>

2.  **[アカウント設定]**をクリックします。

3.  **[パスワードの変更]**タブをクリックし、 **[パスワードの変更]**をクリックして、 TiDB Cloudからの電子メールを確認し、パスワードをリセットします。

## MFA を有効または無効にする (オプション) {#enable-or-disable-mfa-optional}

> **注記：**
>
> このセクションは、電子メールとパスワードを使用してTiDB Cloudにサイン[サインアップ](https://tidbcloud.com/free-trial)する場合にのみ適用されます。Google、GitHub、または Microsoft SSO を使用してTiDB Cloudにサインアップする場合は、選択した ID 管理プラットフォームで MFA を有効にすることができます。

TiDB Cloudにログイン後、法律や規制に従って MFA を有効にすることができます。

2 要素認証では、認証アプリを使用してログイン用のワンタイム パスワードを生成することで、セキュリティが強化されます。このパスワードを生成するには、Google Authenticator や Authy など、iOS または Android App Store の任意の認証アプリを使用できます。

### MFAを有効にする {#enable-mfa}

1.  クリック<mdsvgicon name="icon-top-account-settings">TiDB Cloudコンソールの左下隅にあります。</mdsvgicon>

2.  **[アカウント設定]**をクリックします。

3.  **「2要素認証」**タブをクリックします。

4.  **[有効にする]**をクリックします。

### MFAを無効にする {#disable-mfa}

1.  クリック<mdsvgicon name="icon-top-account-settings">TiDB Cloudコンソールの左下隅にあります。</mdsvgicon>

2.  **[アカウント設定]**をクリックします。

3.  **「2要素認証」**タブをクリックします。

4.  **[無効にする]**をクリックします。
