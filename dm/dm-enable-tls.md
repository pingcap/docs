---
title: Enable TLS for DM Connections
summary: DM 接続で TLS を有効にする方法を学習します。
---

# DM接続にTLSを有効にする {#enable-tls-for-dm-connections}

このドキュメントでは、DM マスター、DM ワーカー、dmctl コンポーネント間の接続、および DM と上流または下流のデータベース間の接続を含む、DM 接続の暗号化されたデータ転送を有効にする方法について説明します。

## DMマスター、DMワーカー、dmctl間の暗号化されたデータ転送を有効にする {#enable-encrypted-data-transmission-between-dm-master-dm-worker-and-dmctl}

このセクションでは、DM マスター、DM ワーカー、dmctl 間の暗号化されたデータ転送を有効にする方法を紹介します。

### 暗号化されたデータ転送を設定して有効にする {#configure-and-enable-encrypted-data-transmission}

1.  証明書を準備します。

    DM-master と DM-worker のサーバー証明書を別々に用意することをお勧めします。2 つのコンポーネントが相互に認証できることを確認してください。dmctl のクライアント証明書を 1 つ共有することもできます。

    自己署名証明書を生成するには、 `openssl` 、 `cfssl`および`easy-rsa`などの`openssl`に基づいた他のツールを使用できます。

    `openssl`選択した場合は[自己署名証明書の生成](/dm/dm-generate-self-signed-certificates.md)を参照できます。

2.  証明書を構成します。

    > **注記：**
    >
    > DM-master、DM-worker、および dmctl が同じ証明書セットを使用するように構成できます。

    -   DMマスター

        設定ファイルまたはコマンドライン引数で設定します。

        ```toml
        ssl-ca = "/path/to/ca.pem"
        ssl-cert = "/path/to/master-cert.pem"
        ssl-key = "/path/to/master-key.pem"
        ```

    -   DMワーカー

        設定ファイルまたはコマンドライン引数で設定します。

        ```toml
        ssl-ca = "/path/to/ca.pem"
        ssl-cert = "/path/to/worker-cert.pem"
        ssl-key = "/path/to/worker-key.pem"
        ```

    -   dmctl

        DM クラスターで暗号化された送信を有効にした後、dmctl を使用してクラスターに接続する必要がある場合は、クライアント証明書を指定します。例:

        ```bash
        ./dmctl --master-addr=127.0.0.1:8261 --ssl-ca /path/to/ca.pem --ssl-cert /path/to/client-cert.pem --ssl-key /path/to/client-key.pem
        ```

### コンポーネント呼び出し元のIDを確認する {#verify-component-caller-s-identity}

共通名は、発信者の検証に使用されます。通常、着信側は、発信者が提供するキー、証明書、および CA を検証するだけでなく、発信者の ID も検証する必要があります。たとえば、DM-worker には DM-master のみがアクセスでき、他の訪問者は正当な証明書を持っていてもブロックされます。

コンポーネントの呼び出し元の ID を確認するには、証明書を生成するときに`Common Name` (CN) を使用して証明書のユーザー ID をマークし、呼び出し先の`Common Name`リストを構成して呼び出し元の ID を確認する必要があります。

-   DMマスター

    設定ファイルまたはコマンドライン引数で設定します。

    ```toml
    cert-allowed-cn = ["dm"]
    ```

-   DMワーカー

    設定ファイルまたはコマンドライン引数で設定します。

    ```toml
    cert-allowed-cn = ["dm"]
    ```

### 証明書を再読み込みする {#reload-certificates}

証明書とキーを再ロードするために、DM-master、DM-worker、および dmctl は、新しい接続が作成されるたびに現在の証明書とキー ファイルを再読み取りします。

`ssl-ca` 、または`ssl-cert`で指定されたファイルが更新`ssl-key`れた場合は、DM コンポーネントを再起動して証明書とキー ファイルを再読み込みし、相互に再接続します。

## DMコンポーネントと上流または下流のデータベース間の暗号化されたデータ転送を有効にする {#enable-encrypted-data-transmission-between-dm-components-and-the-upstream-or-downstream-database}

このセクションでは、DM コンポーネントと上流または下流のデータベース間の暗号化されたデータ転送を有効にする方法について説明します。

### 上流データベースへの暗号化されたデータ転送を有効にする {#enable-encrypted-data-transmission-for-upstream-database}

1.  アップストリームデータベースを設定し、暗号化サポートを有効にし、サーバー証明書を設定します。詳細な操作については、 [暗号化された接続の使用](https://dev.mysql.com/doc/refman/8.0/en/using-encrypted-connections.html)参照してください。

2.  ソース構成ファイルで MySQL クライアント証明書を設定します。

    > **注記：**
    >
    > すべての DM マスターおよび DM ワーカー コンポーネントが指定されたパスを介して証明書とキー ファイルを読み取ることができることを確認します。

    ```yaml
    from:
        security:
            ssl-ca: "/path/to/mysql-ca.pem"
            ssl-cert: "/path/to/mysql-cert.pem"
            ssl-key: "/path/to/mysql-key.pem"
    ```

### 下流のTiDBへの暗号化されたデータ転送を有効にする {#enable-encrypted-data-transmission-for-downstream-tidb}

1.  暗号化された接続を使用するようにダウンストリーム TiDB を構成します。詳細な操作については、 [安全な接続を使用するように TiDBサーバーを構成する](/enable-tls-between-clients-and-servers.md#configure-tidb-server-to-use-secure-connections)を参照してください。

2.  タスク構成ファイルで TiDB クライアント証明書を設定します。

    > **注記：**
    >
    > すべての DM マスターおよび DM ワーカー コンポーネントが指定されたパスを介して証明書とキー ファイルを読み取ることができることを確認します。

    ```yaml
    target-database:
        security:
            ssl-ca: "/path/to/tidb-ca.pem"
            ssl-cert: "/path/to/tidb-client-cert.pem"
            ssl-key: "/path/to/tidb-client-key.pem"
    ```
