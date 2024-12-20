---
title: TiProxy Overview
summary: TiProxy の主な機能、インストール、および使用方法について学習します。
---

# TiProxy の概要 {#tiproxy-overview}

TiProxy は、PingCAP の公式プロキシコンポーネントです。クライアントと TiDBサーバーの間に配置され、負荷分散、接続の永続性、サービス検出、および TiDB のその他の機能を提供します。

TiProxy はオプションのコンポーネントです。サードパーティのプロキシコンポーネントを使用することも、プロキシを使用せずに TiDBサーバーに直接接続することもできます。

次の図は、TiProxy のアーキテクチャを示しています。

<img src="https://download.pingcap.com/images/docs/tiproxy/tiproxy-architecture.png" alt="TiProxy アーキテクチャ" width="500" />

## 主な特徴 {#main-features}

TiProxy は、接続の移行、フェイルオーバー、サービスの検出、および迅速な展開を提供します。

### 接続の移行 {#connection-migration}

TiProxy は、クライアント接続を切断することなく、ある TiDBサーバーから別の TiDB サーバーに接続を移行できます。

次の図に示すように、クライアントは最初、TiProxy を介して TiDB 1 に接続します。接続の移行後、クライアントは実際には TiDB 2 に接続します。TiDB 1 がオフラインになる直前、または TiDB 1 の接続と TiDB 2 の接続の比率が設定されたしきい値を超えると、接続の移行がトリガーされます。クライアントは接続の移行を認識しません。

<img src="https://download.pingcap.com/images/docs/tiproxy/tiproxy-session-migration.png" alt="TiProxy接続の移行" width="400" />

接続の移行は通常、次のシナリオで発生します。

-   TiDBサーバーがスケールイン、ローリング アップグレード、またはローリング再起動を実行すると、TiProxy はオフラインになる予定の TiDBサーバーから他の TiDB サーバーへの接続を移行して、クライアント接続を維持できます。
-   TiDBサーバーがスケールアウトを実行すると、TiProxy は既存の接続を新しい TiDBサーバーに移行して、クライアント接続プールをリセットせずにリアルタイムの負荷分散を実現できます。

### フェイルオーバー {#failover}

TiDBサーバーがメモリ不足 (OOM) になる危険がある場合、または PD または TiKV に接続できない場合、TiProxy は自動的に問題を検出し、接続を別の TiDBサーバーに移行して、継続的なクライアント接続を確保します。

### サービス検出 {#service-discovery}

TiDBサーバーがスケールインまたはスケールアウトを実行する場合、共通のロード バランサーを使用している場合は、TiDBサーバーリストを手動で更新する必要があります。ただし、TiProxy は手動介入なしで TiDBサーバーリストを自動的に検出できます。

### 迅速な展開 {#quick-deployment}

TiProxy は[TiUP](https://github.com/pingcap/tiup) 、 [TiDB Operator](https://github.com/pingcap/tidb-operator) 、 [TiDBダッシュボード](/dashboard/dashboard-intro.md) 、および[グラファナ](/tiproxy/tiproxy-grafana.md)に統合されており、組み込みの仮想 IP 管理をサポートしているため、導入、運用、管理のコストが削減されます。

## ユーザーシナリオ {#user-scenarios}

TiProxy は次のシナリオに適しています。

-   接続の永続性: TiDBサーバーがスケールイン、ローリング アップグレード、またはローリング リスタートを実行すると、クライアント接続が切断され、エラーが発生します。クライアントにべき等エラー再試行メカニズムがない場合は、手動でエラーを確認して修正する必要があり、人件費が大幅に増加します。TiProxy はクライアント接続を維持できるため、クライアントはエラーを報告しません。
-   頻繁なスケールインとスケールアウト: アプリケーションのワークロードは定期的に変化する可能性があります。コストを節約するために、クラウドに TiDB をデプロイし、ワークロードに応じて TiDB サーバーを自動的にスケールインおよびスケールアウトすることができます。ただし、スケールインによってクライアントが切断される可能性があり、スケールアウトによって負荷が不均衡になる可能性があります。TiProxy はクライアント接続を維持し、負荷分散を実現できます。
-   CPU 負荷の不均衡: バックグラウンド タスクが大量の CPU リソースを消費したり、接続間のワークロードが大幅に変化して CPU 負荷が不均衡になったりした場合、TiProxy は CPU 使用率に基づいて接続を移行し、負荷分散を実現します。詳細については、 [CPUベースの負荷分散](/tiproxy/tiproxy-load-balance.md#cpu-based-load-balancing)参照してください。
-   TiDBサーバーのOOM: クエリの暴走により TiDBサーバーのメモリが不足すると、TiProxy は OOM のリスクを事前に検出し、他の正常な接続を別の TiDBサーバーに移行して、クライアントの接続を継続できるようにします。詳細については、 [メモリベースの負荷分散](/tiproxy/tiproxy-load-balance.md#memory-based-load-balancing)参照してください。

TiProxy は次のシナリオには適していません。

-   パフォーマンスに敏感: TiProxy のパフォーマンスは HAProxy や他のロードバランサーに比べて低いため、TiProxy を使用すると QPS が低下します。詳細については[TiProxy パフォーマンス テスト レポート](/tiproxy/tiproxy-performance-test.md)を参照してください。
-   コストに敏感: TiDB クラスターがハードウェア ロード バランサー、仮想 IP、または Kubernetes が提供するロード バランサーを使用している場合、TiProxy を追加するとコストが増加します。さらに、クラウド上のアベイラビリティ ゾーン全体に TiDB クラスターを展開する場合、TiProxy を追加するとアベイラビリティ ゾーン全体のトラフィック コストも増加します。
-   予期しない TiDBサーバーのダウンタイムに対するフェイルオーバー: TiProxy は、TiDBサーバーがオフラインの場合、または計画どおりに再起動された場合にのみクライアント接続を維持できます。TiDBサーバーが予期せずオフラインになった場合、接続は切断されたままになります。

TiProxy が適しているシナリオでは TiProxy を使用し、アプリケーションがパフォーマンスに敏感な場合は HAProxy またはその他のプロキシを使用することをお勧めします。

## インストールと使用方法 {#installation-and-usage}

このセクションでは、 TiUP を使用して TiProxy をデプロイおよび変更する方法について説明します。Kubernetes でTiDB Operator を使用して TiProxy をデプロイする方法については、 [TiDB Operatorのドキュメント](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tiproxy)参照してください。

### TiProxy をデプロイ {#deploy-tiproxy}

1.  TiUP v1.15.0 より前では、自己署名証明書を手動で生成する必要があります。

    TiDB インスタンスの自己署名証明書を生成し、その証明書をすべての TiDB インスタンスに配置して、すべての TiDB インスタンスが同じ証明書を持つようにします。詳細な手順については、 [自己署名証明書を生成する](/generate-self-signed-certificates.md)参照してください。

2.  TiDB インスタンスを構成します。

    TiProxy を使用する場合は、TiDB インスタンスに対して次の項目も構成する必要があります。

    -   TiUP v1.15.0 より前では、TiDB インスタンスの[`security.session-token-signing-cert`](/tidb-configuration-file.md#session-token-signing-cert-new-in-v640)と[`security.session-token-signing-key`](/tidb-configuration-file.md#session-token-signing-key-new-in-v640)を証明書のパスに設定してください。そうしないと、接続を移行できません。
    -   TiDB インスタンスの[`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-new-in-v50)を、アプリケーションの最長トランザクション期間よりも大きい値に設定します。そうしないと、TiDBサーバーがオフラインのときにクライアントが切断される可能性があります。トランザクション期間は[TiDB モニタリング ダッシュボードのトランザクションメトリック](/grafana-tidb-dashboard.md#transaction)で確認できます。詳細については、 [TiProxyの使用制限](#limitations)参照してください。

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

    TiProxy の高可用性を確保するには、少なくとも 2 つの TiProxy インスタンスを展開し、 [`ha.virtual-ip`](/tiproxy/tiproxy-configuration.md#virtual-ip)と[`ha.interface`](/tiproxy/tiproxy-configuration.md#interface)設定して仮想 IP を構成し、使用可能な TiProxy インスタンスにトラフィックをルーティングすることをお勧めします。

    TiProxy インスタンスのモデルと数を選択するときは、次の要素を考慮してください。

    -   ワークロードの種類と最大 QPS については、 [TiProxy パフォーマンス テスト レポート](/tiproxy/tiproxy-performance-test.md)参照してください。
    -   TiProxy インスタンスの数は TiDB サーバの数よりも少ないため、TiProxy のネットワーク帯域が TiDB サーバよりもボトルネックになりやすいです。そのため、ネットワーク帯域も考慮する必要があります。例えば、AWS では、EC2 同シリーズのベースラインネットワーク帯域は CPU コア数に比例しません。詳細は[ネットワークパフォーマンス](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/compute-optimized-instances.html#compute-network-performance)参照してください。このような場合、ネットワーク帯域がボトルネックになるときは、TiProxy インスタンスをより多くの小さなインスタンスに分割すると QPS が向上することがあります。

    TiDB クラスタを[`tiup cluster upgrade`](/tiup/tiup-component-cluster-upgrade.md)にアップグレードするときに TiProxy がアップグレードされないように、トポロジ構成で TiProxy のバージョン番号を指定することをお勧めします。そうしないと、TiProxy のアップグレード中にクライアント接続が切断される可能性があります。

    TiProxy 構成項目を構成するには、 [TiProxy の設定](/tiproxy/tiproxy-configuration.md)参照してください。

    設定例は次のとおりです。

    ```yaml
    component_versions:
      tiproxy: "v1.2.0"
    server_configs:
      tiproxy:
        security.server-tls.ca: "/var/ssl/ca.pem"
        security.server-tls.cert: "/var/ssl/cert.pem"
        security.server-tls.key: "/var/ssl/key.pem"
        ha.virtual-ip: "10.0.1.10/24"
        ha.interface: "eth0"
    ```

4.  クラスターを起動します。

    TiUP を使用してクラスターを起動するには、 [TiUPドキュメント](/tiup/tiup-documentation-guide.md)参照してください。

5.  TiProxyに接続します。

    クラスターがデプロイされると、クラスターは TiDBサーバーと TiProxy のポートを同時に公開します。クライアントは、TiDBサーバーのポートではなく、TiProxy のポートに接続する必要があります。

### TiProxy 構成の変更 {#modify-tiproxy-configuration}

TiProxy がクライアント接続を維持するには、必要な場合を除いて TiProxy を再起動しないでください。したがって、TiProxy 構成項目のほとんどはオンラインで変更できます。オンライン変更をサポートする構成項目のリストについては、 [TiProxy の設定](/tiproxy/tiproxy-configuration.md)参照してください。

TiUP を使用して TiProxy 設定を変更する場合、変更する構成項目がオンライン変更をサポートしている場合は、 [`--skip-restart`](/tiup/tiup-component-cluster-reload.md#--skip-restart)オプションを使用して TiProxy の再起動を回避できます。

### TiProxy をアップグレードする {#upgrade-tiproxy}

TiProxy をデプロイする場合は、TiDB クラスターをアップグレードしても TiProxy がアップグレードされないように、TiProxy のバージョンを指定することをお勧めします。

TiProxy をアップグレードする必要がある場合は、アップグレード コマンドに[`--tiproxy-version`](/tiup/tiup-component-cluster-upgrade.md#--tiproxy-version)を追加して、TiProxy のバージョンを指定します。

```shell
tiup cluster upgrade <cluster-name> <version> --tiproxy-version <tiproxy-version>
```

### TiDBクラスタを再起動します {#restart-the-tidb-cluster}

[`tiup cluster restart`](/tiup/tiup-component-cluster-restart.md)使用して TiDB クラスターを再起動すると、TiDB サーバーはローリング再起動されず、クライアント接続が切断されます。したがって、このコマンドの使用は避けてください。

代わりに、 [`tiup cluster upgrade`](/tiup/tiup-component-cluster-upgrade.md)使用してクラスターをアップグレードするか、 [`tiup cluster reload`](/tiup/tiup-component-cluster-reload.md)使用して構成を再ロードすると、 TiDB サーバーがローリング再起動されるため、クライアント接続は影響を受けません。

## 他のコンポーネントとの互換性 {#compatibility-with-other-components}

-   TiProxy は TiDB v6.5.0 以降のバージョンのみをサポートします。
-   TiProxy の TLS 接続には TiDB と互換性のない機能があります。詳細については[Security](#security)参照してください。
-   TiDB ダッシュボードと Grafana は、v7.6.0 から TiProxy をサポートしています。
-   TiUP はv1.14.1 から TiProxy をサポートし、 TiDB Operator はv1.5.1 から TiProxy をサポートします。
-   TiProxy のステータス ポートによって提供されるインターフェイスは TiDBサーバーのインターフェイスと異なるため、 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)使用してデータをインポートする場合、ターゲット データベースは TiProxy のアドレスではなく、TiDBサーバーのアドレスにする必要があります。

## Security {#security}

TiProxy は TLS 接続を提供します。クライアントと TiProxy 間の TLS 接続は、次のルールに従って有効化されます。

-   TiProxy の[`security.server-tls`](/tiproxy/tiproxy-configuration.md#server-tls)の構成が TLS 接続を使用しないように設定されている場合、クライアントが TLS 接続を有効にしているかどうかに関係なく、クライアントと TiProxy 間の TLS 接続は有効になりません。
-   TiProxy の[`security.server-tls`](/tiproxy/tiproxy-configuration.md#server-tls)の構成が TLS 接続を使用するように設定されている場合、クライアントと TiProxy 間の TLS 接続は、クライアントが TLS 接続を有効にした場合にのみ有効になります。

TiProxy と TiDBサーバー間の TLS 接続は、次のルールに従って有効化されます。

-   TiProxy の[`security.require-backend-tls`](/tiproxy/tiproxy-configuration.md#require-backend-tls) `true`に設定されている場合、クライアントが TLS 接続を有効にしているかどうかに関係なく、TiProxy と TiDBサーバーは常に TLS 接続を有効にします。TiProxy の[`security.sql-tls`](/tiproxy/tiproxy-configuration.md#sql-tls) TLS を使用しないように設定されているか、TiDBサーバーがTLS 証明書を構成していない場合、クライアントはエラーを報告します。
-   TiProxy の[`security.require-backend-tls`](/tiproxy/tiproxy-configuration.md#require-backend-tls)が`false`に設定され、TiProxy の[`security.sql-tls`](/tiproxy/tiproxy-configuration.md#sql-tls)が TLS で構成され、TiDBサーバーがTLS 証明書で構成されている場合、TiProxy と TiDBサーバーは、クライアントが TLS 接続を有効にした場合にのみ TLS 接続を有効にします。
-   TiProxy の[`security.require-backend-tls`](/tiproxy/tiproxy-configuration.md#require-backend-tls) `false`に設定されている場合、TiProxy の[`security.sql-tls`](/tiproxy/tiproxy-configuration.md#sql-tls) TLS を使用しないように設定されているか、TiDBサーバーがTLS 証明書を構成していない場合、TiProxy と TiDBサーバーはTLS 接続を有効にしません。

TiProxy には、TiDB と互換性のない次の動作があります。

-   `STATUS`と`SHOW STATUS`ステートメントは異なる TLS 情報を返す可能性があります。5 `STATUS`ステートメントはクライアントと TiProxy 間の TLS 情報を返し、 `SHOW STATUS`ステートメントは TiProxy と TiDBサーバー間の TLS 情報を返します。
-   TiProxy は[証明書ベースの認証](/certificate-authentication.md)サポートしていません。そうでない場合、クライアントと TiProxy 間の TLS 証明書が TiProxy と TiDBサーバー間の TLS 証明書と異なり、TiDBサーバーがTiProxy 上の TLS 証明書に基づいて TLS 証明書を検証するため、クライアントがログインに失敗する可能性があります。

## 制限事項 {#limitations}

TiProxy は、次のシナリオではクライアント接続を維持できません。

-   TiDB が予期せずオフラインになりました。TiProxy は、TiDBサーバーがオフラインの場合、または計画どおりに再起動された場合にのみクライアント接続を維持し、TiDBサーバーのフェイルオーバーをサポートしません。
-   TiProxy はスケールイン、アップグレード、または再起動を実行します。TiProxy がオフラインになると、クライアント接続は切断されます。
-   TiDB は接続をアクティブに切断します。たとえば、セッションが`wait_timeout`より長い期間リクエストを送信しない場合、TiDB は接続をアクティブに切断し、TiProxy もクライアント接続を切断します。

TiProxy は次のシナリオでは接続を移行できないため、クライアント接続を維持したり負荷分散を実現したりすることができません。

-   単一のステートメントまたは単一のトランザクションの継続時間が、TiDBサーバーで構成された[`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-new-in-v50)超えています。
-   セッションはカーソルを使用してデータを読み取りますが、カーソルが閉じられていないか、TiDBサーバーで構成された[`graceful-wait-before-shutdown`](/tidb-configuration-file.md#graceful-wait-before-shutdown-new-in-v50)以内にデータが読み取られません。
-   セッションは[ローカル一時テーブル](/temporary-tables.md#local-temporary-tables)作成します。
-   セッションは[ユーザーレベルロック](/functions-and-operators/locking-functions.md)です。
-   セッションは[テーブルロック](/sql-statements/sql-statement-lock-tables-and-unlock-tables.md)です。
-   セッションは[プリペアドステートメント](/develop/dev-guide-prepared-statement.md)を作成し、プリペアドステートメントは無効です。たとえば、準備されたプリペアドステートメントが作成された後に、プリペアドステートメントに関連するテーブルが削除されます。
-   セッションはセッション レベル[実行プランバインディング](/sql-plan-management.md#sql-binding)を作成しますが、バインディングは無効です。たとえば、バインディングの作成後に、バインディングに関連するテーブルが削除されます。
-   セッションが作成された後、セッションで使用されたユーザーが削除されるか、ユーザー名が変更されます。

## サポートされているコネクタ {#supported-connectors}

TiProxy では、クライアントが使用するコネクタが[認証プラグイン](https://dev.mysql.com/doc/refman/8.0/en/pluggable-authentication.html)サポートしている必要があります。そうでない場合、接続が失敗する可能性があります。

次の表に、サポートされているコネクタの一部を示します。

| 言語         | コネクタ               | サポートされる最小バージョン |
| ---------- | ------------------ | -------------- |
| Java       | MySQL コネクタ/J       | 5.1.19         |
| Ｃ          | libmysqlクライアント     | 5.5.7          |
| 行く         | Go SQLDriver       | 1.4.0          |
| JavaScript | MySQL コネクタ/Node.js | 1.0.2          |
| JavaScript | mysqljs/mysql      | 2.15.0         |
| JavaScript | ノード-mysql2         | 1.0.0-rc-6     |
| PHP の      | mysqlnd            | 5.4            |
| パイソン       | MySQL コネクタ/Python  | 1.0.7          |
| パイソン       | pyMySQL の          | 0.7            |

一部のコネクタは共通ライブラリを呼び出してデータベースに接続しますが、これらのコネクタは表に記載されていません。対応するライブラリの必要なバージョンについては、上記の表を参照してください。たとえば、MySQL/Ruby は libmysqlclient を使用してデータベースに接続するため、MySQL/Ruby が使用する libmysqlclient はバージョン 5.5.7 以降である必要があります。

## TiProxy リソース {#tiproxy-resources}

-   [TiProxy リリースノート](https://github.com/pingcap/tiproxy/releases)
-   [TiProxy の問題](https://github.com/pingcap/tiproxy/issues) : TiProxy GitHub の問題を一覧表示します
