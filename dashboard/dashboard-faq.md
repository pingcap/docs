---
title: TiDB Dashboard FAQs
summary: Learn about the frequently asked questions (FAQs) and answers about TiDB Dashboard.
---

# TiDB ダッシュボードに関するよくある質問 {#tidb-dashboard-faqs}

このドキュメントは、TiDB ダッシュボードに関するよくある質問 (FAQ) と回答をまとめたものです。指示に従って実行しても問題が見つからない、または解決しない場合は、 [支持を得ます](/support.md) PingCAP またはコミュニティから連絡してください。

## アクセスに関するFAQ {#access-related-faq}

### ファイアウォールまたはリバース プロキシが構成されている場合、TiDB ダッシュボード以外の内部アドレスにリダイレクトされます {#when-the-firewall-or-reverse-proxy-is-configured-i-am-redirected-to-an-internal-address-other-than-tidb-dashboard}

複数の Placement Driver (PD) インスタンスがクラスターにデプロイされている場合、実際に TiDB ダッシュボード サービスを実行する PD インスタンスは 1 つだけです。このインスタンスの代わりに他の PD インスタンスにアクセスすると、ブラウザは別のアドレスにリダイレクトします。ファイアウォールまたはリバース プロキシが TiDB ダッシュボードにアクセスするように適切に構成されていない場合、ダッシュボードにアクセスすると、ファイアウォールまたはリバース プロキシによって保護されている内部アドレスにリダイレクトされることがあります。

-   複数の PD インスタンスを使用した TiDB ダッシュボードの動作原理については、 [TiDB ダッシュボード マルチ PD インスタンスの展開](/dashboard/dashboard-ops-deploy.md)を参照してください。
-   リバース プロキシを正しく構成する方法については、 [リバース プロキシ経由で TiDB ダッシュボードを使用する](/dashboard/dashboard-ops-reverse-proxy.md)を参照してください。
-   ファイアウォールを正しく構成する方法については[セキュリティTiDB ダッシュボード](/dashboard/dashboard-ops-security.md)を参照してください。

### TiDB ダッシュボードがデュアル ネットワーク インターフェイス カード (NIC) で展開されている場合、別の NIC を使用して TiDB ダッシュボードにアクセスすることはできません {#when-tidb-dashboard-is-deployed-with-dual-network-interface-cards-nics-tidb-dashboard-cannot-be-accessed-using-another-nic}

セキュリティ上の理由から、PD 上の TiDB ダッシュボードは、デプロイ時に指定された IP アドレスのみを監視し (つまり、1 つの NIC でのみリッスンします)、 `0.0.0.0`では監視しません。したがって、ホストに複数の NIC がインストールされている場合、別の NIC を使用して TiDB ダッシュボードにアクセスすることはできません。

`tiup cluster`または`tiup playground`コマンドを使用して TiDB をデプロイした場合、現在、この問題は解決できません。リバース プロキシを使用して、TiDB ダッシュボードを別の NIC に安全に公開することをお勧めします。詳細については、 [リバース プロキシの背後で TiDB ダッシュボードを使用する](/dashboard/dashboard-ops-reverse-proxy.md)を参照してください。

## UI関連のFAQ {#ui-related-faq}

### [概要] ページの<strong>[QPS]</strong>セクションと<strong>[レイテンシ]</strong>セクションに<code>prometheus_not_found</code>エラーが表示される {#a-code-prometheus-not-found-code-error-is-shown-in-strong-qps-strong-and-strong-latency-strong-sections-on-the-overview-page}

**[概要]**ページの<strong>[QPS]</strong>および<strong>[レイテンシ]</strong>セクションには、Prometheus がデプロイされたクラスターが必要です。それ以外の場合、エラーが表示されます。この問題は、Prometheus インスタンスをクラスターにデプロイすることで解決できます。

Prometheus インスタンスがデプロイされたときにこの問題が引き続き発生する場合、考えられる理由は、デプロイ ツールが古くなっている (TiUPまたはTiDB Operator) ことであり、ツールはメトリック アドレスを自動的に報告しないため、TiDB ダッシュボードはクエリを実行できません。指標。展開ツールを最新バージョンにアップグレードして、再試行できます。

展開ツールがTiUPの場合は、次の手順に従ってこの問題を解決してください。その他の展開ツールについては、それらのツールの対応するドキュメントを参照してください。

1.  TiUPおよびTiUPクラスタのアップグレード :

    {{< copyable "" >}}

    ```bash
    tiup update --self
    tiup update cluster --force
    ```

2.  アップグレード後、新しいクラスターが Prometheus インスタンスでデプロイされると、メトリックは正常に表示されます。

3.  アップグレード後、既存のクラスターの場合、このクラスターを再起動してメトリクス アドレスを報告できます。 `CLUSTER_NAME`実際のクラスター名に置き換えます。

    {{< copyable "" >}}

    ```bash
    tiup cluster start CLUSTER_NAME
    ```

    クラスタが起動している場合でも、このコマンドを実行してください。このコマンドは、クラスター内の通常のアプリケーションには影響しませんが、監視メトリックが TiDB ダッシュボードに正常に表示されるように、メトリック アドレスを更新して報告します。

### <strong>[スロー クエリ]</strong>ページに<code>invalid connection</code>エラーが表示される {#an-code-invalid-connection-code-error-is-shown-on-the-strong-slow-queries-strong-page}

考えられる理由は、TiDB のプリペアドプランキャッシュ機能を有効にしたことです。実験的機能として、有効にすると、 プリペアドプランキャッシュ が特定の TiDB バージョンで正しく機能しない可能性があり、TiDB ダッシュボード (およびその他のアプリケーション) でこの問題が発生する可能性があります。システム変数[`tidb_enable_prepared_plan_cache = OFF`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)を設定することで、 プリペアドプランキャッシュを無効にすることができます。

### <code>required component NgMonitoring is not started</code>エラーが表示される {#a-code-required-component-ngmonitoring-is-not-started-code-error-is-shown}

NgMonitoring は、v5.4.0 以降のバージョンの TiDB クラスターに組み込まれた高度な監視コンポーネントであり、**継続的なプロファイリング**や<strong>Top SQL</strong>などの TiDB ダッシュボード機能をサポートします。新しいバージョンのTiUPを使用してクラスターをデプロイまたはアップグレードすると、NgMonitoring が自動的にデプロイされます。 TiDB Operatorを使用してデプロイされたクラスターの場合、 [継続的なプロファイリングを有効にする](https://docs.pingcap.com/tidb-in-kubernetes/dev/access-dashboard/#enable-continuous-profiling)を参照して手動で NgMonitoring をデプロイできます。

Web ページに`required component NgMonitoring is not started`表示されている場合は、次のように展開の問題をトラブルシューティングできます。

<details><summary>TiUPを使用してデプロイされたクラスター</summary>

ステップ 1. バージョンを確認する

1.  TiUPクラスタのバージョンを確認してください。 NgMonitoring は、 TiUP がv1.9.0 以降の場合にのみデプロイされます。

    {{< copyable "" >}}

    ```shell
    tiup cluster --version
    ```

    コマンド出力にTiUP のバージョンが表示されます。例えば：

    ```
    tiup version 1.9.0 tiup
    Go Version: go1.17.2
    Git Ref: v1.9.0
    ```

2.  TiUPクラスターのバージョンが v1.9.0 より前の場合は、 TiUPとTiUPクラスターを最新バージョンにアップグレードします。

    {{< copyable "" >}}

    ```shell
    tiup update --all
    ```

ステップ 2. TiUPを使用して、制御マシンに ng_port 構成項目を追加します。次に、Prometheus をリロードします。

1.  クラスター構成ファイルを編集モードで開きます。

    {{< copyable "" >}}

    ```shell
    tiup cluster edit-config ${cluster-name}
    ```

2.  `monitoring_servers`の下に、 `ng_port:12020`パラメータを追加します。

    ```
    monitoring_servers:
    - host: 172.16.6.6
      ng_port: 12020
    ```

3.  プロメテウスをリロードします。

    {{< copyable "" >}}

    ```shell
    tiup cluster reload ${cluster-name} --role prometheus
    ```

上記の手順を実行してもエラー メッセージが引き続き表示される場合は、PingCAP またはコミュニティから[支持を得ます](/support.md) .

</details>

<details><summary>TiDB Operatorを使用してデプロイされたクラスター</summary>

TiDB Operatorドキュメントの[継続的なプロファイリングを有効にする](https://docs.pingcap.com/tidb-in-kubernetes/dev/access-dashboard/#enable-continuous-profiling)セクションの手順に従って、NgMonitoringコンポーネントをデプロイ。

</details>

<details><summary>TiUP Playground を使用して開始されたクラスター</summary>

クラスターを起動すると、 TiUP Playground (&gt;= v1.8.0) は NgMonitoringコンポーネントを自動的に起動します。 TiUP Playground を最新バージョンに更新するには、次のコマンドを実行します。

{{< copyable "" >}}

```shell
tiup update --self
tiup update playground
```

</details>

### <strong>[スロー クエリ]</strong>ページに<code>unknown field</code>エラーが表示される {#an-code-unknown-field-code-error-is-shown-on-the-strong-slow-queries-strong-page}

クラスターのアップグレード後に**[スロー クエリ]**ページに`unknown field`エラーが表示される場合、そのエラーは、TiDB ダッシュボードサーバーフィールド (更新される可能性があります) とユーザー設定フィールド (ブラウザー キャッシュにある) の違いによって引き起こされる互換性の問題に関連しています。 .この問題は修正されました。クラスターが v5.0.3 または v4.0.14 より前の場合は、次の手順を実行してブラウザーのキャッシュをクリアします。

1.  TiDB ダッシュボード ページを開きます。

2.  開発者ツールを開きます。ブラウザーが異なれば、開発者ツールを開く方法も異なります。**メニューバー**をクリックした後:

    -   Firefox: **[メニュー**] &gt; <strong>[Web 開発者]</strong> &gt; <strong>[ツールの切り替え</strong>] または<strong>[ツール]</strong> &gt; <strong>[Web 開発者]</strong> &gt; <strong>[ツールの切り替え]</strong> 。
    -   Chrome:**その他のツール**&gt;<strong>開発者ツール</strong>。
    -   Safari: **[開発]** &gt; <strong>[Web インスペクターを表示]</strong> 。 <strong>[開発]</strong>メニューが表示されない場合は、 <strong>[Safari]</strong> &gt; <strong>[設定</strong>] &gt; <strong>[詳細設定]</strong>に移動し、[メニュー バーに<strong>[開発] メニューを表示する</strong>] チェックボックスをオンにします。

    次の例では、Chrome が使用されています。

    ![Opening DevTools from Chrome's main menu](/media/dashboard/dashboard-faq-devtools.png)

3.  **[アプリケーション]**パネルを選択し、 <strong>[ローカル ストレージ]</strong>メニューを展開して、 <strong>TiDB ダッシュボード ページのドメイン</strong>を選択します。 <strong>[すべてクリア]</strong>ボタンをクリックします。

    ![Clear the Local Storage](/media/dashboard/dashboard-faq-devtools-application.png)
