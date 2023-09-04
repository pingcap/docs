---
title: Secure TiDB Dashboard
summary: Learn how to improve the security of TiDB Dashboard.
---

# セキュリティTiDB ダッシュボード {#secure-tidb-dashboard}

TiDB ダッシュボードにアクセスする前にサインインする必要がありますが、TiDB ダッシュボードはデフォルトで信頼できるユーザー エンティティによってアクセスされるように設計されています。 TiDB ダッシュボードを外部ネットワーク ユーザーまたは信頼されていないユーザーにアクセスのために提供する場合は、セキュリティの脆弱性を回避するために次の措置を講じてください。

## TiDB ユーザーのセキュリティを強化する {#enhance-security-of-tidb-users}

### TiDB <code>root</code>ユーザーに強力なパスワードを設定します。 {#set-a-strong-password-for-the-tidb-code-root-code-user}

TiDB ダッシュボードのアカウント システムは、 TiDB SQLユーザーのアカウント システムと一致しています。デフォルトでは、TiDB の`root`ユーザーにはパスワードがないため、TiDB ダッシュボードへのアクセスにはパスワード認証が必要ありません。これにより、悪意のある訪問者に、特権付き SQL ステートメントの実行などの高い権限が与えられます。

TiDB `root`ユーザーには強力なパスワードを設定することをお勧めします。詳細は[TiDB ユーザーアカウント管理](/user-account-management.md)参照してください。あるいは、TiDB `root`ユーザーを無効にすることもできます。

### TiDB ダッシュボード用に最小権限のユーザーを作成する {#create-a-least-privileged-user-for-tidb-dashboard}

TiDB Dashboard のアカウント システムは、 TiDB SQLのアカウント システムと一致しています。 TiDB ダッシュボードにアクセスするユーザーは、 TiDB SQLユーザーの権限に基づいて認証および許可されます。したがって、TiDB ダッシュボードには、制限された権限、または単に読み取り専用の権限が必要です。最小特権の原則に基づいて TiDB ダッシュボードにアクセスするようにユーザーを構成できるため、高い特権を持つユーザーのアクセスを回避できます。

TiDB ダッシュボードにアクセスしてサインインするには、最小限の権限を持つ SQL ユーザーを作成することをお勧めします。これにより、高い権限を持つユーザーのアクセスが回避され、セキュリティが向上します。詳細については[TiDB ダッシュボードのユーザー管理](/dashboard/dashboard-user.md)を参照してください。

## ファイアウォールを使用して信頼できないアクセスをブロックする {#use-a-firewall-to-block-untrusted-access}

> **注記：**
>
> TiDB v6.5.0 (以降) およびTiDB Operator v1.4.0 (以降) は、TiDB ダッシュボードを Kubernetes 上の独立したポッドとしてデプロイすることをサポートしています。 TiDB Operatorを使用すると、このポッドの IP アドレスにアクセスして TiDB ダッシュボードを起動できます。このポートは PD の他の特権インターフェイスとは通信せず、外部に提供される場合は追加のファイアウォールは必要ありません。詳細は[TiDB Operatorで TiDB ダッシュボードを独立してデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/dev/get-started#deploy-tidb-dashboard-independently)を参照してください。

TiDB ダッシュボードは、PD クライアント ポート (デフォルトは[http://IP:2379/ダッシュボード/](http://IP:2379/dashboard/)を通じてサービスを提供します。 TiDB ダッシュボードには ID 認証が必要ですが、PD クライアント ポートで伝送される PD の他の特権インターフェイス ( [http://IP:2379/pd/api/v1/members](http://IP:2379/pd/api/v1/members)など) は ID 認証を必要とせず、特権操作を実行できます。したがって、PD クライアント ポートを外部ネットワークに直接公開することは非常に危険です。

次のような対策を講じることをお勧めします。

-   ファイアウォールを使用して、コンポーネントが外部ネットワークまたは信頼できないネットワークを介して PDコンポーネントのクライアント**ポート**にアクセスすることを禁止します。

    > **注記：**
    >
    > TiDB、TiKV、およびその他のコンポーネントは、PD クライアント ポートを介して PDコンポーネントと通信する必要があるため、コンポーネント間の内部ネットワークへのアクセスをブロックしないでください。そうしないと、クラスターが使用できなくなります。

-   TiDB ダッシュボード サービスを別のポートで外部ネットワークに安全に提供するためにリバース プロキシを構成する方法については、 [リバース プロキシの背後で TiDB ダッシュボードを使用する](/dashboard/dashboard-ops-reverse-proxy.md)を参照してください。

### 複数の PD インスタンスをデプロイするときに TiDB ダッシュボード ポートへのアクセスを開く方法 {#how-to-open-access-to-tidb-dashboard-port-when-deploying-multiple-pd-instances}

> **警告：**
>
> このセクションでは、テスト環境のみを対象とした、安全でないアクセスのソリューションについて説明します。このソリューションは本番環境では使用**しないでください**。

テスト環境では、外部アクセス用に TiDB ダッシュボード ポートを開くようにファイアウォールを構成する必要がある場合があります。

複数の PD インスタンスがデプロイされている場合、実際に TiDB ダッシュボードを実行するのは PD インスタンスの 1 つだけであり、他の PD インスタンスにアクセスするとブラウザーのリダイレクトが発生します。したがって、ファイアウォールが正しい IP アドレスで構成されていることを確認する必要があります。この仕組みの詳細については、 [複数の PD インスタンスを使用したデプロイメント](/dashboard/dashboard-ops-deploy.md#deployment-with-multiple-pd-instances)を参照してください。

TiUPデプロイメント ツールを使用する場合、次のコマンドを実行することで、TiDB ダッシュボードを実際に実行する PD インスタンスのアドレスを表示できます ( `CLUSTER_NAME`をクラスター名に置き換えます)。

```bash
tiup cluster display CLUSTER_NAME --dashboard
```

出力は実際の TiDB ダッシュボード アドレスです。

> **注記：**
>
> この機能は、 `tiup cluster`導入ツールの新しいバージョン (v1.0.3 以降) でのみ使用できます。
>
> <details>
>   TiUPクラスタのアップグレード
>
>   ```bash
>   tiup update --self
>   tiup update cluster --force
>   ```
> </details>

以下は出力例です。

```bash
http://192.168.0.123:2379/dashboard/
```

この例では、ファイアウォールは`192.168.0.123`のオープン IP の`2379`ポートに対する受信アクセスを設定する必要があり、TiDB ダッシュボードは[http://192.168.0.123:2379/ダッシュボード/](http://192.168.0.123:2379/dashboard/)を介してアクセスされます。

## TiDB ダッシュボード専用のリバース プロキシ {#reverse-proxy-only-for-tidb-dashboard}

[ファイアウォールを使用して信頼できないアクセスをブロックする](#use-a-firewall-to-block-untrusted access) で説明したように、PD クライアント ポートで提供されるサービスには、TiDB ダッシュボード ( [http://IP:2379/ダッシュボード/](http://IP:2379/dashboard/)にあります) だけでなく、その他のサービスも含まれます。 PD の特権インターフェイス ( [http://IP:2379/pd/api/v1/members](http://IP:2379/pd/api/v1/members)など)。したがって**、**リバース プロキシを使用`/dashboard`て TiDB ダッシュボードを外部ネットワークに提供する場合は、外部**ネットワーク**がリバースプロキシ。

安全で推奨されるリバース プロキシ構成については、 [リバース プロキシの背後で TiDB ダッシュボードを使用する](/dashboard/dashboard-ops-reverse-proxy.md)を参照することをお勧めします。

## リバースプロキシのTLSを有効にする {#enable-tls-for-reverse-proxy}

トランスポートレイヤーのセキュリティをさらに強化するには、リバース プロキシの TLS を有効にし、ユーザー証明書を認証するために mTLS を導入することもできます。

詳細については、 [HTTPSサーバーの構成](http://nginx.org/en/docs/http/configuring_https_servers.html)と[HAProxy SSL 終了](https://www.haproxy.com/blog/haproxy-ssl-termination/)を参照してください。

## その他の推奨される安全対策 {#other-recommended-safety-measures}

-   [TLS認証を有効にし、保存されたデータを暗号化する](/enable-tls-between-components.md)
-   [TiDB クライアントとサーバー間で TLS を有効にする](/enable-tls-between-clients-and-servers.md)
