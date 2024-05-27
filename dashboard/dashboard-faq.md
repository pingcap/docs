---
title: TiDB Dashboard FAQs
summary: このドキュメントでは、TiDB ダッシュボードに関する FAQ をまとめています。アクセス関連、UI 関連、およびデプロイメントに関する問題を取り上げ、それぞれの問題の解決策を示します。さらにサポートが必要な場合は、PingCAP またはコミュニティからサポートを受けることができます。
---

# TiDBダッシュボードに関するよくある質問 {#tidb-dashboard-faqs}

このドキュメントでは、TiDB ダッシュボードに関するよくある質問 (FAQ) と回答をまとめています。指示どおりに実行しても問題が見つからない、または問題が解決しない場合は、PingCAP またはコミュニティに[支持を得ます](/support.md)ください。

## アクセスに関するFAQ {#access-related-faq}

### ファイアウォールまたはリバースプロキシが設定されている場合、TiDBダッシュボード以外の内部アドレスにリダイレクトされます {#when-the-firewall-or-reverse-proxy-is-configured-i-am-redirected-to-an-internal-address-other-than-tidb-dashboard}

複数の Placement Driver (PD) インスタンスがクラスターにデプロイされている場合、実際に TiDB ダッシュボード サービスを実行するのは PD インスタンスの 1 つだけです。このインスタンスではなく他の PD インスタンスにアクセスすると、ブラウザーは別のアドレスにリダイレクトします。TiDB ダッシュボードにアクセスするためにファイアウォールまたはリバース プロキシが適切に構成されていない場合、ダッシュボードにアクセスすると、ファイアウォールまたはリバース プロキシによって保護されている内部アドレスにリダイレクトされることがあります。

-   複数の PD インスタンスを使用した TiDB ダッシュボードの動作原理については、 [TiDB ダッシュボード マルチ PD インスタンスの展開](/dashboard/dashboard-ops-deploy.md)参照してください。
-   リバース プロキシを正しく構成する方法については、 [リバースプロキシ経由でTiDBダッシュボードを使用する](/dashboard/dashboard-ops-reverse-proxy.md)参照してください。
-   ファイアウォールを正しく構成する方法については、 [セキュリティTiDB ダッシュボード](/dashboard/dashboard-ops-security.md)参照してください。

### TiDBダッシュボードがデュアルネットワークインターフェースカード（NIC）で展開されている場合、別のNICを使用してTiDBダッシュボードにアクセスすることはできません。 {#when-tidb-dashboard-is-deployed-with-dual-network-interface-cards-nics-tidb-dashboard-cannot-be-accessed-using-another-nic}

セキュリティ上の理由から、PD 上の TiDB ダッシュボードは、 `0.0.0.0`ではなく、デプロイメント時に指定された IP アドレスのみを監視します (つまり、1 つの NIC のみをリッスンします)。したがって、ホストに複数の NIC がインストールされている場合、別の NIC を使用して TiDB ダッシュボードにアクセスすることはできません。

`tiup cluster`または`tiup playground`コマンドを使用して TiDB をデプロイした場合、現時点ではこの問題を解決することはできません。リバース プロキシを使用して、TiDB ダッシュボードを別の NIC に安全に公開することをお勧めします。詳細については、 [リバースプロキシの背後で TiDB ダッシュボードを使用する](/dashboard/dashboard-ops-reverse-proxy.md)を参照してください。

## UI関連のFAQ {#ui-related-faq}

### 概要ページの<strong>QPS</strong>と<strong>レイテンシの</strong>セクションに<code>prometheus_not_found</code>エラーが表示される {#a-code-prometheus-not-found-code-error-is-shown-in-strong-qps-strong-and-strong-latency-strong-sections-on-the-overview-page}

**概要**ページの**QPS セクション**と**レイテンシ**セクションには、Prometheus がデプロイされたクラスターが必要です。そうでない場合は、エラーが表示されます。この問題は、クラスターに Prometheus インスタンスをデプロイすることで解決できます。

Prometheus インスタンスがデプロイされた後もこの問題が発生する場合は、デプロイメント ツールが古く (TiUPまたはTiDB Operator)、ツールがメトリック アドレスを自動的に報告しないため、TiDB ダッシュボードがメトリックをクエリできないことが原因である可能性があります。デプロイメント ツールを最新バージョンにアップグレードして、もう一度試してください。

デプロイメント ツールがTiUPの場合は、次の手順を実行してこの問題を解決してください。その他のデプロイメント ツールについては、それぞれのツールの対応するドキュメントを参照してください。

1.  TiUPおよびTiUPクラスタのアップグレード:

    ```bash
    tiup update --self
    tiup update cluster --force
    ```

2.  アップグレード後、Prometheus インスタンスを使用して新しいクラスターをデプロイすると、メトリックが正常に表示されます。

3.  アップグレード後、既存のクラスターを再起動してメトリック アドレスを報告できます。1 `CLUSTER_NAME`実際のクラスター名に置き換えます。

    ```bash
    tiup cluster start CLUSTER_NAME
    ```

    クラスターが起動している場合でも、このコマンドを実行してください。このコマンドはクラスター内の通常のアプリケーションには影響しませんが、メトリック アドレスを更新してレポートするため、TiDB ダッシュボードで監視メトリックを正常に表示できます。

### <strong>スロークエリ</strong>ページに<code>invalid connection</code>エラーが表示されます {#an-code-invalid-connection-code-error-is-shown-on-the-strong-slow-queries-strong-page}

考えられる原因は、TiDB のプリペアドプランキャッシュ機能を有効にしていることです。実験的機能であるため、有効にすると、特定の TiDB バージョンでプリペアドプランキャッシュが正しく機能しない可能性があり、TiDB ダッシュボード (およびその他のアプリケーション) でこの問題が発生する可能性があります。プリペアドプランキャッシュを無効にするには、システム変数[`tidb_enable_prepared_plan_cache = OFF`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)を設定します。

### <code>required component NgMonitoring is not started</code>エラーが表示されます {#a-code-required-component-ngmonitoring-is-not-started-code-error-is-shown}

NgMonitoring は、**継続的なプロファイリング**や**Top SQL**などの TiDB ダッシュボード機能をサポートするために、v5.4.0 以降のバージョンの TiDB クラスターに組み込まれた高度な監視コンポーネントです。TiUPの新しいバージョンを使用してクラスターをデプロイまたはアップグレードすると、NgMonitoring が自動的にデプロイされます。TiDB TiDB Operatorを使用してデプロイされたクラスターの場合は、 [継続的なプロファイリングを有効にする](https://docs.pingcap.com/tidb-in-kubernetes/dev/access-dashboard/#enable-continuous-profiling)を参照して NgMonitoring を手動でデプロイできます。

Web ページに`required component NgMonitoring is not started`表示される場合は、次のようにしてデプロイメントの問題をトラブルシューティングできます。

<details><summary>TiUPを使用して展開されたクラスター</summary>

ステップ1. バージョンを確認する

1.  TiUPクラスターのバージョンを確認します。NgMonitoring は、 TiUPが v1.9.0 以降の場合にのみデプロイされます。

    ```shell
    tiup cluster --version
    ```

    コマンド出力にはTiUP のバージョンが表示されます。例:

        tiup version 1.9.0 tiup
        Go Version: go1.17.2
        Git Ref: v1.9.0

2.  TiUPクラスターのバージョンが v1.9.0 より前の場合は、 TiUPとTiUPクラスターを最新バージョンにアップグレードします。

    ```shell
    tiup update --all
    ```

ステップ 2. TiUPを使用して、コントロール マシンに ng_port 構成項目を追加します。次に、Prometheus をリロードします。

1.  クラスター構成ファイルを編集モードで開きます。

    ```shell
    tiup cluster edit-config ${cluster-name}
    ```

2.  `monitoring_servers`の下に`ng_port:12020`パラメータを追加します。

        monitoring_servers:
        - host: 172.16.6.6
          ng_port: 12020

3.  Prometheus をリロードします:

    ```shell
    tiup cluster reload ${cluster-name} --role prometheus
    ```

上記の手順を実行した後もエラー メッセージが表示される場合は、PingCAP またはコミュニティから[支持を得ます](/support.md)問い合わせてください。

</details>

<details><summary>TiDB Operatorを使用してデプロイされたクラスター</summary>

TiDB Operatorドキュメントのセクション[継続的なプロファイリングを有効にする](https://docs.pingcap.com/tidb-in-kubernetes/dev/access-dashboard/#enable-continuous-profiling)の手順に従って、NgMonitoringコンポーネントをデプロイ。

</details>

<details><summary>TiUP Playground の使用を開始したクラスター</summary>

クラスターを起動すると、 TiUP Playground (&gt;= v1.8.0) は NgMonitoringコンポーネントを自動的に起動します。TiUP Playgroundを最新バージョンに更新するには、次のコマンドを実行します。

```shell
tiup update --self
tiup update playground
```

</details>

### <strong>スロークエリ</strong>ページに<code>unknown field</code>エラーが表示される {#an-code-unknown-field-code-error-is-shown-on-the-strong-slow-queries-strong-page}

クラスターのアップグレード後に**「遅いクエリ」**ページにエラー`unknown field`が表示される場合、そのエラーは、TiDB ダッシュボードサーバーのフィールド (更新される可能性がある) とユーザー設定フィールド (ブラウザー キャッシュ内にある) の違いによって発生する互換性の問題に関連しています。この問題は修正されています。クラスターが v5.0.3 または v4.0.14 より前の場合は、次の手順を実行してブラウザー キャッシュをクリアしてください。

1.  TiDB ダッシュボード ページを開きます。

2.  開発者ツールを開きます。ブラウザによって開発者ツールを開く方法が異なります。**メニューバーを**クリックした後:

    -   Firefox:**メニュー**&gt; **Web 開発**&gt;**ツールの切り替え**、または**ツール**&gt; **Web 開発**&gt;**ツールの切り替え**。
    -   Chrome:**その他のツール**&gt;**開発者ツール**。
    -   Safari:**開発**&gt; **Web インスペクタを表示**。**開発**メニューが表示されない場合は、 **Safari** &gt;**環境設定**&gt;**詳細**に移動し、メニューバーに**開発**メニューを表示チェックボックスをオンにします。

    次の例では、Chrome が使用されています。

    ![Opening DevTools from Chrome's main menu](/media/dashboard/dashboard-faq-devtools.png)

3.  **アプリケーション**パネルを選択し、**ローカル ストレージ**メニューを展開して、 **TiDB ダッシュボード ページ ドメイン**を選択します。**すべてクリア**ボタンをクリックします。

    ![Clear the Local Storage](/media/dashboard/dashboard-faq-devtools-application.png)
