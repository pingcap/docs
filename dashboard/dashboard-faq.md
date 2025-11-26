---
title: TiDB Dashboard FAQs
summary: このドキュメントは、TiDBダッシュボードに関するよくある質問をまとめたものです。アクセス関連、UI関連、そして導入に関する問題を網羅し、それぞれの解決策をご案内しています。さらにサポートが必要な場合は、PingCAPまたはコミュニティからサポートを受けることができます。
---

# TiDBダッシュボードに関するよくある質問 {#tidb-dashboard-faqs}

このドキュメントは、TiDBダッシュボードに関するよくある質問（FAQ）と回答をまとめたものです。指示通りに実行しても問題が見つからない場合、または問題が解決しない場合は、PingCAPまたはコミュニティにお[サポートを受ける](/support.md)ください。

## アクセスに関するよくあるFAQ {#access-related-faq}

### ファイアウォールまたはリバースプロキシが設定されている場合、TiDBダッシュボード以外の内部アドレスにリダイレクトされます {#when-the-firewall-or-reverse-proxy-is-configured-i-am-redirected-to-an-internal-address-other-than-tidb-dashboard}

クラスター内に複数の配置Driver（PD）インスタンスがデプロイされている場合、TiDBダッシュボードサービスを実際に実行するPDインスタンスは1つだけです。このPDインスタンスではなく他のPDインスタンスにアクセスすると、ブラウザは別のアドレスにリダイレクトします。TiDBダッシュボードへのアクセス用にファイアウォールまたはリバースプロキシが適切に設定されていない場合、ダッシュボードにアクセスした際に、ファイアウォールまたはリバースプロキシによって保護されている内部アドレスにリダイレクトされる可能性があります。

-   複数の PD インスタンスを使用した TiDB ダッシュボードの動作原理については、 [TiDB ダッシュボードのマルチ PD インスタンスの展開](/dashboard/dashboard-ops-deploy.md)参照してください。
-   リバース プロキシを正しく構成する方法については、 [リバースプロキシ経由でTiDBダッシュボードを使用する](/dashboard/dashboard-ops-reverse-proxy.md)参照してください。
-   ファイアウォールを正しく構成する方法については、 [セキュリティTiDBダッシュボード](/dashboard/dashboard-ops-security.md)参照してください。

### TiDBダッシュボードがデュアルネットワークインターフェースカード（NIC）で展開されている場合、別のNICを使用してTiDBダッシュボードにアクセスすることはできません。 {#when-tidb-dashboard-is-deployed-with-dual-network-interface-cards-nics-tidb-dashboard-cannot-be-accessed-using-another-nic}

セキュリティ上の理由から、PD上のTiDBダッシュボードは、デプロイメント時に指定されたIPアドレスのみを監視します（つまり、1つのNICのみを監視します）。1 `0.0.0.0`のNICのみを監視するわけではありません。そのため、ホストに複数のNICがインストールされている場合、別のNICを使用してTiDBダッシュボードにアクセスすることはできません。

`tiup cluster`または`tiup playground`コマンドを使用して TiDB をデプロイした場合、現時点ではこの問題を解決できません。リバースプロキシを使用して、TiDB ダッシュボードを別の NIC に安全に公開することをお勧めします。詳細は[リバースプロキシの背後で TiDB ダッシュボードを使用する](/dashboard/dashboard-ops-reverse-proxy.md)参照してください。

## UIに関するよくあるFAQ {#ui-related-faq}

### 概要ページの<strong>QPS</strong>と<strong>レイテンシの</strong>セクションに<code>prometheus_not_found</code>エラーが表示される {#a-code-prometheus-not-found-code-error-is-shown-in-strong-qps-strong-and-strong-latency-strong-sections-on-the-overview-page}

**概要**ページの**QPS**と**レイテンシの**セクションには、Prometheusがデプロイされたクラスターが必要です。そうでない場合、エラーが表示されます。この問題を解決するには、クラスターにPrometheusインスタンスをデプロイしてください。

Prometheusインスタンスをデプロイしてもこの問題が引き続き発生する場合は、デプロイメントツール（TiUPまたはTiDB Operator）が古く、ツールがメトリクスアドレスを自動的に報告しないため、TiDBダッシュボードでメトリクスをクエリできないことが原因である可能性があります。デプロイメントツールを最新バージョンにアップグレードして、もう一度お試しください。

デプロイメントツールがTiUPの場合は、以下の手順に従って問題を解決してください。その他のデプロイメントツールについては、それぞれのツールのドキュメントを参照してください。

1.  TiUPおよびTiUPクラスタのアップグレード:

    ```bash
    tiup update --self
    tiup update cluster --force
    ```

2.  アップグレード後、Prometheus インスタンスを使用して新しいクラスターをデプロイすると、メトリックが正常に表示されます。

3.  アップグレード後、既存のクラスターを再起動してメトリクスアドレスを報告できます。1 `CLUSTER_NAME`実際のクラスター名に置き換えてください。

    ```bash
    tiup cluster start CLUSTER_NAME
    ```

    クラスタが起動している場合でも、このコマンドを実行してください。このコマンドはクラスタ内の通常のアプリケーションには影響を与えませんが、メトリクスアドレスを更新してレポートするため、TiDBダッシュボードに監視メトリクスが正常に表示されるようになります。

### <strong>スロークエリ</strong>ページに<code>invalid connection</code>エラーが表示されます {#an-code-invalid-connection-code-error-is-shown-on-the-strong-slow-queries-strong-page}

原因として考えられるのは、TiDBのプリペアドプランキャッシュ機能を有効にしていることです。これは実験的機能であるため、有効にすると特定のTiDBバージョンでプリペアドプランキャッシュが正常に機能しない可能性があり、TiDBダッシュボード（およびその他のアプリケーション）でこの問題が発生する可能性があります。プリペアドプランキャッシュを無効にするには、システム変数[`tidb_enable_prepared_plan_cache = OFF`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)設定します。

### <code>required component NgMonitoring is not started</code>というエラーが表示されます {#a-code-required-component-ngmonitoring-is-not-started-code-error-is-shown}

NgMonitoringは、TiDB v5.4.0以降のバージョンに組み込まれた高度な監視コンポーネントで、**継続的プロファイリング**や**Top SQL**などのTiDBダッシュボード機能をサポートします。TiUPの新しいバージョンを使用してクラスターをデプロイまたはアップグレードすると、NgMonitoringが自動的にデプロイされます。TiDB TiDB Operatorを使用してデプロイされたクラスターの場合は、 [継続的なプロファイリングを有効にする](https://docs.pingcap.com/tidb-in-kubernetes/v1.6/access-dashboard/#enable-continuous-profiling)を参照してTiUPを手動でデプロイできます。

Web ページに`required component NgMonitoring is not started`が表示されている場合は、次のようにしてデプロイメントの問題をトラブルシューティングできます。

<details><summary>TiUPを使用して展開されたクラスター</summary>

ステップ1. バージョンを確認する

1.  TiUPクラスターのバージョンを確認してください。NgMonitoring はTiUP v1.9.0 以降の場合にのみデプロイされます。

    ```shell
    tiup cluster --version
    ```

    コマンド出力にはTiUPのバージョンが表示されます。例:

        tiup version 1.9.0 tiup
        Go Version: go1.17.2
        Git Ref: v1.9.0

2.  TiUPクラスターのバージョンが v1.9.0 より前の場合は、 TiUPとTiUPクラスターを最新バージョンにアップグレードします。

    ```shell
    tiup update --all
    ```

ステップ2. TiUPを使用して、コントロールマシンにng_port設定項目を追加します。その後、Prometheusをリロードします。

1.  クラスター構成ファイルを編集モードで開きます。

    ```shell
    tiup cluster edit-config ${cluster-name}
    ```

2.  `monitoring_servers`の下に`ng_port:12020`パラメータを追加します。

        monitoring_servers:
        - host: 172.16.6.6
          ng_port: 12020

3.  Prometheus をリロードします。

    ```shell
    tiup cluster reload ${cluster-name} --role prometheus
    ```

上記の手順を実行した後もエラー メッセージが表示される場合は、PingCAP またはコミュニティに問い合わせて[サポートを受ける](/support.md) 。

</details>

<details><summary>TiDB Operatorを使用してデプロイされたクラスター</summary>

TiDB Operatorのドキュメントのセクション[継続的なプロファイリングを有効にする](https://docs.pingcap.com/tidb-in-kubernetes/v1.6/access-dashboard/#enable-continuous-profiling)手順に従って、NgMonitoringコンポーネントをデプロイ。

</details>

<details><summary>TiUP Playgroundを使用したクラスターの開始</summary>

クラスタを起動すると、 TiUP Playground (&gt;= v1.8.0) は NgMonitoringコンポーネントを自動的に起動します。TiUP Playgroundを最新バージョンに更新するには、次のコマンドを実行します。

```shell
tiup update --self
tiup update playground
```

</details>

### <strong>スロークエリ</strong>ページに<code>unknown field</code>エラーが表示されます {#an-code-unknown-field-code-error-is-shown-on-the-strong-slow-queries-strong-page}

クラスターのアップグレード後に**「スロークエリ」**ページにエラー`unknown field`が表示される場合、そのエラーはTiDBダッシュボードのサーバーフィールド（更新される可能性があります）とユーザー設定フィールド（ブラウザキャッシュ内）の差異に起因する互換性の問題に関連しています。この問題は修正されています。クラスターのバージョンがv5.0.3またはv4.0.14より前の場合は、以下の手順に従ってブラウザキャッシュをクリアしてください。

1.  TiDB ダッシュボード ページを開きます。

2.  開発者ツールを開きます。ブラウザによって開発者ツールの開き方が異なります。**メニューバー**をクリックした後、以下の手順に従ってください。

    -   Firefox:**メニュー**&gt; **Web 開発**&gt;**ツールの切り替え**、または**ツール**&gt; **Web 開発**&gt;**ツールの切り替え**。
    -   Chrome:**その他のツール**&gt;**開発者ツール**。
    -   Safari:**開発**&gt; **Webインスペクタを表示**。**開発**メニューが表示されない場合は、 **Safari** &gt;**環境設定**&gt;**詳細**に移動し、メニューバーに**開発メニューを表示**チェックボックスをオンにします。

    次の例では、Chrome が使用されています。

    ![Opening DevTools from Chrome's main menu](/media/dashboard/dashboard-faq-devtools.png)

3.  **アプリケーション**パネルを選択し、**ローカルストレージ**メニューを展開して、 **TiDBダッシュボードページのドメイン**を選択します。「**すべてクリア」**ボタンをクリックします。

    ![Clear the Local Storage](/media/dashboard/dashboard-faq-devtools-application.png)
