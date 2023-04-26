---
title: Access TiDB Dashboard
summary: Learn how to access TiDB Dashboard.
---

# TiDB ダッシュボードにアクセスする {#access-tidb-dashboard}

TiDB ダッシュボードにアクセスするには、ブラウザから[http://127.0.0.1:2379/ダッシュボード](http://127.0.0.1:2379/dashboard)にアクセスしてください。 `127.0.0.1:2379`を実際の PD インスタンスのアドレスとポートに置き換えます。

> **ノート：**
>
> TiDB v6.5.0 (およびそれ以降) およびTiDB Operator v1.4.0 (およびそれ以降) は、TiDB ダッシュボードを Kubernetes 上の独立した Pod としてデプロイすることをサポートしています。 TiDB Operatorを使用して、この Pod の IP アドレスにアクセスし、TiDB ダッシュボードを起動できます。詳細については、 [TiDB Operatorで TiDB ダッシュボードを個別にデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/dev/get-started#deploy-tidb-dashboard-independently)を参照してください。

## 複数の PD インスタンスがデプロイされている場合に TiDB ダッシュボードにアクセスする {#access-tidb-dashboard-when-multiple-pd-instances-are-deployed}

複数の複数の PD インスタンスがクラスターにデプロイされ、**すべての**PD インスタンスとポートに直接アクセスできる場合、 `127.0.0.1:2379` in the [http://127.0.0.1:2379/ダッシュボード/](http://127.0.0.1:2379/dashboard/)アドレスを<strong>任意の</strong>PD インスタンスのアドレスとポートに置き換えるだけです。

> **ノート：**
>
> ファイアウォールまたはリバース プロキシが構成されていて、すべての PD インスタンスに直接アクセスできない場合、TiDB ダッシュボードにアクセスできない可能性があります。通常、これは、ファイアウォールまたはリバース プロキシが正しく構成されていないことが原因です。複数の PD インスタンスがデプロイされている場合にファイアウォールまたはリバース プロキシを正しく構成する方法については、 [リバース プロキシの背後で TiDB ダッシュボードを使用する](/dashboard/dashboard-ops-reverse-proxy.md)と[セキュリティTiDB ダッシュボード](/dashboard/dashboard-ops-security.md)を参照してください。

## ブラウザの互換性 {#browser-compatibility}

TiDB ダッシュボードは、比較的新しいバージョンの次の一般的なデスクトップ ブラウザーで使用できます。

-   クローム &gt;= 77
-   Firefox &gt;= 68
-   エッジ &gt;= 17

> **ノート：**
>
> 上記の旧バージョンのブラウザや他のブラウザでTiDB Dashboardにアクセスすると、一部の関数が正常に動作しない場合があります。

## ログイン {#sign-in}

TiDB ダッシュボードにアクセスすると、下の画像に示すように、ユーザー ログイン インターフェイスが表示されます。

-   TiDB `root`アカウントを使用して TiDB ダッシュボードにサインインできます。
-   [ユーザー定義の SQL ユーザー](/dashboard/dashboard-user.md)を作成した場合は、このアカウントと対応するパスワードを使用してサインインできます。

![Login interface](/media/dashboard/dashboard-access-login.png)

次のいずれかの状況が存在する場合、ログインが失敗する可能性があります。

-   TiDB `root`ユーザーが存在しません。
-   PD が開始されていないか、アクセスできません。
-   TiDB が開始されていないか、アクセスできません。
-   パスワードが`root`間違っています。

サインインすると、セッションは 24 時間以内に有効になります。サインアウトする方法については、セクション[ログアウト](#logout)を参照してください。

## 言語を切り替える {#switch-language}

次の言語が TiDB ダッシュボードでサポートされています。

-   英語
-   中国語（簡体字）

**[SQL ユーザー サインイン]**ページで、 <strong>[言語の</strong>切り替え] ドロップダウン リストをクリックして、インターフェイスの言語を切り替えることができます。

![Switch language](/media/dashboard/dashboard-access-switch-language.png)

## ログアウト {#logout}

ログインしたら、左側のナビゲーション バーにあるログイン ユーザー名をクリックして、ユーザー ページに切り替えます。ユーザー ページの**[ログアウト]**ボタンをクリックして、現在のユーザーをログアウトします。ログアウト後、ユーザー名とパスワードを再入力する必要があります。

![Logout](/media/dashboard/dashboard-access-logout.png)
