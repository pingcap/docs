---
title: Secure TiDB Dashboard
summary: Learn how to improve the security of TiDB Dashboard.
---

# セキュリティTiDBダッシュボード {#secure-tidb-dashboard}

TiDBダッシュボードにアクセスする前にサインインする必要がありますが、TiDBダッシュボードは、デフォルトで信頼できるユーザーエンティティからアクセスできるように設計されています。外部ネットワークユーザーまたは信頼できないユーザーにアクセスのためにTiDBダッシュボードを提供する場合は、セキュリティの脆弱性を回避するために次の対策を講じてください。

## TiDBユーザーのセキュリティを強化する {#enhance-security-of-tidb-users}

### <code>root</code>ユーザーに強力なパスワードを設定します {#set-a-strong-password-for-the-tidb-code-root-code-user}

TiDBダッシュボードのアカウントシステムは、 TiDB SQLユーザーのアカウントシステムと一致しています。デフォルトでは、TiDBの`root`ユーザーにはパスワードがないため、TiDBダッシュボードにアクセスするためにパスワード認証は必要ありません。これにより、悪意のある訪問者に、特権SQLステートメントの実行を含む高い特権が与えられます。

`root`ユーザーには強力なパスワードを設定することをお勧めします。詳細については、 [TiDBユーザーアカウント管理](/user-account-management.md)を参照してください。または、 `root`ユーザーを無効にすることもできます。

### TiDBダッシュボードの最小特権ユーザーを作成します {#create-a-least-privileged-user-for-tidb-dashboard}

TiDBダッシュボードのアカウントシステムは、TiDBSQLのアカウントシステムと一致していTiDB SQL。 TiDBダッシュボードにアクセスするユーザーは、 TiDB SQLユーザーの権限に基づいて認証および承認されます。したがって、TiDBダッシュボードには、制限された特権、または単に読み取り専用の特権が必要です。最小特権の原則に基づいてTiDBダッシュボードにアクセスするようにユーザーを構成できるため、特権の高いユーザーのアクセスを回避できます。

TiDBダッシュボードにアクセスしてサインインするための最小特権SQLユーザーを作成することをお勧めします。これにより、特権の高いユーザーのアクセスが回避され、セキュリティが向上します。詳細については、 [TiDBダッシュボードユーザー管理](/dashboard/dashboard-user.md)を参照してください。

## ファイアウォールを使用して、信頼できないアクセスをブロックします {#use-a-firewall-to-block-untrusted-access}

TiDBダッシュボードは、PDクライアントポートを介してサービスを提供します。デフォルトは[http：// IP：2379 / dashboard /](http://IP:2379/dashboard/)です。 TiDBダッシュボードにはID認証が必要ですが、PDクライアントポートで伝送されるPDの他の特権インターフェイス（ [http：// IP：2379 / pd / api / v1 / members](http://IP:2379/pd/api/v1/members)など）はID認証を必要とせず、特権操作を実行できます。したがって、PDクライアントポートを外部ネットワークに直接公開することは非常に危険です。

次の対策を講じることをお勧めします。

-   ファイアウォールを使用して、コンポーネントが外部ネットワークまたは信頼できないネットワークを介してPDコンポーネントのクライアントポートにアクセス**すること**を禁止します。

    > **ノート：**
    >
    > TiDB、TiKV、およびその他のコンポーネントは、PDクライアントポートを介してPDコンポーネントと通信する必要があるため、コンポーネント間の内部ネットワークへのアクセスをブロックしないでください。そうしないと、クラスタが使用できなくなります。

-   別のポートで外部ネットワークにTiDBダッシュボードサービスを安全に提供するようにリバースプロキシを構成する方法については、 [リバースプロキシの背後でTiDBダッシュボードを使用する](/dashboard/dashboard-ops-reverse-proxy.md)を参照してください。

### 複数のPDインスタンスを展開するときにTiDBダッシュボードポートへのアクセスを開く方法 {#how-to-open-access-to-tidb-dashboard-port-when-deploying-multiple-pd-instances}

> **警告：**
>
> このセクションでは、テスト環境専用の安全でないアクセスソリューションについて説明します。このソリューションを実稼働環境で使用し**ない**でください。

テスト環境では、外部アクセス用にTiDBダッシュボードポートを開くようにファイアウォールを構成する必要がある場合があります。

複数のPDインスタンスがデプロイされている場合、実際に実行されるのは1つのPDインスタンスのみであり、他のPDインスタンスにアクセスするとブラウザーのリダイレクトが発生します。したがって、ファイアウォールが正しいIPアドレスで構成されていることを確認する必要があります。このメカニズムの詳細については、 [複数のPDインスタンスを使用した展開](/dashboard/dashboard-ops-deploy.md#deployment-with-multiple-pd-instances)を参照してください。

TiUPデプロイメントツールを使用する場合、次のコマンドを実行することにより、実際にTiDBダッシュボードを実行するPDインスタンスのアドレスを表示できます（ `CLUSTER_NAME`をクラスタ名に置き換えます）。

{{< copyable "" >}}

```bash
tiup cluster display CLUSTER_NAME --dashboard
```

出力は実際のTiDBダッシュボードアドレスです。

> **ノート：**
>
> この機能は、 `tiup cluster`デプロイメントツールの新しいバージョン（v1.0.3以降）でのみ使用できます。
>
> <details><summary>TiUPクラスターをアップグレードする</summary>
>
> {{< copyable "" >}}
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

この例では、ファイアウォールは`192.168.0.123`のオープンIPの`2379`のポートへのインバウンドアクセスで構成する必要があり、TiDBダッシュボードは[http://192.168.0.123:2379/dashboard/](http://192.168.0.123:2379/dashboard/)を介してアクセスされます。

## TiDBダッシュボード専用のリバースプロキシ {#reverse-proxy-only-for-tidb-dashboard}

[ファイアウォールを使用して信頼できないアクセスをブロックする]（＃use-a-firewall-to-block-untrustedアクセス）で説明したように、PDクライアントポートで提供されるサービスには、TiDBダッシュボード（ [http：// IP：2379 / dashboard /](http://IP:2379/dashboard/)にあります）だけでなく、他のPDの特権インターフェイス（ [http：// IP：2379 / pd / api / v1 / members](http://IP:2379/pd/api/v1/members)など）。したがって、リバースプロキシを使用して外部ネットワークにTiDBダッシュボードを提供する場合は、外部ネットワークがPDの特権インターフェイスにアクセスできるように、プレフィックスが`/dashboard`のサービス**のみ**が提供されていることを確認してください（ポート内のすべてのサービスではあり<strong>ません</strong>）。リバースプロキシ。

安全で推奨されるリバースプロキシ構成を学習するには、 [リバースプロキシの背後でTiDBダッシュボードを使用する](/dashboard/dashboard-ops-reverse-proxy.md)を表示することをお勧めします。

## リバースプロキシのTLSを有効にする {#enable-tls-for-reverse-proxy}

トランスポート層のセキュリティをさらに強化するために、リバースプロキシのTLSを有効にしたり、ユーザー証明書を認証するためにmTLSを導入したりすることもできます。

詳細については、 [HTTPSサーバーの構成](http://nginx.org/en/docs/http/configuring_https_servers.html)と[HAProxySSLターミネーション](https://www.haproxy.com/blog/haproxy-ssl-termination/)を参照してください。

## その他の推奨される安全対策 {#other-recommended-safety-measures}

-   [TLS認証を有効にし、保存されたデータを暗号化する](/enable-tls-between-components.md)
-   [TiDBクライアントとサーバー間のTLSを有効にする](/enable-tls-between-clients-and-servers.md)
