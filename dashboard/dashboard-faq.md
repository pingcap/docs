---
title: TiDB Dashboard FAQs
summary: Learn about the frequently asked questions (FAQs) and answers about TiDB Dashboard.
---

# TiDB ダッシュボードに関するよくある質問 {#tidb-dashboard-faqs}

このドキュメントには、TiDB ダッシュボードに関するよくある質問 (FAQ) とその回答がまとめられています。指示どおりに実行しても問題が見つからない場合、または問題が解決しない場合は、 [支持を得ます](/support.md) PingCAP またはコミュニティから連絡を受けます。

## アクセスに関するFAQ {#access-related-faq}

### ファイアウォールまたはリバース プロキシが構成されている場合、TiDB ダッシュボード以外の内部アドレスにリダイレクトされます {#when-the-firewall-or-reverse-proxy-is-configured-i-am-redirected-to-an-internal-address-other-than-tidb-dashboard}

複数の配置Driver(PD) インスタンスがクラスターにデプロイされている場合、PD インスタンスのうちの 1 つだけが実際に TiDB ダッシュボード サービスを実行します。このインスタンスではなく他の PD インスタンスにアクセスすると、ブラウザは別のアドレスにリダイレクトします。ファイアウォールまたはリバース プロキシが TiDB ダッシュボードにアクセスするために適切に構成されていない場合、ダッシュボードにアクセスすると、ファイアウォールまたはリバース プロキシによって保護されている内部アドレスにリダイレクトされる可能性があります。

-   複数の PD インスタンスを使用した TiDB ダッシュボードの動作原理については、 [TiDB ダッシュボードのマルチ PD インスタンスの展開](/dashboard/dashboard-ops-deploy.md)を参照してください。
-   リバース プロキシを正しく構成する方法については、 [リバース プロキシ経由で TiDB ダッシュボードを使用する](/dashboard/dashboard-ops-reverse-proxy.md)を参照してください。
-   ファイアウォールを正しく構成する方法については[セキュリティTiDB ダッシュボード](/dashboard/dashboard-ops-security.md)を参照してください。

### TiDB ダッシュボードがデュアル ネットワーク インターフェイス カード (NIC) で展開されている場合、別の NIC を使用して TiDB ダッシュボードにアクセスすることはできません {#when-tidb-dashboard-is-deployed-with-dual-network-interface-cards-nics-tidb-dashboard-cannot-be-accessed-using-another-nic}

セキュリティ上の理由から、PD 上の TiDB ダッシュボードは、展開中に指定された IP アドレスのみを監視します (つまり、 `0.0.0.0`つの NIC でのみリッスンします)。したがって、ホストに複数の NIC がインストールされている場合、別の NIC を使用して TiDB ダッシュボードにアクセスすることはできません。

`tiup cluster`または`tiup playground`コマンドを使用して TiDB をデプロイした場合、現時点ではこの問題は解決できません。 TiDB ダッシュボードを別の NIC に安全に公開するには、リバース プロキシを使用することをお勧めします。詳細は[リバース プロキシの背後で TiDB ダッシュボードを使用する](/dashboard/dashboard-ops-reverse-proxy.md)を参照してください。

## UI関連のFAQ {#ui-related-faq}

### <code>prometheus_not_found</code>エラーが、概要ページの<strong>QPS</strong>セクションと<strong>レイテンシ</strong>セクションに表示される {#a-code-prometheus-not-found-code-error-is-shown-in-strong-qps-strong-and-strong-latency-strong-sections-on-the-overview-page}

**「概要」**ページの**「QPS」**および**「レイテンシー」**セクションでは、Prometheus がデプロイされたクラスターが必要です。それ以外の場合は、エラーが表示されます。この問題は、クラスターに Prometheus インスタンスをデプロイすることで解決できます。

Prometheus インスタンスがデプロイされているときに引き続きこの問題が発生する場合は、デプロイメント ツール (TiUPまたはTiDB Operator) が古く、ツールがメトリクス アドレスを自動的にレポートしないため、TiDB ダッシュボードがクエリを実行できないことが考えられます。メトリクス。導入ツールを最新バージョンにアップグレードして、再試行できます。

デプロイメント ツールがTiUPの場合は、次の手順を実行してこの問題を解決してください。他の展開ツールについては、それらのツールの対応するドキュメントを参照してください。

1.  TiUPおよびTiUPクラスタをアップグレードします。

    ```bash
    tiup update --self
    tiup update cluster --force
    ```

2.  アップグレード後、Prometheus インスタンスを使用して新しいクラスターがデプロイされると、メトリックが通常どおり表示されます。

3.  アップグレード後、既存のクラスターの場合、このクラスターを再起動してメトリック アドレスをレポートできます。 `CLUSTER_NAME`実際のクラスター名に置き換えます。

    ```bash
    tiup cluster start CLUSTER_NAME
    ```

    クラスタが起動している場合でも、このコマンドを実行してください。このコマンドはクラスター内の通常のアプリケーションには影響しませんが、モニタリング メトリックを TiDB ダッシュボードに通常どおり表示できるように、メトリック アドレスを更新してレポートします。

### <strong>「遅いクエリ」</strong>ページに<code>invalid connection</code>エラーが表示される {#an-code-invalid-connection-code-error-is-shown-on-the-strong-slow-queries-strong-page}

考えられる理由は、TiDB のプリペアドプランキャッシュ機能を有効にしていることです。実験的機能として、有効にすると、プリペアドプランキャッシュが特定の TiDB バージョンで正しく機能しない可能性があり、TiDB ダッシュボード (および他のアプリケーション) でこの問題が発生する可能性があります。システム変数[`tidb_enable_prepared_plan_cache = OFF`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)を設定すると、プリペアドプランキャッシュを無効にできます。

### <code>required component NgMonitoring is not started</code>エラーが表示される {#a-code-required-component-ngmonitoring-is-not-started-code-error-is-shown}

NgMonitoring は、**継続的プロファイリング**や**Top SQL**などの TiDB ダッシュボード機能をサポートするために、v5.4.0 以降のバージョンの TiDB クラスターに組み込まれた高度な監視コンポーネントです。新しいバージョンのTiUPを使用してクラスターをデプロイまたはアップグレードすると、NgMonitoring が自動的にデプロイされます。 TiDB Operatorを使用してデプロイされたクラスターの場合は、 [継続的プロファイリングを有効にする](https://docs.pingcap.com/tidb-in-kubernetes/dev/access-dashboard/#enable-continuous-profiling)を参照して NgMonitoring を手動でデプロイできます。

Web ページに`required component NgMonitoring is not started`表示されている場合は、次のように展開の問題をトラブルシューティングできます。

<details><summary>TiUPを使用してデプロイされたクラスター</summary>

ステップ 1. バージョンを確認する

1.  TiUPクラスターのバージョンを確認します。 NgMonitoring は、 TiUP がv1.9.0 以降の場合にのみデプロイされます。

    ```shell
    tiup cluster --version
    ```

    コマンド出力には、 TiUP のバージョンが表示されます。例えば：

        tiup version 1.9.0 tiup
        Go Version: go1.17.2
        Git Ref: v1.9.0

2.  TiUPクラスターのバージョンが v1.9.0 より前の場合は、 TiUPとTiUPクラスターを最新バージョンにアップグレードします。

    ```shell
    tiup update --all
    ```

ステップ 2. TiUPを使用して、制御マシンに ng_port 構成項目を追加します。次に、Prometheus をリロードします。

1.  クラスター構成ファイルを編集モードで開きます。

    ```shell
    tiup cluster edit-config ${cluster-name}
    ```

2.  `monitoring_servers`の下に`ng_port:12020`パラメータを追加します。

        monitoring_servers:
        - host: 172.16.6.6
          ng_port: 12020

3.  プロメテウスをリロードします:

    ```shell
    tiup cluster reload ${cluster-name} --role prometheus
    ```

上記の手順を実行した後もエラー メッセージが表示される場合は、PingCAP またはコミュニティから[支持を得ます](/support.md) 。

</details>

<details><summary>TiDB Operatorを使用してデプロイされたクラスター</summary>

TiDB Operatorドキュメントの[継続的プロファイリングを有効にする](https://docs.pingcap.com/tidb-in-kubernetes/dev/access-dashboard/#enable-continuous-profiling)セクションの手順に従って、NgMonitoringコンポーネントをデプロイ。

</details>

<details><summary>TiUP Playground を使用して開始されたクラスター</summary>

クラスターを起動すると、 TiUP Playground (&gt;= v1.8.0) は自動的に NgMonitoringコンポーネントを起動します。 TiUP Playground を最新バージョンに更新するには、次のコマンドを実行します。

```shell
tiup update --self
tiup update playground
```

</details>

### <strong>「遅いクエリ」</strong>ページに<code>unknown field</code>エラーが表示される {#an-code-unknown-field-code-error-is-shown-on-the-strong-slow-queries-strong-page}

クラスターのアップグレード後に**[スロー クエリ]**ページに`unknown field`エラーが表示される場合、そのエラーは、TiDB ダッシュボードサーバーフィールド (更新される可能性があります) とユーザー設定フィールド (ブラウザー キャッシュ内にある) の間の違いによって引き起こされる互換性の問題に関連しています。 。この問題は修正されました。クラスターが v5.0.3 または v4.0.14 より前の場合は、次の手順を実行してブラウザーのキャッシュをクリアします。

1.  TiDB ダッシュボード ページを開きます。

2.  開発者ツールを開きます。ブラウザーが異なれば、開発者ツールを開く方法も異なります。**メニュー バー**をクリックした後:

    -   Firefox: **[メニュー**] &gt; **[Web 開発者]** &gt; **[ツールの切り替え]** 、または**[ツール]** &gt; **[Web 開発者]** &gt; **[ツールの切り替え]** 。
    -   Chrome:**その他のツール**&gt;**開発者ツール**。
    -   Safari: **[開発]** &gt; **[Web インスペクターを表示]** 。 **[開発]**メニューが表示されない場合は、 **[Safari]** &gt; **[環境設定**] &gt; **[詳細設定]**に移動し、[メニュー バーに**開発メニューを表示する**] チェックボックスをオンにします。

    次の例では Chrome が使用されています。

    ![Opening DevTools from Chrome's main menu](/media/dashboard/dashboard-faq-devtools.png)

3.  **「アプリケーション」**パネルを選択し、 **「ローカルストレージ」**メニューを展開して、 **「TiDB ダッシュボード」ページのドメイン**を選択します。 **「すべてクリア」**ボタンをクリックします。

    ![Clear the Local Storage](/media/dashboard/dashboard-faq-devtools-application.png)
