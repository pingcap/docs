---
title: Configure SSO for TiDB Dashboard
summary: Learn how to enable SSO to sign into TiDB Dashboard.
---

# TiDBダッシュボードのSSOを構成する {#configure-sso-for-tidb-dashboard}

TiDBダッシュボードは、 [OIDC](https://openid.net/connect/)ベースのシングルサインオン（SSO）をサポートします。 TiDBダッシュボードのSSO機能を有効にすると、構成済みのSSOサービスがサインイン認証に使用され、SQLユーザーパスワードを入力せずにTiDBダッシュボードにアクセスできるようになります。

## OIDCSSOを構成する {#configure-oidc-sso}

### SSOを有効にする {#enable-sso}

1.  TiDBダッシュボードにサインインします。

2.  左側のサイドバーのユーザー名をクリックして、構成ページにアクセスします。

3.  [**シングルサインオン**]セクションで、[ <strong>TiDBダッシュボードにサインインするときにSSOを使用するに</strong>は[有効にする]]を選択します。

4.  フォームの**OIDCクライアントID**フィールドと<strong>OIDCディスカバリーURL</strong>フィールドに入力します。

    通常、SSOサービスプロバイダーから2つのフィールドを取得できます。

    -   OIDCクライアントIDは、OIDCトークン発行者とも呼ばれます。
    -   OIDCディスカバリURLは、OIDCトークンオーディエンスとも呼ばれます。

5.  [**偽装の承認]**をクリックして、SQLパスワードを入力します。

    TiDBダッシュボードはこのSQLパスワードを保存し、SSOサインインが完了した後、これを使用して通常のSQLサインインになりすます。

    ![Sample Step](/media/dashboard/dashboard-session-sso-enable-1.png)

    > **ノート：**
    >
    > 入力したパスワードは暗号化されて保存されます。 SQLユーザーのパスワードが変更された後、SSOサインインは失敗します。この場合、パスワードを再入力してSSOを元に戻すことができます。

6.  [**承認して保存]を**クリックします。

    ![Sample Step](/media/dashboard/dashboard-session-sso-enable-2.png)

7.  [**更新**（更新）]をクリックして、構成を保存します。

    ![Sample Step](/media/dashboard/dashboard-session-sso-enable-3.png)

これで、TiDBダッシュボードでSSOサインインが有効になりました。

> **ノート：**
>
> セキュリティ上の理由から、一部のSSOサービスでは、信頼できるサインインおよびサインアウトURIなど、SSOサービスの追加構成が必要です。詳細については、SSOサービスのドキュメントを参照してください。

### SSOを無効にする {#disable-sso}

SSOを無効にすると、保存されているSQLパスワードが完全に消去されます。

1.  TiDBダッシュボードにサインインします。

2.  左側のサイドバーのユーザー名をクリックして、構成ページにアクセスします。

3.  [**シングルサインオン**]セクションで、 <strong>[TiDBダッシュボードにサインインするときにSSOを使用するには[有効にする]]</strong>の選択を解除します。

4.  [**更新**（更新）]をクリックして、構成を保存します。

    ![Sample Step](/media/dashboard/dashboard-session-sso-disable.png)

### パスワード変更後、パスワードを再入力してください {#re-enter-the-password-after-a-password-change}

SQLユーザーのパスワードが変更されると、SSOサインインは失敗します。この場合、SQLパスワードを再入力することにより、SSOサインインを元に戻すことができます。

1.  TiDBダッシュボードにサインインします。

2.  左側のサイドバーのユーザー名をクリックして、構成ページにアクセスします。

3.  [**シングルサインオン**]セクションで、[<strong>偽装の承認]</strong>をクリックし、更新されたSQLパスワードを入力します。

    ![Sample Step](/media/dashboard/dashboard-session-sso-reauthorize.png)

4.  [**承認して保存]を**クリックします。

## SSO経由でサインイン {#sign-in-via-sso}

TiDBダッシュボード用にSSOを構成したら、次の手順を実行してSSO経由でサインインできます。

1.  TiDBダッシュボードのサインインページで、[**会社のアカウントからサインイン**]をクリックします。

    ![Sample Step](/media/dashboard/dashboard-session-sso-signin.png)

2.  SSOサービスが構成された状態でシステムにサインインします。

3.  サインインを完了するために、TiDBダッシュボードにリダイレクトされます。

## 例1：TiDBダッシュボードのSSOサインインにOktaを使用する {#example-1-use-okta-for-tidb-dashboard-sso-sign-in}

[オクタ](https://www.okta.com/)はOIDCSSOIDサービスであり、TiDBダッシュボードのSSO機能と互換性があります。以下の手順は、OktaをTiDBダッシュボードSSOプロバイダーとして使用できるようにOktaとTiDBダッシュボードを構成する方法を示しています。

### ステップ1：Oktaを構成する {#step-1-configure-okta}

まず、SSOを統合するためのOktaアプリケーション統合を作成します。

1.  Okta管理サイトにアクセスします。

2.  左側のサイドバーから[**アプリケーション**]&gt;[<strong>アプリケーション</strong>]に移動します。

3.  [**アプリ統合の作成]**をクリックします。

    ![Sample Step](/media/dashboard/dashboard-session-sso-okta-1.png)

4.  ポップアップダイアログで、[ **OIDC]-[OpenID ConnectinSign** <strong>-inメソッド</strong>]を選択します。

5.  **アプリケーションタイプ**で<strong>シングルページアプリケーション</strong>を選択します。

6.  [**次へ**]ボタンをクリックします。

    ![Sample Step](/media/dashboard/dashboard-session-sso-okta-2.png)

7.  **サインインリダイレクトURI**を次のように入力します。

    ```
    http://DASHBOARD_IP:PORT/dashboard/?sso_callback=1
    ```

    `DASHBOARD_IP:PORT`を、ブラウザでTiDBダッシュボードにアクセスするために使用する実際のドメイン（またはIPアドレス）とポートに置き換えます。

8.  **サインアウトリダイレクトURI**を次のように入力します。

    ```
    http://DASHBOARD_IP:PORT/dashboard/
    ```

    同様に、 `DASHBOARD_IP:PORT`を実際のドメイン（またはIPアドレス）とポートに置き換えます。

    ![Sample Step](/media/dashboard/dashboard-session-sso-okta-3.png)

9.  組織内のどのタイプのユーザーにSSOサインインを許可するかを[**割り当て**]フィールドで構成し、[<strong>保存</strong>]をクリックして構成を保存します。

    ![Sample Step](/media/dashboard/dashboard-session-sso-okta-4.png)

### ステップ2：OIDC情報を取得し、TiDBダッシュボードに入力します {#step-2-obtain-oidc-information-and-fill-in-tidb-dashboard}

1.  Oktaで作成したばかりのアプリケーション統合で、[**サインオン**]をクリックします。

    ![Sample Step 1](/media/dashboard/dashboard-session-sso-okta-info-1.png)

2.  **OpenID ConnectIDToken**セクションから<strong>Issuer</strong>フィールドと<strong>Audience</strong>フィールドの値をコピーします。

    ![Sample Step 2](/media/dashboard/dashboard-session-sso-okta-info-2.png)

3.  TiDBダッシュボード構成ページを開き、最後の手順で取得した**発行者**を<strong>OIDCクライアントID</strong>に入力し、 <strong>OIDCディスカバリーURL</strong>に<strong>オーディエンス</strong>を入力します。次に、認証を終了し、構成を保存します。例えば：

    ![Sample Step 3](/media/dashboard/dashboard-session-sso-okta-info-3.png)

これで、TiDBダッシュボードはサインインにOktaSSOを使用するように構成されました。

## 例2：TiDBダッシュボードのSSOサインインにAuth0を使用する {#example-2-use-auth0-for-tidb-dashboard-sso-sign-in}

Oktaと同様に、 [Auth0](https://auth0.com/)もOIDCSSOIDサービスを提供します。次の手順では、Auth0をTiDBダッシュボードSSOプロバイダーとして使用できるようにAuth0とTiDBダッシュボードを構成する方法について説明します。

### ステップ1：Auth0を構成する {#step-1-configure-auth0}

1.  Auth0管理サイトにアクセスします。

2.  左側のサイドバー[**アプリケーション**]&gt;[<strong>アプリケーション</strong>]に移動します。

3.  [**アプリ統合の作成]**をクリックします。

    ![Create Application](/media/dashboard/dashboard-session-sso-auth0-create-app.png)

    ポップアップダイアログで、「**名前**」（「TiDBダッシュボード」など）を入力します。<strong>アプリケーションタイプの</strong>選択で<strong>シングルページWebアプリケーション</strong>を選択します。 [<strong>作成]</strong>をクリックします。

4.  [**設定]**をクリックします。

    ![Settings](/media/dashboard/dashboard-session-sso-auth0-settings-1.png)

5.  **許可されたコールバックURL**を次のように入力します。

    ```
    http://DASHBOARD_IP:PORT/dashboard/?sso_callback=1
    ```

    `DASHBOARD_IP:PORT`を、ブラウザでTiDBダッシュボードにアクセスするために使用する実際のドメイン（またはIPアドレス）とポートに置き換えます。

6.  **許可されたログアウトURL**を次のように入力します。

    ```
    http://DASHBOARD_IP:PORT/dashboard/
    ```

    同様に、 `DASHBOARD_IP:PORT`を実際のドメイン（またはIPアドレス）とポートに置き換えます。

    ![Settings](/media/dashboard/dashboard-session-sso-auth0-settings-2.png)

7.  他の設定のデフォルト値を保持し、[**変更を保存**]をクリックします。

### ステップ2：OIDC情報を取得し、TiDBダッシュボードに入力します {#step-2-obtain-oidc-information-and-fill-in-tidb-dashboard}

1.  Auth0の**[設定**]タブの[<strong>基本情報</strong>]に、TiDBダッシュボードの<strong>OIDCクライアントID</strong>に<strong>クライアント</strong>IDを入力します。

2.  **OIDC Discovery URL**に、プレフィックス`https://`とサフィックス`/`の<strong>ドメイン</strong>フィールド値を入力します（例： `https://example.us.auth0.com/` ）。承認を完了し、構成を保存します。

    ![Settings](/media/dashboard/dashboard-session-sso-auth0-settings-3.png)

これで、TiDBダッシュボードはサインインにAuth0SSOを使用するように構成されました。

## 例3：TiDBダッシュボードのSSOサインインにCasdoorを使用する {#example-3-use-casdoor-for-tidb-dashboard-sso-sign-in}

[キャスドア](https://casdoor.org/)は、独自のホストに展開できるオープンソースのSSOプラットフォームです。 TiDBダッシュボードのSSO機能と互換性があります。次の手順では、CasdoorをTiDBダッシュボードSSOプロバイダーとして使用できるようにCasdoorとTiDBダッシュボードを構成する方法について説明します。

### ステップ1：Casdoorを構成する {#step-1-configure-casdoor}

1.  Casdoor管理サイトをデプロイしてアクセスします。

2.  上部のサイドバー**アプリケーション**から移動します。

3.  [**アプリケーション]-[追加]を**クリックします。 ![Settings](/media/dashboard/dashboard-session-sso-casdoor-settings-1.png)

4.  塗りつぶし**名**と<strong>表示名</strong>（ <strong>TiDBダッシュボード</strong>など）。

5.  次のように**リダイレクトURL**を追加します。

    ```
    http://DASHBOARD_IP:PORT/dashboard/?sso_callback=1
    ```

    `DASHBOARD_IP:PORT`を、ブラウザでTiDBダッシュボードにアクセスするために使用する実際のドメイン（またはIPアドレス）とポートに置き換えます。

    ![Settings](/media/dashboard/dashboard-session-sso-casdoor-settings-2.png)

6.  他の設定のデフォルト値を保持し、[**保存して終了**]をクリックします。

7.  ページに表示されている**クライアントID**を保存します。

### ステップ2：OIDC情報を取得し、TiDBダッシュボードに入力します {#step-2-obtain-oidc-information-and-fill-in-tidb-dashboard}

1.  TiDBダッシュボードの**OIDCクライアントID**に、前の手順で保存した<strong>クライアントID</strong>を入力します。

2.  **OIDC Discovery URL**に、プレフィックス`https://`とサフィックス`/`の<strong>ドメイン</strong>フィールド値を入力します（例： `https://casdoor.example.com/` ）。承認を完了し、構成を保存します。

    ![Settings](/media/dashboard/dashboard-session-sso-casdoor-settings-3.png)

これで、TiDBダッシュボードはサインインにCasdoorSSOを使用するように構成されました。
