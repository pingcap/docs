---
title: Access TiDB Dashboard
summary: Learn how to access TiDB Dashboard.
---

# TiDB ダッシュボードにアクセスする {#access-tidb-dashboard}

TiDB ダッシュボードにアクセスするには、ブラウザから[<a href="http://127.0.0.1:2379/dashboard">http://127.0.0.1:2379/ダッシュボード</a>](http://127.0.0.1:2379/dashboard)にアクセスしてください。 `127.0.0.1:2379`を実際の PD インスタンスのアドレスとポートに置き換えます。

> **ノート：**
>
> TiDB v6.5.0 (以降) およびTiDB Operator v1.4.0 (以降) は、Kubernetes 上の独立したポッドとして TiDB ダッシュボードをデプロイすることをサポートしています。 TiDB Operatorを使用すると、このポッドの IP アドレスにアクセスして TiDB ダッシュボードを起動できます。詳細は[<a href="https://docs.pingcap.com/tidb-in-kubernetes/dev/get-started#deploy-tidb-dashboard-independently">TiDB Operatorで TiDB ダッシュボードを独立してデプロイ</a>](https://docs.pingcap.com/tidb-in-kubernetes/dev/get-started#deploy-tidb-dashboard-independently)を参照してください。

## 複数の PD インスタンスがデプロイされている場合に TiDB ダッシュボードにアクセスする {#access-tidb-dashboard-when-multiple-pd-instances-are-deployed}

クラスターに複数の PD インスタンスがデプロイされており、**すべての**PD インスタンスとポートに直接アクセスできる場合は、 [<a href="http://127.0.0.1:2379/dashboard/">http://127.0.0.1:2379/ダッシュボード/</a>](http://127.0.0.1:2379/dashboard/)アドレスの`127.0.0.1:2379`任意**の**PD インスタンスのアドレスとポートに置き換えるだけで済みます。

> **ノート：**
>
> ファイアウォールまたはリバース プロキシが構成されており、すべての PD インスタンスに直接アクセスできない場合は、TiDB ダッシュボードにアクセスできない可能性があります。通常、これはファイアウォールまたはリバース プロキシが正しく構成されていないことが原因です。複数の PD インスタンスがデプロイされている場合にファイアウォールまたはリバース プロキシを正しく構成する方法については、 [<a href="/dashboard/dashboard-ops-reverse-proxy.md">リバース プロキシの背後で TiDB ダッシュボードを使用する</a>](/dashboard/dashboard-ops-reverse-proxy.md)と[<a href="/dashboard/dashboard-ops-security.md">セキュリティTiDB ダッシュボード</a>](/dashboard/dashboard-ops-security.md)を参照してください。

## ブラウザの互換性 {#browser-compatibility}

TiDB ダッシュボードは、次の比較的新しいバージョンの一般的なデスクトップ ブラウザーで使用できます。

-   クロム &gt;= 77
-   Firefox &gt;= 68
-   エッジ &gt;= 17

> **ノート：**
>
> 上記の以前のバージョンのブラウザまたは他のブラウザを使用して TiDB ダッシュボードにアクセスすると、一部の関数が正しく動作しない可能性があります。

## ログイン {#sign-in}

TiDB ダッシュボードにアクセスすると、以下の図に示すように、ユーザー ログイン インターフェイスが表示されます。

-   TiDB `root`アカウントを使用して TiDB ダッシュボードにサインインできます。
-   [<a href="/dashboard/dashboard-user.md">ユーザー定義の SQL ユーザー</a>](/dashboard/dashboard-user.md)を作成した場合は、このアカウントと対応するパスワードを使用してサインインできます。

![Login interface](/media/dashboard/dashboard-access-login.png)

次のいずれかの状況が存在する場合、ログインが失敗する可能性があります。

-   TiDB `root`ユーザーは存在しません。
-   PD が開始されていないか、アクセスできません。
-   TiDB が起動していないか、アクセスできません。
-   パスワードが`root`間違っています。

サインインすると、セッションは 24 時間以内は有効です。サインアウトする方法については、 [<a href="#logout">ログアウト</a>](#logout)セクションを参照してください。

## 言語を切り替える {#switch-language}

TiDB ダッシュボードでは次の言語がサポートされています。

-   英語
-   中国語（簡体字）

**[SQL ユーザー サインイン]**ページで、 **[言語の**切り替え] ドロップダウン リストをクリックしてインターフェイス言語を切り替えることができます。

![Switch language](/media/dashboard/dashboard-access-switch-language.png)

## ログアウト {#logout}

ログインしたら、左側のナビゲーション バーでログイン ユーザー名をクリックしてユーザー ページに切り替えます。ユーザーページの**「ログアウト」**ボタンをクリックして、現在のユーザーをログアウトします。ログアウトした後、ユーザー名とパスワードを再入力する必要があります。

![Logout](/media/dashboard/dashboard-access-logout.png)
