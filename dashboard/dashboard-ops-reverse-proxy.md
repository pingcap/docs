---
title: Use TiDB Dashboard behind a Reverse Proxy
summary: TiDBダッシュボードは、リバースプロキシを使用して安全に公開できます。これを行うには、TiDBダッシュボードの実際のアドレスを取得し、HAProxyまたはNGINXを使用してリバースプロキシを設定します。TiDBダッシュボードサービスのパスプレフィックスをカスタマイズすることもできます。セキュリティを強化するには、ファイアウォールの設定を検討してください。
---

# リバースプロキシの背後でTiDBダッシュボードを使用する {#use-tidb-dashboard-behind-a-reverse-proxy}

リバース プロキシを使用すると、TiDB ダッシュボード サービスを内部ネットワークから外部に安全に公開できます。

## 手順 {#procedures}

### ステップ1: 実際のTiDBダッシュボードのアドレスを取得する {#step-1-get-the-actual-tidb-dashboard-address}

クラスター内に複数のPDインスタンスがデプロイされている場合、TiDBダッシュボードを実際に実行するのは1つのPDインスタンスのみです。そのため、リバースプロキシのアップストリームが正しいアドレスを指していることを確認する必要があります。このメカニズムの詳細については、 [複数のPDインスタンスを使用したデプロイメント](/dashboard/dashboard-ops-deploy.md#deployment-with-multiple-pd-instances)参照してください。

デプロイメントにTiUPツールを使用する場合は、次のコマンドを実行して実際の TiDB ダッシュボード アドレスを取得します ( `CLUSTER_NAME`クラスター名に置き換えます)。

```shell
tiup cluster display CLUSTER_NAME --dashboard
```

出力は実際のTiDBダッシュボードのアドレスです。例を以下に示します。

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

1.  例えば、TiDBダッシュボードのリバースプロキシを`8033`ポート（例）で使用します。HAProxy設定ファイルに以下の設定を追加します。

    ```haproxy
    frontend tidb_dashboard_front
      bind *:8033
      use_backend tidb_dashboard_back if { path /dashboard } or { path_beg /dashboard/ }

    backend tidb_dashboard_back
      mode http
      server tidb_dashboard 192.168.0.123:2379
    ```

    `192.168.0.123:2379` 、 [ステップ1](#step-1-get-the-actual-tidb-dashboard-address)で取得した TiDB ダッシュボードの実際のアドレスの IP とポートに置き換えます。

    > **警告：**
    >
    > **このパス内のサービスのみが**リバースプロキシの背後にあることを保証するには、 `use_backend`ディレクティブの`if`部分を保持する必要があります。そうしないと、セキュリティリスクが発生する可能性があります。7 [セキュリティTiDBダッシュボード](/dashboard/dashboard-ops-security.md)参照してください。

2.  設定を有効にするには、HAProxy を再起動します。

3.  リバース プロキシが有効かどうかをテストします。HAProxy が配置されているマシンの`8033`ポートの`/dashboard/`アドレス ( `http://example.com:8033/dashboard/`など) にアクセスして、TiDB ダッシュボードにアクセスします。

</details>

<details><summary><strong>NGINXを使用する</strong></summary>

[NGINX](https://nginx.org/)リバース プロキシとして使用する場合は、次の手順を実行します。

1.  TiDBダッシュボードのリバースプロキシを`8033`ポート（例）で使用します。NGINX設定ファイルに以下の設定を追加します。

    ```nginx
    server {
        listen 8033;
        location /dashboard/ {
        proxy_pass http://192.168.0.123:2379/dashboard/;
        }
    }
    ```

    `http://192.168.0.123:2379/dashboard/` 、 [ステップ1](#step-1-get-the-actual-tidb-dashboard-address)で取得した TiDB ダッシュボードの実際のアドレスに置き換えます。

    > **警告：**
    >
    > `proxy_pass`ディレクティブの`/dashboard/`パスは必ず保持してください。これにより、このパスの下にあるサービスのみがリバースプロキシされます。そうしないと、セキュリティリスクが発生します。5 [セキュリティTiDBダッシュボード](/dashboard/dashboard-ops-security.md)参照してください。

2.  設定を有効にするには、NGINX をリロードします。

    ```shell
    sudo nginx -s reload
    ```

3.  リバース プロキシが有効かどうかをテストします。NGINX が配置されているマシンの`8033`ポートの`/dashboard/`アドレス ( `http://example.com:8033/dashboard/`など) にアクセスして、TiDB ダッシュボードにアクセスします。

</details>

## パスプレフィックスをカスタマイズする {#customize-path-prefix}

TiDBダッシュボードは、デフォルトで`/dashboard/`パス（例えば`http://example.com:8033/dashboard/` ）でサービスを提供します。これはリバースプロキシでも同様です。リバースプロキシを設定して、TiDBダッシュボードサービスにデフォルト以外のパス（例えば`http://example.com:8033/foo/`や`http://example.com:8033/` ）を提供するには、以下の手順を実行してください。

### ステップ1: PD構成を変更して、TiDBダッシュボードサービスのパスプレフィックスを指定します。 {#step-1-modify-pd-configuration-to-specify-the-path-prefix-of-tidb-dashboard-service}

PD設定の`[dashboard]`のカテゴリにある`public-path-prefix`設定項目を変更し、TiDBダッシュボードサービスのパスプレフィックスを指定します。この項目を変更した後、変更を有効にするにはPDインスタンスを再起動してください。

たとえば、クラスターがTiUPを使用してデプロイされており、サービスを`http://example.com:8033/foo/`で実行する場合は、次の構成を指定できます。

```yaml
server_configs:
  pd:
    dashboard.public-path-prefix: /foo
```

<details><summary><strong>TiUPを使用して新しいクラスターを展開するときに構成を変更する</strong></summary>

新しいクラスタをデプロイする場合は、上記の設定を`topology.yaml` TiUPトポロジファイルに追加してクラスタをデプロイできます。具体的な手順については、 [TiUP展開ドキュメント](/production-deployment-using-tiup.md#step-3-initialize-the-cluster-topology-file)参照してください。

</details>

<details>

<summary><strong>TiUPを使用してデプロイされたクラスターの構成を変更する</strong></summary>

デプロイされたクラスターの場合:

1.  クラスターの構成ファイルを編集モードで開きます ( `CLUSTER_NAME`クラスター名に置き換えます)。

    ```shell
    tiup cluster edit-config CLUSTER_NAME
    ```

2.  `server_configs`の`pd`設定の下にある設定項目を変更または追加します。5 `server_configs`存在しない場合は、最上位レベルに追加します。

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

    変更後の構成ファイルは次のファイルのようになります。

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
> 変更およびカスタマイズされたパスプレフィックスが有効になると、TiDBダッシュボードに直接アクセスできなくなります。TiDBダッシュボードにアクセスするには、パスプレフィックスに一致するリバースプロキシを経由する必要があります。

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

`192.168.0.123:2379` 、 [ステップ1](#step-1-get-the-actual-tidb-dashboard-address)で取得した TiDB ダッシュボードの実際のアドレスの IP とポートに置き換えます。

> **警告：**
>
> **このパス内のサービスのみが**リバースプロキシの背後にあることを保証するには、 `use_backend`ディレクティブの`if`部分を保持する必要があります。そうしないと、セキュリティリスクが発生する可能性があります。7 [セキュリティTiDBダッシュボード](/dashboard/dashboard-ops-security.md)参照してください。

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

`http://192.168.0.123:2379/dashboard/` 、 [ステップ1](#step-1-get-the-actual-tidb-dashboard-address)で取得した TiDB ダッシュボードの実際のアドレスに置き換えます。

> **警告：**
>
> `proxy_pass`ディレクティブの`/dashboard/`パスは必ず保持し**、このパス内のサービスのみが**リバースプロキシの背後にあるようにする必要があります。そうしないと、セキュリティリスクが発生する可能性があります。7 [セキュリティTiDBダッシュボード](/dashboard/dashboard-ops-security.md)参照してください。

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

## 次は何？ {#what-s-next}

ファイアウォールの設定など、TiDB ダッシュボードのセキュリティを強化する方法については、 [セキュリティTiDBダッシュボード](/dashboard/dashboard-ops-security.md)参照してください。
