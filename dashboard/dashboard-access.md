---
title: Access TiDB Dashboard
summary: TiDB Dashboardにアクセスするには、ブラウザで指定されたURLにアクセスしてください。複数のPDインスタンスの場合は、アドレスを任意のPDインスタンスのアドレスとポートに置き換えてください。Chrome、Firefox、またはEdgeブラウザ（最新バージョン）をご利用ください。TiDBルートアカウントまたはユーザー定義のSQLユーザーでサインインしてください。セッションは24時間有効です。言語は英語と中国語で切り替えられます。ログアウトするには、ユーザー名をクリックし、「ログアウト」ボタンをクリックしてください。
---

# TiDB Dashboardにアクセスする {#access-tidb-dashboard}

TiDB Dashboardにアクセスするには、ブラウザから[http://127.0.0.1:2379/dashboard](http://127.0.0.1:2379/dashboard)にアクセスしてください。`127.0.0.1:2379`を実際のPDインスタンスのアドレスとポートに置き換えてください。

> **Note:**
>
> TiDB v6.5.0以降およびTiDB Operator v1.4.0以降では、Kubernetes上にTiDB Dashboardを独立したPodとしてデプロイできます。TiDB Operatorを使用すると、このPodのIPアドレスにアクセスしてTiDB Dashboardを起動できます。詳細は[TiDB DashboardをTiDB Operatorで独立してデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/v1.6/get-started#deploy-tidb-dashboard-independently)を参照してください。

## 複数のPDインスタンスがデプロイされている場合にTiDB Dashboardにアクセスする {#access-tidb-dashboard-when-multiple-pd-instances-are-deployed}

クラスターに複数の PD インスタンスがデプロイされていて、**すべての**PD インスタンスとポートに直接アクセスできる場合は、アドレス[http://127.0.0.1:2379/dashboard/](http://127.0.0.1:2379/dashboard/)の`127.0.0.1:2379`**任意の**PD インスタンスのアドレスとポートに置き換えるだけです。

> **Note:**
>
> ファイアウォールまたはリバースプロキシが設定されており、すべてのPDインスタンスに直接アクセスできない場合、TiDB Dashboardにアクセスできない可能性があります。これは通常、ファイアウォールまたはリバースプロキシが正しく設定されていないことが原因です。複数のPDインスタンスがデプロイされている場合にファイアウォールまたはリバースプロキシを正しく設定する方法については、 [リバースプロキシの背後でTiDB Dashboardを使用する](/dashboard/dashboard-ops-reverse-proxy.md)と[TiDB Dashboardのセキュリティ保護](/dashboard/dashboard-ops-security.md)を参照してください。

## ブラウザの互換性 {#browser-compatibility}

TiDB Dashboardは、比較的新しいバージョンの次の一般的なデスクトップ ブラウザーで使用できます。

-   Chrome &gt;= 77
-   Firefox &gt;= 68
-   Edge &gt;= 17

> **Note:**
>
> 上記のブラウザまたは以前のバージョンのブラウザ、あるいはその他のブラウザを使用して TiDB Dashboardにアクセスすると、一部の機能が正しく動作しない可能性があります。

## サインイン {#sign-in}

TiDB Dashboardにアクセスすると、ユーザー ログイン インターフェイスに移動します。

-   TiDB `root`アカウントを使用して TiDB Dashboardにサインインできます。
-   TiDB Dashboardには、シングルサインオン（SSO）経由でサインインすることもできます。詳細については、 [TiDB DashboardのSSOを構成する](/dashboard/dashboard-session-sso.md)ご覧ください。
-   [ユーザー定義のSQLユーザー](/dashboard/dashboard-user.md)を作成した場合は、このアカウントと対応するパスワードを使用してサインインできます。

次のいずれかの状況が存在する場合、ログインが失敗する可能性があります。

-   TiDB `root`ユーザーが存在しません。
-   PD が起動していないか、アクセスできません。
-   TiDB が起動されていないか、アクセスできません。
-   パスワードが`root`間違っています。

サインイン後、セッションは24時間有効です。サインアウトの方法については、 [ログアウト](#logout)セクションをご覧ください。

## 言語を切り替える {#switch-language}

TiDB Dashboardでは次の言語がサポートされています。

-   英語
-   中国語（簡体字）

**SQL ユーザー サインイン**ページで、**言語の切り替え**ドロップダウン リストをクリックしてインターフェイス言語を切り替えることができます。

![Switch language](/media/dashboard/dashboard-access-switch-language.png)

## ログアウト {#logout}

ログイン後、左側のナビゲーションバーにあるログインユーザー名をクリックしてユーザーページに切り替えます。ユーザーページの**「ログアウト」**ボタンをクリックすると、現在のユーザーがログアウトします。ログアウト後、ユーザー名とパスワードを再度入力する必要があります。

![Logout](/media/dashboard/dashboard-access-logout.png)
