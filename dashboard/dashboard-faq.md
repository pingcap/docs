---
title: TiDB Dashboard FAQ
summary: Learn about the frequently asked questions (FAQs) and answers about TiDB Dashboard.
aliases: ['/docs/dev/dashboard/dashboard-faq/']
---

# TiDBダッシュボードFAQ {#tidb-dashboard-faq}

このドキュメントでは、TiDBダッシュボードに関するよくある質問（FAQ）と回答をまとめています。指示どおりに実行しても問題が見つからない、または解決しない場合は、PingCAPテクニカルサポートに連絡してください。

## アクセス関連のFAQ {#access-related-faq}

### ファイアウォールまたはリバースプロキシが構成されている場合、TiDBダッシュボード以外の内部アドレスにリダイレクトされます {#when-the-firewall-or-reverse-proxy-is-configured-i-am-redirected-to-an-internal-address-other-than-tidb-dashboard}

複数のPlacementDriver（PD）インスタンスがクラスタにデプロイされている場合、実際にTiDBダッシュボードサービスを実行しているのはPDインスタンスの1つだけです。これの代わりに他のPDインスタンスにアクセスすると、ブラウザは別のアドレスにリダイレクトします。ファイアウォールまたはリバースプロキシがTiDBダッシュボードにアクセスするように適切に構成されていない場合、ダッシュボードにアクセスすると、ファイアウォールまたはリバースプロキシによって保護されている内部アドレスにリダイレクトされる可能性があります。

-   複数のPDインスタンスを使用するTiDBダッシュボードの動作原理については、 [TiDBダッシュボードマルチPDインスタンスの展開](/dashboard/dashboard-ops-deploy.md)を参照してください。
-   リバースプロキシを正しく構成する方法については、 [リバースプロキシを介してTiDBダッシュボードを使用する](/dashboard/dashboard-ops-reverse-proxy.md)を参照してください。
-   ファイアウォールを正しく構成する方法については、 [セキュリティTiDBダッシュボード](/dashboard/dashboard-ops-security.md)を参照してください。

### TiDBダッシュボードがデュアルネットワークインターフェイスカード（NIC）で展開されている場合、別のNICを使用してTiDBダッシュボードにアクセスすることはできません {#when-tidb-dashboard-is-deployed-with-dual-network-interface-cards-nics-tidb-dashboard-cannot-be-accessed-using-another-nic}

セキュリティ上の理由から、PD上のTiDBダッシュボードは、展開中に指定されたIPアドレスのみを監視します（つまり、1つのNICでのみリッスンします） `0.0.0.0`では監視しません。したがって、ホストに複数のNICがインストールされている場合、別のNICを使用してTiDBダッシュボードにアクセスすることはできません。

`tiup cluster`または`tiup playground`コマンドを使用してTiDBを展開した場合、現在この問題は解決できません。 TiDBダッシュボードを別のNICに安全に公開するには、リバースプロキシを使用することをお勧めします。詳細については、 [リバースプロキシの背後でTiDBダッシュボードを使用する](/dashboard/dashboard-ops-reverse-proxy.md)を参照してください。

## UI関連のFAQ {#ui-related-faq}

### <code>prometheus_not_found</code>エラーは、[概要]ページの[ <strong>QPS</strong> ]セクションと[<strong>レイテンシ</strong>]セクションに表示されます {#a-code-prometheus-not-found-code-error-is-shown-in-strong-qps-strong-and-strong-latency-strong-sections-on-the-overview-page}

[**概要]**ページの[ <strong>QPS</strong> ]セクションと[<strong>レイテンシ]</strong>セクションには、Prometheusがデプロイされたクラスタが必要です。それ以外の場合は、エラーが表示されます。この問題は、Prometheusインスタンスをクラスタにデプロイすることで解決できます。

Prometheusインスタンスがデプロイされたときにこの問題が引き続き発生する場合は、デプロイメントツールが古く（TiUPまたはTiDB Operator）、ツールがメトリックアドレスを自動的に報告しないため、TiDBダッシュボードがクエリを実行できないことが考えられます。メトリック。デプロイメントツールを最新バージョンにアップグレードして、再試行できます。

展開ツールがTiUPの場合は、次の手順を実行してこの問題を解決してください。その他の展開ツールについては、それらのツールの対応するドキュメントを参照してください。

1.  TiUPおよびTiUPクラスターのアップグレード：

    {{< copyable "" >}}

    ```bash
    tiup update --self
    tiup update cluster --force
    ```

2.  アップグレード後、Prometheusインスタンスを使用して新しいクラスタをデプロイすると、メトリックを正常に表示できます。

3.  アップグレード後、既存のクラスタの場合、このクラスタを再起動してメトリックアドレスをレポートできます。 `CLUSTER_NAME`を実際のクラスタ名に置き換えます。

    {{< copyable "" >}}

    ```bash
    tiup cluster start CLUSTER_NAME
    ```

    クラスタが起動している場合でも、このコマンドを実行してください。このコマンドは、クラスタの通常のアプリケーションには影響しませんが、メトリックアドレスを更新して報告するため、監視メトリックをTiDBダッシュボードに通常どおり表示できます。

### <code>invalid connection</code>エラーは、[概要]ページの[<strong>Top SQLステートメント</strong>と<strong>最近の低速クエリ]</strong>に表示されます。 {#an-code-invalid-connection-code-error-is-shown-in-strong-top-sql-statements-strong-and-strong-recent-slow-queries-strong-on-the-overview-page}

考えられる理由は、TiDBの`prepared-plan-cache`つの機能を有効にしたことです。実験的機能として、有効にすると、 `prepared-plan-cache`は特定のTiDBバージョンで正しく機能しない可能性があり、TiDBダッシュボード（および他のアプリケーション）でこの問題を引き起こす可能性があります。この問題を解決するために[TiDBConfiguration / コンフィグレーションファイル](/tidb-configuration-file.md#prepared-plan-cache)を更新することにより、 `prepared-plan-cache`を無効にすることができます。

### <code>unknown field</code>エラーが<strong>[低速クエリ]</strong>ページに表示されます {#an-code-unknown-field-code-error-is-shown-in-strong-slow-queries-strong-page}

クラスタのアップグレード後に[**低速クエリ**]ページに`unknown field`のエラーが表示される場合、エラーは、TiDBダッシュボードサーバーフィールド（更新される可能性があります）とユーザー設定フィールド（ブラウザーキャッシュにある）の違いによって引き起こされる互換性の問題に関連しています。 。この問題は修正されました。クラスタがv5.0.3またはv4.0.14より前の場合は、次の手順を実行して問題を解決します。

ブラウザのキャッシュをクリアするには、次の手順を実行します。

1.  TiDBダッシュボードページを開きます。

2.  開発者ツールを開きます。ブラウザが異なれば、開発者ツールを開く方法も異なります。**メニューバー**をクリックした後：

    -   Firefox： **[メニュー]** &gt;[ <strong>Web開発者</strong>]&gt;[<strong>ツールの切り替え</strong>]、または[<strong>ツール</strong>]&gt;[ <strong>Web</strong>開発者]&gt;[ツールの<strong>切り替え</strong>]。
    -   Chrome：**その他のツール**&gt;<strong>開発者ツール</strong>。
    -   Safari：[**開発**]&gt;[ <strong>Webインスペクターを表示</strong>]。 [<strong>開発</strong>]メニューが表示されない場合は、[ <strong>Safari</strong> ]&gt;[<strong>設定]</strong> &gt;[<strong>詳細</strong>設定]に移動し、[メニューバーに[<strong>開発]メニューを表示する</strong>]チェックボックスをオンにします。

    次の例では、Chromeが使用されています。

    ![Opening DevTools from Chrome's main menu](/media/dashboard/dashboard-faq-devtools.png)

3.  [**アプリケーション**]パネルを選択し、[<strong>ローカルストレージ</strong>]メニューを展開して、[ <strong>TiDBダッシュボード]ページのドメイン</strong>を選択します。 [<strong>すべてクリア</strong>]ボタンをクリックします。

    ![Clear the Local Storage](/media/dashboard/dashboard-faq-devtools-application.png)

### <code>required component NgMonitoring is not started</code>エラーが表示されます {#a-code-required-component-ngmonitoring-is-not-started-code-error-is-shown}

NgMonitoringは、v5.4.0以降のバージョンのTiDBクラスターに組み込まれている高度な監視コンポーネントです。**連続プロファイリング**や<strong>Top SQL</strong>などの機能をサポートしています。 TiUPを使用してデプロイされたTiDBクラスタでは、NgMonitoringが自動的にデプロイされます。 TiDB Operatorを使用してデプロイされたTiDBクラスタでは、 [継続的なプロファイリングを有効にする](https://docs.pingcap.com/tidb-in-kubernetes/dev/access-dashboard/#enable-continuous-profiling)を参照してNgMonitoringを手動でデプロイする必要があります。

[**継続的なプロファイリング**]ページに`required component NgMonitoring is not started`が表示されている場合は、TiDBクラスタの展開方法に基づいて問題に対処します。

#### TiUPを使用してデプロイされたクラスター {#clusters-deployed-using-tiup}

手順1.バージョンを確認する

1.  TiUPクラスタのバージョンを確認してください。 NgMonitoringは、TiUPがv1.9.0以降の場合にのみ使用できます。

    {{< copyable "" >}}

    ```shell
    tiup cluster --version
    ```

    コマンド出力には、TiUPのバージョンが表示されます。例えば：

    ```
    tiup version 1.9.0 tiup
    Go Version: go1.17.2
    Git Ref: v1.9.0
    ```

2.  TiUPクラスタのバージョンがv1.9.0より前の場合は、TiUPおよびTiUPクラスタを最新バージョンにアップグレードします。

    {{< copyable "" >}}

    ```shell
    tiup update --all
    ```

手順2.TiUPを使用して、制御マシンにng_port構成項目を追加します。次に、Prometheusをリロードします。

1.  クラスタ構成ファイルを編集モードで開きます。

    {{< copyable "" >}}

    ```shell
    tiup cluster edit-config ${cluster-name}
    ```

2.  `monitoring_servers`の下に、 `ng_port:${port}`のパラメーターを追加します。

    ```
    monitoring_servers:
    - host: 172.16.6.6
      ng_port: ${port}
    ```

3.  プロメテウスをリロード：

    {{< copyable "" >}}

    ```shell
    tiup cluster reload ${cluster-name} --role prometheus
    ```

上記の手順を実行した後、TiDBダッシュボードで継続的プロファイリングを有効にします。それでもNgMonitoringを開始できない場合は、PingCAPテクニカルサポートに問い合わせてください。

#### TiDB Operatorを使用してデプロイされたクラスター {#clusters-deployed-using-tidb-operator}

[継続的なプロファイリングを有効にする](https://docs.pingcap.com/tidb-in-kubernetes/dev/access-dashboard/#enable-continuous-profiling)を参照してNgMonitoringをデプロイします。
