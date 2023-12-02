---
title: Configure SSO for TiDB Dashboard
summary: Learn how to enable SSO to sign into TiDB Dashboard.
---

# TiDB ダッシュボードの SSO を構成する {#configure-sso-for-tidb-dashboard}

TiDB ダッシュボードは、 [OIDC](https://openid.net/connect/)ベースのシングル サインオン (SSO) をサポートしています。 TiDB ダッシュボードの SSO 機能を有効にすると、構成された SSO サービスがサインイン認証に使用され、SQL ユーザー パスワードを入力せずに TiDB ダッシュボードにアクセスできるようになります。

## OIDC SSO の構成 {#configure-oidc-sso}

### SSOを有効にする {#enable-sso}

1.  TiDB ダッシュボードにサインインします。

2.  左側のサイドバーでユーザー名をクリックして、設定ページにアクセスします。

3.  **「シングル サインオン」**セクションで、 **「TiDB ダッシュボードにサインインするときに SSO を使用するには有効にする」**を選択します。

4.  フォームの**「OIDC クライアント ID」フィールド**と**「OIDC Discovery URL」**フィールドに入力します。

    通常、次の 2 つのフィールドは SSO サービス プロバイダーから取得できます。

    -   OIDC クライアント ID は、OIDC トークン発行者とも呼ばれます。
    -   OIDC ディスカバリー URL は、OIDC トークン・オーディエンスとも呼ばれます。

5.  **「偽装の許可」**をクリックし、SQL パスワードを入力します。

    TiDB ダッシュボードはこの SQL パスワードを保存し、SSO サインインの完了後に通常の SQL サインインを偽装するために使用します。

    ![Sample Step](/media/dashboard/dashboard-session-sso-enable-1.png)

    > **注記：**
    >
    > 入力したパスワードは暗号化されて保存されます。 SQL ユーザーのパスワードを変更すると、SSO サインインが失敗します。この場合、パスワードを再入力して SSO を戻すことができます。

6.  **[承認して保存]**をクリックします。

    ![Sample Step](/media/dashboard/dashboard-session-sso-enable-2.png)

7.  **「更新」** (Update) をクリックして構成を保存します。

    ![Sample Step](/media/dashboard/dashboard-session-sso-enable-3.png)

これで、TiDB ダッシュボードに対して SSO サインインが有効になりました。

> **注記：**
>
> セキュリティ上の理由から、一部の SSO サービスでは、信頼されたサインイン URI やサインアウト URI など、SSO サービスの追加構成が必要です。詳細については、SSO サービスのドキュメントを参照してください。

### SSO を無効にする {#disable-sso}

SSO を無効にすると、保存されている SQL パスワードが完全に消去されます。

1.  TiDB ダッシュボードにサインインします。

2.  左側のサイドバーでユーザー名をクリックして、設定ページにアクセスします。

3.  **[シングル サインオン]**セクションで、 **[TiDB ダッシュボードにサインインするときに SSO を使用できるようにする] の**選択を解除します。

4.  **「更新」** (Update) をクリックして構成を保存します。

    ![Sample Step](/media/dashboard/dashboard-session-sso-disable.png)

### パスワード変更後はパスワードを再入力してください {#re-enter-the-password-after-a-password-change}

SQL ユーザーのパスワードが変更されると、SSO サインインは失敗します。この場合、SQL パスワードを再入力することで SSO サインインを戻すことができます。

1.  TiDB ダッシュボードにサインインします。

2.  左側のサイドバーでユーザー名をクリックして、設定ページにアクセスします。

3.  **[シングル サインオン]**セクションで、 **[偽装の承認]**をクリックし、更新された SQL パスワードを入力します。

    ![Sample Step](/media/dashboard/dashboard-session-sso-reauthorize.png)

4.  **[承認して保存]**をクリックします。

## SSO 経由でサインインする {#sign-in-via-sso}

TiDB ダッシュボードに SSO が設定されたら、次の手順を実行して SSO 経由でサインインできます。

1.  TiDB ダッシュボードのサインイン ページで、 **[会社アカウント経由でサインイン] を**クリックします。

    ![Sample Step](/media/dashboard/dashboard-session-sso-signin.png)

2.  SSO サービスが構成された状態でシステムにサインインします。

3.  TiDB ダッシュボードにリダイレクトされてサインインが完了します。

## 例 1: TiDB ダッシュボードの SSO サインインに Okta を使用する {#example-1-use-okta-for-tidb-dashboard-sso-sign-in}

[オクタ](https://www.okta.com/)は OIDC SSO アイデンティティ サービスであり、TiDB ダッシュボードの SSO 機能と互換性があります。以下の手順では、Okta を TiDB ダッシュボード SSO プロバイダーとして使用できるように Okta と TiDB ダッシュボードを構成する方法を示します。

### ステップ 1: Okta を構成する {#step-1-configure-okta}

まず、SSO を統合するための Okta アプリケーション統合を作成します。

1.  Okta 管理サイトにアクセスします。

2.  左側のサイドバーから**[アプリケーション]** &gt; **[アプリケーション]**に移動します。

3.  **[アプリ統合の作成]**をクリックします。

    ![Sample Step](/media/dashboard/dashboard-session-sso-okta-1.png)

4.  ポップアップされたダイアログで、 **「サインイン方法」**で**「OIDC - OpenID Connect」**を選択します。

5.  **[アプリケーション タイプ]**で**[シングル ページ アプリケーション]**を選択します。

6.  **「次へ」**ボタンをクリックします。

    ![Sample Step](/media/dashboard/dashboard-session-sso-okta-2.png)

7.  次のように**サインイン リダイレクト URI**を入力します。

        http://DASHBOARD_IP:PORT/dashboard/?sso_callback=1

    `DASHBOARD_IP:PORT`ブラウザで TiDB ダッシュボードにアクセスするために使用する実際のドメイン (または IP アドレス) とポートに置き換えます。

8.  次のように**サインアウト リダイレクト URI**を入力します。

        http://DASHBOARD_IP:PORT/dashboard/

    同様に、 `DASHBOARD_IP:PORT`実際のドメイン (または IP アドレス) とポートに置き換えます。

    ![Sample Step](/media/dashboard/dashboard-session-sso-okta-3.png)

9.  **[割り当て]**フィールドで、組織内のどのタイプのユーザーに SSO サインインを許可するかを構成し、 **[保存]**をクリックして構成を保存します。

    ![Sample Step](/media/dashboard/dashboard-session-sso-okta-4.png)

### ステップ 2: OIDC 情報を取得し、TiDB ダッシュボードに入力します {#step-2-obtain-oidc-information-and-fill-in-tidb-dashboard}

1.  Okta で作成したばかりのアプリケーション統合で、 **[サインオン]**をクリックします。

    ![Sample Step 1](/media/dashboard/dashboard-session-sso-okta-info-1.png)

2.  **「OpenID Connect ID トークン」**セクションから**「発行者」**フィールドと**「対象者」**フィールドの値をコピーします。

    ![Sample Step 2](/media/dashboard/dashboard-session-sso-okta-info-2.png)

3.  TiDB ダッシュボード構成ページを開き、 **OIDC クライアント ID**に最後のステップで取得した**発行者**を入力し、 **OIDC 検出 URL**に**Audience**を入力します。次に、認証を完了し、設定を保存します。例えば：

    ![Sample Step 3](/media/dashboard/dashboard-session-sso-okta-info-3.png)

これで、TiDB ダッシュボードはサインインに Okta SSO を使用するように構成されました。

## 例 2: TiDB ダッシュボードの SSO サインインに Auth0 を使用する {#example-2-use-auth0-for-tidb-dashboard-sso-sign-in}

Okta と同様に、 [認証0](https://auth0.com/)も OIDC SSO ID サービスを提供します。次の手順では、Auth0 を TiDB ダッシュボード SSO プロバイダーとして使用できるように、Auth0 と TiDB ダッシュボードを構成する方法について説明します。

### ステップ 1: Auth0 を構成する {#step-1-configure-auth0}

1.  Auth0管理サイトにアクセスします。

2.  左側のサイドバーで**[アプリケーション]** &gt; **[アプリケーション]**に移動します。

3.  **[アプリ統合の作成]**をクリックします。

    ![Create Application](/media/dashboard/dashboard-session-sso-auth0-create-app.png)

    ポップアップされたダイアログで、 **「名前**」を入力します (例: 「TiDB ダッシュボード」)。 **[アプリケーション タイプの選択]**で**[シングル ページ Web アプリケーション]**を選択します。 **「作成」**をクリックします。

4.  **[設定]**をクリックします。

    ![Settings](/media/dashboard/dashboard-session-sso-auth0-settings-1.png)

5.  次のように、**許可されたコールバック URL**を入力します。

        http://DASHBOARD_IP:PORT/dashboard/?sso_callback=1

    `DASHBOARD_IP:PORT`ブラウザで TiDB ダッシュボードにアクセスするために使用する実際のドメイン (または IP アドレス) とポートに置き換えます。

6.  **許可されたログアウト URL を**次のように入力します。

        http://DASHBOARD_IP:PORT/dashboard/

    同様に、 `DASHBOARD_IP:PORT`実際のドメイン (または IP アドレス) とポートに置き換えます。

    ![Settings](/media/dashboard/dashboard-session-sso-auth0-settings-2.png)

7.  他の設定についてはデフォルト値をそのまま使用し、 **「変更を保存」**をクリックします。

### ステップ 2: OIDC 情報を取得し、TiDB ダッシュボードに入力します {#step-2-obtain-oidc-information-and-fill-in-tidb-dashboard}

1.  TiDB ダッシュボードの**OIDC クライアント ID**に、Auth0 の**[設定]**タブの**[基本情報]**の**クライアント ID**を入力します。

2.  **OIDC Discovery URL**に、接頭辞`https://`と接尾辞`/`を付けた**Domain**フィールド値を入力します (例: `https://example.us.auth0.com/` 。認証を完了し、設定を保存します。

    ![Settings](/media/dashboard/dashboard-session-sso-auth0-settings-3.png)

これで、TiDB ダッシュボードはサインインに Auth0 SSO を使用するように構成されました。

## 例 3: TiDB ダッシュボードの SSO サインインに Casdoor を使用する {#example-3-use-casdoor-for-tidb-dashboard-sso-sign-in}

[カスドア](https://casdoor.org/)は、独自のホストに展開できるオープンソースの SSO プラットフォームです。 TiDB ダッシュボードの SSO 機能と互換性があります。次の手順では、Casdoor を TiDB ダッシュボード SSO プロバイダーとして使用できるように Casdoor と TiDB ダッシュボードを構成する方法について説明します。

### ステップ 1: Casdoor を構成する {#step-1-configure-casdoor}

1.  Casdoor 管理サイトをデプロイてアクセスします。

2.  上部のサイドバーから**[アプリケーション]**に移動します。

3.  **[アプリケーション] - [追加]**をクリックします。 ![Settings](/media/dashboard/dashboard-session-sso-casdoor-settings-1.png)

4.  **[名前]**と**[表示名]**を入力します (例: **TiDB Dashboard** )。

5.  次のように**リダイレクト URL**を追加します。

        http://DASHBOARD_IP:PORT/dashboard/?sso_callback=1

    `DASHBOARD_IP:PORT`ブラウザで TiDB ダッシュボードにアクセスするために使用する実際のドメイン (または IP アドレス) とポートに置き換えます。

    ![Settings](/media/dashboard/dashboard-session-sso-casdoor-settings-2.png)

6.  他の設定についてはデフォルト値をそのまま使用し、 **「保存して終了」**をクリックします。

7.  ページに表示された**クライアント ID**を保存します。

### ステップ 2: OIDC 情報を取得し、TiDB ダッシュボードに入力します {#step-2-obtain-oidc-information-and-fill-in-tidb-dashboard}

1.  TiDB ダッシュボードの**OIDC クライアント ID**に、前の手順で保存した**クライアント ID**を入力します。

2.  **OIDC Discovery URL**に、接頭辞`https://`と接尾辞`/`を付けた**Domain**フィールド値を入力します (例: `https://casdoor.example.com/` 。認証を完了し、設定を保存します。

    ![Settings](/media/dashboard/dashboard-session-sso-casdoor-settings-3.png)

これで、TiDB ダッシュボードはサインインに Casdoor SSO を使用するように構成されました。
