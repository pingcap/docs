---
title: AWS PrivateLink を使用した TiDB Cloud Lake への接続
summary: 主要なクラウドが提供する PrivateLink スタイルのプライベートエンドポイント（AWS PrivateLink、Azure Private Link、Google Private Service Connect など）を使用すると、自身のネットワーク境界内のプライベート IP アドレスを通じて TiDB Cloud Lake にアクセスできるため、トラフィックがパブリックインターネットを経由する必要がありません。これにより、データセット、認証情報、管理操作はクラウドプロバイダーのバックボーン上にとどまり、既存のネットワークポリシーにも適合します。
---

# AWS PrivateLink を使用した TiDB Cloud Lake への接続

主要なクラウドが提供する PrivateLink スタイルのプライベートエンドポイント（AWS PrivateLink、Azure Private Link、Google Private Service Connect など）を使用すると、自身のネットワーク境界内のプライベート IP アドレスを通じて {{{ .lake }}} にアクセスできるため、トラフィックがパブリックインターネットを経由する必要がありません。これにより、データセット、認証情報、管理操作はクラウドプロバイダーのバックボーン上にとどまり、既存のネットワークポリシーにも適合します。

## 利点 {#benefits}

- ネットワーク分離: トラフィックが VPC/VPN 境界の外に出ることがなく、パブリックエンドポイントへの露出を排除できます。
- コンプライアンス対応: インターネットへの送信を禁止する社内監査や業界要件を満たしやすくなります。
- 安定したパフォーマンス: トラフィックは予測しにくいインターネット経路ではなく、クラウドプロバイダーのバックボーンを通ります。
- 制御の簡素化: 既存の security group、route table、monitoring を再利用してアクセスを管理できます。

## 仕組み {#how-it-works}

**Connect to {{{ .lake }}}** ダイアログから PrivateLink のサービス名を取得し、それを指すプライベートエンドポイントを作成します。クラウドプロバイダーは自動的にプライベート IP アドレスを割り当ててエンドポイントを受け入れ、private DNS を有効にすると、{{{ .lake }}} のドメインはそれらのアドレスに解決されるため、すべてのセッションが安全なプライベート経路上に維持されます。

## AWS PrivateLink の設定方法 {#how-to-setup-aws-privatelink}

1. VPC 設定を確認します。

    `Enable DNS resolution` と `Enable DNS hostnames` がチェックされていることを確認します。

2. **Connect to {{{ .lake }}}** ダイアログから接続先のサービス名を取得します。

    例: `com.amazonaws.vpce.us-east-2.vpce-svc-0123456789abcdef0`。

3. tcp 443 ポートを開放した security group を準備します。

   ![Security Group](/media/tidb-cloud-lake/security-group.png)

4. AWS Console に移動します。

   <https://us-east-2.console.aws.amazon.com/vpcconsole/home?region=us-east-2#Endpoints>:

   `Create endpoint` をクリックします。

   ![Create Endpoint Button](/media/tidb-cloud-lake/create-endpoint-1.png)

   ![Create Endpoint Sheet](/media/tidb-cloud-lake/create-endpoint-2.png)

   先ほど作成した security group `HTTPS` を選択します。

   ![Create Endpoint SG](/media/tidb-cloud-lake/create-endpoint-3.png)

5. PrivateLink の作成が完了するまで待ちます。

6. private DNS name の設定を変更します。

    ![DNS Menu](/media/tidb-cloud-lake/dns-1.png)

    private DNS names を有効にします。

    ![DNS Sheet](/media/tidb-cloud-lake/dns-2.png)

    変更が適用されるまで待ちます。

7. PrivateLink 経由で {{{ .lake }}} にアクセスできることを確認します。

    Gateway ドメインが VPC 内部 IP アドレスに解決されます。

    > **Note:**
    >
    > おめでとうございます。AWS PrivateLink を使用した {{{ .lake }}} への接続に成功しました。