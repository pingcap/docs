---
title: TiProxy Configuration File
summary: TiProxy を構成する方法を学習します。
---

# TiProxyコンフィグレーションファイル {#tiproxy-configuration-file}

このドキュメントでは、TiProxy の導入と使用に関連する構成パラメータについて説明します。次に構成例を示します。

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
> 設定項目の値を調整する必要がある場合は、 [設定を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。通常、変更すると再起動が必要になります。TiProxy はホットリロードをサポートしているため、 `tiup cluster reload --skip-restart`実行することで再起動をスキップできます。

### プロキシ {#proxy}

SQL ポートのコンフィグレーション。

#### <code>addr</code> {#code-addr-code}

-   デフォルト値: `0.0.0.0:6000`
-   ホットリロードのサポート: いいえ
-   SQL ゲートウェイ アドレス。形式は`<ip>:<port>`です。

#### <code>graceful-wait-before-shutdown</code> {#code-graceful-wait-before-shutdown-code}

-   デフォルト値: `0`
-   ホットリロードのサポート: はい
-   単位: 秒
-   TiProxy がシャットダウンすると、HTTP ステータスは異常を返しますが、SQL ポートは`graceful-wait-before-shutdown`秒間新しい接続を受け入れ続けます。その後、新しい接続は拒否され、クライアントがドレインされます。クライアントと TiProxy の間に他のプロキシ (NLB など) がない場合は、 `0`に設定することをお勧めします。

#### <code>graceful-close-conn-timeout</code> {#code-graceful-close-conn-timeout-code}

-   デフォルト値: `15`
-   ホットリロードのサポート: はい
-   単位: 秒
-   TiProxy がシャットダウンすると、現在のトランザクション (クライアントのドレインとも呼ばれます) が`graceful-close-conn-timeout`秒以内に完了すると、接続が閉じられます。その後、すべての接続が一度に閉じられます。3 `graceful-close-conn-timeout` `graceful-wait-before-shutdown`後に発生します。このタイムアウトは、トランザクションのライフサイクルよりも長く設定することをお勧めします。

#### <code>max-connections</code> {#code-max-connections-code}

-   デフォルト値: `0`
-   ホットリロードのサポート: はい
-   各 TiProxy インスタンスは最大`max-connections`接続を受け入れることができます。3 `0`制限がないことを意味します。

#### <code>conn-buffer-size</code> {#code-conn-buffer-size-code}

-   デフォルト値: `32768`
-   ホットリロードのサポート: はい、ただし新規接続のみ
-   範囲: `[1024, 16777216]`
-   この構成項目では、接続バッファ サイズを決定できます。各接続では、読み取りバッファ 1 つと書き込みバッファ`0`つが使用されます。これは、メモリとパフォーマンスのトレードオフです。バッファが大きいほどパフォーマンスは向上しますが、メモリの消費量も多くなります。1 の場合、TiProxy はデフォルトのバッファ サイズを使用します。

#### <code>pd-addrs</code> {#code-pd-addrs-code}

-   デフォルト値: `127.0.0.1:2379`
-   ホットリロードのサポート: いいえ
-   TiProxy が接続する PD アドレス。TiProxy は、PD から TiDB リストを取得して TiDB インスタンスを検出します。TiProxy がTiUPまたはTiDB Operatorによってデプロイされると、自動的に設定されます。

#### <code>proxy-protocol</code> {#code-proxy-protocol-code}

-   デフォルト値: `""`
-   ホットリロードのサポート: はい、ただし新規接続のみ
-   可能な値: `""` 、 `"v2"`
-   ポートの[PROXYプロトコル](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)有効にします。PROXY プロトコルを有効にすると、TiProxy は実際のクライアント IP アドレスを TiDB に渡すことができます。3 `"v2"` PROXY プロトコル バージョン 2 を使用することを示し、 `""` PROXY プロトコルを無効にすることを示します。TiProxy で PROXY プロトコルが有効になっている場合は、TiDBサーバーで[PROXYプロトコル](/tidb-configuration-file.md#proxy-protocol)も有効にする必要があります。

### アピ {#api}

HTTP ゲートウェイの構成。

#### <code>addr</code> {#code-addr-code}

-   デフォルト値: `0.0.0.0:3080`
-   ホットリロードのサポート: いいえ
-   API ゲートウェイ アドレス。1 `ip:port`指定できます。

#### <code>proxy-protocol</code> {#code-proxy-protocol-code}

-   デフォルト値: `""`
-   ホットリロードのサポート: いいえ
-   可能な値: `""` 、 `"v2"`
-   ポートの[PROXYプロトコル](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)有効にします。3 `"v2"` PROXY プロトコル バージョン 2 を使用することを示し、 `""` PROXY プロトコルを無効にすることを示します。

### ログ {#log}

#### <code>level</code> {#code-level-code}

-   デフォルト値: `info`
-   ホットリロードのサポート: はい
-   `panic` `warn` `info` `error` `debug`
-   ログ レベルを指定します。レベル`panic`の場合、エラーが発生すると TiProxy はpanicになります。

#### <code>encoder</code> {#code-encoder-code}

-   デフォルト値: `tidb`
-   以下を指定できます:

    -   `tidb` : TiDBで使用される形式。詳細については[統合ログ形式](https://github.com/tikv/rfcs/blob/master/text/0018-unified-log-format.md)を参照してください。
    -   `json` : 構造化された JSON 形式。
    -   `console` : 人間が読めるログ形式。

### log.ログファイル {#log-log-file}

#### <code>filename</code> {#code-filename-code}

-   デフォルト値: `""`
-   ホットリロードのサポート: はい
-   ログ ファイル パス。空でない値を指定すると、ファイルへのログ記録が有効になります。TiProxy がTiUPとともに展開されると、ファイル名は自動的に設定されます。

#### <code>max-size</code> {#code-max-size-code}

-   デフォルト値: `300`
-   ホットリロードのサポート: はい
-   単位: MB
-   ログ ファイルの最大サイズを指定します。ログ ファイルのサイズがこの制限を超えると、ログ ファイルはローテーションされます。

#### <code>max-days</code> {#code-max-days-code}

-   デフォルト値: `3`
-   ホットリロードのサポート: はい
-   古いログ ファイルを保持する最大日数を指定します。この期間を過ぎると、古いログ ファイルは削除されます。

#### <code>max-backups</code> {#code-max-backups-code}

-   デフォルト値: `3`
-   ホットリロードのサポート: はい
-   保持するログ ファイルの最大数を指定します。 超過数に達すると、余分なログ ファイルは自動的に削除されます。

### 安全 {#security}

`[security]`セクションには、名前の異なる TLS オブジェクトが 4 つあります。これらは同じ構成形式とフィールドを共有していますが、名前に応じて解釈が異なります。

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
-   `min-tls-version` : 最小の TLS バージョンを設定します。可能な値は`1.0` 、 `1.1` 、 `1.2` 、および`1.3`です。デフォルト値は`1.2`で、v1.2 以上の TLS バージョンが許可されます。
-   `rsa-key-size` : `auto-certs`が有効な場合に RSA キー サイズを設定します。
-   `autocert-expire-duration` : 自動生成された証明書のデフォルトの有効期限を設定します。

オブジェクトは名前によってクライアント オブジェクトまたはサーバーオブジェクトに分類されます。

クライアント TLS オブジェクトの場合:

-   サーバー証明書の検証をスキップするには、 `ca`または`skip-ca`設定する必要があります。
-   オプションで、サーバー側のクライアント検証に合格するために`cert`または`key`設定できます。
-   役に立たないフィールド: 自動証明書。

サーバーTLS オブジェクトの場合:

-   TLS 接続をサポートするには、 `cert` 、または`key` `auto-certs`いずれかを設定できます。それ以外の場合、TiProxy は TLS 接続をサポートしません。
-   オプションとして、 `ca`が空でない場合、サーバー側のクライアント検証が有効になります。クライアントは証明書を提供する必要があります。または、 `skip-ca`が true で`ca`が空でない場合、サーバーはクライアント証明書が提供された場合にのみクライアント証明書を検証します。

#### <code>cluster-tls</code> {#code-cluster-tls-code}

クライアント TLS オブジェクト。TiDB または PD にアクセスするために使用されます。

#### <code>require-backend-tls</code> {#code-require-backend-tls-code}

-   デフォルト値: `false`
-   ホットリロードのサポート: はい、ただし新規接続のみ
-   TiProxy と TiDB サーバー間の TLS が必要です。TiDBサーバーがTLS をサポートしていない場合、クライアントは TiProxy に接続するときにエラーを報告します。

#### <code>sql-tls</code> {#code-sql-tls-code}

クライアント TLS オブジェクト。TiDB TiDB SQLポート (4000) にアクセスするために使用されます。

#### <code>server-tls</code> {#code-server-tls-code}

サーバーTLS オブジェクト。SQL ポート (6000) で TLS を提供するために使用されます。

#### <code>server-http-tls</code> {#code-server-http-tls-code}

サーバーTLS オブジェクト。HTTP ステータス ポート (3080) で TLS を提供するために使用されます。
