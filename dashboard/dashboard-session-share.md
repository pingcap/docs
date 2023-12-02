---
title: Share TiDB Dashboard Sessions
summary: Learn how to share the current TiDB Dashboard session to other users.
---

# TiDB ダッシュボード セッションを共有する {#share-tidb-dashboard-sessions}

TiDB ダッシュボードの現在のセッションを他のユーザーと共有すると、ユーザーはユーザー パスワードを入力せずに TiDB ダッシュボードにアクセスして操作できるようになります。

## 招待者の手順 {#steps-for-the-inviter}

1.  TiDB ダッシュボードにサインインします。

2.  左側のサイドバーでユーザー名をクリックして、設定ページにアクセスします。

3.  **[現在のセッションを共有]**をクリックします。

    ![Sample Step](/media/dashboard/dashboard-session-share-settings-1-v650.png)

    > **注記：**
    >
    > セキュリティ上の理由から、共有セッションを再度共有することはできません。

4.  ポップアップ ダイアログで共有設定を調整します。

    -   有効期限: 共有セッションが有効な期間。現在のセッションからサインアウトしても、共有セッションの有効時間には影響しません。

    -   読み取り専用権限として共有: 共有セッションでは読み取り操作のみが許可されますが、書き込み操作 (構成の変更など) は許可されません。

5.  **「認証コードの生成」**をクリックします。

    ![Sample Step](/media/dashboard/dashboard-session-share-settings-2-v650.png)

6.  生成された**認証コードを**セッションを共有するユーザーに提供します。

    ![Sample Step](/media/dashboard/dashboard-session-share-settings-3-v650.png)

    > **警告：**
    >
    > 認証コードは安全に保管し、信頼できない人には送信しないでください。そうしないと、ユーザーはあなたの許可なしに TiDB ダッシュボードにアクセスして操作できるようになります。

## 招待者の手順 {#steps-for-the-invitee}

1.  TiDB ダッシュボードのサインイン ページで、 **[代替認証を使用する]**をクリックします。

    ![Sample Step](/media/dashboard/dashboard-session-share-signin-1-v650.png)

2.  **「認証コード」**をクリックしてサインインに使用します。

    ![Sample Step](/media/dashboard/dashboard-session-share-signin-2-v650.png)

3.  招待者から受け取った認証コードを入力します。

4.  **「サインイン」**をクリックします。

    ![Sample Step](/media/dashboard/dashboard-session-share-signin-3-v650.png)
