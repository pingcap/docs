---
title: TiProxy Configuration File
summary: TiProxy を構成する方法を学びます。
---

# TiProxyコンフィグレーションファイル {#tiproxy-configuration-file}

このドキュメントでは、 TiProxyの導入と使用に関連する設定パラメータについて説明します。TiUP導入トポロジの設定については、 [tiproxy-servers の設定](/tiup/tiup-cluster-topology-reference.md#tiproxy_servers)参照してください。

以下に構成例を示します。

```toml
[proxy]
addr = "0.0.0.0:6000"
max-connections = 100

[api]
addr = "0.0.0.0:3080"

[ha]
virtual-ip = "10.0.1.10/24"
interface = "eth0"

[security]
[security.cluster-tls]
skip-ca = true

[security.sql-tls]
skip-ca = true
```

## <code>tiproxy.toml</code>ファイルを設定する {#configure-the-code-tiproxy-toml-code-file}

このセクションでは、TiProxy の構成パラメータについて説明します。

> **Tip:**
>
> 設定項目の値を調整する必要がある場合は、 [設定を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。通常、変更を行うと再起動が必要になります。TiProxy はホットリロードをサポートしているため、 `tiup cluster reload --skip-restart`実行することで再起動を省略できます。

### プロキシ {#proxy}

SQL ポートのコンフィグレーション。

#### `addr` {#addr}

-   デフォルト値: `0.0.0.0:6000`
-   ホットリロードのサポート: いいえ
-   SQLサービスのリスニングアドレス。形式は`<ip>:<port>`です。この構成項目は、 TiUPまたはTiDB Operatorを使用してTiProxyをデプロイすると自動的に設定されます。

#### `advertise-addr` {#advertise-addr}

-   デフォルト値: `""`
-   ホットリロードのサポート: いいえ
-   他のコンポーネントがこのTiProxyインスタンスに接続するために使用するアドレスを指定します。このアドレスにはホスト名のみが含まれ、ポート番号は含まれません。このアドレスは[`addr`](#addr)のホスト名とは異なる場合があります。例えば、TiProxyのTLS証明書の`Subject Alternative Name`ドメイン名のみが含まれている場合、他のコンポーネントはIP経由でTiProxyに接続できません。この設定項目は、 TiUPまたはTiDB Operatorを使用してTiProxyをデプロイすると自動的に設定されます。設定されていない場合は、TiProxyインスタンスの外部IPアドレスが使用されます。

#### `graceful-wait-before-shutdown` {#graceful-wait-before-shutdown}

-   デフォルト値: `0`
-   ホットリロードのサポート: はい
-   単位: 秒
-   TiProxyがシャットダウンすると、HTTPステータスは「unhealthy」を返しますが、SQLポートは`graceful-wait-before-shutdown`秒間は新規接続を受け付けます。その後、新規接続は拒否され、クライアントの負荷が増大します。クライアントとTiProxyの間に他のプロキシ（NLBなど）が存在しない場合は、この値を`0`に設定することをお勧めします。

#### `graceful-close-conn-timeout` {#graceful-close-conn-timeout}

-   デフォルト値: `15`
-   ホットリロードのサポート: はい
-   単位: 秒
-   TiProxy がシャットダウンする際、現在のトランザクション（ドレインクライアントとも呼ばれます）が`graceful-close-conn-timeout`秒以内に完了すると、接続が閉じられます。その後、すべての接続が一度に閉じられます。3 `graceful-close-conn-timeout` `graceful-wait-before-shutdown`後に発生します。このタイムアウトは、トランザクションのライフサイクルよりも長く設定することをお勧めします。

#### `max-connections` {#max-connections}

-   デフォルト値: `0`
-   ホットリロードのサポート: はい
-   各 TiProxy インスタンスは最大`max-connections`接続を受け入れることができます。3 `0`制限がないことを意味します。

#### `conn-buffer-size` {#conn-buffer-size}

-   デフォルト値: `32768`
-   ホットリロードのサポート: はい、ただし新規接続のみ
-   範囲: `[1024, 16777216]`
-   この設定項目では、接続バッファのサイズを指定できます。各接続は、読み取りバッファと書き込みバッファをそれぞれ1つずつ使用します。これはメモリとパフォーマンスのトレードオフです。バッファサイズを大きくするとパフォーマンスは向上しますが、メモリ消費量も増加します。1 `0`設定すると、TiProxy はデフォルトのバッファサイズを使用します。

#### `pd-addrs` {#pd-addrs}

-   デフォルト値: `127.0.0.1:2379`
-   ホットリロードのサポート: いいえ
-   TiProxyが接続するPDアドレス。TiProxyはPDからTiDBリストを取得することでTiDBインスタンスを検出します。TiUPまたはTiDB OperatorによってTiProxyがデプロイされると、自動的に設定されます。

#### `proxy-protocol` {#proxy-protocol}

-   デフォルト値: `""`
-   ホットリロードのサポート: はい、ただし新規接続のみ
-   可能な`"v2"` : `""`
-   ポートの[PROXYプロトコル](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)有効にしてください。PROXYプロトコルを有効にすると、TiProxyは実際のクライアントIPアドレスをTiDBに渡すことができます。3 `"v2"` PROXYプロトコルバージョン2の使用を示し、 `""` PROXYプロトコルの無効化を示します。TiProxyでPROXYプロトコルが有効になっている場合は、TiDBサーバーでも[PROXYプロトコル](/tidb-configuration-file.md#proxy-protocol)有効にする必要があります。

### API {#api}

HTTP ゲートウェイの構成。

#### `addr` {#addr}

-   デフォルト値: `0.0.0.0:3080`
-   ホットリロードのサポート: いいえ
-   APIゲートウェイアドレス。1 `ip:port`指定できます。

#### `proxy-protocol` {#proxy-protocol}

-   デフォルト値: `""`
-   ホットリロードのサポート: いいえ
-   可能な`"v2"` : `""`
-   ポートの[PROXYプロトコル](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)有効にします。3 `"v2"` PROXY プロトコル バージョン 2 を使用することを示し、 `""` PROXY プロトコルを無効にすることを示します。

### バランス {#balance}

TiProxy の負荷分散ポリシーの構成。

#### `label-name` {#label-name}

-   デフォルト値: `""`
-   ホットリロードのサポート: はい
-   [ラベルベースの負荷分散](/tiproxy/tiproxy-load-balance.md#label-based-load-balancing)に使用するラベル名を指定します。TiProxy は、このラベル名に基づいて TiDB サーバーのラベル値を照合し、自分と同じラベル値を持つ TiDB サーバーへのルーティング要求を優先します。
-   デフォルト値の`label-name`は空文字列で、ラベルベースの負荷分散が使用されないことを示します。この負荷分散ポリシーを有効にするには、この設定項目を空でない文字列に設定し、TiProxy で[`labels`](#labels) 、TiDB で[`labels`](/tidb-configuration-file.md#labels)の両方を設定する必要があります。詳細については、 [ラベルベースの負荷分散](/tiproxy/tiproxy-load-balance.md#label-based-load-balancing)参照してください。

#### `policy` {#policy}

-   デフォルト値: `resource`
-   ホットリロードのサポート: はい
-   `location` `connection`値: `resource`
-   負荷分散ポリシーを指定します。各値の意味については、 [TiProxy 負荷分散ポリシー](/tiproxy/tiproxy-load-balance.md#configure-load-balancing-policies)参照してください。

### ハ {#ha}

TiProxy の高可用性構成。

#### `virtual-ip` {#virtual-ip}

-   デフォルト値: `""`
-   ホットリロードのサポート: いいえ
-   仮想IPアドレスをCIDR形式（例： `"10.0.1.10/24"` ）で指定します。クラスタ内で複数のTiProxyインスタンスを同じ仮想IPで構成した場合、一度にバインドできるインスタンスは1つだけです。このインスタンスがオフラインになると、別のTiProxyインスタンスが自動的に仮想IPを引き継ぎます。これにより、クライアントは常に仮想IPを介して利用可能なTiProxyに接続できるようになります。

以下に構成例を示します。

```yaml
server_configs:
  tiproxy:
    ha.virtual-ip: "10.0.1.10/24"
    ha.interface: "eth0"
```

TiProxy v1.3.1以降、複数の仮想IPアドレスの設定がサポートされます。コンピューティングレイヤーのリソースを分離する必要がある場合は、複数の仮想IPアドレスを設定し、 [ラベルベースの負荷分散](/tiproxy/tiproxy-load-balance.md#label-based-load-balancing)組み合わせて使用​​できます。設定例については、 [ラベルベースの負荷分散](/tiproxy/tiproxy-load-balance.md#label-based-load-balancing)参照してください。

> **Note:**
>
> -   仮想 IP は Linux オペレーティング システムでのみサポートされます。
> -   TiProxy を実行する Linux ユーザーには、IP アドレスをバインドする権限が必要です。
> -   1 つの TiProxy インスタンスの実際の IP アドレスと仮想 IP アドレスは、同じ CIDR 範囲内にある必要があります。

#### `interface` {#interface}

-   デフォルト値: `""`
-   ホットリロードのサポート: いいえ
-   仮想IPをバインドするネットワークインターフェースを指定します（例： `"eth0"` ）。仮想IPは、 [`ha.virtual-ip`](#virtual-ip)と`ha.interface`両方が設定されている場合にのみTiProxyインスタンスにバインドされます。

### `labels` {#labels}

-   デフォルト値: `{}`
-   ホットリロードのサポート: はい
-   サーバーのラベルを指定します。例： `{ zone = "us-west-1", dc = "dc1" }` 。

### ログ {#log}

#### `level` {#level}

-   デフォルト値: `info`
-   ホットリロードのサポート: はい
-   `info` `error` `panic` `warn` `debug`
-   ログレベルを指定します。レベル`panic`の場合、TiProxyはエラー発生時にpanicになります。

#### `encoder` {#encoder}

-   デフォルト値: `tidb`
-   以下を指定できます:

    -   `tidb` : TiDBで使用されるフォーマット。詳細は[統合ログ形式](https://github.com/tikv/rfcs/blob/master/text/0018-unified-log-format.md)を参照してください。
    -   `json` : 構造化された JSON 形式。
    -   `console` : 人間が読めるログ形式。

### log.ログファイル {#log-log-file}

#### `filename` {#filename}

-   デフォルト値: `""`
-   ホットリロードのサポート: はい
-   ログファイルのパス。空でない値を指定すると、ファイルへのログ記録が有効になります。TiProxy がTiUPと共にデプロイされている場合、ファイル名は自動的に設定されます。

#### `max-size` {#max-size}

-   デフォルト値: `300`
-   ホットリロードのサポート: はい
-   単位: MB
-   ログファイルの最大サイズを指定します。ログファイルのサイズがこの制限を超えると、ログファイルはローテーションされます。

#### `max-days` {#max-days}

-   デフォルト値: `3`
-   ホットリロードのサポート: はい
-   古いログファイルを保存する最大日数を指定します。この期間を過ぎると、古いログファイルは削除されます。

#### `max-backups` {#max-backups}

-   デフォルト値: `3`
-   ホットリロードのサポート: はい
-   保持するログファイルの最大数を指定します。超過したログファイルは自動的に削除されます。

### 安全 {#security}

> **Note:**
>
> TiProxyは1時間に1回、ディスクから証明書を再読み込みします。そのため、ディスク上の証明書ファイルに加えた変更が有効になるまでに最大1時間かかる場合があります。

`[security]`セクションには、名前の異なる TLS オブジェクトが 4 つあります。これらは設定形式とフィールドは同じですが、名前によって解釈が異なります。

```toml
[security]
    [sql-tls]
    skip-ca = true
    [server-tls]
    auto-certs = true
```

すべての TLS オプションはホットリロードされます。

TLS オブジェクト フィールド:

-   `ca` : CAを指定する
-   `cert` : 証明書を指定します
-   `key` : 秘密鍵を指定する
-   `auto-certs` : 主にテストに使用されます。証明書またはキーが指定されていない場合は証明書を生成します。
-   `skip-ca` : クライアント オブジェクト上の CA を使用した証明書の検証をスキップするか、サーバーオブジェクト上のサーバー側の検証をスキップします。
-   `min-tls-version` : 最小のTLSバージョンを設定します。設定可能な値は`1.0` 、 `1.1` 、 `1.2` 、 `1.3`です。デフォルト値は`1.2`で、v1.2以上のTLSバージョンが許可されます。
-   `rsa-key-size` : `auto-certs`が有効な場合の RSA キー サイズを設定します。
-   `autocert-expire-duration` : 自動生成された証明書のデフォルトの有効期限を設定します。

オブジェクトは名前によってクライアント オブジェクトまたはサーバーオブジェクトに分類されます。

クライアント TLS オブジェクトの場合:

-   サーバー証明書の検証をスキップするには、 `ca`または`skip-ca`を設定する必要があります。
-   オプションで、サーバー側のクライアント検証に合格するために`cert`または`key`設定できます。
-   役に立たないフィールド: 自動証明書。

サーバーTLS オブジェクトの場合:

-   TLS接続をサポートするには、 `cert` 、 `key` 、または`auto-certs`のいずれかを設定できます。それ以外の場合、TiProxyはTLS接続をサポートしません。
-   オプションとして、 `ca`空でない場合、サーバー側でのクライアント検証が有効になります。クライアントは証明書を提供する必要があります。また、 `skip-ca`が true かつ`ca`空でない場合、サーバーはクライアントが証明書を提供した場合にのみ検証を行います。

#### `cluster-tls` {#cluster-tls}

クライアントTLSオブジェクト。TiDBまたはPDへのアクセスに使用されます。

#### `require-backend-tls` {#require-backend-tls}

-   デフォルト値: `false`
-   ホットリロードのサポート: はい、ただし新規接続のみ
-   TiProxyとTiDBサーバー間のTLS接続を必須にします。TiDBサーバーがTLSをサポートしていない場合、クライアントはTiProxyへの接続時にエラーを報告します。

#### `sql-tls` {#sql-tls}

クライアントTLSオブジェクト。TiDB SQLポート（4000）へのアクセスに使用されます。

#### `server-tls` {#server-tls}

サーバーTLSオブジェクト。SQLポート（6000）でTLSを提供するために使用されます。

#### `server-http-tls` {#server-http-tls}

サーバーTLSオブジェクト。HTTPステータスポート（3080）でTLSを提供するために使用されます。
