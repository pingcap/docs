---
title: Configure an IP Access List
summary: TiDB Cloud Dedicatedクラスターへのアクセスを許可するIPアドレスを設定する方法を学びましょう。
---

# IPアクセスリストを設定する

TiDB Cloudの各TiDB Cloud Dedicatedクラスターに対して、IPアクセスリストを設定することで、クラスターへのアクセスを試みるインターネットトラフィックをフィルタリングできます。これは、ファイアウォールのアクセスコントロールリストと同様に機能します。設定後は、IPアクセスリストに含まれるIPアドレスを持つクライアントおよびアプリケーションのみが、TiDB Cloud Dedicatedクラスターに接続できます。

> **Note:**
>
> このドキュメントは[**TiDB Cloud Dedicated**](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)に適用されます。**{{{ .starter }}}** または **{{{ .essential }}}** のIPアクセスリストを設定する手順については、[Configure {{{ .starter }}} or Essential Firewall Rules for Public Endpoints](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md)を参照してください。

## IP アドレスを追加する {#add-an-ip-address}

TiDB Cloud Dedicated クラスターの IP アクセスリストに IP アドレスを追加するには、次の手順を実行します。

1. [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動し、対象の TiDB Cloud Dedicated クラスター名をクリックして、その概要ページに移動します。

    > **Tip:**
    >
    > 複数の組織に所属している場合は、まず左上隅のコンボボックスを使用して対象の組織に切り替えてください。

2. 左側のナビゲーションペインで、**Settings** > **Networking** をクリックします。
3. **Networking** ページで、**Add IP Address** をクリックします。
4. **Add IP Address** ダイアログで、必要に応じて説明を付けて IP アドレスを追加します。TiDB Cloud Dedicated クラスターごとに、最大 100 個の IP アドレスを追加できます。

    - カスタム IP アドレスを追加するには、**+** アイコンをクリックし、CIDR 表記の IP アドレス（例: `192.168.1.1/32`）を入力して、説明を追加します。
    - 現在使用しているコンピューターの IP アドレスを追加するには、**Add Current IP** をクリックします。
    - 任意の IP アドレスからクラスターへのアクセスを許可するには、**Allow access from anywhere** をクリックします。これにより、`0.0.0.0/0` の CIDR エントリが追加されます。これは非常にリスクが高く、本番環境では**推奨されません**。

5. **Save** をクリックします。

## IP アドレスを編集する {#edit-an-ip-address}

IP アクセスリスト内の既存の IP アドレスを編集するには、次の手順を実行します。

1. **Networking** ページで、**IP Access List** 内から編集したい IP アドレスを見つけます。
2. 対象の IP アドレスの行で **...** をクリックし、**Edit** をクリックします。
3. **Edit IP Address** ダイアログで、必要に応じて IP アドレスまたは説明を変更します。
4. **Submit** をクリックします。

## IP アドレスを削除する {#delete-an-ip-address}

IP アクセスリストから既存の IP アドレスを削除するには、次の手順を実行します。

1. **Networking** ページで、**IP Access List** 内の削除したい IP アドレスを見つけます。
2. その IP アドレスの行にある **...** をクリックし、**Delete** をクリックします。
3. 確認ダイアログで、**Delete** をクリックします。
