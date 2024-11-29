---
title: Secure TiDB Dashboard
summary: TiDB ダッシュボードでは、ルート ユーザーに強力なパスワードを設定し、最小権限のユーザーを作成し、ファイアウォールを使用して信頼できないアクセスをブロックするなど、強化されたセキュリティ対策が必要です。また、セキュリティをさらに強化するために、リバース プロキシを使用し、TLS を有効にすることもお勧めします。
---

# セキュリティTiDB ダッシュボード {#secure-tidb-dashboard}

TiDB ダッシュボードにアクセスするにはサインインする必要がありますが、デフォルトでは、TiDB ダッシュボードは信頼できるユーザー エンティティによってアクセスされるように設計されています。外部ネットワーク ユーザーまたは信頼できないユーザーに TiDB ダッシュボードへのアクセスを提供する場合は、セキュリティの脆弱性を回避するために次の対策を講じてください。

## TiDBユーザーのセキュリティを強化する {#enhance-security-of-tidb-users}

### TiDB <code>root</code>ユーザーに強力なパスワードを設定する {#set-a-strong-password-for-the-tidb-code-root-code-user}

TiDB ダッシュボードのアカウント システムは、 TiDB SQLユーザーのアカウント システムと一致しています。デフォルトでは、TiDB の`root`ユーザーにはパスワードがないため、TiDB ダッシュボードへのアクセスにはパスワード認証は必要なく、悪意のある訪問者に特権 SQL ステートメントの実行を含む高い権限が与えられます。

TiDB `root`ユーザーには強力なパスワードを設定することをお勧めします。詳細については[TiDB ユーザーアカウント管理](/user-account-management.md)参照してください。または、TiDB `root`ユーザーを無効にすることもできます。

### TiDBダッシュボードの最小権限ユーザーを作成する {#create-a-least-privileged-user-for-tidb-dashboard}

TiDB ダッシュボードのアカウント システムは、 TiDB SQLのアカウント システムと一致しています。TiDB ダッシュボードにアクセスするユーザーは、 TiDB SQLユーザーの権限に基づいて認証および承認されます。したがって、TiDB ダッシュボードには、制限された権限、つまり読み取り専用権限のみが必要です。最小限の権限の原則に基づいてユーザーが TiDB ダッシュボードにアクセスするように構成することで、高い権限を持つユーザーのアクセスを回避できます。

TiDB ダッシュボードにアクセスしてサインインするには、最小限の権限を持つ SQL ユーザーを作成することをお勧めします。これにより、高い権限を持つユーザーのアクセスが回避され、セキュリティが向上します。詳細については、 [TiDBダッシュボードユーザー管理](/dashboard/dashboard-user.md)参照してください。

## ファイアウォールを使用して信頼できないアクセスをブロックする {#use-a-firewall-to-block-untrusted-access}

> **注記：**
>
> TiDB v6.5.0 (以降) およびTiDB Operator v1.4.0 (以降) では、Kubernetes 上の独立した Pod として TiDB Dashboard をデプロイできます。 TiDB Operator を使用すると、この Pod の IP アドレスにアクセスして TiDB Dashboard を起動できます。 このポートは PD の他の特権インターフェイスと通信しないため、外部から提供される場合は追加のファイアウォールは必要ありません。 詳細については、 [TiDB ダッシュボードをTiDB Operatorに独立してデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/dev/get-started#deploy-tidb-dashboard-independently)参照してください。

TiDB ダッシュボードは、デフォルトで[http://IP:2379/ダッシュボード/](http://IP:2379/dashboard/)に設定されている PD クライアント ポートを通じてサービスを提供します。TiDB ダッシュボードでは ID 認証が必要ですが、PD クライアント ポートで実行される PD 内の他の特権インターフェイス ( [http://IP:2379/pd/api/v1/メンバー](http://IP:2379/pd/api/v1/members)など) では ID 認証は必要なく、特権操作を実行できます。したがって、PD クライアント ポートを外部ネットワークに直接公開することは非常に危険です。

以下の対策を講じることをお勧めします。

-   ファイアウォールを使用して、コンポーネントが外部ネットワークまたは信頼できないネットワーク経由で PDコンポーネントの**クライアント**ポートにアクセスすることを禁止します。

    > **注記：**
    >
    > TiDB、TiKV、およびその他のコンポーネントは、PD クライアント ポートを介して PDコンポーネントと通信する必要があるため、コンポーネント間の内部ネットワークへのアクセスをブロックしないでください。そうしないと、クラスターが使用できなくなります。

-   リバース プロキシを構成して、別のポートで TiDB ダッシュボード サービスを外部ネットワークに安全に提供する方法の詳細については、 [リバースプロキシの背後でTiDBダッシュボードを使用する](/dashboard/dashboard-ops-reverse-proxy.md)参照してください。

### 複数の PD インスタンスを展開するときに TiDB ダッシュボード ポートへのアクセスを開く方法 {#how-to-open-access-to-tidb-dashboard-port-when-deploying-multiple-pd-instances}

> **警告：**
>
> このセクションでは、テスト環境のみを対象とした安全でないアクセス ソリューションについて説明します。このソリューションは本番環境では使用し**ないでください**。

テスト環境では、外部アクセス用に TiDB ダッシュボード ポートを開くようにファイアウォールを構成する必要がある場合があります。

複数の PD インスタンスがデプロイされている場合、実際に TiDB Dashboard を実行するのは PD インスタンスの 1 つだけであり、他の PD インスタンスにアクセスするとブラウザのリダイレクトが発生します。そのため、ファイアウォールが正しい IP アドレスで設定されていることを確認する必要があります。このメカニズムの詳細については、 [複数のPDインスタンスを使用したデプロイメント](/dashboard/dashboard-ops-deploy.md#deployment-with-multiple-pd-instances)参照してください。

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

[ファイアウォールを使用して信頼できないアクセスをブロックする](#use-a-firewall-to-block-untrusted access) で説明したように、PD クライアント ポートで提供されるサービスには、TiDB ダッシュボード ( [http://IP:2379/ダッシュボード/](http://IP:2379/dashboard/)に配置) だけでなく、PD 内の他の特権インターフェイス ( [http://IP:2379/pd/api/v1/メンバー](http://IP:2379/pd/api/v1/members)など) も含まれます。したがって、リバース プロキシを使用して TiDB ダッシュボードを外部ネットワークに提供する場合、外部ネットワークがリバース プロキシを介して PD 内の特権インターフェイスにアクセスできないように、プレフィックスが`/dashboard`サービス**のみ**が提供されていることを確認してください (ポートのすべてのサービスでは**ありません**)。

安全で推奨されるリバース プロキシ構成を確認するには、 [リバースプロキシの背後でTiDBダッシュボードを使用する](/dashboard/dashboard-ops-reverse-proxy.md)参照することをお勧めします。

## リバースプロキシのTLSを有効にする {#enable-tls-for-reverse-proxy}

トランスポートレイヤーのセキュリティをさらに強化するには、リバース プロキシの TLS を有効にし、ユーザー証明書を認証するために mTLS を導入することもできます。

詳細は[HTTPS サーバーの設定](http://nginx.org/en/docs/http/configuring_https_servers.html)と[HAProxy SSL 終了](https://www.haproxy.com/blog/haproxy-ssl-termination/)ご覧ください。

## その他の推奨される安全対策 {#other-recommended-safety-measures}

-   [TLS認証を有効にして保存データを暗号化する](/enable-tls-between-components.md)
-   [TiDBクライアントとサーバー間のTLSを有効にする](/enable-tls-between-clients-and-servers.md)
