---
title: TiProxy Overview
summary: TiProxy の主な機能、インストール、および使用方法を学びます。
---

# TiProxy の概要 {#tiproxy-overview}

TiProxyはPingCAPの公式プロキシコンポーネントです。クライアントとTiDBサーバーの間に配置され、負荷分散、接続の持続性、サービス検出、その他のTiDB機能を提供します。

TiProxy はオプションのコンポーネントです。サードパーティ製のプロキシコンポーネントを使用することも、プロキシを使用せずに TiDBサーバーに直接接続することもできます。

次の図は、TiProxy のアーキテクチャを示しています。

<img src="https://docs-download.pingcap.com/media/images/docs/tiproxy/tiproxy-architecture.png" alt="TiProxyアーキテクチャ" width="500" />

## 主な特徴 {#main-features}

TiProxy は、接続の移行、フェイルオーバー、サービスの検出、および迅速な展開を提供します。

### 接続の移行 {#connection-migration}

TiProxy は、クライアント接続を切断することなく、ある TiDBサーバーから別の TiDB サーバーに接続を移行できます。

下図に示すように、クライアントは当初TiProxyを介してTiDB 1に接続します。接続の移行後、クライアントは実際にはTiDB 2に接続します。TiDB 1がオフラインになりそうになった場合、またはTiDB 1とTiDB 2の接続比率が設定されたしきい値を超えた場合、接続の移行がトリガーされます。クライアントは接続の移行を認識しません。

<img src="https://docs-download.pingcap.com/media/images/docs/tiproxy/tiproxy-session-migration.png" alt="TiProxy接続の移行" width="400" />

接続の移行は通常、次のシナリオで発生します。

-   TiDBサーバーがスケールイン、ローリング アップグレード、またはローリング リスタートを実行する場合、TiProxy はオフラインになる予定の TiDBサーバーから他の TiDB サーバーへの接続を移行して、クライアント接続を維持できます。
-   TiDBサーバーがスケールアウトを実行すると、TiProxy は既存の接続を新しい TiDBサーバーに移行し、クライアント接続プールをリセットせずにリアルタイムの負荷分散を実現できます。

### フェイルオーバー {#failover}

TiDBサーバーがメモリ不足 (OOM) になる危険がある場合、または PD または TiKV に接続できない場合、TiProxy は問題を自動的に検出し、接続を別の TiDBサーバーに移行して、継続的なクライアント接続を確保します。

### サービス検出 {#service-discovery}

TiDBサーバーがスケールインまたはスケールアウトを実行する際、共通のロードバランサーを使用している場合は、TiDBサーバーリストを手動で更新する必要があります。しかし、TiProxyは手動操作なしでTiDBサーバーリストを自動的に検出します。

### 迅速な展開 {#quick-deployment}

TiProxy は[TiUP](https://github.com/pingcap/tiup) 、 [TiDB Operator](https://github.com/pingcap/tidb-operator) 、 [TiDBダッシュボード](/dashboard/dashboard-intro.md) 、および[グラファナ](/tiproxy/tiproxy-grafana.md)に統合されており、組み込みの仮想 IP 管理をサポートしているため、導入、運用、および管理のコストが削減されます。

## ユーザーシナリオ {#user-scenarios}

TiProxy は次のシナリオに適しています。

-   接続の持続性：TiDBサーバーがスケールイン、ローリングアップグレード、またはローリングリスタートを実行すると、クライアント接続が切断され、エラーが発生します。クライアントに冪等なエラーリトライメカニズムがない場合、手動でエラーを確認して修正する必要があり、人件費が大幅に増加します。TiProxyはクライアント接続を維持できるため、クライアントはエラーを報告しません。
-   頻繁なスケールインとスケールアウト：アプリケーションのワークロードは定期的に変化する可能性があります。コスト削減のため、TiDBをクラウドにデプロイし、ワークロードに応じてTiDBサーバーを自動的にスケールインおよびスケールアウトすることができます。ただし、スケールインはクライアントの接続を切断する可能性があり、スケールアウトは負荷の不均衡を引き起こす可能性があります。TiProxyはクライアント接続を維持し、負荷分散を実現します。
-   CPU負荷の不均衡：バックグラウンドタスクが大量のCPUリソースを消費したり、接続間のワークロードが大きく変動してCPU負荷の不均衡が生じたりした場合、TiProxyはCPU使用率に基づいて接続を移行することで負荷分散を実現します。詳細については、 [CPUベースの負荷分散](/tiproxy/tiproxy-load-balance.md#cpu-based-load-balancing)参照してください。
-   TiDBサーバーのメモリ不足：クエリの暴走によってTiDBサーバーのメモリが不足した場合、TiProxyはOOMリスクを事前に検出し、他の正常な接続を別のTiDBサーバーに移行することで、クライアントの継続的な接続を確保します。詳細については、 [メモリベースの負荷分散](/tiproxy/tiproxy-load-balance.md#memory-based-load-balancing)参照してください。

TiProxy は次のシナリオには適していません。

-   パフォーマンスの影響を受けやすい：TiProxyのパフォーマンスはHAProxyや他のロードバランサよりも低いため、TiProxyを使用する場合は、同等のパフォーマンスレベルを維持するためにより多くのCPUリソースを予約する必要があります。詳細については、 [TiProxy パフォーマンステストレポート](/tiproxy/tiproxy-performance-test.md)を参照してください。
-   コストの影響を受けやすい：TiDB クラスターがハードウェアロードバランサー、仮想 IP、または Kubernetes が提供するロードバランサーを使用している場合、TiProxy を追加するとコストが増加します。さらに、クラウド上の複数のアベイラビリティゾーンに TiDB クラスターを展開する場合、TiProxy を追加するとアベイラビリティゾーン間のトラフィックコストも増加します。
-   予期せぬTiDBサーバーのダウンタイムに対するフェイルオーバー：TiProxyは、TiDBサーバーがオフラインの場合、または計画通りに再起動された場合にのみクライアント接続を維持できます。TiDBサーバーが予期せずオフラインになった場合、接続は依然として切断されます。

TiProxy が適しているシナリオでは TiProxy を使用し、アプリケーションがパフォーマンスに敏感な場合は HAProxy またはその他のプロキシを使用することをお勧めします。

## インストールと使用方法 {#installation-and-usage}

このセクションでは、 TiUPを使用して TiProxy をデプロイおよび変更する方法について説明します。TiProxy をスケールアウトすることで、 [TiProxyで新しいクラスターを作成する](#create-a-cluster-with-tiproxy)または[既存のクラスターで TiProxy を有効にする](#enable-tiproxy-for-an-existing-cluster)いずれかを実行できます。

> **注記：**
>
> TiUPが v1.16.1 以降であることを確認してください。

その他の展開方法については、次のドキュメントを参照してください。

-   TiDB Operatorを使用して TiProxy をデプロイするには、 [TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tiproxy)ドキュメントを参照してください。
-   TiUPを使用して TiProxy をローカルに素早く展開するには、 [TiProxyをデプロイ](/tiup/tiup-playground.md#deploy-tiproxy)参照してください。

### TiProxyでクラスターを作成する {#create-a-cluster-with-tiproxy}

次の手順では、新しいクラスターを作成するときに TiProxy をデプロイする方法について説明します。

1.  TiDB インスタンスを構成します。

    TiProxyを使用する場合、TiDBに[`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-new-in-v50)設定する必要があります。この値は、アプリケーションの最長トランザクションの所要時間より少なくとも10秒長く設定する必要があります。これにより、TiDBサーバーがオフラインになった場合にクライアント接続が中断されるのを回避できます。トランザクションの所要時間は[TiDB モニタリング ダッシュボードのトランザクションメトリック](/grafana-tidb-dashboard.md#transaction)で確認できます。詳細については、 [制限事項](#limitations)参照してください。

    設定例は次のとおりです。

    ```yaml
    server_configs:
      tidb:
        graceful-wait-before-shutdown: 30
    ```

2.  TiProxy インスタンスを構成します。

    TiProxy の高可用性を確保するには、少なくとも 2 つの TiProxy インスタンスを展開し、 [`ha.virtual-ip`](/tiproxy/tiproxy-configuration.md#virtual-ip)と[`ha.interface`](/tiproxy/tiproxy-configuration.md#interface)設定して仮想 IP を構成し、使用可能な TiProxy インスタンスにトラフィックをルーティングすることをお勧めします。

    次の点に注意してください。

    -   ワークロードの種類と最大QPSに基づいて、TiProxyインスタンスのモデルと数を選択してください。詳細については、 [TiProxy パフォーマンステストレポート](/tiproxy/tiproxy-performance-test.md)参照してください。
    -   通常、TiProxyインスタンス数はTiDBサーバーインスタンス数よりも少ないため、TiProxyのネットワーク帯域幅がボトルネックになりやすくなります。例えばAWSでは、同シリーズのEC2インスタンスのベースラインネットワーク帯域幅はCPUコア数に比例しません。ネットワーク帯域幅がボトルネックになる場合は、TiProxyインスタンスをより多くの小さなインスタンスに分割することでQPSを向上させることができます。詳細は[ネットワーク仕様](https://docs.aws.amazon.com/ec2/latest/instancetypes/co.html#co_network)参照してください。
    -   トポロジ設定ファイルでTiProxyのバージョンを指定することをお勧めします。これにより、TiDBクラスタをアップグレードするために[`tiup cluster upgrade`](/tiup/tiup-component-cluster-upgrade.md)実行した際にTiProxyが自動的にアップグレードされることがなくなり、TiProxyのアップグレードによってクライアント接続が切断されることを防ぐことができます。

    TiProxy のテンプレートの詳細については、 [TiProxyトポロジのシンプルなテンプレート](https://github.com/pingcap/docs/blob/master/config-templates/simple-tiproxy.yaml)参照してください。

    TiDB クラスタ トポロジ ファイル内の構成項目の詳細については、 [TiUPを使用した TiDB デプロイメントのトポロジコンフィグレーションファイル](/tiup/tiup-cluster-topology-reference.md)参照してください。

    設定例は次のとおりです。

    ```yaml
    component_versions:
      tiproxy: "v1.3.2"
    server_configs:
      tiproxy:
        ha.virtual-ip: "10.0.1.10/24"
        ha.interface: "eth0"
    tiproxy_servers:
      - host: 10.0.1.11
        port: 6000
        status_port: 3080
      - host: 10.0.1.12
        port: 6000
        status_port: 3080
    ```

3.  クラスターを起動します。

    TiUPを使用してクラスターを起動するには、 [TiUPドキュメント](/tiup/tiup-documentation-guide.md)参照してください。

4.  TiProxy に接続します。

    クラスタがデプロイされると、TiDBサーバーポートとTiProxyポートが同時に公開されます。クライアントはTiDBサーバーに直接接続するのではなく、TiProxyポートに接続する必要があります。

### 既存のクラスターで TiProxy を有効にする {#enable-tiproxy-for-an-existing-cluster}

TiProxy がデプロイされていないクラスターの場合は、TiProxy インスタンスをスケールアウトすることで TiProxy を有効にすることができます。

1.  TiProxy インスタンスを構成します。

    `tiproxy.toml`ような別のトポロジ ファイルで TiProxy を構成します。

    ```yaml
    component_versions:
      tiproxy: "v1.3.2"
    server_configs:
      tiproxy:
        ha.virtual-ip: "10.0.1.10/24"
        ha.interface: "eth0"
    tiproxy_servers:
      - host: 10.0.1.11
        deploy_dir: "/tiproxy-deploy"
        port: 6000
        status_port: 3080
      - host: 10.0.1.12
        deploy_dir: "/tiproxy-deploy"
        port: 6000
        status_port: 3080
    ```

2.  TiProxy をスケールアウトします。

    [`tiup cluster scale-out`](/tiup/tiup-component-cluster-scale-out.md)コマンドを使用して TiProxy インスタンスをスケールアウトします。例:

    ```shell
    tiup cluster scale-out <cluster-name> tiproxy.toml
    ```

    TiProxyをスケールアウトすると、 TiUPはTiDB用の自己署名証明書[`security.session-token-signing-cert`](/tidb-configuration-file.md#session-token-signing-cert-new-in-v640)と[`security.session-token-signing-key`](/tidb-configuration-file.md#session-token-signing-key-new-in-v640)自動的に構成します。この証明書は接続の移行に使用されます。

3.  TiDB 構成を変更します。

    TiProxyを使用する場合、TiDBに[`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-new-in-v50)設定する必要があります。TiDBサーバーがオフラインになった際にクライアント接続が中断されるのを防ぐため、この値はアプリケーションの最長トランザクションの所要時間より少なくとも10秒長く設定する必要があります。トランザクションの所要時間は[TiDB モニタリング ダッシュボードのトランザクションメトリック](/grafana-tidb-dashboard.md#transaction)で確認できます。詳細については、 [制限事項](#limitations)参照してください。

    設定例は次のとおりです。

    ```yaml
    server_configs:
      tidb:
        graceful-wait-before-shutdown: 30
    ```

4.  TiDB 構成を再読み込みします。

    TiDBは自己署名証明書と`graceful-wait-before-shutdown`設定されているため、設定を有効にするには[`tiup cluster reload`](/tiup/tiup-component-cluster-reload.md)コマンドを使用して設定を再読み込みする必要があります。設定を再読み込みすると、TiDBはローリング再起動を実行し、クライアント接続が切断されることに注意してください。

    ```shell
    tiup cluster reload <cluster-name> -R tidb
    ```

5.  TiProxy に接続します。

    TiProxy を有効にすると、クライアントは TiDBサーバーポートではなく TiProxy ポートに接続する必要があります。

### TiProxy構成の変更 {#modify-tiproxy-configuration}

TiProxy がクライアント接続を維持するには、必要な場合を除き TiProxy を再起動しないでください。そのため、TiProxy の設定項目のほとんどはオンラインで変更できます。オンライン変更をサポートする設定項目の一覧については、 [TiProxyの設定](/tiproxy/tiproxy-configuration.md)参照してください。

TiUPを使用して TiProxy の設定を変更する場合、変更する構成項目がオンライン変更をサポートしている場合は、 [`--skip-restart`](/tiup/tiup-component-cluster-reload.md#--skip-restart)オプションを使用して TiProxy の再起動を回避できます。

### TiProxy をアップグレードする {#upgrade-tiproxy}

TiProxy をデプロイする場合は、TiDB クラスターをアップグレードしても TiProxy がアップグレードされないように、TiProxy のバージョンを指定することをお勧めします。

TiProxy をアップグレードする必要がある場合は、アップグレード コマンドに[`--tiproxy-version`](/tiup/tiup-component-cluster-upgrade.md#--tiproxy-version)追加して、TiProxy のバージョンを指定します。

```shell
tiup cluster upgrade <cluster-name> <version> --tiproxy-version <tiproxy-version>
```

> **注記：**
>
> このコマンドは、クラスターのバージョンが変更されない場合でも、TiDB クラスターをアップグレードして再起動します。

### TiDBクラスタを再起動します {#restart-the-tidb-cluster}

[`tiup cluster restart`](/tiup/tiup-component-cluster-restart.md)使用して TiDB クラスタを再起動すると、TiDB サーバはローリング再起動されず、クライアント接続が切断されます。したがって、このコマンドの使用は避けてください。

代わりに、 [`tiup cluster upgrade`](/tiup/tiup-component-cluster-upgrade.md)使用してクラスターをアップグレードするか、 [`tiup cluster reload`](/tiup/tiup-component-cluster-reload.md)使用して構成を再ロードすると、 TiDB サーバーがローリング再起動されるため、クライアント接続は影響を受けません。

## 他のコンポーネントとの互換性 {#compatibility-with-other-components}

-   TiProxy は TiDB v6.5.0 以降のバージョンのみをサポートします。
-   TiProxyのTLS接続にはTiDBと互換性のない機能があります。詳細については[Security](#security)参照してください。
-   TiDB ダッシュボードと Grafana は、v7.6.0 から TiProxy をサポートしています。
-   TiUP はv1.14.1 から TiProxy をサポートし、 TiDB Operator はv1.5.1 から TiProxy をサポートします。
-   TiProxy のステータス ポートによって提供されるインターフェイスは TiDBサーバーのインターフェイスとは異なるため、 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)使用してデータをインポートする場合、ターゲット データベースは TiProxy のアドレスではなく、TiDBサーバーのアドレスにする必要があります。

## Security {#security}

TiProxyはTLS接続を提供します。クライアントとTiProxy間のTLS接続は、以下のルールに従って有効化されます。

-   TiProxy の[`security.server-tls`](/tiproxy/tiproxy-configuration.md#server-tls)構成が TLS 接続を使用しないように設定されている場合、クライアントが TLS 接続を有効にしているかどうかに関係なく、クライアントと TiProxy 間の TLS 接続は有効になりません。
-   TiProxy の[`security.server-tls`](/tiproxy/tiproxy-configuration.md#server-tls)の構成が TLS 接続を使用するように設定されている場合、クライアントと TiProxy 間の TLS 接続は、クライアントが TLS 接続を有効にした場合にのみ有効になります。

TiProxy と TiDBサーバー間の TLS 接続は、次のルールに従って有効化されます。

-   TiProxyの[`security.require-backend-tls`](/tiproxy/tiproxy-configuration.md#require-backend-tls) `true`に設定されている場合、クライアントがTLS接続を有効にしているかどうかに関係なく、TiProxyとTiDBサーバーは常にTLS接続を有効にします。TiProxyの[`security.sql-tls`](/tiproxy/tiproxy-configuration.md#sql-tls) TLSを使用しないように設定されているか、TiDBサーバーがTLS証明書を設定していない場合、クライアントはエラーを報告します。
-   TiProxy の[`security.require-backend-tls`](/tiproxy/tiproxy-configuration.md#require-backend-tls) `false`に設定され、TiProxy の[`security.sql-tls`](/tiproxy/tiproxy-configuration.md#sql-tls) TLS で構成され、TiDBサーバーがTLS 証明書で構成されている場合、TiProxy と TiDBサーバーは、クライアントが TLS 接続を有効にした場合にのみ TLS 接続を有効にします。
-   TiProxy の[`security.require-backend-tls`](/tiproxy/tiproxy-configuration.md#require-backend-tls) `false`に設定されている場合、TiProxy の[`security.sql-tls`](/tiproxy/tiproxy-configuration.md#sql-tls) TLS を使用しないように設定されているか、TiDBサーバーがTLS 証明書を構成していない場合、TiProxy と TiDBサーバーはTLS 接続を有効にしません。

TiProxy には、TiDB と互換性のない次の動作があります。

-   `STATUS`と`SHOW STATUS`ステートメントは異なるTLS情報を返す可能性があります。5 `STATUS`ステートメントはクライアントとTiProxy間のTLS情報を返し、 `SHOW STATUS`ステートメントはTiProxyとTiDBサーバー間のTLS情報を返します。
-   TiProxy は[証明書ベースの認証](/certificate-authentication.md)サポートしていません。そうでない場合、クライアントと TiProxy 間の TLS 証明書が TiProxy と TiDBサーバー間の TLS 証明書と異なるため、クライアントがログインに失敗する可能性があります。TiDBサーバーはTiProxy 上の TLS 証明書に基づいて TLS 証明書を検証します。

## 制限事項 {#limitations}

次のシナリオでは、TiProxy はクライアント接続を維持できません。

-   TiDB が予期せずオフラインになりました。TiProxy は、TiDBサーバーがオフラインの場合、または計画どおりに再起動された場合にのみクライアント接続を維持し、TiDBサーバーのフェイルオーバーをサポートしません。
-   TiProxy はスケールイン、アップグレード、または再起動を実行します。TiProxy がオフラインになると、クライアント接続は切断されます。
-   TiDBは接続を積極的に切断します。例えば、セッションが`wait_timeout`以上リクエストを送信しない場合、TiDBは接続を積極的に切断し、TiProxyもクライアント接続を切断します。

TiProxy は次のシナリオでは接続を移行できないため、クライアント接続が中断されたり、負荷分散が失敗したりします。

-   長時間実行される単一のステートメントまたは単一のトランザクション: 実行時間が、TiDBサーバーで構成された値[`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-new-in-v50)から 10 秒を引いた値を超えています。
-   カーソルを使用していて、時間内に完了しない: セッションはカーソルを使用してデータを読み取りますが、TiDBサーバーで構成された値[`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-new-in-v50)から 10 秒を引いた時間が経過してもデータの読み取りが完了しないか、カーソルが閉じられません。
-   セッションは[ローカル一時テーブル](/temporary-tables.md#local-temporary-tables)を作成します。
-   セッションは[ユーザーレベルロック](/functions-and-operators/locking-functions.md)を開催します。
-   セッションは[テーブルロック](/sql-statements/sql-statement-lock-tables-and-unlock-tables.md)を開催します。
-   セッションで[プリペアドステートメント](/develop/dev-guide-prepared-statement.md)が作成されましたが、プリペアドステートメントは無効です。例えば、プリペアドステートメントの作成後に、そのプリペアドステートメントに関連するテーブルが削除された場合などです。
-   セッションはセッションレベル[実行プランのバインディング](/sql-plan-management.md#sql-binding)を作成しましたが、バインディングが無効です。例えば、バインディングの作成後に、バインディングに関連するテーブルが削除されています。
-   セッションが作成された後、セッションで使用されたユーザーが削除されるか、ユーザー名が変更されます。

## サポートされているコネクタ {#supported-connectors}

TiProxy では、クライアントが使用するコネクタが[認証プラグイン](https://dev.mysql.com/doc/refman/8.0/en/pluggable-authentication.html)サポートしている必要があります。そうでない場合、接続に失敗する可能性があります。

次の表に、サポートされているコネクタの一部を示します。

| 言語         | コネクタ               | サポートされる最小バージョン |
| ---------- | ------------------ | -------------- |
| Java       | MySQL コネクタ/J       | 5.1.19         |
| C          | libmysqlクライアント     | 5.5.7          |
| 行く         | Go SQLDriver       | 1.4.0          |
| JavaScript | MySQL コネクタ/Node.js | 1.0.2          |
| JavaScript | mysqljs/mysql      | 2.15.0         |
| JavaScript | ノード-mysql2         | 1.0.0-rc-6     |
| PHP        | mysqlnd            | 5.4            |
| パイソン       | MySQL コネクタ/Python  | 1.0.7          |
| パイソン       | パイMySQL            | 0.7            |

一部のコネクタはデータベース接続に共通ライブラリを呼び出しますが、これらのコネクタは表に記載されていません。対応するライブラリの必要なバージョンについては、上記の表を参照してください。例えば、MySQL/Rubyはデータベース接続にlibmysqlclientを使用するため、MySQL/Rubyが使用するlibmysqlclientのバージョンは5.5.7以降である必要があります。

## TiProxyリソース {#tiproxy-resources}

-   [TiProxy リリースノート](https://github.com/pingcap/tiproxy/releases)
-   [TiProxy の問題](https://github.com/pingcap/tiproxy/issues) : TiProxy GitHub の問題を一覧表示します
