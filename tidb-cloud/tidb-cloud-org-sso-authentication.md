---
title: Organization SSO Authentication
summary: カスタマイズされた組織認証を使用してTiDB Cloudコンソールにログインする方法を学びます。
---

# 組織のSSO認証 {#organization-sso-authentication}

シングル サインオン (SSO) は、 TiDB Cloud [組織](/tidb-cloud/tidb-cloud-glossary.md#organization)のメンバーが電子メール アドレスとパスワードの代わりに ID プロバイダー (IdP) の ID を使用してTiDB Cloudにログインできるようにする認証スキームです。

TiDB Cloud は、次の 2 種類の SSO 認証をサポートしています。

-   [基本的なSSO](/tidb-cloud/tidb-cloud-sso-authentication.md) : メンバーは、GitHub、Google、または Microsoft の認証方法を使用して[TiDB Cloudコンソール](https://tidbcloud.com/)にログインできます。基本 SSO は、 TiDB Cloudのすべての組織に対してデフォルトで有効になっています。

-   Cloud Organization SSO: メンバーは、組織で指定された認証方法を使用して、 TiDB Cloudのカスタム ログイン ページにログインできます。Cloud Organization SSO は、デフォルトでは無効になっています。

基本的な SSO と比較して、Cloud Organization SSO は柔軟性とカスタマイズ性に優れているため、組織のセキュリティとコンプライアンスの要件をより適切に満たすことができます。たとえば、ログイン ページに表示される認証方法を指定したり、ログインに許可されるメール アドレス ドメインを制限したり、 [OpenIDコネクト（OIDC）](https://openid.net/connect/)または[Securityアサーションマークアップ言語 (SAML)](https://en.wikipedia.org/wiki/Security_Assertion_Markup_Language) ID プロトコルを使用する ID プロバイダー (IdP) を使用してメンバーがTiDB Cloudにログインできるようにしたりできます。

このドキュメントでは、組織の認証スキームを基本 SSO から Cloud Organization SSO に移行する方法について説明します。

> **注記：**
>
> Cloud Organization SSO 機能は有料組織でのみご利用いただけます。

## 始める前に {#before-you-begin}

Cloud Organization SSO に移行する前に、組織についてこのセクションの項目を確認してください。

> **注記：**
>
> -   Cloud Organization SSO を有効にすると、無効にすることはできません。
> -   Cloud Organization SSO を有効にするには、 TiDB Cloud組織の`Organization Owner`ロールに属している必要があります。ロールの詳細については、 [ユーザーロール](/tidb-cloud/manage-user-access.md#user-roles)参照してください。

### 組織のTiDB CloudログインページのカスタムURLを決定します {#decide-a-custom-url-for-the-tidb-cloud-login-page-of-your-organization}

Cloud Organization SSO が有効になっている場合、メンバーはTiDB Cloudにログインするために、パブリック ログイン URL ( `https://tidbcloud.com` ) ではなくカスタム URL を使用する必要があります。

カスタム URL は有効化後に変更することはできないため、事前に使用する URL を決定する必要があります。

カスタム URL の形式は`https://tidbcloud.com/enterprise/signin/your-company-name`で、会社名をカスタマイズできます。

### 組織メンバーの認証方法を決定する {#decide-authentication-methods-for-your-organization-members}

TiDB Cloud は、組織 SSO に次の認証方法を提供します。

-   ユーザー名とパスワード
-   グーグル
-   GitHub
-   マイクロソフト
-   国際データセンター
-   サムエル

Cloud Organization SSO を有効にすると、最初の 4 つの方法がデフォルトで有効になります。組織で SSO の使用を強制する場合は、ユーザー名とパスワードの認証方法を無効にすることができます。

有効になっているすべての認証方法はカスタムTiDB Cloudログイン ページに表示されるため、事前に有効または無効にする認証方法を決定する必要があります。

### 自動プロビジョニングを有効にするかどうかを決定する {#decide-whether-to-enable-auto-provision}

自動プロビジョニングは、 `Organization Owner`または`Project Owner`からの招待を必要とせずにメンバーが組織に自動的に参加できるようにする機能です。 TiDB Cloudでは、サポートされているすべての認証方法でデフォルトで無効になっています。

-   認証方法の自動プロビジョニングが無効になっている場合、 `Organization Owner`または`Project Owner`によって招待されたユーザーのみがカスタム URL にログインできます。
-   認証方法の自動プロビジョニングが有効になっている場合、この認証方法を使用するすべてのユーザーはカスタム URL にログインできます。ログイン後、組織内のデフォルトの**メンバー**ロールが自動的に割り当てられます。

セキュリティ上の理由から、自動プロビジョニングを有効にする場合は、 [認証方法の詳細を設定する](#step-2-configure-authentication-methods)ときに認証に許可される電子メール ドメインを制限することをお勧めします。

### Cloud Organization SSO移行計画についてメンバーに通知する {#notify-your-members-about-the-cloud-organization-sso-migration-plan}

Cloud Organization SSO を有効にする前に、メンバーに次の点を必ず通知してください。

-   TiDB CloudのカスタムログインURL
-   ログインに`https://tidbcloud.com`代わりにカスタムログインURLを使い始める時間
-   利用可能な認証方法
-   メンバーがカスタム URL にログインするために招待が必要かどうか

## ステップ 1. クラウド組織の SSO を有効にする {#step-1-enable-cloud-organization-sso}

Cloud Organization SSO を有効にするには、次の手順を実行します。

1.  `Organization Owner`ロールを持つユーザーとして[TiDB Cloudコンソール](https://tidbcloud.com)にログインします。

2.  TiDB Cloudコンソールの左下隅で、<mdsvgicon name="icon-top-organization">をクリックし、**組織設定を**クリックします。</mdsvgicon>

3.  左側のナビゲーション ウィンドウで、 **[認証]**タブをクリックし、 **[有効化]**をクリックします。

4.  ダイアログで、組織のカスタム URL を入力します。この URL はTiDB Cloud内で一意である必要があります。

    > **注記：**
    >
    > Cloud Organization SSO を有効にすると、URL を変更できなくなります。組織のメンバーは、カスタム URL を使用してのみTiDB Cloudにログインできます。後で構成された URL を変更する必要がある場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)に連絡してサポートを受けてください。

5.  **[理解して確認します]**チェックボックスをクリックし、 **[有効にする]**をクリックします。

    > **注記：**
    >
    > ダイアログに、Cloud Organization SSO に再度招待して再度参加するユーザーのリストが含まれている場合、Cloud Organization SSO を有効にすると、 TiDB Cloud はそれらのユーザーに招待メールを自動的に送信します。招待メールを受信した後、各ユーザーはメール内のリンクをクリックして自分の ID を確認する必要があり、カスタム ログイン ページが表示されます。

## ステップ2. 認証方法を構成する {#step-2-configure-authentication-methods}

TiDB Cloudで認証方法を有効にすると、その方法を使用するメンバーはカスタム URL を使用してTiDB Cloudにログインできるようになります。

### ユーザー名とパスワード、Google、GitHub、またはMicrosoftの認証方法を設定します {#configure-username-and-password-google-github-or-microsoft-authentication-methods}

Cloud Organization Cloud を有効にした後、次のようにユーザー名とパスワード、Google、GitHub、または Microsoft の認証方法を構成できます。

1.  「**組織設定」**ページで、必要に応じて Google、GitHub、または Microsoft の認証方法を有効または無効にします。

2.  有効な認証方法の場合は、 <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 20H21M3.00003 20H4.67457C5.16376 20 5.40835 20 5.63852 19.9447C5.84259 19.8957 6.03768 19.8149 6.21663 19.7053C6.41846 19.5816 6.59141 19.4086 6.93732 19.0627L19.5001 6.49998C20.3285 5.67156 20.3285 4.32841 19.5001 3.49998C18.6716 2.67156 17.3285 2.67156 16.5001 3.49998L3.93729 16.0627C3.59139 16.4086 3.41843 16.5816 3.29475 16.7834C3.18509 16.9624 3.10428 17.1574 3.05529 17.3615C3.00003 17.5917 3.00003 17.8363 3.00003 18.3255V20Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>メソッドの詳細を設定します。

3.  メソッドの詳細では、以下を設定できます。

    -   [**自動プロビジョニングアカウント**](#decide-whether-to-enable-auto-provision)

        デフォルトでは無効になっています。必要に応じて有効にすることができます。セキュリティ上の理由から、自動プロビジョニングを有効にする場合は、認証に許可される電子メール ドメインを制限することをお勧めします。

    -   **許可されたメールドメイン**

        このフィールドが設定されると、この認証方法の指定された電子メール ドメインのみがカスタム URL を使用してTiDB Cloudにログインできるようになります。ドメイン名を入力するときは、 `@`記号を除外し、カンマで区切る必要があります。たとえば、 `company1.com,company2.com`です。

        > **注記：**
        >
        > 電子メール ドメインを構成している場合は、設定を保存する前に、 TiDB Cloudによってロックアウトされないように、現在ログインに使用している電子メール ドメインを必ず追加してください。

4.  **「保存」**をクリックします。

### OIDC認証方法を設定する {#configure-the-oidc-authentication-method}

OIDC ID プロトコルを使用する ID プロバイダーがある場合は、 TiDB Cloudログインに OIDC 認証方法を有効にすることができます。

TiDB Cloudでは、OIDC 認証方法はデフォルトで無効になっています。Cloud Organization Cloud を有効にした後、次のように OIDC 認証方法を有効にして構成できます。

1.  TiDB Cloud Organization SSO の ID プロバイダーから次の情報を取得します。

    -   発行者 URL
    -   クライアントID
    -   クライアントシークレット

2.  **組織設定**ページで、**認証**タブをクリックし、**認証方法**領域でOIDCの行を見つけて、 <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 20H21M3.00003 20H4.67457C5.16376 20 5.40835 20 5.63852 19.9447C5.84259 19.8957 6.03768 19.8149 6.21663 19.7053C6.41846 19.5816 6.59141 19.4086 6.93732 19.0627L19.5001 6.49998C20.3285 5.67156 20.3285 4.32841 19.5001 3.49998C18.6716 2.67156 17.3285 2.67156 16.5001 3.49998L3.93729 16.0627C3.59139 16.4086 3.41843 16.5816 3.29475 16.7834C3.18509 16.9624 3.10428 17.1574 3.05529 17.3615C3.00003 17.5917 3.00003 17.8363 3.00003 18.3255V20Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg> OIDC メソッドの詳細を表示します。

3.  メソッドの詳細では、以下を設定できます。

    -   **名前**

        カスタム ログイン ページに表示される OIDC 認証方法の名前を指定します。

    -   **発行者 URL** 、**クライアント ID** 、**クライアント シークレット**

        IdP から取得した対応する値を貼り付けます。

    -   [**自動プロビジョニングアカウント**](#decide-whether-to-enable-auto-provision)

        デフォルトでは無効になっています。必要に応じて有効にすることができます。セキュリティ上の理由から、自動プロビジョニングを有効にする場合は、認証に許可される電子メール ドメインを制限することをお勧めします。

    -   **許可されたメールドメイン**

        このフィールドが設定されると、この認証方法の指定された電子メール ドメインのみがカスタム URL を使用してTiDB Cloudにログインできるようになります。ドメイン名を入力するときは、 `@`記号を除外し、カンマで区切る必要があります。たとえば、 `company1.com,company2.com`です。

        > **注記：**
        >
        > 電子メール ドメインを構成している場合は、設定を保存する前に、 TiDB Cloudによってロックアウトされないように、現在ログインに使用している電子メール ドメインを必ず追加してください。

4.  **「保存」**をクリックします。

### SAML認証方法を設定する {#configure-the-saml-authentication-method}

SAML ID プロトコルを使用する ID プロバイダーがある場合は、 TiDB Cloudログインに SAML 認証方法を有効にすることができます。

> **注記：**
>
> TiDB Cloud は、異なるユーザーの一意の識別子として電子メール アドレスを使用します。したがって、組織メンバーの`email`属性が ID プロバイダーで設定されていることを確認してください。

TiDB Cloudでは、SAML 認証方法はデフォルトで無効になっています。Cloud Organization Cloud を有効にした後、次のように SAML 認証方法を有効にして構成できます。

1.  TiDB Cloud Organization SSO の ID プロバイダーから次の情報を取得します。

    -   サインオンURL
    -   署名証明書

2.  **組織設定**ページで、左側のナビゲーションペインの**認証**タブをクリックし、**認証方法**領域でSAMLの行を見つけて、 <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 20H21M3.00003 20H4.67457C5.16376 20 5.40835 20 5.63852 19.9447C5.84259 19.8957 6.03768 19.8149 6.21663 19.7053C6.41846 19.5816 6.59141 19.4086 6.93732 19.0627L19.5001 6.49998C20.3285 5.67156 20.3285 4.32841 19.5001 3.49998C18.6716 2.67156 17.3285 2.67156 16.5001 3.49998L3.93729 16.0627C3.59139 16.4086 3.41843 16.5816 3.29475 16.7834C3.18509 16.9624 3.10428 17.1574 3.05529 17.3615C3.00003 17.5917 3.00003 17.8363 3.00003 18.3255V20Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg> SAML メソッドの詳細を表示します。

3.  メソッドの詳細では、以下を設定できます。

    -   **名前**

        カスタム ログイン ページに表示される SAML 認証方法の名前を指定します。

    -   **サインオンURL**

        IdP から取得した URL を貼り付けます。

    -   **署名証明書**

        開始行`---begin certificate---`と終了行`---end certificate---`含む、IdP からの署名証明書全体を貼り付けます。

    -   [**自動プロビジョニングアカウント**](#decide-whether-to-enable-auto-provision)

        デフォルトでは無効になっています。必要に応じて有効にすることができます。セキュリティを考慮して、自動プロビジョニングを有効にする場合は、認証に許可される電子メール ドメインを制限することをお勧めします。

    -   **許可されたメールドメイン**

        このフィールドが設定されると、この認証方法の指定された電子メール ドメインのみがカスタム URL を使用してTiDB Cloudにログインできるようになります。ドメイン名を入力するときは、 `@`記号を除外し、カンマで区切る必要があります。たとえば、 `company1.com,company2.com`です。

        > **注記：**
        >
        > 電子メール ドメインを構成している場合は、設定を保存する前に、 TiDB Cloudによってロックアウトされないように、現在ログインに使用している電子メール ドメインを必ず追加してください。

    -   **SCIM プロビジョニング アカウント**

        デフォルトでは無効になっています。TiDB TiDB Cloud組織のユーザーとグループのプロビジョニング、プロビジョニング解除、および ID 管理を ID プロバイダーから一元化して自動化する場合は、有効にすることができます。詳細な構成手順については、 [SCIMプロビジョニングを構成する](#configure-scim-provisioning)参照してください。

4.  **「保存」**をクリックします。

#### SCIMプロビジョニングを構成する {#configure-scim-provisioning}

[クロスドメイン ID 管理システム (SCIM)](https://www.rfc-editor.org/rfc/rfc7644)は、アイデンティティ ドメインと IT システム間のユーザー アイデンティティ情報の交換を自動化するオープン スタンダードです。SCIM プロビジョニングを構成すると、アイデンティティ プロバイダーのユーザー グループをTiDB Cloudに自動的に同期し、 TiDB Cloudでこれらのグループの役割を一元管理できます。

> **注記：**
>
> SCIM プロビジョニングは[SAML認証方式](#configure-the-saml-authentication-method)でのみ有効にできます。

1.  TiDB Cloudで、 [SAML認証方式](#configure-the-saml-authentication-method)の**SCIM プロビジョニング アカウント**オプションを有効にし、後で使用するために次の情報を記録します。

    -   SCIM コネクタ ベース URL
    -   ユーザーの一意の識別子フィールド
    -   認証モード

2.  ID プロバイダーで、 TiDB Cloudの SCIM プロビジョニングを構成します。

    1.  ID プロバイダーで、 TiDB Cloud組織の SCIM プロビジョニングを SAML アプリ統合に追加します。

        たとえば、ID プロバイダーが Okta の場合は、 [アプリ統合にSCIMプロビジョニングを追加する](https://help.okta.com/en-us/content/topics/apps/apps_app_integration_wizard_scim.htm)参照してください。

    2.  SAML アプリ統合を ID プロバイダー内の目的のグループに割り当てて、グループのメンバーがアプリ統合にアクセスして使用できるようにします。

        たとえば、ID プロバイダーが Okta の場合は、 [アプリ統合をグループに割り当てる](https://help.okta.com/en-us/content/topics/provisioning/lcm/lcm-assign-app-groups.htm)参照してください。

    3.  アイデンティティ プロバイダーからTiDB Cloudにユーザー グループをプッシュします。

        たとえば、ID プロバイダーが Okta の場合は、 [グループプッシュを管理する](https://help.okta.com/en-us/content/topics/users-groups-profiles/usgp-group-push-main.htm)参照してください。

3.  TiDB Cloudで、ID プロバイダーからプッシュされたグループを表示します。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com)の左下隅にある<mdsvgicon name="icon-top-organization">をクリックし、**組織設定を**クリックします。</mdsvgicon>
    2.  左側のナビゲーション ペインで、 **[認証]**タブをクリックします。
    3.  **[グループ]**タブをクリックします。ID プロバイダーから同期されたグループが表示されます。
    4.  グループ内のユーザーを表示するには、 **「ビュー」**をクリックします。

4.  TiDB Cloudで、アイデンティティ プロバイダーからプッシュされたグループにロールを付与します。

    > **注記：**
    >
    > グループにロールを付与すると、グループ内のすべてのメンバーがそのロールを取得します。グループにTiDB Cloud組織にすでに存在するメンバーが含まれている場合、これらのメンバーもグループの新しいロールを取得します。

    1.  グループに組織ロールを付与するには、 **「組織別」を**クリックし、 **「組織ロール」**列でロールを構成します。組織ロールの権限の詳細については、 [組織の役割](/tidb-cloud/manage-user-access.md#organization-roles)参照してください。
    2.  グループにプロジェクト ロールを付与するには、 **[プロジェクト別] を**クリックし、 **[プロジェクト ロール]**列でロールを構成します。プロジェクト ロールの権限の詳細については、 [プロジェクトの役割](/tidb-cloud/manage-user-access.md#project-roles)参照してください。

5.  アイデンティティ プロバイダーでプッシュされたグループのメンバーを変更すると、これらの変更はTiDB Cloud内の対応するグループに動的に同期されます。

    -   アイデンティティ プロバイダーのグループに新しいメンバーが追加されると、これらのメンバーは対応するグループの役割を取得します。
    -   一部のメンバーが ID プロバイダーのグループから削除されると、これらのメンバーはTiDB Cloudの対応するグループからも削除されます。
