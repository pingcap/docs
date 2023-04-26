---
title: Deploy TiDB Dashboard
summary: Learn how to deploy TiDB Dashboard.
---

# TiDB ダッシュボードをデプロイ {#deploy-tidb-dashboard}

TiDB ダッシュボード UI は、v4.0 以降のバージョンの PDコンポーネントに組み込まれており、追加のデプロイは必要ありません。標準の TiDB クラスターをデプロイするだけで、TiDB ダッシュボードが表示されます。

> **ノート：**
>
> TiDB v6.5.0 (およびそれ以降) およびTiDB Operator v1.4.0 (およびそれ以降) は、TiDB ダッシュボードを Kubernetes 上の独立した Pod としてデプロイすることをサポートします。詳細については、 [TiDB Operatorで TiDB ダッシュボードを個別にデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/dev/get-started#deploy-tidb-dashboard-independently)を参照してください。

標準の TiDB クラスターをデプロイする方法については、次のドキュメントを参照してください。

-   [TiDB データベース プラットフォームのクイック スタート ガイド](/quick-start-with-tidb.md)
-   [TiDB を本番環境にデプロイ](/production-deployment-using-tiup.md)
-   [Kubernetes 環境のデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/stable/access-dashboard)

> **ノート：**
>
> v4.0 より前の TiDB クラスターに TiDB ダッシュボードをデプロイすることはできません。

## 複数の PD インスタンスを使用した展開 {#deployment-with-multiple-pd-instances}

複数の PD インスタンスがクラスターにデプロイされている場合、これらのインスタンスの 1 つだけが TiDB ダッシュボードを提供します。

PD インスタンスが初めて実行されるとき、それらは自動的に相互にネゴシエートして、TiDB ダッシュボードにサービスを提供するインスタンスを 1 つ選択します。 TiDB ダッシュボードは、他の PD インスタンスでは実行されません。 TiDB ダッシュボード サービスは、PD インスタンスが再起動されたり、新しい PD インスタンスが結合されたりしても、選択された PD インスタンスによって常に提供されます。ただし、TiDB ダッシュボードを提供する PD インスタンスがクラスターから削除される (スケールインされる) と、再ネゴシエーションが発生します。ネゴシエーション プロセスでは、ユーザーの介入は必要ありません。

TiDB ダッシュボードを提供しない PD インスタンスにアクセスすると、ブラウザが自動的にリダイレクトされ、TiDB ダッシュボードを提供する PD インスタンスにアクセスするように誘導されるため、通常どおりサービスにアクセスできます。このプロセスを下の図に示します。

![Process Schematic](/media/dashboard/dashboard-ops-multiple-pd.png)

> **ノート：**
>
> TiDB ダッシュボードを提供する PD インスタンスは、PD リーダーではない可能性があります。

### 実際に TiDB ダッシュボードを提供する PD インスタンスを確認する {#check-the-pd-instance-that-actually-serves-tidb-dashboard}

TiUP を使用してデプロイされた実行中のクラスターの場合、 `tiup cluster display`コマンドを使用して、どの PD インスタンスが TiDB ダッシュボードを提供しているかを確認できます。 `CLUSTER_NAME`クラスター名に置き換えます。

{{< copyable "" >}}

```bash
tiup cluster display CLUSTER_NAME --dashboard
```

出力例は次のとおりです。

```bash
http://192.168.0.123:2379/dashboard/
```

> **ノート：**
>
> この機能は、 `tiup cluster`展開ツールの新しいバージョン (v1.0.3 以降) でのみ使用できます。
>
> <details><summary>TiUPクラスタのアップグレード</summary>
>
> ```bash
> tiup update --self
> tiup update cluster --force
> ```
>
> </details>

### TiDB ダッシュボードを提供するために別の PD インスタンスに切り替える {#switch-to-another-pd-instance-to-serve-tidb-dashboard}

TiUPを使用してデプロイされた実行中のクラスターの場合、 `tiup ctl:v<CLUSTER_VERSION> pd`コマンドを使用して、TiDB ダッシュボードを提供する PD インスタンスを変更するか、無効になっている場合に TiDB ダッシュボードを提供する PD インスタンスを再指定できます。

{{< copyable "" >}}

```bash
tiup ctl:v<CLUSTER_VERSION> pd -u http://127.0.0.1:2379 config set dashboard-address http://9.9.9.9:2379
```

上記のコマンドでは:

-   `127.0.0.1:2379`を任意の PD インスタンスの IP とポートに置き換えます。
-   `9.9.9.9:2379`を、TiDB ダッシュボード サービスを実行する新しい PD インスタンスの IP とポートに置き換えます。

`tiup cluster display`コマンドを使用して、変更が有効になっているかどうかを確認できます ( `CLUSTER_NAME`クラスター名に置き換えます)。

{{< copyable "" >}}

```bash
tiup cluster display CLUSTER_NAME --dashboard
```

> **警告：**
>
> インスタンスを変更して TiDB ダッシュボードを実行すると、以前の TiDB ダッシュボード インスタンスに保存されていたローカル データ (キー ビジュアライズの履歴や検索履歴など) が失われます。

## TiDB ダッシュボードを無効にする {#disable-tidb-dashboard}

TiUPを使用してデプロイされた実行中のクラスターの場合、 `tiup ctl:v<CLUSTER_VERSION> pd`コマンドを使用して、すべての PD インスタンスで TiDB ダッシュボードを無効にします ( `127.0.0.1:2379`任意の PD インスタンスの IP とポートに置き換えます)。

{{< copyable "" >}}

```bash
tiup ctl:v<CLUSTER_VERSION> pd -u http://127.0.0.1:2379 config set dashboard-address none
```

TiDB ダッシュボードを無効にした後、どの PD インスタンスが TiDB ダッシュボード サービスを提供しているかの確認に失敗します。

```
Error: TiDB Dashboard is disabled
```

ブラウザ経由で PD インスタンスの TiDB ダッシュボード アドレスにアクセスしても失敗します。

```
Dashboard is not started.
```

## TiDB ダッシュボードを再度有効にする {#re-enable-tidb-dashboard}

TiUPを使用して展開された実行中のクラスターの場合、 `tiup ctl:v<CLUSTER_VERSION> pd`コマンドを使用して PD に要求し、インスタンスを再ネゴシエートして TiDB ダッシュボードを実行します ( `127.0.0.1:2379`任意の PD インスタンスの IP とポートに置き換えます)。

{{< copyable "" >}}

```bash
tiup ctl:v<CLUSTER_VERSION> pd -u http://127.0.0.1:2379 config set dashboard-address auto
```

上記のコマンドを実行した後、 `tiup cluster display`コマンドを使用して、PD によって自動的にネゴシエートされた TiDB ダッシュボード インスタンス アドレスを表示できます ( `CLUSTER_NAME`クラスター名に置き換えます)。

{{< copyable "" >}}

```bash
tiup cluster display CLUSTER_NAME --dashboard
```

TiDB ダッシュボードを提供する PD インスタンスを手動で指定して、TiDB ダッシュボードを再度有効にすることもできます。 [TiDB ダッシュボードを提供するために別の PD インスタンスに切り替える](#switch-to-another-pd-instance-to-serve-tidb-dashboard)を参照してください。

> **警告：**
>
> 新しく有効化された TiDB ダッシュボード インスタンスが、TiDB ダッシュボードを提供していた以前のインスタンスと異なる場合、以前の TiDB ダッシュボード インスタンスに保存されたローカル データ (キー ビジュアライズ履歴や検索履歴など) は失われます。

## 次は何ですか {#what-s-next}

-   TiDB ダッシュボード UI にアクセスしてログインする方法については、 [TiDB ダッシュボードにアクセスする](/dashboard/dashboard-access.md)を参照してください。

-   ファイアウォールの構成など、TiDB ダッシュボードのセキュリティを強化する方法については、 [セキュリティTiDB ダッシュボード](/dashboard/dashboard-ops-security.md)を参照してください。
