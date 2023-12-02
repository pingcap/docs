---
title: Use TiDB Dashboard behind a Reverse Proxy
---

# リバース プロキシの背後で TiDB ダッシュボードを使用する {#use-tidb-dashboard-behind-a-reverse-proxy}

リバース プロキシを使用すると、TiDB ダッシュボード サービスを内部ネットワークから外部に安全に公開できます。

## 手順 {#procedures}

### ステップ 1: 実際の TiDB ダッシュボード アドレスを取得する {#step-1-get-the-actual-tidb-dashboard-address}

複数の PD インスタンスがクラスターにデプロイされている場合、PD インスタンスのうちの 1 つだけが実際に TiDB ダッシュボードを実行します。したがって、リバース プロキシの上流が正しいアドレスを指していることを確認する必要があります。この仕組みの詳細については、 [複数の PD インスタンスを使用したデプロイメント](/dashboard/dashboard-ops-deploy.md#deployment-with-multiple-pd-instances)を参照してください。

TiUPツールを使用して展開する場合は、次のコマンドを実行して実際の TiDB ダッシュボード アドレスを取得します ( `CLUSTER_NAME`をクラスター名に置き換えます)。

```shell
tiup cluster display CLUSTER_NAME --dashboard
```

出力は実際の TiDB ダッシュボード アドレスです。サンプルは次のとおりです。

```bash
http://192.168.0.123:2379/dashboard/
```

> **注記：**
>
> この機能は、 `tiup cluster`導入ツールの新しいバージョン (v1.0.3 以降) でのみ使用できます。
>
> <details><summary>TiUPクラスタのアップグレード</summary>
>
> ```bash
> tiup update --self
> tiup update cluster --force
> ```
>
> </details>

### ステップ 2: リバース プロキシを構成する {#step-2-configure-the-reverse-proxy}

<details><summary><strong>HAProxy を使用する</strong></summary>

リバース プロキシとして[HAプロキシ](https://www.haproxy.org/)を使用する場合は、次の手順を実行します。

1.  `8033`ポートで TiDB ダッシュボードにリバース プロキシを使用します (たとえば)。 HAProxy 構成ファイルに、次の構成を追加します。

    ```haproxy
    frontend tidb_dashboard_front
      bind *:8033
      use_backend tidb_dashboard_back if { path /dashboard } or { path_beg /dashboard/ }

    backend tidb_dashboard_back
      mode http
      server tidb_dashboard 192.168.0.123:2379
    ```

    `192.168.0.123:2379` [ステップ1](#step-1-get-the-actual-tidb-dashboard-address)で取得した TiDB ダッシュボードの実際のアドレスの IP およびポートに置き換えます。

    > **警告：**
    >
    > **このパス内のサービスのみが**リバース プロキシの背後にあることを保証するには、 `use_backend`ディレクティブの`if`部分を保持する必要があります。そうしないと、セキュリティ上のリスクが発生する可能性があります。 [セキュリティTiDB ダッシュボード](/dashboard/dashboard-ops-security.md)を参照してください。

2.  HAProxy を再起動して、構成を有効にします。

3.  リバース プロキシが有効かどうかをテストします。HAProxy が配置されているマシンの`8033`ポートの`/dashboard/`アドレス ( `http://example.com:8033/dashboard/`など) にアクセスして、TiDB ダッシュボードにアクセスします。

</details>

<details><summary><strong>NGINXを使用する</strong></summary>

リバース プロキシとして[NGINX](https://nginx.org/)を使用する場合は、次の手順を実行します。

1.  `8033`ポートで TiDB ダッシュボードにリバース プロキシを使用します (たとえば)。 NGINX 構成ファイルに、次の構成を追加します。

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
    > このパスの下のサービスのみがリバース プロキシされるようにするには、 `proxy_pass`ディレクティブで`/dashboard/`パスを保持する必要があります。そうしないと、セキュリティ上のリスクが発生します。 [セキュリティTiDB ダッシュボード](/dashboard/dashboard-ops-security.md)を参照してください。

2.  構成を有効にするには、NGINX をリロードします。

    ```shell
    sudo nginx -s reload
    ```

3.  リバース プロキシが有効かどうかをテストします。NGINX が配置されているマシンの`8033`ポートの`/dashboard/`アドレス ( `http://example.com:8033/dashboard/`など) にアクセスして、TiDB ダッシュボードにアクセスします。

</details>

## パスのプレフィックスをカスタマイズする {#customize-path-prefix}

TiDB ダッシュボードは、デフォルトで`http://example.com:8033/dashboard/`などの`/dashboard/`パスでサービスを提供します。これはリバース プロキシの場合でも同様です。 TiDB ダッシュボード サービスに`http://example.com:8033/foo/`や`http://example.com:8033/`などのデフォルト以外のパスを提供するようにリバース プロキシを構成するには、次の手順を実行します。

### ステップ 1: PD 構成を変更して TiDB ダッシュボード サービスのパス プレフィックスを指定する {#step-1-modify-pd-configuration-to-specify-the-path-prefix-of-tidb-dashboard-service}

PD 構成の`[dashboard]`カテゴリの`public-path-prefix`構成項目を変更して、TiDB ダッシュボード サービスのパス プレフィックスを指定します。この項目を変更した後、PD インスタンスを再起動して変更を有効にします。

たとえば、クラスターがTiUPを使用してデプロイされており、サービスを`http://example.com:8033/foo/`で実行する場合は、次の構成を指定できます。

```yaml
server_configs:
  pd:
    dashboard.public-path-prefix: /foo
```

<details><summary><strong>TiUPを使用して新しいクラスターをデプロイするときに構成を変更する</strong></summary>

新しいクラスターを展開する場合は、上記の構成を`topology.yaml` TiUPトポロジ ファイルに追加して、クラスターを展開できます。具体的な手順については、 [TiUP導入ドキュメント](/production-deployment-using-tiup.md#step-3-initialize-cluster-topology-file)を参照してください。

</details>

<details>

<summary><strong>TiUPを使用してデプロイされたクラスターの構成を変更する</strong></summary>

デプロイされたクラスターの場合:

1.  クラスターの構成ファイルを編集モードで開きます ( `CLUSTER_NAME`クラスター名に置き換えます)。

    ```shell
    tiup cluster edit-config CLUSTER_NAME
    ```

2.  `pd`の`server_configs`の設定の下に、設定項目を変更または追加します。 `server_configs`存在しない場合は、最上位に追加します。

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

    変更後の構成ファイルは次のようなファイルになります。

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

3.  変更した構成を有効にするために、すべての PD インスタンスに対してローリング再起動を実行します ( `CLUSTER_NAME`クラスター名に置き換えます)。

    ```shell
    tiup cluster reload CLUSTER_NAME -R pd
    ```

詳細については[一般的なTiUP操作 - 構成の変更](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。

</details>

TiDB ダッシュボード サービスをルート パス ( `http://example.com:8033/`など) で実行する場合は、次の構成を使用します。

```yaml
server_configs:
  pd:
    dashboard.public-path-prefix: /
```

> **警告：**
>
> 変更およびカスタマイズされたパス プレフィックスが有効になると、TiDB ダッシュボードに直接アクセスできなくなります。 TiDB ダッシュボードには、パス プレフィックスと一致するリバース プロキシ経由でのみアクセスできます。

### ステップ 2: リバース プロキシ構成を変更する {#step-2-modify-the-reverse-proxy-configuration}

<details><summary><strong>HAProxy を使用する</strong></summary>

`http://example.com:8033/foo/`例に取ると、対応する HAProxy 構成は次のようになります。

```haproxy
frontend tidb_dashboard_front
  bind *:8033
  use_backend tidb_dashboard_back if { path /foo } or { path_beg /foo/ }

backend tidb_dashboard_back
  mode http
  http-request set-path %[path,regsub(^/foo/?,/dashboard/)]
  server tidb_dashboard 192.168.0.123:2379
```

`192.168.0.123:2379` [ステップ1](#step-1-get-the-actual-tidb-dashboard-address)で取得した TiDB ダッシュボードの実際のアドレスの IP およびポートに置き換えます。

> **警告：**
>
> **このパス内のサービスのみが**リバース プロキシの背後にあることを保証するには、 `use_backend`ディレクティブの`if`部分を保持する必要があります。そうしないと、セキュリティ上のリスクが発生する可能性があります。 [セキュリティTiDB ダッシュボード](/dashboard/dashboard-ops-security.md)を参照してください。

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

構成を変更し、HAProxy を再起動して、変更した構成を有効にします。

</details>

<details><summary><strong>NGINXを使用する</strong></summary>

`http://example.com:8033/foo/`を例として、対応する NGINX 構成は次のとおりです。

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
> **このパス内のサービスのみが**リバース プロキシの背後にあることを保証するには、 `proxy_pass`ディレクティブの`/dashboard/`パスを保持する必要があります。そうしないと、セキュリティ上のリスクが発生する可能性があります。 [セキュリティTiDB ダッシュボード](/dashboard/dashboard-ops-security.md)を参照してください。

TiDB ダッシュボード サービスをルート パス ( `http://example.com:8033/`など) で実行する場合は、次の構成を使用します。

```nginx
server {
  listen 8033;
  location / {
    proxy_pass http://192.168.0.123:2379/dashboard/;
  }
}
```

構成を変更し、NGINX を再起動して、変更した構成を有効にします。

```shell
sudo nginx -s reload
```

</details>

## 次は何ですか {#what-s-next}

ファイアウォールの構成など、TiDB ダッシュボードのセキュリティを強化する方法については、 [セキュリティTiDB ダッシュボード](/dashboard/dashboard-ops-security.md)を参照してください。
