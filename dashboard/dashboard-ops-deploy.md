---
title: Deploy TiDB Dashboard
summary: Learn how to deploy TiDB Dashboard.
---

# TiDB ダッシュボードのデプロイ {#deploy-tidb-dashboard}

TiDB ダッシュボード UI は、v4.0 以降のバージョンの PDコンポーネントに組み込まれており、追加の展開は必要ありません。標準の TiDB クラスターをデプロイするだけで、TiDB ダッシュボードがそこに表示されます。

> **注記：**
>
> TiDB v6.5.0 (以降) およびTiDB Operator v1.4.0 (以降) は、TiDB ダッシュボードを Kubernetes 上の独立したポッドとしてデプロイすることをサポートしています。詳細は[TiDB Operatorで TiDB ダッシュボードを独立してデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/dev/get-started#deploy-tidb-dashboard-independently)を参照してください。

標準の TiDB クラスターをデプロイする方法については、次のドキュメントを参照してください。

-   [TiDB データベース プラットフォームのクイック スタート ガイド](/quick-start-with-tidb.md)
-   [TiDB を実稼働環境にデプロイ](/production-deployment-using-tiup.md)
-   [Kubernetes環境の導入](https://docs.pingcap.com/tidb-in-kubernetes/stable/access-dashboard)

> **注記：**
>
> TiDB ダッシュボードを v4.0 より前の TiDB クラスターにデプロイすることはできません。

## 複数の PD インスタンスを使用したデプロイメント {#deployment-with-multiple-pd-instances}

複数の PD インスタンスがクラスターにデプロイされている場合、これらのインスタンスのうちの 1 つだけが TiDB ダッシュボードにサービスを提供します。

PD インスタンスが初めて実行されるとき、それらは自動的に相互にネゴシエートして、TiDB ダッシュボードにサービスを提供するインスタンスを 1 つ選択します。 TiDB ダッシュボードは他の PD インスタンスでは実行されません。 TiDB ダッシュボード サービスは、PD インスタンスが再起動されたり、新しい PD インスタンスが参加したりしても、選択した PD インスタンスによって常に提供されます。ただし、TiDB ダッシュボードを提供する PD インスタンスがクラスターから削除される (スケールインされる) 場合は、再ネゴシエーションが必要になります。ネゴシエーション プロセスにはユーザーの介入は必要ありません。

TiDB ダッシュボードを提供しない PD インスタンスにアクセスすると、ブラウザは自動的にリダイレクトされ、TiDB ダッシュボードを提供する PD インスタンスにアクセスするように案内され、サービスに通常どおりアクセスできるようになります。このプロセスを以下の図に示します。

![Process Schematic](/media/dashboard/dashboard-ops-multiple-pd.png)

> **注記：**
>
> TiDB ダッシュボードを提供する PD インスタンスは PD リーダーではない可能性があります。

### 実際に TiDB ダッシュボードを提供する PD インスタンスを確認する {#check-the-pd-instance-that-actually-serves-tidb-dashboard}

TiUP を使用してデプロイされた実行中のクラスターの場合、 `tiup cluster display`コマンドを使用して、どの PD インスタンスが TiDB ダッシュボードにサービスを提供しているかを確認できます。 `CLUSTER_NAME`クラスター名に置き換えます。

```bash
tiup cluster display CLUSTER_NAME --dashboard
```

出力例は次のとおりです。

```bash
http://192.168.0.123:2379/dashboard/
```

> **注記：**
>
> この機能は、 `tiup cluster`導入ツールの新しいバージョン (v1.0.3 以降) でのみ使用できます。
>
> <details><summary>TiUPクラスタのアップグレード</summary>
>
> ```bash
> tiup update --self
> tiup update cluster --force
> ```
>
> </details>

### 別の PD インスタンスに切り替えて TiDB ダッシュボードを提供する {#switch-to-another-pd-instance-to-serve-tidb-dashboard}

TiUPを使用してデプロイされた実行中のクラスターの場合、 `tiup ctl:v<CLUSTER_VERSION> pd`コマンドを使用して TiDB ダッシュボードを提供する PD インスタンスを変更するか、TiDB ダッシュボードが無効になっているときに TiDB ダッシュボードを提供する PD インスタンスを再指定できます。

```bash
tiup ctl:v<CLUSTER_VERSION> pd -u http://127.0.0.1:2379 config set dashboard-address http://9.9.9.9:2379
```

上記のコマンドでは次のようになります。

-   `127.0.0.1:2379`を任意の PD インスタンスの IP とポートに置き換えます。
-   `9.9.9.9:2379`を、TiDB ダッシュボード サービスを実行する新しい PD インスタンスの IP とポートに置き換えます。

`tiup cluster display`コマンドを使用すると、変更が有効になっているかどうかを確認できます ( `CLUSTER_NAME`クラスター名に置き換えます)。

```bash
tiup cluster display CLUSTER_NAME --dashboard
```

> **警告：**
>
> TiDB ダッシュボードを実行するインスタンスを変更すると、Key Visualize 履歴や検索履歴など、以前の TiDB ダッシュボード インスタンスに保存されていたローカル データが失われます。

## TiDB ダッシュボードを無効にする {#disable-tidb-dashboard}

TiUPを使用してデプロイされた実行中のクラスターの場合は、 `tiup ctl:v<CLUSTER_VERSION> pd`コマンドを使用して、すべての PD インスタンスで TiDB ダッシュボードを無効にします ( `127.0.0.1:2379`任意の PD インスタンスの IP とポートに置き換えます)。

```bash
tiup ctl:v<CLUSTER_VERSION> pd -u http://127.0.0.1:2379 config set dashboard-address none
```

TiDB ダッシュボードを無効にした後、どの PD インスタンスが TiDB ダッシュボード サービスを提供するかを確認すると失敗します。

    Error: TiDB Dashboard is disabled

ブラウザ経由で PD インスタンスの TiDB ダッシュボード アドレスにアクセスしても失敗します。

    Dashboard is not started.

## TiDB ダッシュボードを再度有効にする {#re-enable-tidb-dashboard}

TiUPを使用してデプロイされた実行中のクラスターの場合は、 `tiup ctl:v<CLUSTER_VERSION> pd`コマンドを使用して、TiDB ダッシュボードを実行するインスタンスを再ネゴシエートするように PD に要求します ( `127.0.0.1:2379`任意の PD インスタンスの IP とポートに置き換えます)。

```bash
tiup ctl:v<CLUSTER_VERSION> pd -u http://127.0.0.1:2379 config set dashboard-address auto
```

上記のコマンドを実行した後、 `tiup cluster display`コマンドを使用して、PD によって自動的にネゴシエートされた TiDB ダッシュボード インスタンスのアドレスを表示できます ( `CLUSTER_NAME`クラスター名に置き換えます)。

```bash
tiup cluster display CLUSTER_NAME --dashboard
```

TiDB ダッシュボードを提供する PD インスタンスを手動で指定することで、TiDB ダッシュボードを再度有効にすることもできます。 [別の PD インスタンスに切り替えて TiDB ダッシュボードを提供する](#switch-to-another-pd-instance-to-serve-tidb-dashboard)を参照してください。

> **警告：**
>
> 新しく有効になった TiDB ダッシュボード インスタンスが、TiDB ダッシュボードを提供していた以前のインスタンスと異なる場合、Key Visualize 履歴や検索履歴など、以前の TiDB ダッシュボード インスタンスに保存されていたローカル データが失われます。

## 次は何ですか {#what-s-next}

-   TiDB ダッシュボード UI にアクセスしてログインする方法については、 [TiDB ダッシュボードにアクセスする](/dashboard/dashboard-access.md)を参照してください。

-   ファイアウォールの構成など、TiDB ダッシュボードのセキュリティを強化する方法については、 [セキュリティTiDB ダッシュボード](/dashboard/dashboard-ops-security.md)を参照してください。
