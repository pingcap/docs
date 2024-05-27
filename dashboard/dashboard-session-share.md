---
title: Share TiDB Dashboard Sessions
summary: TiDB ダッシュボードを使用すると、ユーザーは現在のセッションを他のユーザーと共有できるため、ユーザー パスワードは不要になります。招待者は、特定の共有設定で認証コードを生成し、招待者に提供できます。招待者は、認証コードを使用してパスワードなしでサインインできます。
---

# TiDBダッシュボードセッションを共有する {#share-tidb-dashboard-sessions}

TiDB ダッシュボードの現在のセッションを他のユーザーと共有して、他のユーザーがユーザー パスワードを入力せずに TiDB ダッシュボードにアクセスして操作できるようにすることができます。

## 招待者の手順 {#steps-for-the-inviter}

1.  TiDB ダッシュボードにサインインします。

2.  左側のサイドバーにあるユーザー名をクリックして、設定ページにアクセスします。

3.  **[現在のセッションを共有]を**クリックします。

    ![Sample Step](/media/dashboard/dashboard-session-share-settings-1-v650.png)

    > **注記：**
    >
    > セキュリティ上の理由から、共有されたセッションを再度共有することはできません。

4.  ポップアップダイアログで共有設定を調整します。

    -   有効期限: 共有セッションが有効な期間。現在のセッションからサインアウトしても、共有セッションの有効時間は影響を受けません。

    -   読み取り専用権限として共有: 共有セッションでは読み取り操作のみが許可され、書き込み操作 (構成の変更など) は許可されません。

5.  **「認証コードの生成」を**クリックします。

    ![Sample Step](/media/dashboard/dashboard-session-share-settings-2-v650.png)

6.  生成された**認証コードを、**セッションを共有するユーザーに提供します。

    ![Sample Step](/media/dashboard/dashboard-session-share-settings-3-v650.png)

    > **警告：**
    >
    > 認証コードは安全に保管し、信頼できない人には送信しないでください。そうしないと、あなたの許可なく TiDB ダッシュボードにアクセスして操作できるようになります。

## 招待される側の手順 {#steps-for-the-invitee}

1.  TiDB ダッシュボードのサインイン ページで、 **[代替認証の使用] を**クリックします。

    ![Sample Step](/media/dashboard/dashboard-session-share-signin-1-v650.png)

2.  **認証コード**をクリックしてサインインに使用します。

    ![Sample Step](/media/dashboard/dashboard-session-share-signin-2-v650.png)

3.  招待者から受け取った認証コードを入力します。

4.  **[サインイン]を**クリックします。

    ![Sample Step](/media/dashboard/dashboard-session-share-signin-3-v650.png)
