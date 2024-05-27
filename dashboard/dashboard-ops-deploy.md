---
title: Deploy TiDB Dashboard
summary: TiDB ダッシュボードは、v4.0 以降の PD に組み込まれています。追加のデプロイメントは必要ありません。Kubernetes に独立してデプロイすることもできます。複数の PD インスタンスがデプロイされている場合、ダッシュボードとして機能するのは 1 つだけです。サービス提供インスタンスを確認するには、`tiup cluster displayを使用します。`tiup ctl` を使用してダッシュボードを無効にしたり、再度有効にしたりできます。
---

# TiDBダッシュボードをデプロイ {#deploy-tidb-dashboard}

TiDB ダッシュボード UI は、v4.0 以降のバージョンの PDコンポーネントに組み込まれているため、追加のデプロイメントは必要ありません。標準の TiDB クラスターをデプロイするだけで、TiDB ダッシュボードが利用可能になります。

> **注記：**
>
> TiDB v6.5.0（以降）およびTiDB Operator v1.4.0（以降）では、Kubernetes上の独立したポッドとしてTiDB Dashboardをデプロイすることがサポートされています。詳細については、 [TiDB ダッシュボードをTiDB Operatorに独立してデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/dev/get-started#deploy-tidb-dashboard-independently)参照してください。

標準の TiDB クラスターをデプロイする方法については、次のドキュメントを参照してください。

-   [TiDB データベース プラットフォームのクイック スタート ガイド](/quick-start-with-tidb.md)
-   [本番環境にTiDBをデプロイ](/production-deployment-using-tiup.md)
-   [Kubernetes環境の展開](https://docs.pingcap.com/tidb-in-kubernetes/stable/access-dashboard)

> **注記：**
>
> v4.0 より前の TiDB クラスターに TiDB ダッシュボードをデプロイすることはできません。

## 複数のPDインスタンスを使用したデプロイメント {#deployment-with-multiple-pd-instances}

クラスターに複数の PD インスタンスがデプロイされている場合、これらのインスタンスのうち 1 つだけが TiDB ダッシュボードとして機能します。

PD インスタンスが初めて実行されると、インスタンス間で自動的にネゴシエートされ、TiDB ダッシュボードを提供するインスタンスが 1 つ選択されます。TiDB ダッシュボードは他の PD インスタンスでは実行されません。PD インスタンスが再起動されたり、新しい PD インスタンスが参加したりしても、TiDB ダッシュボード サービスは、選択された PD インスタンスによって常に提供されます。ただし、TiDB ダッシュボードを提供する PD インスタンスがクラスターから削除されると (スケールインされると)、再ネゴシエーションが行われます。ネゴシエーション プロセスでは、ユーザーの介入は必要ありません。

TiDB ダッシュボードを提供していない PD インスタンスにアクセスすると、ブラウザが自動的にリダイレクトされ、TiDB ダッシュボードを提供している PD インスタンスへのアクセスが誘導され、正常にサービスにアクセスできるようになります。このプロセスは、以下の画像に示されています。

![Process Schematic](/media/dashboard/dashboard-ops-multiple-pd.png)

> **注記：**
>
> TiDB ダッシュボードを提供する PD インスタンスは、PD リーダーではない可能性があります。

### 実際にTiDBダッシュボードを提供しているPDインスタンスを確認する {#check-the-pd-instance-that-actually-serves-tidb-dashboard}

TiUPを使用してデプロイされた実行中のクラスターの場合、 `tiup cluster display`コマンドを使用して、どの PD インスタンスが TiDB ダッシュボードを提供しているかを確認できます。3 `CLUSTER_NAME`クラスター名に置き換えます。

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

上記のコマンドでは:

-   `127.0.0.1:2379`任意の PD インスタンスの IP とポートに置き換えます。
-   `9.9.9.9:2379` 、TiDB ダッシュボード サービスを実行する新しい PD インスタンスの IP とポートに置き換えます。

変更が有効になっているかどうかを確認するには、 `tiup cluster display`コマンドを使用します ( `CLUSTER_NAME`クラスター名に置き換えます)。

```bash
tiup cluster display CLUSTER_NAME --dashboard
```

> **警告：**
>
> TiDB ダッシュボードを実行するインスタンスを変更すると、Key Visualize 履歴や検索履歴など、以前の TiDB ダッシュボード インスタンスに保存されたローカル データが失われます。

## TiDBダッシュボードを無効にする {#disable-tidb-dashboard}

TiUPを使用してデプロイされた実行中のクラスターの場合は、 `tiup ctl:v<CLUSTER_VERSION> pd`コマンドを使用してすべての PD インスタンスで TiDB ダッシュボードを無効にします ( `127.0.0.1:2379`任意の PD インスタンスの IP とポートに置き換えます)。

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

TiDB ダッシュボードを提供する PD インスタンスを手動で指定することで、TiDB ダッシュボードを再度有効にすることもできます。 [TiDBダッシュボードを提供するために別のPDインスタンスに切り替える](#switch-to-another-pd-instance-to-serve-tidb-dashboard)参照してください。

> **警告：**
>
> 新しく有効になった TiDB ダッシュボード インスタンスが、TiDB ダッシュボードを提供していた以前のインスタンスと異なる場合、Key Visualize 履歴や検索履歴など、以前の TiDB ダッシュボード インスタンスに保存されたローカル データは失われます。

## 次は何ですか {#what-s-next}

-   TiDB ダッシュボード UI にアクセスしてログインする方法については、 [TiDBダッシュボードにアクセスする](/dashboard/dashboard-access.md)参照してください。

-   ファイアウォールの設定など、TiDB ダッシュボードのセキュリティを強化する方法については、 [セキュリティTiDB ダッシュボード](/dashboard/dashboard-ops-security.md)を参照してください。
