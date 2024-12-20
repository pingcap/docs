---
title: TiCDC Client Authentication
summary: コマンドライン ツールまたは OpenAPI を使用して TiCDC クライアント認証を実行する方法を紹介します。
---

# TiCDC クライアント認証 {#ticdc-client-authentication}

v8.1.0 以降、TiCDC は Mutual Transport Layer Security (mTLS) または TiDB ユーザー名とパスワードを使用したクライアント認証をサポートします。

-   mTLS 認証はトランスポートレイヤーでのセキュリティ制御を提供し、TiCDC がクライアント ID を検証できるようにします。
-   TiDB のユーザー名とパスワードの認証により、アプリケーションレイヤーでセキュリティ制御が提供され、許可されたユーザーのみが TiCDC ノードを通じてログインできるようになります。

これら 2 つの認証方法は、さまざまなシナリオやセキュリティ要件を満たすために、単独でも組み合わせても使用できます。

> **注記：**
>
> ネットワーク アクセスのセキュリティを確保するため、 [TLSが有効になっています](/enable-tls-between-clients-and-servers.md)場合にのみ TiCDC クライアント認証を使用することを強くお勧めします。TLS が有効になっていないと、ユーザー名とパスワードがネットワーク上でプレーンテキストとして送信され、重大な資格情報漏洩につながる可能性があります。

## クライアント認証にmTLSを使用する {#use-mtls-for-client-authentication}

1.  TiCDCサーバーで、 `security.mtls`パラメータを`true`に設定して、mTLS 認証を有効にします。

    ```toml
    [security]
    # This parameter controls whether to enable the TLS client authentication. The default value is false.
    mtls = true
    ```

2.  クライアント証明書を構成します。

    <SimpleTab groupId="cdc">
     <div label="TiCDC command-line tool" value="cdc-cli">

    [TiCDC コマンドラインツール](/ticdc/ticdc-manage-changefeed.md)を使用する場合、次の方法でクライアント証明書を指定できます。TiCDC は次の順序でクライアント証明書の読み取りを試みます。

    1.  コマンドラインパラメータ`--cert`と`--key`使用して、証明書と秘密キーを指定します。サーバーが自己署名証明書を使用する場合は、パラメータ`--ca`を使用して信頼できる CA 証明書も指定する必要があります。

        ```bash
        cdc cli changefeed list --cert client.crt --key client.key --ca ca.crt
        ```

    2.  環境変数`TICDC_CERT_PATH` `TICDC_CA_PATH`使用して`TICDC_KEY_PATH`証明書、秘密鍵、CA 証明書へのパスを指定します。

        ```bash
        export TICDC_CERT_PATH=client.crt
        export TICDC_KEY_PATH=client.key
        export TICDC_CA_PATH=ca.crt
        ```

    3.  共有資格情報ファイル`~/.ticdc/credentials`を使用して証明書を指定します。 `cdc cli configure-credentials`コマンドを使用して設定を変更できます。

    </div>

    <div label="TiCDC OpenAPI" value="cdc-api">

    [TiCDC オープンAPI](/ticdc/ticdc-open-api-v2.md)使用する場合、 `--cert`と`--key`使用してクライアント証明書と秘密鍵を指定できます。サーバーが自己署名証明書を使用する場合は、 `--cacert`パラメータを使用して信頼できる CA 証明書も指定する必要があります。例:

    ```bash
    curl -X GET http://127.0.0.1:8300/api/v2/status --cert client.crt --key client.key --cacert ca.crt
    ```

    </div>
     </SimpleTab>

## クライアント認証にTiDBのユーザー名とパスワードを使用する {#use-tidb-username-and-password-for-client-authentication}

1.  [ユーザーを作成する](/sql-statements/sql-statement-create-user.md) TiDB に追加し、ユーザーに TiCDC ノードからログインする権限を付与します。

    ```sql
    CREATE USER 'test'@'ticdc_ip_address' IDENTIFIED BY 'password';
    ```

2.  TiCDCサーバーで、ユーザー名とパスワードの認証を有効にするために`security.client-user-required`と`security.client-allowed-user`設定します。

    ```toml
    [security]
    # This parameter controls whether to use username and password for client authentication. The default value is false.
    client-user-required = true
    # This parameter lists the usernames that are allowed for client authentication. Authentication requests with usernames not in this list will be rejected. The default value is null.
    client-allowed-user = ["test"]
    ```

3.  手順 1 で作成したユーザーのユーザー名とパスワードを指定します。

    <SimpleTab groupId="cdc">
     <div label="TiCDC command-line tool" value="cdc-cli">

    [TiCDC コマンドラインツール](/ticdc/ticdc-manage-changefeed.md)を使用する場合、次の方法でユーザー名とパスワードを指定できます。TiCDC は次の順序でクライアント証明書の読み取りを試みます。

    1.  コマンドラインパラメータ`--user`と`--password`使用してユーザー名とパスワードを指定します。

        ```bash
        cdc cli changefeed list --user test --password password
        ```

    2.  コマンドラインパラメータ`--user`を使用してユーザー名を指定します。次に、ターミナルにパスワードを入力します。

        ```bash
        cdc cli changefeed list --user test
        ```

    3.  環境変数`TICDC_USER`と`TICDC_PASSWORD`使用してユーザー名とパスワードを指定します。

        ```bash
        export TICDC_USER=test
        export TICDC_PASSWORD=password
        ```

    4.  共有資格情報ファイル`~/.ticdc/credentials`を使用してユーザー名とパスワードを指定します。 `cdc cli configure-credentials`コマンドを使用して設定を変更できます。

    </div>

    <div label="TiCDC OpenAPI" value="cdc-api">

    [TiCDC オープンAPI](/ticdc/ticdc-open-api-v2.md)使用する場合は、 `--user <user>:<password>`使用してユーザー名とパスワードを指定できます。例:

    ```bash
    curl -X GET http://127.0.0.1:8300/api/v2/status --user test:password
    ```

    </div>
     </SimpleTab>
