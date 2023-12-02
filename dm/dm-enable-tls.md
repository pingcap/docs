---
title: Enable TLS for DM Connections
summary: Learn how to enable TLS for DM connections.
---

# DM 接続の TLS を有効にする {#enable-tls-for-dm-connections}

このドキュメントでは、DM 接続 (DM マスター、DM ワーカー、および dmctl コンポーネント間の接続、および DM とアップストリームまたはダウンストリーム データベース間の接続を含む) で暗号化されたデータ送信を有効にする方法について説明します。

## DM マスター、DM ワーカー、および dmctl 間の暗号化されたデータ送信を有効にする {#enable-encrypted-data-transmission-between-dm-master-dm-worker-and-dmctl}

このセクションでは、DM マスター、DM ワーカー、および dmctl の間で暗号化されたデータ送信を有効にする方法を紹介します。

### 暗号化されたデータ送信を構成して有効にする {#configure-and-enable-encrypted-data-transmission}

1.  証明書を準備します。

    サーバー証明書はDM-masterとDM-workerで別々に用意することを推奨します。 2 つのコンポーネントが相互に認証できることを確認してください。 dmctl に対して 1 つのクライアント証明書を共有することを選択できます。

    自己署名証明書を生成するには、 `openssl` 、 `cfssl` 、および`easy-rsa`などの`openssl`に基づくその他のツールを使用できます。

    `openssl`を選択すると[自己署名証明書の生成](/dm/dm-generate-self-signed-certificates.md)を参照できます。

2.  証明書を構成します。

    > **注記：**
    >
    > 同じ証明書セットを使用するように DM マスター、DM ワーカー、および dmctl を構成できます。

    -   DMマスター

        構成ファイルまたはコマンドライン引数で構成します。

        ```toml
        ssl-ca = "/path/to/ca.pem"
        ssl-cert = "/path/to/master-cert.pem"
        ssl-key = "/path/to/master-key.pem"
        ```

    -   DMワーカー

        構成ファイルまたはコマンドライン引数で構成します。

        ```toml
        ssl-ca = "/path/to/ca.pem"
        ssl-cert = "/path/to/worker-cert.pem"
        ssl-key = "/path/to/worker-key.pem"
        ```

    -   dmctl

        DM クラスターで暗号化送信を有効にした後、dmctl を使用してクラスターに接続する必要がある場合は、クライアント証明書を指定します。例えば：

        ```bash
        ./dmctl --master-addr=127.0.0.1:8261 --ssl-ca /path/to/ca.pem --ssl-cert /path/to/client-cert.pem --ssl-key /path/to/client-key.pem
        ```

### コンポーネントの呼び出し元の身元を確認する {#verify-component-caller-s-identity}

共通名は発信者の確認に使用されます。一般に、呼び出し先は、呼び出し元が提供したキー、証明書、および CA の検証に加えて、呼び出し元の ID を検証する必要があります。たとえば、DM ワーカーには DM マスターのみがアクセスでき、他の訪問者は正規の証明書を持っていてもブロックされます。

コンポーネントの呼び出し元の ID を検証するには、証明書の生成時に`Common Name` (CN) を使用して証明書ユーザー ID をマークし、呼び出し先の`Common Name`リストを構成して呼び出し元の ID を確認する必要があります。

-   DMマスター

    構成ファイルまたはコマンドライン引数で構成します。

    ```toml
    cert-allowed-cn = ["dm"]
    ```

-   DMワーカー

    構成ファイルまたはコマンドライン引数で構成します。

    ```toml
    cert-allowed-cn = ["dm"]
    ```

### 証明書をリロードする {#reload-certificates}

証明書とキーをリロードするには、新しい接続が作成されるたびに、DM マスター、DM ワーカー、および dmctl が現在の証明書とキー ファイルを再読み込みします。

`ssl-ca` `ssl-cert`または`ssl-key`で指定されたファイルが更新されたら、DM コンポーネントを再起動して証明書とキー ファイルをリロードし、相互に再接続します。

## DM コンポーネントと上流または下流のデータベース間の暗号化されたデータ送信を有効にする {#enable-encrypted-data-transmission-between-dm-components-and-the-upstream-or-downstream-database}

このセクションでは、DM コンポーネントとアップストリームまたはダウンストリームのデータベース間の暗号化されたデータ送信を有効にする方法を紹介します。

### 上流データベースの暗号化されたデータ送信を有効にする {#enable-encrypted-data-transmission-for-upstream-database}

1.  アップストリーム データベースを構成し、暗号化サポートを有効にし、サーバー証明書を設定します。詳しい操作方法は[暗号化された接続の使用](https://dev.mysql.com/doc/refman/8.0/en/using-encrypted-connections.html)を参照してください。

2.  ソース構成ファイルに MySQL クライアント証明書を設定します。

    > **注記：**
    >
    > すべての DM マスター コンポーネントと DM ワーカー コンポーネントが、指定されたパスを介して証明書とキー ファイルを読み取ることができることを確認してください。

    ```yaml
    from:
        security:
            ssl-ca: "/path/to/mysql-ca.pem"
            ssl-cert: "/path/to/mysql-cert.pem"
            ssl-key: "/path/to/mysql-key.pem"
    ```

### ダウンストリーム TiDB の暗号化データ送信を有効にする {#enable-encrypted-data-transmission-for-downstream-tidb}

1.  暗号化された接続を使用するようにダウンストリーム TiDB を構成します。詳しい操作については[安全な接続を使用するように TiDBサーバーを構成する](/enable-tls-between-clients-and-servers.md#configure-tidb-server-to-use-secure-connections)を参照してください。

2.  タスク構成ファイルに TiDB クライアント証明書を設定します。

    > **注記：**
    >
    > すべての DM マスター コンポーネントと DM ワーカー コンポーネントが、指定されたパスを介して証明書とキー ファイルを読み取ることができることを確認してください。

    ```yaml
    target-database:
        security:
            ssl-ca: "/path/to/tidb-ca.pem"
            ssl-cert: "/path/to/tidb-client-cert.pem"
            ssl-key: "/path/to/tidb-client-key.pem"
    ```
