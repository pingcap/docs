---
title: Configure SSO for TiDB Dashboard
summary: Learn how to enable SSO to sign into TiDB Dashboard.
---

# TiDB ダッシュボードの SSO を構成する {#configure-sso-for-tidb-dashboard}

TiDB ダッシュボードは、 [OIDC](https://openid.net/connect/)ベースのシングル サインオン (SSO) をサポートしています。 TiDB ダッシュボードの SSO 機能を有効にすると、構成された SSO サービスがサインイン認証に使用され、SQL ユーザー パスワードを入力せずに TiDB ダッシュボードにアクセスできるようになります。

## OIDC SSO の構成 {#configure-oidc-sso}

### SSO を有効にする {#enable-sso}

1.  TiDB ダッシュボードにサインインします。

2.  左側のサイドバーでユーザー名をクリックして、構成ページにアクセスします。

3.  **[シングル サインオン]**セクションで、 <strong>[有効にする] を選択して、TiDB ダッシュボードにサインインするときに SSO を使用します</strong>。

4.  フォームの**OIDC クライアント ID**と<strong>OIDC 検出 URL</strong>フィールドに入力します。

    通常、SSO サービス プロバイダーから次の 2 つのフィールドを取得できます。

    -   OIDC クライアント ID は、OIDC トークン発行者とも呼ばれます。
    -   OIDC Discovery URL は、OIDC Token Audience とも呼ばれます。

5.  **Authorize Impersonation を**クリックし、SQL パスワードを入力します。

    TiDB ダッシュボードはこの SQL パスワードを保存し、SSO サインインが完了した後に通常の SQL サインインを偽装するために使用します。

    ![Sample Step](/media/dashboard/dashboard-session-sso-enable-1.png)

    > **ノート：**
    >
    > 入力したパスワードは暗号化されて保存されます。 SQL ユーザーのパスワードが変更されると、SSO サインインは失敗します。この場合、パスワードを再入力して SSO を元に戻すことができます。

6.  **[認証して保存]**をクリックします。

    ![Sample Step](/media/dashboard/dashboard-session-sso-enable-2.png)

7.  **更新**(更新) をクリックして構成を保存します。

    ![Sample Step](/media/dashboard/dashboard-session-sso-enable-3.png)

これで、TiDB ダッシュボードで SSO サインインが有効になりました。

> **ノート：**
>
> セキュリティ上の理由から、一部の SSO サービスでは、信頼できるサインイン URI やサインアウト URI など、SSO サービスの追加構成が必要です。詳細については、SSO サービスのドキュメントを参照してください。

### SSO を無効にする {#disable-sso}

SSO を無効にすると、保存されている SQL パスワードが完全に消去されます。

1.  TiDB ダッシュボードにサインインします。

2.  左側のサイドバーでユーザー名をクリックして、構成ページにアクセスします。

3.  **[シングル サインオン]**セクションで、 <strong>[TiDB ダッシュボードにサインインするときに SSO を使用するには有効にする] の</strong>選択を解除します。

4.  **更新**(更新) をクリックして構成を保存します。

    ![Sample Step](/media/dashboard/dashboard-session-sso-disable.png)

### パスワード変更後のパスワード再入力 {#re-enter-the-password-after-a-password-change}

SQL ユーザーのパスワードが変更されると、SSO サインインは失敗します。この場合、SQL パスワードを再入力することで、SSO サインインを元に戻すことができます。

1.  TiDB ダッシュボードにサインインします。

2.  左側のサイドバーでユーザー名をクリックして、構成ページにアクセスします。

3.  **[Single Sign-On]**セクションで、 <strong>[Authorize Impersonation]</strong>をクリックし、更新された SQL パスワードを入力します。

    ![Sample Step](/media/dashboard/dashboard-session-sso-reauthorize.png)

4.  **[認証して保存]**をクリックします。

## SSO 経由でサインインする {#sign-in-via-sso}

SSO が TiDB ダッシュボード用に構成されたら、次の手順を実行して SSO 経由でサインインできます。

1.  TiDB ダッシュボードのサインイン ページで、 **[Sign in via Company Account]**をクリックします。

    ![Sample Step](/media/dashboard/dashboard-session-sso-signin.png)

2.  SSO サービスが構成されたシステムにサインインします。

3.  サインインを完了するために、TiDB ダッシュボードにリダイレクトされます。

## 例 1: TiDB ダッシュボードの SSO サインインに Okta を使用する {#example-1-use-okta-for-tidb-dashboard-sso-sign-in}

[オクタ](https://www.okta.com/) 、TiDB ダッシュボードの SSO 機能と互換性のある OIDC SSO ID サービスです。以下の手順は、Okta を TiDB ダッシュボード SSO プロバイダーとして使用できるように、Okta と TiDB ダッシュボードを構成する方法を示しています。

### ステップ 1: Okta を構成する {#step-1-configure-okta}

まず、Okta アプリケーション統合を作成して SSO を統合します。

1.  Okta 管理サイトにアクセスします。

2.  左側のサイドバーから**[アプリケーション]** &gt; <strong>[アプリケーション]</strong>に移動します。

3.  **[アプリ統合の作成]**をクリックします。

    ![Sample Step](/media/dashboard/dashboard-session-sso-okta-1.png)

4.  ポップアップしたダイアログで、 **OIDC - OpenID Connect** in <strong>Sign-in method</strong>を選択します。

5.  **Application Type**で<strong>Single-Page Application</strong>を選択します。

6.  **[次へ]**ボタンをクリックします。

    ![Sample Step](/media/dashboard/dashboard-session-sso-okta-2.png)

7.  **サインイン リダイレクト URI を**次のように入力します。

    ```
    http://DASHBOARD_IP:PORT/dashboard/?sso_callback=1
    ```

    `DASHBOARD_IP:PORT`ブラウザーで TiDB ダッシュボードにアクセスするために使用する実際のドメイン (または IP アドレス) とポートに置き換えます。

8.  **サインアウト リダイレクト URI を**次のように入力します。

    ```
    http://DASHBOARD_IP:PORT/dashboard/
    ```

    同様に、 `DASHBOARD_IP:PORT`実際のドメイン (または IP アドレス) とポートに置き換えます。

    ![Sample Step](/media/dashboard/dashboard-session-sso-okta-3.png)

9.  **[割り当て]**フィールドで SSO サインインを許可する組織内のユーザーのタイプを構成し、 <strong>[保存]</strong>をクリックして構成を保存します。

    ![Sample Step](/media/dashboard/dashboard-session-sso-okta-4.png)

### ステップ 2: OIDC 情報を取得し、TiDB ダッシュボードに入力する {#step-2-obtain-oidc-information-and-fill-in-tidb-dashboard}

1.  Okta で作成した Application Integration で、 **Sign On を**クリックします。

    ![Sample Step 1](/media/dashboard/dashboard-session-sso-okta-info-1.png)

2.  **OpenID Connect ID Token**セクションから<strong>Issuer フィールド</strong>と<strong>Audience</strong>フィールドの値をコピーします。

    ![Sample Step 2](/media/dashboard/dashboard-session-sso-okta-info-2.png)

3.  TiDB ダッシュボードの構成ページを開き、 **OIDC クライアント ID**に最後の手順で取得した<strong>発行者</strong>を入力し、 <strong>OIDC 検出 URL</strong>に<strong>Audience</strong>を入力します。次に、承認を完了し、構成を保存します。例えば：

    ![Sample Step 3](/media/dashboard/dashboard-session-sso-okta-info-3.png)

これで、サインインに Okta SSO を使用するように TiDB ダッシュボードが構成されました。

## 例 2: TiDB ダッシュボードの SSO サインインに Auth0 を使用する {#example-2-use-auth0-for-tidb-dashboard-sso-sign-in}

Okta と同様に、 [Auth0](https://auth0.com/)も OIDC SSO ID サービスを提供します。次の手順では、Auth0 を TiDB ダッシュボード SSO プロバイダーとして使用できるように、Auth0 と TiDB ダッシュボードを構成する方法について説明します。

### ステップ 1: Auth0 を構成する {#step-1-configure-auth0}

1.  Auth0 管理サイトにアクセスします。

2.  左側のサイドバーの**[アプリケーション]** &gt; <strong>[アプリケーション]</strong>に移動します。

3.  **[アプリ統合の作成]**をクリックします。

    ![Create Application](/media/dashboard/dashboard-session-sso-auth0-create-app.png)

    ポップアップしたダイアログで、「TiDB ダッシュボード」などの**名前**を入力します。 <strong>Choose an application type</strong>で<strong>Single Page Web Applications を</strong>選択します。 <strong>[作成]</strong>をクリックします。

4.  **[設定]**をクリックします。

    ![Settings](/media/dashboard/dashboard-session-sso-auth0-settings-1.png)

5.  **許可されたコールバック URL を**次のように入力します。

    ```
    http://DASHBOARD_IP:PORT/dashboard/?sso_callback=1
    ```

    `DASHBOARD_IP:PORT`ブラウザで TiDB ダッシュボードにアクセスするために使用する実際のドメイン (または IP アドレス) とポートに置き換えます。

6.  **許可されたログアウト URL を**次のように入力します。

    ```
    http://DASHBOARD_IP:PORT/dashboard/
    ```

    同様に、 `DASHBOARD_IP:PORT`実際のドメイン (または IP アドレス) とポートに置き換えます。

    ![Settings](/media/dashboard/dashboard-session-sso-auth0-settings-2.png)

7.  その他の設定はデフォルト値のままにして、 **[Save Changes]**をクリックします。

### ステップ 2: OIDC 情報を取得し、TiDB ダッシュボードに入力する {#step-2-obtain-oidc-information-and-fill-in-tidb-dashboard}

1.  TiDB ダッシュボードの**OIDC クライアント ID**に、Auth0 の<strong>[設定]</strong>タブの<strong>[基本情報]</strong>にある<strong>クライアント ID</strong>を入力します。

2.  **OIDC 検出 URL**に、接頭辞`https://`と接尾辞`/`を付けた<strong>Domain</strong>フィールド値を入力します (例: `https://example.us.auth0.com/` )。承認を完了し、構成を保存します。

    ![Settings](/media/dashboard/dashboard-session-sso-auth0-settings-3.png)

これで、サインインに Auth0 SSO を使用するように TiDB ダッシュボードが構成されました。

## 例 3: TiDB ダッシュボードの SSO サインインに Casdoor を使用する {#example-3-use-casdoor-for-tidb-dashboard-sso-sign-in}

[カスドア](https://casdoor.org/)は、独自のホストにデプロイできるオープンソースの SSO プラットフォームです。 TiDB ダッシュボードの SSO 機能と互換性があります。次の手順では、Casdoor を TiDB ダッシュボード SSO プロバイダーとして使用できるように Casdoor と TiDB ダッシュボードを構成する方法について説明します。

### ステップ 1: Casdoor を構成する {#step-1-configure-casdoor}

1.  Casdoor 管理サイトをデプロイてアクセスします。

2.  上部のサイドバー**アプリケーション**から移動します。

3.  **[アプリケーション - 追加]**をクリックします。 ![Settings](/media/dashboard/dashboard-session-sso-casdoor-settings-1.png)

4.  **名前**と<strong>表示名</strong>を入力します (例: <strong>TiDB Dashboard</strong> )。

5.  次のように**リダイレクト URL**を追加します。

    ```
    http://DASHBOARD_IP:PORT/dashboard/?sso_callback=1
    ```

    `DASHBOARD_IP:PORT`ブラウザで TiDB ダッシュボードにアクセスするために使用する実際のドメイン (または IP アドレス) とポートに置き換えます。

    ![Settings](/media/dashboard/dashboard-session-sso-casdoor-settings-2.png)

6.  他の設定はデフォルト値のままにして、 **[保存して終了]**をクリックします。

7.  ページに表示された**クライアント ID**を保存します。

### ステップ 2: OIDC 情報を取得し、TiDB ダッシュボードに入力する {#step-2-obtain-oidc-information-and-fill-in-tidb-dashboard}

1.  TiDB ダッシュボードの**OIDC クライアント ID**に、前の手順で保存した<strong>クライアント ID</strong>を入力します。

2.  **OIDC 検出 URL**に、接頭辞`https://`と接尾辞`/`を付けた<strong>Domain</strong>フィールド値を入力します (例: `https://casdoor.example.com/` )。承認を完了し、構成を保存します。

    ![Settings](/media/dashboard/dashboard-session-sso-casdoor-settings-3.png)

これで、サインインに Casdoor SSO を使用するように TiDB ダッシュボードが構成されました。
