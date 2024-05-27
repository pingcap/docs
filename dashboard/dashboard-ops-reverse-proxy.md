---
title: Use TiDB Dashboard behind a Reverse Proxy
summary: TiDB ダッシュボードは、リバース プロキシを使用して安全に公開できます。これを行うには、実際の TiDB ダッシュボード アドレスを取得し、HAProxy または NGINX を使用してリバース プロキシを構成します。TiDB ダッシュボード サービスのパス プレフィックスをカスタマイズすることもできます。セキュリティを強化するには、ファイアウォールの構成を検討してください。
---

# リバースプロキシの背後で TiDB ダッシュボードを使用する {#use-tidb-dashboard-behind-a-reverse-proxy}

リバース プロキシを使用すると、TiDB ダッシュボード サービスを内部ネットワークから外部に安全に公開できます。

## 手順 {#procedures}

### ステップ1: 実際のTiDBダッシュボードアドレスを取得する {#step-1-get-the-actual-tidb-dashboard-address}

クラスター内に複数の PD インスタンスがデプロイされている場合、実際に TiDB Dashboard を実行するのは PD インスタンスのうちの 1 つだけです。そのため、リバース プロキシのアップストリームが正しいアドレスを指していることを確認する必要があります。このメカニズムの詳細については、 [複数のPDインスタンスを使用したデプロイメント](/dashboard/dashboard-ops-deploy.md#deployment-with-multiple-pd-instances)参照してください。

デプロイメントにTiUPツールを使用する場合は、次のコマンドを実行して実際の TiDB ダッシュボード アドレスを取得します ( `CLUSTER_NAME`クラスター名に置き換えます)。

```shell
tiup cluster display CLUSTER_NAME --dashboard
```

出力は実際の TiDB ダッシュボード アドレスです。サンプルは次のとおりです。

```bash
http://192.168.0.123:2379/dashboard/
```

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

### ステップ2: リバースプロキシを構成する {#step-2-configure-the-reverse-proxy}

<details><summary><strong>HAProxyを使用する</strong></summary>

[HAプロキシ](https://www.haproxy.org/)リバース プロキシとして使用する場合は、次の手順を実行します。

1.  たとえば、 `8033`ポートで TiDB ダッシュボードのリバース プロキシを使用します。HAProxy 構成ファイルに、次の構成を追加します。

    ```haproxy
    frontend tidb_dashboard_front
      bind *:8033
      use_backend tidb_dashboard_back if { path /dashboard } or { path_beg /dashboard/ }

    backend tidb_dashboard_back
      mode http
      server tidb_dashboard 192.168.0.123:2379
    ```

    `192.168.0.123:2379`を、 [ステップ1](#step-1-get-the-actual-tidb-dashboard-address)で取得した TiDB ダッシュボードの実際のアドレスの IP とポートに置き換えます。

    > **警告：**
    >
    > **このパス内のサービスのみが**リバース プロキシの背後にあることを保証するために、 `use_backend`ディレクティブの`if`部分を保持する必要があります。そうしないと、セキュリティ リスクが発生する可能性があります。 [セキュリティTiDB ダッシュボード](/dashboard/dashboard-ops-security.md)を参照してください。

2.  設定を有効にするには、HAProxy を再起動します。

3.  リバース プロキシが有効かどうかをテストします。HAProxy が配置されているマシンの`8033`ポート ( `http://example.com:8033/dashboard/`など) の`/dashboard/`アドレスにアクセスして、TiDB ダッシュボードにアクセスします。

</details>

<details><summary><strong>NGINXを使用する</strong></summary>

[NGINX とは](https://nginx.org/)リバース プロキシとして使用する場合は、次の手順を実行します。

1.  たとえば、 `8033`ポートで TiDB ダッシュボードのリバース プロキシを使用します。NGINX 構成ファイルに次の構成を追加します。

    ```nginx
    server {
        listen 8033;
        location /dashboard/ {
        proxy_pass http://192.168.0.123:2379/dashboard/;
        }
    }
    ```

    `http://192.168.0.123:2379/dashboard/` [ステップ1](#step-1-get-the-actual-tidb-dashboard-address)で取得した TiDB ダッシュボードの実際のアドレスに置き換えます。

    > **警告：**
    >
    > このパスの下にあるサービスのみがリバース プロキシされるようにするには、 `proxy_pass`ディレクティブに`/dashboard/`パスを保持する必要があります。そうしないと、セキュリティ リスクが発生します。 [セキュリティTiDB ダッシュボード](/dashboard/dashboard-ops-security.md)を参照してください。

2.  設定を有効にするには、NGINX をリロードします。

    ```shell
    sudo nginx -s reload
    ```

3.  リバース プロキシが有効かどうかをテストします。NGINX が配置されているマシンの`8033`ポートの`/dashboard/`アドレス ( `http://example.com:8033/dashboard/`など) にアクセスして、TiDB ダッシュボードにアクセスします。

</details>

## パスプレフィックスをカスタマイズする {#customize-path-prefix}

TiDB ダッシュボードは、デフォルトで`/dashboard/`パス ( `http://example.com:8033/dashboard/`など) でサービスを提供します。これはリバース プロキシの場合でも当てはまります。リバース プロキシを構成して、 `http://example.com:8033/foo/`や`http://example.com:8033/`などのデフォルト以外のパスで TiDB ダッシュボード サービスを提供するには、次の手順を実行します。

### ステップ1: PD構成を変更して、TiDBダッシュボードサービスのパスプレフィックスを指定します。 {#step-1-modify-pd-configuration-to-specify-the-path-prefix-of-tidb-dashboard-service}

PD 構成の`[dashboard]`カテゴリの`public-path-prefix`構成項目を変更して、TiDB ダッシュボード サービスのパス プレフィックスを指定します。この項目を変更したら、変更を有効にするために PD インスタンスを再起動します。

たとえば、クラスターがTiUPを使用してデプロイされており、サービスを`http://example.com:8033/foo/`で実行する場合は、次の構成を指定できます。

```yaml
server_configs:
  pd:
    dashboard.public-path-prefix: /foo
```

<details><summary><strong>TiUPを使用して新しいクラスターを展開するときに構成を変更する</strong></summary>

新しいクラスターを展開する場合は、上記の構成を`topology.yaml` TiUPトポロジ ファイルに追加してクラスターを展開できます。具体的な手順については、 [TiUP展開ドキュメント](/production-deployment-using-tiup.md#step-3-initialize-cluster-topology-file)を参照してください。

</details>

<details>

<summary><strong>TiUPを使用してデプロイされたクラスターの構成を変更する</strong></summary>

デプロイされたクラスターの場合:

1.  クラスターの構成ファイルを編集モードで開きます ( `CLUSTER_NAME`クラスター名に置き換えます)。

    ```shell
    tiup cluster edit-config CLUSTER_NAME
    ```

2.  `server_configs`の`pd`構成の下にある構成項目を変更または追加します。 `server_configs`存在しない場合は、最上位レベルに追加します。

    ```yaml
    monitored:
      ...
    server_configs:
      tidb: ...
      tikv: ...
      pd:
        dashboard.public-path-prefix: /foo
      ...
    ```

    変更後の設定ファイルは次のファイルのようになります。

    ```yaml
    server_configs:
      pd:
        dashboard.public-path-prefix: /foo
      global:
        user: tidb
        ...
    ```

    または

    ```yaml
    monitored:
      ...
    server_configs:
      tidb: ...
      tikv: ...
      pd:
        dashboard.public-path-prefix: /foo
    ```

3.  変更した設定を有効にするには、すべての PD インスタンスに対してローリング再起動を実行します ( `CLUSTER_NAME`クラスター名に置き換えます)。

    ```shell
    tiup cluster reload CLUSTER_NAME -R pd
    ```

詳細は[一般的なTiUP操作 - 構成の変更](/maintain-tidb-using-tiup.md#modify-the-configuration)参照。

</details>

TiDB ダッシュボード サービスをルート パス ( `http://example.com:8033/`など) で実行する場合は、次の構成を使用します。

```yaml
server_configs:
  pd:
    dashboard.public-path-prefix: /
```

> **警告：**
>
> 変更およびカスタマイズされたパス プレフィックスが有効になると、TiDB ダッシュボードに直接アクセスできなくなります。パス プレフィックスに一致するリバース プロキシを介してのみ、TiDB ダッシュボードにアクセスできます。

### ステップ2: リバースプロキシ構成を変更する {#step-2-modify-the-reverse-proxy-configuration}

<details><summary><strong>HAProxyを使用する</strong></summary>

`http://example.com:8033/foo/`例にとると、対応する HAProxy 構成は次のようになります。

```haproxy
frontend tidb_dashboard_front
  bind *:8033
  use_backend tidb_dashboard_back if { path /foo } or { path_beg /foo/ }

backend tidb_dashboard_back
  mode http
  http-request set-path %[path,regsub(^/foo/?,/dashboard/)]
  server tidb_dashboard 192.168.0.123:2379
```

`192.168.0.123:2379`を、 [ステップ1](#step-1-get-the-actual-tidb-dashboard-address)で取得した TiDB ダッシュボードの実際のアドレスの IP とポートに置き換えます。

> **警告：**
>
> **このパス内のサービスのみが**リバース プロキシの背後にあることを保証するために、 `use_backend`ディレクティブの`if`部分を保持する必要があります。そうしないと、セキュリティ リスクが発生する可能性があります。 [セキュリティTiDB ダッシュボード](/dashboard/dashboard-ops-security.md)を参照してください。

TiDB ダッシュボード サービスをルート パス ( `http://example.com:8033/`など) で実行する場合は、次の構成を使用します。

```haproxy
frontend tidb_dashboard_front
  bind *:8033
  use_backend tidb_dashboard_back
backend tidb_dashboard_back
  mode http
  http-request set-path /dashboard%[path]
  server tidb_dashboard 192.168.0.123:2379
```

設定を変更し、変更した設定を有効にするために HAProxy を再起動します。

</details>

<details><summary><strong>NGINXを使用する</strong></summary>

`http://example.com:8033/foo/`例にとると、対応する NGINX 構成は次のようになります。

```nginx
server {
  listen 8033;
  location /foo/ {
    proxy_pass http://192.168.0.123:2379/dashboard/;
  }
}
```

`http://192.168.0.123:2379/dashboard/` [ステップ1](#step-1-get-the-actual-tidb-dashboard-address)で取得した TiDB ダッシュボードの実際のアドレスに置き換えます。

> **警告：**
>
> `proxy_pass`ディレクティブの`/dashboard/`パスを保持して**、このパス内のサービスのみが**リバース プロキシの背後にあることを確認する必要があります。そうしないと、セキュリティ リスクが発生する可能性があります[セキュリティTiDB ダッシュボード](/dashboard/dashboard-ops-security.md)を参照してください。

TiDB ダッシュボード サービスをルート パス ( `http://example.com:8033/`など) で実行する場合は、次の構成を使用します。

```nginx
server {
  listen 8033;
  location / {
    proxy_pass http://192.168.0.123:2379/dashboard/;
  }
}
```

設定を変更し、変更した設定を有効にするために NGINX を再起動します。

```shell
sudo nginx -s reload
```

</details>

## 次は何ですか {#what-s-next}

ファイアウォールの設定など、TiDB ダッシュボードのセキュリティを強化する方法については、 [セキュリティTiDB ダッシュボード](/dashboard/dashboard-ops-security.md)を参照してください。
