---
title: Secure TiDB Dashboard
summary: TiDBダッシュボードでは、ルートユーザーに強力なパスワードを設定すること、最小権限ユーザーを作成すること、信頼できないアクセスをブロックするためのファイアウォールの使用など、強化されたセキュリティ対策が必要です。また、セキュリティをさらに強化するために、リバースプロキシを使用し、TLSを有効にすることも推奨されます。
---

# セキュリティTiDBダッシュボード {#secure-tidb-dashboard}

TiDBダッシュボードにアクセスするにはサインインする必要がありますが、TiDBダッシュボードはデフォルトで信頼できるユーザーエンティティからのアクセスを想定して設計されています。外部ネットワークユーザーや信頼できないユーザーにTiDBダッシュボードへのアクセスを許可する場合は、セキュリティ上の脆弱性を回避するために以下の対策を講じてください。

## TiDBユーザーのセキュリティを強化する {#enhance-security-of-tidb-users}

### TiDB <code>root</code>ユーザーに強力なパスワードを設定する {#set-a-strong-password-for-the-tidb-code-root-code-user}

TiDBダッシュボードのアカウントシステムは、 TiDB SQLユーザーのアカウントシステムと一致しています。デフォルトでは、TiDBの`root`ユーザーにはパスワードが設定されていないため、TiDBダッシュボードへのアクセスにはパスワード認証が不要です。これにより、悪意のある訪問者は、特権SQL文の実行を含む高い権限を取得できます。

TiDB `root`ユーザーには強力なパスワードを設定することをお勧めします。詳細は[TiDB ユーザーアカウント管理](/user-account-management.md)ご覧ください。または、TiDB `root`ユーザーを無効にすることもできます。

### TiDBダッシュボード用の最小権限ユーザーを作成する {#create-a-least-privileged-user-for-tidb-dashboard}

TiDBダッシュボードのアカウントシステムは、 TiDB SQLのアカウントシステムと一致しています。TiDBダッシュボードにアクセスするユーザーは、 TiDB SQLユーザーの権限に基づいて認証および承認されます。そのため、TiDBダッシュボードでは限定的な権限、つまり読み取り専用権限のみが必要です。最小権限の原則に基づいてユーザーがTiDBダッシュボードにアクセスできるように設定することで、高い権限を持つユーザーのアクセスを回避できます。

TiDBダッシュボードにアクセスしてサインインするには、最小限の権限を持つSQLユーザーを作成することをお勧めします。これにより、高い権限を持つユーザーによるアクセスを回避し、セキュリティを向上できます。詳細は[TiDBダッシュボードのユーザー管理](/dashboard/dashboard-user.md)ご覧ください。

## ファイアウォールを使用して信頼できないアクセスをブロックする {#use-a-firewall-to-block-untrusted-access}

> **注記：**
>
> TiDB v6.5.0以降およびTiDB Operator v1.4.0以降は、Kubernetes上にTiDB Dashboardを独立したPodとしてデプロイすることをサポートしています。TiDB TiDB Operatorを使用すると、このPodのIPアドレスにアクセスしてTiDB Dashboardを起動できます。このポートはPDの他の特権インターフェースとは通信しないため、外部から提供される場合は追加のファイアウォールは必要ありません。詳細については、 [TiDB ダッシュボードをTiDB Operatorで独立してデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/v1.6/get-started#deploy-tidb-dashboard-independently)参照してください。

TiDBダッシュボードはPDクライアントポート（デフォルトは[http://IP:2379/ダッシュボード/](http://IP:2379/dashboard/) ）を介してサービスを提供します。TiDBダッシュボードはID認証を必要としますが、PDクライアントポート上のPD内の他の特権インターフェース（例： [http://IP:2379/pd/api/v1/members](http://IP:2379/pd/api/v1/members) ）はID認証を必要とせず、特権操作を実行できます。したがって、PDクライアントポートを外部ネットワークに直接公開することは非常に危険です。

以下の対策を講じることをお勧めします。

-   ファイアウォールを使用して、コンポーネントが外部ネットワークまたは信頼できないネットワーク経由で PDコンポーネントの**クライアント**ポートにアクセスすることを禁止します。

    > **注記：**
    >
    > TiDB、TiKV、その他のコンポーネントは、PDクライアントポートを介してPDコンポーネントと通信する必要があるため、コンポーネント間の内部ネットワークへのアクセスをブロックしないでください。ブロックすると、クラスターが使用できなくなります。

-   リバース プロキシを構成して、別のポートで TiDB ダッシュボード サービスを外部ネットワークに安全に提供する方法の詳細については、 [リバースプロキシの背後で TiDB ダッシュボードを使用する](/dashboard/dashboard-ops-reverse-proxy.md)参照してください。

### 複数のPDインスタンスを展開するときにTiDBダッシュボードポートへのアクセスを開く方法 {#how-to-open-access-to-tidb-dashboard-port-when-deploying-multiple-pd-instances}

> **警告：**
>
> このセクションでは、テスト環境のみを対象とした、安全でないアクセスに対する解決策について説明します。本番環境では使用**しないでください**。

テスト環境では、外部アクセス用に TiDB ダッシュボード ポートを開くようにファイアウォールを構成する必要がある場合があります。

複数のPDインスタンスがデプロイされている場合、TiDBダッシュボードは実際に1つのPDインスタンスのみで実行され、他のPDインスタンスにアクセスするとブラウザのリダイレクトが発生します。そのため、ファイアウォールに正しいIPアドレスが設定されていることを確認する必要があります。このメカニズムの詳細については、 [複数のPDインスタンスを使用したデプロイメント](/dashboard/dashboard-ops-deploy.md#deployment-with-multiple-pd-instances)参照してください。

TiUPデプロイメント ツールを使用する場合、次のコマンドを実行すると、実際に TiDB ダッシュボードを実行している PD インスタンスのアドレスを表示できます ( `CLUSTER_NAME`クラスター名に置き換えます)。

```bash
tiup cluster display CLUSTER_NAME --dashboard
```

出力は実際の TiDB ダッシュボード アドレスです。

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

以下はサンプル出力です。

```bash
http://192.168.0.123:2379/dashboard/
```

この例では、ファイアウォールは、開いている IP `192.168.0.123`のポート`2379`への受信アクセスを設定する必要があり、TiDB ダッシュボードには[http://192.168.0.123:2379/ダッシュボード/](http://192.168.0.123:2379/dashboard/)経由でアクセスします。

## TiDB ダッシュボード専用のリバース プロキシ {#reverse-proxy-only-for-tidb-dashboard}

[ファイアウォールを使用して信頼できないアクセスをブロックする](#ファイアウォールを使用して信頼できないアクセスをブロックする)で述べたように、PDクライアントポートで提供されるサービスには、TiDBダッシュボード（ [http://IP:2379/ダッシュボード/](http://IP:2379/dashboard/)に配置）だけでなく、PD内の他の特権インターフェース（ [http://IP:2379/pd/api/v1/members](http://IP:2379/pd/api/v1/members)など）も含まれます。したがって、リバースプロキシを使用してTiDBダッシュボードを外部ネットワークに提供する場合は、外部ネットワークが**リバース**プロキシを介してPD内の特権インターフェースにアクセスできないように、ポート内のすべてのサービスで**はなく**、プレフィックスが`/dashboard`サービスのみを提供するようにしてください。

安全で推奨されるリバース プロキシ構成を確認するには、 [リバースプロキシの背後で TiDB ダッシュボードを使用する](/dashboard/dashboard-ops-reverse-proxy.md)参照することをお勧めします。

## リバースプロキシのTLSを有効にする {#enable-tls-for-reverse-proxy}

トランスポートレイヤーのセキュリティをさらに強化するには、リバース プロキシに対して TLS を有効にし、さらに mTLS を導入してユーザー証明書を認証することもできます。

詳細は[HTTPSサーバーの設定](http://nginx.org/en/docs/http/configuring_https_servers.html)と[HAProxy SSL 終了](https://www.haproxy.com/blog/haproxy-ssl-termination/)ご覧ください。

## その他の推奨される安全対策 {#other-recommended-safety-measures}

-   [TLS認証を有効にして保存データを暗号化する](/enable-tls-between-components.md)
-   [TiDBクライアントとサーバー間のTLSを有効にする](/enable-tls-between-clients-and-servers.md)
