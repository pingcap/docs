---
title: Configure TiDB Cloud Starter or Essential Firewall Rules for Public Endpoints
summary: TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスへのパブリックアクセスを安全に設定および管理するためのファイアウォールルールの構成方法を学びましょう。
---

# パブリックエンドポイント向けにTiDB Cloud StarterまたはEssential Firewallルールを設定する {#configure-tidb-cloud-starter-or-essential-firewall-rules-for-public-endpoints}

このドキュメントでは、 TiDB Cloud StarterおよびTiDB Cloud Essentialインスタンスのパブリック接続オプションについて説明します。インターネット経由でアクセス可能なTiDB Cloud StarterまたはEssentialインスタンスを安全に管理するための重要な概念を習得できます。

> **Note:**
>
> このドキュメントは**TiDB Cloud Starter**および**TiDB Cloud Essential**に適用されます。 **TiDB Cloud Dedicated**の IP アクセス リストを設定する手順については、 [TiDB Cloud Dedicatedの IP アクセス リストを設定する](/tidb-cloud/configure-ip-access-list.md)を参照してください。

## 公開エンドポイント {#public-endpoints}

TiDB Cloud StarterまたはEssentialインスタンスでパブリックアクセスを設定すると、パブリックエンドポイント経由でインスタンスにアクセスできるようになります。つまり、 TiDB Cloud StarterまたはEssentialインスタンスはインターネット経由でアクセス可能になります。パブリックエンドポイントは、公開されている DNS アドレスです。「承認済みネットワーク」とは、TiDB Cloud StarterまたはEssentialインスタンスへのアクセスを許可する IP アドレスの範囲を指します。これらのアクセス許可は、**ファイアウォールルール**によって適用されます。

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

このセクションでは、TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスのファイアウォールルールを管理する方法について説明します。パブリックエンドポイントを使用する場合、インスタンスへの接続はファイアウォールルールで指定された IP アドレスに制限されます。

TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスにファイアウォールルールを追加するには、次の手順を実行します。

1.  [**My TiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして、概要ページに移動します。

2.  左側のナビゲーションペインで、 **Settings** &gt; **Networking**をクリックします。

3.  **Networking**ページで、**Public Endpoint**が無効になっている場合は有効にしてください。

4.  （オプション）新しく作成したTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスでは、 TiDB Cloud はデフォルトで**Allow_all_public_connections**を有効にします。特定の IP アドレスまたは範囲へのアクセスを制限するには、 **Allow_all_public_connections**の行にある**...**をクリックし、次に**Delete**をクリックします。

5.  **Authorized Networks**セクションで、 **Add rule**をクリックし、許可するIPアドレスまたはIPアドレス範囲を追加します。

    -   お使いのコンピュータの現在のIPアドレスを追加するには、 **Add Current IP**をクリックします。これにより、 TiDB Cloudが認識するコンピュータのパブリックIPアドレスを含むファイアウォールルールが自動的に作成されます。

        > **Note:**
        >
        > TiDB Cloudコンソールが認識するIPアドレスは、データベースクライアントが使用するIPアドレスと異なる場合があります。ルールが期待どおりに機能しない場合は、開始IPアドレスと終了IPアドレスを調整してください。公開IPアドレスを確認するには、検索エンジンまたはオンラインツールを使用できます。たとえば、「自分のIPアドレスは何ですか」と検索してください。

    -   TiDB Cloud StarterまたはEssentialインスタンスがAWS上でホストされている場合、すべてのAWS IPアドレスからのアクセスを有効にするには、 **Add AWS Access**をクリックします。これにより、すべてのAWS IPアドレス範囲を含むファイアウォールルールが自動的に作成されます。TiDB Cloudは、予約済みIPアドレス**169.254.65.87**を使用してAWS IPアドレス範囲を表し、公式の[AWS IPアドレスリスト](https://docs.aws.amazon.com/vpc/latest/userguide/aws-ip-ranges.html)に基づいてリストを定期的に更新します。

    -   アドレス範囲を追加するには、単一のIPアドレスまたはIPアドレスの範囲を指定します。ルールを単一のIPアドレスに限定するには、 **Start IP Address**と**End IP Address**のフィールドに同じIPアドレスを入力します。

        > **Note:**
        >
        > ファイアウォールを開放すると、指定されたIPアドレスまたはIPアドレス範囲からの管理者、ユーザー、およびアプリケーションは、有効な認証情報を持つTiDB Cloud StarterまたはEssentialインスタンス上の任意のデータベースにアクセスできるようになります。

6.  **Save**をクリックしてください。

## 次は？ {#what-s-next}

-   [パブリックエンドポイント経由でTiDB Cloud StarterまたはEssentialに接続します](/tidb-cloud/connect-via-standard-connection-serverless.md)
