---
title: Generate Self-signed Certificates
summary: Use `openssl` to generate self-signed certificates.
---

# 証明書を生成する {#generate-self-signed-certificates}

> **注記：**
>
> クライアントとサーバーの間で TLS を有効にするには、 `auto-tls`を設定するだけです。

このドキュメントでは、 `openssl`を使用して自己署名証明書を生成する例を示します。必要に応じて、要件を満たす証明書とキーを生成することもできます。

インスタンス クラスターのトポロジが次のとおりであると仮定します。

| 名前   | ホストIP        | サービス      |
| ---- | ------------ | --------- |
| ノード1 | 172.16.10.11 | PD1、TiDB1 |
| ノード2 | 172.16.10.12 | PD2       |
| ノード3 | 172.16.10.13 | PD3       |
| ノード4 | 172.16.10.14 | TiKV1     |
| ノード5 | 172.16.10.15 | TiKV2     |
| ノード6 | 172.16.10.16 | TiKV3     |

## OpenSSL をインストールする {#install-openssl}

-   Debian または Ubuntu OS の場合:

    ```bash
    apt install openssl
    ```

-   RedHat または CentOS OS の場合:

    ```bash
    yum install openssl
    ```

インストールについては、OpenSSL の公式[ドキュメントをダウンロードする](https://www.openssl.org/source/)を参照することもできます。

## CA証明書を生成する {#generate-the-ca-certificate}

認証局 (CA) は、デジタル証明書を発行する信頼できるエンティティです。実際には、管理者に連絡して証明書を発行するか、信頼できる CA を使用してください。 CA は複数の証明書ペアを管理します。ここで必要なのは、次のように元の証明書のペアを生成することだけです。

1.  ルートキーを生成します。

    ```bash
    openssl genrsa -out root.key 4096
    ```

2.  ルート証明書を生成します。

    ```bash
    openssl req -new -x509 -days 1000 -key root.key -out root.crt
    ```

3.  ルート証明書を検証します。

    ```bash
    openssl x509 -text -in root.crt -noout
    ```

## 個々のコンポーネントの証明書を発行する {#issue-certificates-for-individual-components}

このセクションでは、個々のコンポーネントの証明書を発行する方法について説明します。

### クラスターで使用される可能性のある証明書 {#certificates-that-might-be-used-in-the-cluster}

-   tidb-server 証明書: 他のコンポーネントおよびクライアントに対して TiDB を認証するために TiDB によって使用されます。
-   tikv-server 証明書: 他のコンポーネントおよびクライアントに対して TiKV を認証するために TiKV によって使用されます。
-   pd-server 証明書: 他のコンポーネントおよびクライアントに対して PD を認証するために PD によって使用されます。
-   クライアント証明書: PD、TiKV、TiDB からクライアントを認証するために使用されます ( `pd-ctl` 、 `tikv-ctl`など)。

### TiKV インスタンスに証明書を発行する {#issue-certificates-to-tikv-instances}

TiKV インスタンスに証明書を発行するには、次の手順を実行します。

1.  証明書に対応する秘密キーを生成します。

    ```bash
    openssl genrsa -out tikv.key 2048
    ```

2.  OpenSSL 構成テンプレート ファイルのコピーを作成します (複数の場所がある場合があるため、テンプレート ファイルの実際の場所を参照してください)。

    ```bash
    cp /usr/lib/ssl/openssl.cnf .
    ```

    実際の場所がわからない場合は、ルート ディレクトリで探してください。

    ```bash
    find / -name openssl.cnf
    ```

3.  `openssl.cnf`を編集し、 `[ req ]`フィールドの下に`req_extensions = v3_req`追加し、 `[ v3_req ]`フィールドの下に`subjectAltName = @alt_names`を追加します。最後に、新しいフィールドを作成し、SAN の情報を編集します。

        [ alt_names ]
        IP.1 = 127.0.0.1
        IP.2 = 172.16.10.14
        IP.3 = 172.16.10.15
        IP.4 = 172.16.10.16

4.  `openssl.cnf`ファイルを保存し、証明書要求ファイルを生成します (この手順では、サーバーがクライアントの ID を検証できるようにするために使用される共通名を証明書に割り当てることもできます。各コンポーネントは、次のような検証を有効にしません)デフォルトであり、構成ファイルで有効にすることができます):

    ```bash
    openssl req -new -key tikv.key -out tikv.csr -config openssl.cnf
    ```

5.  証明書を発行して生成します。

    ```bash
    openssl x509 -req -days 365 -CA root.crt -CAkey root.key -CAcreateserial -in tikv.csr -out tikv.crt -extensions v3_req -extfile openssl.cnf
    ```

6.  証明書に SAN フィールドが含まれていることを確認します (オプション)。

    ```bash
    openssl x509 -text -in tikv.crt -noout
    ```

7.  現在のディレクトリに次のファイルが存在することを確認します。

        root.crt
        tikv.crt
        tikv.key

他の TiDB コンポーネントの証明書を発行するプロセスも同様であるため、このドキュメントでは繰り返しません。

### クライアントに証明書を発行する {#issue-certificates-for-clients}

クライアントに証明書を発行するには、次の手順を実行します。

1.  証明書に対応する秘密キーを生成します。

    ```bash
    openssl genrsa -out client.key 2048
    ```

2.  証明書要求ファイルを生成します (この手順では、サーバーがクライアントの ID を検証できるようにするために使用される共通名を証明書に割り当てることもできます。各コンポーネントはデフォルトでは検証を有効にしませんが、有効にすることができます)構成ファイル内にあります):

    ```bash
    openssl req -new -key client.key -out client.csr
    ```

3.  証明書を発行して生成します。

    ```bash
    openssl x509 -req -days 365 -CA root.crt -CAkey root.key -CAcreateserial -in client.csr -out client.crt
    ```
