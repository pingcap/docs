---
title: Deploy TiDB Dashboard
summary: TiDB Dashboardは、v4.0以降のPDに組み込まれています。追加のデプロイメントは不要です。Kubernetes上に独立してデプロイすることも可能です。複数のPDインスタンスがデプロイされている場合、ダッシュボードとして機能するのは1つだけです。「tiup cluster display」コマンドを使用して、ダッシュボードの機能を確認してください。ダッシュボードの無効化と有効化は「tiup ctl」コマンドを使用して行うことができます。
---

# TiDB Dashboardをデプロイ {#deploy-tidb-dashboard}

TiDB Dashboard UIは、v4.0以降のバージョンのPDコンポーネントに組み込まれているため、追加のデプロイメントは必要ありません。標準のTiDBクラスターをデプロイするだけで、TiDB Dashboardが利用可能になります。

> **Note:**
>
> TiDB v6.5.0以降およびTiDB Operator v1.4.0以降では、TiDB DashboardをKubernetes上の独立したPodとしてデプロイできます。詳細については、 [TiDB DashboardをTiDB Operatorで独立してデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/v1.6/get-started#deploy-tidb-dashboard-independently)参照してください。

標準の TiDB クラスターをデプロイする方法については、次のドキュメントを参照してください。

-   [TiDB Self-Managedのクイックスタート](/quick-start-with-tidb.md)
-   [本番環境にTiDBをデプロイ](/production-deployment-using-tiup.md)
-   [Kubernetes環境のデプロイメント](https://docs.pingcap.com/tidb-in-kubernetes/stable/access-dashboard)

> **Note:**
>
> v4.0 より前の TiDB クラスターに TiDB Dashboardをデプロイすることはできません。

## 複数のPDインスタンスを使用したデプロイメント {#deployment-with-multiple-pd-instances}

クラスターに複数の PD インスタンスがデプロイされている場合、これらのインスタンスのうち 1 つだけが TiDB Dashboardとして機能します。

PDインスタンスが初めて実行される際、インスタンスは自動的に相互にネゴシエーションを行い、TiDB Dashboardを提供するインスタンスを1つ選択します。TiDB Dashboardは他のPDインスタンスでは実行されません。PDインスタンスが再起動されたり、新しいPDインスタンスが追加された場合でも、TiDB Dashboardサービスは選択されたPDインスタンスによって常に提供されます。ただし、TiDB Dashboardを提供するPDインスタンスがクラスターから削除（スケールイン）された場合は、再ネゴシエーションが行われます。このネゴシエーションプロセスではユーザーの介入は必要ありません。

TiDB Dashboardを提供していないPDインスタンスにアクセスすると、ブラウザが自動的にリダイレクトされ、TiDB Dashboardを提供するPDインスタンスへのアクセスが誘導されます。これにより、通常通りサービスにアクセスできるようになります。このプロセスは、以下の図に示されています。

![Process Schematic](/media/dashboard/dashboard-ops-multiple-pd.png)

> **Note:**
>
> TiDB Dashboardを提供する PD インスタンスは、PD リーダーではない可能性があります。

### 実際にTiDB Dashboardを提供しているPDインスタンスを確認する {#check-the-pd-instance-that-actually-serves-tidb-dashboard}

TiUPを使用してデプロイされた実行中のクラスターの場合、 `tiup cluster display`コマンドを使用して、TiDB Dashboardを提供している PD インスタンスを確認できます。`CLUSTER_NAME`をクラスター名に置き換えてください。

```bash
tiup cluster display CLUSTER_NAME --dashboard
```

サンプル出力は次のとおりです。

```bash
http://192.168.0.123:2379/dashboard/
```

> **Note:**
>
> この機能は、 `tiup cluster`デプロイメント ツールの新しいバージョン (v1.0.3 以降) でのみ使用できます。
>
> <details><summary>TiUPクラスタのアップグレード</summary>
>
> ```bash
> tiup update --self
> tiup update cluster --force
> ```
>
> </details>

### TiDB Dashboardを提供するために別のPDインスタンスに切り替える {#switch-to-another-pd-instance-to-serve-tidb-dashboard}

TiUPを使用してデプロイされた実行中のクラスターの場合、 `tiup ctl:v<CLUSTER_VERSION> pd`コマンドを使用して、TiDB Dashboardを提供する PD インスタンスを変更したり、無効になっている場合に TiDB Dashboardを提供する PD インスタンスを再指定したりできます。

```bash
tiup ctl:v<CLUSTER_VERSION> pd -u http://127.0.0.1:2379 config set dashboard-address http://9.9.9.9:2379
```

上記のコマンドでは、

-   `127.0.0.1:2379`任意の PD インスタンスの IP とポートに置き換えます。
-   `9.9.9.9:2379` TiDB Dashboard サービスを実行する新しい PD インスタンスの IP とポートに置き換えます。

変更が有効になっているかどうかを確認するには、 `tiup cluster display`コマンドを使用します ( `CLUSTER_NAME`をクラスター名に置き換えます)。

```bash
tiup cluster display CLUSTER_NAME --dashboard
```

> **Warning:**
>
> TiDB Dashboard を実行するインスタンスを変更すると、Key Visualize 履歴や検索履歴など、以前の TiDB Dashboard インスタンスに保存されたローカル データが失われます。

## TiDB Dashboardを無効にする {#disable-tidb-dashboard}

TiUPを使用してデプロイされた実行中のクラスターの場合は、 `tiup ctl:v<CLUSTER_VERSION> pd`コマンドを使用して、すべての PD インスタンスで TiDB Dashboardを無効にします ( `127.0.0.1:2379`任意の PD インスタンスの IP とポートに置き換えます)。

```bash
tiup ctl:v<CLUSTER_VERSION> pd -u http://127.0.0.1:2379 config set dashboard-address none
```

TiDB Dashboardを無効にすると、どの PD インスタンスが TiDB Dashboard サービスを提供しているかの確認が失敗します。

    Error: TiDB Dashboard is disabled

ブラウザ経由で任意の PD インスタンスの TiDB Dashboard アドレスにアクセスしても失敗します。

    Dashboard is not started.

## TiDB Dashboardを再度有効にする {#re-enable-tidb-dashboard}

TiUPを使用してデプロイされた実行中のクラスターの場合は、 `tiup ctl:v<CLUSTER_VERSION> pd`コマンドを使用して、PD にインスタンスの再ネゴシエートを要求し、TiDB Dashboardを実行します ( `127.0.0.1:2379`任意の PD インスタンスの IP とポートに置き換えます)。

```bash
tiup ctl:v<CLUSTER_VERSION> pd -u http://127.0.0.1:2379 config set dashboard-address auto
```

上記のコマンドを実行した後、 `tiup cluster display`コマンドを使用して、PD によって自動的にネゴシエートされた TiDB Dashboard インスタンス アドレスを表示できます ( `CLUSTER_NAME`をクラスター名に置き換えます)。

```bash
tiup cluster display CLUSTER_NAME --dashboard
```

TiDB Dashboardを提供するPDインスタンスを手動で指定することで、TiDB Dashboardを再度有効にすることもできます。[TiDB Dashboardを提供するために別のPDインスタンスに切り替える](#switch-to-another-pd-instance-to-serve-tidb-dashboard)を参照してください。

> **Warning:**
>
> 新しく有効になった TiDB Dashboard インスタンスが、TiDB Dashboardを提供していた以前のインスタンスと異なる場合、Key Visualize 履歴や検索履歴など、以前の TiDB Dashboard インスタンスに保存されたローカル データは失われます。

## 次は何か {#what-s-next}

-   TiDB Dashboard UI にアクセスしてログインする方法については、 [TiDB Dashboardにアクセスする](/dashboard/dashboard-access.md)参照してください。

-   ファイアウォールの設定など、TiDB Dashboardのセキュリティを強化する方法については、 [TiDB Dashboardのセキュリティ保護](/dashboard/dashboard-ops-security.md)を参照してください。
