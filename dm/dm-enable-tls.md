---
title: Enable TLS for DM Connections
summary: Learn how to enable TLS for DM connections.
---

# DM接続のTLSを有効にする {#enable-tls-for-dm-connections}

このドキュメントでは、DM-master、DM-worker、およびdmctlコンポーネント間の接続、DMとアップストリームまたはダウンストリームデータベース間の接続など、DM接続の暗号化されたデータ送信を有効にする方法について説明します。

## DM-master、DM-worker、およびdmctl間の暗号化されたデータ送信を有効にする {#enable-encrypted-data-transmission-between-dm-master-dm-worker-and-dmctl}

このセクションでは、DM-master、DM-worker、およびdmctl間の暗号化されたデータ送信を有効にする方法を紹介します。

### 暗号化されたデータ送信を構成して有効にする {#configure-and-enable-encrypted-data-transmission}

1.  証明書を準備します。

    DM-masterとDM-workerのサーバー証明書を別々に準備することをお勧めします。 2つのコンポーネントが相互に認証できることを確認してください。 dmctlの1つのクライアント証明書を共有することを選択できます。

    自己署名証明書を生成するには、 `openssl` 、および`cfssl`に基づく他のツール（ `openssl`など）を使用でき`easy-rsa` 。

    `openssl`を選択すると、 [自己署名証明書の生成](/dm/dm-generate-self-signed-certificates.md)を参照できます。

2.  証明書を構成します。

    > **ノート：**
    >
    > 同じ証明書のセットを使用するようにDM-master、DM-worker、およびdmctlを構成できます。

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

        DMクラスタで暗号化された送信を有効にした後、dmctlを使用してクラスタに接続する必要がある場合は、クライアント証明書を指定します。例えば：

        {{< copyable "" >}}

        ```bash
        ./dmctl --master-addr=127.0.0.1:8261 --ssl-ca /path/to/ca.pem --ssl-cert /path/to/client-cert.pem --ssl-key /path/to/client-key.pem
        ```

### コンポーネントの呼び出し元のIDを確認する {#verify-component-caller-s-identity}

共通名は、発信者の確認に使用されます。一般に、呼び出し先は、呼び出し元から提供されたキー、証明書、およびCAの確認に加えて、呼び出し元のIDを確認する必要があります。たとえば、DM-workerにはDM-masterのみがアクセスでき、他の訪問者は正当な証明書を持っていてもブロックされます。

コンポーネントの呼び出し元のIDを確認するには、証明書の生成時に`Common Name` （CN）を使用して証明書のユーザーIDをマークし、呼び出し先の`Common Name`リストを構成して呼び出し元のIDを確認する必要があります。

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

### 証明書をリロードします {#reload-certificates}

証明書とキーを再ロードするために、DM-master、DM-worker、およびdmctlは、新しい接続が作成されるたびに、現在の証明書とキーファイルを再読み取りします。

`ssl-ca` 、または`ssl-cert`で指定されたファイルが更新されたら、DMコンポーネントを再始動して、証明書とキー・ファイルを再`ssl-key`し、相互に再接続します。

## DMコンポーネントとアップストリームまたはダウンストリームデータベース間の暗号化されたデータ送信を有効にする {#enable-encrypted-data-transmission-between-dm-components-and-the-upstream-or-downstream-database}

このセクションでは、DMコンポーネントとアップストリームまたはダウンストリームデータベース間の暗号化されたデータ送信を有効にする方法を紹介します。

### アップストリームデータベースの暗号化されたデータ送信を有効にする {#enable-encrypted-data-transmission-for-upstream-database}

1.  アップストリームデータベースを構成し、暗号化サポートを有効にして、サーバー証明書を設定します。詳細な操作については、 [暗号化された接続の使用](https://dev.mysql.com/doc/refman/5.7/en/using-encrypted-connections.html)を参照してください。

2.  ソース構成ファイルにMySQLクライアント証明書を設定します。

    > **ノート：**
    >
    > すべてのDM-masterおよびDM-workerコンポーネントが、指定されたパスを介して証明書とキーファイルを読み取れることを確認してください。

    ```yaml
    from:
        security:
            ssl-ca: "/path/to/mysql-ca.pem"
            ssl-cert: "/path/to/mysql-cert.pem"
            ssl-key: "/path/to/mysql-key.pem"
    ```

### ダウンストリームTiDBの暗号化されたデータ送信を有効にする {#enable-encrypted-data-transmission-for-downstream-tidb}

1.  暗号化された接続を使用するようにダウンストリームTiDBを構成します。詳細な操作については、 [安全な接続を使用するようにTiDBサーバーを構成する](/enable-tls-between-clients-and-servers.md#configure-tidb-server-to-use-secure-connections)を参照してください。

2.  タスク構成ファイルにTiDBクライアント証明書を設定します。

    > **ノート：**
    >
    > すべてのDM-masterおよびDM-workerコンポーネントが、指定されたパスを介して証明書とキーファイルを読み取れることを確認してください。

    ```yaml
    target-database:
        security:
            ssl-ca: "/path/to/tidb-ca.pem"
            ssl-cert: "/path/to/tidb-client-cert.pem"
            ssl-key: "/path/to/tidb-client-key.pem"
    ```
