---
title: Deploy TiDB Dashboard
summary: TiDBダッシュボードは、v4.0以降のPDに組み込まれています。追加のデプロイメントは不要です。Kubernetes上に独立してデプロイすることも可能です。複数のPDインスタンスがデプロイされている場合、ダッシュボードとして機能するのは1つだけです。「tiup cluster display」コマンドを使用して、ダッシュボードの機能を確認してください。ダッシュボードの無効化と有効化は「tiup ctl」コマンドを使用して行うことができます。
---

# TiDBダッシュボードをデプロイ {#deploy-tidb-dashboard}

TiDBダッシュボードUIは、v4.0以降のバージョンのPDコンポーネントに組み込まれているため、追加のデプロイメントは必要ありません。標準のTiDBクラスターをデプロイするだけで、TiDBダッシュボードが利用可能になります。

> **注記：**
>
> TiDB v6.5.0以降およびTiDB Operator v1.4.0以降では、TiDB DashboardをKubernetes上の独立したPodとしてデプロイできます。詳細については、 [TiDB ダッシュボードをTiDB Operatorで独立してデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/v1.6/get-started#deploy-tidb-dashboard-independently)参照してください。

標準の TiDB クラスターをデプロイする方法については、次のドキュメントを参照してください。

-   [TiDBセルフマネージドのクイックスタート](/quick-start-with-tidb.md)
-   [本番環境にTiDBをデプロイ](/production-deployment-using-tiup.md)
-   [Kubernetes環境のデプロイメント](https://docs.pingcap.com/tidb-in-kubernetes/stable/access-dashboard)

> **注記：**
>
> v4.0 より前の TiDB クラスターに TiDB ダッシュボードをデプロイすることはできません。

## 複数のPDインスタンスを使用したデプロイメント {#deployment-with-multiple-pd-instances}

クラスターに複数の PD インスタンスがデプロイされている場合、これらのインスタンスのうち 1 つだけが TiDB ダッシュボードとして機能します。

PDインスタンスが初めて実行される際、インスタンスは自動的に相互にネゴシエーションを行い、TiDBダッシュボードを提供するインスタンスを1つ選択します。TiDBダッシュボードは他のPDインスタンスでは実行されません。PDインスタンスが再起動されたり、新しいPDインスタンスが追加された場合でも、TiDBダッシュボードサービスは選択されたPDインスタンスによって常に提供されます。ただし、TiDBダッシュボードを提供するPDインスタンスがクラスターから削除（スケールイン）された場合は、再ネゴシエーションが行われます。このネゴシエーションプロセスではユーザーの介入は必要ありません。

TiDBダッシュボードを提供していないPDインスタンスにアクセスすると、ブラウザが自動的にリダイレクトされ、TiDBダッシュボードを提供するPDインスタンスへのアクセスが誘導されます。これにより、通常通りサービスにアクセスできるようになります。このプロセスは、以下の図に示されています。

![Process Schematic](/media/dashboard/dashboard-ops-multiple-pd.png)

> **注記：**
>
> TiDB ダッシュボードを提供する PD インスタンスは、PD リーダーではない可能性があります。

### 実際にTiDBダッシュボードを提供しているPDインスタンスを確認する {#check-the-pd-instance-that-actually-serves-tidb-dashboard}

TiUPを使用してデプロイされた実行中のクラスターの場合、 `tiup cluster display`コマンドを使用して、TiDB ダッシュボードを提供している PD インスタンスを確認できます。3 `CLUSTER_NAME`クラスター名に置き換えてください。

```bash
tiup cluster display CLUSTER_NAME --dashboard
```

サンプル出力は次のとおりです。

```bash
http://192.168.0.123:2379/dashboard/
```

> **注記：**
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

### TiDBダッシュボードを提供するために別のPDインスタンスに切り替える {#switch-to-another-pd-instance-to-serve-tidb-dashboard}

TiUPを使用してデプロイされた実行中のクラスターの場合、 `tiup ctl:v<CLUSTER_VERSION> pd`コマンドを使用して、TiDB ダッシュボードを提供する PD インスタンスを変更したり、無効になっている場合に TiDB ダッシュボードを提供する PD インスタンスを再指定したりできます。

```bash
tiup ctl:v<CLUSTER_VERSION> pd -u http://127.0.0.1:2379 config set dashboard-address http://9.9.9.9:2379
```

上記のコマンドでは、

-   `127.0.0.1:2379`任意の PD インスタンスの IP とポートに置き換えます。
-   `9.9.9.9:2379` TiDB ダッシュボード サービスを実行する新しい PD インスタンスの IP とポートに置き換えます。

変更が有効になっているかどうかを確認するには、 `tiup cluster display`コマンドを使用します ( `CLUSTER_NAME`クラスター名に置き換えます)。

```bash
tiup cluster display CLUSTER_NAME --dashboard
```

> **警告：**
>
> TiDB Dashboard を実行するインスタンスを変更すると、Key Visualize 履歴や検索履歴など、以前の TiDB Dashboard インスタンスに保存されたローカル データが失われます。

## TiDBダッシュボードを無効にする {#disable-tidb-dashboard}

TiUPを使用してデプロイされた実行中のクラスターの場合は、 `tiup ctl:v<CLUSTER_VERSION> pd`コマンドを使用して、すべての PD インスタンスで TiDB ダッシュボードを無効にします ( `127.0.0.1:2379`任意の PD インスタンスの IP とポートに置き換えます)。

```bash
tiup ctl:v<CLUSTER_VERSION> pd -u http://127.0.0.1:2379 config set dashboard-address none
```

TiDB ダッシュボードを無効にすると、どの PD インスタンスが TiDB ダッシュボード サービスを提供しているかの確認が失敗します。

    Error: TiDB Dashboard is disabled

ブラウザ経由で任意の PD インスタンスの TiDB ダッシュボード アドレスにアクセスしても失敗します。

    Dashboard is not started.

## TiDBダッシュボードを再度有効にする {#re-enable-tidb-dashboard}

TiUPを使用してデプロイされた実行中のクラスターの場合は、 `tiup ctl:v<CLUSTER_VERSION> pd`コマンドを使用して、PD にインスタンスの再ネゴシエートを要求し、TiDB ダッシュボードを実行します ( `127.0.0.1:2379`任意の PD インスタンスの IP とポートに置き換えます)。

```bash
tiup ctl:v<CLUSTER_VERSION> pd -u http://127.0.0.1:2379 config set dashboard-address auto
```

上記のコマンドを実行した後、 `tiup cluster display`コマンドを使用して、PD によって自動的にネゴシエートされた TiDB ダッシュボード インスタンス アドレスを表示できます ( `CLUSTER_NAME`クラスター名に置き換えます)。

```bash
tiup cluster display CLUSTER_NAME --dashboard
```

TiDBダッシュボードを提供するPDインスタンスを手動で指定することで、TiDBダッシュボードを再度有効にすることもできます。1 [TiDBダッシュボードを提供するために別のPDインスタンスに切り替える](#switch-to-another-pd-instance-to-serve-tidb-dashboard)参照してください。

> **警告：**
>
> 新しく有効になった TiDB ダッシュボード インスタンスが、TiDB ダッシュボードを提供していた以前のインスタンスと異なる場合、Key Visualize 履歴や検索履歴など、以前の TiDB ダッシュボード インスタンスに保存されたローカル データは失われます。

## 次は何か {#what-s-next}

-   TiDB ダッシュボード UI にアクセスしてログインする方法については、 [TiDBダッシュボードにアクセスする](/dashboard/dashboard-access.md)参照してください。

-   ファイアウォールの設定など、TiDB ダッシュボードのセキュリティを強化する方法については、 [セキュリティTiDBダッシュボード](/dashboard/dashboard-ops-security.md)参照してください。
