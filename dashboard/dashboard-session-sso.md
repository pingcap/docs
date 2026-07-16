---
title: Configure SSO for TiDB Dashboard
summary: TiDB Dashboardは、サインイン認証にOIDCベースのSSOをサポートしています。SSOを有効にするには、OIDCクライアントIDと検出URLを入力し、偽装を承認して設定を保存します。SSOを無効にするには、オプションの選択を解除して設定を更新します。SQLユーザーのパスワードが変更された場合は、パスワードを再入力してSSOを再度有効にしてください。設定後、「会社アカウントでサインイン」をクリックしてサインインプロセスを完了することで、SSO経由でサインインできます。Okta、Auth0、Casdoorを使用したSSO設定の例も提供されています。
---

# TiDB DashboardのSSOを構成する {#configure-sso-for-tidb-dashboard}

TiDB Dashboardは、SQLベースの[OIDC](https://openid.net/connect/)サインオン（SSO）をサポートしています。TiDB DashboardのSSO機能を有効にすると、設定されたSSOサービスがサインイン認証に使用され、SQLユーザーのパスワードを入力せずにTiDB Dashboardにアクセスできるようになります。

## OIDC SSO を構成する {#configure-oidc-sso}

### SSOを有効にする {#enable-sso}

1.  TiDB Dashboardにサインインします。

2.  左側のサイドバーにあるユーザー名をクリックして、設定ページにアクセスします。

3.  **[シングル サインオン]**セクションで、 **[有効にする] を選択して、TiDB Dashboardにサインインするときに SSO を使用します**。

    > **Note:**
    >
    > アカウントに`SYSTEM_VARIABLES_ADMIN`権限がない場合、 **「TiDB Dashboardへのサインイン時にSSOを有効にする」**オプションは無効になります。権限の詳細については、 [TiDB Dashboardのユーザー管理](/dashboard/dashboard-user.md)ご覧ください。

4.  フォームの**OIDC クライアント ID**と**OIDC 検出 URL**フィールドに入力します。

    通常、SSO サービス プロバイダーから次の 2 つのフィールドを取得できます。

    -   OIDC クライアント ID は、OIDC トークン発行者とも呼ばれます。
    -   OIDC Discovery URL は、OIDC Token Audience とも呼ばれます。

5.  **「偽装の承認」**をクリックし、SQL パスワードを入力します。

    TiDB Dashboardはこの SQL パスワードを保存し、SSO サインインが完了した後に通常の SQL サインインを偽装するために使用します。

    ![Sample Step](/media/dashboard/dashboard-session-sso-enable-1.png)

    > **Note:**
    >
    > 入力したパスワードは暗号化されて保存されます。SQLユーザーのパスワードを変更すると、SSOサインインが失敗します。その場合は、パスワードを再入力することでSSOを復旧できます。

6.  **[承認して保存]を**クリックします。

    ![Sample Step](/media/dashboard/dashboard-session-sso-enable-2.png)

7.  設定を保存するには、 **[**更新] (Update) をクリックします。

    ![Sample Step](/media/dashboard/dashboard-session-sso-enable-3.png)

TiDB Dashboardで SSO サインインが有効になりました。

> **Note:**
>
> セキュリティ上の理由から、一部のSSOサービスでは、信頼できるサインインおよびサインアウトURIなど、SSOサービスに追加の設定が必要です。詳細については、SSOサービスのドキュメントを参照してください。

### SSOを無効にする {#disable-sso}

SSO を無効にすると、保存されている SQL パスワードが完全に消去されます。

1.  TiDB Dashboardにサインインします。

2.  左側のサイドバーにあるユーザー名をクリックして、設定ページにアクセスします。

3.  **[シングル サインオン]**セクションで、 **[TiDB Dashboardにサインインするときに SSO を使用する] の**選択を解除します。

4.  設定を保存するには、 **[**更新] (Update) をクリックします。

    ![Sample Step](/media/dashboard/dashboard-session-sso-disable.png)

### パスワード変更後にパスワードを再入力してください {#re-enter-the-password-after-a-password-change}

SQLユーザーのパスワードを変更すると、SSOサインインは失敗します。この場合、SQLパスワードを再入力することでSSOサインインを再開できます。

1.  TiDB Dashboardにサインインします。

2.  左側のサイドバーにあるユーザー名をクリックして、設定ページにアクセスします。

3.  **[シングル サインオン]**セクションで、 **[偽装の承認]**をクリックし、更新された SQL パスワードを入力します。

    ![Sample Step](/media/dashboard/dashboard-session-sso-reauthorize.png)

4.  **[承認して保存]を**クリックします。

## SSO経由でサインイン {#sign-in-via-sso}

TiDB Dashboardに SSO が設定されると、次の手順に従って SSO 経由でサインインできます。

1.  TiDB Dashboardのサインイン ページで、 **[会社アカウントでサインイン] を**クリックします。

    ![Sample Step](/media/dashboard/dashboard-session-sso-signin.png)

2.  SSO サービスが設定されたシステムにサインインします。

3.  サインインを完了するために、TiDB Dashboardにリダイレクトされます。

## 例 1: TiDB Dashboardの SSO サインインに Okta を使用する {#example-1-use-okta-for-tidb-dashboard-sso-sign-in}

[Okta](https://www.okta.com/)はOIDC SSOアイデンティティサービスであり、TiDB DashboardのSSO機能と互換性があります。以下の手順では、OktaをTiDB DashboardのSSOプロバイダーとして使用できるように、OktaとTiDB Dashboardを設定する方法を説明します。

### ステップ1: Oktaを構成する {#step-1-configure-okta}

まず、SSO を統合するための Okta アプリケーション統合を作成します。

1.  Okta 管理サイトにアクセスします。

2.  左側のサイドバーから**「アプリケーション」** &gt; **「アプリケーション」に**移動します。

3.  **「アプリ統合の作成」を**クリックします。

    ![Sample Step](/media/dashboard/dashboard-session-sso-okta-1.png)

4.  ポップアップされたダイアログで、**サインイン方法**で**OIDC - OpenID Connect**を選択します。

5.  **アプリケーションの種類**で**シングルページ アプリケーション**を選択します。

6.  **「次へ」**ボタンをクリックします。

    ![Sample Step](/media/dashboard/dashboard-session-sso-okta-2.png)

7.  **サインイン リダイレクト URI を**次のように入力します。

        http://DASHBOARD_IP:PORT/dashboard/?sso_callback=1

    `DASHBOARD_IP:PORT` 、ブラウザで TiDB Dashboardにアクセスするために使用する実際のドメイン (または IP アドレス) とポートに置き換えます。

8.  **サインアウトリダイレクト URI を**次のように入力します。

        http://DASHBOARD_IP:PORT/dashboard/

    同様に、 `DASHBOARD_IP:PORT`実際のドメイン (または IP アドレス) とポートに置き換えます。

    ![Sample Step](/media/dashboard/dashboard-session-sso-okta-3.png)

9.  **[割り当て]**フィールドで、組織内のどのタイプのユーザーに SSO サインインを許可するかを構成し、 **[保存]**をクリックして構成を保存します。

    ![Sample Step](/media/dashboard/dashboard-session-sso-okta-4.png)

### ステップ2: OIDC情報を取得し、TiDB Dashboardに入力します {#step-2-obtain-oidc-information-and-fill-in-tidb-dashboard}

1.  Okta で作成したアプリケーション統合で、 **[サインオン]**をクリックします。

    ![Sample Step 1](/media/dashboard/dashboard-session-sso-okta-info-1.png)

2.  **OpenID Connect ID トークン**セクションから**Issuer フィールド**と**Audience**フィールドの値をコピーします。

    ![Sample Step 2](/media/dashboard/dashboard-session-sso-okta-info-2.png)

3.  TiDB Dashboardの設定ページを開き、 **OIDCクライアントID**に前の手順で取得した**Issuer**を入力し、 **OIDCディスカバリURL**に**Audience**を入力します。その後、認証を完了し、設定を保存します。例：

    ![Sample Step 3](/media/dashboard/dashboard-session-sso-okta-info-3.png)

これで、TiDB Dashboardはサインインに Okta SSO を使用するように構成されました。

## 例2: TiDB DashboardのSSOサインインにAuth0を使用する {#example-2-use-auth0-for-tidb-dashboard-sso-sign-in}

Oktaと同様に、 [オーソ0](https://auth0.com/)もOIDC SSOアイデンティティサービスを提供します。以下の手順では、Auth0をTiDB DashboardのSSOプロバイダーとして使用できるように、Auth0とTiDB Dashboardを設定する方法について説明します。

### ステップ1: Auth0を構成する {#step-1-configure-auth0}

1.  Auth0 管理サイトにアクセスします。

2.  左側のサイドバーで**「アプリケーション」** &gt; **「アプリケーション」**に移動します。

3.  **「アプリ統合の作成」を**クリックします。

    ![Create Application](/media/dashboard/dashboard-session-sso-auth0-create-app.png)

    ポップアップダイアログで、**名前**を入力します（例：「TiDB Dashboard」）。**アプリケーションの種類を選択**で**「シングルページWebアプリケーション」を**選択します。 **「作成」**をクリックします。

4.  **[設定]**をクリックします。

    ![Settings](/media/dashboard/dashboard-session-sso-auth0-settings-1.png)

5.  **許可されたコールバック URL**を次のように入力します。

        http://DASHBOARD_IP:PORT/dashboard/?sso_callback=1

    `DASHBOARD_IP:PORT` 、ブラウザで TiDB Dashboardにアクセスするために使用する実際のドメイン (または IP アドレス) とポートに置き換えます。

6.  **許可されたログアウト URL**を次のように入力します。

        http://DASHBOARD_IP:PORT/dashboard/

    同様に、 `DASHBOARD_IP:PORT`実際のドメイン (または IP アドレス) とポートに置き換えます。

    ![Settings](/media/dashboard/dashboard-session-sso-auth0-settings-2.png)

7.  その他の設定はデフォルト値のままにして、 **「変更を保存」**をクリックします。

### ステップ2: OIDC情報を取得し、TiDB Dashboardに入力します {#step-2-obtain-oidc-information-and-fill-in-tidb-dashboard}

1.  Auth0 の**[設定]**タブの**基本情報**の**クライアント****ID を、TiDB Dashboardの OIDC クライアント**ID に入力します。

2.  **OIDC検出URL**に、**ドメイン**フィールドの値の先頭に`https://` 、末尾に`/`入力します（例： `https://example.us.auth0.com/` ）。認証を完了し、設定を保存します。

    ![Settings](/media/dashboard/dashboard-session-sso-auth0-settings-3.png)

これで、TiDB Dashboardはサインインに Auth0 SSO を使用するように構成されました。

## 例3: TiDB DashboardのSSOサインインにCasdoorを使用する {#example-3-use-casdoor-for-tidb-dashboard-sso-sign-in}

[Casdoor](https://casdoor.org/) 、独自のホストに導入できるオープンソースのSSOプラットフォームです。TiDB DashboardのSSO機能と互換性があります。以下の手順では、CasdoorをTiDB DashboardのSSOプロバイダーとして使用できるように、CasdoorとTiDB Dashboardを設定する方法について説明します。

### ステップ1：Casdoorを設定する {#step-1-configure-casdoor}

1.  Casdoor 管理サイトをデプロイてアクセスします。

2.  上部のサイドバーの**「アプリケーション」**から移動します。

3.  **アプリケーション - 追加を**クリックします![Settings](/media/dashboard/dashboard-session-sso-casdoor-settings-1.png)

4.  **名前**と**表示名**を入力します (例: **TiDB Dashboard)** 。

5.  次のように**リダイレクト URL**を追加します。

        http://DASHBOARD_IP:PORT/dashboard/?sso_callback=1

    `DASHBOARD_IP:PORT` 、ブラウザで TiDB Dashboardにアクセスするために使用する実際のドメイン (または IP アドレス) とポートに置き換えます。

    ![Settings](/media/dashboard/dashboard-session-sso-casdoor-settings-2.png)

6.  その他の設定はデフォルト値のままにして、 **「保存して終了」**をクリックします。

7.  ページに表示されている**クライアント ID**を保存します。

### ステップ2: OIDC情報を取得し、TiDB Dashboardに入力します {#step-2-obtain-oidc-information-and-fill-in-tidb-dashboard}

1.  前の手順で保存した**クライアント ID**を TiDB Dashboardの**OIDC クライアント ID**に入力します。

2.  **OIDC検出URL**に、**ドメイン**フィールドの値の先頭に`https://` 、末尾に`/`入力します（例： `https://casdoor.example.com/` ）。認証を完了し、設定を保存します。

    ![Settings](/media/dashboard/dashboard-session-sso-casdoor-settings-3.png)

これで、TiDB Dashboardはサインインに Casdoor SSO を使用するように構成されました。
