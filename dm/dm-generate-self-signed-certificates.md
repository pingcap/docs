---
title: Generate Self-signed Certificates
summary: Use `openssl` to generate self-signed certificates.
---

# 自己署名証明書を生成する {#generate-self-signed-certificates}

このドキュメントでは、 `openssl`を使用して自己署名証明書を生成する例を示します。要求に応じて、要件を満たす証明書とキーを生成することもできます。

インスタンスクラスタのトポロジが次のとおりであると想定します。

| 名前    | ホストIP        | サービス       |
| ----- | ------------ | ---------- |
| node1 | 172.16.10.11 | DM-master1 |
| node2 | 172.16.10.12 | DM-master2 |
| node3 | 172.16.10.13 | DM-master3 |
| node4 | 172.16.10.14 | DM-worker1 |
| node5 | 172.16.10.15 | DM-worker2 |
| node6 | 172.16.10.16 | DM-worker3 |

## OpenSSLをインストールします {#install-openssl}

-   DebianまたはUbuntuOSの場合：

    {{< copyable "" >}}

    ```bash
    apt install openssl
    ```

-   RedHatまたはCentOSOSの場合：

    {{< copyable "" >}}

    ```bash
    yum install openssl
    ```

インストールについては、OpenSSLの公式[ドキュメントをダウンロード](https://www.openssl.org/source/)を参照することもできます。

## CA証明書を生成する {#generate-the-ca-certificate}

認証局（CA）は、デジタル証明書を発行する信頼できるエンティティです。実際には、管理者に連絡して証明書を発行するか、信頼できるCAを使用してください。 CAは複数の証明書ペアを管理します。ここでは、次のように元の証明書のペアを生成するだけで済みます。

1.  CAキーを生成します。

    {{< copyable "" >}}

    ```bash
    openssl genrsa -out ca-key.pem 4096
    ```

2.  CA証明書を生成します。

    {{< copyable "" >}}

    ```bash
    openssl req -new -x509 -days 1000 -key ca-key.pem -out ca.pem
    ```

3.  CA証明書を検証します。

    {{< copyable "" >}}

    ```bash
    openssl x509 -text -in ca.pem -noout
    ```

## 個々のコンポーネントの証明書を発行します {#issue-certificates-for-individual-components}

### クラスタで使用される可能性のある証明書 {#certificates-that-might-be-used-in-the-cluster}

-   DMマスターが他のコンポーネントのDMマスターを認証するために使用する`master`の証明書。
-   DM-workerが他のコンポーネントのDM-workerを認証するために使用する`worker`の証明書。
-   DM-masterおよびDM-workerのクライアントを認証するためにdmctlによって使用される`client`の証明書。

### DMマスターの証明書を発行する {#issue-certificates-for-dm-master}

DMマスターインスタンスに証明書を発行するには、次の手順を実行します。

1.  証明書に対応する秘密鍵を生成します。

    {{< copyable "" >}}

    ```bash
    openssl genrsa -out master-key.pem 2048
    ```

2.  OpenSSL構成テンプレートファイルのコピーを作成します（複数の場所がある可能性があるため、テンプレートファイルの実際の場所を参照してください）。

    {{< copyable "" >}}

    ```bash
    cp /usr/lib/ssl/openssl.cnf .
    ```

    実際の場所がわからない場合は、ルートディレクトリで探してください。

    ```bash
    find / -name openssl.cnf
    ```

3.  `openssl.cnf`を編集し、 `[ req ]`フィールドの下に`req_extensions = v3_req`を追加し、 `[ v3_req ]`フィールドの下に`subjectAltName = @alt_names`を追加します。最後に、新しいフィールドを作成し、上記のクラスタトポロジの説明に従って`Subject Alternative Name` （SAN）の情報を編集します。

    ```
    [ alt_names ]
    IP.1 = 127.0.0.1
    IP.2 = 172.16.10.11
    IP.3 = 172.16.10.12
    IP.4 = 172.16.10.13
    ```

    SANの次のチェック項目が現在サポートされています。

    -   `IP`

    -   `DNS`

    -   `URI`

    > **ノート：**
    >
    > `0.0.0.0`などの特殊なIPを接続や通信に使用する場合は、 `alt_names`にも追加する必要があります。

4.  `openssl.cnf`のファイルを保存し、証明書要求ファイルを生成します。（ `Common Name (e.g. server FQDN or YOUR name) []:`に入力を与える場合、 `dm`などの共通名（CN）を証明書に割り当てます。これはサーバーがクライアントのIDを検証するために使用します。それぞれコンポーネントはデフォルトでは検証を有効にしません。構成ファイルで有効にできます。）

    {{< copyable "" >}}

    ```bash
    openssl req -new -key master-key.pem -out master-cert.pem -config openssl.cnf
    ```

5.  証明書を発行して生成します。

    {{< copyable "" >}}

    ```bash
    openssl x509 -req -days 365 -CA ca.pem -CAkey ca-key.pem -CAcreateserial -in master-cert.pem -out master-cert.pem -extensions v3_req -extfile openssl.cnf
    ```

6.  証明書にSANフィールドが含まれていることを確認します（オプション）。

    {{< copyable "" >}}

    ```bash
    openssl x509 -text -in master-cert.pem -noout
    ```

7.  次のファイルが現在のディレクトリに存在することを確認します。

    ```
    ca.pem
    master-cert.pem
    master-key.pem
    ```

> **ノート：**
>
> DM-workerインスタンスの証明書を発行するプロセスも同様であり、このドキュメントでは繰り返されません。

### クライアントの証明書を発行します（dmctl） {#issue-certificates-for-the-client-dmctl}

クライアント（dmctl）に証明書を発行するには、次の手順を実行します。

1.  証明書に対応する秘密鍵を生成します。

    {{< copyable "" >}}

    ```bash
    openssl genrsa -out client-key.pem 2048
    ```

2.  証明書要求ファイルを生成します（このステップでは、サーバーがクライアントのIDを検証できるようにするために使用される共通名を証明書に割り当てることもできます。各コンポーネントはデフォルトで検証を有効にせず、有効にすることができます構成ファイル内）：

    {{< copyable "" >}}

    ```bash
    openssl req -new -key client-key.pem -out client-cert.pem
    ```

3.  証明書を発行して生成します。

    {{< copyable "" >}}

    ```bash
    openssl x509 -req -days 365 -CA ca.pem -CAkey ca-key.pem -CAcreateserial -in client-cert.pem -out client-cert.pem
    ```
