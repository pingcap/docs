---
title: Enable TLS Between TiDB Components
summary: TiDB コンポーネント間の TLS 認証を有効にする方法を学習します。
---

# TiDB コンポーネント間の TLS を有効にする {#enable-tls-between-tidb-components}

このドキュメントでは、TiDBクラスタ内のコンポーネント間で暗号化されたデータ転送を有効にする方法について説明します。有効にすると、以下のコンポーネント間で暗号化された転送が使用されます。

-   TiDB、TiKV、PD、 TiFlash間の通信
-   TiDB コントロールと TiDB、 TiKV Controlと TiKV、 PD Controlと PD
-   各 TiDB、TiKV、PD、およびTiFlashクラスタ内の内部通信

現在、特定のコンポーネントの暗号化された送信のみを有効にすることはサポートされていません。

## 暗号化されたデータ転送を設定して有効にする {#configure-and-enable-encrypted-data-transmission}

1.  証明書を準備します。

    TiDB、TiKV、PD それぞれにサーバー証明書を用意することをお勧めします。これらのコンポーネントが相互に認証できることを確認してください。TiDB、TiKV、PD の制御ツールは、1 つのクライアント証明書を共有することもできます。

    自己署名証明書を生成するには`easy-rsa` `openssl` `cfssl`ツールを使用できます。

    <CustomContent platform="tidb">

    `openssl`選択した場合は[自己署名証明書の生成](/generate-self-signed-certificates.md)を参照できます。

    </CustomContent>

    <CustomContent platform="tidb-cloud">

    `openssl`選択した場合は[自己署名証明書の生成](https://docs.pingcap.com/tidb/stable/generate-self-signed-certificates)を参照できます。

    </CustomContent>

2.  証明書を構成します。

    TiDB コンポーネント間の相互認証を有効にするには、TiDB、TiKV、PD の証明書を次のように構成します。

    -   ティドブ

        設定ファイルまたはコマンドライン引数で設定します。

        ```toml
        [security]
        # Path of the file that contains list of trusted SSL CAs for connection with cluster components.
        cluster-ssl-ca = "/path/to/ca.pem"
        # Path of the file that contains X509 certificate in PEM format for connection with cluster components.
        cluster-ssl-cert = "/path/to/tidb-server.pem"
        # Path of the file that contains X509 key in PEM format for connection with cluster components.
        cluster-ssl-key = "/path/to/tidb-server-key.pem"
        ```

    -   ティクブ

        設定ファイルまたはコマンドライン引数で設定し、対応する URL を`https`に設定します。

        ```toml
        [security]
        ## The path for certificates. An empty string means that secure connections are disabled.
        # Path of the file that contains a list of trusted SSL CAs. If it is set, the following settings `cert_path` and `key_path` are also needed.
        ca-path = "/path/to/ca.pem"
        # Path of the file that contains X509 certificate in PEM format.
        cert-path = "/path/to/tikv-server.pem"
        # Path of the file that contains X509 key in PEM format.
        key-path = "/path/to/tikv-server-key.pem"
        ```

    -   PD

        設定ファイルまたはコマンドライン引数で設定し、対応する URL を`https`に設定します。

        ```toml
        [security]
        ## The path for certificates. An empty string means that secure connections are disabled.
        # Path of the file that contains a list of trusted SSL CAs. If it is set, the following settings `cert_path` and `key_path` are also needed.
        cacert-path = "/path/to/ca.pem"
        # Path of the file that contains X509 certificate in PEM format.
        cert-path = "/path/to/pd-server.pem"
        # Path of the file that contains X509 key in PEM format.
        key-path = "/path/to/pd-server-key.pem"
        ```

    -   TiFlash (v4.0.5 の新機能)

        `tiflash.toml`ファイルで設定します。

        ```toml
        [security]
        ## The path for certificates. An empty string means that secure connections are disabled.
        # Path of the file that contains a list of trusted SSL CAs. If it is set, the following settings `cert_path` and `key_path` are also needed.
        ca_path = "/path/to/ca.pem"
        # Path of the file that contains X509 certificate in PEM format.
        cert_path = "/path/to/tiflash-server.pem"
        # Path of the file that contains X509 key in PEM format.
        key_path = "/path/to/tiflash-server-key.pem"
        ```

        `tiflash-learner.toml`ファイルで設定します。

        ```toml
        [security]
        # Path of the file that contains a list of trusted SSL CAs. If it is set, the following settings `cert_path` and `key_path` are also needed.
        ca-path = "/path/to/ca.pem"
        # Path of the file that contains X509 certificate in PEM format.
        cert-path = "/path/to/tiflash-server.pem"
        # Path of the file that contains X509 key in PEM format.
        key-path = "/path/to/tiflash-server-key.pem"
        ```

    -   TiCDC

        設定ファイルで設定します。

        ```toml
        [security]
        ca-path = "/path/to/ca.pem"
        cert-path = "/path/to/cdc-server.pem"
        key-path = "/path/to/cdc-server-key.pem"
        ```

        あるいは、コマンドライン引数で設定し、対応する URL を`https`に設定します。

        ```bash
        cdc server --pd=https://127.0.0.1:2379 --log-file=ticdc.log --addr=0.0.0.0:8301 --advertise-addr=127.0.0.1:8301 --ca=/path/to/ca.pem --cert=/path/to/ticdc-cert.pem --key=/path/to/ticdc-key.pem
        ```

        これで、TiDB コンポーネント間の暗号化された送信が有効になります。

    > **注記：**
    >
    > TiDB クラスターで暗号化転送を有効にした後、tidb-ctl、tikv-ctl、または pd-ctl を使用してクラスターに接続する必要がある場合は、クライアント証明書を指定します。例:

    ```bash
    ./tidb-ctl -u https://127.0.0.1:10080 --ca /path/to/ca.pem --ssl-cert /path/to/client.pem --ssl-key /path/to/client-key.pem
    ```

    ```bash
    tiup ctl:v<CLUSTER_VERSION> pd -u https://127.0.0.1:2379 --cacert /path/to/ca.pem --cert /path/to/client.pem --key /path/to/client-key.pem
    ```

    ```bash
    ./tikv-ctl --host="127.0.0.1:20160" --ca-path="/path/to/ca.pem" --cert-path="/path/to/client.pem" --key-path="/path/to/clinet-key.pem"
    ```

### コンポーネント呼び出し元のIDを確認する {#verify-component-caller-s-identity}

一般的に、呼び出し先は、呼び出し元が提供する鍵、証明書、およびCAを検証するだけでなく、 `Common Name`を使用して呼び出し元のIDを検証する必要があります。例えば、TiKVはTiDBのみがアクセスでき、他の訪問者は正当な証明書を持っていてもブロックされます。

コンポーネントの呼び出し元の ID を確認するには、証明書を生成するときに証明書のユーザー ID を`Common Name`でマークし、呼び出し先に`cluster-verify-cn` (TiDB の場合) または`cert-allowed-cn` (その他のコンポーネントの場合) を設定して呼び出し元の ID を確認する必要があります。

> **注記：**
>
> -   v8.4.0以降、PD構成項目`cert-allowed-cn`複数の値をサポートします。必要に応じて、TiDB用構成項目`cluster-verify-cn`とその他のコンポーネント用構成項目`cert-allowed-cn`に、複数の`Common Name`設定できます。TiUPはコンポーネントのステータスを照会する際に別の識別子を使用することに注意してください。例えば、クラスター名が`test`の場合、 TiUPは`Common Name`として`test-client`使用します。
> -   v8.3.0以前のバージョンでは、PD設定項目`cert-allowed-cn`には単一の値しか設定できません。そのため、すべての認証オブジェクトの`Common Name`同じ値に設定する必要があります。関連する設定例については、 [v8.3.0 ドキュメント](https://docs-archive.pingcap.com/tidb/v8.3/enable-tls-between-components/)参照してください。

-   ティドブ

    設定ファイルまたはコマンドライン引数で設定します。

    ```toml
    [security]
    cluster-verify-cn = ["tidb", "test-client", "prometheus"]
    ```

-   ティクブ

    設定ファイルまたはコマンドライン引数で設定します。

    ```toml
    [security]
    cert-allowed-cn = ["tidb", "pd", "tikv", "tiflash", "prometheus"]
    ```

-   PD

    設定ファイルまたはコマンドライン引数で設定します。

    ```toml
    [security]
    cert-allowed-cn = ["tidb", "pd", "tikv", "tiflash", "test-client", "prometheus"]
    ```

-   TiFlash (v4.0.5 の新機能)

    `tiflash.toml`ファイルまたはコマンドライン引数で設定します。

    ```toml
    [security]
    cert_allowed_cn = ["tidb", "tikv", "prometheus"]
    ```

    `tiflash-learner.toml`ファイルで設定します。

    ```toml
    [security]
    cert-allowed-cn = ["tidb", "tikv", "tiflash", "prometheus"]
    ```

## TiDBコンポーネント間のTLSを検証する {#validate-tls-between-tidb-components}

TiDBコンポーネント間の通信にTLSを設定したら、以下のコマンドを使用してTLSが正常に有効化されたことを確認できます。これらのコマンドは、各コンポーネントの証明書とTLSハンドシェイクの詳細を出力します。

-   ティドブ

    ```sh
    openssl s_client -connect <tidb_host>:10080 -cert /path/to/client.pem -key /path/to/client-key.pem -CAfile ./ca.crt < /dev/null
    ```

-   PD

    ```sh
    openssl s_client -connect <pd_host>:2379 -cert /path/to/client.pem -key /path/to/client-key.pem -CAfile ./ca.crt < /dev/null
    ```

-   ティクブ

    ```sh
    openssl s_client -connect <tikv_host>:20160 -cert /path/to/client.pem -key /path/to/client-key.pem -CAfile ./ca.crt < /dev/null
    ```

-   TiFlash (v4.0.5 の新機能)

    ```sh
    openssl s_client -connect <tiflash_host>:<tiflash_port> -cert /path/to/client.pem -key /path/to/client-key.pem -CAfile ./ca.crt < /dev/null
    ```

-   TiProxy

    ```sh
    openssl s_client -connect <tiproxy_host>:3080 -cert /path/to/client.pem -key /path/to/client-key.pem -CAfile ./ca.crt < /dev/null
    ```

## 証明書を再読み込みする {#reload-certificates}

-   TiDB クラスターがローカル データ センターに展開されている場合、証明書とキーを再ロードするために、TiDB、PD、TiKV、 TiFlash、TiCDC、およびすべての種類のクライアントは、新しい接続が作成されるたびに、TiDB クラスターを再起動せずに現在の証明書とキー ファイルを再読み取ります。

-   TiProxy は 1 時間に 1 回、ディスクから証明書を再読み込みします。

-   TiDB クラスタを自社マネージドクラウドにデプロイしている場合は、TLS 証明書の発行がクラウドプロバイダーの証明書管理サービスと統合されていることを確認してください。TiDB、PD、TiKV、 TiFlash、および TiCDC コンポーネントの TLS 証明書は、TiDB クラスタを再起動することなく自動的にローテーションできます。

## 証明書の有効期限 {#certificate-validity}

TiDBクラスタ内の各コンポーネントのTLS証明書の有効期間をカスタマイズできます。例えば、OpenSSLを使用してTLS証明書を発行・生成する場合、 **days**パラメータを使用して有効期間を設定できます。詳細については、 [自己署名証明書を生成する](/generate-self-signed-certificates.md)参照してください。

## 参照 {#see-also}

-   [TiDBクライアントとサーバー間のTLSを有効にする](/enable-tls-between-clients-and-servers.md)
