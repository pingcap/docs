---
title: Configure SSO for TiDB Dashboard
summary: TiDB ダッシュボードは、サインイン認証に OIDC ベースの SSO をサポートしています。SSO を有効にするには、OIDC クライアント ID と検出 URL を入力し、偽装を承認して、構成を保存します。SSO を無効にするには、オプションの選択を解除して構成を更新します。SQL ユーザーのパスワードが変更された場合は、パスワードを再入力して SSO を再度有効にします。構成後、「会社のアカウントでサインイン」をクリックしてサインイン プロセスを完了し、SSO 経由でサインインします。SSO 構成に Okta、Auth0、および Casdoor を使用する例が提供されています。
---

# TiDB ダッシュボードの SSO を構成する {#configure-sso-for-tidb-dashboard}

TiDB ダッシュボードは、 [国際データセンター](https://openid.net/connect/)ベースのシングル サインオン (SSO) をサポートしています。TiDB ダッシュボードの SSO 機能を有効にすると、構成された SSO サービスがサインイン認証に使用され、SQL ユーザー パスワードを入力せずに TiDB ダッシュボードにアクセスできるようになります。

## OIDC SSO を構成する {#configure-oidc-sso}

### SSOを有効にする {#enable-sso}

1.  TiDB ダッシュボードにサインインします。

2.  左側のサイドバーにあるユーザー名をクリックして、設定ページにアクセスします。

3.  **「シングル サインオン」**セクションで、 **「有効」を選択して、TiDB ダッシュボードにサインインするときに SSO を使用します**。

4.  フォームの**OIDC クライアント ID**と**OIDC 検出 URL**フィールドに入力します。

    通常、SSO サービス プロバイダーから次の 2 つのフィールドを取得できます。

    -   OIDC クライアント ID は、OIDC トークン発行者とも呼ばれます。
    -   OIDC Discovery URL は、OIDC Token Audience とも呼ばれます。

5.  **「偽装の承認」**をクリックし、SQL パスワードを入力します。

    TiDB ダッシュボードはこの SQL パスワードを保存し、SSO サインインが完了した後に通常の SQL サインインを偽装するために使用します。

    ![Sample Step](/media/dashboard/dashboard-session-sso-enable-1.png)

    > **注記：**
    >
    > 入力したパスワードは暗号化されて保存されます。SQL ユーザーのパスワードが変更されると、SSO サインインは失敗します。この場合、パスワードを再入力して SSO を復元できます。

6.  **「承認して保存」**をクリックします。

    ![Sample Step](/media/dashboard/dashboard-session-sso-enable-2.png)

7.  設定を保存するには、 **[**更新] をクリックします。

    ![Sample Step](/media/dashboard/dashboard-session-sso-enable-3.png)

TiDB ダッシュボードで SSO サインインが有効になりました。

> **注記：**
>
> セキュリティ上の理由から、一部の SSO サービスでは、信頼できるサインイン URI やサインアウト URI など、SSO サービスの追加構成が必要になります。詳細については、SSO サービスのドキュメントを参照してください。

### SSOを無効にする {#disable-sso}

SSO を無効にすると、保存されている SQL パスワードが完全に消去されます。

1.  TiDB ダッシュボードにサインインします。

2.  左側のサイドバーにあるユーザー名をクリックして、設定ページにアクセスします。

3.  **「シングル サインオン」**セクションで、 **「TiDB ダッシュボードにサインインするときに SSO を使用する」の**選択を解除します。

4.  設定を保存するには、 **[**更新] をクリックします。

    ![Sample Step](/media/dashboard/dashboard-session-sso-disable.png)

### パスワード変更後にパスワードを再入力してください {#re-enter-the-password-after-a-password-change}

SQL ユーザーのパスワードが変更されると、SSO サインインは失敗します。この場合、SQL パスワードを再入力することで SSO サインインを復元できます。

1.  TiDB ダッシュボードにサインインします。

2.  左側のサイドバーにあるユーザー名をクリックして、設定ページにアクセスします。

3.  **[シングル サインオン]**セクションで、 **[偽装の承認]**をクリックし、更新された SQL パスワードを入力します。

    ![Sample Step](/media/dashboard/dashboard-session-sso-reauthorize.png)

4.  **「承認して保存」**をクリックします。

## SSO経由でサインイン {#sign-in-via-sso}

TiDB ダッシュボードに SSO が設定されると、次の手順に従って SSO 経由でサインインできます。

1.  TiDB ダッシュボードのサインイン ページで、 **[会社アカウント経由でサインイン] を**クリックします。

    ![Sample Step](/media/dashboard/dashboard-session-sso-signin.png)

2.  SSO サービスが設定されたシステムにサインインします。

3.  サインインを完了するために、TiDB ダッシュボードにリダイレクトされます。

## 例 1: TiDB ダッシュボードの SSO サインインに Okta を使用する {#example-1-use-okta-for-tidb-dashboard-sso-sign-in}

[オクタ](https://www.okta.com/) OIDC SSO アイデンティティ サービスであり、TiDB ダッシュボードの SSO 機能と互換性があります。以下の手順では、Okta を TiDB ダッシュボード SSO プロバイダーとして使用できるように Okta と TiDB ダッシュボードを構成する方法を示します。

### ステップ1: Oktaを構成する {#step-1-configure-okta}

まず、SSO を統合するための Okta アプリケーション統合を作成します。

1.  Okta 管理サイトにアクセスします。

2.  左側のサイドバーから**「アプリケーション」** &gt; **「アプリケーション」**に移動します。

3.  **「アプリ統合の作成」を**クリックします。

    ![Sample Step](/media/dashboard/dashboard-session-sso-okta-1.png)

4.  ポップアップダイアログで、**サインイン方法**で**OIDC - OpenID Connect**を選択します。

5.  **アプリケーションタイプ**で**シングルページアプリケーション**を選択します。

6.  **「次へ」**ボタンをクリックします。

    ![Sample Step](/media/dashboard/dashboard-session-sso-okta-2.png)

7.  **サインイン リダイレクト URI を**次のように入力します。

        http://DASHBOARD_IP:PORT/dashboard/?sso_callback=1

    `DASHBOARD_IP:PORT` 、ブラウザで TiDB ダッシュボードにアクセスするために使用する実際のドメイン (または IP アドレス) とポートに置き換えます。

8.  **サインアウト リダイレクト URI を**次のように入力します。

        http://DASHBOARD_IP:PORT/dashboard/

    同様に、 `DASHBOARD_IP:PORT`実際のドメイン (または IP アドレス) とポートに置き換えます。

    ![Sample Step](/media/dashboard/dashboard-session-sso-okta-3.png)

9.  **[割り当て**] フィールドで、組織内のどのタイプのユーザーに SSO サインインを許可するかを設定し、 **[保存]**をクリックして設定を保存します。

    ![Sample Step](/media/dashboard/dashboard-session-sso-okta-4.png)

### ステップ2: OIDC情報を取得し、TiDBダッシュボードに入力します {#step-2-obtain-oidc-information-and-fill-in-tidb-dashboard}

1.  Okta で作成したアプリケーション統合で、 **「サインオン」を**クリックします。

    ![Sample Step 1](/media/dashboard/dashboard-session-sso-okta-info-1.png)

2.  **OpenID Connect ID トークン**セクションから**Issuer**フィールドと**Audience**フィールドの値をコピーします。

    ![Sample Step 2](/media/dashboard/dashboard-session-sso-okta-info-2.png)

3.  TiDB ダッシュボードの設定ページを開き、前の手順で取得した**Issuer**を**OIDC クライアント ID**に入力し、 **Audience**を**OIDC 検出 URL**に入力します。次に、認証を完了して設定を保存します。例:

    ![Sample Step 3](/media/dashboard/dashboard-session-sso-okta-info-3.png)

これで、TiDB ダッシュボードはサインインに Okta SSO を使用するように構成されました。

## 例 2: TiDB ダッシュボードの SSO サインインに Auth0 を使用する {#example-2-use-auth0-for-tidb-dashboard-sso-sign-in}

Okta と同様に、 [作者0](https://auth0.com/)も OIDC SSO アイデンティティ サービスを提供します。次の手順では、Auth0 を TiDB ダッシュボード SSO プロバイダーとして使用できるように Auth0 と TiDB ダッシュボードを構成する方法について説明します。

### ステップ1: Auth0を構成する {#step-1-configure-auth0}

1.  Auth0 管理サイトにアクセスします。

2.  左側のサイドバーで**「アプリケーション」** &gt; **「アプリケーション」**に移動します。

3.  **「アプリ統合の作成」を**クリックします。

    ![Create Application](/media/dashboard/dashboard-session-sso-auth0-create-app.png)

    ポップアップ ダイアログで、**名前**(例:「TiDB Dashboard」) を入力します。**アプリケーションの種類の選択**で、**シングル ページ Web アプリケーション**を選択します。**作成を**クリックします。

4.  **[設定]を**クリックします。

    ![Settings](/media/dashboard/dashboard-session-sso-auth0-settings-1.png)

5.  **許可されたコールバック URL を**次のように入力します。

        http://DASHBOARD_IP:PORT/dashboard/?sso_callback=1

    `DASHBOARD_IP:PORT` 、ブラウザで TiDB ダッシュボードにアクセスするために使用する実際のドメイン (または IP アドレス) とポートに置き換えます。

6.  **許可されたログアウト URL を**次のように入力します。

        http://DASHBOARD_IP:PORT/dashboard/

    同様に、 `DASHBOARD_IP:PORT`実際のドメイン (または IP アドレス) とポートに置き換えます。

    ![Settings](/media/dashboard/dashboard-session-sso-auth0-settings-2.png)

7.  他の設定はデフォルト値のままにして、 **「変更を保存」**をクリックします。

### ステップ2: OIDC情報を取得し、TiDBダッシュボードに入力します {#step-2-obtain-oidc-information-and-fill-in-tidb-dashboard}

1.  Auth0 の**「設定」**タブの**「基本情報**」にある**クライアント**ID を、TiDB ダッシュボードの**OIDC クライアント ID**に入力します。

2.  **OIDC 検出 URL**に、 `https://`で始まり`/`で終わる**ドメイン**フィールド値 (例: `https://example.us.auth0.com/` ) を入力します。認証を完了し、構成を保存します。

    ![Settings](/media/dashboard/dashboard-session-sso-auth0-settings-3.png)

これで、TiDB ダッシュボードはサインインに Auth0 SSO を使用するように構成されました。

## 例 3: TiDB ダッシュボードの SSO サインインに Casdoor を使用する {#example-3-use-casdoor-for-tidb-dashboard-sso-sign-in}

[カスドア](https://casdoor.org/) 、独自のホストに導入できるオープンソースの SSO プラットフォームです。TiDB ダッシュボードの SSO 機能と互換性があります。次の手順では、Casdoor を TiDB ダッシュボード SSO プロバイダーとして使用できるように Casdoor と TiDB ダッシュボードを構成する方法について説明します。

### ステップ1: Casdoorを設定する {#step-1-configure-casdoor}

1.  Casdoor 管理サイトをデプロイてアクセスします。

2.  上部のサイドバーの**「アプリケーション」**から移動します。

3.  **アプリケーション - 追加を**クリックします![Settings](/media/dashboard/dashboard-session-sso-casdoor-settings-1.png)

4.  **名前**と**表示名**を入力します (例: **TiDB Dashboard)** 。

5.  次のように**リダイレクト URL**を追加します。

        http://DASHBOARD_IP:PORT/dashboard/?sso_callback=1

    `DASHBOARD_IP:PORT` 、ブラウザで TiDB ダッシュボードにアクセスするために使用する実際のドメイン (または IP アドレス) とポートに置き換えます。

    ![Settings](/media/dashboard/dashboard-session-sso-casdoor-settings-2.png)

6.  その他の設定はデフォルト値のままにして、 **「保存して終了」**をクリックします。

7.  ページに表示されている**クライアント ID**を保存します。

### ステップ2: OIDC情報を取得し、TiDBダッシュボードに入力します {#step-2-obtain-oidc-information-and-fill-in-tidb-dashboard}

1.  前の手順で保存した**クライアント ID**を TiDB ダッシュボードの**OIDC クライアント ID**に入力します。

2.  **OIDC 検出 URL**に、 `https://`で始まり`/`で終わる**ドメイン**フィールド値 (例: `https://casdoor.example.com/` ) を入力します。認証を完了し、構成を保存します。

    ![Settings](/media/dashboard/dashboard-session-sso-casdoor-settings-3.png)

これで、TiDB ダッシュボードはサインインに Casdoor SSO を使用するように構成されました。
