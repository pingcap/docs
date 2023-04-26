---
title: Secure TiDB Dashboard
summary: Learn how to improve the security of TiDB Dashboard.
---

# セキュリティTiDB ダッシュボード {#secure-tidb-dashboard}

アクセスする前に TiDB ダッシュボードにサインインする必要がありますが、デフォルトでは、TiDB ダッシュボードは信頼できるユーザー エンティティによってアクセスされるように設計されています。 TiDB ダッシュボードを外部ネットワーク ユーザーまたは信頼されていないユーザーにアクセス用に提供する場合は、セキュリティの脆弱性を回避するために次の対策を講じてください。

## TiDB ユーザーのセキュリティを強化する {#enhance-security-of-tidb-users}

### TiDB <code>root</code>ユーザーに強力なパスワードを設定する {#set-a-strong-password-for-the-tidb-code-root-code-user}

TiDB ダッシュボードのアカウント システムは、 TiDB SQLユーザーのアカウント システムと一致しています。デフォルトでは、TiDB の`root`ユーザーにはパスワードがないため、TiDB ダッシュボードへのアクセスにパスワード認証は必要ありません。これにより、悪意のある訪問者に特権 SQL ステートメントの実行を含む高い権限が与えられます。

TiDB `root`ユーザーには強力なパスワードを設定することをお勧めします。詳細は[TiDB ユーザー アカウント管理](/user-account-management.md)参照してください。または、TiDB `root`ユーザーを無効にすることもできます。

### TiDB ダッシュボード用の最小特権ユーザーを作成する {#create-a-least-privileged-user-for-tidb-dashboard}

TiDB ダッシュボードのアカウント システムは、 TiDB SQLのアカウント システムと一致しています。 TiDB ダッシュボードにアクセスするユーザーは、 TiDB SQLユーザーの権限に基づいて認証および承認されます。したがって、TiDB ダッシュボードには限定された権限、または単に読み取り専用権限が必要です。最小権限の原則に基づいて TiDB ダッシュボードにアクセスするようにユーザーを構成できるため、高い権限を持つユーザーのアクセスを回避できます。

TiDB ダッシュボードにアクセスしてサインインするには、最小限の特権を持つ SQL ユーザーを作成することをお勧めします。これにより、権限の高いユーザーのアクセスが回避され、セキュリティが向上します。詳細は[TiDB ダッシュボードのユーザー管理](/dashboard/dashboard-user.md)を参照してください。

## ファイアウォールを使用して信頼できないアクセスをブロックする {#use-a-firewall-to-block-untrusted-access}

> **ノート：**
>
> TiDB v6.5.0 (およびそれ以降) およびTiDB Operator v1.4.0 (およびそれ以降) は、TiDB ダッシュボードを Kubernetes 上の独立した Pod としてデプロイすることをサポートします。 TiDB Operatorを使用して、この Pod の IP アドレスにアクセスし、TiDB ダッシュボードを起動できます。このポートは、PD の他の特権インターフェイスと通信しないため、外部から提供された場合、追加のファイアウォールは必要ありません。詳細については、 [TiDB Operatorで TiDB ダッシュボードを個別にデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/dev/get-started#deploy-tidb-dashboard-independently)を参照してください。

TiDB ダッシュボードは、デフォルトで[http://IP:2379/ダッシュボード/](http://IP:2379/dashboard/)に設定されている PD クライアント ポートを介してサービスを提供します。 TiDB ダッシュボードには ID 認証が必要ですが、PD クライアント ポートで実行される PD の他の特権インターフェイス ( [http://IP:2379/pd/api/v1/members](http://IP:2379/pd/api/v1/members)など) は ID 認証を必要とせず、特権操作を実行できます。したがって、PD クライアント ポートを外部ネットワークに直接公開することは非常に危険です。

次の対策を講じることをお勧めします。

-   ファイアウォールを使用して、コンポーネントが外部ネットワークまたは信頼できないネットワーク経由で PDコンポーネントのクライアント**ポート**にアクセスすることを禁止します。

    > **ノート：**
    >
    > TiDB、TiKV、およびその他のコンポーネントは、PD クライアント ポートを介して PDコンポーネントと通信する必要があるため、コンポーネント間の内部ネットワークへのアクセスをブロックしないでください。そうしないと、クラスターが使用できなくなります。

-   外部ネットワークへの別のポートで TiDB ダッシュボード サービスを安全に提供するようにリバース プロキシを構成する方法については、 [リバース プロキシの背後で TiDB ダッシュボードを使用する](/dashboard/dashboard-ops-reverse-proxy.md)を参照してください。

### 複数の PD インスタンスをデプロイするときに TiDB ダッシュボード ポートへのアクセスを開く方法 {#how-to-open-access-to-tidb-dashboard-port-when-deploying-multiple-pd-instances}

> **警告：**
>
> このセクションでは、テスト環境専用の安全でないアクセス ソリューションについて説明します。このソリューションを本番環境で使用**しないでください**。

テスト環境では、外部アクセス用に TiDB ダッシュボード ポートを開くようにファイアウォールを構成する必要がある場合があります。

複数の PD インスタンスがデプロイされている場合、実際に TiDB ダッシュボードを実行する PD インスタンスは 1 つだけであり、他の PD インスタンスにアクセスするとブラウザーのリダイレクトが発生します。したがって、ファイアウォールが正しい IP アドレスで構成されていることを確認する必要があります。このメカニズムの詳細については、 [複数の PD インスタンスを使用した展開](/dashboard/dashboard-ops-deploy.md#deployment-with-multiple-pd-instances)を参照してください。

TiUPデプロイ ツールを使用する場合、次のコマンドを実行して、実際に TiDB ダッシュボードを実行する PD インスタンスのアドレスを表示できます ( `CLUSTER_NAME`をクラスター名に置き換えます)。

{{< copyable "" >}}

```bash
tiup cluster display CLUSTER_NAME --dashboard
```

出力は、実際の TiDB ダッシュボード アドレスです。

> **ノート：**
>
> この機能は、 `tiup cluster`展開ツールの新しいバージョン (v1.0.3 以降) でのみ使用できます。
>
> <details><summary>TiUPクラスタのアップグレード</summary>
>
> ```bash
> tiup update --self
> tiup update cluster --force
> ```
>
> </details>

次に出力例を示します。

```bash
http://192.168.0.123:2379/dashboard/
```

この例では、ファイアウォールは`192.168.0.123`のオープン IP の`2379`ポートのインバウンド アクセスで構成する必要があり、TiDB ダッシュボードは[http://192.168.0.123:2379/ダッシュボード/](http://192.168.0.123:2379/dashboard/)経由でアクセスされます。

## TiDB ダッシュボード専用のリバース プロキシ {#reverse-proxy-only-for-tidb-dashboard}

[ファイアウォールを使用して信頼されていないアクセスをブロックする](#use-a-firewall-to-block-untrusted access) で述べたように、PD クライアント ポートで提供されるサービスには、TiDB ダッシュボード ( [http://IP:2379/ダッシュボード/](http://IP:2379/dashboard/)にあります) だけでなく、他のサービスも含まれます。 PD の特権インターフェイス ( [http://IP:2379/pd/api/v1/members](http://IP:2379/pd/api/v1/members)など)。**したがって**、リバース プロキシを`/dashboard`して TiDB ダッシュボードを外部ネットワーク<strong>に</strong>提供する場合は、外部ネットワークが PD の特権インターフェイスにリバース プロキシ。

[リバース プロキシの背後で TiDB ダッシュボードを使用する](/dashboard/dashboard-ops-reverse-proxy.md)を参照して、安全で推奨されるリバース プロキシ構成を学習することをお勧めします。

## リバース プロキシの TLS を有効にする {#enable-tls-for-reverse-proxy}

トランスポートレイヤーのセキュリティをさらに強化するために、リバース プロキシに対して TLS を有効にしたり、mTLS を導入してユーザー証明書を認証したりすることもできます。

詳細については、 [HTTPS サーバーの構成](http://nginx.org/en/docs/http/configuring_https_servers.html)と[HAProxy SSL 終了](https://www.haproxy.com/blog/haproxy-ssl-termination/)を参照してください。

## その他の推奨される安全対策 {#other-recommended-safety-measures}

-   [TLS 認証を有効にして保存データを暗号化する](/enable-tls-between-components.md)
-   [TiDB クライアントとサーバー間で TLS を有効にする](/enable-tls-between-clients-and-servers.md)
