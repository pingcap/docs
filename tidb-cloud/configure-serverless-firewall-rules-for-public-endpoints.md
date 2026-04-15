---
title: Configure TiDB Cloud Starter or Essential Firewall Rules for Public Endpoints
summary: TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスへのパブリックアクセスを安全に設定および管理するためのファイアウォールルールの構成方法を学びましょう。
---

# パブリックエンドポイント向けにTiDB Cloud StarterまたはEssential Firewallルールを設定する {#configure-tidb-cloud-starter-or-essential-firewall-rules-for-public-endpoints}

このドキュメントでは、 TiDB Cloud StarterおよびTiDB Cloud Essentialインスタンスのパブリック接続オプションについて説明します。インターネット経由でアクセス可能なTiDB Cloud StarterまたはEssentialインスタンスを安全に管理するための重要な概念を習得できます。

> **注記：**
>
> このドキュメントは**TiDB Cloud Starter**および**TiDB Cloud Essential**に適用されます。 **TiDB Cloud Dedicated**の IP アクセス リストを設定する手順については、 [TiDB Cloud Dedicatedの IP アクセス リストを設定する](/tidb-cloud/configure-ip-access-list.md)参照してください。

## 公開エンドポイント {#public-endpoints}

TiDB Cloud StarterまたはEssentialインスタンスでパブリック アクセスを設定すると、パブリック エンドポイント経由でインスタンスにアクセスできるようになります。つまり、 TiDB Cloud StarterまたはEssentialインスタンスはインターネット経由でアクセス可能になります。パブリック エンドポイントは、公開されている DNS アドレスです。「承認済みネットワーク」とは、TiDB Cloud StarterまたはEssentialインスタンスへのアクセスを許可する IP アドレスの範囲を指します。これらのアクセス許可は、**ファイアウォール ルール**によって適用されます。

### 公共アクセスの特徴 {#characteristics-of-public-access}

-   指定されたIPアドレスのみが、TiDB Cloud StarterまたはEssentialインスタンスにアクセスできます。
    -   デフォルトでは、すべてのIPアドレス（ `0.0.0.0 - 255.255.255.255` ）が許可されます。
    -   TiDB Cloud StarterまたはEssentialインスタンスの作成後、許可するIPアドレスを更新できます。
-   TiDB Cloud StarterまたはEssentialインスタンスには、公開解決可能なDNS名が割り当てられています。
-   TiDB Cloud StarterまたはEssentialインスタンスとの間のネットワークトラフィックは、プライベートネットワークではなく、**パブリックインターネット**を経由してルーティングされます。

### ファイアウォールルール {#firewall-rules}

IPアドレスへのアクセス権限は**ファイアウォールルール**によって付与されます。承認されていないIPアドレスからの接続試行があった場合、クライアントはエラーを受け取ります。

IPファイアウォールルールは最大200個まで作成できます。

### AWSへのアクセスを許可する {#allow-aws-access}

TiDB Cloud Starterインスタンスが AWS でホストされている場合は、公式[AWS IPアドレスリスト](https://docs.aws.amazon.com/vpc/latest/userguide/aws-ip-ranges.html)を参照して、**すべての AWS IP アドレス**からのアクセスを有効にすることができます。

TiDB Cloud はこのリストを定期的に更新し、予約済みの IP アドレス**169.254.65.87**を使用してすべての AWS IP アドレスを表します。

## ファイアウォールルールの作成と管理 {#create-and-manage-a-firewall-rule}

このセクションでは、TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスのファイアウォール ルールを管理する方法について説明します。パブリック エンドポイントを使用する場合、インスタンスへの接続はファイアウォール ルールで指定された IP アドレスに制限されます。

TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスにファイアウォールルールを追加するには、次の手順を実行します。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして、概要ページに移動します。

2.  左側のナビゲーションペインで、 **[設定]** &gt; **[ネットワーク]**をクリックします。

3.  **ネットワーク**ページで、**パブリックエンドポイント**が無効になっている場合は有効にします。**承認済みネットワーク**で、 **[+ 現在のIPアドレスを追加]**をクリックします。これにより、 TiDB Cloudが認識するコンピュータのパブリックIPアドレスを含むファイアウォールルールが自動的に作成されます。

    > **注記：**
    >
    > TiDB Cloudコンソールで確認されるIPアドレスが、インターネットアクセス時に使用するIPアドレスと異なる場合があります。そのため、ルールが正しく機能するように、開始IPアドレスと終了IPアドレスを変更する必要があるかもしれません。検索エンジンやその他のオンラインツールを使用して、自分のIPアドレスを確認できます。例えば、「自分のIPアドレスは何ですか」と検索してみてください。

4.  アドレス範囲を追加するには、 **「ルールの追加」**をクリックします。表示されたウィンドウで、単一のIPアドレスまたはIPアドレスの範囲を指定できます。ルールを単一のIPアドレスに限定する場合は、 **「開始IPアドレス」**と**「終了IPアドレス」**フィールドに同じIPアドレスを入力します。ファイアウォールを開くと、管理者、ユーザー、およびアプリケーションは、有効な認証情報を持つTiDB Cloud StarterまたはEssentialインスタンス上の任意のデータベースにアクセスできるようになります。「**送信」**をクリックしてファイアウォールルールを追加します。

## 次は？ {#what-s-next}

-   [パブリックエンドポイント経由でTiDB Cloud StarterまたはEssentialに接続します](/tidb-cloud/connect-via-standard-connection-serverless.md)
