---
title: Generate Self-signed Certificates
summary: openssl` を使用して自己署名証明書を生成します。
---

# 証明書を生成する {#generate-self-signed-certificates}

> **注記：**
>
> クライアントとサーバー間の TLS を有効にするには、 `auto-tls`設定するだけです。

このドキュメントでは、 `openssl`使用して自己署名証明書を生成する例を示します。また、必要に応じて要件を満たす証明書とキーを生成することもできます。

インスタンス クラスターのトポロジが次のとおりであると仮定します。

| 名前   | ホストIP        | サービス      |
| ---- | ------------ | --------- |
| ノード1 | 172.16.10.11 | PD1、TiDB1 |
| ノード2 | 172.16.10.12 | PD2       |
| ノード3 | 172.16.10.13 | PD3       |
| ノード4 | 172.16.10.14 | ティクV1     |
| ノード5 | 172.16.10.15 | ティクV2     |
| ノード6 | 172.16.10.16 | ティクV3     |

## OpenSSLをインストールする {#install-openssl}

-   Debian または Ubuntu OS の場合:

    ```bash
    apt install openssl
    ```

-   RedHat または CentOS OS の場合:

    ```bash
    yum install openssl
    ```

インストールについては OpenSSL の公式[ドキュメントをダウンロード](https://www.openssl.org/source/)も参照してください。

## CA証明書を生成する {#generate-the-ca-certificate}

証明機関 (CA) は、デジタル証明書を発行する信頼できる機関です。実際には、管理者に連絡して証明書を発行するか、信頼できる CA を使用します。CA は複数の証明書ペアを管理します。ここでは、次のようにしてオリジナルの証明書ペアを生成するだけです。

1.  ルートキーを生成します:

    ```bash
    openssl genrsa -out root.key 4096
    ```

2.  ルート証明書を生成します:

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

-   tidb-server 証明書: TiDB が他のコンポーネントやクライアントに対して TiDB を認証するために使用します。
-   tikv-server 証明書: TiKV が他のコンポーネントやクライアントに対して TiKV を認証するために使用します。
-   pd-server 証明書: PD が他のコンポーネントやクライアントに対して PD を認証するために使用します。
-   クライアント証明書: PD、TiKV、TiDBからのクライアントの認証に使用されます（ `pd-ctl`など`tikv-ctl` 。

### TiKVインスタンスに証明書を発行する {#issue-certificates-to-tikv-instances}

TiKV インスタンスに証明書を発行するには、次の手順を実行します。

1.  証明書に対応する秘密鍵を生成します。

    ```bash
    openssl genrsa -out tikv.key 2048
    ```

2.  OpenSSL 構成テンプレート ファイルのコピーを作成します (テンプレート ファイルは複数の場所にある可能性があるため、実際の場所を参照してください)。

    ```bash
    cp /usr/lib/ssl/openssl.cnf .
    ```

    実際の場所がわからない場合は、ルート ディレクトリで探します。

    ```bash
    find / -name openssl.cnf
    ```

3.  `openssl.cnf`編集し、 `[ req ]`フィールドの下に`req_extensions = v3_req`を追加し、 `[ v3_req ]`フィールドの下に`subjectAltName = @alt_names`を追加します。最後に、新しいフィールドを作成し、SAN の情報を編集します。

        [ alt_names ]
        IP.1 = 127.0.0.1
        IP.2 = 172.16.10.14
        IP.3 = 172.16.10.15
        IP.4 = 172.16.10.16

4.  `openssl.cnf`ファイルを保存し、証明書要求ファイルを生成します (この手順では、証明書に共通名を割り当てることもできます。共通名は、サーバーがクライアントの ID を検証するために使用されます。各コンポーネントは、デフォルトでは検証を有効にしていませんが、構成ファイルで有効にすることができます)。

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

1.  証明書に対応する秘密鍵を生成します。

    ```bash
    openssl genrsa -out client.key 2048
    ```

2.  証明書要求ファイルを生成します (この手順では、証明書に共通名を割り当てることもできます。共通名は、サーバーがクライアントの ID を検証するために使用されます。各コンポーネントはデフォルトで検証を有効にしませんが、構成ファイルで有効にすることができます)。

    ```bash
    openssl req -new -key client.key -out client.csr
    ```

3.  証明書を発行して生成します。

    ```bash
    openssl x509 -req -days 365 -CA root.crt -CAkey root.key -CAcreateserial -in client.csr -out client.crt
    ```
