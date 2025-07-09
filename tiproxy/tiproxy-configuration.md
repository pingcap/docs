---
title: TiProxy Configuration File
summary: TiProxy を構成する方法を学びます。
---

# TiProxyコンフィグレーションファイル {#tiproxy-configuration-file}

このドキュメントでは、TiProxy の導入と使用に関連する設定パラメータについて説明します。設定例を以下に示します。

```toml
[proxy]
addr = "0.0.0.0:6000"
max-connections = 100

[api]
addr = "0.0.0.0:3080"

[log]
level = "info"

[security]
[security.cluster-tls]
skip-ca = true

[security.sql-tls]
skip-ca = true
```

## <code>tiproxy.toml</code>ファイルを設定する {#configure-the-code-tiproxy-toml-code-file}

このセクションでは、TiProxy の構成パラメータについて説明します。

> **ヒント：**
>
> 設定項目の値を調整する必要がある場合は、 [設定を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。通常、変更を行うと再起動が必要になります。TiProxy はホットリロードをサポートしているため、 `tiup cluster reload --skip-restart`実行することで再起動を省略できます。

### プロキシ {#proxy}

SQL ポートのコンフィグレーション。

#### <code>addr</code> {#code-addr-code}

-   デフォルト値: `0.0.0.0:6000`
-   ホットリロードのサポート: いいえ
-   SQLゲートウェイアドレス。形式は`<ip>:<port>`です。

#### <code>graceful-wait-before-shutdown</code> {#code-graceful-wait-before-shutdown-code}

-   デフォルト値: `0`
-   ホットリロードのサポート: はい
-   単位：秒
-   TiProxyがシャットダウンすると、HTTPステータスは「unhealthy」に戻りますが、SQLポートは`graceful-wait-before-shutdown`秒間は新規接続を受け付けます。その後、新規接続は拒否され、クライアントの負荷が増大します。クライアントとTiProxyの間に他のプロキシ（NLBなど）が存在しない場合は、この値を`0`に設定することをお勧めします。

#### <code>graceful-close-conn-timeout</code> {#code-graceful-close-conn-timeout-code}

-   デフォルト値: `15`
-   ホットリロードのサポート: はい
-   単位：秒
-   TiProxy がシャットダウンする際、現在のトランザクション（ドレインクライアントとも呼ばれます）が`graceful-close-conn-timeout`秒以内に完了すると、接続が閉じられます。その後、すべての接続が一度に閉じられます。3 `graceful-close-conn-timeout` `graceful-wait-before-shutdown`後に発生します。このタイムアウトは、トランザクションのライフサイクルよりも長く設定することをお勧めします。

#### <code>max-connections</code> {#code-max-connections-code}

-   デフォルト値: `0`
-   ホットリロードのサポート: はい
-   各 TiProxy インスタンスは最大`max-connections`接続を受け入れることができます。3 `0`制限がないことを意味します。

#### <code>conn-buffer-size</code> {#code-conn-buffer-size-code}

-   デフォルト値: `32768`
-   ホットリロードのサポート: はい、ただし新規接続のみ
-   範囲: `[1024, 16777216]`
-   この設定項目では、接続バッファサイズを指定できます。各接続は、読み取りバッファと書き込みバッファをそれぞれ`0`使用します。これはメモリとパフォーマンスのトレードオフです。バッファサイズを大きくするとパフォーマンスは向上しますが、メモリ消費量も増加します。1 に設定すると、TiProxy はデフォルトのバッファサイズを使用します。

#### <code>pd-addrs</code> {#code-pd-addrs-code}

-   デフォルト値: `127.0.0.1:2379`
-   ホットリロードのサポート: いいえ
-   TiProxyが接続するPDアドレス。TiProxyはPDからTiDBリストを取得することでTiDBインスタンスを検出します。TiUPまたはTiUP TiDB OperatorによってTiProxyがデプロイされると、自動的に設定されます。

#### <code>proxy-protocol</code> {#code-proxy-protocol-code}

-   デフォルト値: `""`
-   ホットリロードのサポート: はい、ただし新規接続のみ
-   可能`"v2"`値: `""`
-   ポートの[PROXYプロトコル](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)有効にしてください。PROXYプロトコルを有効にすると、TiProxyは実際のクライアントIPアドレスをTiDBに渡すことができます。3 `"v2"` PROXYプロトコルバージョン2の使用を示し、 `""` PROXYプロトコルの無効化を示します。TiProxyでPROXYプロトコルが有効になっている場合は、TiDBサーバーでも[PROXYプロトコル](/tidb-configuration-file.md#proxy-protocol)有効にする必要があります。

### API {#api}

HTTP ゲートウェイの構成。

#### <code>addr</code> {#code-addr-code}

-   デフォルト値: `0.0.0.0:3080`
-   ホットリロードのサポート: いいえ
-   APIゲートウェイアドレス。1 `ip:port`指定できます。

#### <code>proxy-protocol</code> {#code-proxy-protocol-code}

-   デフォルト値: `""`
-   ホットリロードのサポート: いいえ
-   可能`"v2"`値: `""`
-   ポートの[PROXYプロトコル](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)有効にします。3 `"v2"` PROXY プロトコル バージョン 2 を使用することを示し、 `""` PROXY プロトコルを無効にすることを示します。

### ログ {#log}

#### <code>level</code> {#code-level-code}

-   デフォルト値: `info`
-   ホットリロードのサポート: はい
-   `warn` `panic` `info` `error` `debug`
-   ログレベルを指定します。レベル`panic`の場合、エラー発生時にTiProxyはpanicになります。

#### <code>encoder</code> {#code-encoder-code}

-   デフォルト値: `tidb`
-   以下を指定できます:

    -   `tidb` : TiDBで使用されるフォーマット。詳細は[統合ログ形式](https://github.com/tikv/rfcs/blob/master/text/0018-unified-log-format.md)を参照してください。
    -   `json` : 構造化された JSON 形式。
    -   `console` : 人間が読めるログ形式。

### log.ログファイル {#log-log-file}

#### <code>filename</code> {#code-filename-code}

-   デフォルト値: `""`
-   ホットリロードのサポート: はい
-   ログファイルのパス。空でない値を指定すると、ファイルへのログ記録が有効になります。TiProxy がTiUPと共にデプロイされている場合、ファイル名は自動的に設定されます。

#### <code>max-size</code> {#code-max-size-code}

-   デフォルト値: `300`
-   ホットリロードのサポート: はい
-   単位: MB
-   ログファイルの最大サイズを指定します。ログファイルのサイズがこの制限を超えると、ログファイルはローテーションされます。

#### <code>max-days</code> {#code-max-days-code}

-   デフォルト値: `3`
-   ホットリロードのサポート: はい
-   古いログファイルを保存する最大日数を指定します。この期間を過ぎると、古いログファイルは削除されます。

#### <code>max-backups</code> {#code-max-backups-code}

-   デフォルト値: `3`
-   ホットリロードのサポート: はい
-   保持するログファイルの最大数を指定します。超過数に達した場合、余分なログファイルは自動的に削除されます。

### 安全 {#security}

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
-   `cert` : 証明書を指定する
-   `key` : 秘密鍵を指定する
-   `auto-certs` : 主にテストに使用されます。証明書またはキーが指定されていない場合は証明書を生成します。
-   `skip-ca` : クライアント オブジェクト上の CA を使用した証明書の検証をスキップするか、サーバーオブジェクト上のサーバー側検証をスキップします。
-   `min-tls-version` : 最小のTLSバージョンを設定します。指定可能な値は`1.0` 、 `1.1` 、 `1.2` 、 `1.3`です。デフォルト値は`1.2`で、v1.2以上のTLSバージョンが許可されます。
-   `rsa-key-size` : `auto-certs`が有効な場合の RSA キー サイズを設定します。
-   `autocert-expire-duration` : 自動生成された証明書のデフォルトの有効期限を設定します。

オブジェクトは、名前によってクライアント オブジェクトまたはサーバーオブジェクトに分類されます。

クライアント TLS オブジェクトの場合:

-   サーバー証明書の検証をスキップするには、 `ca`または`skip-ca`設定する必要があります。
-   オプションで、サーバー側のクライアント検証に合格するために`cert`または`key`設定できます。
-   役に立たないフィールド: 自動証明書。

サーバーTLS オブジェクトの場合:

-   TLS接続をサポートするには、 `cert` 、または`auto-certs` `key`かを設定できます。それ以外の場合、TiProxyはTLS接続をサポートしません。
-   オプションとして、 `ca`空でない場合、サーバー側でのクライアント検証が有効になります。クライアントは証明書を提供する必要があります。また、 `skip-ca`真で`ca`空でない場合、サーバーが証明書を提供した場合にのみクライアント証明書を検証します。

#### <code>cluster-tls</code> {#code-cluster-tls-code}

クライアントTLSオブジェクト。TiDBまたはPDへのアクセスに使用されます。

#### <code>require-backend-tls</code> {#code-require-backend-tls-code}

-   デフォルト値: `false`
-   ホットリロードのサポート: はい、ただし新規接続のみ
-   TiProxyとTiDBサーバー間のTLS接続を必須にします。TiDBサーバーがTLSをサポートしていない場合、クライアントはTiProxyへの接続時にエラーを報告します。

#### <code>sql-tls</code> {#code-sql-tls-code}

クライアントTLSオブジェクト。TiDB TiDB SQLポート（4000）へのアクセスに使用されます。

#### <code>server-tls</code> {#code-server-tls-code}

サーバーTLSオブジェクト。SQLポート（6000）でTLSを提供するために使用されます。

#### <code>server-http-tls</code> {#code-server-http-tls-code}

サーバーTLSオブジェクト。HTTPステータスポート（3080）でTLSを提供するために使用されます。
