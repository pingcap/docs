---
title: Generate Self-signed Certificates
summary: Use `openssl` to generate self-signed certificates.
---

# 証明書を生成する {#generate-self-signed-certificates}

> **ノート：**
>
> クライアントとサーバー間でTLSを有効にするには、 `auto-tls`を設定するだけです。

このドキュメントでは、 `openssl`を使用して自己署名証明書を生成する例を示します。要求に応じて、要件を満たす証明書とキーを生成することもできます。

インスタンスクラスタのトポロジは次のとおりであると想定します。

| 名前    | ホストIP        | サービス      |
| ----- | ------------ | --------- |
| node1 | 172.16.10.11 | PD1、TiDB1 |
| node2 | 172.16.10.12 | PD2       |
| node3 | 172.16.10.13 | PD3       |
| node4 | 172.16.10.14 | TiKV1     |
| node5 | 172.16.10.15 | TiKV2     |
| node6 | 172.16.10.16 | TiKV3     |

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

認証局（CA）は、デジタル証明書を発行する信頼できるエンティティです。実際には、管理者に連絡して証明書を発行するか、信頼できるCAを使用してください。 CAは複数の証明書ペアを管理します。ここでは、次のように証明書の元のペアを生成するだけで済みます。

1.  ルートキーを生成します。

    {{< copyable "" >}}

    ```bash
    openssl genrsa -out root.key 4096
    ```

2.  ルート証明書を生成します。

    {{< copyable "" >}}

    ```bash
    openssl req -new -x509 -days 1000 -key root.key -out root.crt
    ```

3.  ルート証明書を検証します。

    {{< copyable "" >}}

    ```bash
    openssl x509 -text -in root.crt -noout
    ```

## 個々のコンポーネントの証明書を発行する {#issue-certificates-for-individual-components}

このセクションでは、個々のコンポーネントの証明書を発行する方法について説明します。

### クラスタで使用される可能性のある証明書 {#certificates-that-might-be-used-in-the-cluster}

-   tidb-server証明書：他のコンポーネントおよびクライアントのTiDBを認証するためにTiDBによって使用されます
-   tikv-server証明書：他のコンポーネントおよびクライアントのTiKVを認証するためにTiKVによって使用されます
-   pd-server証明書：PDが他のコンポーネントやクライアントのPDを認証するために使用します
-   クライアント証明書：PD、TiKV、TiDBからクライアントを認証するために使用され`tikv-ctl` （ `pd-ctl`など）。

### TiKVインスタンスに証明書を発行します {#issue-certificates-to-tikv-instances}

TiKVインスタンスに証明書を発行するには、次の手順を実行します。

1.  証明書に対応する秘密鍵を生成します。

    {{< copyable "" >}}

    ```bash
    openssl genrsa -out tikv.key 2048
    ```

2.  OpenSSL構成テンプレートファイルのコピーを作成します（テンプレートファイルには複数の場所がある可能性があるため、テンプレートファイルの実際の場所を参照してください）。

    {{< copyable "" >}}

    ```bash
    cp /usr/lib/ssl/openssl.cnf .
    ```

    実際の場所がわからない場合は、ルートディレクトリで探してください。

    ```bash
    find / -name openssl.cnf
    ```

3.  `openssl.cnf`を編集し、 `[ req ]`フィールドの下に`req_extensions = v3_req`を追加し、 `[ v3_req ]`フィールドの下に`subjectAltName = @alt_names`を追加します。最後に、新しいフィールドを作成し、SANの情報を編集します。

    ```
    [ alt_names ]
    IP.1 = 127.0.0.1
    IP.2 = 172.16.10.14
    IP.3 = 172.16.10.15
    IP.4 = 172.16.10.16
    ```

4.  `openssl.cnf`のファイルを保存し、証明書要求ファイルを生成します（このステップでは、サーバーがクライアントのIDを検証できるようにするために使用される、証明書に共通名を割り当てることもできます。各コンポーネントは、デフォルトであり、構成ファイルで有効にできます）：

    {{< copyable "" >}}

    ```bash
    openssl req -new -key tikv.key -out tikv.csr -config openssl.cnf
    ```

5.  証明書を発行して生成します。

    {{< copyable "" >}}

    ```bash
    openssl x509 -req -days 365 -CA root.crt -CAkey root.key -CAcreateserial -in tikv.csr -out tikv.crt -extensions v3_req -extfile openssl.cnf
    ```

6.  証明書にSANフィールドが含まれていることを確認します（オプション）。

    {{< copyable "" >}}

    ```bash
    openssl x509 -text -in tikv.crt -noout
    ```

7.  次のファイルが現在のディレクトリに存在することを確認します。

    ```
    root.crt
    tikv.crt
    tikv.key
    ```

他のTiDBコンポーネントの証明書を発行するプロセスも同様であり、このドキュメントでは繰り返されません。

### クライアントに証明書を発行する {#issue-certificates-for-clients}

クライアントに証明書を発行するには、次の手順を実行します。

1.  証明書に対応する秘密鍵を生成します。

    {{< copyable "" >}}

    ```bash
    openssl genrsa -out client.key 2048
    ```

2.  証明書要求ファイルを生成します（このステップでは、サーバーがクライアントのIDを検証できるようにするために使用される共通名を証明書に割り当てることもできます。各コンポーネントはデフォルトで検証を有効にせず、有効にすることができます構成ファイルにあります）：

    {{< copyable "" >}}

    ```bash
    openssl req -new -key client.key -out client.csr
    ```

3.  証明書を発行して生成します。

    {{< copyable "" >}}

    ```bash
    openssl x509 -req -days 365 -CA root.crt -CAkey root.key -CAcreateserial -in client.csr -out client.crt
    ```
