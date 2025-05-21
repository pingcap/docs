---
title: TiProxy Overview
summary: TiProxy の主な機能、インストール、および使用方法を学びます。
---

# TiProxy の概要 {#tiproxy-overview}

TiProxyはPingCAPの公式プロキシコンポーネントです。クライアントとTiDBサーバーの間に配置され、負荷分散、接続の持続性、サービス検出、その他のTiDB機能を提供します。

TiProxy はオプションのコンポーネントです。サードパーティのプロキシコンポーネントを使用することも、プロキシを使用せずに TiDBサーバーに直接接続することもできます。

次の図は、TiProxy のアーキテクチャを示しています。

<img src="https://docs-download.pingcap.com/media/images/docs/tiproxy/tiproxy-architecture.png" alt="TiProxyアーキテクチャ" width="500" />

## 主な特徴 {#main-features}

TiProxy は、接続の移行、サービスの検出、および迅速な展開を提供します。

### 接続の移行 {#connection-migration}

TiProxy は、クライアント接続を切断することなく、ある TiDBサーバーから別の TiDB サーバーに接続を移行できます。

下図に示すように、クライアントはTiProxyを介してTiDB 1に接続します。接続の移行後、クライアントは実際にはTiDB 2に接続します。TiDB 1がオフラインになりそうになった場合、またはTiDB 1とTiDB 2の接続比率が設定されたしきい値を超えた場合、接続の移行がトリガーされます。クライアントは接続の移行を認識しません。

<img src="https://docs-download.pingcap.com/media/images/docs/tiproxy/tiproxy-session-migration.png" alt="TiProxy接続の移行" width="400" />

接続の移行は通常、次のシナリオで発生します。

-   TiDBサーバーがスケールイン、ローリング アップグレード、またはローリング リスタートを実行する場合、TiProxy はオフラインになる予定の TiDBサーバーから他の TiDB サーバーへの接続を移行して、クライアント接続を維持できます。
-   TiDBサーバーがスケールアウトを実行すると、TiProxy は既存の接続を新しい TiDBサーバーに移行し、クライアント接続プールをリセットせずにリアルタイムの負荷分散を実現できます。

### サービス検出 {#service-discovery}

TiDBサーバーがスケールインまたはスケールアウトを実行する際、共通のロードバランサーを使用している場合は、TiDBサーバーリストを手動で更新する必要があります。しかし、TiProxyは手動操作なしでTiDBサーバーリストを自動的に検出します。

### 迅速な展開 {#quick-deployment}

TiProxy は[TiUP](https://github.com/pingcap/tiup) 、 [TiDB Operator](https://github.com/pingcap/tidb-operator) 、 [TiDBダッシュボード](/dashboard/dashboard-intro.md) 、 [グラファナ](/tiproxy/tiproxy-grafana.md)に統合されており、導入、運用、管理のコストが削減されます。

## ユーザーシナリオ {#user-scenarios}

TiProxy は次のシナリオに適しています。

-   接続の永続性：TiDBサーバーがスケールイン、ローリングアップグレード、またはローリングリスタートを実行すると、クライアント接続が切断され、エラーが発生します。クライアントに冪等なエラーリトライメカニズムがない場合、手動でエラーを確認して修正する必要があり、人件費が大幅に増加します。TiProxyはクライアント接続を維持できるため、クライアントはエラーを報告しません。
-   頻繁なスケールインとスケールアウト：アプリケーションのワークロードは定期的に変化する可能性があります。コスト削減のため、TiDBをクラウドに導入し、ワークロードに応じてTiDBサーバーを自動的にスケールインおよびスケールアウトすることができます。ただし、スケールインはクライアントの接続を切断する可能性があり、スケールアウトは負荷の不均衡を引き起こす可能性があります。TiProxyはクライアント接続を維持し、負荷分散を実現します。

TiProxy は次のシナリオには適していません。

-   パフォーマンスの影響を受けやすい：TiProxyのパフォーマンスはHAProxyや他のロードバランサに比べて低いため、TiProxyを使用する場合は、同等のパフォーマンスレベルを維持するためにより多くのCPUリソースを予約する必要があります。詳細については、 [TiProxy パフォーマンステストレポート](/tiproxy/tiproxy-performance-test.md)を参照してください。
-   コストに敏感：TiDB クラスターがハードウェアロードバランサー、仮想 IP、または Kubernetes が提供するロードバランサーを使用している場合、TiProxy を追加するとコストが増加します。さらに、クラウド上の複数のアベイラビリティゾーンに TiDB クラスターを展開する場合、TiProxy を追加するとアベイラビリティゾーン間のトラフィックコストも増加します。
-   TiDBサーバーのフェイルオーバー：TiProxyは、TiDBサーバーがオフラインの場合、または計画通りに再起動された場合にのみクライアント接続を維持できます。TiDBサーバーが予期せずオフラインになった場合、接続は依然として切断されます。

TiProxy が適しているシナリオでは TiProxy を使用し、アプリケーションがパフォーマンスに敏感な場合は HAProxy またはその他のプロキシを使用することをお勧めします。

## インストールと使用方法 {#installation-and-usage}

このセクションでは、 TiUPを使用して TiProxy をデプロイおよび変更する方法について説明します。Kubernetes でTiDB Operatorを使用して TiProxy をデプロイする方法については、 [TiDB Operatorのドキュメント](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tiproxy)参照してください。

### TiProxyをデプロイ {#deploy-tiproxy}

1.  TiUP v1.15.0 より前のバージョンでは、自己署名証明書を手動で生成する必要があります。

    TiDBインスタンス用の自己署名証明書を生成し、すべてのTiDBインスタンスに同じ証明書を配置して、すべてのTiDBインスタンスが同じ証明書を持つようにします。詳細な手順については、 [自己署名証明書を生成する](/generate-self-signed-certificates.md)参照してください。

2.  TiDB インスタンスを構成します。

    TiProxy を使用する場合は、TiDB インスタンスに対して次の項目も設定する必要があります。

    -   TiUP v1.15.0より前のバージョンでは、TiDBインスタンスの[`security.session-token-signing-cert`](/tidb-configuration-file.md#session-token-signing-cert-new-in-v640)と[`security.session-token-signing-key`](/tidb-configuration-file.md#session-token-signing-key-new-in-v640)証明書のパスに設定してください。そうしないと、接続を移行できません。
    -   TiDBインスタンスの[`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-new-in-v50) 、アプリケーションの最長トランザクション継続時間よりも大きな値に設定してください。そうしないと、TiDBサーバーがオフラインになったときにクライアントが切断される可能性があります。トランザクション継続時間は[TiDB 監視ダッシュボードのトランザクションメトリック](/grafana-tidb-dashboard.md#transaction)で確認できます。詳細は[TiProxyの使用制限](#limitations)ご覧ください。

    設定例は次のとおりです。

    ```yaml
    server_configs:
      tidb:
        security.session-token-signing-cert: "/var/sess/cert.pem"
        security.session-token-signing-key: "/var/sess/key.pem"
        security.ssl-ca: "/var/ssl/ca.pem"
        security.ssl-cert: "/var/ssl/cert.pem"
        security.ssl-key: "/var/ssl/key.pem"
        graceful-wait-before-shutdown: 15
    ```

3.  TiProxy インスタンスを構成します。

    TiProxy の高可用性を確保するには、少なくとも 2 つの TiProxy インスタンスを導入することをお勧めします。ハードウェアロードバランサーを使用して各 TiProxy インスタンスにトラフィックを分散するか、仮想 IP を設定して利用可能な TiProxy インスタンスにトラフィックをルーティングすることもできます。

    TiProxy インスタンスのモデルと数を選択するときは、次の要素を考慮してください。

    -   ワークロードの種類と最大 QPS については、 [TiProxy パフォーマンステストレポート](/tiproxy/tiproxy-performance-test.md)参照してください。
    -   TiProxyインスタンス数はTiDBサーバ数よりも少ないため、TiProxyのネットワーク帯域がボトルネックになりやすいです。そのため、ネットワーク帯域も考慮する必要があります。例えばAWSでは、EC2の同系列のベースラインネットワーク帯域はCPUコア数に比例しません。詳細は[ネットワークパフォーマンス](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/compute-optimized-instances.html#compute-network-performance)参照してください。このような場合、ネットワーク帯域がボトルネックになる場合は、TiProxyインスタンスをより多くの小さなインスタンスに分割することでQPSを向上させることができます。

    TiDBクラスタを[`tiup cluster upgrade`](/tiup/tiup-component-cluster-upgrade.md)にアップグレードする際にTiProxyがアップグレードされないように、トポロジ構成でTiProxyのバージョン番号を指定することをお勧めします。そうしないと、TiProxyのアップグレード中にクライアント接続が切断される可能性があります。

    TiProxy 構成項目を構成するには、 [TiProxy の設定](/tiproxy/tiproxy-configuration.md)参照してください。

    設定例は次のとおりです。

    ```yaml
    component_versions:
      tiproxy: "v1.0.0"
    server_configs:
      tiproxy:
        security.server-tls.ca: "/var/ssl/ca.pem"
        security.server-tls.cert: "/var/ssl/cert.pem"
        security.server-tls.key: "/var/ssl/key.pem"
    ```

4.  クラスターを起動します。

    TiUPを使用してクラスターを起動するには、 [TiUPドキュメント](/tiup/tiup-documentation-guide.md)参照してください。

5.  TiProxy に接続します。

    クラスタがデプロイされると、クラスタはTiDBサーバーとTiProxyのポートを同時に公開します。クライアントはTiDBサーバーのポートではなく、TiProxyのポートに接続する必要があります。

### TiProxy構成の変更 {#modify-tiproxy-configuration}

TiProxy がクライアント接続を維持するには、必要な場合を除き TiProxy を再起動しないでください。そのため、TiProxy の設定項目のほとんどはオンラインで変更できます。オンライン変更をサポートする設定項目のリストについては、 [TiProxy の設定](/tiproxy/tiproxy-configuration.md)参照してください。

TiUPを使用して TiProxy の設定を変更する場合、変更する構成項目がオンライン変更をサポートしている場合は、 [`--skip-restart`](/tiup/tiup-component-cluster-reload.md#--skip-restart)オプションを使用して TiProxy の再起動を回避できます。

### TiProxy をアップグレードする {#upgrade-tiproxy}

TiProxy をデプロイする場合は、TiDB クラスターをアップグレードしても TiProxy がアップグレードされないように、TiProxy のバージョンを指定することをお勧めします。

TiProxy をアップグレードする必要がある場合は、アップグレード コマンドに[`--tiproxy-version`](/tiup/tiup-component-cluster-upgrade.md#--tiproxy-version)追加して、TiProxy のバージョンを指定します。

```shell
tiup cluster upgrade <cluster-name> <version> --tiproxy-version <tiproxy-version>
```

### TiDBクラスタを再起動します {#restart-the-tidb-cluster}

[`tiup cluster restart`](/tiup/tiup-component-cluster-restart.md)使用して TiDB クラスタを再起動すると、TiDB サーバはローリング再起動されず、クライアント接続が切断されます。したがって、このコマンドの使用は避けてください。

代わりに、 [`tiup cluster upgrade`](/tiup/tiup-component-cluster-upgrade.md)使用してクラスターをアップグレードするか、 [`tiup cluster reload`](/tiup/tiup-component-cluster-reload.md)使用して構成を再ロードすると、 TiDB サーバーがローリング再起動されるため、クライアント接続は影響を受けません。

## 他のコンポーネントとの互換性 {#compatibility-with-other-components}

-   TiProxy は TiDB v6.5.0 以降のバージョンのみをサポートします。
-   TiProxyのTLS接続にはTiDBと互換性のない機能があります。詳細については[Security](#security)参照してください。
-   TiDB ダッシュボードと Grafana は、v7.6.0 から TiProxy をサポートしています。
-   TiUP はv1.14.1 から TiProxy をサポートし、 TiDB Operator はv1.5.1 から TiProxy をサポートします。
-   TiProxy のステータス ポートによって提供されるインターフェイスは TiDBサーバーのインターフェイスと異なるため、 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)使用してデータをインポートする場合、ターゲット データベースは TiProxy のアドレスではなく、TiDBサーバーのアドレスにする必要があります。

## Security {#security}

TiProxyはTLS接続を提供します。クライアントとTiProxy間のTLS接続は、以下のルールに従って有効化されます。

-   TiProxy の[`security.server-tls`](/tiproxy/tiproxy-configuration.md#server-tls)構成が TLS 接続を使用しないように設定されている場合、クライアントが TLS 接続を有効にしているかどうかに関係なく、クライアントと TiProxy 間の TLS 接続は有効になりません。
-   TiProxy の[`security.server-tls`](/tiproxy/tiproxy-configuration.md#server-tls)の構成が TLS 接続を使用するように設定されている場合、クライアントと TiProxy 間の TLS 接続は、クライアントが TLS 接続を有効にした場合にのみ有効になります。

TiProxy と TiDBサーバー間の TLS 接続は、次のルールに従って有効化されます。

-   TiProxyの[`security.require-backend-tls`](/tiproxy/tiproxy-configuration.md#require-backend-tls) `true`に設定されている場合、クライアントがTLS接続を有効にしているかどうかに関係なく、TiProxyとTiDBサーバーは常にTLS接続を有効にします。TiProxyの[`security.sql-tls`](/tiproxy/tiproxy-configuration.md#sql-tls) TLSを使用しないように設定されているか、TiDBサーバーがTLS証明書を設定していない場合、クライアントはエラーを報告します。
-   TiProxy の[`security.require-backend-tls`](/tiproxy/tiproxy-configuration.md#require-backend-tls) `false`に設定され、TiProxy の[`security.sql-tls`](/tiproxy/tiproxy-configuration.md#sql-tls) TLS で構成され、TiDBサーバーがTLS 証明書で構成されている場合、TiProxy と TiDBサーバーは、クライアントが TLS 接続を有効にした場合にのみ TLS 接続を有効にします。
-   TiProxy の[`security.require-backend-tls`](/tiproxy/tiproxy-configuration.md#require-backend-tls) `false`に設定されている場合、TiProxy の[`security.sql-tls`](/tiproxy/tiproxy-configuration.md#sql-tls) TLS を使用しないように設定されているか、TiDBサーバーがTLS 証明書を構成していない場合、TiProxy と TiDBサーバーはTLS 接続を有効にしません。

TiProxy には、TiDB と互換性のない次の動作があります。

-   `STATUS`と`SHOW STATUS`ステートメントは異なる TLS 情報を返す可能性があります。5 `STATUS`ステートメントはクライアントと TiProxy 間の TLS 情報を返し、 `SHOW STATUS`ステートメントは TiProxy と TiDBサーバー間の TLS 情報を返します。
-   TiProxy は[証明書ベースの認証](/certificate-authentication.md)サポートしていません。そうでない場合、クライアントと TiProxy 間の TLS 証明書が TiProxy と TiDBサーバー間の TLS 証明書と異なるため、クライアントがログインに失敗する可能性があります。TiDBサーバーはTiProxy 上の TLS 証明書に基づいて TLS 証明書を検証します。

## 制限事項 {#limitations}

次のシナリオでは、TiProxy はクライアント接続を維持できません。

-   TiDB が予期せずオフラインになりました。TiProxy は、TiDBサーバーがオフラインの場合、または計画どおりに再起動された場合にのみクライアント接続を維持し、TiDBサーバーのフェイルオーバーをサポートしません。
-   TiProxy はスケールイン、アップグレード、または再起動を実行します。TiProxy がオフラインになると、クライアント接続は切断されます。
-   TiDBは接続を積極的に切断します。例えば、セッションが`wait_timeout`以上リクエストを送信しなかった場合、TiDBは接続を積極的に切断し、TiProxyもクライアント接続を切断します。

TiProxy は次のシナリオでは接続を移行できないため、クライアント接続を維持したり負荷分散を実現したりすることができません。

-   単一のステートメントまたは単一のトランザクションの継続時間が、TiDBサーバーで構成された[`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-new-in-v50)超えています。
-   セッションはカーソルを使用してデータを読み取りますが、カーソルが閉じられていないか、TiDBサーバーで構成された[`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-new-in-v50)以内にデータが読み取られません。
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
